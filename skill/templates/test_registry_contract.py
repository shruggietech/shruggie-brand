#!/usr/bin/env python3
"""Registry schema and semantic checks for generated delivery."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from registry_contract import validate_registry


THEME = {
    "$schema": "https://ui.shadcn.com/schema/registry-item.json",
    "name": "theme",
    "type": "registry:theme",
    "title": "Alpha Theme",
    "description": "Installable tokens",
    "cssVars": {"light": {"background": "oklch(1 0 0)"}, "dark": {"background": "oklch(0 0 0)"}},
    "files": [],
}
ROW = {
    "$schema": "https://ui.shadcn.com/schema/registry-item.json",
    "name": "alpha-row",
    "type": "registry:ui",
    "title": "Alpha Row",
    "description": "A static row",
    "files": [{"path": "components/alpha/alpha-row.tsx", "target": "@components/alpha/alpha-row.tsx", "type": "registry:ui", "content": "export function AlphaRow() { return <div>Alpha</div> }\n"}],
}


class RegistryContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.items = [copy.deepcopy(THEME), copy.deepcopy(ROW)]
        self.write()

    def write(self):
        for item in self.items:
            (self.root / (item["name"] + ".json")).write_text(json.dumps(item), encoding="utf-8")
        catalog = {"$schema": "https://ui.shadcn.com/schema/registry.json", "name": "alpha", "homepage": "https://example.com", "items": self.items}
        (self.root / "registry.json").write_text(json.dumps(catalog), encoding="utf-8")

    def test_fileless_theme_and_ui_item_pass(self):
        validate_registry(self.root, "alpha")

    def test_catalog_payload_mismatch_fails(self):
        self.items[1]["description"] = "Changed only in catalog"
        (self.root / "registry.json").write_text(json.dumps({"$schema": "https://ui.shadcn.com/schema/registry.json", "name": "alpha", "homepage": "https://example.com", "items": self.items}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "alpha-row.*catalog.*mismatch"):
            validate_registry(self.root, "alpha")

    def test_empty_ui_content_fails(self):
        self.items[1]["files"][0]["content"] = "  "
        self.write()
        with self.assertRaisesRegex(ValueError, "alpha-row.*content"):
            validate_registry(self.root, "alpha")

    def test_unsafe_target_fails(self):
        self.items[1]["files"][0]["target"] = "../../outside.tsx"
        self.write()
        with self.assertRaisesRegex(ValueError, "alpha-row.*target"):
            validate_registry(self.root, "alpha")

    def test_missing_endpoint_fails(self):
        (self.root / "alpha-row.json").unlink()
        with self.assertRaisesRegex(ValueError, "alpha-row.*missing"):
            validate_registry(self.root, "alpha")

    def test_unsupported_local_font_provider_fails(self):
        font = {"$schema": "https://ui.shadcn.com/schema/registry-item.json", "name": "fonts", "type": "registry:font", "title": "Fonts", "description": "Unsupported provider", "font": {"family": "Local", "provider": "local", "import": "Local", "variable": "--font-body"}}
        self.items.append(font)
        self.write()
        with self.assertRaisesRegex(ValueError, "fonts.*schema"):
            validate_registry(self.root, "alpha")

    def test_broken_registry_dependency_fails(self):
        self.items[1]["registryDependencies"] = ["missing-item"]
        self.write()
        with self.assertRaisesRegex(ValueError, "alpha-row.*dependency"):
            validate_registry(self.root, "alpha")

    def test_undeclared_endpoint_fails(self):
        (self.root / "stale.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "undeclared"):
            validate_registry(self.root, "alpha")

    def test_empty_catalog_description_fails(self):
        self.items[1]["description"] = ""
        self.write()
        with self.assertRaisesRegex(ValueError, "alpha-row.*description"):
            validate_registry(self.root, "alpha")

    def test_duplicate_file_target_fails(self):
        second = copy.deepcopy(ROW)
        second["name"] = "another-row"
        second["files"][0]["path"] = "components/alpha/another-row.tsx"
        self.items.append(second)
        self.write()
        with self.assertRaisesRegex(ValueError, "another-row.*target.*duplicated"):
            validate_registry(self.root, "alpha")


if __name__ == "__main__":
    unittest.main()
