#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Focused regressions for the ownership-neutral authoritative-input contract."""

from __future__ import annotations

import copy
import base64
import hashlib
import json
import shutil
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from brand_contract import ContractError, SERVICE_CREDIT, _font_metadata, affiliation_text, analyze_authoritative_inputs, application_icon_profile, approval_ledger, canonical_gate_binding, custom_assets, derivative_configuration_sha256, guide_surface_mode, logo_source_contract, public_showcase, scan_affiliation_output, sha256_file, showcase_surface, social_copy, square_enclosure_profile, validate_brand, validate_brand_file, validate_source_inventory, validate_supplied_icon_dimensions, vendor_boundary, wordmark_role_colors
from identity_continuity import canonical_digest, identity_snapshot, record_digest
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
        "logo": {"source_mode": "constructed", "paths": {"full": [{"d": "M0 0H1V1Z", "role": "accent"}], "reduced": [{"d": "M0 0H1V1Z", "role": "accent"}]}},
    }


def stage_house_fonts(kit):
    shutil.copytree(ROOT / "assets" / "fonts", kit / "fonts")


class CustomAssetContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.kit = Path(self.temp.name)
        source = self.kit / "assets" / "source" / "sand.svg"
        source.parent.mkdir(parents=True)
        source.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path d="M0 0H10V10Z"/></svg>', encoding="utf-8")
        self.asset = {
            "id": "sand", "title": "Sand treatment", "description": "A quiet editorial treatment.",
            "role": "campaign-treatment",
            "source": {"path": "assets/source/sand.svg", "format": "svg", "sha256": sha256_file(source)},
            "provenance": {"kind": "supplied", "owner": "Brand owner", "detail": "Owner-supplied master"},
            "approval": {"status": "approved", "publication_eligible": True},
            "transformations": ["embed-unchanged"],
            "usage": {"use": "Editorial atmosphere", "avoid": "Do not replace the core logo"},
            "accessibility": {"alt": "Sand-toned decorative treatment", "legibility": "Use on a plain light well", "text_overlay": "prohibited", "reduced_motion": "not-applicable", "disclosure": "Illustration, not photography"},
            "credit": {"attribution": "Brand owner", "license": "Owner-approved brand use"},
            "preview": {"well": "light", "fit": "contain"},
        }

    def test_absent_and_valid_public_asset(self):
        self.assertEqual([], custom_assets({}, self.kit, public_only=True))
        self.assertEqual([self.asset], custom_assets({"custom_assets": [self.asset]}, self.kit, public_only=True))

    def test_private_asset_is_valid_but_not_published(self):
        item = copy.deepcopy(self.asset)
        item["approval"] = {"status": "pending", "publication_eligible": False}
        self.assertEqual([], custom_assets({"custom_assets": [item]}, self.kit, public_only=True))

    def test_bad_paths_hash_and_rights_are_rejected(self):
        for section, field, value in [
            ("source", "path", "../outside.svg"), ("source", "path", "https://example.com/sand.svg"),
            ("source", "path", "assets\\source\\sand.svg"), ("source", "path", "assets/source/absent.svg"),
            ("source", "sha256", "0" * 64), ("source", "format", "png"),
            ("provenance", "owner", ""), ("credit", "license", ""),
            ("credit", "attribution", ""), ("accessibility", "alt", ""),
        ]:
            with self.subTest(section=section, field=field, value=value):
                item = copy.deepcopy(self.asset)
                item[section][field] = value
                with self.assertRaises(ContractError):
                    custom_assets({"custom_assets": [item]}, self.kit)

    def test_duplicate_and_unapproved_public_asset_are_rejected(self):
        with self.assertRaisesRegex(ContractError, "duplicate custom asset id"):
            custom_assets({"custom_assets": [self.asset, self.asset]}, self.kit)
        second = copy.deepcopy(self.asset)
        second["id"] = "other-sand"
        with self.assertRaisesRegex(ContractError, "duplicate custom asset path"):
            custom_assets({"custom_assets": [self.asset, second]}, self.kit)
        item = copy.deepcopy(self.asset)
        item["approval"]["status"] = "pending"
        with self.assertRaisesRegex(ContractError, "cannot be public"):
            custom_assets({"custom_assets": [item]}, self.kit)

    def test_active_svg_and_symlink_escape_are_rejected(self):
        source = self.kit / self.asset["source"]["path"]
        source.write_text('<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>', encoding="utf-8")
        item = copy.deepcopy(self.asset)
        item["source"]["sha256"] = sha256_file(source)
        with self.assertRaisesRegex(ContractError, "prohibited <script>"):
            custom_assets({"custom_assets": [item]}, self.kit)
        source.unlink()
        try:
            source.symlink_to(HERE / "brand_contract.py")
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation unavailable")
        with self.assertRaisesRegex(ContractError, "symbolic-link"):
            custom_assets({"custom_assets": [self.asset]}, self.kit)

    def test_svg_motion_and_truncated_rasters_are_rejected(self):
        source = self.kit / self.asset["source"]["path"]
        for element in ("animate", "set", "animateTransform", "animateMotion", "discard"):
            with self.subTest(element=element):
                source.write_text('<svg xmlns="http://www.w3.org/2000/svg"><%s attributeName="opacity" dur="1s" repeatCount="indefinite"/></svg>' % element, encoding="utf-8")
                item = copy.deepcopy(self.asset)
                item["source"]["sha256"] = sha256_file(source)
                with self.assertRaisesRegex(ContractError, "prohibited"):
                    custom_assets({"custom_assets": [item]}, self.kit)
        for format_name, suffix, header in (("png", ".png", b"\x89PNG\r\n\x1a\n"),
                                            ("jpeg", ".jpg", b"\xff\xd8\xff"),
                                            ("webp", ".webp", b"RIFF\x04\x00\x00\x00WEBP")):
            with self.subTest(format=format_name):
                raster = source.with_suffix(suffix)
                raster.write_bytes(header)
                item = copy.deepcopy(self.asset)
                item["source"] = {"path": raster.relative_to(self.kit).as_posix(), "format": format_name,
                                  "sha256": sha256_file(raster)}
                with self.assertRaisesRegex(ContractError, "incomplete or invalid"):
                    custom_assets({"custom_assets": [item]}, self.kit)
                Image.new("RGB", (3, 2), (22, 44, 66)).save(raster, format={"png": "PNG", "jpeg": "JPEG", "webp": "WEBP"}[format_name])
                item["source"]["sha256"] = sha256_file(raster)
                self.assertEqual([item], custom_assets({"custom_assets": [item]}, self.kit, public_only=True))

    def test_every_svg_css_url_must_be_local(self):
        source = self.kit / self.asset["source"]["path"]
        for reference in ("/cursor.cur", "file:///cursor.cur", "../cursor.cur"):
            with self.subTest(reference=reference):
                source.write_text('<svg xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="paint"/></defs><rect style="fill:url(#paint);cursor:url(%s)"/></svg>' % reference, encoding="utf-8")
                item = copy.deepcopy(self.asset)
                item["source"]["sha256"] = sha256_file(source)
                with self.assertRaisesRegex(ContractError, "external paint reference"):
                    custom_assets({"custom_assets": [item]}, self.kit)
        source.write_text('<svg xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="paint"/></defs><rect style="fill:url(#paint);stroke:url(\'#paint\')"/></svg>', encoding="utf-8")
        item = copy.deepcopy(self.asset)
        item["source"]["sha256"] = sha256_file(source)
        self.assertEqual([item], custom_assets({"custom_assets": [item]}, self.kit, public_only=True))

    def test_nonpublic_sources_cannot_live_in_always_published_trees(self):
        original = self.kit / self.asset["source"]["path"]
        for relative in ("logos/private.svg", "favicons/private.svg", "icons/private.svg", "specimens/private.svg", "guidelines/private.svg", "nextjs/registry/private.svg"):
            with self.subTest(path=relative):
                source = self.kit / relative
                source.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(original, source)
                item = copy.deepcopy(self.asset)
                item["source"] = {"path": relative, "format": "svg", "sha256": sha256_file(source)}
                item["approval"] = {"status": "pending", "publication_eligible": False}
                with self.assertRaisesRegex(ContractError, "always-published source tree"):
                    custom_assets({"custom_assets": [item]}, self.kit)


