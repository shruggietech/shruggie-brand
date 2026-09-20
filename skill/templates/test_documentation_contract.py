#!/usr/bin/env python3
"""Tests for documentation ownership, projections, and drift rejection."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from documentation_contract import (DocumentationContractError, build_documentation_facts,
                                    load_documentation_contract, manual_catalog,
                                    render_implementation, validate_documentation_contract,
                                    validate_route_dispositions, verify_documentation_facts,
                                    verify_rendered_implementation)
from schema_validation import validate_json_schema


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class DocumentationContractTests(unittest.TestCase):
    def test_policy_schema_inventory_topics_and_navigation_are_complete(self):
        contract = load_documentation_contract()
        validate_json_schema(contract, read_json(ROOT / "skill" / "references" / "documentation-contract.schema.json"))
        pages = manual_catalog(contract)
        self.assertEqual(15, len(pages))
        self.assertEqual(list(range(1, 16)), [page["pagination_order"] for page in pages])
        self.assertEqual(set(contract["required_topics"]), {topic for page in pages for topic in page["topics"]})

    def test_unlisted_source_duplicate_navigation_and_missing_topic_fail_closed(self):
        contract = load_documentation_contract()
        with tempfile.TemporaryDirectory() as temporary:
            references = Path(temporary)
            for page in contract["manual_pages"]:
                (references / page["source"]).write_text("# Test\n", encoding="utf-8")
            (references / "unlisted.md").write_text("# Unlisted\n", encoding="utf-8")
            with self.assertRaisesRegex(DocumentationContractError, "inventory differs"):
                validate_documentation_contract(copy.deepcopy(contract), references)
        duplicate = copy.deepcopy(contract)
        duplicate["manual_pages"][1]["section_order"] = duplicate["manual_pages"][0]["section_order"]
        duplicate["manual_pages"][1]["order"] = duplicate["manual_pages"][0]["order"]
        with self.assertRaisesRegex(DocumentationContractError, "positions"):
            validate_documentation_contract(duplicate, ROOT / "skill" / "references")
        missing = copy.deepcopy(contract)
        missing["manual_pages"][-1]["topics"].remove("extension-workflow")
        with self.assertRaisesRegex(DocumentationContractError, "topics"):
            validate_documentation_contract(missing, ROOT / "skill" / "references")

    def test_route_dispositions_cover_every_public_documentation_surface(self):
        routes = [{"kind": kind} for kind in ("docs-index", "docs-page", "guidelines", "guidelines-topic", "downloads")]
        self.assertEqual(routes, validate_route_dispositions(routes))
        contract = load_documentation_contract()
        contract["route_dispositions"] = contract["route_dispositions"][:-1]
        with self.assertRaisesRegex(DocumentationContractError, "incomplete"):
            validate_documentation_contract(contract, ROOT / "skill" / "references")

    def test_shared_facts_render_deterministically_and_reject_drift(self):
        contract = load_documentation_contract()
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            paths = ["brand.json", "enforcement/interface-canon.json", "enforcement/component-recipes.json", "web/adapter.json", "web/support-matrix.json", "native/egui/adapter.json", "native/egui/support-matrix.json", "enforcement/gap.json", "enforcement/distributions/recovery.skill"]
            for relative in paths:
                path = kit / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_text("{}\n", encoding="utf-8")
            versions = {"canon_version": "1.2.1", "interface_canon_version": "1.0.0", "component_recipe_version": "1.0.0", "web_react_adapter_version": "1.0.0", "egui_adapter_version": "1.0.0", "compiler_version": "1.2.1", "brand_version": "1.0.0"}
            consumer = {"brand": {"slug": "test", "title": "Test", "affiliation": None, "brand_version": "1.0.0"}, "versions": versions,
                        "authority": {"brand_source": "brand.json", "interface_canon": "enforcement/interface-canon.json", "component_recipes": "enforcement/component-recipes.json", "version_policy": "enforcement/version-policy.json", "web_adapter": "web/adapter.json", "support_matrix": "web/support-matrix.json", "egui_adapter": "native/egui/adapter.json", "egui_support_matrix": "native/egui/support-matrix.json", "instructions": "enforcement/IMPLEMENTATION.md", "precedence": ["brand.json"], "permitted_exceptions": ["governed literals"]},
                        "verification": {"entry_points": ["python verify.py", "python validate_glyph.py"], "success": "zero failures"},
                        "recovery": {"distribution": "recovery.skill", "path": "enforcement/distributions/recovery.skill", "sha256": "a" * 64, "extract_to": "enforcement/brandbuilder", "sources": [{"kind": "delivered-bundle"}], "instruction": "verify"},
                        "capability_gap": {"template_path": "enforcement/gap.json", "submission_requires_authorization": True}}
            facts = build_documentation_facts(contract, consumer, kit)
            rendered = render_implementation(facts, "Use the governed palette.")
            self.assertEqual(rendered, render_implementation(facts, "Use the governed palette."))
            self.assertIn("[/docs/](https://brand.shruggie.tech/docs/)", rendered)
            self.assertNotIn("[/docs/](/docs/)", rendered)
            verify_rendered_implementation(rendered, facts)
            drifted = copy.deepcopy(facts); drifted["versions"]["compiler_version"] = "9.9.9"
            with self.assertRaisesRegex(DocumentationContractError, "versions"):
                verify_documentation_facts(drifted, contract, consumer, kit)
            missing = copy.deepcopy(facts); missing["bindings"]["web_adapter"] = "web/missing.json"
            with self.assertRaisesRegex(DocumentationContractError, "binding facts"):
                verify_documentation_facts(missing, contract, consumer, kit)


if __name__ == "__main__":
    unittest.main(verbosity=2)
