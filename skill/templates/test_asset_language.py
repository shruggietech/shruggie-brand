#!/usr/bin/env python3
"""S058 semantic asset names and approved-byte publication aliases."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import asset_language


class AssetLanguageTests(unittest.TestCase):
    def test_wide_and_stacked_lockups_have_distinct_identities(self):
        wide = {"family": "logo", "platform": "identity", "kind": "lockup", "variant": "full",
                "colourway": "color", "path": "logos/svg/example-horizontal-color.svg", "format": "svg"}
        stacked = dict(wide, path="logos/svg/example-stacked-color.svg")
        self.assertNotEqual(asset_language.design_key(wide), asset_language.design_key(stacked))
        self.assertEqual("Wide logo lockup, full color, for dark backgrounds", asset_language.describe(wide)["title"])
        self.assertEqual("Stacked logo lockup, full color, for dark backgrounds", asset_language.describe(stacked)["title"])

    def test_background_surface_and_ink_are_distinct(self):
        base = {"family": "logo", "platform": "identity", "kind": "mark", "variant": "full",
                "path": "logos/svg/example-mark-black.svg", "format": "svg", "colourway": "black"}
        black = asset_language.describe(base)
        white = asset_language.describe(dict(base, colourway="white", path="logos/svg/example-mark-white.svg"))
        self.assertEqual("clear", black["background"])
        self.assertEqual("light", black["surface"])
        self.assertEqual("black", black["ink"])
        self.assertEqual("white", white["ink"])
        self.assertNotEqual(asset_language.design_key(base), asset_language.design_key(dict(base, colourway="white", path="logos/svg/example-mark-white.svg")))

    def test_descriptive_name_keeps_size_and_format(self):
        item = {"family": "logo", "platform": "identity", "kind": "lockup", "variant": "full",
                "colourway": "light", "path": "logos/png/example-horizontal-light-1024.png", "format": "png",
                "width": 1024, "height": 201}
        self.assertEqual("logos/named/example-logo-lockup-wide-full-color-clear-for-light-1024.png",
                         asset_language.preferred_path("example", item))

    def test_aliases_preserve_source_bytes_and_reject_unsafe_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            source = kit / "logos" / "svg" / "example-horizontal-color.svg"
            source.parent.mkdir(parents=True)
            source.write_bytes(b"<svg/>")
            records = [{"path": "logos/svg/example-horizontal-color.svg", "kind": "lockup",
                        "variant": "full", "colourway": "color"}]
            mapping = asset_language.write_aliases(kit, "example", records)
            self.assertEqual(1, len(mapping["aliases"]))
            alias = kit / mapping["aliases"][0]["preferred_path"]
            self.assertEqual(source.read_bytes(), alias.read_bytes())
            self.assertEqual([], asset_language.validate_aliases(kit, records))
            mapping["aliases"][0]["source_path"] = "../escape.svg"
            self.assertTrue(asset_language.validate_aliases(kit, records, mapping))

    def test_alias_tamper_and_unindexed_file_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            source = kit / "logos" / "svg" / "example-mark-color.svg"
            source.parent.mkdir(parents=True)
            source.write_bytes(b"<svg/>")
            records = [{"path": "logos/svg/example-mark-color.svg", "kind": "mark",
                        "variant": "full", "colourway": "color"}]
            mapping = asset_language.write_aliases(kit, "example", records)
            alias = kit / mapping["aliases"][0]["preferred_path"]
            alias.write_bytes(b"tampered")
            self.assertTrue(asset_language.validate_aliases(kit, records))
            alias.write_bytes(source.read_bytes())
            (alias.parent / "unindexed.svg").write_bytes(b"<svg/>")
            self.assertTrue(asset_language.validate_aliases(kit, records))

    def test_missing_wordmark_is_not_inferred_from_lockup(self):
        lockup = {"family": "logo", "kind": "lockup", "variant": "full", "colourway": "color",
                  "path": "logos/svg/i-heart-pr-tours-horizontal-color.svg"}
        self.assertEqual("lockup", asset_language.describe(lockup)["form"])
        self.assertEqual("wide", asset_language.describe(lockup)["layout"])
        self.assertNotIn("wordmark", asset_language.describe(lockup)["title"].lower())

    def test_reused_web_icon_pixels_share_design_across_delivery_roles(self):
        base = {"family": "icon", "platform": "web", "appearance": "default",
                "source_variant": "full", "format": "png"}
        favicon = dict(base, role="favicon", path="icons/web/favicon-180x180.png", width=180, height=180)
        touch = dict(base, role="apple-touch", path="icons/web/apple-touch-icon.png", width=180, height=180)
        installable = dict(base, role="installable", path="icons/web/android-chrome-192x192.png", width=192, height=192)
        self.assertEqual(asset_language.design_key(favicon), asset_language.design_key(touch))
        self.assertEqual(asset_language.design_key(favicon), asset_language.design_key(installable))
        self.assertNotEqual(asset_language.design_key(favicon), asset_language.design_key(dict(favicon, source_variant="reduced")))
        self.assertNotEqual(asset_language.design_key(favicon), asset_language.design_key(dict(favicon, role="maskable")))

    def test_icon_background_uses_actual_alpha_and_surface_uses_appearance(self):
        icon = {"family": "icon", "platform": "windows", "role": "target-size",
                "source_variant": "full", "appearance": "default", "alpha": "opaque"}
        plated = asset_language.describe(icon)
        unplated = asset_language.describe(dict(icon, appearance="light-unplated", alpha="transparent"))
        self.assertEqual(("opaque", "none"), (plated["background"], plated["surface"]))
        self.assertEqual(("clear", "light"), (unplated["background"], unplated["surface"]))
        self.assertNotEqual(asset_language.design_key(icon), asset_language.design_key(dict(icon, alpha="transparent")))


if __name__ == "__main__":
    unittest.main()
