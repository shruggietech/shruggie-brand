#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for source-bound identity approval and promotion."""

from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from identity_continuity import (  # noqa: E402
    ContinuityError,
    PROOF_SIZES,
    PROOF_SURFACES,
    REQUIRED_APPROVAL_SCOPE,
    canonical_digest,
    canonical_source_binding,
    compare_proofs,
    identity_snapshot,
    measured_oklch,
    palette_roles,
    record_digest,
    safe_path,
    validate_glyphkit_helper,
    validate_lifecycle_transition,
    validate_palette_qualification,
    validate_current_proof_matrix,
    validate_continuity_report,
    validate_record,
    write_continuity_report,
)
from promote_identity import PromotionError, promote  # noqa: E402


def brand_fixture():
    return {
        "slug": "example",
        "wordmark_text": "Example",
        "affiliation": {"showcase": "private"},
        "accent": {"bright": "#62BEB2", "deep": "#005D55", "accessible": "#005D55"},
        "surfaces": {"base": "#080A14", "light": "#F7F8FC"},
        "typography": {"mode": "house"},
        "logo": {
            "source_mode": "constructed",
            "geometry_provenance": "glyphkit",
            "grid": 512,
            "canvas_width": 512,
            "canvas_height": 512,
            "artwork_width": 320,
            "artwork_height": 320,
            "clear_space_units": 48,
            "standalone_padding_units": {"full": 96, "reduced": 104},
            "role_colors": {"dark": {"accent": "#62BEB2", "ink": "#F7F8FC"}},
            "paths": {
                "full": [{"role": "accent", "d": "M96 96 L416 96 L416 416 L96 416 Z"}],
                "reduced": [{"role": "accent", "d": "M112 112 L400 112 L400 400 L112 400 Z"}],
            },
        },
    }


def palette_qualification(brand=None):
    brand = brand or brand_fixture()
    roles = palette_roles(identity_snapshot(brand, "glyphkit-constructed")["palette"])
    evidence = {
        "status": "passed",
        "srgb_roles": roles,
        "oklch_roles": {role: measured_oklch(color) for role, color in roles.items()},
        "checks": {
            "contrast": True,
            "sibling_separation": True,
            "color_vision": True,
            "semantic_roles": True,
            "surfaces": True,
            "single_ink": True,
            "rendered_color": True,
        },
    }
    evidence["evidence_sha256"] = canonical_digest(evidence)
    return evidence


def historical_record(brand, root, source_class="legacy-constructed"):
    snapshot = identity_snapshot(brand, source_class)
    record = {
        "schema_version": 1,
        "brand": brand["slug"],
        "status": "historical-baseline",
        "source_class": source_class,
        "recorded_on": "2026-09-09",
        "source_revision": "011f35303ef1d555dbbbcf6708447cc321df40db",
        "source_files": [],
        "identity_snapshot": snapshot,
        "topology": snapshot["topology"],
        "framing": snapshot["framing"],
        "palette": snapshot["palette"],
        "renderer": None,
        "proofs": [],
        "approval": None,
        "historical_evidence": {
            "basis": "current-authoritative-source",
            "baseline_revision": "011f35303ef1d555dbbbcf6708447cc321df40db",
            "approval_completeness": "unknown",
            "limitation": "Records current source and does not claim retrospective owner approval.",
            "migration_issue": 185,
        },
    }
    record["record_sha256"] = record_digest(record)
    return record


