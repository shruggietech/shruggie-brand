#!/usr/bin/env python3
"""Contract tests for the renderer-neutral canon and consumer handover."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from interface_contract import (
    BEGIN_MARKER,
    END_MARKER,
    InterfaceContractError,
    emit_consumer_contract,
    load_interface_canon,
    merge_governed_block,
    resolve_interface_contract,
    route_operating_mode,
    validate_interface_canon,
    validate_runtime_profile,
    verify_consumer_contract,
    write_deterministic_skill_bundle,
)
from schema_validation import validate_json_schema


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class InterfaceCanonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canon = load_interface_canon()

    def test_canon_is_structurally_valid_and_all_roles_resolve(self):
        validate_interface_canon(self.canon)
        validate_json_schema(self.canon, read_json(ROOT / "skill" / "references" / "interface-canon.schema.json"))
        self.assertEqual(set(self.canon["role_catalog"]), set(self.canon["aliases"]))
        self.assertTrue(set(self.canon["required_roles"]).issubset(self.canon["aliases"]))

    def test_published_schemas_are_valid_json_and_define_closed_required_fields(self):
        references = ROOT / "skill" / "references"
        for name in ("interface-canon.schema.json", "consumer-contract.schema.json"):
            schema = read_json(references / name)
            pending = [schema]
            while pending:
                node = pending.pop()
                if isinstance(node, dict):
                    if node.get("type") == "object" and node.get("additionalProperties") is False:
                        self.assertTrue(set(node.get("required", [])).issubset(node.get("properties", {})), name)
                    pending.extend(node.values())
                elif isinstance(node, list):
                    pending.extend(node)

    def test_every_production_brand_resolves_without_identity_mutation(self):
        for brand_path in sorted((ROOT / "brands").glob("*/brand.json")):
            before = brand_path.read_bytes()
            brand = json.loads(before.decode("utf-8"))
            resolved = resolve_interface_contract(brand, canon=self.canon)
            self.assertEqual(self.canon["version"], resolved["interface_canon_version"])
            self.assertEqual(brand.get("canon", "1.2.1"), resolved["canon_version"])
            self.assertEqual({"dark", "light"}, set(resolved["roles_by_theme"]))
            self.assertEqual(resolved["roles"], resolved["roles_by_theme"]["dark"])
            self.assertEqual(before, brand_path.read_bytes())

    def test_theme_indexed_roles_use_legal_light_and_dark_values(self):
        brand = read_json(ROOT / "brands" / "shruggietech" / "brand.json")
        resolved = resolve_interface_contract(brand, canon=self.canon)
        self.assertEqual("#000000", resolved["roles_by_theme"]["dark"]["surface.background"])
        self.assertEqual("#FFFFFF", resolved["roles_by_theme"]["light"]["surface.background"])
        self.assertEqual("#037B40", resolved["roles_by_theme"]["light"]["focus.ring"])
        self.assertEqual(["light", "dark"], resolved["system_theme_resolution"])

        tour = read_json(ROOT / "brands" / "i-heart-pr-tours" / "brand.json")
        tour_roles = resolve_interface_contract(tour, canon=self.canon)["roles_by_theme"]["light"]
        self.assertEqual(tour["accent"]["accessible"], tour_roles["text.muted"])
        self.assertNotEqual(tour["accent"]["dim"], tour_roles["text.muted"])

        glitchpad = read_json(ROOT / "brands" / "glitchpad" / "brand.json")
        glitchpad_roles = resolve_interface_contract(glitchpad, canon=self.canon)["roles_by_theme"]["dark"]
        self.assertEqual(glitchpad["accent"]["bright"], glitchpad_roles["text.muted"])
        self.assertNotEqual(glitchpad["accent"]["dim"], glitchpad_roles["text.muted"])

    def test_unknown_missing_invalid_and_cyclic_roles_fail_closed(self):
        unknown = copy.deepcopy(self.canon)
        unknown["aliases"]["product.hero.layout"] = "$primitive.spacing.4"
        with self.assertRaisesRegex(InterfaceContractError, "unknown role"):
            validate_interface_canon(unknown)

        missing = copy.deepcopy(self.canon)
        del missing["aliases"][missing["required_roles"][0]]
        with self.assertRaisesRegex(InterfaceContractError, "missing required role"):
            validate_interface_canon(missing)

        invalid = copy.deepcopy(self.canon)
        invalid["aliases"][invalid["required_roles"][0]] = "$renderer.css.padding"
        with self.assertRaisesRegex(InterfaceContractError, "reference root"):
            validate_interface_canon(invalid)

        cyclic = copy.deepcopy(self.canon)
        first, second = cyclic["required_roles"][:2]
        cyclic["aliases"][first] = "$alias.%s" % second
        cyclic["aliases"][second] = "$alias.%s" % first
        with self.assertRaisesRegex(InterfaceContractError, "alias cycle"):
            validate_interface_canon(cyclic)

    def test_unsupported_cross_boundary_and_inaccessible_overrides_fail(self):
        brand = read_json(ROOT / "brands" / "i-heart-pr-tours" / "brand.json")
        brand["interface"] = {"canon": self.canon["version"], "overrides": {"focus.width": "$primitive.focus.width"}}
        with self.assertRaisesRegex(InterfaceContractError, "unsupported override"):
            resolve_interface_contract(brand, canon=self.canon)

        brand["interface"]["overrides"] = {"action.primary": "$brand_canon.color.immutable.orange-cta.hex"}
        with self.assertRaisesRegex(InterfaceContractError, "crosses affiliation"):
            resolve_interface_contract(brand, canon=self.canon)

        inaccessible = copy.deepcopy(self.canon)
        inaccessible["aliases"]["text.primary"] = "$alias.surface.background"
        with self.assertRaisesRegex(InterfaceContractError, "contrast"):
            resolve_interface_contract(read_json(ROOT / "brands" / "shruggietech" / "brand.json"), canon=inaccessible)

    def test_runtime_accepts_mixed_capabilities_and_rejects_os_inference(self):
        for profile in self.canon["runtime"]["mixed_profile_examples"]:
            validate_runtime_profile(profile, self.canon)
        profile = copy.deepcopy(self.canon["runtime"]["mixed_profile_examples"][0])
        profile["operating_system"] = "Windows"
        with self.assertRaisesRegex(InterfaceContractError, "operating-system"):
            validate_runtime_profile(profile, self.canon)


class RoutingTests(unittest.TestCase):
    def test_behavioral_fixtures_select_expected_mode_without_new_authority(self):
        payload = read_json(ROOT / "skill" / "references" / "routing-fixtures.json")
        for fixture in payload["fixtures"]:
            decision = route_operating_mode(fixture["signals"])
            self.assertEqual(fixture["expected_mode"], decision["mode"], fixture["id"])
            self.assertEqual(fixture["requires_clarification"], decision["requires_clarification"], fixture["id"])
            self.assertTrue(decision["authority_preserved"], fixture["id"])
            if decision["requires_clarification"]:
                self.assertTrue(decision["clarification"])

    def test_skill_and_ambient_host_instructions_have_equivalent_body(self):
        from sync_agents_md import PREAMBLE, body_of

        skill = ROOT / "skill" / "SKILL.md"
        ambient = (ROOT / "skill" / "AGENTS.md").read_text(encoding="utf-8")
        body = body_of(str(skill))
        lines = body.splitlines()
        if lines and lines[0].startswith("# "):
            lines = lines[1:]
            while lines and not lines[0].strip():
                lines = lines[1:]
        self.assertEqual(PREAMBLE + "\n".join(lines).rstrip() + "\n", ambient)
        for phrase in ("Author mode", "Implementation mode", "Audit mode", "consumer-contract.json", "exact pinned"):
            self.assertIn(phrase, ambient)


class ConsumerContractTests(unittest.TestCase):
    def test_recovery_bundle_excludes_host_generated_dependency_and_cache_trees(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / "skill"
            (skill / "references").mkdir(parents=True)
            (skill / "node_modules" / "package").mkdir(parents=True)
            (skill / "templates" / "__pycache__").mkdir(parents=True)
            (skill / "SKILL.md").write_text("source\n", encoding="utf-8")
            (skill / "references" / "canon.json").write_text("{}\n", encoding="utf-8")
            (skill / "node_modules" / "package" / "host.js").write_text("host state\n", encoding="utf-8")
            (skill / "templates" / "__pycache__" / "host.pyc").write_bytes(b"host state")
            destination = root / "recovery.skill"
            first = write_deterministic_skill_bundle(destination, skill_root=skill)
            (skill / "node_modules" / "package" / "host.js").write_text("changed host state\n", encoding="utf-8")
            second = write_deterministic_skill_bundle(destination, skill_root=skill)
            self.assertEqual(first, second)
            with zipfile.ZipFile(destination) as archive:
                self.assertEqual({"SKILL.md", "references/canon.json"}, set(archive.namelist()))

    def test_governed_block_merge_preserves_human_content_and_rejects_malformed_markers(self):
        block = "%s\nnew governed content\n%s" % (BEGIN_MARKER, END_MARKER)
        existing = "# Human instructions\n\nkeep before\n\n%s\nold\n%s\n\nkeep after\n\n" % (BEGIN_MARKER, END_MARKER)
        merged = merge_governed_block(existing, block)
        self.assertTrue(merged.startswith("# Human instructions\n\nkeep before\n\n"))
        self.assertTrue(merged.endswith("\n\nkeep after\n\n"))
        self.assertIn("new governed content", merged)
        self.assertNotIn("\nold\n", merged)

        appended = merge_governed_block("# Human only\n", block)
        self.assertEqual("# Human only\n\n" + block + "\n", appended)
        for malformed in (BEGIN_MARKER, END_MARKER, BEGIN_MARKER + "\n" + BEGIN_MARKER + "\n" + END_MARKER):
            with self.assertRaisesRegex(InterfaceContractError, "marker"):
                merge_governed_block(malformed, block)

    def test_emitted_contract_is_deterministic_verifiable_and_offline_complete(self):
        brand_source = ROOT / "brands" / "shruggietech" / "brand.json"
        brand = read_json(brand_source)
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary) / "shruggietech"
            kit.mkdir()
            (kit / "brand.json").write_bytes(brand_source.read_bytes())
            first = emit_consumer_contract(brand, kit / "brand.json", kit, "# Implementation\n\nExact guidance.\n")
            tracked = [kit / item["path"] for item in first["provenance"]] + [kit / "enforcement" / "consumer-contract.json"]
            before = {path.relative_to(kit).as_posix(): path.read_bytes() for path in tracked}
            second = emit_consumer_contract(brand, kit / "brand.json", kit, "# Implementation\n\nExact guidance.\n")
            after = {path.relative_to(kit).as_posix(): path.read_bytes() for path in tracked}
            self.assertEqual(first, second)
            self.assertEqual(before, after)
            self.assertEqual([], verify_consumer_contract(kit))

            schema = read_json(kit / "enforcement" / "consumer-contract.schema.json")
            validate_json_schema(first, schema)
            self.assertEqual(
                ["python3 enforcement/brandbuilder/templates/verify.py .",
                 "python3 enforcement/brandbuilder/templates/validate_glyph.py brand.json"],
                first["verification"]["entry_points"],
            )

            recovery = first["recovery"]
            distribution = kit / recovery["path"]
            self.assertTrue(distribution.is_file())
            self.assertEqual(recovery["sha256"], hashlib.sha256(distribution.read_bytes()).hexdigest())
            self.assertEqual("delivered-bundle", recovery["sources"][0]["kind"])
            self.assertNotIn("latest", json.dumps(recovery).lower())

            gap = read_json(kit / first["capability_gap"]["template_path"])
            self.assertFalse(gap["submission_authorized"])
            self.assertEqual(brand["version"], gap["consumer"]["brand_version"])

            contract_path = kit / "enforcement" / "consumer-contract.json"
            for field, value in (("title", "Impostor"), ("affiliation", {"parent": "false-owner"})):
                contract = read_json(contract_path)
                contract["brand"][field] = value
                contract_path.write_text(json.dumps(contract), encoding="utf-8")
                problems = verify_consumer_contract(kit)
                self.assertTrue(any("brand metadata disagrees" in problem for problem in problems), problems)
                contract_path.write_bytes(before["enforcement/consumer-contract.json"])

            contract = read_json(contract_path)
            contract["authority"]["instructions"] = "enforcement/missing.md"
            contract_path.write_text(json.dumps(contract), encoding="utf-8")
            problems = verify_consumer_contract(kit)
            self.assertTrue(any("file is missing" in problem for problem in problems), problems)
            contract_path.write_bytes(before["enforcement/consumer-contract.json"])

            contract = read_json(contract_path)
            contract["provenance"] = contract["provenance"][:-1]
            contract_path.write_text(json.dumps(contract), encoding="utf-8")
            problems = verify_consumer_contract(kit)
            self.assertTrue(any("omits required authority" in problem for problem in problems))
            contract_path.write_bytes(before["enforcement/consumer-contract.json"])

            for mutation in (
                lambda value: value.__setitem__("version_semantics", {}),
                lambda value: value["environment"].__setitem__("renderer", "browser"),
                lambda value: value["environment"].__setitem__("supported_targets", []),
                lambda value: value["authority"].__setitem__("precedence", []),
            ):
                contract = read_json(contract_path)
                mutation(contract)
                contract_path.write_text(json.dumps(contract), encoding="utf-8")
                problems = verify_consumer_contract(kit)
                self.assertTrue(any("schema violation" in problem for problem in problems), problems)
                contract_path.write_bytes(before["enforcement/consumer-contract.json"])

            implementation = kit / "enforcement" / "IMPLEMENTATION.md"
            implementation.write_text(implementation.read_text(encoding="utf-8") + "drift\n", encoding="utf-8")
            problems = verify_consumer_contract(kit)
            self.assertTrue(any("checksum" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
