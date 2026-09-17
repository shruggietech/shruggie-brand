#!/usr/bin/env python3
"""Regression tests for release packaging version selection."""

import hashlib
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import package_release


ROOT = Path(__file__).resolve().parents[1]


class PackageReleaseTests(unittest.TestCase):
    def test_tree_packaging_excludes_host_generated_dependency_and_cache_trees(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            (source / "node_modules" / "package").mkdir(parents=True)
            (source / "templates" / "__pycache__").mkdir(parents=True)
            (source / "SKILL.md").write_text("source\n", encoding="utf-8")
            (source / "node_modules" / "package" / "host.js").write_text("host state\n", encoding="utf-8")
            (source / "templates" / "__pycache__" / "host.pyc").write_bytes(b"host state")
            archive_path = root / "skill.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                package_release.add_tree(archive, source)
            with zipfile.ZipFile(archive_path) as archive:
                self.assertEqual(["SKILL.md"], archive.namelist())

    def make_brand_source(self, root: Path) -> Path:
        for name in package_release.LICENSES:
            (root / name).write_text(name + "\n", encoding="utf-8")
        reference_dir = root / "skill" / "references"
        reference_dir.mkdir(parents=True)
        for name in ("interface-canon.schema.json", "component-recipes.schema.json", "consumer-contract.schema.json", "version-policy.json"):
            (reference_dir / name).write_bytes((ROOT / "skill" / "references" / name).read_bytes())
        source = root / "alpha"
        source.mkdir()
        brand = {"slug": "alpha", "title": "Alpha", "version": "1.0.0", "canon": "1.2.1", "affiliation": {}}
        consumer_schema = (ROOT / "skill" / "references" / "consumer-contract.schema.json").read_bytes()
        policy_bytes = (ROOT / "skill" / "references" / "version-policy.json").read_bytes()
        policy = json.loads(policy_bytes.decode("utf-8"))
        bundle_buffer = io.BytesIO()
        with zipfile.ZipFile(bundle_buffer, "w") as bundle:
            bundle.writestr("SKILL.md", "---\nmetadata:\n  version: 1.2.1\n  canon: 1.2.1\n  interface-canon: 1.0.0\n  component-recipes: 1.0.0\n  web-react-adapter: 1.0.0\n  egui-adapter: 1.0.0\n---\n")
            bundle.writestr("AGENTS.md", "instructions\n")
            bundle.writestr("references/interface-canon.json", json.dumps({"version": "1.0.0"}))
            bundle.writestr("references/component-recipes.json", json.dumps({"version": "1.0.0"}))
            bundle.writestr("references/component-recipes.schema.json", (ROOT / "skill" / "references" / "component-recipes.schema.json").read_bytes())
            bundle.writestr("references/version-policy.json", policy_bytes)
            bundle.writestr("references/consumer-contract.schema.json", consumer_schema)
            bundle.writestr("templates/verify.py", "# verifier\n")
            bundle.writestr("templates/validate_glyph.py", "# glyph gate\n")
        bundle = bundle_buffer.getvalue()
        begin = "<!-- BEGIN SHRUGGIE-BRANDBUILDER: CONSUMER CONTRACT -->"
        end = "<!-- END SHRUGGIE-BRANDBUILDER: CONSUMER CONTRACT -->"
        distribution = "enforcement/distributions/shruggie-brandbuilder-1.2.1.skill"
        values = {
            "brand.json": json.dumps(brand).encode(),
            "VERIFY.md": b"verified\n",
            "brand-guide.pdf": b"%PDF-1.4\n",
            "logos/mark.svg": b"<svg/>\n",
            "enforcement/AGENTS.md": (begin + "\ncontract\n" + end + "\n").encode(),
            "enforcement/IMPLEMENTATION.md": b"# Implementation\n",
            "enforcement/interface-canon.json": json.dumps({"version": "1.0.0"}).encode(),
            "enforcement/interface-canon.schema.json": (ROOT / "skill" / "references" / "interface-canon.schema.json").read_bytes(),
            "enforcement/component-recipes.json": json.dumps({"version": "1.0.0"}).encode(),
            "enforcement/component-recipes.schema.json": (ROOT / "skill" / "references" / "component-recipes.schema.json").read_bytes(),
            "enforcement/version-policy.json": policy_bytes,
            "enforcement/consumer-contract.schema.json": consumer_schema,
            "web/adapter.json": json.dumps({"adapter_version": "1.0.0", "component_recipe_version": "1.0.0"}).encode(),
            "web/support-matrix.json": json.dumps({"adapter_version": "1.0.0"}).encode(),
            "native/egui/adapter.json": json.dumps({"adapter_version": "1.0.0", "component_recipe_version": "1.0.0"}).encode(),
            "native/egui/Cargo.lock": b"# deterministic lockfile\n",
            "native/egui/support-matrix.json": json.dumps({"adapter_version": "1.0.0"}).encode(),
            "enforcement/capability-gap.example.json": json.dumps({"submission_authorized": False}).encode(),
            distribution: bundle,
        }
        provenance_names = [
            "brand.json", "enforcement/AGENTS.md", "enforcement/IMPLEMENTATION.md",
            "enforcement/interface-canon.json", "enforcement/interface-canon.schema.json",
            "enforcement/component-recipes.json", "enforcement/component-recipes.schema.json",
            "enforcement/version-policy.json", "web/adapter.json", "web/support-matrix.json",
            "native/egui/Cargo.lock", "native/egui/adapter.json", "native/egui/support-matrix.json",
            "enforcement/consumer-contract.schema.json", "enforcement/capability-gap.example.json", distribution,
        ]
        consumer = {
            "schema_version": 3,
            "brand": {"slug": "alpha", "title": "Alpha", "affiliation": {}, "brand_version": "1.0.0"},
            "versions": {"brand_version": "1.0.0", "canon_version": "1.2.1", "interface_canon_version": "1.0.0", "component_recipe_version": "1.0.0", "web_react_adapter_version": "1.0.0", "egui_adapter_version": "1.0.0", "compiler_version": "1.2.1"},
            "version_semantics": {
                "brand_version": "Brand version.", "canon_version": "Brand Canon version.",
                "interface_canon_version": "Interface Canon version.", "component_recipe_version": "Component recipe version.", "web_react_adapter_version": "Web adapter version.", "egui_adapter_version": "egui adapter version.", "compiler_version": "Compiler version.",
            },
            "compatibility": {
                "policy_version": policy["version"], "status": "compatible",
                "validated_versions": {"brand_canon": "1.2.1", "interface_canon": "1.0.0", "component_recipes": "1.0.0", "web_react_adapter": "1.0.0", "egui_adapter": "1.0.0", "compiler": "1.2.1", "brand": "1.0.0"},
                "rules_checked": len(policy["compatibility_rules"]), "publication_status": "candidate", "adoption_status": "unadopted",
            },
            "environment": {
                "renderer": "renderer-neutral", "host": "none", "supported_targets": ["web"],
                "viewport_profiles": ["compact"], "adapter_versions": {"vanilla": "1.2.1"},
            },
            "authority": {
                "brand_source": "brand.json", "interface_canon": "enforcement/interface-canon.json", "component_recipes": "enforcement/component-recipes.json", "version_policy": "enforcement/version-policy.json", "web_adapter": "web/adapter.json", "support_matrix": "web/support-matrix.json", "egui_adapter": "native/egui/adapter.json", "egui_support_matrix": "native/egui/support-matrix.json",
                "instructions": "enforcement/IMPLEMENTATION.md", "precedence": ["brand.json"],
                "permitted_exceptions": [],
            },
            "verification": {
                "entry_points": ["python3 enforcement/brandbuilder/templates/verify.py .", "python3 enforcement/brandbuilder/templates/validate_glyph.py brand.json"],
                "success": "zero failures",
            },
            "recovery": {
                "distribution": "shruggie-brandbuilder-1.2.1.skill",
                "path": distribution,
                "sha256": hashlib.sha256(bundle).hexdigest(),
                "extract_to": "enforcement/brandbuilder",
                "sources": [{"kind": "delivered-bundle", "path": distribution, "network_required": False}],
                "instruction": "Use exact delivered bytes.",
            },
            "provenance": [
                {"path": name, "bytes": len(values[name]), "sha256": hashlib.sha256(values[name]).hexdigest()}
                for name in provenance_names
            ],
            "capability_gap": {"template_path": "enforcement/capability-gap.example.json", "submission_requires_authorization": True},
        }
        values["enforcement/consumer-contract.json"] = json.dumps(consumer).encode()
        for name, value in values.items():
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(value)
        manifest = {
            "name": "alpha-brand-kit",
            "version": "1.0.0",
            "canon": "1.2.1",
            "files": [
                {"path": name, "bytes": len(value), "sha256": hashlib.sha256(value).hexdigest()}
                for name, value in sorted(values.items())
            ],
        }
        (source / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        return source

    def test_omitted_version_uses_validated_current_metadata(self):
        with mock.patch.object(package_release, "current_version", return_value="1.2.1") as current:
            self.assertEqual(package_release.resolve_version(ROOT, None), "1.2.1")
        current.assert_called_once_with(ROOT)

    def test_explicit_version_does_not_rediscover_current_metadata(self):
        with mock.patch.object(package_release, "current_version") as current:
            self.assertEqual(package_release.resolve_version(ROOT, "1.2.1"), "1.2.1")
        current.assert_not_called()

    def test_brand_archive_writer_is_complete_deterministic_and_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.make_brand_source(root)
            first = root / "one" / "alpha-brand-1.0.0.zip"
            second = root / "two" / "alpha-brand-1.0.0.zip"
            package_release.write_brand_archive(source, first, root=root, expected_canon="1.2.1")
            package_release.write_brand_archive(source, second, root=root, expected_canon="1.2.1")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                expected = {
                    path.relative_to(source).as_posix()
                    for path in source.rglob("*") if path.is_file()
                } | set(package_release.LICENSES)
                self.assertEqual(
                    set(archive.namelist()),
                    expected,
                )

    def test_brand_archive_rejects_corrupt_offline_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.make_brand_source(root)
            distribution = source / "enforcement" / "distributions" / "shruggie-brandbuilder-1.2.1.skill"
            distribution.write_bytes(distribution.read_bytes() + b"drift")
            destination = root / "release" / "alpha-brand-1.0.0.zip"
            with self.assertRaisesRegex(ValueError, "recovery checksum mismatch"):
                package_release.write_brand_archive(source, destination, root=root, expected_canon="1.2.1")

    def test_brand_archive_writer_preserves_destination_when_verification_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.make_brand_source(root)
            destination = root / "published" / "alpha-brand-1.0.0.zip"
            destination.parent.mkdir()
            destination.write_bytes(b"last known good")
            (source / "logos" / "mark.svg").write_bytes(b"corrupt")
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                package_release.write_brand_archive(source, destination, root=root, expected_canon="1.2.1")
            self.assertEqual(b"last known good", destination.read_bytes())
            self.assertFalse(destination.with_name(f".{destination.name}.tmp").exists())

    def test_brand_archive_preserves_a_manifest_certified_consumer_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.make_brand_source(root)
            handoff = b'{"brand":"cueson","sha256":"approved"}\n'
            (source / "consumer-handoff.json").write_bytes(handoff)
            manifest_path = source / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["files"].append({
                "path": "consumer-handoff.json",
                "bytes": len(handoff),
                "sha256": hashlib.sha256(handoff).hexdigest(),
            })
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            archive_path = root / "release" / "alpha-brand-1.0.0.zip"
            package_release.write_brand_archive(source, archive_path, root=root, expected_canon="1.2.1")
            with zipfile.ZipFile(archive_path) as archive:
                self.assertEqual(handoff, archive.read("consumer-handoff.json"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