def transparent_proof(path, size=64, shift=0, hole=False, color=(98, 190, 178, 255)):
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    inset = max(3, size // 4)
    draw.rounded_rectangle(
        (inset + shift, inset, size - inset + shift - 1, size - inset - 1),
        radius=max(1, size // 12),
        fill=color,
    )
    if hole:
        cut = max(1, size // 10)
        cx = size // 2 + shift
        cy = size // 2
        draw.rectangle((cx - cut, cy - cut, cx + cut, cy + cut), fill=(0, 0, 0, 0))
    image.save(path)


_PROOF_ARTIFACT_CACHE = {}


def proof_artifact_bytes(size):
    if size not in _PROOF_ARTIFACT_CACHE:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proof = root / "proof.png"
            transparent_proof(proof, size=size)
            result = compare_proofs(proof, proof, same_renderer=True, evidence_dir=root / "evidence",
                                    prefix="comparison")
            _PROOF_ARTIFACT_CACHE[size] = {
                "proof": proof.read_bytes(),
                "evidence": {kind: (root / "evidence" / filename).read_bytes()
                             for kind, filename in result["evidence_paths"].items()},
            }
    return _PROOF_ARTIFACT_CACHE[size]


class IdentityContinuityTests(unittest.TestCase):
    def make_promotion_bundle(self, root):
        approval = root / "approval"
        source = approval / "source"
        brands = root / "brands"
        (source / "build").mkdir(parents=True)
        (source / "proofs").mkdir()
        brands.mkdir()
        brand = brand_fixture()
        brand["identity_continuity"] = {"record": "identity-continuity.json", "status": "approved-canonical"}
        brand["approval_ledger"] = {"gate_1": {"canonical_source_sha256": "pending"}}
        brand_bytes = (json.dumps(brand, indent=2) + "\n").encode("utf-8")
        (source / "brand.json").write_bytes(brand_bytes)
        helper_bytes = b'import glyphkit as G\nfull=[{"role":"accent","d":G.rect(0,0,1,1)}]\nreduced=full\n'
        (source / "build" / "mk_paths.py").write_bytes(helper_bytes)
        proofs = []
        for variant in ("full", "reduced"):
            for size in PROOF_SIZES:
                for surface in PROOF_SURFACES:
                    relative = "proofs/%s-%s-%s.png" % (variant, size, surface)
                    artifacts = proof_artifact_bytes(size)
                    (source / relative).write_bytes(artifacts["proof"])
                    payload = artifacts["proof"]
                    evidence = {}
                    for kind, evidence_payload in artifacts["evidence"].items():
                        evidence_relative = "evidence/%s-%s-%s-%s.png" % (variant, size, surface, kind)
                        evidence_path = source / evidence_relative
                        evidence_path.parent.mkdir(exist_ok=True)
                        evidence_path.write_bytes(evidence_payload)
                        evidence[kind] = {"path": evidence_relative,
                                          "sha256": canonical_digest(evidence_payload)}
                    proofs.append({"variant": variant, "size_px": size, "surface": surface,
                                   "path": relative, "sha256": canonical_digest(payload),
                                   "evidence": evidence})
        snapshot = identity_snapshot(brand, "glyphkit-constructed")
        qualification = palette_qualification(brand)
        record = {
            "schema_version": 1, "brand": "example", "status": "approved-canonical",
            "source_class": "glyphkit-constructed", "recorded_on": "2026-09-09",
            "source_revision": "approved-test-source",
            "source_files": [
                {"path": "brand.json", "purpose": "canonical brand source", "bytes": len(brand_bytes),
                 "sha256": canonical_digest(brand_bytes)},
                {"path": "build/mk_paths.py", "purpose": "identity construction source", "bytes": len(helper_bytes),
                 "sha256": canonical_digest(helper_bytes)},
            ],
            "identity_snapshot": snapshot, "topology": snapshot["topology"],
            "framing": snapshot["framing"], "palette": snapshot["palette"],
            "renderer": {"id": "test-renderer", "version": "1", "settings_sha256": canonical_digest({"scale": 1})},
            "proofs": proofs,
            "approval": {"bundle_id": "example-canonical-r1", "approved_by": "owner",
                         "approved_on": "2026-09-09", "owner_wording": "approved",
                         "scope": list(REQUIRED_APPROVAL_SCOPE), "proposal_sha256": "a" * 64,
                         "source_snapshot_sha256": snapshot["sha256"]},
            "historical_evidence": None, "palette_qualification": qualification,
            "record_sha256": "",
        }
        brand["approval_ledger"]["gate_1"]["canonical_source_sha256"] = canonical_source_binding(record)
        brand_bytes = (json.dumps(brand, indent=2) + "\n").encode("utf-8")
        (source / "brand.json").write_bytes(brand_bytes)
        record["source_files"][0].update({"bytes": len(brand_bytes), "sha256": canonical_digest(brand_bytes)})
        record["record_sha256"] = record_digest(record)
        record_bytes = (json.dumps(record, indent=2) + "\n").encode("utf-8")
        (source / "identity-continuity.json").write_bytes(record_bytes)
        bundle = {
            "schema_version": 1, "source_root": "source", "record_path": "identity-continuity.json",
            "record_file_sha256": canonical_digest(record_bytes), "record_sha256": "",
        }
        bundle["record_sha256"] = record_digest(bundle)
        bundle_path = approval / "bundle.json"
        bundle_path.write_text(json.dumps(bundle), encoding="utf-8")
        return approval, source, brands, bundle_path

    def test_canonical_digest_is_order_independent(self):
        self.assertEqual(canonical_digest({"b": 2, "a": 1}), canonical_digest({"a": 1, "b": 2}))
        self.assertEqual(64, len(canonical_digest({"a": "é"})))

    def test_snapshot_binds_geometry_framing_palette_and_typography(self):
        brand = brand_fixture()
        baseline = identity_snapshot(brand, "glyphkit-constructed")
        for mutation in (
            lambda value: value["logo"]["paths"]["full"][0].update({"d": "M0 0 L1 1 Z"}),
            lambda value: value["logo"].update({"artwork_width": 300}),
            lambda value: value["logo"].update({"square_enclosure": {"content_scale": 0.8}}),
            lambda value: value["accent"].update({"bright": "#FFFFFF"}),
            lambda value: value.update({"wordmark_text": "Changed"}),
        ):
            changed = copy.deepcopy(brand)
            mutation(changed)
            self.assertNotEqual(baseline["sha256"], identity_snapshot(changed, "glyphkit-constructed")["sha256"])

    def test_safe_path_rejects_escape_absolute_backslash_and_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ok.txt").write_text("ok", encoding="utf-8")
            self.assertEqual((root / "ok.txt").resolve(), safe_path(root, "ok.txt"))
            for candidate in ("../escape", "/absolute", "bad\\path"):
                with self.subTest(candidate=candidate), self.assertRaises(ContinuityError):
                    safe_path(root, candidate, required=False)
            if hasattr(os, "symlink"):
                try:
                    os.symlink(str(root / "ok.txt"), str(root / "link.txt"))
                except OSError:
                    return
                with self.assertRaises(ContinuityError):
                    safe_path(root, "link.txt")

    def test_lifecycle_rejects_direction_to_approval_and_historical_promotion(self):
        self.assertTrue(validate_lifecycle_transition("exploratory", "direction-selected"))
        self.assertTrue(validate_lifecycle_transition("canonical-approved", "promoted"))
        for current, target in (("direction-selected", "canonical-approved"),
                                ("historical-baseline", "promoted"),
                                ("invalidated", "publication-eligible")):
            with self.subTest(current=current, target=target), self.assertRaises(ContinuityError):
                validate_lifecycle_transition(current, target)

    def test_historical_record_is_valid_but_cannot_claim_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            brand = brand_fixture()
            record = historical_record(brand, Path(tmp))
            self.assertEqual("historical-baseline", validate_record(brand, Path(tmp), record)["status"])
            forged = copy.deepcopy(record)
            forged["approval"] = {"approved_by": "owner"}
            forged["record_sha256"] = record_digest(forged)
            with self.assertRaises(ContinuityError):
                validate_record(brand, Path(tmp), forged)

    def test_record_rejects_malformed_hash_duplicate_source_and_snapshot_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.svg"
            source.write_text("<svg/>", encoding="utf-8")
            brand = brand_fixture()
            record = historical_record(brand, root)
            digest = canonical_digest(source.read_bytes())
            record["source_files"] = [
                {"path": "source.svg", "purpose": "authoritative-master", "bytes": source.stat().st_size, "sha256": digest},
                {"path": "source.svg", "purpose": "duplicate", "bytes": source.stat().st_size, "sha256": digest},
            ]
            record["record_sha256"] = record_digest(record)
            with self.assertRaises(ContinuityError):
                validate_record(brand, root, record)
            record["source_files"] = []
            record["identity_snapshot"]["sha256"] = "bad"
            record["record_sha256"] = record_digest(record)
            with self.assertRaises(ContinuityError):
                validate_record(brand, root, record)

    def test_cueson_helper_uses_glyphkit_and_custom_serializer_fails(self):
        validate_glyphkit_helper(ROOT / "brands" / "cueson" / "build" / "mk_paths.py")
        with tempfile.TemporaryDirectory() as tmp:
            helper = Path(tmp) / "mk_paths.py"
            helper.write_text('import glyphkit as G\ndef band():\n    return "M0 0 L1 1 Z"\nfull=[{"role":"ink","d":band()}]\n', encoding="utf-8")
            with self.assertRaises(ContinuityError):
                validate_glyphkit_helper(helper)
            helper.write_text(
                'import glyphkit as G\ndef serialize():\n    return "".join(["M",str(0)," 0Z"])\n'
                'unused=G.rect(0,0,1,1)\nfull=[{"role":"ink","d":serialize()}]\nreduced=full\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ContinuityError, "directly from a glyphkit"):
                validate_glyphkit_helper(helper)
            helper.write_text(
                'import glyphkit as G\ndef serialize():\n    return "".join(["M",str(0)," 0Z"])\n'
                'unused=G.rect(0,0,1,1)\nentry={"role":"ink"}\nentry.update(d=serialize())\n'
                'full=[entry]\nreduced=full\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ContinuityError, "constructed d mutation"):
                validate_glyphkit_helper(helper)

    def test_palette_qualification_requires_every_check_and_bound_values(self):
        valid = palette_qualification()
        self.assertEqual("passed", validate_palette_qualification(valid)["status"])
        for mutation in (
            lambda value: value["checks"].update({"contrast": False}),
            lambda value: value["checks"].pop("color_vision"),
            lambda value: value["oklch_roles"].pop("accent.deep"),
            lambda value: value["oklch_roles"].update({"accent.deep": [1.1, 0.08, 180.0]}),
            lambda value: value.update({"evidence_sha256": "0" * 64}),
        ):
            changed = copy.deepcopy(valid)
            mutation(changed)
            with self.assertRaises(ContinuityError):
                validate_palette_qualification(changed)
        unrelated = copy.deepcopy(valid)
        unrelated["srgb_roles"] = {"unrelated": "#000000"}
        unrelated["oklch_roles"] = {"unrelated": measured_oklch("#000000")}
        unrelated["evidence_sha256"] = canonical_digest({key: value for key, value in unrelated.items()
                                                          if key != "evidence_sha256"})
        governed = identity_snapshot(brand_fixture(), "glyphkit-constructed")["palette"]
        with self.assertRaisesRegex(ContinuityError, "governed identity palette"):
            validate_palette_qualification(unrelated, governed)

    def test_cueson_equivalent_renderer_fixture_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            approved = root / "approved.png"
            production = root / "production.png"
            transparent_proof(approved)
            transparent_proof(production)
            result = compare_proofs(approved, production, same_renderer=False, evidence_dir=root / "evidence")
            self.assertTrue(result["passes"], result)
            self.assertEqual(0, result["changed_outside_edge_fraction"])
            self.assertEqual({"side_by_side", "overlay", "silhouette_xor", "color_difference"}, set(result["evidence_paths"]))

    def test_cueson_reconstruction_and_framing_drift_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            approved = root / "approved.png"
            production = root / "production.png"
            transparent_proof(approved)
            transparent_proof(production, shift=4, hole=True)
            result = compare_proofs(approved, production, same_renderer=False)
            self.assertFalse(result["passes"])
            self.assertNotEqual(result["approved_topology"], result["production_topology"])

    def test_same_renderer_requires_exact_file_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            approved = root / "approved.png"
            production = root / "production.png"
            transparent_proof(approved)
            transparent_proof(production)
            self.assertTrue(compare_proofs(approved, production, same_renderer=True)["passes"])
            image = Image.open(production).convert("RGBA")
            image.putpixel((0, 0), (0, 0, 0, 1))
            image.save(production)
            self.assertFalse(compare_proofs(approved, production, same_renderer=True)["passes"])

    def test_color_and_new_hole_fail_cross_renderer_comparison(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            approved = root / "approved.png"
            production = root / "production.png"
            transparent_proof(approved)
            transparent_proof(production, hole=True, color=(255, 0, 0, 255))
            result = compare_proofs(approved, production, same_renderer=False)
            self.assertFalse(result["passes"])
            self.assertGreater(result["interior_delta_e_2000"], 1.0)

    def test_proof_comparison_rejects_non_png_or_non_square_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            approved = root / "approved.png"
            production = root / "production.png"
            Image.new("RGBA", (64, 32), (0, 0, 0, 0)).save(approved)
            Image.new("RGBA", (64, 32), (0, 0, 0, 0)).save(production)
            with self.assertRaisesRegex(ContinuityError, "square"):
                compare_proofs(approved, production, same_renderer=False)
            Image.new("RGB", (64, 64), (255, 255, 255)).save(production.with_suffix(".jpg"))
            with self.assertRaisesRegex(ContinuityError, "PNG"):
                compare_proofs(approved, production.with_suffix(".jpg"), same_renderer=False)

    def test_proof_matrix_coordinates_are_complete(self):
        expected = {(variant, size, surface) for variant in ("full", "reduced")
                    for size in PROOF_SIZES for surface in PROOF_SURFACES}
        self.assertEqual(32, len(expected))

    def test_canonical_record_rejects_proof_with_wrong_dimensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _approval, source, _brands, _bundle_path = self.make_promotion_bundle(root)
            record_path = source / "identity-continuity.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            proof = record["proofs"][0]
            proof_path = source / proof["path"]
            transparent_proof(proof_path, size=17)
            proof["sha256"] = canonical_digest(proof_path.read_bytes())
            record["record_sha256"] = record_digest(record)
            with self.assertRaisesRegex(ContinuityError, "dimensions"):
                validate_record(json.loads((source / "brand.json").read_text(encoding="utf-8")), source, record,
                                verify_proof_files=True)

    def test_current_proof_matrix_requires_bound_settings_and_exact_implementation_renders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _approval, source, _brands, _bundle_path = self.make_promotion_bundle(root)
            record = json.loads((source / "identity-continuity.json").read_text(encoding="utf-8"))
            generated = source / "qc" / "identity-continuity-proofs"
            generated.mkdir(parents=True)
            for item in record["proofs"]:
                target = generated / ("%s-%d-%s.png" % (item["variant"], item["size_px"], item["surface"]))
                target.write_bytes((source / item["path"]).read_bytes())
            result = validate_current_proof_matrix(record, source, renderer=record["renderer"])
            self.assertEqual("passed", result["status"])
            host_version = dict(record["renderer"], version="host-version")
            result = validate_current_proof_matrix(record, source, renderer=host_version)
            self.assertTrue(all(item["comparison"]["same_renderer"] for item in result["proofs"]))
            equivalent = dict(record["renderer"], id="equivalent-renderer", version="2")
            result = validate_current_proof_matrix(record, source, renderer=equivalent)
            self.assertTrue(all(not item["comparison"]["same_renderer"] for item in result["proofs"]))
            with self.assertRaisesRegex(ContinuityError, "renderer"):
                validate_current_proof_matrix(record, source, renderer={"id": "changed", "version": "1",
                                                                       "settings_sha256": "0" * 64})
            first = generated / "full-256-dark.png"
            first.write_bytes(first.read_bytes() + b"drift")
            with self.assertRaisesRegex(ContinuityError, "proof drift"):
                validate_current_proof_matrix(record, source, renderer=record["renderer"])

    def test_approved_report_binds_fresh_production_proof_matrix(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _approval, source, _brands, _bundle_path = self.make_promotion_bundle(root)
            record = json.loads((source / "identity-continuity.json").read_text(encoding="utf-8"))
            generated = source / "qc" / "identity-continuity-proofs"
            generated.mkdir(parents=True)
            for item in record["proofs"]:
                target = generated / ("%s-%d-%s.png" % (item["variant"], item["size_px"], item["surface"]))
                target.write_bytes((source / item["path"]).read_bytes())
            with mock.patch("identity_continuity.generate_current_proofs"), \
                    mock.patch("identity_continuity.production_renderer_contract", return_value=record["renderer"]):
                report = write_continuity_report(
                    json.loads((source / "brand.json").read_text(encoding="utf-8")), source
                )
                self.assertEqual(32, len(report["proof_validation"]["proofs"]))
                self.assertEqual(report, validate_continuity_report(
                    json.loads((source / "brand.json").read_text(encoding="utf-8")), source
                ))

    def test_promotion_copies_exact_bytes_and_refuses_existing_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            approval, source, brands, bundle_path = self.make_promotion_bundle(root)
            payload = (source / "brand.json").read_bytes()
            result = promote(bundle_path, approval, brands)
            self.assertEqual(payload, (brands / "example" / "brand.json").read_bytes())
            self.assertEqual((source / "identity-continuity.json").read_bytes(),
                             (brands / "example" / "identity-continuity.json").read_bytes())
            self.assertEqual("promoted", result["result"])
            with self.assertRaises(PromotionError):
                promote(bundle_path, approval, brands)

    def test_promotion_rejects_escape_stale_hash_generated_path_and_symlink(self):
        for mutation in ("escape", "stale", "generated", "undeclared", "executable", "symlink"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                approval, source, brands, bundle_path = self.make_promotion_bundle(root)
                bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                record_path = source / "identity-continuity.json"
                record = json.loads(record_path.read_text(encoding="utf-8"))
                if mutation == "escape":
                    bundle["source_root"] = "../escape"
                elif mutation == "stale":
                    bundle["record_file_sha256"] = "0" * 64
                elif mutation == "generated":
                    record["source_files"][0]["path"] = "proofs/brand.png"
                    record["record_sha256"] = record_digest(record)
                    record_path.write_text(json.dumps(record), encoding="utf-8")
                    bundle["record_file_sha256"] = canonical_digest(record_path.read_bytes())
                elif mutation == "undeclared":
                    (source / "surprise.txt").write_text("undeclared", encoding="utf-8")
                elif mutation == "executable":
                    payload = b"blocked"
                    (source / "helper.exe").write_bytes(payload)
                    record["source_files"].append({"path": "helper.exe", "purpose": "bad", "bytes": len(payload),
                                                   "sha256": canonical_digest(payload)})
                    record["record_sha256"] = record_digest(record)
                    record_path.write_text(json.dumps(record), encoding="utf-8")
                    bundle["record_file_sha256"] = canonical_digest(record_path.read_bytes())
                else:
                    try:
                        os.symlink(str(source / "brand.json"), str(source / "link.json"))
                    except OSError:
                        continue
                bundle["record_sha256"] = record_digest(bundle)
                bundle_path.write_text(json.dumps(bundle), encoding="utf-8")
                with self.assertRaises(PromotionError):
                    promote(bundle_path, approval, brands)

    def test_replacement_rolls_back_after_partial_install_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            approval, _source, brands, bundle_path = self.make_promotion_bundle(root)
            destination = brands / "example"
            destination.mkdir()
            (destination / "sentinel.txt").write_text("last known good", encoding="utf-8")
            real_replace = os.replace
            calls = []

            def fail_install(source, target):
                calls.append((source, target))
                if len(calls) == 2:
                    raise OSError("simulated install failure")
                return real_replace(source, target)

            with mock.patch("promote_identity.os.replace", side_effect=fail_install):
                with self.assertRaisesRegex(PromotionError, "rolled back"):
                    promote(bundle_path, approval, brands, replace=True)
            self.assertEqual("last known good", (destination / "sentinel.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