def approval_brand(status="pending"):
    gate_2 = {"status": status, "approved_by": None, "approved_on": None,
              "derivative_manifest_sha256": None, "surfaces": []}
    if status == "approved":
        gate_2 = {"status": "approved", "approved_by": "owner", "approved_on": "2026-09-07",
                  "derivative_manifest_sha256": "b" * 64,
                  "surfaces": ["showcase-card", "brand-landing-page", "guideline-topics", "downloads",
                               "registry-endpoints", "public-metadata", "structured-data", "social-preview"]}
    brand = {
        "affiliation": {"ownership": "third-party", "showcase": "public", "parent": None,
                        "inheritance": "independent", "endorsement": "none", "service_credit": "none"},
        "approval_ledger": {
            "source_hashes": {"source-mark": "a" * 64},
            "gate_1": {"status": "approved", "approved_by": "owner", "approved_on": "2026-09-07",
                       "scope": sorted(["reduced-and-platform", "horizontal-lockup", "stacked-lockup", "wordmark-only", "single-ink"]),
                       "derivative_config_sha256": ""},
            "gate_2": gate_2,
        },
    }
    brand["approval_ledger"]["gate_1"]["derivative_config_sha256"] = derivative_configuration_sha256(brand)
    return brand


class ApprovalLedgerTests(unittest.TestCase):
    def test_cueson_source_preserves_exact_verbal_identity_and_approval_hashes(self):
        brand = json.loads((ROOT / "brands" / "cueson" / "brand.json").read_text(encoding="utf-8"))
        self.assertEqual("Cueson", brand["title"])
        self.assertEqual("Universal captions and subtitles", brand["brand_idea"])
        self.assertEqual(
            "A lossless, structured interchange layer for subtitle and caption content.",
            brand["descriptor"],
        )
        self.assertEqual(
            ["A lossless, structured interchange layer", "for subtitle and caption content."],
            brand["description_lines"],
        )
        self.assertEqual("shruggietech-owned", brand["affiliation"]["ownership"])
        self.assertEqual("#62BEB2", brand["accent"]["bright"])
        self.assertEqual("house", brand["typography"]["mode"])
        ledger = approval_ledger(brand, [])
        self.assertEqual(
            "4c71cbf518a6de9d8861eea203e882469461feae18f576ea03e8c435ea71ab7c",
            ledger["gate_1"]["derivative_config_sha256"],
        )
        self.assertEqual(
            "b68a1d19e1e5033c353b23807b02fbcc9486d9dd74660d5d93be42d919297451",
            ledger["gate_2"]["derivative_manifest_sha256"],
        )

    def test_constructed_identity_may_bind_gate_one_without_imported_sources(self):
        brand = approval_brand()
        brand["logo"] = {"source_mode": "constructed", "paths": {
            "full": [{"d": "M0 0 L1 0 L1 1 Z", "role": "accent"}],
            "reduced": [{"d": "M0 0 L1 0 L1 1 Z", "role": "accent"}],
        }}
        brand["approval_ledger"]["source_hashes"] = {}
        brand["approval_ledger"]["gate_1"]["derivative_config_sha256"] = derivative_configuration_sha256(brand)
        self.assertEqual({}, approval_ledger(brand, [])["source_hashes"])

        authoritative = copy.deepcopy(brand)
        authoritative["logo"]["source_mode"] = "authoritative"
        authoritative["approval_ledger"]["gate_1"]["derivative_config_sha256"] = derivative_configuration_sha256(authoritative)
        with self.assertRaisesRegex(ContractError, "constructed identity"):
            approval_ledger(authoritative, [])

        with_input = [({"id": "source-mark", "sha256": "a" * 64,
                        "usage_status": "approved", "role": "mark"}, Path("unused"))]
        with self.assertRaisesRegex(ContractError, "stale"):
            approval_ledger(brand, with_input)

    def test_approved_gate_two_cannot_hide_a_completed_brand(self):
        brand = approval_brand("approved")
        brand["affiliation"]["showcase"] = "private"
        brand["approval_ledger"]["gate_2"]["surfaces"] = []
        approved_input = [({"id": "source-mark", "sha256": "a" * 64,
                            "usage_status": "approved", "role": "mark"}, Path("unused"))]
        with self.assertRaisesRegex(ContractError, "must be published"):
            approval_ledger(brand, approved_input)

    def test_private_gate_two_is_bound_to_generated_derivative_provenance(self):
        brand = approval_brand("approved")
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            approval = kit / "logos" / "approval.json"
            approval.parent.mkdir()
            approval.write_text("{}\n", encoding="utf-8")
            brand["approval_ledger"]["gate_2"]["derivative_manifest_sha256"] = sha256_file(approval)
            self.assertTrue(public_showcase(brand, kit))
            approval.write_text('{"stale":true}\n', encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "stale"):
                public_showcase(brand, kit)

    def test_private_gate_two_accepts_canonical_manifest_with_equivalent_local_inventory(self):
        brand = approval_brand("approved")
        brand["slug"] = "sample"
        brand["approval_ledger"]["gate_1"]["derivative_config_sha256"] = (
            derivative_configuration_sha256(brand))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            kit = root / "local"
            canonical = root / "portable" / brand["slug"]
            (kit / "logos").mkdir(parents=True)
            (canonical / "logos").mkdir(parents=True)
            payload = {"schema_version": 1, "brand": brand["slug"], "derivatives": []}
            local_approval = kit / "logos" / "approval.json"
            canonical_approval = canonical / "logos" / "approval.json"
            local_approval.write_text(
                json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
            canonical_approval.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            brand["approval_ledger"]["gate_2"]["derivative_manifest_sha256"] = sha256_file(
                canonical_approval)
            with patch.dict("os.environ", {"GP_APPROVED_PROOF_ROOT": str(root / "portable")}):
                self.assertTrue(public_showcase(brand, kit))

    def test_gate_1_is_required_and_hash_bound(self):
        brand = approval_brand()
        missing = copy.deepcopy(brand)
        del missing["approval_ledger"]["gate_1"]
        with self.assertRaisesRegex(ContractError, "approval_ledger"):
            approval_ledger(missing)
        with self.assertRaisesRegex(ContractError, "stale"):
            approval_ledger(brand, [({"id": "source-mark", "sha256": "c" * 64,
                                     "usage_status": "approved", "role": "mark"}, Path("unused"))])
        changed = copy.deepcopy(brand)
        changed["logo"] = {"paths": {"single-ink": [{"d": "M0 0 L1 1"}]}}
        with self.assertRaisesRegex(ContractError, "derivative-producing configuration"):
            approval_ledger(changed)
        incomplete = copy.deepcopy(brand)
        incomplete["approval_ledger"]["gate_1"]["scope"].pop()
        with self.assertRaisesRegex(ContractError, "account for every derivative family"):
            approval_ledger(incomplete)

    def test_gate_1_can_explicitly_mark_unavailable_derivative_families(self):
        brand = approval_brand()
        brand["approval_ledger"]["gate_1"]["scope"] = [
            "horizontal-lockup", "reduced-and-platform", "stacked-lockup",
        ]
        brand["approval_ledger"]["gate_1"]["unavailable_derivatives"] = {
            "single-ink": "No monochrome source was supplied.",
            "wordmark-only": "No standalone wordmark source was supplied.",
        }
        brand["approval_ledger"]["gate_1"]["derivative_config_sha256"] = derivative_configuration_sha256(brand)
        self.assertEqual(2, len(approval_ledger(brand)["gate_1"]["unavailable_derivatives"]))
        brand["approval_ledger"]["gate_1"]["scope"].append("single-ink")
        with self.assertRaisesRegex(ContractError, "both approved and unavailable"):
            approval_ledger(brand)

    def test_publication_waits_for_gate_2(self):
        self.assertFalse(public_showcase(approval_brand("pending")))
        self.assertTrue(public_showcase(approval_brand("approved")))

    def test_publication_rejects_partial_surfaces_and_stale_derivative_provenance(self):
        brand = approval_brand("approved")
        brand["approval_ledger"]["gate_2"]["surfaces"].pop()
        with self.assertRaisesRegex(ContractError, "complete public surface"):
            public_showcase(brand)
        brand = approval_brand("approved")
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            approval = kit / "logos" / "approval.json"
            approval.parent.mkdir()
            approval.write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "stale"):
                public_showcase(brand, kit)

    def test_vendor_boundary_requires_every_named_party_and_responsibility(self):
        brand = {"vendor_boundary": {"required": True, "notice": "Acme is independent. Users are responsible.",
                                     "entities": ["Acme"], "trademark_owner": "Acme",
                                     "terms_responsibility": "Users are responsible."}}
        self.assertEqual("Acme", vendor_boundary(brand)["entities"][0])
        brand["vendor_boundary"]["entities"].append("Missing Corp")
        with self.assertRaisesRegex(ContractError, "omits"):
            vendor_boundary(brand)


