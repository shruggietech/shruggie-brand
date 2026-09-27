#!/usr/bin/env python3
"""Stable bibliography and citation checks for both source and hosted manual."""

import tempfile
import unittest
from pathlib import Path

from check_documentation_references import validate_references
from documentation_render import render_page


ROOT = Path(__file__).resolve().parents[1]


class ReferenceTests(unittest.TestCase):
    def test_canonical_library_and_source_citations(self):
        ids = validate_references(ROOT / "skill" / "references")
        self.assertGreaterEqual(len(ids), 50)
        self.assertIn("ref-a11y-wcag21", ids)
        self.assertIn("ref-wp-global", ids)

    def test_duplicate_unknown_and_missing_manual_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "references.md").write_text(
                "# References\n### REF-TEST\n**Source:** [Test](https://example.com) **Class:** Guide **Use:** Do a task. **Limit:** A caveat.\n",
                encoding="utf-8")
            (root / "guide.md").write_text("[Source](references.md#ref-test)\n", encoding="utf-8")
            self.assertEqual({"ref-test"}, validate_references(root))
            (root / "guide.md").write_text("[Source](references.md#ref-missing)\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown reference"):
                validate_references(root)
            (root / "guide.md").write_text("[Other](absent.md)\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing manual"):
                validate_references(root)
            (root / "guide.md").write_text("[Source](references.md#ref-test)\n", encoding="utf-8")
            with (root / "references.md").open("a", encoding="utf-8") as output:
                output.write("\n### REF-TEST\n**Source:** [Other](https://example.org) **Class:** Guide **Use:** Do more. **Limit:** Other.\n")
            with self.assertRaisesRegex(ValueError, "duplicate reference ID"):
                validate_references(root)

    def test_hosted_transform_preserves_offline_source(self):
        source = "# Guide\nRead [WCAG](references.md#ref-a11y-wcag21) and [the manual](03-interview.md).\n"
        rendered = render_page(source, "Test", {
            "status": "candidate", "version": "2.6.0", "releaseUrl": "https://example.com/release",
            "skillUrl": "https://example.com/skill",
        })
        self.assertIn("/docs/references/#ref-a11y-wcag21", rendered)
        self.assertIn("/docs/03-interview/", rendered)
        self.assertIn("references.md#ref-a11y-wcag21", source)


if __name__ == "__main__":
    unittest.main()
