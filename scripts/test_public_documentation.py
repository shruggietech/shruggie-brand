#!/usr/bin/env python3
"""Focused source and publication audit regressions for public guidance."""

import json
import tempfile
import unittest
from pathlib import Path

import audit_public_documentation as audit


class PublicDocumentationAuditTests(unittest.TestCase):
    def test_rejects_planning_codes_and_nonreader_process_language(self):
        text = "## S007 contract commands\nA future Spec Kit slice will decide this.\n"
        problems = audit.scan_text("manual.md", text)
        self.assertTrue(any("S007" in problem for problem in problems))
        self.assertTrue(any("Spec Kit" in problem for problem in problems))

    def test_rejects_known_historical_and_vague_prose(self):
        text = "Fragcap 1.0.0 once said this. It is genuinely good at opening up a concept space quickly.\n"
        problems = audit.scan_text("voice.md", text)
        self.assertTrue(any("historical" in problem for problem in problems))
        self.assertTrue(any("vague" in problem for problem in problems))

    def test_preserves_current_compatibility_terms_and_normative_permission(self):
        text = "A historical-baseline may record the current source. Legacy-constructed geometry remains byte-identical.\n"
        self.assertEqual([], audit.scan_text("current.md", text))

    def test_html_scan_ignores_script_and_style_payloads(self):
        html = "<style>.x{content:'S007'}</style><script>const x='S008'</script><main><h1>Current guide</h1><p>S009 leaked</p></main>"
        self.assertEqual("Current guide S009 leaked", audit.visible_html_text(html))

    def test_source_inventory_is_catalogued_and_brand_scoped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            refs = root / "skill" / "references"
            refs.mkdir(parents=True)
            (refs / "documentation-contract.json").write_text(
                json.dumps({"manual_pages": [{"source": "guide.md"}]}), encoding="utf-8"
            )
            (refs / "guide.md").write_text("Current manual\n", encoding="utf-8")
            brand = root / "brands" / "alpha"
            brand.mkdir(parents=True)
            (brand / "brand.json").write_text('{"slug":"alpha"}', encoding="utf-8")
            (brand / "README.md").write_text("Current brand\n", encoding="utf-8")
            (brand / "provenance").mkdir()
            (brand / "provenance" / "history.md").write_text("S012 archive\n", encoding="utf-8")
            labels = [label for label, _ in audit.source_documents(root, brands=("alpha",))]
            self.assertIn("skill/references/guide.md", labels)
            self.assertIn("brands/alpha/README.md", labels)
            self.assertNotIn("brands/alpha/provenance/history.md", labels)
            (brand / "brand.json").write_text('{"slug":"beta"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "brand scope"):
                list(audit.source_documents(root, brands=("alpha",)))

    def test_prepared_inventory_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root.parent / "not-in-kit.md"
            with self.assertRaisesRegex(ValueError, "outside publication root"):
                audit.require_contained(root, outside)


if __name__ == "__main__":
    unittest.main(verbosity=2)
