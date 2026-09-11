#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Behavioral tests for categorized native icon delivery."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

from apply_supplied_icons import apply_supplied_targets
from iconkit import contain_visible, generate_icon_suites, inspect_png, safe_reset


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


def topology_render(source, target, size):
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    margin = size // 10
    for y in range(margin, size - margin):
        for x in range(margin, size - margin):
            image.putpixel((x, y), (43, 204, 115, 255))
    if Path(source).name == "monochrome.svg":
        for y in range(size * 3 // 10, size * 7 // 10):
            for x in range(size * 3 // 10, size * 7 // 10):
                image.putpixel((x, y), (0, 0, 0, 0))
    image.save(target, format="PNG")


class IconKitTests(unittest.TestCase):
    def test_contain_visible_centers_portrait_landscape_and_offset_ink(self):
        cases = ((30, 70, (9, 4)), (70, 30, (4, 11)), (43, 61, (31, 7)))
        for width, height, offset in cases:
            with self.subTest(width=width, height=height, offset=offset):
                source = Image.new("RGBA", (120, 100), (0, 0, 0, 0))
                for y in range(offset[1], offset[1] + height):
                    for x in range(offset[0], offset[0] + width):
                        source.putpixel((x, y), (43, 204, 115, 255))
                contained = contain_visible(source, 101, 0.72)
                box = contained.getchannel("A").getbbox()
                self.assertLessEqual(abs(box[0] - (101 - box[2])), 1)
                self.assertLessEqual(abs(box[1] - (101 - box[3])), 1)
                self.assertLessEqual(max(box[2] - box[0], box[3] - box[1]), 73)

    def test_contain_visible_rejects_empty_and_invalid_inputs(self):
        empty = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
        with self.assertRaisesRegex(ValueError, "no visible pixels"):
            contain_visible(empty, 16, 0.72)
        visible = Image.new("RGBA", (10, 10), (43, 204, 115, 255))
        for size, ratio in ((0, 0.72), (16, 0), (16, 1.01)):
            with self.assertRaisesRegex(ValueError, "size|ratio"):
                contain_visible(visible, size, ratio)

    def test_platform_roles_retain_distinct_occupancy(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            legacy = inspect_png(kit / "icons" / "android" / "app" / "src" / "main" / "res" / "mipmap-xxxhdpi" / "ic_launcher.png", "#FFFFFF")
            adaptive = inspect_png(kit / "icons" / "android" / "app" / "src" / "main" / "res" / "drawable-nodpi" / "ic_launcher_foreground.png")
            play = inspect_png(kit / "icons" / "android" / "play-store" / "google-play-512.png", "#FFFFFF")
            self.assertLessEqual(max(legacy["content_bbox"][2] - legacy["content_bbox"][0], legacy["content_bbox"][3] - legacy["content_bbox"][1]), 139)
            self.assertLessEqual(max(adaptive["visible_bbox"][2] - adaptive["visible_bbox"][0], adaptive["visible_bbox"][3] - adaptive["visible_bbox"][1]), 264)
            self.assertLessEqual(max(play["content_bbox"][2] - play["content_bbox"][0], play["content_bbox"][3] - play["content_bbox"][1]), 384)

    def test_platform_monochrome_exports_preserve_interior_knockout(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary) / "kit"
            kit.mkdir()
            full = kit / "full.svg"
            reduced = kit / "reduced.svg"
            monochrome = kit / "monochrome.svg"
            for source in (full, reduced, monochrome):
                source.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>\n', encoding="utf-8")
            generate_icon_suites(
                brand_fixture(), kit, full, reduced, topology_render,
                {"tier": "full", "svg_raster": True, "ico_writer": True},
                monochrome_svg=monochrome,
            )
            manifest = json.loads((kit / "icons" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual({"full": "full.svg", "reduced": "reduced.svg", "monochrome": "monochrome.svg"},
                             manifest["source_masters"])
            for suite in manifest["suites"]:
                child = json.loads((kit / suite["manifest"]).read_text(encoding="utf-8"))
                self.assertEqual(manifest["source_masters"], child["source_masters"])
            android = kit / "icons" / "android" / "app" / "src" / "main" / "res" / "drawable-nodpi" / "ic_launcher_monochrome.png"
            ios = kit / "icons" / "apple" / "ios" / "Assets.xcassets" / "AppIcon.appiconset" / "AppIcon-1024-tinted.png"
            with Image.open(android) as image:
                rgba = image.convert("RGBA")
                self.assertEqual(0, rgba.getpixel((216, 216))[3])
                self.assertEqual(255, rgba.getpixel((216, 100))[3])
            with Image.open(ios) as image:
                rgb = image.convert("RGB")
                self.assertEqual((255, 255, 255), rgb.getpixel((512, 512)))
                self.assertEqual((0, 0, 0), rgb.getpixel((512, 256)))

    def test_explicitly_unavailable_monochrome_omits_platform_derivatives(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary) / "kit"
            kit.mkdir()
            full = kit / "full.svg"
            reduced = kit / "reduced.svg"
            for source in (full, reduced):
                source.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>\n', encoding="utf-8")
            manifest = generate_icon_suites(
                brand_fixture(), kit, full, reduced, fake_render,
                {"tier": "full", "svg_raster": True, "ico_writer": True},
                monochrome_svg=None,
            )
            self.assertIsNone(manifest["source_masters"]["monochrome"])
            android = kit / "icons" / "android" / "app" / "src" / "main" / "res"
            self.assertFalse((android / "drawable-nodpi" / "ic_launcher_monochrome.png").exists())
            adaptive = (android / "mipmap-anydpi-v26" / "ic_launcher.xml").read_text(encoding="utf-8")
            self.assertNotIn("<monochrome", adaptive)
            ios = kit / "icons" / "apple" / "ios" / "Assets.xcassets" / "AppIcon.appiconset"
            self.assertFalse((ios / "AppIcon-1024-tinted.png").exists())
            contents = json.loads((ios / "Contents.json").read_text(encoding="utf-8"))
            self.assertNotIn("tinted", {image.get("appearances", [{}])[0].get("value") for image in contents["images"]})

    def test_supplied_favicon_target_replaces_generated_bytes_exactly(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary) / "kit"
            kit.mkdir()
            full = kit / "full.svg"
            reduced = kit / "reduced.svg"
            for source in (full, reduced):
                source.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>\n', encoding="utf-8")
            supplied = kit / "source.png"
            Image.new("RGBA", (32, 32), (197, 52, 44, 127)).save(supplied, format="PNG")
            brand = brand_fixture()
            brand["logo"]["application_icon"].update({
                "monochrome_platforms": False,
                "supplied_targets": [{
                    "source": "source.png",
                    "sha256": hashlib.sha256(supplied.read_bytes()).hexdigest(),
                    "target": "icons/web/favicon-32x32.png",
                }],
            })
            manifest = generate_icon_suites(
                brand, kit, full, reduced, fake_render,
                {"tier": "full", "svg_raster": True, "ico_writer": True},
            )
            target = kit / "icons" / "web" / "favicon-32x32.png"
            self.assertEqual(supplied.read_bytes(), target.read_bytes())
            record = next(item for item in manifest["artifacts"] if item["path"] == "icons/web/favicon-32x32.png")
            self.assertEqual("source-preserved", record["source_variant"])
            self.assertEqual("transparent", record["alpha"])
            self.assertIsNone(manifest["source_masters"]["monochrome"])

    def test_core_tier_copies_and_records_supplied_platform_targets(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary) / "kit"
            kit.mkdir()
            full = kit / "full.svg"
            reduced = kit / "reduced.svg"
            for source in (full, reduced):
                source.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>\n', encoding="utf-8")
            supplied_web = kit / "source-web.png"
            supplied_android = kit / "source-android.png"
            Image.new("RGBA", (32, 32), (197, 52, 44, 127)).save(supplied_web, format="PNG")
            Image.new("RGBA", (48, 48), (197, 52, 44, 127)).save(supplied_android, format="PNG")
            brand = brand_fixture()
            brand["logo"]["application_icon"].update({
                "monochrome_platforms": False,
                "supplied_targets": [
                    {"source": "source-web.png", "sha256": hashlib.sha256(supplied_web.read_bytes()).hexdigest(),
                     "target": "icons/web/favicon-32x32.png"},
                    {"source": "source-android.png", "sha256": hashlib.sha256(supplied_android.read_bytes()).hexdigest(),
                     "target": "icons/android/app/src/main/res/mipmap-mdpi/ic_launcher.png"},
                ],
            })
            manifest = generate_icon_suites(
                brand, kit, full, reduced, fake_render,
                {"tier": "core", "svg_raster": False, "raster_reason": "test core tier"},
            )
            manifest = apply_supplied_targets(brand, kit)
            web_target = kit / "icons" / "web" / "favicon-32x32.png"
            android_target = kit / "icons" / "android" / "app" / "src" / "main" / "res" / "mipmap-mdpi" / "ic_launcher.png"
            self.assertEqual(supplied_web.read_bytes(), web_target.read_bytes())
            self.assertEqual(supplied_android.read_bytes(), android_target.read_bytes())
            records = {item["path"]: item for item in manifest["artifacts"]}
            self.assertEqual("source-preserved", records["icons/web/favicon-32x32.png"]["source_variant"])
            self.assertEqual("source-preserved", records["icons/android/app/src/main/res/mipmap-mdpi/ic_launcher.png"]["source_variant"])
            web_manifest = json.loads((kit / "icons" / "web" / "manifest.json").read_text(encoding="utf-8"))
            android_manifest = json.loads((kit / "icons" / "android" / "manifest.json").read_text(encoding="utf-8"))
            self.assertIn("icons/web/favicon-32x32.png", {item["path"] for item in web_manifest["artifacts"]})
            self.assertIn("icons/android/app/src/main/res/mipmap-mdpi/ic_launcher.png",
                          {item["path"] for item in android_manifest["artifacts"]})
            self.assertEqual("icons/web/favicon-32x32.png", manifest["aliases"]["favicons/favicon-32x32.png"])

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
                self.assertTrue((assets / ("Square44x44Logo.targetsize-%d.png" % size)).is_file())
                self.assertTrue((assets / ("Square44x44Logo.targetsize-%d_altform-unplated.png" % size)).is_file())
                self.assertTrue((assets / ("Square44x44Logo.targetsize-%d_altform-lightunplated.png" % size)).is_file())
            msix = kit / "icons" / "windows" / "msix"
            visual = ET.parse(msix / "ApplicationVisualElements.fragment.xml").getroot()
            self.assertEqual("{http://schemas.microsoft.com/appx/manifest/uap/windows10}VisualElements", visual.tag)
            self.assertEqual("Assets\\Square44x44Logo.png", visual.attrib["Square44x44Logo"])
            properties = ET.parse(msix / "PackageProperties.fragment.xml").getroot()
            namespace = "{http://schemas.microsoft.com/appx/manifest/foundation/windows10}"
            self.assertEqual(namespace + "Properties", properties.tag)
            self.assertEqual("Assets\\StoreLogo.png", properties.find(namespace + "Logo").text)

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
