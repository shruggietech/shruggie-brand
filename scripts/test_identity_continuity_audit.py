#!/usr/bin/env python3
"""Regression tests for the S027 production-brand continuity migration."""

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "skill" / "templates"))

from audit_identity_continuity import (BRAND_CLASSES, MIGRATION_BASELINE_BRANDS, MIGRATION_BASELINE_REVISION, audit,
                                       build_record, compare_brand_state, compare_historical_identity,
                                       discover_brands)
from identity_continuity import validate_brand_continuity


class IdentityContinuityAuditTests(unittest.TestCase):
    def test_inventory_is_complete_and_classification_is_explicit(self):
        self.assertEqual(set(BRAND_CLASSES), set(discover_brands(ROOT)))
        self.assertEqual("glyphkit-constructed", BRAND_CLASSES["cueson"])
        self.assertEqual("legacy-constructed", BRAND_CLASSES["covarity"])
        self.assertEqual("authoritative", BRAND_CLASSES["eso-weave"])
        self.assertEqual("authoritative", BRAND_CLASSES["i-heart-pr-tours"])
        self.assertEqual("authoritative", BRAND_CLASSES["scruggs-tire-alignment"])
        self.assertEqual("authoritative", BRAND_CLASSES["dancewithme865"])
        self.assertEqual("glyphkit-constructed", BRAND_CLASSES["local-companion"])
        self.assertEqual("glyphkit-constructed", BRAND_CLASSES["insonic"])
        self.assertTrue({"dancewithme865", "scruggs-tire-alignment", "local-companion", "insonic"}.isdisjoint(
            MIGRATION_BASELINE_BRANDS))

    def test_historical_record_is_revision_bound_without_fake_approval(self):
        source = ROOT / "brands" / "cueson"
        brand = json.loads((source / "brand.json").read_text(encoding="utf-8"))
        brand["identity_continuity"] = {"record": "identity-continuity.json", "status": "historical-baseline"}
        record = build_record(source, brand, "glyphkit-constructed", "abc123", "2026-09-09")
        self.assertEqual("abc123", record["source_revision"])
        self.assertIsNone(record["approval"])
        self.assertEqual([], record["proofs"])
        self.assertIn("not", record["historical_evidence"]["limitation"].lower())

    def test_preservation_comparison_allows_only_reference_and_covarity_provenance(self):
        before = json.loads((ROOT / "brands" / "covarity" / "brand.json").read_text(encoding="utf-8"))
        after = copy.deepcopy(before)
        after["identity_continuity"] = {"record": "identity-continuity.json", "status": "historical-baseline"}
        after["logo"]["geometry_provenance"] = "legacy-constructed"
        after["logo"]["geometry_provenance_reason"] = "Predates glyphkit and is preserved byte-for-byte."
        self.assertEqual([], compare_brand_state("covarity", before, after))
        after["accent"]["bright"] = "#FFFFFF"
        self.assertIn("accent", " ".join(compare_brand_state("covarity", before, after)))

    def test_every_committed_record_validates(self):
        missing = []
        for slug, source in discover_brands(ROOT).items():
            record = source / "identity-continuity.json"
            if not record.is_file():
                missing.append(slug)
                continue
            brand = json.loads((source / "brand.json").read_text(encoding="utf-8"))
            validate_brand_continuity(brand, source)
        self.assertEqual([], missing)

    def test_check_mode_preserves_historical_identity_after_nonidentity_updates(self):
        report = audit(MIGRATION_BASELINE_REVISION, write=False)
        self.assertEqual([], report["problems"])
        preservation = {item["brand"]: item["preservation"] for item in report["brands"]}
        self.assertEqual("baseline-preserved", preservation["cueson"])
        self.assertEqual("baseline-preserved", preservation["go-schedule"])
        self.assertEqual("new-approved-source", preservation["local-companion"])

    def test_check_mode_rejects_rewritten_historical_identity_and_record(self):
        for change, expected in (("palette", "palette"), ("geometry", "geometry")):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temporary:
                source = Path(temporary) / "cueson"
                shutil.copytree(ROOT / "brands" / "cueson", source)
                brand_path = source / "brand.json"
                brand = json.loads(brand_path.read_text(encoding="utf-8"))
                if change == "palette":
                    brand["accent"]["bright"] = "#FFFFFF"
                else:
                    brand["logo"]["paths"]["full"][0]["d"] += " m1 0"
                with brand_path.open("w", encoding="utf-8", newline="\n") as handle:
                    handle.write(json.dumps(brand, indent=2) + "\n")
                record = build_record(source, brand, BRAND_CLASSES["cueson"], MIGRATION_BASELINE_REVISION, "2026-09-09")
                with (source / "identity-continuity.json").open("w", encoding="utf-8", newline="\n") as handle:
                    handle.write(json.dumps(record, indent=2) + "\n")
                brands = discover_brands(ROOT)
                brands["cueson"] = source
                with mock.patch("audit_identity_continuity.discover_brands", return_value=brands):
                    report = audit(MIGRATION_BASELINE_REVISION, write=False)
                self.assertIn("cueson: %s changed" % expected, report["problems"])

    def test_approved_shruggietech_baseline_rejects_later_framing_drift(self):
        brand = json.loads((ROOT / "brands" / "shruggietech" / "brand.json").read_text(encoding="utf-8"))
        self.assertEqual([], compare_historical_identity("shruggietech", MIGRATION_BASELINE_REVISION, brand))
        brand["logo"]["reduced_viewbox"][0] += 1
        self.assertIn("derivative_settings changed", compare_historical_identity(
            "shruggietech", MIGRATION_BASELINE_REVISION, brand))


if __name__ == "__main__":
    unittest.main()
