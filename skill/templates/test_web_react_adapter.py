#!/usr/bin/env python3
"""Generated Web/React adapter regression tests."""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from component_contract import COMPONENT_IDS, RESPONSIBILITIES  # noqa: E402
from gen_web_react import generate_web_react  # noqa: E402


class WebReactAdapterTests(unittest.TestCase):
    def generate(self, root):
        kit = Path(root) / "shruggietech"
        kit.mkdir()
        shutil.copy2(ROOT / "brands" / "shruggietech" / "brand.json", kit / "brand.json")
        generate_web_react(kit / "brand.json", kit)
        return kit

    def test_output_is_deterministic_complete_and_server_safe(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            tracked = {
                path.relative_to(kit).as_posix(): path.read_bytes()
                for path in (kit / "web").rglob("*") if path.is_file()
            }
            tracked["tokens/interface.css"] = (kit / "tokens" / "interface.css").read_bytes()
            generate_web_react(kit / "brand.json", kit)
            after = {
                path.relative_to(kit).as_posix(): path.read_bytes()
                for path in (kit / "web").rglob("*") if path.is_file()
            }
            after["tokens/interface.css"] = (kit / "tokens" / "interface.css").read_bytes()
            self.assertEqual(tracked, after)

            manifest = json.loads((kit / "web" / "adapter.json").read_text(encoding="utf-8"))
            self.assertEqual(set(COMPONENT_IDS), set(manifest["recipes"]))
            self.assertEqual("1.0.0", manifest["adapter_version"])
            self.assertEqual("1.6.7", manifest["dependencies"]["radix-ui"]["version"])
            self.assertEqual("MIT", manifest["dependencies"]["radix-ui"]["license"])
            server = (kit / "web" / "react" / "server.tsx").read_text(encoding="utf-8")
            client = (kit / "web" / "react" / "client.tsx").read_text(encoding="utf-8")
            self.assertNotIn('"use client"', server)
            self.assertNotRegex(server, r"\b(?:window|document)\b")
            self.assertTrue(client.startswith('"use client";'))
            self.assertIn('from "radix-ui"', client)
            self.assertNotIn("asChild", client)
            self.assertIn("setPointerCapture", client)
            self.assertIn("releasePointerCapture", client)
            self.assertIn('orientation === "horizontal" ? "vertical" : "horizontal"', client)

    def test_tokens_are_react_free_and_component_css_uses_semantic_namespace(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            tokens = (kit / "tokens" / "interface.css").read_text(encoding="utf-8")
            css = (kit / "web" / "components.css").read_text(encoding="utf-8")
            self.assertIn("--bb-surface-background", tokens)
            self.assertNotIn("import ", tokens)
            self.assertNotIn("radix", tokens.lower())
            self.assertNotRegex(css, r"#[0-9a-fA-F]{3,8}\b")
            self.assertNotRegex(css, r"(?<![-\w])\d+(?:\.\d+)?px\b")
            self.assertIn("var(--bb-interaction-target-minimum)", css)
            self.assertIn("@media (forced-colors: active)", css)
            self.assertIn("@media (prefers-reduced-motion: reduce)", css)
            self.assertIn("block-size: 100dvh", css)
            self.assertIn("overflow: hidden", css)
            self.assertIn("body:has(.bb-app-frame)", css)
            self.assertIn(".bb-button--destructive { background: var(--bb-action-destructive); color: var(--bb-text-on-destructive); }", css)
            self.assertIn(".bb-menu { background: var(--bb-surface-overlay); color: var(--bb-text-primary); }", css)
            self.assertIn(".bb-dialog { background: var(--bb-surface-overlay); color: var(--bb-text-primary); }", css)
            self.assertIn(".bb-toast { background: var(--bb-surface-overlay); color: var(--bb-text-primary); }", css)
            self.assertIn(".bb-field__control { background: var(--bb-surface-background); color: var(--bb-text-primary); }", css)

    def test_app_frame_profiles_are_emitted_with_one_owner(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            profiles = json.loads((kit / "web" / "app-frame-hosts.json").read_text(encoding="utf-8"))
            self.assertEqual({"browser", "tauri", "wails"}, {item["profile"] for item in profiles})
            for profile in profiles:
                self.assertEqual(set(RESPONSIBILITIES), set(profile["responsibilities"]))
                self.assertTrue(all(owner in {"app-frame", "host"} for owner in profile["responsibilities"].values()))

    def test_specimen_contains_behavior_and_accessibility_contract(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            specimen = (kit / "web" / "specimen.html").read_text(encoding="utf-8")
            for marker in (
                'data-bb-app-frame', 'role="tablist"', 'role="menu"', '<dialog',
                'role="separator"', 'aria-live="polite"', 'data-bb-overlay-root',
                "prefers-reduced-motion", "forced-colors", "visualViewport",
            ):
                self.assertIn(marker, specimen)


if __name__ == "__main__":
    unittest.main()
