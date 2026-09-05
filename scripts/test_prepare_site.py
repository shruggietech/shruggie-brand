#!/usr/bin/env python3
"""Focused tests for production-only site materialization."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import prepare_site


class PrepareSiteTests(unittest.TestCase):
    def test_source_dirs_require_exact_production_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp)
            for slug in ("alpha", "stale"):
                target = dist / slug
                target.mkdir()
                (target / "brand.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unexpected.*stale"):
                prepare_site.source_dirs(dist, {"alpha"})
            (dist / "stale" / "brand.json").unlink()
            self.assertEqual([path.name for path in prepare_site.source_dirs(dist, {"alpha"})], ["alpha"])

    def test_source_dirs_reject_missing_production_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "missing.*alpha"):
                prepare_site.source_dirs(Path(tmp), {"alpha"})

    def test_public_markdown_rewrites_prose_and_preserves_literal_code(self):
        source = "# Canon contract\n\nThe canon guides decisions.\n\n`canon` stays literal.\n\n```json\n{\"canon\": \"1.1.2\"}\n```\n"
        title, body = prepare_site.derive_public_markdown(source)
        self.assertEqual(title, "Brand system contract")
        self.assertIn("The brand system guides decisions.", body)
        self.assertIn("`canon` stays literal.", body)
        self.assertIn('{"canon": "1.1.2"}', body)

    def test_write_docs_derives_frontmatter_navigation_and_source_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            references = root / "references"
            output = root / "generated"
            references.mkdir()
            (references / "00-start.md").write_text(
                "# Start here\n\nUse this reference.\n\n| A | B |\n| --- | --- |\n| one | two |\n",
                encoding="utf-8",
            )
            records = prepare_site.write_docs(references, output, {"00-start": "Start description."})
            self.assertEqual(records, [{"slug": "00-start", "title": "Start here", "description": "Start description."}])
            page = (output / "00-start.mdx").read_text(encoding="utf-8")
            self.assertIn('title: "Start here"', page)
            self.assertIn("| one | two |", page)
            self.assertNotIn("# Start here", page)
            meta = json.loads((output / "meta.json").read_text(encoding="utf-8"))
            self.assertEqual(meta["pages"], ["index", "00-start"])

    def test_active_source_paths_do_not_reference_retired_fixture(self):
        root = Path(__file__).resolve().parents[1]
        active = [
            root / "README.md",
            root / ".gitignore",
            root / "scripts" / "build_all.py",
            root / "scripts" / "prepare_site.py",
            root / "skill" / "templates" / "test_pipeline.py",
            root / "site" / "app",
        ]
        needle = "example" + "-brand"
        found = []
        for target in active:
            paths = target.rglob("*") if target.is_dir() else [target]
            for path in paths:
                if path.is_file() and path.suffix in {".md", ".py", ".ts", ".tsx", ".css", ".json"}:
                    if needle in path.read_text(encoding="utf-8"):
                        found.append(str(path.relative_to(root)))
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
