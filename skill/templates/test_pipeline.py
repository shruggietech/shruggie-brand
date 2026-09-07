#!/usr/bin/env python3
"""Regression tests for portability, registry, and release-critical pipeline behavior."""

import json
import base64
import copy
import hashlib
from io import BytesIO
import os
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import gen_guide_pdf
import gen_guidelines
import gen_logo
import gen_nextjs
import build_kit
import probe
import qc_images
import verify
from brand_contract import sha256_file
from capabilities import load_capabilities
from iconkit import generate_icon_suites
from process_utils import hidden_process_kwargs


def write_utf8(path, value):
    with open(str(path), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(value)


class PipelineTests(unittest.TestCase):
    def test_guideline_color_references_are_deterministic_and_complete(self):
        reference = gen_guidelines.color_reference("primary", "#2BCC73")
        self.assertEqual("#2BCC73", reference["hex"])
        self.assertEqual("rgb(43 204 115)", reference["rgb"])
        self.assertIn("hsl(", reference["hsl"])
        self.assertIn("oklch(", reference["oklch"])
        self.assertIn("lab(", reference["lab"])
        self.assertEqual("CMYK: output profile required", reference["print"])

        neutral = gen_guidelines.color_reference("border", "#262626")
        self.assertEqual("hsl(0.0 0.0% 14.9%)", neutral["hsl"])
        self.assertEqual("oklch(0.2686 0.0000 0.0)", neutral["oklch"])
        canonical = gen_guidelines.Color(reference["hex"]).convert("srgb").coords()
        for format_ in ("hsl", "oklch", "lab"):
            converted = gen_guidelines.Color(reference[format_].split(" (")[0]).convert("srgb").coords()
            self.assertLessEqual(max(abs(left - right) * 255 for left, right in zip(canonical, converted)), 0.5)

    def test_guideline_asset_groups_deduplicate_sizes_without_losing_deliveries(self):
        deliveries = [
            {"path": "icons/web/favicon-16x16.png", "family": "icon", "platform": "web", "role": "favicon", "appearance": "default", "source_variant": "reduced", "format": "png", "width": 16, "height": 16, "destination": "Web root"},
            {"path": "icons/web/favicon-32x32.png", "family": "icon", "platform": "web", "role": "favicon", "appearance": "default", "source_variant": "reduced", "format": "png", "width": 32, "height": 32, "destination": "Web root"},
        ]
        groups = gen_guidelines.group_asset_deliveries(deliveries)
        self.assertEqual(1, len(groups))
        self.assertEqual(2, len(groups[0]["deliveries"]))
        self.assertEqual("icons/web/favicon-32x32.png", groups[0]["representative"]["path"])

    def test_guideline_asset_groups_merge_macos_integration_roles_without_losing_role_data(self):
        deliveries = [
            {"path": "icons/apple/macos/Assets.xcassets/AppIcon.appiconset/icon_16x16.png", "family": "icon", "platform": "apple-macos", "role": "asset-catalog-icon", "appearance": "default", "source_variant": "full", "format": "png", "width": 16, "height": 16, "destination": "Xcode AppIcon.appiconset"},
            {"path": "icons/apple/macos/AppIcon.iconset/icon_16x16.png", "family": "icon", "platform": "apple-macos", "role": "iconset-icon", "appearance": "default", "source_variant": "full", "format": "png", "width": 16, "height": 16, "destination": "macOS AppIcon.iconset"},
        ]
        groups = gen_guidelines.group_asset_deliveries(deliveries)
        self.assertEqual(1, len(groups))
        self.assertEqual({"asset-catalog-icon", "iconset-icon"}, {item["role"] for item in groups[0]["deliveries"]})

    def test_guideline_asset_groups_merge_web_destination_roles_without_losing_role_data(self):
        deliveries = [
            {"path": "icons/web/favicon-180x180.png", "family": "icon", "platform": "web", "role": "favicon", "appearance": "default", "source_variant": "reduced", "format": "png", "width": 180, "height": 180, "destination": "Web root"},
            {"path": "icons/web/apple-touch-icon.png", "family": "icon", "platform": "web", "role": "apple-touch", "appearance": "default", "source_variant": "reduced", "format": "png", "width": 180, "height": 180, "destination": "Apple touch icon"},
            {"path": "icons/web/icon-192.png", "family": "icon", "platform": "web", "role": "installable", "appearance": "default", "source_variant": "reduced", "format": "png", "width": 192, "height": 192, "destination": "Web app manifest"},
        ]
        groups = gen_guidelines.group_asset_deliveries(deliveries)
        self.assertEqual(1, len(groups))
        self.assertEqual({"favicon", "apple-touch", "installable"}, {item["role"] for item in groups[0]["deliveries"]})

    def test_guideline_swatches_cover_every_role_and_deduplicate_equal_values(self):
        html = gen_guidelines._swatches("Dark palette", [
            ("primary", "#2BCC73"), ("ring", "#2BCC73"), ("chart-1", "#58A6FF"),
        ], "Example")
        self.assertIn("primary, ring", html)
        self.assertIn("chart-1", html)
        self.assertEqual(2, html.count('class="color-card"'))
        self.assertIn("Copy Example chart-1 OKLCH", html)

    def test_guideline_catalog_uses_manifests_and_reports_skipped_capabilities(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            (kit / "logos").mkdir()
            (kit / "icons" / "web").mkdir(parents=True)
            (kit / "logos" / "provenance.json").write_text(
                json.dumps({"derivatives": []}), encoding="utf-8")
            artifacts = []
            for size in (16, 32):
                relative = "icons/web/favicon-%dx%d.png" % (size, size)
                Image.new("RGBA", (size, size), (43, 204, 115, 255)).save(kit / relative)
                artifacts.append({"path": relative, "platform": "web", "role": "favicon",
                                  "appearance": "default", "source_variant": "reduced", "format": "png",
                                  "width": size, "height": size, "destination": "Web root"})
            instructions = "icons/web/README.md"
            (kit / instructions).write_text("# Web icon instructions\n", encoding="utf-8")
            artifacts.append({"path": instructions, "platform": "web", "role": "instructions",
                              "appearance": "default", "source_variant": "reduced", "format": "markdown",
                              "destination": "Web integration guide"})
            (kit / "icons" / "manifest.json").write_text(json.dumps({
                "artifacts": artifacts,
                "suites": [{"id": "windows-store", "status": "skipped"}],
                "aliases": {"favicon.png": "icons/web/favicon-32x32.png"},
            }), encoding="utf-8")
            (kit / "favicon.png").write_bytes((kit / "icons" / "web" / "favicon-32x32.png").read_bytes())

            catalog = gen_guidelines._asset_catalog(kit, "Example")
            self.assertEqual(1, catalog.count('class="asset-card"'))
            self.assertIn("favicon-16x16.png", catalog)
            self.assertIn("favicon-32x32.png", catalog)
            self.assertIn("favicon.png", catalog)
            self.assertIn("Integration instructions", catalog)
            self.assertIn("icons/web/README.md", catalog)
            self.assertEqual(4, catalog.count("data-kit-asset"))
            self.assertIn("Unavailable at this capability tier: windows-store", catalog)
            self.assertIn("aliases are listed with their canonical delivery group", catalog)

    def test_guideline_catalog_rejects_manifest_records_for_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            (kit / "logos").mkdir()
            (kit / "icons").mkdir()
            (kit / "logos" / "provenance.json").write_text(json.dumps({"derivatives": [{
                "path": "logos/missing.svg", "kind": "mark", "variant": "full", "colourway": "color",
            }]}), encoding="utf-8")
            (kit / "icons" / "manifest.json").write_text(json.dumps({"artifacts": []}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing file"):
                gen_guidelines.asset_deliveries(kit)

    def test_guideline_catalog_rejects_manifest_dimensions_that_disagree_with_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            (kit / "logos").mkdir()
            (kit / "icons").mkdir()
            (kit / "logos" / "provenance.json").write_text(json.dumps({"derivatives": []}), encoding="utf-8")
            Image.new("RGBA", (32, 32), (43, 204, 115, 255)).save(kit / "icons" / "mark.png")
            (kit / "icons" / "manifest.json").write_text(json.dumps({"artifacts": [{
                "path": "icons/mark.png", "platform": "web", "role": "favicon", "format": "png",
                "width": 16, "height": 16, "appearance": "default", "source_variant": "reduced",
            }]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "dimensions disagree"):
                gen_guidelines.asset_deliveries(kit)

    def test_guideline_container_sizes_are_listed_from_ico_and_icns_payloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ico = root / "app.ico"
            ico.write_bytes(b"\x00\x00\x01\x00\x02\x00" + bytes([16, 16]) + bytes(14) + bytes([0, 0]) + bytes(14))
            self.assertEqual([16, 256], gen_guidelines._container_sizes(ico, "ico"))

            icns = root / "AppIcon.icns"
            chunks = b"icp4\x00\x00\x00\x08" + b"ic10\x00\x00\x00\x08"
            icns.write_bytes(b"icns" + (len(chunks) + 8).to_bytes(4, "big") + chunks)
            self.assertEqual([16, 1024], gen_guidelines._container_sizes(icns, "icns"))

    def test_standalone_mark_ratio_honors_declared_long_edge_clear_space(self):
        brand = {"logo": {"artwork_width": 720, "artwork_height": 900, "clear_space_units": 70}}
        self.assertAlmostEqual(900.0 / 1040.0, gen_logo.standalone_mark_ratio(brand))
        brand["logo"]["artwork_width"] = 1200
        self.assertAlmostEqual(1200.0 / 1340.0, gen_logo.standalone_mark_ratio(brand))

    def test_guide_metrics_describe_the_composed_square(self):
        brand = json.loads((ROOT / "brands" / "glitchpad" / "brand.json").read_text(encoding="utf-8"))
        self.assertEqual((50.0, 1000.0, 1000.0, 900.0), gen_guide_pdf.logo_metrics(brand))
        self.assertEqual((50.0, 1000.0, 1000.0, 900.0), gen_guidelines.logo_metrics(brand))
        guidance = gen_guidelines.clear_space_guidance(brand, 50.0)
        self.assertIn("50 units of external clear space", guidance)
        self.assertIn("70-unit G channel", guidance)
        self.assertIn("not the external clear-space requirement", guidance)

    @staticmethod
    def owned_affiliation():
        return {"ownership": "shruggietech-owned", "showcase": "public", "parent": "ShruggieTech", "inheritance": "shruggietech-house", "endorsement": "shruggietech-project", "service_credit": "none"}

    def copy_production_test_input(self, destination):
        """Create an isolated test input from a production source kit."""
        shutil.copytree(ROOT / "brands" / "covarity", destination)
        shutil.copytree(ROOT / "assets" / "fonts", destination / "fonts")

    def test_manifest_uses_the_declared_kit_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            write_utf8(kit / "brand.json", json.dumps({
                "slug": "fragcap",
                "kind": "sub-brand",
                "version": "1.1.0",
                "canon": "1.1.2",
                "affiliation": self.owned_affiliation(),
            }) + "\n")
            write_utf8(kit / "tokens.css", ":root {}\n")

            build_kit.manifest(str(kit))

            manifest = json.loads((kit / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["name"], "fragcap-brand-kit")
            self.assertEqual(manifest["version"], "1.1.0")
            self.assertEqual(manifest["canon"], "1.1.2")

    def test_complete_manifest_records_verification_and_qc_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            write_utf8(kit / "brand.json", json.dumps({
                "slug": "fragcap",
                "kind": "sub-brand",
                "version": "1.1.0",
                "canon": "1.1.2",
                "affiliation": self.owned_affiliation(),
            }) + "\n")
            write_utf8(kit / "VERIFY.md", "verified\n")
            (kit / "qc").mkdir()
            write_utf8(kit / "qc" / "probe.json", "{}\n")
            (kit / "qc" / "contact-sheet.png").write_bytes(b"png")
            (kit / "icons").mkdir()
            write_utf8(kit / "icons" / "manifest.json", "{}\n")

            build_kit.manifest(str(kit), complete=True)

            manifest = json.loads((kit / "manifest.json").read_text(encoding="utf-8"))
            recorded = {item["path"] for item in manifest["files"]}
            self.assertIn("VERIFY.md", recorded)
            self.assertIn("qc/probe.json", recorded)
            self.assertIn("qc/contact-sheet.png", recorded)
            self.assertIn("icons/manifest.json", recorded)
            self.assertNotIn("manifest.json", recorded)

    def write_probe(self, kit, tier="core", raster=False, chromium=False, ico=False,
                    renderer=None, pillow=None, raster_reason=None):
        qc = Path(kit) / "qc"
        qc.mkdir(parents=True, exist_ok=True)
        renderer = raster if renderer is None else renderer
        pillow = raster if pillow is None else pillow
        if raster_reason is None and not raster:
            raster_reason = ("Pillow unavailable for required image compositing"
                             if renderer and not pillow else "SVG rasterizer unavailable")
        write_utf8(qc / "probe.json",
                   json.dumps({"tier": tier, "svg_raster": raster, "chromium": chromium,
                               "ico_writer": ico, "svg_renderer": renderer,
                               "pillow_composite": pillow,
                               "raster_reason": raster_reason}) + "\n")

    def test_capabilities_require_a_valid_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, "probe is missing"):
                load_capabilities(tmp)
            self.write_probe(tmp, tier="unknown")
            with self.assertRaisesRegex(RuntimeError, "invalid tier"):
                load_capabilities(tmp)

    def test_windows_subprocesses_are_hidden_and_noninteractive(self):
        with mock.patch.object(os, "name", "nt"):
            kwargs = hidden_process_kwargs()
        self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
        self.assertEqual(kwargs["creationflags"], getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000))

    def test_generated_nextjs_binding_uses_local_fonts_and_plural_registry_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / "input"
            self.copy_production_test_input(kit)
            old_argv = sys.argv
            try:
                sys.argv = ["gen_nextjs.py", str(kit / "brand.json"), tmp]
                gen_nextjs.main()
            finally:
                sys.argv = old_argv
            registry = Path(tmp) / "nextjs" / "registry"
            fonts_ts = (Path(tmp) / "nextjs" / "fonts.ts").read_text(encoding="utf-8")
            self.assertTrue((registry / "fonts.json").is_file())
            self.assertFalse((registry / "font.json").exists())
            self.assertIn('from "next/font/local"', fonts_ts)
            self.assertNotIn("next/font/google", fonts_ts)
            for name in ("Geist-Regular.woff2", "Geist-Medium.woff2",
                         "GeistMono-Regular.woff2", "SpaceGrotesk-Medium.woff2",
                         "SpaceGrotesk-Bold.woff2"):
                self.assertIn(name, fonts_ts)

    def test_third_party_fixed_font_pipeline_is_offline_and_ownership_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / "client-brand"
            self.copy_production_test_input(kit)
            for name in ("README.md", "SKILL.md", "NOTES.md"):
                path = kit / name
                if path.exists():
                    path.unlink()
            shutil.rmtree(kit / "ui_kits")
            brand_path = kit / "brand.json"
            brand = json.loads(brand_path.read_text(encoding="utf-8"))
            brand["slug"] = "client-brand"
            brand["id"] = "client-brand"
            brand["title"] = "Client Brand"
            brand["kind"] = "fixture"
            brand["affiliation"] = {"ownership": "third-party", "showcase": "private", "parent": None, "inheritance": "independent", "endorsement": "none", "service_credit": "brand-system-by-shruggietech"}
            brand["semantic_colors"] = {"emphasis": "#C659FF", "action": "#A000EC"}
            brand["guide"].pop("logo", None)
            brand["guide"].pop("palette", None)
            supplied_wordmark = kit / "assets" / "client-wordmark.svg"
            supplied_wordmark.parent.mkdir(parents=True, exist_ok=True)
            write_utf8(supplied_wordmark, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 100"><path fill="#F2F5FA" d="M0 0H600V100H0Z"/></svg>\n')
            supplied_wordmark_bytes = supplied_wordmark.read_bytes()
            brand["logo"]["paths"]["wordmark"] = [{"element": "image", "source": "assets/client-wordmark.svg", "x": 0, "y": 0, "width": 600, "height": 100}]
            brand["authoritative_inputs"] = [{"id": "client-wordmark", "role": "wordmark", "path": "assets/client-wordmark.svg", "format": "svg", "sha256": sha256_file(supplied_wordmark), "color_profile": "none", "usage_status": "approved", "license": "Client-approved integration fixture", "approved_transformations": ["embed-unchanged"]}]
            families = brand["typography"]["families"]
            filenames = {
                "display": [("SpaceGrotesk-Medium.ttf", 500), ("SpaceGrotesk-Bold.ttf", 700)],
                "body": [("Geist-Regular.ttf", 400), ("Geist-Medium.ttf", 500)],
                "mono": [("GeistMono-Regular.ttf", 400)],
            }
            faces = []
            for role, entries in filenames.items():
                for filename, weight in entries:
                    relative = "fonts/ttf/%s" % filename
                    faces.append({"role": role, "path": relative, "weight": weight, "style": "normal", "format": "ttf", "sha256": sha256_file(kit / relative), "license": "OFL-1.1", "provenance": "Repository licensed integration face", "usage_status": "approved"})
            brand["typography"] = {"mode": "fixed", "families": families, "faces": faces}
            write_utf8(brand_path, json.dumps(brand, indent=2) + "\n")
            completed = subprocess.run([sys.executable, str(HERE / "build_kit.py"), str(kit)], cwd=ROOT, capture_output=True, text=True, **hidden_process_kwargs())
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertEqual(supplied_wordmark_bytes, supplied_wordmark.read_bytes())
            generated = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in kit.rglob("*") if path.is_file() and path.suffix.lower() in {".css", ".html", ".js", ".json", ".jsx", ".md", ".mjs", ".svg", ".ts", ".tsx", ".txt"})
            self.assertNotIn("A ShruggieTech project", generated)
            self.assertIn("Brand system by ShruggieTech", generated)
            manifest = json.loads((kit / "manifest.json").read_text(encoding="utf-8"))
            self.assertIsNone(manifest["parent"])
            self.assertEqual("third-party", manifest["affiliation"]["ownership"])
            fonts_ts = (kit / "nextjs" / "fonts.ts").read_text(encoding="utf-8")
            self.assertNotIn("next/font/google", fonts_ts)
            self.assertIn("../fonts/ttf/Geist-Regular.ttf", fonts_ts)
            self.assertIn("data:image/svg+xml;base64,", (kit / "logos" / "svg" / "client-brand-wordmark-color.svg").read_text(encoding="utf-8"))
            semantic_outputs = "\n".join((kit / relative).read_text(encoding="utf-8") for relative in ("tokens/colors.css", "tokens/brand.tokens.json", "nextjs/globals.css"))
            self.assertNotIn("#FF5300", semantic_outputs)
            self.assertNotIn("#C24000", semantic_outputs)
            self.assertIn("#C659FF", semantic_outputs)
            self.assertIn("#A000EC", semantic_outputs)
            logo_svg = (kit / "logos" / "svg" / "client-brand-mark-color.svg").read_text(encoding="utf-8")
            guide_html = (kit / "build" / "brand-guide.print.html").read_text(encoding="utf-8")
            self.assertIn("#C659FF", logo_svg)
            self.assertNotIn("#FF5300", logo_svg)
            self.assertNotIn("inherited orange", guide_html.lower())
            self.assertNotIn("warning orange", guide_html.lower())
            self.assertNotIn("emphasis orange", guide_html.lower())

    def test_supported_raster_masters_recolour_to_png(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for extension, image in (
                    ("jpeg", Image.new("RGB", (2, 2), (240, 240, 240))),
                    ("webp", Image.new("RGBA", (2, 2), (240, 240, 240, 128)))):
                with self.subTest(extension=extension):
                    source = root / ("master." + extension)
                    target = root / ("recoloured-" + extension + ".png")
                    image.save(source, format="JPEG" if extension == "jpeg" else "WEBP")
                    gen_logo.recolour_raster(source, target, "#123456", False)
                    with Image.open(target) as rendered:
                        self.assertEqual("PNG", rendered.format)
                        self.assertEqual((18, 52, 86), rendered.convert("RGBA").getpixel((0, 0))[:3])

    def test_pdf_heading_weights_follow_typography_contract(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary) / "input"
            self.copy_production_test_input(kit)
            brand_path = kit / "brand.json"
            brand = json.loads(brand_path.read_text(encoding="utf-8"))
            old_argv = sys.argv
            try:
                sys.argv = ["gen_nextjs.py", str(brand_path), str(kit)]
                gen_nextjs.main()
            finally:
                sys.argv = old_argv
            context = gen_guide_pdf.type_context(brand)
            context.update({"display_bold": 650, "display_regular": 350})
            with mock.patch.object(gen_guide_pdf, "type_context", return_value=context):
                html = gen_guide_pdf.build(brand, kit)
            self.assertIn("h2 { font-weight:650;", html)
            self.assertIn("h3 { font-weight:350;", html)

    def test_core_logo_generation_keeps_vectors_and_skips_rasters(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / "example"
            self.copy_production_test_input(kit)
            stale_png = kit / "logos" / "png" / "stale.png"
            stale_favicon = kit / "favicons" / "stale.png"
            stale_png.parent.mkdir(parents=True)
            stale_favicon.parent.mkdir(parents=True)
            stale_png.write_bytes(b"stale")
            stale_favicon.write_bytes(b"stale")
            self.write_probe(kit)
            old_argv = sys.argv
            try:
                sys.argv = ["gen_logo.py", str(kit / "brand.json"), str(kit)]
                result = gen_logo.main()
            finally:
                sys.argv = old_argv
            self.assertEqual(result, 0)
            self.assertTrue(any((kit / "logos" / "svg").glob("*.svg")))
            self.assertFalse(any((kit / "logos" / "png").glob("*.png")))
            self.assertTrue((kit / "icons" / "web" / "favicon.svg").is_file())
            self.assertTrue((kit / "favicons" / "favicon.svg").is_file())
            self.assertFalse(any(path.suffix.lower() in {".png", ".ico", ".icns"}
                                 for path in (kit / "icons").rglob("*")))
            icon_manifest = json.loads((kit / "icons" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual({
                "full": "logos/svg/covarity-mark-color.svg",
                "reduced": "logos/svg/covarity-mark-reduced-color.svg",
                "monochrome": "logos/svg/covarity-mark-white.svg",
            }, icon_manifest["source_masters"])
            self.assertTrue(all(row["status"] == "skipped" for row in icon_manifest["suites"]
                                if row["id"] != "web"))

    def test_authoritative_logo_provenance_is_complete_and_tamper_evident(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / "shruggietech"
            shutil.copytree(ROOT / "brands" / "shruggietech", kit)
            shutil.copytree(ROOT / "assets" / "fonts", kit / "fonts")
            self.write_probe(kit)
            old_argv = sys.argv
            try:
                sys.argv = ["gen_logo.py", str(kit / "brand.json"), str(kit)]
                self.assertEqual(gen_logo.main(), 0)
            finally:
                sys.argv = old_argv
            index_path = kit / "logos" / "provenance.json"
            provenance = json.loads(index_path.read_text(encoding="utf-8"))
            paths = [item["path"] for item in provenance["derivatives"]]
            self.assertEqual(paths, sorted(paths))
            self.assertEqual(set(paths), {path.relative_to(kit).as_posix() for path in (kit / "logos" / "svg").glob("*.svg")})
            mark = next(item for item in provenance["derivatives"] if item["path"].endswith("-mark-color.svg"))
            self.assertEqual("full-mark-master", mark["input_id"])
            self.assertEqual(["recolor-mask", "resize"], mark["transformations"])
            svg_path = kit / mark["path"]
            text = svg_path.read_text(encoding="utf-8")
            self.assertIn('data-logo-source-mode="authoritative"', text)
            self.assertIn('data-authoritative-input-id="full-mark-master"', text)
            report = verify.Report()
            verify.c_logo_provenance(str(kit), json.loads((kit / "brand.json").read_text(encoding="utf-8")), report)
            self.assertFalse(report.problems)

            mutations = {}
            missing = copy.deepcopy(provenance)
            missing["derivatives"].pop()
            mutations["missing"] = missing
            extra = copy.deepcopy(provenance)
            ghost = copy.deepcopy(extra["derivatives"][-1])
            ghost["path"] = "logos/svg/ghost.svg"
            extra["derivatives"].append(ghost)
            mutations["extra"] = extra
            duplicate = copy.deepcopy(provenance)
            duplicate["derivatives"].append(copy.deepcopy(duplicate["derivatives"][-1]))
            mutations["duplicate"] = duplicate
            stale = copy.deepcopy(provenance)
            stale["derivatives"][0]["source_sha256"] = "0" * 64
            mutations["stale"] = stale
            undeclared = copy.deepcopy(provenance)
            authoritative = next(item for item in undeclared["derivatives"] if item["input_id"])
            authoritative["transformations"].append("trace")
            mutations["undeclared"] = undeclared
            for name, mutated in mutations.items():
                with self.subTest(provenance_mutation=name):
                    index_path.write_text(json.dumps(mutated, indent=2) + "\n", encoding="utf-8")
                    report = verify.Report()
                    verify.c_logo_provenance(str(kit), json.loads((kit / "brand.json").read_text(encoding="utf-8")), report)
                    self.assertTrue(report.problems)

            index_path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
            svg_path.write_text(text.replace('data-authoritative-input-id="full-mark-master"',
                                             'data-authoritative-input-id="substitute"'), encoding="utf-8")
            report = verify.Report()
            verify.c_logo_provenance(str(kit), json.loads((kit / "brand.json").read_text(encoding="utf-8")), report)
            self.assertTrue(any("metadata disagrees" in problem for problem in report.problems))

    def test_authoritative_logo_provenance_rejects_changed_mask_topology(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / "shruggietech"
            shutil.copytree(ROOT / "brands" / "shruggietech", kit)
            shutil.copytree(ROOT / "assets" / "fonts", kit / "fonts")
            self.write_probe(kit)
            old_argv = sys.argv
            try:
                sys.argv = ["gen_logo.py", str(kit / "brand.json"), str(kit)]
                self.assertEqual(gen_logo.main(), 0)
            finally:
                sys.argv = old_argv
            svg_path = kit / "logos" / "svg" / "shruggietech-mark-color.svg"
            root = verify.ET.parse(str(svg_path)).getroot()
            image = next(node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "image")
            blank = Image.new("RGBA", (919, 302), (0, 0, 0, 0))
            payload = BytesIO()
            blank.save(payload, format="PNG")
            data_url = "data:image/png;base64," + base64.b64encode(payload.getvalue()).decode("ascii")
            image.set("href", data_url)
            image.set("{http://www.w3.org/1999/xlink}href", data_url)
            verify.ET.ElementTree(root).write(str(svg_path), encoding="unicode")
            report = verify.Report()
            verify.c_logo_provenance(str(kit), json.loads((kit / "brand.json").read_text(encoding="utf-8")), report)
            self.assertTrue(any("mask topology" in problem for problem in report.problems), report.problems)

    def test_passive_svg_authority_verifies_embedded_source_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / "svg-authority"
            shutil.copytree(ROOT / "brands" / "covarity", kit)
            shutil.copytree(ROOT / "assets" / "fonts", kit / "fonts")
            (kit / "build" / "mk_paths.py").unlink()
            assets = kit / "assets"
            assets.mkdir()
            full = assets / "full.svg"
            reduced = assets / "reduced.svg"
            full.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 2"><path d="M0 0h4v2H0z"/></svg>\n', encoding="utf-8")
            reduced.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2 2"><circle cx="1" cy="1" r="1"/></svg>\n', encoding="utf-8")
            brand_path = kit / "brand.json"
            brand = json.loads(brand_path.read_text(encoding="utf-8"))
            brand["logo"]["source_mode"] = "authoritative"
            brand["logo"]["geometry_provenance"] = "imported"
            brand["logo"]["geometry_provenance_reason"] = "Passive SVG test masters are imported unchanged."
            brand["logo"]["authoritative_input_ids"] = {"full": "full-svg", "reduced": "reduced-svg"}
            brand["logo"]["paths"]["full"] = [{"element": "image", "source": "assets/full.svg", "x": 0, "y": 0, "width": 4, "height": 2}]
            brand["logo"]["paths"]["reduced"] = [{"element": "image", "source": "assets/reduced.svg", "x": 0, "y": 0, "width": 2, "height": 2}]
            brand["authoritative_inputs"] = [
                {"id": "full-svg", "role": "mark", "path": "assets/full.svg", "format": "svg", "sha256": hashlib.sha256(full.read_bytes()).hexdigest(), "color_profile": "none", "usage_status": "approved", "license": "Test fixture", "approved_transformations": ["embed-unchanged", "resize", "place-in-lockup"]},
                {"id": "reduced-svg", "role": "reduced-mark", "path": "assets/reduced.svg", "format": "svg", "sha256": hashlib.sha256(reduced.read_bytes()).hexdigest(), "color_profile": "none", "usage_status": "approved", "license": "Test fixture", "approved_transformations": ["embed-unchanged", "resize"]},
            ]
            write_utf8(brand_path, json.dumps(brand, indent=2) + "\n")
            self.write_probe(kit)
            old_argv = sys.argv
            try:
                sys.argv = ["gen_logo.py", str(brand_path), str(kit)]
                self.assertEqual(gen_logo.main(), 0)
            finally:
                sys.argv = old_argv
            report = verify.Report()
            verify.c_logo_provenance(str(kit), brand, report)
            self.assertFalse(report.problems, report.problems)

    def test_authoritative_rasters_icons_and_rendered_placement_are_tamper_evident(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / "shruggietech"
            shutil.copytree(ROOT / "brands" / "shruggietech", kit)
            shutil.copytree(ROOT / "assets" / "fonts", kit / "fonts")
            self.write_probe(kit, tier="full", raster=True, chromium=True, ico=True)

            def fake_raster(args):
                size = int(args[args.index("-w") + 1] if "-w" in args else args[args.index("-h") + 1])
                output = Path(args[args.index("-o") + 1])
                output.parent.mkdir(parents=True, exist_ok=True)
                Image.new("RGBA", (size, size), (43, 204, 115, 255)).save(output)

            old_argv = sys.argv
            try:
                with mock.patch.object(gen_logo, "raster", fake_raster):
                    sys.argv = ["gen_logo.py", str(kit / "brand.json"), str(kit)]
                    self.assertEqual(gen_logo.main(), 0)
                    brand = json.loads((kit / "brand.json").read_text(encoding="utf-8"))
                    logo_report = verify.Report()
                    verify.c_logo_provenance(str(kit), brand, logo_report)
                    self.assertFalse(logo_report.problems, logo_report.problems)
                    icon_report = verify.Report()
                    verify.c_icon_suites(str(kit), brand, icon_report)
                    self.assertFalse(icon_report.problems, icon_report.problems)

                    logo_png = kit / "logos" / "png" / "shruggietech-mark-color-1024.png"
                    original_png = logo_png.read_bytes()
                    with Image.open(logo_png) as image:
                        changed = image.convert("RGBA")
                    changed.putpixel((0, 0), (255, 0, 0, 0))
                    changed.save(logo_png)
                    logo_report = verify.Report()
                    verify.c_logo_provenance(str(kit), brand, logo_report)
                    self.assertIn("pixels disagree", "\n".join(logo_report.problems))
                    logo_png.write_bytes(original_png)

                    logo_svg = kit / "logos" / "svg" / "shruggietech-mark-color.svg"
                    original_svg = logo_svg.read_text(encoding="utf-8")
                    logo_svg.write_text(original_svg.replace('<image x="0"', '<image opacity="0" x="1"'), encoding="utf-8")
                    logo_report = verify.Report()
                    verify.c_logo_provenance(str(kit), brand, logo_report)
                    detail = "\n".join(logo_report.problems)
                    self.assertIn("changes the authoritative image placement", detail)
                    self.assertIn("hides or modifies", detail)
                    logo_svg.write_text(original_svg, encoding="utf-8")

                    with mock.patch.object(verify, "_authoritative_identity_unobscured", return_value=False):
                        logo_report = verify.Report()
                        verify.c_logo_provenance(str(kit), brand, logo_report)
                    self.assertIn("obscures authoritative identity pixels", "\n".join(logo_report.problems))

                    icon = kit / "icons" / "web" / "favicon-32x32.png"
                    with Image.open(icon) as image:
                        substitute = image.convert("RGBA")
                    substitute.putpixel((16, 16), (255, 0, 0, 255))
                    substitute.save(icon)
                    icon_report = verify.Report()
                    verify.c_icon_suites(str(kit), brand, icon_report)
                    self.assertIn("identity pixels disagree", "\n".join(icon_report.problems))
            finally:
                sys.argv = old_argv

    def test_square_enclosure_preserves_page_paths_and_contextual_roles(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / "glitchpad"
            shutil.copytree(ROOT / "brands" / "glitchpad", kit)
            shutil.copytree(ROOT / "assets" / "fonts", kit / "fonts")
            brand_path = kit / "brand.json"
            brand = json.loads(brand_path.read_text(encoding="utf-8"))
            protected_paths = [item["d"] for item in brand["logo"]["paths"]["full"]]
            self.write_probe(kit)
            old_argv = sys.argv
            try:
                sys.argv = ["gen_logo.py", str(brand_path), str(kit)]
                self.assertEqual(gen_logo.main(), 0)
            finally:
                sys.argv = old_argv
            svg_dir = kit / "logos" / "svg"
            color = (svg_dir / "glitchpad-mark-color.svg").read_text(encoding="utf-8")
            light = (svg_dir / "glitchpad-mark-light.svg").read_text(encoding="utf-8")
            reduced_color = (svg_dir / "glitchpad-mark-reduced-color.svg").read_text(encoding="utf-8")
            reduced_light = (svg_dir / "glitchpad-mark-reduced-light.svg").read_text(encoding="utf-8")
            black = (svg_dir / "glitchpad-mark-black.svg").read_text(encoding="utf-8")
            horizontal = (svg_dir / "glitchpad-horizontal-color.svg").read_text(encoding="utf-8")
            horizontal_light = (svg_dir / "glitchpad-horizontal-light.svg").read_text(encoding="utf-8")
            wordmark = (svg_dir / "glitchpad-wordmark-color.svg").read_text(encoding="utf-8")
            wordmark_light = (svg_dir / "glitchpad-wordmark-light.svg").read_text(encoding="utf-8")
            for output in (color, light, black, horizontal):
                self.assertIn('data-square-enclosure="true"', output)
                self.assertNotIn("#867100", output)
            for output in (color, light, horizontal):
                for path in protected_paths:
                    self.assertIn(path, output)
            self.assertIn(protected_paths[0], black)
            self.assertIn('viewBox="0 0 1000 1000"', color)
            self.assertIn('fill="#FFD900"', color)
            self.assertIn('fill="#0B0C0D"', color)
            self.assertIn('fill="#0B0C0D"', light)
            self.assertIn('fill="#FFD900"', light)
            self.assertIn('fill="#0B0C0D"', reduced_color)
            self.assertNotIn('fill="#667788"', reduced_color)
            self.assertIn('fill="#FFD900"', reduced_light)
            self.assertNotIn('fill="#667788"', reduced_light)
            self.assertIn("<mask", black)
            self.assertIn('fill="#F2F5FA"', horizontal)
            self.assertIn('fill="#0A0A0A"', horizontal_light)
            self.assertIn('fill="#F2F5FA"', wordmark)
            self.assertIn('fill="#0A0A0A"', wordmark_light)

    def test_full_tier_page_qc_error_is_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            write_utf8(kit / "brand.json",
                       json.dumps({"surfaces": {"base": "#000000"}}) + "\n")
            self.write_probe(kit, tier="full", raster=True, chromium=True, ico=True)
            old_argv = sys.argv
            try:
                sys.argv = ["qc_images.py", str(kit)]
                with mock.patch.object(qc_images, "logo_sheet", side_effect=RuntimeError("renderer broke")), \
                        mock.patch.object(qc_images, "page_shots", return_value=[]):
                    result = qc_images.main()
            finally:
                sys.argv = old_argv
            self.assertEqual(result, 1)

    def test_lower_tier_page_qc_removes_stale_sheets(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            qc = kit / "qc"
            qc.mkdir()
            stale_logo = qc / "logo-sheet.png"
            stale_page = qc / "pages-old.png"
            stale_logo.write_bytes(b"stale")
            stale_page.write_bytes(b"stale")
            write_utf8(kit / "brand.json", '{"surfaces":{"base":"#000000"}}\n')
            self.write_probe(kit)
            old_argv = sys.argv
            try:
                sys.argv = ["qc_images.py", str(kit)]
                self.assertEqual(qc_images.main(), 0)
            finally:
                sys.argv = old_argv
            self.assertFalse(stale_logo.exists())
            self.assertFalse(stale_page.exists())

    def test_renderer_without_pillow_records_a_named_core_skip(self):
        self.assertEqual(
            probe.raster_capability(True, False),
            (False, "Pillow unavailable for required image compositing"),
        )
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / "shruggietech"
            shutil.copytree(ROOT / "brands" / "shruggietech", kit)
            shutil.copytree(ROOT / "assets" / "fonts", kit / "fonts")
            self.write_probe(kit, renderer=True, pillow=False)
            old_argv = sys.argv
            try:
                sys.argv = ["gen_logo.py", str(kit / "brand.json"), str(kit)]
                with mock.patch.dict(sys.modules, {"PIL": None, "PIL.Image": None}):
                    self.assertEqual(gen_logo.main(), 0)
                sys.argv = ["qc_images.py", str(kit)]
                with mock.patch.dict(sys.modules, {"PIL": None, "PIL.Image": None}):
                    self.assertEqual(qc_images.main(), 0)
            finally:
                sys.argv = old_argv
            capabilities = load_capabilities(str(kit))
            self.assertIn("Pillow unavailable", capabilities["raster_reason"])
            self.assertFalse(any((kit / "logos" / "png").iterdir()))

    def test_imagemagick_is_not_measured_as_an_svg_renderer(self):
        found = {"rsvg-convert": False, "resvg": False, "inkscape": False,
                 "magick": True, "convert": False}
        self.assertFalse(probe.svg_renderer_capability(found, False))
        found["magick"] = False
        found["convert"] = True
        self.assertFalse(probe.svg_renderer_capability(found, False))

    def test_windows_convert_utility_is_not_imagemagick(self):
        windows_result = types.SimpleNamespace(
            returncode=4, stdout="", stderr="Invalid drive specification."
        )
        image_result = types.SimpleNamespace(
            returncode=0, stdout="Version: ImageMagick 6.9.13", stderr=""
        )
        with mock.patch.object(probe.subprocess, "run", return_value=windows_result):
            self.assertFalse(probe.imagemagick_convert_ok("convert.exe"))
        with mock.patch.object(probe.subprocess, "run", return_value=image_result):
            self.assertTrue(probe.imagemagick_convert_ok("convert.exe"))

    def test_ico_generation_reuses_the_validated_converter_result(self):
        capabilities = {
            "cli": {"magick": False, "convert": False},
            "modules": {"PIL": True},
            "ico_writer": True,
        }
        with mock.patch.object(gen_logo.shutil, "which", return_value="convert.exe"):
            self.assertIsNone(gen_logo.measured_ico_converter(capabilities))

        capabilities["cli"]["convert"] = True
        self.assertEqual(gen_logo.measured_ico_converter(capabilities), "convert")

    def test_svg_consumers_do_not_use_imagemagick(self):
        def which(name):
            return "magick.exe" if name == "magick" else None

        with mock.patch.object(qc_images.shutil, "which", side_effect=which), \
                mock.patch.object(qc_images, "NODE", None):
            with self.assertRaises(RuntimeError):
                qc_images.rsvg("mark.svg", 64)
        with mock.patch.object(gen_logo.shutil, "which", side_effect=which), \
                mock.patch.object(gen_logo, "NODE", None):
            with self.assertRaises(RuntimeError):
                gen_logo.raster(["-w", "64", "mark.svg", "-o", "mark.png"])

    def test_pdf_skip_is_only_allowed_without_chromium(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            brand = kit / "brand.json"
            write_utf8(brand, "{}\n")
            stale_pdf = kit / "brand-guide.pdf"
            stale_pdf.write_bytes(b"stale")
            stale_contact = kit / "qc" / "contact-sheet.png"
            stale_page = kit / "qc" / "_pdf-pages" / "p-1.png"
            stale_contact.parent.mkdir()
            stale_contact.write_bytes(b"stale")
            stale_page.parent.mkdir()
            stale_page.write_bytes(b"stale")
            self.write_probe(kit)
            old_argv = sys.argv
            try:
                sys.argv = ["gen_guide_pdf.py", str(brand), str(kit)]
                with mock.patch.object(gen_guide_pdf, "build", return_value="<html></html>"):
                    self.assertEqual(gen_guide_pdf.main(), 0)
                    self.assertFalse(stale_pdf.exists())
                    self.assertFalse(stale_contact.exists())
                    self.assertFalse(stale_page.parent.exists())
            finally:
                sys.argv = old_argv

    def test_pagination_skips_when_playwright_is_unavailable(self):
        with tempfile.TemporaryDirectory() as temporary:
            html = Path(temporary) / "guide.html"
            write_utf8(html, "<!doctype html><title>Guide</title><p>Body</p>\n")
            completed = subprocess.run(
                [sys.executable, "-S", str(HERE / "qc_paginate.py"), str(html)],
                capture_output=True,
                text=True,
                **hidden_process_kwargs()
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertIn("pagination: SKIP, headless Chromium unavailable", completed.stdout)

    def test_pdf_failure_after_full_probe_is_fatal(self):
        class BrokenChromium:
            def launch(self):
                raise RuntimeError("launch failed")

        class FakePlaywright:
            chromium = BrokenChromium()

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

        sync_api = types.ModuleType("playwright.sync_api")
        sync_api.sync_playwright = lambda: FakePlaywright()
        playwright = types.ModuleType("playwright")
        playwright.sync_api = sync_api

        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            brand = kit / "brand.json"
            write_utf8(brand, "{}\n")
            self.write_probe(kit, tier="full", raster=True, chromium=True, ico=True)
            old_argv = sys.argv
            try:
                sys.argv = ["gen_guide_pdf.py", str(brand), str(kit)]
                with mock.patch.object(gen_guide_pdf, "build", return_value="<html></html>"), \
                        mock.patch.dict(sys.modules, {"playwright": playwright,
                                                      "playwright.sync_api": sync_api}):
                    self.assertEqual(gen_guide_pdf.main(), 1)
            finally:
                sys.argv = old_argv

    def test_generated_forms_forward_required(self):
        source = (HERE / "gen_vanilla.py").read_text(encoding="utf-8")
        self.assertEqual(source.count("required={required}"), 2)

    def test_generated_anchor_default_does_not_force_hover_underlines(self):
        source = (HERE / "gen_vanilla.py").read_text(encoding="utf-8")
        self.assertNotIn("a:hover {{ text-decoration: underline; }}", source)
        self.assertIn("a:hover {{ color: var(--{p}-link); }}", source)

    def test_ico_output_follows_its_measured_capability(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            png_dir = kit / "logos" / "png"
            png_dir.mkdir(parents=True)
            (png_dir / "logo.png").write_bytes(b"png")
            self.write_probe(kit, tier="raster", raster=True, ico=False)
            report = verify.Report()
            verify.c_capability_artifacts(str(kit), report)
            self.assertTrue(any(problem.startswith("ico-artifact:") for problem in report.problems))

            ico = kit / "favicons" / "favicon.ico"
            ico.parent.mkdir(parents=True)
            ico.write_bytes(b"ico")
            self.write_probe(kit, tier="raster", raster=True, ico=False)
            report = verify.Report()
            verify.c_capability_artifacts(str(kit), report)
            self.assertFalse(report.problems)
            self.assertTrue(any(row[0] == "ico-artifact" and row[1] == "pass"
                                for row in report.rows))

            ico.unlink()
            self.write_probe(kit, tier="core", raster=False, ico=True)
            report = verify.Report()
            verify.c_capability_artifacts(str(kit), report)
            self.assertFalse(report.problems)
            self.assertTrue(any(skip.startswith("ico-artifact:") for skip in report.skips))

    def test_icon_suite_verifier_rejects_corrupt_unsafe_and_stale_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / "kit"
            kit.mkdir()
            full = kit / "full.svg"
            reduced = kit / "reduced.svg"
            full.write_text('<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0H1V1Z"/></svg>\n', encoding="utf-8")
            reduced.write_text(full.read_text(encoding="utf-8"), encoding="utf-8")
            brand = {"slug": "example", "title": "Example", "surfaces": {"base": "#000000"},
                     "logo": {"reduced_below_px": 32, "application_icon": {"background": "#FFFFFF"}}}

            def render(_source, target, size):
                image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
                for y in range(size // 4, size * 3 // 4):
                    for x in range(size // 4, size * 3 // 4):
                        image.putpixel((x, y), (43, 204, 115, 255))
                image.save(target)

            capabilities = {"tier": "full", "svg_raster": True, "ico_writer": True}
            generate_icon_suites(brand, kit, full, reduced, render, capabilities)
            self.write_probe(kit, tier="full", raster=True, chromium=True, ico=True)
            manifest_path = kit / "icons" / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["artifacts"][0]["path"] = "../escape.md"
            missing_mac = "icons/apple/macos/AppIcon.iconset/icon_512x512@2x.png"
            manifest["artifacts"] = [item for item in manifest["artifacts"] if item["path"] != missing_mac]
            mac_manifest_path = kit / "icons" / "apple" / "macos" / "manifest.json"
            mac_manifest = json.loads(mac_manifest_path.read_text(encoding="utf-8"))
            mac_manifest["artifacts"] = [item for item in mac_manifest["artifacts"] if item["path"] != missing_mac]
            write_utf8(mac_manifest_path, json.dumps(mac_manifest, indent=2) + "\n")
            (kit / missing_mac).unlink()
            ios_contents_path = kit / "icons" / "apple" / "ios" / "Assets.xcassets" / "AppIcon.appiconset" / "Contents.json"
            ios_contents = json.loads(ios_contents_path.read_text(encoding="utf-8"))
            ios_contents["images"][0]["filename"] = "missing.png"
            write_utf8(ios_contents_path, json.dumps(ios_contents, indent=2) + "\n")
            visual_fragment = kit / "icons" / "windows" / "msix" / "ApplicationVisualElements.fragment.xml"
            write_utf8(visual_fragment, '<?xml version="1.0" encoding="utf-8"?>\n<ApplicationVisualElements/>\n')
            write_utf8(manifest_path, json.dumps(manifest, indent=2) + "\n")
            (kit / "icons" / "undeclared.bin").write_bytes(b"stale")
            (kit / "favicons" / "favicon.svg").write_text("drift\n", encoding="utf-8")
            (kit / "icons" / "windows" / "classic" / "app.ico").write_bytes(b"broken")
            touch = kit / "icons" / "web" / "apple-touch-icon.png"
            Image.new("RGBA", (180, 180), (43, 204, 115, 0)).save(touch)
            Image.new("RGB", (32, 32), (43, 204, 115)).save(kit / "icons" / "web" / "favicon-32x32.png")
            report = verify.Report()
            verify.c_icon_suites(str(kit), brand, report)
            detail = "\n".join(report.problems)
            self.assertIn("unsafe path", detail)
            self.assertIn("undeclared icon files", detail)
            self.assertIn("compatibility alias differs", detail)
            self.assertIn("native icon container is invalid", detail)
            self.assertIn("must be opaque", detail)
            self.assertIn("color mode RGB", detail)
            self.assertIn("lacks an sRGB declaration", detail)
            self.assertIn("required platform artifacts are absent", detail)
            self.assertIn("iOS Contents.json does not match", detail)
            self.assertIn("ApplicationVisualElements.fragment.xml does not match", detail)

            generate_icon_suites(brand, kit, full, reduced, render, capabilities)
            self.write_probe(kit, tier="full", raster=True, chromium=True, ico=True)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["aliases"] = {}
            write_utf8(manifest_path, json.dumps(manifest, indent=2) + "\n")
            shutil.rmtree(kit / "favicons")
            alias_report = verify.Report()
            verify.c_icon_suites(str(kit), brand, alias_report)
            self.assertIn("required favicon aliases", "\n".join(alias_report.problems))

    def test_shruggietech_runtime_uses_native_form_and_link_semantics(self):
        kit = ROOT / "brands" / "shruggietech" / "ui_kits" / "shruggie-web"
        runtime = (kit / "runtime.js").read_text(encoding="utf-8")
        all_scripts = "\n".join(path.read_text(encoding="utf-8")
                                for path in kit.glob("*.js"))
        self.assertIn("required={required}", runtime)
        self.assertNotIn('<Button variant="primary" size="sm">Get in Touch</Button>',
                         all_scripts)
        self.assertIn('<a href={href} className={classNames("sh-button"', runtime)

    def test_ui_fixtures_have_mobile_overflow_guards(self):
        glitchpad = (ROOT / "brands" / "glitchpad" / "ui_kits" /
                     "glitchpad-web" / "index.html").read_text(encoding="utf-8")
        shruggie = (ROOT / "brands" / "shruggietech" / "ui_kits" /
                    "shruggie-web" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("--gp-", glitchpad)
        self.assertNotIn('class="gp-', glitchpad)
        self.assertIn("grid-template-columns: minmax(0, 1fr)", glitchpad)
        self.assertIn(".bytes { display: block; overflow-x: auto", glitchpad)
        self.assertIn(".site-nav{display:none!important}", shruggie)


if __name__ == "__main__":
    unittest.main(verbosity=2)