class IdentityContinuityIntegrationTests(unittest.TestCase):
    def test_canonical_gate_binding_cannot_be_faked_by_direction_or_historical_state(self):
        brand = approval_brand()
        approved = {"status": "approved-canonical", "record_sha256": "e" * 64,
                    "canonical_source_sha256": "f" * 64}
        with self.assertRaisesRegex(ContractError, "canonical source"):
            canonical_gate_binding(brand, approved)
        brand["approval_ledger"]["gate_1"]["canonical_source_sha256"] = "f" * 64
        self.assertTrue(canonical_gate_binding(brand, approved))
        with self.assertRaisesRegex(ContractError, "historical"):
            canonical_gate_binding(brand, {"status": "historical-baseline", "record_sha256": "f" * 64,
                                           "canonical_source_sha256": None})

    def test_schema_requires_a_bounded_continuity_reference_for_brand_sources(self):
        schema = json.loads((ROOT / "skill" / "references" / "canon.schema.json").read_text(encoding="utf-8"))
        then_required = schema["allOf"][0]["then"]["required"]
        self.assertIn("identity_continuity", then_required)
        reference = schema["$defs"]["identityContinuityReference"]
        self.assertFalse(reference["additionalProperties"])
        self.assertEqual(["identity-continuity.json"], reference["properties"]["record"]["enum"])
        self.assertEqual(
            ["approved-canonical", "historical-baseline"],
            reference["properties"]["status"]["enum"],
        )
        self.assertEqual(
            ["authoritative", "glyphkit-constructed", "legacy-constructed"],
            schema["$defs"]["identityContinuityRecord"]["properties"]["source_class"]["enum"],
        )

    def test_brand_file_requires_and_validates_continuity_record(self):
        from brand_contract import validate_brand_file

        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            stage_house_fonts(kit)
            brand = owned_brand()
            brand["accent"]["dim"] = "#A0B0A0"
            brand["color_roles"] = {"identity": [{"id": "primary", "label": "Example green", "source": "brand.accent.bright", "use": "Approved mark"}],
                                    "combinations": [{"id": "core-mark", "label": "Example mark", "colors": ["primary"], "artwork": "logo.full", "use": "Approved full mark"}]}
            brand_path = kit / "brand.json"
            brand_path.write_text(json.dumps(brand), encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "identity_continuity"):
                validate_brand_file(brand_path)

            brand["identity_continuity"] = {
                "record": "identity-continuity.json",
                "status": "historical-baseline",
            }
            snapshot = identity_snapshot(brand, "legacy-constructed")
            record = {
                "schema_version": 1,
                "brand": "example",
                "status": "historical-baseline",
                "source_class": "legacy-constructed",
                "recorded_on": "2026-09-09",
                "source_revision": "test-revision",
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
                    "baseline_revision": "test-revision",
                    "approval_completeness": "unknown",
                    "limitation": "This baseline is not retrospective owner approval.",
                    "migration_issue": 185,
                },
                "record_sha256": "",
            }
            record["record_sha256"] = record_digest(record)
            (kit / "identity-continuity.json").write_text(json.dumps(record), encoding="utf-8")
            brand_path.write_text(json.dumps(brand), encoding="utf-8")
            loaded, evidence = validate_brand_file(brand_path)
            self.assertEqual("example", loaded["slug"])
            self.assertEqual([], evidence)


