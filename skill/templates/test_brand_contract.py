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

from brand_contract import ContractError, SERVICE_CREDIT, _font_metadata, affiliation_text, analyze_authoritative_inputs, application_icon_profile, approval_ledger, derivative_configuration_sha256, logo_source_contract, public_showcase, scan_affiliation_output, sha256_file, showcase_surface, square_enclosure_profile, validate_brand, validate_source_inventory, vendor_boundary, wordmark_role_colors
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
            "e9f3aef341ed8910426abd6d7876dac1f39f69afe370efc9c1cddb7af41f9dc5",
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
        with self.assertRaisesRegex(ContractError, "every derivative family"):
            approval_ledger(incomplete)

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
            {"background": "#FFFFFF", "reduced_below_px": 32},
            application_icon_profile(brand),
        )

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


if __name__ == "__main__":
    unittest.main()
