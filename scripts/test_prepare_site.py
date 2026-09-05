#!/usr/bin/env python3
"""Focused tests for production-only site materialization."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

import prepare_site


class PrepareSiteTests(unittest.TestCase):
    def test_showcase_permission_is_independent_and_fail_closed(self):
        brand = {"kind": "sub-brand", "affiliation": {"ownership": "third-party", "showcase": "private", "parent": None, "inheritance": "independent", "endorsement": "none", "service_credit": "none"}}
        self.assertFalse(prepare_site.public_showcase(brand))
        brand["affiliation"]["showcase"] = "public"
        self.assertTrue(prepare_site.public_showcase(brand))
        del brand["affiliation"]["showcase"]
        with self.assertRaisesRegex(ValueError, "exactly"):
            prepare_site.public_showcase(brand)

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

    def test_source_identity_requires_matching_unique_slug(self):
        source = Path("alpha")
        with self.assertRaisesRegex(ValueError, "must match"):
            prepare_site.validate_source_identity(source, {"slug": "beta"}, set())
        seen = {"alpha"}
        with self.assertRaisesRegex(ValueError, "duplicate"):
            prepare_site.validate_source_identity(source, {"slug": "alpha"}, seen)

    def test_stale_generated_public_brand_is_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            public = Path(tmp)
            stale = public / "stale"
            (stale / "brand" / "r").mkdir(parents=True)
            (stale / "downloads" / "files").mkdir(parents=True)
            (stale / "brand" / "r" / "registry.json").write_text("{}\n", encoding="utf-8")
            unrelated = public / "unrelated"
            unrelated.mkdir()
            self.assertEqual(prepare_site.remove_stale_public_brands(public, {"alpha"}), ["stale"])
            self.assertFalse(stale.exists())
            self.assertTrue(unrelated.exists())

    def test_guideline_metadata_is_complete_and_absolute(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "index.html"
            page.write_text("<html><head><title>Guide</title></head><body></body></html>", encoding="utf-8")
            prepare_site.add_guideline_metadata(page, {"slug": "alpha", "title": "Alpha", "descriptor": "One & only."})
            content = page.read_text(encoding="utf-8")
            self.assertIn("<title>Alpha guidelines | ShruggieTech</title>", content)
            self.assertIn('rel="canonical" href="https://brand.shruggie.tech/alpha/guidelines/"', content)
            self.assertIn('property="og:title"', content)
            self.assertIn('name="twitter:card"', content)
            self.assertIn("One &amp; only.", content)

    def test_public_markdown_rewrites_prose_and_preserves_literal_code(self):
        source = "# Canon contract\n\nThe canon guides decisions for A ShruggieTech project.\n\n`canon` and `A ShruggieTech project` stay literal.\n\n```json\n{\"canon\": \"1.1.2\", \"endorsement\": \"A ShruggieTech project\"}\n```\n"
        title, body = prepare_site.derive_public_markdown(source)
        self.assertEqual(title, "Brand system contract")
        self.assertIn("The brand system guides decisions for Brand system by ShruggieTech.", body)
        self.assertIn("`canon` and `A ShruggieTech project` stay literal.", body)
        self.assertIn('{"canon": "1.1.2", "endorsement": "A ShruggieTech project"}', body)

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

    def test_site_identity_requires_and_copies_generated_web_suite(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "kit"
            public = root / "public"
            web = source / "icons" / "web"
            logos = source / "logos" / "svg"
            logo_png = source / "logos" / "png"
            web.mkdir(parents=True)
            logos.mkdir(parents=True)
            logo_png.mkdir(parents=True)
            public.mkdir()
            (web / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"><rect width="1" height="1"/></svg>\n', encoding="utf-8")
            for name, size in (("favicon-16x16.png", 16), ("favicon-32x32.png", 32),
                               ("apple-touch-icon.png", 180), ("android-chrome-192x192.png", 192),
                               ("android-chrome-512x512.png", 512)):
                Image.new("RGBA", (size, size), (255, 255, 255, 255)).save(web / name)
            (web / "favicon.ico").write_bytes(b"\x00\x00\x01\x00test")
            (web / "site.webmanifest").write_text(json.dumps({
                "name": "ShruggieTech", "short_name": "ShruggieTech", "display": "standalone",
                "background_color": "#FFFFFF", "theme_color": "#FFFFFF",
                "icons": [{"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"}],
            }) + "\n", encoding="utf-8")
            (logos / "shruggietech-horizontal-white.svg").write_text("<svg/>\n", encoding="utf-8")
            Image.new("RGB", (1200, 630), (0, 0, 0)).save(logo_png / "shruggietech-social-preview-1280.png")

            prepare_site.copy_site_identity(source, public)

            self.assertEqual((web / "favicon.svg").read_bytes(), (public / "favicon.svg").read_bytes())
            self.assertEqual((web / "favicon.ico").read_bytes(), (public / "favicon.ico").read_bytes())
            manifest = json.loads((public / "site.webmanifest").read_text(encoding="utf-8"))
            self.assertEqual("Brands | ShruggieTech", manifest["name"])
            self.assertEqual("#FFFFFF", manifest["background_color"])

    def test_site_identity_does_not_mask_missing_generated_assets(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "kit"
            public = root / "public"
            source.mkdir()
            public.mkdir()
            with self.assertRaisesRegex(ValueError, "generated site identity asset"):
                prepare_site.copy_site_identity(source, public)


if __name__ == "__main__":
    unittest.main(verbosity=2)
