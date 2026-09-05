#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Focused regressions for the ownership-neutral authoritative-input contract."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from brand_contract import ContractError, SERVICE_CREDIT, _font_metadata, affiliation_text, analyze_authoritative_inputs, scan_affiliation_output, sha256_file, validate_brand
from ingest_font import ingest_font


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def owned_brand():
    return {
        "slug": "example",
        "kind": "sub-brand",
        "affiliation": {
            "ownership": "shruggietech-owned",
            "showcase": "public",
            "parent": "ShruggieTech",
            "inheritance": "shruggietech-house",
            "endorsement": "shruggietech-project",
            "service_credit": "none",
        },
        "typography": {
            "mode": "house",
            "families": {
                "display": {"name": "Space Grotesk", "weights": [500, 700]},
                "body": {"name": "Geist", "weights": [400, 500]},
                "mono": {"name": "Geist Mono", "weights": [400]},
            },
        },
        "accent": {"bright": "#2BCC73", "deep": "#00AB21", "accessible": "#037B40"},
        "logo": {"paths": {"full": [{"d": "M0 0H1V1Z", "role": "accent"}], "reduced": []}},
    }


def stage_house_fonts(kit):
    shutil.copytree(ROOT / "assets" / "fonts", kit / "fonts")


class AffiliationTests(unittest.TestCase):
    def test_missing_affiliation_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            stage_house_fonts(kit)
            brand = owned_brand()
            del brand["affiliation"]
            with self.assertRaisesRegex(ContractError, "affiliation is required"):
                validate_brand(brand, kit)

    def test_third_party_has_no_owned_parent_or_default_credit(self):
        brand = owned_brand()
        brand["affiliation"] = {"ownership": "third-party", "showcase": "private", "parent": None, "inheritance": "independent", "endorsement": "none", "service_credit": "none"}
        brand["semantic_colors"] = {"emphasis": "#6750A4", "action": "#5B3F98"}
        self.assertEqual("", affiliation_text(brand))
        brand["affiliation"]["service_credit"] = "brand-system-by-shruggietech"
        self.assertEqual(SERVICE_CREDIT, affiliation_text(brand))
        brand["affiliation"]["parent"] = "ShruggieTech"
        with self.assertRaisesRegex(ContractError, "cannot declare"):
            affiliation_text(brand)

    def test_independent_inheritance_requires_semantic_colors(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            stage_house_fonts(kit)
            brand = owned_brand()
            brand["affiliation"] = {"ownership": "third-party", "showcase": "private", "parent": None, "inheritance": "independent", "endorsement": "none", "service_credit": "none"}
            with self.assertRaisesRegex(ContractError, "independent inheritance requires"):
                validate_brand(brand, kit)

    def test_output_scan_finds_owned_claims_for_third_party(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            brand = owned_brand()
            brand["affiliation"] = {"ownership": "third-party", "showcase": "public", "parent": None, "inheritance": "independent", "endorsement": "none", "service_credit": "none"}
            brand["semantic_colors"] = {"emphasis": "#6750A4", "action": "#5B3F98"}
            (kit / "README.md").write_text("A ShruggieTech project\n", encoding="utf-8")
            self.assertEqual(1, len(scan_affiliation_output(brand, kit)))
            (kit / "README.md").write_text("Brand system by ShruggieTech\n", encoding="utf-8")
            self.assertEqual(1, len(scan_affiliation_output(brand, kit)))


class AuthoritativeInputTests(unittest.TestCase):
    def make_raster_brand(self, kit):
        stage_house_fonts(kit)
        assets = kit / "assets"
        assets.mkdir()
        image = Image.new("RGBA", (3, 2))
        image.putdata([(43, 204, 115, 255), (43, 204, 115, 255), (255, 255, 255, 0), (0, 171, 33, 255), (43, 204, 115, 128), (0, 171, 33, 255)])
        source = assets / "mark.png"
        image.save(source)
        brand = owned_brand()
        brand["logo"]["paths"]["full"] = [{"element": "image", "source": "assets/mark.png", "mask": "alpha", "x": 0, "y": 0, "width": 3, "height": 2}]
        brand["authoritative_inputs"] = [{
            "id": "master-mark", "role": "mark", "path": "assets/mark.png", "format": "png",
            "sha256": sha256_file(source), "color_profile": "unknown", "usage_status": "approved",
            "license": "Test fixture", "approved_transformations": ["embed-unchanged", "recolor-mask", "palette-analysis"],
        }]
        brand["palette_approvals"] = [{
            "input_id": "master-mark", "source_sha256": sha256_file(source), "selected_candidate": "#2BCC73",
            "canonical_tokens": ["accent.bright"], "approved_by": "human-test-operator", "approved_on": "2026-09-05",
        }]
        return brand, source

    def test_raster_analysis_is_deterministic_and_ignores_alpha_zero(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            brand, source = self.make_raster_brand(kit)
            before = source.read_bytes()
            first = validate_brand(brand, kit)
            second = analyze_authoritative_inputs(brand, kit)
            self.assertEqual(first, second)
            self.assertEqual(before, source.read_bytes())
            self.assertEqual(1, first[0]["transparent_samples_ignored"])
            self.assertEqual("#2BCC73", first[0]["candidates"][0]["hex"])

    def test_hash_drift_and_stale_approval_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            brand, source = self.make_raster_brand(kit)
            stale = copy.deepcopy(brand)
            stale["palette_approvals"][0]["source_sha256"] = "0" * 64
            with self.assertRaisesRegex(ContractError, "stale"):
                validate_brand(stale, kit)
            source.write_bytes(source.read_bytes() + b"drift")
            with self.assertRaisesRegex(ContractError, "hash drift"):
                validate_brand(brand, kit)

    def test_svg_active_content_external_reference_and_live_text_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            stage_house_fonts(kit)
            source = kit / "mark.svg"
            cases = {
                "active content": ('<script>alert(1)</script>', "prohibited"),
                "external reference": ('<image href="https://example.test/mark.png"/>', "external reference"),
                "live text": ("<text>Mutable wordmark</text>", "prohibited"),
            }
            for label, (content, message) in cases.items():
                with self.subTest(label=label):
                    source.write_text('<svg xmlns="http://www.w3.org/2000/svg">%s<path fill="#112233" d="M0 0Z"/></svg>\n' % content, encoding="utf-8")
                    brand = owned_brand()
                    brand["authoritative_inputs"] = [{"id": "svg-mark", "role": "mark", "path": "mark.svg", "format": "svg", "sha256": sha256_file(source), "color_profile": "none", "usage_status": "approved", "license": "Test fixture", "approved_transformations": []}]
                    with self.assertRaisesRegex(ContractError, message):
                        validate_brand(brand, kit)

    def test_authoritative_input_path_escape_and_role_collision_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            kit = root / "kit"
            kit.mkdir()
            stage_house_fonts(kit)
            outside = root / "outside.svg"
            outside.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path fill="#112233" d="M0 0Z"/></svg>\n', encoding="utf-8")
            record = {"id": "svg-mark", "role": "mark", "path": "../outside.svg", "format": "svg", "sha256": sha256_file(outside), "color_profile": "none", "usage_status": "approved", "license": "Test fixture", "approved_transformations": []}
            brand = owned_brand()
            brand["authoritative_inputs"] = [record]
            with self.assertRaisesRegex(ContractError, "escapes"):
                validate_brand(brand, kit)

            first = kit / "first.svg"
            second = kit / "second.svg"
            shutil.copy2(outside, first)
            shutil.copy2(outside, second)
            first_record = dict(record, id="first-mark", path="first.svg")
            second_record = dict(record, id="second-mark", path="second.svg")
            brand["authoritative_inputs"] = [first_record, second_record]
            with self.assertRaisesRegex(ContractError, "duplicate authoritative input role"):
                validate_brand(brand, kit)

    def test_imported_logo_requires_declared_recolor_operation(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            brand, _ = self.make_raster_brand(kit)
            brand["authoritative_inputs"][0]["approved_transformations"].remove("recolor-mask")
            with self.assertRaisesRegex(ContractError, "does not approve"):
                validate_brand(brand, kit)


class FixedFontTests(unittest.TestCase):
    def fixed_brand(self, kit):
        sources = {
            "display": ROOT / "assets" / "fonts" / "ttf" / "SpaceGrotesk-Medium.ttf",
            "body": ROOT / "assets" / "fonts" / "ttf" / "Geist-Regular.ttf",
            "mono": ROOT / "assets" / "fonts" / "ttf" / "GeistMono-Regular.ttf",
        }
        expected = {"display": ("Space Grotesk", 500), "body": ("Geist", 400), "mono": ("Geist Mono", 400)}
        faces = []
        for role, source in sources.items():
            target = kit / "fonts" / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            family, weight = expected[role]
            faces.append({"role": role, "path": "fonts/%s" % source.name, "weight": weight, "style": "normal", "format": "ttf", "sha256": sha256_file(target), "license": "OFL-1.1", "provenance": "Repository licensed test face", "usage_status": "approved"})
        brand = owned_brand()
        brand["typography"] = {"mode": "fixed", "families": {role: {"name": expected[role][0], "weights": [expected[role][1]]} for role in ("display", "body", "mono")}, "faces": faces}
        return brand

    def test_fixed_fonts_validate_measured_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            brand = self.fixed_brand(kit)
            validate_brand(brand, kit)
            brand["typography"]["families"]["body"]["name"] = "Wrong Family"
            with self.assertRaisesRegex(ContractError, "family mismatch"):
                validate_brand(brand, kit)

    def assert_fixed_font_error(self, mutation, message):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            brand = self.fixed_brand(kit)
            mutation(brand, kit)
            with self.assertRaisesRegex(ContractError, message):
                validate_brand(brand, kit)

    @staticmethod
    def body_face(brand):
        return next(face for face in brand["typography"]["faces"] if face["role"] == "body")

    def test_fixed_fonts_reject_missing_face_wrong_weight_bad_style_and_hash_drift(self):
        self.assert_fixed_font_error(
            lambda brand, _kit: brand["typography"]["faces"].__setitem__(slice(None), [face for face in brand["typography"]["faces"] if face["role"] != "mono"]),
            "role mono needs an outline-capable",
        )

        def wrong_weight(brand, _kit):
            brand["typography"]["families"]["body"]["weights"] = [500]
            self.body_face(brand)["weight"] = 500

        self.assert_fixed_font_error(wrong_weight, "weight mismatch")
        self.assert_fixed_font_error(lambda brand, _kit: self.body_face(brand).__setitem__("style", "italic"), "style mismatch")
        self.assert_fixed_font_error(lambda brand, _kit: self.body_face(brand).__setitem__("sha256", "0" * 64), "hash drift")

    def test_fixed_fonts_reject_corrupt_and_variable_binaries(self):
        def corrupt(brand, kit):
            face = self.body_face(brand)
            path = kit / face["path"]
            path.write_bytes(b"not a font")
            face["sha256"] = sha256_file(path)

        self.assert_fixed_font_error(corrupt, "cannot read font binary")

        class VariableFont:
            def __contains__(self, key):
                return key == "fvar"

            def close(self):
                pass

        with patch("fontTools.ttLib.TTFont", return_value=VariableFont()):
            with self.assertRaisesRegex(ContractError, "variable fonts"):
                _font_metadata(Path("variable.ttf"))

    def test_atomic_local_ingestion_and_boundary(self):
        source = ROOT / "assets" / "fonts" / "ttf" / "Geist-Regular.ttf"
        woff2_source = ROOT / "assets" / "fonts" / "woff2" / "SpaceGrotesk-Medium.woff2"
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            (repo / "assets" / "fonts").mkdir(parents=True)
            target = ingest_font(str(source), "assets/fonts/client/Geist-Regular.ttf", sha256_file(source), "Geist", 400, "normal", "OFL-1.1", "Repository licensed test face", repo_root=repo)
            self.assertEqual(source.read_bytes(), target.read_bytes())
            woff2_target = ingest_font(str(woff2_source), "assets/fonts/client/SpaceGrotesk-Medium.woff2", sha256_file(woff2_source), "Space Grotesk", 500, "normal", "OFL-1.1", "Repository licensed test face", repo_root=repo)
            self.assertEqual(woff2_source.read_bytes(), woff2_target.read_bytes())
            with self.assertRaisesRegex(ContractError, "escapes"):
                ingest_font(str(source), "outside.ttf", sha256_file(source), "Geist", 400, "normal", "OFL-1.1", "Test", repo_root=repo)
            existing = target.read_bytes()
            with self.assertRaisesRegex(ContractError, "SHA-256"):
                ingest_font(str(source), "assets/fonts/client/Geist-Regular.ttf", "0" * 64, "Geist", 400, "normal", "OFL-1.1", "Test", repo_root=repo)
            self.assertEqual(existing, target.read_bytes())


if __name__ == "__main__":
    unittest.main()
