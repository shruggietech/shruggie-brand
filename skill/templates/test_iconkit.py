#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Behavioral tests for categorized native icon delivery."""

from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

from iconkit import generate_icon_suites, inspect_png, safe_reset


def brand_fixture():
    return {
        "slug": "example",
        "title": "Example",
        "surfaces": {"base": "#080B0D"},
        "logo": {
            "reduced_below_px": 32,
            "application_icon": {"background": "#FFFFFF"},
        },
    }


def fake_render(_source, target, size):
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    margin = max(1, size // 5)
    for y in range(margin, size - margin):
        for x in range(margin, size - margin):
            image.putpixel((x, y), (43, 204, 115, 255))
    image.save(target, format="PNG")


class IconKitTests(unittest.TestCase):
    def generate(self, root):
        kit = Path(root) / "kit"
        kit.mkdir()
        full = kit / "full.svg"
        reduced = kit / "reduced.svg"
        full.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0H1V1Z"/></svg>\n', encoding="utf-8")
        reduced.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0H1V1Z"/></svg>\n', encoding="utf-8")
        generate_icon_suites(
            brand_fixture(), kit, full, reduced, fake_render,
            {"tier": "full", "svg_raster": True, "ico_writer": True},
        )
        return kit

    def test_safe_reset_is_confined_to_generated_icon_roots(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary) / "kit"
            kit.mkdir()
            safe_reset(kit, kit / "icons")
            safe_reset(kit, kit / "favicons")
            with self.assertRaisesRegex(ValueError, "refusing"):
                safe_reset(kit, Path(temporary))

    def test_generates_navigable_exact_manifest_and_aliases(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            manifest = json.loads((kit / "icons" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual("1.0.0", manifest["schema_version"])
            self.assertEqual("example", manifest["brand"])
            self.assertEqual({"web", "android", "apple-ios", "apple-macos", "windows"}, {suite["id"] for suite in manifest["suites"]})
            self.assertTrue(all(suite["status"] == "generated" for suite in manifest["suites"]))
            paths = [item["path"] for item in manifest["artifacts"]]
            self.assertEqual(len(paths), len(set(paths)))
            for relative in paths:
                self.assertTrue((kit / relative).is_file(), relative)
            self.assertTrue((kit / "icons" / "README.md").is_file())
            for alias, target in manifest["aliases"].items():
                self.assertEqual((kit / alias).read_bytes(), (kit / target).read_bytes())

    def test_source_domain_icons_are_preserved_and_categorized(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary) / "kit"
            kit.mkdir()
            full = kit / "full.svg"
            reduced = kit / "reduced.svg"
            full.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0H1V1Z"/></svg>\n', encoding="utf-8")
            reduced.write_bytes(full.read_bytes())
            source = kit / "icons" / "capture.svg"
            source.parent.mkdir()
            payload = b'<svg xmlns="http://www.w3.org/2000/svg"/>\n'
            source.write_bytes(payload)
            generate_icon_suites(brand_fixture(), kit, full, reduced, fake_render, {"tier": "full", "svg_raster": True})
            preserved = kit / "icons" / "domain" / "capture.svg"
            self.assertEqual(payload, preserved.read_bytes())
            manifest = json.loads((kit / "icons" / "manifest.json").read_text(encoding="utf-8"))
            self.assertIn("icons/domain/capture.svg", {item["path"] for item in manifest["artifacts"]})
            generate_icon_suites(brand_fixture(), kit, full, reduced, fake_render, {"tier": "full", "svg_raster": True})
            self.assertEqual(payload, preserved.read_bytes())

    def test_interrupted_generated_tree_is_not_reclassified_as_domain_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary) / "kit"
            kit.mkdir()
            full = kit / "full.svg"
            reduced = kit / "reduced.svg"
            full.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0H1V1Z"/></svg>\n', encoding="utf-8")
            reduced.write_bytes(full.read_bytes())
            interrupted = kit / "icons" / "web" / "partial.svg"
            interrupted.parent.mkdir(parents=True)
            interrupted.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>\n', encoding="utf-8")
            generate_icon_suites(brand_fixture(), kit, full, reduced, fake_render, {"tier": "core", "svg_raster": False})
            self.assertFalse((kit / "icons" / "domain" / "web" / "partial.svg").exists())
            self.assertTrue((kit / "icons" / ".iconkit-generated.json").is_file())

    def test_preferred_favicon_embeds_the_reduced_mark(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary) / "kit"
            kit.mkdir()
            full = kit / "full.svg"
            reduced = kit / "reduced.svg"
            full.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path id="full" d="M0 0H1V1Z"/></svg>\n', encoding="utf-8")
            reduced.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path id="reduced" d="M0 0H1V1Z"/></svg>\n', encoding="utf-8")
            generate_icon_suites(brand_fixture(), kit, full, reduced, fake_render, {"tier": "core", "svg_raster": False})
            preferred = (kit / "icons" / "web" / "favicon.svg").read_text(encoding="utf-8")
            self.assertIn(base64.b64encode(reduced.read_bytes()).decode("ascii"), preferred)
            self.assertNotIn(base64.b64encode(full.read_bytes()).decode("ascii"), preferred)

    def test_core_vector_generation_does_not_import_pillow(self):
        module_root = str(Path(__file__).resolve().parent)
        script = "\n".join((
            "import sys, tempfile",
            "from pathlib import Path",
            "sys.path.insert(0, %s)" % json.dumps(module_root),
            "from iconkit import generate_icon_suites",
            "brand = %s" % repr(brand_fixture()),
            "with tempfile.TemporaryDirectory() as temporary:",
            "    kit = Path(temporary)",
            "    full = kit / 'full.svg'",
            "    reduced = kit / 'reduced.svg'",
            "    full.write_text('<svg xmlns=\"http://www.w3.org/2000/svg\"/>\\n', encoding='utf-8')",
            "    reduced.write_bytes(full.read_bytes())",
            "    generate_icon_suites(brand, kit, full, reduced, lambda *_: (_ for _ in ()).throw(RuntimeError('raster called')), {'tier': 'core', 'svg_raster': False})",
            "    assert (kit / 'icons' / 'web' / 'favicon.svg').is_file()",
        ))
        kwargs = {"stdin": subprocess.DEVNULL, "capture_output": True, "text": True, "check": False}
        if os.name == "nt":
            kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
        result = subprocess.run([sys.executable, "-S", "-c", script], **kwargs)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_android_matrix_and_play_artwork(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            sizes = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
            for density, size in sizes.items():
                path = kit / "icons" / "android" / "app" / "src" / "main" / "res" / ("mipmap-%s" % density) / "ic_launcher.png"
                self.assertEqual((size, size), inspect_png(path)["size"])
            res = kit / "icons" / "android" / "app" / "src" / "main" / "res"
            ET.parse(res / "mipmap-anydpi-v26" / "ic_launcher.xml")
            ET.parse(res / "values" / "ic_launcher_colors.xml")
            foreground = inspect_png(res / "drawable-nodpi" / "ic_launcher_foreground.png")
            monochrome = inspect_png(res / "drawable-nodpi" / "ic_launcher_monochrome.png")
            self.assertEqual((432, 432), foreground["size"])
            self.assertTrue(foreground["has_transparency"])
            self.assertTrue(monochrome["has_transparency"])
            play = inspect_png(kit / "icons" / "android" / "play-store" / "google-play-512.png")
            self.assertEqual((512, 512), play["size"])
            self.assertFalse(play["has_transparency"])
            self.assertEqual("RGBA", play["mode"])
            self.assertTrue(play["srgb"])
            self.assertLessEqual((kit / "icons" / "android" / "play-store" / "google-play-512.png").stat().st_size, 1024 * 1024)

    def test_apple_catalogs_and_icns(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            ios = kit / "icons" / "apple" / "ios" / "Assets.xcassets" / "AppIcon.appiconset"
            mobile = json.loads((ios / "Contents.json").read_text(encoding="utf-8"))
            self.assertEqual(3, len(mobile["images"]))
            self.assertEqual({"AppIcon-1024.png", "AppIcon-1024-dark.png", "AppIcon-1024-tinted.png"}, {row["filename"] for row in mobile["images"]})
            self.assertTrue(all(not inspect_png(ios / row["filename"])["has_transparency"] for row in mobile["images"]))
            mac = kit / "icons" / "apple" / "macos"
            catalog = json.loads((mac / "Assets.xcassets" / "AppIcon.appiconset" / "Contents.json").read_text(encoding="utf-8"))
            self.assertEqual(10, len(catalog["images"]))
            self.assertEqual(b"icns", (mac / "AppIcon.icns").read_bytes()[:4])

    def test_windows_classic_and_msix_matrix(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            ico = kit / "icons" / "windows" / "classic" / "app.ico"
            self.assertEqual(b"\x00\x00\x01\x00", ico.read_bytes()[:4])
            self.assertEqual(7, int.from_bytes(ico.read_bytes()[4:6], "little"))
            assets = kit / "icons" / "windows" / "msix" / "Assets"
            for scale, pixels in {100: 44, 200: 88, 400: 176}.items():
                self.assertEqual((pixels, pixels), inspect_png(assets / ("Square44x44Logo.scale-%d.png" % scale))["size"])
            targets = (16, 20, 24, 30, 32, 36, 40, 48, 60, 64, 72, 80, 96, 256)
            for size in targets:
                self.assertTrue((assets / ("AppList.targetsize-%d.png" % size)).is_file())
                self.assertTrue((assets / ("AppList.targetsize-%d_altform-unplated.png" % size)).is_file())
                self.assertTrue((assets / ("AppList.targetsize-%d_altform-lightunplated.png" % size)).is_file())
            ET.parse(kit / "icons" / "windows" / "msix" / "Package.appxmanifest.fragment.xml")

    def test_generation_removes_stale_outputs_and_core_records_skips(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            stale = kit / "icons" / "stale.bin"
            stale.write_bytes(b"stale")
            full = kit / "full.svg"
            reduced = kit / "reduced.svg"
            generate_icon_suites(brand_fixture(), kit, full, reduced, fake_render, {"tier": "core", "svg_raster": False})
            self.assertFalse(stale.exists())
            manifest = json.loads((kit / "icons" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual("generated", next(row for row in manifest["suites"] if row["id"] == "web")["status"])
            self.assertTrue(all(row["status"] == "skipped" for row in manifest["suites"] if row["id"] != "web"))
            self.assertTrue((kit / "icons" / "web" / "favicon.svg").is_file())
            self.assertFalse(any(path.suffix.lower() in {".png", ".ico", ".icns"} for path in (kit / "icons").rglob("*")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