class SourceInventoryTests(unittest.TestCase):
    def test_inventory_is_deterministic_and_byte_preserving(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "brands" / "example" / "source.svg"
            source.parent.mkdir(parents=True)
            source.write_bytes(b"<svg/>\n")
            inventory = root / "inventory.json"
            record = {
                "schema_version": 1,
                "records": [{
                    "id": "source-svg",
                    "contained_path": "brands/example/source.svg",
                    "bytes": source.stat().st_size,
                    "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                }],
            }
            inventory.write_text(json.dumps(record), encoding="utf-8")
            self.assertEqual(record, validate_source_inventory(inventory, root))
            source.write_bytes(b"<svg>changed</svg>\n")
            with self.assertRaisesRegex(ContractError, "byte drift"):
                validate_source_inventory(inventory, root)

    def test_inventory_rejects_duplicate_contained_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.txt"
            source.write_bytes(b"evidence\n")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            inventory = root / "inventory.json"
            inventory.write_text(json.dumps({"schema_version": 1, "records": [
                {"id": "first", "contained_path": "source.txt", "bytes": 9, "sha256": digest},
                {"id": "second", "contained_path": "source.txt", "bytes": 9, "sha256": digest},
            ]}), encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "duplicate source inventory path"):
                validate_source_inventory(inventory, root)


class AffiliationTests(unittest.TestCase):
    def test_production_source_requires_authored_color_roles(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = json.loads((ROOT / "brands" / "covarity" / "brand.json").read_text(encoding="utf-8"))
            del source["color_roles"]
            path = Path(temporary) / "brand.json"
            path.write_text(json.dumps(source), encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "color_roles is required"):
                validate_brand_file(path)

    def test_owned_child_can_select_independent_palette_without_losing_parentage(self):
        brand = owned_brand()
        brand["affiliation"]["inheritance"] = "independent"
        brand["semantic_colors"] = {"emphasis": "#2BCC73", "action": "#037B40"}
        self.assertEqual("A ShruggieTech project", affiliation_text(brand))
        from brand_contract import semantic_colors
        canon = json.loads((ROOT / "skill" / "references" / "01-canon.json").read_text(encoding="utf-8"))
        self.assertEqual(brand["semantic_colors"], semantic_colors(brand, canon))

    def test_owned_independent_palette_validates_and_generates_sibling_hue_tokens(self):
        from color_roles import resolve_color_roles
        from gen_nextjs import build_slots

        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            stage_house_fonts(kit)
            sibling = json.loads((ROOT / "brands" / "go-schedule" / "brand.json").read_text(encoding="utf-8"))
            brand = owned_brand()
            brand["affiliation"]["inheritance"] = "independent"
            brand["semantic_colors"] = {"emphasis": "#A1CFF4", "action": "#1C5B8D"}
            brand["accent"] = dict(sibling["accent"])
            brand["color_roles"] = {
                "identity": [{"id": "primary", "label": "Example blue", "source": "brand.accent.bright", "use": "Approved fixture mark"}],
                "combinations": [{"id": "core-mark", "label": "Example mark", "colors": ["primary"], "artwork": "logo.full", "use": "Approved fixture mark"}],
            }
            self.assertEqual([], validate_brand(brand, kit))
            canon = json.loads((ROOT / "skill" / "references" / "01-canon.json").read_text(encoding="utf-8"))
            dark, light = build_slots(canon, brand)
            roles = resolve_color_roles(brand, canon)
            self.assertEqual(sibling["accent"]["bright"], dark["primary"])
            self.assertEqual(sibling["accent"]["accessible"], light["primary"])
            self.assertEqual("#A1CFF4", roles["interface"]["dark"][1]["hex"])
            self.assertNotIn("#FF5300", {row["hex"] for row in roles["identity"]})

    def test_third_party_can_explicitly_choose_house_palette_without_endorsement(self):
        brand = owned_brand()
        brand["affiliation"].update({"ownership": "third-party", "parent": None, "endorsement": "none"})
        self.assertEqual("", affiliation_text(brand))

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

    def test_output_scan_requires_each_generated_vendor_boundary_surface(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            notice = "Acme is independent. Users are responsible."
            brand = owned_brand()
            brand["affiliation"] = {"ownership": "third-party", "showcase": "public", "parent": None, "inheritance": "independent", "endorsement": "none", "service_credit": "none"}
            brand["semantic_colors"] = {"emphasis": "#6750A4", "action": "#5B3F98"}
            brand["vendor_boundary"] = {"required": True, "notice": notice, "entities": ["Acme"], "trademark_owner": "Acme", "terms_responsibility": "Users are responsible."}
            (kit / "README.md").write_text(notice, encoding="utf-8")
            expected = ("guidelines/portal.json", "guidelines/index.html", "enforcement/AGENTS.md", "build/brand-guide.print.html")
            for relative in expected:
                path = kit / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(notice, encoding="utf-8")
            self.assertEqual([], scan_affiliation_output(brand, kit))
            (kit / expected[0]).write_text("missing", encoding="utf-8")
            self.assertEqual(["guidelines/portal.json omits the required vendor boundary"], scan_affiliation_output(brand, kit))


class ApplicationIconProfileTests(unittest.TestCase):
    def test_existing_glitchpad_frame_role_supplies_mask_background(self):
        brand = json.loads((ROOT / "brands" / "glitchpad" / "brand.json").read_text(encoding="utf-8"))
        profile = application_icon_profile(brand)
        self.assertEqual("#FFD900", profile["masked_background"])
        self.assertEqual("#0B0C0D", profile["background"])
        self.assertFalse(profile.get("windows_unplated", False))

    def test_eso_taskbar_is_unplated_without_changing_approved_source_settings(self):
        brand = json.loads((ROOT / "brands" / "eso-weave" / "brand.json").read_text(encoding="utf-8"))
        self.assertNotIn("windows_unplated", brand["logo"]["application_icon"])
        self.assertTrue(application_icon_profile(brand)["windows_unplated"])

    def test_shruggietech_uses_canonical_void_background(self):
        brand = json.loads((ROOT / "brands" / "shruggietech" / "brand.json").read_text(encoding="utf-8"))
        self.assertEqual(brand["surfaces"]["base"], application_icon_profile(brand)["background"])
        self.assertEqual("#000000", application_icon_profile(brand)["background"])

    def test_profile_uses_declared_background_and_reduced_threshold(self):
        brand = owned_brand()
        brand["surfaces"] = {"base": "#080B0D"}
        brand["logo"]["reduced_below_px"] = 32
        brand["logo"]["application_icon"] = {"background": "#FFFFFF"}
        self.assertEqual(
            {"background": "#FFFFFF", "reduced_below_px": 32, "windows_unplated": True},
            application_icon_profile(brand),
        )

    def test_profile_rejects_supplied_target_path_escape(self):
        brand = owned_brand()
        brand["logo"]["application_icon"] = {
            "background": "#FFFFFF",
            "supplied_targets": [{"source": "../favicon.png", "sha256": "0" * 64,
                                  "target": "icons/web/favicon-32x32.png"}],
        }
        with self.assertRaisesRegex(ContractError, "stay inside the kit"):
            application_icon_profile(brand)

    def test_profile_requires_explicit_boolean_for_transparent_web_icons(self):
        brand = owned_brand()
        brand["logo"]["application_icon"] = {
            "background": "#FFFFFF",
            "transparent_web_icons": "yes",
        }
        with self.assertRaisesRegex(ContractError, "transparent_web_icons must be boolean"):
            application_icon_profile(brand)

    def test_profile_rejects_monochrome_platforms_without_white_colourway(self):
        brand = owned_brand()
        brand["logo"]["colourways"] = ["color", "black"]
        brand["logo"]["application_icon"] = {
            "background": "#000000",
            "monochrome_platforms": True,
        }
        with self.assertRaisesRegex(ContractError, "require a white logo colourway"):
            application_icon_profile(brand)

    def test_supplied_png_must_match_its_generated_target_dimensions(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "favicon.png"
            Image.new("RGBA", (16, 16), (197, 52, 44, 127)).save(source, format="PNG")
            brand = owned_brand()
            brand["logo"]["application_icon"] = {
                "background": "#FFFFFF",
                "supplied_targets": [{
                    "source": "favicon.png",
                    "sha256": sha256_file(source),
                    "target": "icons/web/favicon-32x32.png",
                }],
            }
            with self.assertRaisesRegex(ContractError, "dimensions 16x16 do not match target"):
                validate_supplied_icon_dimensions(brand, root)
            Image.new("RGBA", (300, 300), (197, 52, 44, 127)).save(source, format="PNG")
            brand["logo"]["application_icon"]["supplied_targets"][0].update({
                "sha256": sha256_file(source),
                "target": "icons/windows/msix/Assets/Square150x150Logo.scale-200.png",
            })
            self.assertTrue(validate_supplied_icon_dimensions(brand, root))
            Image.new("RGBA", (256, 256), (197, 52, 44, 127)).save(source, format="PNG")
            brand["logo"]["application_icon"]["supplied_targets"][0].update({
                "sha256": sha256_file(source),
                "target": "icons/windows/msix/Assets/Square44x44Logo.targetsize-256.png",
            })
            self.assertTrue(validate_supplied_icon_dimensions(brand, root))

    def test_profile_falls_back_to_canonical_base(self):
        brand = owned_brand()
        brand["surfaces"] = {"base": "#080B0D"}
        self.assertEqual("#080B0D", application_icon_profile(brand)["background"])

    def test_profile_rejects_invalid_background_and_threshold(self):
        brand = owned_brand()
        brand["surfaces"] = {"base": "#080B0D"}
        brand["logo"]["application_icon"] = {"background": "white"}
        with self.assertRaisesRegex(ContractError, "application icon background"):
            application_icon_profile(brand)
        brand["logo"]["application_icon"] = {"background": "#FFFFFF", "extra": True}
        with self.assertRaisesRegex(ContractError, "exactly"):
            application_icon_profile(brand)
        brand["logo"]["application_icon"] = {}
        with self.assertRaisesRegex(ContractError, "exactly"):
            application_icon_profile(brand)
        del brand["logo"]["application_icon"]
        brand["logo"]["reduced_below_px"] = 0
        with self.assertRaisesRegex(ContractError, "reduced mark threshold"):
            application_icon_profile(brand)


class ShowcaseSurfaceTests(unittest.TestCase):
    def test_optional_role_resolves_from_governed_surfaces(self):
        brand = owned_brand()
        brand["surfaces"] = {"base": "#080B0D", "card": "#121416"}
        self.assertIsNone(showcase_surface(brand))
        brand["showcase_surface"] = "card"
        self.assertEqual("#121416", showcase_surface(brand))

    def test_light_role_resolves_from_governed_light_surfaces(self):
        brand = owned_brand()
        brand["surfaces"] = {"card": "#121416"}
        brand["light_surfaces"] = {"card": "#FFFFFF"}
        brand["showcase_surface"] = "light.card"
        self.assertEqual("#FFFFFF", showcase_surface(brand))

    def test_invalid_role_and_color_fail_closed(self):
        brand = owned_brand()
        brand["surfaces"] = {"card": "#121416"}
        brand["showcase_surface"] = "missing"
        with self.assertRaisesRegex(ContractError, "showcase surface role"):
            showcase_surface(brand)
        brand["showcase_surface"] = "card"
        brand["surfaces"]["card"] = "charcoal"
        with self.assertRaisesRegex(ContractError, "six-digit hex"):
            showcase_surface(brand)
        brand["showcase_surface"] = ""
        with self.assertRaisesRegex(ContractError, "non-empty"):
            showcase_surface(brand)
        brand["showcase_surface"] = "light.missing"
        brand["light_surfaces"] = {"card": "#FFFFFF"}
        with self.assertRaisesRegex(ContractError, "showcase surface role"):
            showcase_surface(brand)


class GuideSurfaceModeTests(unittest.TestCase):
    def test_missing_mode_defaults_to_dark_and_explicit_light_is_valid(self):
        brand = owned_brand()
        self.assertEqual("dark", guide_surface_mode(brand))
        brand["guide"] = {"surface_mode": "light"}
        brand["light_surfaces"] = {
            "base": "#FFFFFF", "card": "#FFFFFF", "popover": "#FFFFFF",
            "secondary": "#F8F6F2", "hover": "#EEF4F8",
            "foreground": "#111111", "muted_foreground": "#555555",
        }
        self.assertEqual("light", guide_surface_mode(brand))

    def test_invalid_mode_and_incomplete_light_palette_fail_early(self):
        brand = owned_brand()
        for guide in ("light", {"surface_mode": "sepia"}, {"surface_mode": None}):
            brand["guide"] = guide
            with self.assertRaisesRegex(ContractError, "guide.surface_mode|guide must"):
                guide_surface_mode(brand)
        brand["guide"] = {"surface_mode": "light"}
        with self.assertRaisesRegex(ContractError, "light_surfaces"):
            guide_surface_mode(brand)

    def test_light_palette_rejects_low_contrast_local_text(self):
        brand = owned_brand()
        brand["guide"] = {"surface_mode": "light"}
        brand["light_surfaces"] = {
            "base": "#FFFFFF", "card": "#FFFFFF", "popover": "#FFFFFF",
            "secondary": "#F8F6F2", "hover": "#EEF4F8",
            "foreground": "#AAAAAA", "muted_foreground": "#555555",
        }
        with self.assertRaisesRegex(ContractError, "contrast"):
            guide_surface_mode(brand)

    def test_dark_guide_with_light_showcase_validates_the_light_palette(self):
        brand = owned_brand()
        brand["showcase_surface"] = "light.card"
        brand["light_surfaces"] = {"card": "#FFFFFF"}
        self.assertEqual("dark", guide_surface_mode(brand))
        with tempfile.TemporaryDirectory() as temporary:
            stage_house_fonts(Path(temporary))
            with self.assertRaisesRegex(ContractError, "light showcase_surface requires complete light_surfaces"):
                validate_brand(brand, Path(temporary))
            brand["light_surfaces"].update({
                "base": "#FFFFFF", "popover": "#FFFFFF", "secondary": "#F8F6F2",
                "hover": "#EEF4F8", "foreground": "#AAAAAA",
                "muted_foreground": "#555555",
            })
            with self.assertRaisesRegex(ContractError, "foreground contrast on light_surfaces"):
                validate_brand(brand, Path(temporary))


class SquareEnclosureProfileTests(unittest.TestCase):
    def test_optional_profile_resolves_complete_safe_geometry(self):
        brand = owned_brand()
        self.assertIsNone(square_enclosure_profile(brand))
        brand["logo"]["square_enclosure"] = {
            "canvas_size": 1000,
            "inset": 62,
            "corner_radius": 142,
            "stroke_width": 24,
            "content_scale": 0.72,
            "frame_role": "frame",
            "stroke_role": "frame_stroke",
            "knockout_role": "neutral",
            "monochrome_knockout": True,
        }
        brand["logo"]["role_colors"] = {
            "color": {"frame": "#FFD900", "frame_stroke": "#FFD900"},
            "light": {"frame": "#0B0C0D", "frame_stroke": "#0B0C0D"},
        }
        self.assertEqual(876, square_enclosure_profile(brand)["size"])

    def test_profile_rejects_unsafe_or_incomplete_geometry(self):
        brand = owned_brand()
        profile = {
            "canvas_size": 1000,
            "inset": 62,
            "corner_radius": 142,
            "stroke_width": 24,
            "content_scale": 0.72,
            "frame_role": "frame",
            "stroke_role": "frame_stroke",
            "knockout_role": "neutral",
            "monochrome_knockout": True,
        }
        brand["logo"]["square_enclosure"] = profile
        brand["logo"]["role_colors"] = {
            "color": {"frame": "#FFD900", "frame_stroke": "#FFD900"},
            "light": {"frame": "#0B0C0D", "frame_stroke": "#0B0C0D"},
        }
        for field in tuple(profile):
            broken = copy.deepcopy(brand)
            del broken["logo"]["square_enclosure"][field]
            with self.subTest(field=field), self.assertRaisesRegex(ContractError, "square enclosure"):
                square_enclosure_profile(broken)
        brand["logo"]["square_enclosure"]["inset"] = 10
        with self.assertRaisesRegex(ContractError, "stroke inside"):
            square_enclosure_profile(brand)
        brand["logo"]["square_enclosure"]["inset"] = 62
        brand["logo"]["square_enclosure"]["content_scale"] = 1.2
        with self.assertRaisesRegex(ContractError, "content_scale"):
            square_enclosure_profile(brand)
        brand["logo"]["square_enclosure"]["content_scale"] = 1.0
        brand["logo"]["paths"]["full"] = [{"role": "accent", "d": "M0 0H2000V2000Z"}]
        brand["logo"]["paths"]["reduced"] = [{"role": "accent", "d": "M0 0H2000V2000Z"}]
        with self.assertRaisesRegex(ContractError, "exceed the safe content area"):
            square_enclosure_profile(brand)

    def test_optional_wordmark_role_is_complete_and_source_owned(self):
        brand = owned_brand()
        self.assertIsNone(wordmark_role_colors(brand))
        brand["logo"]["role_colors"] = {
            "color": {"wordmark": "#F2F5FA"},
            "light": {"wordmark": "#0A0A0A"},
        }
        self.assertEqual({"color": "#F2F5FA", "light": "#0A0A0A"},
                         wordmark_role_colors(brand))
        del brand["logo"]["role_colors"]["light"]["wordmark"]
        with self.assertRaisesRegex(ContractError, "light.wordmark"):
            wordmark_role_colors(brand)


class AuthoritativeInputTests(unittest.TestCase):
    def make_raster_brand(self, kit):
        stage_house_fonts(kit)
        assets = kit / "assets"
        assets.mkdir()
        image = Image.new("RGBA", (3, 2))
        image.putdata([(43, 204, 115, 255), (43, 204, 115, 255), (255, 255, 255, 0), (0, 171, 33, 255), (43, 204, 115, 128), (0, 171, 33, 255)])
        source = assets / "mark.png"
        reduced = assets / "reduced.png"
        image.save(source)
        image.save(reduced)
        brand = owned_brand()
        brand["logo"]["source_mode"] = "authoritative"
        brand["logo"]["authoritative_input_ids"] = {"full": "master-mark", "reduced": "master-reduced"}
        brand["logo"]["paths"]["full"] = [{"element": "image", "source": "assets/mark.png", "mask": "alpha", "x": 0, "y": 0, "width": 3, "height": 2}]
        brand["logo"]["paths"]["reduced"] = [{"element": "image", "source": "assets/reduced.png", "mask": "alpha", "x": 0, "y": 0, "width": 3, "height": 2}]
        operations = ["recolor-mask", "resize", "place-in-lockup", "palette-analysis"]
        brand["authoritative_inputs"] = [
            {"id": "master-mark", "role": "mark", "path": "assets/mark.png", "format": "png", "sha256": sha256_file(source), "color_profile": "unknown", "usage_status": "approved", "license": "Test fixture", "approved_mask": "alpha", "mask_source_sha256": sha256_file(source), "mask_approved_by": "Test owner", "mask_approved_on": "2026-09-07", "approved_transformations": operations},
            {"id": "master-reduced", "role": "reduced-mark", "path": "assets/reduced.png", "format": "png", "sha256": sha256_file(reduced), "color_profile": "unknown", "usage_status": "approved", "license": "Test fixture", "approved_mask": "alpha", "mask_source_sha256": sha256_file(reduced), "mask_approved_by": "Test owner", "mask_approved_on": "2026-09-07", "approved_transformations": ["recolor-mask", "resize"]},
        ]
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
                "stylesheet import": ('<style>@import url(https://example.test/mark.css)</style>', "prohibited"),
            }
            for label, (content, message) in cases.items():
                with self.subTest(label=label):
                    source.write_text('<svg xmlns="http://www.w3.org/2000/svg">%s<path fill="#112233" d="M0 0Z"/></svg>\n' % content, encoding="utf-8")
                    brand = owned_brand()
                    brand["authoritative_inputs"] = [{"id": "svg-mark", "role": "mark", "path": "mark.svg", "format": "svg", "sha256": sha256_file(source), "color_profile": "none", "usage_status": "approved", "license": "Test fixture", "approved_transformations": []}]
                    with self.assertRaisesRegex(ContractError, message):
                        validate_brand(brand, kit)

    def test_svg_allows_only_self_contained_base64_png_images(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            stage_house_fonts(kit)
            png = BytesIO()
            Image.new("RGBA", (1, 1), (17, 34, 51, 255)).save(png, format="PNG")
            encoded = base64.b64encode(png.getvalue()).decode("ascii")
            source = kit / "mark.svg"
            source.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"><image href="data:image/png;base64,%s"/></svg>\n' % encoded,
                encoding="utf-8",
            )
            brand = owned_brand()
            brand["authoritative_inputs"] = [{"id": "svg-mark", "role": "reference-art", "path": "mark.svg", "format": "svg", "sha256": sha256_file(source), "color_profile": "none", "usage_status": "reference-only", "license": "Test fixture", "approved_transformations": []}]
            validate_brand(brand, kit)
            cases = (
                ("data:image/png;base64,SGVsbG8=", "not a PNG"),
                ("data:image/png;base64,%%%", "malformed"),
                ("data:text/plain;base64,SGVsbG8=", "external reference"),
            )
            for payload, message in cases:
                source.write_text('<svg xmlns="http://www.w3.org/2000/svg"><image href="%s"/></svg>\n' % payload, encoding="utf-8")
                brand["authoritative_inputs"][0]["sha256"] = sha256_file(source)
                with self.subTest(payload=payload), self.assertRaisesRegex(ContractError, message):
                    validate_brand(brand, kit)

    def test_multiple_supplied_lockups_are_allowed(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            stage_house_fonts(kit)
            source = kit / "lockup.svg"
            source.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path fill="#112233" d="M0 0H1V1Z"/></svg>\n', encoding="utf-8")
            copy_path = kit / "lockup-copy.svg"
            shutil.copy2(source, copy_path)
            record = {"role": "lockup", "format": "svg", "sha256": sha256_file(source), "color_profile": "none", "usage_status": "approved", "license": "Test fixture", "approved_transformations": ["embed-unchanged", "resize"]}
            brand = owned_brand()
            brand["authoritative_inputs"] = [dict(record, id="horizontal-lockup", path="lockup.svg"), dict(record, id="vertical-lockup", path="lockup-copy.svg")]
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

    def test_source_mode_is_required_and_constructed_mode_rejects_mark_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            stage_house_fonts(kit)
            brand = owned_brand()
            del brand["logo"]["source_mode"]
            with self.assertRaisesRegex(ContractError, "logo.source_mode is required"):
                validate_brand(brand, kit)
            brand["logo"]["source_mode"] = "automatic"
            with self.assertRaisesRegex(ContractError, "constructed or authoritative"):
                validate_brand(brand, kit)

        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            brand, _ = self.make_raster_brand(kit)
            brand["logo"]["source_mode"] = "constructed"
            del brand["logo"]["authoritative_input_ids"]
            with self.assertRaisesRegex(ContractError, "constructed logo cannot declare approved mark"):
                validate_brand(brand, kit)

    def test_authoritative_bindings_reject_substitute_geometry_and_wrong_sources(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            brand, _ = self.make_raster_brand(kit)
            self.assertEqual("master-mark", logo_source_contract(brand, kit)["full"]["record"]["id"])

            cases = []
            missing = copy.deepcopy(brand)
            del missing["logo"]["authoritative_input_ids"]["reduced"]
            cases.append((missing, "exactly full and reduced"))
            unrelated = copy.deepcopy(brand)
            unrelated["logo"]["paths"]["full"].append({"d": "M0 0H1V1Z", "role": "accent"})
            cases.append((unrelated, "exactly one bound image"))
            wrong_source = copy.deepcopy(brand)
            wrong_source["logo"]["paths"]["full"][0]["source"] = "assets/reduced.png"
            cases.append((wrong_source, "does not use bound source"))
            wrong_role = copy.deepcopy(brand)
            wrong_role["authoritative_inputs"][0]["role"] = "wordmark"
            cases.append((wrong_role, "requires authoritative role mark"))
            reference_only = copy.deepcopy(brand)
            reference_only["authoritative_inputs"][0]["usage_status"] = "reference-only"
            cases.append((reference_only, "is not approved"))
            distorted = copy.deepcopy(brand)
            distorted["logo"]["paths"]["full"][0]["width"] = 4
            cases.append((distorted, "distorts authoritative source aspect ratio"))
            for broken, message in cases:
                with self.subTest(message=message), self.assertRaisesRegex(ContractError, message):
                    validate_brand(broken, kit)

    def test_authoritative_colourways_and_supplied_lockups_bind_exact_sources(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            brand, _ = self.make_raster_brand(kit)
            for name in ("full-light", "horizontal-dark", "horizontal-light", "vertical-dark", "vertical-light"):
                path = kit / "assets" / (name + ".svg")
                path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2 1"><path fill="#112233" d="M0 0H2V1H0Z"/></svg>\n', encoding="utf-8")
                brand["authoritative_inputs"].append({
                    "id": name,
                    "role": "lockup",
                    "path": "assets/%s.svg" % name,
                    "format": "svg",
                    "sha256": sha256_file(path),
                    "color_profile": "none",
                    "usage_status": "approved",
                    "license": "Test fixture",
                    "approved_transformations": ["embed-unchanged", "resize"],
                })
            brand["logo"].update({
                "colourways": ["color", "light"],
                "full_colourway_input_ids": {"light": "full-light"},
                "supplied_lockup_input_ids": {
                    "horizontal": {"color": "horizontal-dark", "light": "horizontal-light"},
                    "stacked": {"color": "vertical-dark", "light": "vertical-light"},
                },
            })
            brand["approval_ledger"] = {
                "gate_1": {"unavailable_derivatives": {"wordmark-only": "No approved standalone wordmark."}},
            }
            resolved = logo_source_contract(brand, kit)
            self.assertEqual("full-light", resolved["full_colourways"]["light"]["record"]["id"])
            self.assertEqual("horizontal-dark", resolved["supplied_lockups"]["horizontal"]["color"]["record"]["id"])

            del brand["approval_ledger"]
            with self.assertRaisesRegex(ContractError, "generated wordmarks cannot replace approved masters"):
                logo_source_contract(brand, kit)

    def test_logo_colourways_include_required_downstream_variants(self):
        with tempfile.TemporaryDirectory() as temporary:
            brand = owned_brand()
            for colourways in (["color", "black"], ["light", "black"]):
                brand["logo"]["colourways"] = colourways
                with self.subTest(colourways=colourways), self.assertRaisesRegex(
                        ContractError, "must include color and light"):
                    logo_source_contract(brand, Path(temporary))

    def test_authoritative_mode_rejects_construction_helper_and_reduced_redraw(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            brand, _ = self.make_raster_brand(kit)
            helper = kit / "build" / "mk_paths.py"
            helper.parent.mkdir()
            helper.write_text("raise RuntimeError('must never execute')\n", encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "construction helper"):
                validate_brand(brand, kit)
            helper.unlink()
            brand["logo"]["paths"]["reduced"] = [{"d": "M0 0H1V1Z", "role": "accent"}]
            with self.assertRaisesRegex(ContractError, "reduced.*exactly one bound image"):
                validate_brand(brand, kit)

    def test_authoritative_png_requires_portable_rgba8_profile(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            brand, source = self.make_raster_brand(kit)
            Image.new("RGB", (3, 2), (43, 204, 115)).save(source)
            brand["authoritative_inputs"][0]["sha256"] = sha256_file(source)
            with self.assertRaisesRegex(ContractError, "non-interlaced RGBA8"):
                validate_brand(brand, kit)

    def test_authoritative_mask_method_requires_current_owner_approval(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            brand, _source = self.make_raster_brand(kit)
            brand["logo"]["paths"]["full"][0]["mask"] = "luminance"
            with self.assertRaisesRegex(ContractError, "mask method lacks matching owner approval"):
                validate_brand(brand, kit)
            brand["logo"]["paths"]["full"][0]["mask"] = "alpha"
            brand["authoritative_inputs"][0]["mask_source_sha256"] = "0" * 64
            with self.assertRaisesRegex(ContractError, "mask approval is stale"):
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

    def test_fixed_fonts_require_outline_face_for_every_declared_weight(self):
        def woff2_only_bold(brand, kit):
            source = ROOT / "assets" / "fonts" / "woff2" / "SpaceGrotesk-Bold.woff2"
            target = kit / "fonts" / source.name
            shutil.copy2(source, target)
            brand["typography"]["families"]["display"]["weights"].append(700)
            brand["typography"]["faces"].append({
                "role": "display", "path": "fonts/%s" % source.name, "weight": 700,
                "style": "normal", "format": "woff2", "sha256": sha256_file(target),
                "license": "OFL-1.1", "provenance": "Repository licensed test face",
                "usage_status": "approved",
            })

        self.assert_fixed_font_error(woff2_only_bold, "lacks outline-capable weight 700")

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


class SocialCopyTests(unittest.TestCase):
    def test_exact_production_copy_decisions(self):
        expected = {
            "shruggietech": ("We advance your vision.", []),
            "i-heart-pr-tours": ("Experience Puerto Rico", []),
            "go-schedule": ("A cross-platform scheduler in Go.", []),
            "glitchpad": ("View your files.", []),
            "fragcap": ("See what your game is actually saying.", []),
            "eso-weave": ("Unofficial automation for ESO", []),
            "cueson": ("Universal captions and subtitles", ["A lossless, structured interchange layer", "for subtitle and caption content."]),
            "covarity": ("See what is known.", []),
        }
        for slug, (slogan, lines) in expected.items():
            with self.subTest(brand=slug):
                brand = json.loads((ROOT / "brands" / slug / "brand.json").read_text(encoding="utf-8"))
                approved = social_copy(brand)
                self.assertEqual(slogan, approved["slogan"])
                self.assertEqual(lines, approved["description_lines"])
                self.assertEqual("slogan-description" if lines else "slogan-only", approved["layout"])

    def test_social_copy_rejects_inferred_or_incomplete_decisions(self):
        brand = {"brand_idea": "Candidate only"}
        with self.assertRaisesRegex(ContractError, "social_copy"):
            social_copy(brand)
        brand["social_copy"] = {"slogan": "Chosen", "layout": "slogan-only",
                                "description_lines": ["Unapproved extra"],
                                "approval": {"approved_by": "owner", "approved_on": "2026-09-25", "source": "decision"}}
        with self.assertRaisesRegex(ContractError, "description lines"):
            social_copy(brand)


if __name__ == "__main__":
    unittest.main()
