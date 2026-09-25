#!/usr/bin/env python3
"""Source-to-guide color role contract regressions."""

import json
import unittest
from pathlib import Path

from color_roles import ColorRoleError, resolve_color_roles
from gen_nextjs import build_slots, emit_theme_item, oklch
from verify import Report, c_accent


ROOT = Path(__file__).resolve().parents[2]
CANON = json.loads((ROOT / "skill" / "references" / "01-canon.json").read_text(encoding="utf-8"))


def brand(slug):
    return json.loads((ROOT / "brands" / slug / "brand.json").read_text(encoding="utf-8"))


class ColorRoleTests(unittest.TestCase):
    def test_all_production_brands_resolve_eight_cues_in_both_themes(self):
        for path in sorted((ROOT / "brands").glob("*/brand.json")):
            source = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(slug=source["slug"]):
                roles = resolve_color_roles(source, CANON)
                self.assertGreaterEqual(len(roles["identity"]), 1)
                self.assertGreaterEqual(len(roles["identity_combinations"]), 1)
                self.assertEqual(8, len(roles["interface"]["dark"]))
                self.assertEqual(8, len(roles["interface"]["light"]))
                for theme in ("dark", "light"):
                    for cue in roles["interface"][theme]:
                        self.assertGreaterEqual(cue["foreground_contrast"], 4.5)
                        self.assertTrue(cue["non_color_cue"])
                        self.assertTrue(cue["source"])

    def test_unknown_and_unsafe_formal_sources_fail(self):
        source = brand("covarity")
        source["color_roles"]["identity"][0]["source"] = "brand.logo.role_colors.color.nonexistent"
        with self.assertRaisesRegex(ColorRoleError, "unknown"):
            resolve_color_roles(source, CANON)
        source["color_roles"]["identity"][0]["source"] = "brand.../../../secrets"
        with self.assertRaisesRegex(ColorRoleError, "unsupported"):
            resolve_color_roles(source, CANON)

    def test_missing_role_declaration_fails(self):
        source = brand("covarity")
        del source["color_roles"]
        with self.assertRaisesRegex(ColorRoleError, "color_roles must declare"):
            resolve_color_roles(source, CANON)

    def test_house_choice_is_explicit_and_ownership_neutral(self):
        source = brand("covarity")
        source["affiliation"].update({"ownership": "third-party", "parent": None, "endorsement": "none"})
        roles = resolve_color_roles(source, CANON)
        self.assertEqual("#FF5300", next(cue["hex"] for cue in roles["interface"]["dark"] if cue["id"] == "warning"))

    def test_multicolor_mark_keeps_identity_roles_separate_from_interface_cues(self):
        source = brand("covarity")
        roles = resolve_color_roles(source, CANON)
        self.assertEqual({"primary", "terminal"}, {row["id"] for row in roles["identity"]})
        terminal = next(row for row in roles["identity"] if row["id"] == "terminal")
        self.assertEqual(source["logo"]["role_colors"]["color"]["emphasis"], terminal["hex"])
        self.assertNotIn("warning", {row["id"] for row in roles["identity"]})
        self.assertEqual("warning", next(row["id"] for row in roles["interface"]["dark"] if row["hex"] == terminal["hex"]))
        self.assertEqual({"primary", "terminal"}, set(roles["identity_combinations"][0]["colors"]))
        self.assertEqual("logo.full", roles["identity_combinations"][0]["artwork"])

    def test_authoritative_heart_colors_are_bound_to_existing_palette(self):
        source = brand("i-heart-pr-tours")
        roles = resolve_color_roles(source, CANON)
        formal = {row["id"]: row for row in roles["identity"]}
        self.assertEqual(source["legacy_palette"][3], formal["heart-red"]["hex"])
        self.assertEqual(source["accent"]["deep"], formal["heart-blue"]["hex"])
        self.assertEqual({"heart-blue", "heart-red"}, set(roles["identity_combinations"][0]["colors"]))

    def test_existing_theme_tokens_agree_with_explicit_interface_roles(self):
        for slug in ("covarity", "i-heart-pr-tours", "shruggietech"):
            source = brand(slug)
            roles = resolve_color_roles(source, CANON)
            dark, light = build_slots(CANON, source)
            for theme, tokens in (("dark", dark), ("light", light)):
                cues = {cue["id"]: cue for cue in roles["interface"][theme]}
                with self.subTest(slug=slug, theme=theme):
                    self.assertEqual(tokens["brand-cta"], cues["action"]["hex"])
                    self.assertEqual(tokens["brand-emphasis"], cues["warning"]["hex"])
                    self.assertEqual(tokens["destructive"], cues["error"]["hex"])
                    self.assertEqual(tokens["ring"], cues["focus"]["hex"])
                    self.assertEqual(tokens["primary"], cues["selection"]["hex"])
                    registry = emit_theme_item(CANON, source, dark, light)["cssVars"][theme]
                    for cue, token in (("action", "brand-cta"), ("warning", "brand-emphasis"),
                                       ("error", "destructive"), ("focus", "ring"),
                                       ("selection", "primary")):
                        self.assertEqual(oklch(cues[cue]["hex"]), registry[token])

    def test_owned_child_sibling_hue_is_allowed_but_contrast_still_fails(self):
        source = brand("cueson")
        sibling = brand("go-schedule")
        source["affiliation"]["inheritance"] = "independent"
        source["semantic_colors"] = {"emphasis": "#A1CFF4", "action": "#1C5B8D"}
        source["accent"]["bright"] = sibling["accent"]["bright"]
        source["accent"]["accessible"] = sibling["accent"]["accessible"]
        good = Report()
        c_accent(CANON, source, good)
        self.assertFalse(good.problems)
        self.assertEqual("#A1CFF4", next(row["hex"] for row in resolve_color_roles(source, CANON)["interface"]["dark"] if row["id"] == "warning"))
        source["accent"]["accessible"] = "#FFFFFF"
        weak = Report()
        c_accent(CANON, source, weak)
        self.assertTrue(any("needs 4.5" in problem for problem in weak.problems))

    def test_invalid_weak_surface_cue_fails(self):
        source = brand("covarity")
        source["color_roles"]["interface_overrides"] = {"focus": {"dark": "brand.surfaces.base", "light": "brand.light_surfaces.base"}}
        with self.assertRaisesRegex(ColorRoleError, "surface contrast"):
            resolve_color_roles(source, CANON)

    def test_status_requires_non_color_cue_and_valid_formal_combination(self):
        source = brand("covarity")
        source["color_roles"]["combinations"][0]["colors"] = ["missing"]
        with self.assertRaisesRegex(ColorRoleError, "distinct formal colors"):
            resolve_color_roles(source, CANON)
        changed = json.loads(json.dumps(CANON))
        source = brand("covarity")
        changed["color"]["role_model"]["interface_cues"]["warning"]["non_color_cue"] = ""
        with self.assertRaisesRegex(ColorRoleError, "non-color cue"):
            resolve_color_roles(source, changed)


if __name__ == "__main__":
    unittest.main()
