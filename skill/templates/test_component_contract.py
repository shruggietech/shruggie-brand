#!/usr/bin/env python3
"""Contract tests for bounded component recipes and Web/React ownership."""

import copy
import json
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from component_contract import (  # noqa: E402
    COMPONENT_IDS,
    RESPONSIBILITIES,
    ComponentContractError,
    load_component_catalog,
    resolve_component_catalog,
    validate_app_frame_profiles,
    validate_component_catalog,
)


class ComponentCatalogTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_component_catalog()
        self.interface = json.loads(
            (ROOT / "skill" / "references" / "interface-canon.json").read_text(encoding="utf-8")
        )

    def test_catalog_is_closed_complete_and_covered(self):
        validate_component_catalog(self.catalog, self.interface)
        self.assertEqual(set(COMPONENT_IDS), set(self.catalog["components"]))
        self.assertEqual(
            set(COMPONENT_IDS),
            {row["component"] for row in self.catalog["coverage"]},
        )
        for name, recipe in self.catalog["components"].items():
            self.assertEqual(
                set(self.catalog["required_dimensions"]), set(recipe), name
            )

    def test_unknown_roles_raw_values_and_unbounded_composition_fail(self):
        unknown = copy.deepcopy(self.catalog)
        unknown["components"]["Button"]["roles"]["fill"] = "$role.product.hero"
        with self.assertRaisesRegex(ComponentContractError, "Button.*unknown role"):
            validate_component_catalog(unknown, self.interface)

        raw = copy.deepcopy(self.catalog)
        raw["components"]["Button"]["roles"]["fill"] = "#ffffff"
        with self.assertRaisesRegex(ComponentContractError, "Button.*role reference"):
            validate_component_catalog(raw, self.interface)

        screen = copy.deepcopy(self.catalog)
        screen["grammar"]["expresses"] = ["application-screen"]
        with self.assertRaisesRegex(ComponentContractError, "grammar.*application-screen"):
            validate_component_catalog(screen, self.interface)

    def test_states_targets_names_and_invariant_overrides_fail_closed(self):
        states = copy.deepcopy(self.catalog)
        states["components"]["Button"]["states"].remove("focus-visible")
        with self.assertRaisesRegex(ComponentContractError, "Button.*focus-visible"):
            validate_component_catalog(states, self.interface)

        extra_state = copy.deepcopy(self.catalog)
        extra_state["components"]["Button"]["states"].append("sparkling")
        with self.assertRaisesRegex(ComponentContractError, "Button.*unknown state"):
            validate_component_catalog(extra_state, self.interface)

        variant = copy.deepcopy(self.catalog)
        variant["components"]["Button"]["variants"].append("hero")
        with self.assertRaisesRegex(ComponentContractError, "Button.*unknown or missing variant"):
            validate_component_catalog(variant, self.interface)

        target = copy.deepcopy(self.catalog)
        target["components"]["IconButton"]["target"]["minimum"] = 32
        with self.assertRaisesRegex(ComponentContractError, "IconButton.*minimum target"):
            validate_component_catalog(target, self.interface)

        name = copy.deepcopy(self.catalog)
        name["components"]["IconButton"]["accessibility"]["name"] = "optional"
        with self.assertRaisesRegex(ComponentContractError, "IconButton.*accessible name"):
            validate_component_catalog(name, self.interface)

        override = copy.deepcopy(self.catalog)
        override["components"]["Button"]["overrides"].append("keyboard")
        with self.assertRaisesRegex(ComponentContractError, "Button.*invariant override"):
            validate_component_catalog(override, self.interface)

    def test_app_frame_profiles_have_exactly_one_owner(self):
        validate_app_frame_profiles(self.catalog["app_frame_profiles"])
        for profile in self.catalog["app_frame_profiles"]:
            self.assertEqual(set(RESPONSIBILITIES), set(profile["responsibilities"]))

        missing = copy.deepcopy(self.catalog["app_frame_profiles"])
        del missing[0]["responsibilities"][RESPONSIBILITIES[0]]
        with self.assertRaisesRegex(ComponentContractError, "missing owner"):
            validate_app_frame_profiles(missing)

        duplicate = copy.deepcopy(self.catalog["app_frame_profiles"])
        duplicate[0]["responsibilities"][RESPONSIBILITIES[0]] = ["app-frame", "host"]
        with self.assertRaisesRegex(ComponentContractError, "exactly one owner"):
            validate_app_frame_profiles(duplicate)

        handoff = copy.deepcopy(self.catalog["app_frame_profiles"])
        handoff[1]["responsibilities"][RESPONSIBILITIES[0]] = "host"
        handoff[1]["handoff"].pop(RESPONSIBILITIES[0], None)
        with self.assertRaisesRegex(ComponentContractError, "host handoff"):
            validate_app_frame_profiles(handoff)

    def test_resolved_catalog_is_deterministic_and_brand_safe(self):
        brand_path = ROOT / "brands" / "shruggietech" / "brand.json"
        brand = json.loads(brand_path.read_text(encoding="utf-8"))
        first = resolve_component_catalog(brand, self.catalog, self.interface)
        second = resolve_component_catalog(brand, self.catalog, self.interface)
        self.assertEqual(first, second)
        self.assertEqual("1.0.0", first["version"])
        self.assertEqual("1.0.0", first["interface_canon_version"])
        self.assertEqual(brand["slug"], first["brand"])

        unsafe = copy.deepcopy(brand)
        unsafe["component_overrides"] = {"Button": {"keyboard": ["none"]}}
        with self.assertRaisesRegex(ComponentContractError, "invariant override"):
            resolve_component_catalog(unsafe, self.catalog, self.interface)


if __name__ == "__main__":
    unittest.main()
