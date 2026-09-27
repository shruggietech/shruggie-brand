#!/usr/bin/env python3
"""Isolated WordPress generator, inventory, and source-authority regression tests."""

import base64
import hashlib
import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from color_roles import resolve_color_roles
from gen_wordpress import WordPressError, generate_wordpress, theme_settings
from interface_contract import load_brand_canon, resolve_interface_contract
from verify_wordpress import verify_wordpress


ROOT = Path(__file__).resolve().parents[2]
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/lXcAAAAASUVORK5CYII=")


class WordPressGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.kit = Path(self.temp.name) / "kit"
        self.kit.mkdir()
        brand = json.loads((ROOT / "brands" / "go-schedule" / "brand.json").read_text(encoding="utf-8"))
        (self.kit / "brand.json").write_text(json.dumps(brand), encoding="utf-8")
        (self.kit / "color-roles.json").write_text(json.dumps(resolve_color_roles(brand, load_brand_canon())), encoding="utf-8")
        shutil.copytree(ROOT / "assets" / "fonts", self.kit / "fonts")
        logo_dir = self.kit / "logos" / "png"
        logo_dir.mkdir(parents=True)
        for name, size in (("horizontal-black", 1024), ("mark-black", 1024), ("social-preview", 1280)):
            (logo_dir / ("go-schedule-%s-%d.png" % (name, size))).write_bytes(PNG)
        self.brand = brand

    def generate(self):
        return generate_wordpress(self.kit / "brand.json", self.kit)

    def test_installer_and_source_mapping(self):
        manifest = self.generate()
        self.assertEqual(manifest["adapter_version"], "1.0.0")
        self.assertGreater(verify_wordpress(self.kit), 15)
        settings = json.loads((self.kit / manifest["entries"]["theme_json"]).read_text(encoding="utf-8"))
        palette = {item["slug"]: item["color"] for item in settings["settings"]["color"]["palette"]}
        self.assertEqual(palette["stbb-go-schedule-identity-primary"], "#58A6FF")
        self.assertIn("stbb-go-schedule-cue-action", palette)
        self.assertNotIn("stbb-go-schedule-border-default", palette)
        self.assertTrue(all(item["color"].startswith("#") for item in settings["settings"]["color"]["palette"]))
        self.assertNotEqual(palette["stbb-go-schedule-identity-primary"], palette["stbb-go-schedule-cue-action"])
        dark = json.loads((self.kit / "wordpress" / "theme" / "stbb-go-schedule" / "styles" / "dark.json").read_text(encoding="utf-8"))
        dark_palette = {item["slug"]: item["color"] for item in dark["settings"]["color"]["palette"]}
        self.assertEqual(dark_palette["stbb-go-schedule-identity-primary"], palette["stbb-go-schedule-identity-primary"])
        self.assertNotEqual(dark_palette["stbb-go-schedule-surface-background"], palette["stbb-go-schedule-surface-background"])
        css = (self.kit / "wordpress" / "theme" / "stbb-go-schedule" / "assets" / "css" / "stbb-content.css").read_text(encoding="utf-8")
        self.assertIn(":is(.wp-site-blocks, .editor-styles-wrapper) :is(a, button, .wp-element-button, input, select, textarea):focus-visible", css)
        self.assertIn("outline: 2px solid var(--wp--preset--color--stbb-go-schedule-focus-ring)", css)
        self.assertIn("border: 1px solid var(--wp--preset--color--stbb-go-schedule-text-muted)", css)
        media_pattern = (self.kit / "wordpress" / "theme" / "stbb-go-schedule" / "patterns" / "text-media.php").read_text(encoding="utf-8")
        self.assertIn("get_theme_file_uri", media_pattern)
        self.assertIn("go-schedule-social-preview-1280.png", media_pattern)
        self.assertNotIn("<!-- wp:image /-->", media_pattern)
        header = (self.kit / "wordpress" / "theme" / "stbb-go-schedule" / "parts" / "header.html").read_text(encoding="utf-8")
        self.assertIn('<!-- wp:home-link {"label":"Home"} /-->', header)

    def test_missing_font_fails(self):
        (self.kit / "fonts" / "woff2" / "Geist-Regular.woff2").unlink()
        with self.assertRaisesRegex(WordPressError, "font asset is missing"):
            self.generate()

    def test_missing_approved_image_fails(self):
        (self.kit / "logos" / "png" / "go-schedule-mark-black-1024.png").unlink()
        with self.assertRaisesRegex(WordPressError, "approved raster asset is missing"):
            self.generate()

    def test_missing_optional_social_preview_uses_approved_mark(self):
        self.generate()
        (self.kit / "logos" / "png" / "go-schedule-social-preview-1280.png").unlink()
        manifest = self.generate()
        media = (self.kit / "wordpress" / "theme" / "stbb-go-schedule" / "patterns" / "text-media.php").read_text(encoding="utf-8")
        self.assertIn("go-schedule-mark-black-1024.png", media)
        self.assertIn("stbb-go-schedule-sample-mark", media)
        stale = "assets/images/go-schedule-social-preview-1280.png"
        self.assertFalse((self.kit / "wordpress" / "theme" / "stbb-go-schedule" / stale).exists())
        self.assertNotIn(stale, {item["path"] for item in json.loads((self.kit / "wordpress" / "theme-inventory.json").read_text(encoding="utf-8"))["files"]})
        with zipfile.ZipFile(self.kit / manifest["entries"]["zip"]) as archive:
            self.assertNotIn("stbb-go-schedule/" + stale, archive.namelist())
        self.assertGreater(verify_wordpress(self.kit), 15)

    def test_core_tier_packages_source_exact_vector_assets(self):
        (self.kit / "qc").mkdir()
        (self.kit / "qc" / "probe.json").write_text('{"svg_raster": false}\n', encoding="utf-8")
        svg_dir = self.kit / "logos" / "svg"
        svg_dir.mkdir()
        embedded = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg"/>').decode("ascii")
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><image href="data:image/svg+xml;base64,%s"/></svg>\n' % embedded).encode("utf-8")
        for name in ("horizontal-black", "mark-black"):
            (svg_dir / ("go-schedule-%s.svg" % name)).write_bytes(svg)
        shutil.rmtree(self.kit / "logos" / "png")
        manifest = self.generate()
        media = (self.kit / "wordpress" / "theme" / "stbb-go-schedule" / "patterns" / "text-media.php").read_text(encoding="utf-8")
        self.assertIn("go-schedule-mark-black.svg", media)
        self.assertIn("vector theme assets only", (self.kit / "wordpress" / "README.md").read_text(encoding="utf-8"))
        self.assertEqual(verify_wordpress(self.kit), len(json.loads((self.kit / "wordpress" / "theme-inventory.json").read_text(encoding="utf-8"))["files"]))
        with zipfile.ZipFile(self.kit / manifest["entries"]["zip"]) as archive:
            self.assertIn("stbb-go-schedule/assets/images/go-schedule-mark-black.svg", archive.namelist())

    def test_stylesheet_cache_version_follows_css_bytes(self):
        self.generate()
        theme = self.kit / "wordpress" / "theme" / "stbb-go-schedule"
        css = (theme / "assets" / "css" / "stbb-content.css").read_text(encoding="utf-8")
        original_version = hashlib.sha256(css.encode("utf-8")).hexdigest()
        functions = (theme / "functions.php").read_text(encoding="utf-8")
        self.assertIn("array(), '%s'" % original_version, functions)
        with patch("gen_wordpress.content_css", return_value=css + "/* source revision */\n"):
            self.generate()
        updated_css = (theme / "assets" / "css" / "stbb-content.css").read_bytes()
        updated_version = hashlib.sha256(updated_css).hexdigest()
        self.assertNotEqual(updated_version, original_version)
        self.assertIn("array(), '%s'" % updated_version, (theme / "functions.php").read_text(encoding="utf-8"))

    def test_archive_tamper_fails(self):
        manifest = self.generate()
        target = self.kit / manifest["entries"]["zip"]
        target.write_bytes(target.read_bytes() + b"tamper")
        with self.assertRaisesRegex(WordPressError, "ZIP checksum disagrees"):
            verify_wordpress(self.kit)

    def test_archive_traversal_fails_before_inventory_lookup(self):
        manifest = self.generate()
        target = self.kit / manifest["entries"]["zip"]
        with zipfile.ZipFile(target) as archive:
            members = [(item.filename, archive.read(item.filename)) for item in archive.infolist()]
        with zipfile.ZipFile(target, "w") as archive:
            for index, (name, payload) in enumerate(members):
                archive.writestr("../escape" if index == 0 else name, payload)
        manifest["zip"] = {"bytes": target.stat().st_size, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
        (self.kit / "wordpress" / "adapter.json").write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(WordPressError, "archive contains an unsafe path"):
            verify_wordpress(self.kit)

    def test_unsupported_theme_format_fails(self):
        manifest = self.generate()
        path = self.kit / manifest["entries"]["theme_json"]
        settings = json.loads(path.read_text(encoding="utf-8"))
        settings["version"] = 4
        path.write_text(json.dumps(settings), encoding="utf-8")
        with self.assertRaisesRegex(WordPressError, "theme.json identity or format disagrees"):
            verify_wordpress(self.kit)

    def test_dark_palette_drift_fails(self):
        self.generate()
        path = self.kit / "wordpress" / "theme" / "stbb-go-schedule" / "styles" / "dark.json"
        dark = json.loads(path.read_text(encoding="utf-8"))
        dark["settings"]["color"]["palette"][0]["color"] = "#000000"
        path.write_text(json.dumps(dark), encoding="utf-8")
        with self.assertRaisesRegex(WordPressError, "dark variation is not source-derived"):
            verify_wordpress(self.kit)

    def test_full_slug_is_used_for_namespace(self):
        self.generate()
        text = (self.kit / "wordpress" / "theme" / "stbb-go-schedule" / "theme.json").read_text(encoding="utf-8")
        self.assertIn("stbb-go-schedule-identity-primary", text)
        self.assertNotIn('"stbb-go-identity-primary"', text)

    def test_independent_brand_palette_and_shared_prefix_remain_distinct(self):
        self.generate()
        interface = resolve_interface_contract(self.brand)
        source_colors = json.loads((self.kit / "color-roles.json").read_text(encoding="utf-8"))
        alternate = json.loads(json.dumps(source_colors))
        alternate["identity"][0]["hex"] = "#123456"
        sibling = json.loads(json.dumps(self.brand))
        sibling["slug"] = "go-second"
        settings = theme_settings(sibling, interface, alternate, [])
        palette = {item["slug"]: item["color"] for item in settings["settings"]["color"]["palette"]}
        self.assertEqual(palette["stbb-go-second-identity-primary"], "#123456")
        self.assertNotIn("stbb-go-schedule-identity-primary", palette)


if __name__ == "__main__":
    unittest.main()
