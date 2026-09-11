#!/usr/bin/env python3
"""Regression tests for the S027 production-brand continuity migration."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "skill" / "templates"))

from audit_identity_continuity import BRAND_CLASSES, build_record, compare_brand_state, discover_brands
from identity_continuity import validate_brand_continuity


class IdentityContinuityAuditTests(unittest.TestCase):
    def test_inventory_is_complete_and_classification_is_explicit(self):
        self.assertEqual(set(BRAND_CLASSES), set(discover_brands(ROOT)))
        self.assertEqual("glyphkit-constructed", BRAND_CLASSES["cueson"])
        self.assertEqual("legacy-constructed", BRAND_CLASSES["covarity"])
        self.assertEqual("authoritative", BRAND_CLASSES["eso-weave"])
        self.assertEqual("authoritative", BRAND_CLASSES["i-heart-pr-tours"])

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


if __name__ == "__main__":
    unittest.main()
