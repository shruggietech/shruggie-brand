#!/usr/bin/env python3
"""Regression tests for portability, registry, and release-critical pipeline behavior."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import gen_guide_pdf
import gen_logo
import gen_nextjs
import qc_images
import verify
from capabilities import load_capabilities
from process_utils import hidden_process_kwargs


class PipelineTests(unittest.TestCase):
    def write_probe(self, kit, tier="core", raster=False, chromium=False, ico=False):
        qc = Path(kit) / "qc"
        qc.mkdir(parents=True, exist_ok=True)
        (qc / "probe.json").write_text(
            json.dumps({"tier": tier, "svg_raster": raster, "chromium": chromium,
                        "ico_writer": ico}) + "\n",
            encoding="utf-8",
            newline="\n",
        )

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
            old_argv = sys.argv
            try:
                sys.argv = ["gen_nextjs.py", str(ROOT / "fixtures" / "example-brand" / "brand.json"), tmp]
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

    def test_core_logo_generation_keeps_vectors_and_skips_rasters(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / "example"
            shutil.copytree(ROOT / "fixtures" / "example-brand", kit)
            shutil.copytree(ROOT / "assets" / "fonts", kit / "fonts")
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
            self.assertFalse(any((kit / "favicons").iterdir()))

    def test_full_tier_page_qc_error_is_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            (kit / "brand.json").write_text(
                json.dumps({"surfaces": {"base": "#000000"}}) + "\n",
                encoding="utf-8",
                newline="\n",
            )
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

    def test_pdf_skip_is_only_allowed_without_chromium(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            brand = kit / "brand.json"
            brand.write_text("{}\n", encoding="utf-8", newline="\n")
            stale_pdf = kit / "brand-guide.pdf"
            stale_pdf.write_bytes(b"stale")
            self.write_probe(kit)
            old_argv = sys.argv
            try:
                sys.argv = ["gen_guide_pdf.py", str(brand), str(kit)]
                with mock.patch.object(gen_guide_pdf, "build", return_value="<html></html>"):
                    self.assertEqual(gen_guide_pdf.main(), 0)
                    self.assertFalse(stale_pdf.exists())
            finally:
                sys.argv = old_argv

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
            brand.write_text("{}\n", encoding="utf-8", newline="\n")
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

    def test_ico_output_follows_its_measured_capability(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp)
            png_dir = kit / "logos" / "png"
            png_dir.mkdir(parents=True)
            (png_dir / "logo.png").write_bytes(b"png")
            self.write_probe(kit, tier="raster", raster=True, ico=False)
            report = verify.Report()
            verify.c_capability_artifacts(str(kit), report)
            self.assertFalse(report.problems)
            self.assertTrue(any(skip.startswith("ico-artifact:") for skip in report.skips))

            ico = kit / "favicons" / "favicon.ico"
            ico.parent.mkdir(parents=True)
            ico.write_bytes(b"ico")
            self.write_probe(kit, tier="raster", raster=True, ico=True)
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

    def test_shruggietech_runtime_uses_native_form_and_link_semantics(self):
        source = (ROOT / "brands" / "shruggietech" / "ui_kits" /
                  "shruggie-web" / "runtime.js").read_text(encoding="utf-8")
        self.assertIn("required={required}", source)
        self.assertNotIn("<a href={href}><Button", source)
        self.assertIn('<a href={href} className={classNames("sh-button"', source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
