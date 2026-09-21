#!/usr/bin/env python3
"""Regression tests for release metadata and archive certification."""

import hashlib
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import release_contract


ROOT = Path(__file__).resolve().parents[1]
LICENSES = ("LICENSE", "NOTICE", "LICENSE-BRAND.md")


def write_zip(path, entries):
    with zipfile.ZipFile(str(path), "w") as archive:
        for name, value in entries.items():
            archive.writestr(name, value)


def brand_archive_entries(slug="fragcap", version="1.1.0", canon="1.1.2",
                          extra_entries=None, recorded_entries=None):
    brand = {"slug": slug, "title": slug.title(), "version": version, "canon": canon}
    consumer_schema = (ROOT / "skill" / "references" / "consumer-contract.schema.json").read_bytes()
    policy = json.loads((ROOT / "skill" / "references" / "version-policy.json").read_text(encoding="utf-8"))
    bundle_buffer = io.BytesIO()
    with zipfile.ZipFile(bundle_buffer, "w") as bundle:
        bundle.writestr("SKILL.md", "---\nmetadata:\n  version: 2.0.0\n  canon: %s\n  interface-canon: 1.0.0\n  component-recipes: 1.0.0\n  web-react-adapter: 1.0.0\n  egui-adapter: 1.0.0\n---\n" % canon)
        bundle.writestr("AGENTS.md", "instructions\n")
        bundle.writestr("references/interface-canon.json", json.dumps({"version": "1.0.0"}))
        bundle.writestr("references/component-recipes.json", json.dumps({"version": "1.0.0"}))
        bundle.writestr("references/component-recipes.schema.json", (ROOT / "skill" / "references" / "component-recipes.schema.json").read_bytes())
        bundle.writestr("references/version-policy.json", json.dumps(policy))
        bundle.writestr("references/consumer-contract.schema.json", consumer_schema)
        bundle.writestr("references/documentation-contract.json", (ROOT / "skill" / "references" / "documentation-contract.json").read_bytes())
        bundle.writestr("references/documentation-contract.schema.json", (ROOT / "skill" / "references" / "documentation-contract.schema.json").read_bytes())
        bundle.writestr("references/release-impact.json", (ROOT / "skill" / "references" / "release-impact.json").read_bytes())
        bundle.writestr("references/release-impact.schema.json", (ROOT / "skill" / "references" / "release-impact.schema.json").read_bytes())
        bundle.writestr("templates/documentation_contract.py", "# documentation contract\n")
        bundle.writestr("templates/verify.py", "# verifier\n")
        bundle.writestr("templates/validate_glyph.py", "# glyph gate\n")
    bundle = bundle_buffer.getvalue()
    begin = "<!-- BEGIN SHRUGGIE-BRANDBUILDER: CONSUMER CONTRACT -->"
    end = "<!-- END SHRUGGIE-BRANDBUILDER: CONSUMER CONTRACT -->"
    distribution = "enforcement/distributions/shruggie-brandbuilder-2.0.0.skill"
    versions = {"brand_version": version, "canon_version": canon, "interface_canon_version": "1.0.0", "component_recipe_version": "1.0.0", "web_react_adapter_version": "1.0.0", "egui_adapter_version": "1.0.0", "compiler_version": "2.0.0"}
    package = {"id": "%s-brand-%s-bb2.0.0" % (slug, version), "filename": "%s-brand-%s-bb2.0.0.zip" % (slug, version), "brand_slug": slug, "brand_version": version, "brandbuilder_version": "2.0.0"}
    kit_bundle = {"schema_version": 1, "package": package, "versions": versions, "source_revision": "a" * 40, "publication": {"status": "candidate", "version": "2.0.0", "tag": "v2.0.0"}, "checksum_authority": {"algorithm": "sha256", "manifest": "manifest.json", "release_checksums": None}}
    values = {
        "brand.json": json.dumps(brand).encode("utf-8"),
        "VERIFY.md": b"verification",
        "brand-guide.pdf": b"%PDF-1.4\n",
        "enforcement/AGENTS.md": (begin + "\ncontract\n" + end + "\n").encode("utf-8"),
        "enforcement/IMPLEMENTATION.md": b"# Implementation\n",
        "enforcement/MIGRATION.md": b"# Migration\n",
        "enforcement/bundle.json": json.dumps(kit_bundle).encode("utf-8"),
        "enforcement/release-impact.json": (ROOT / "skill" / "references" / "release-impact.json").read_bytes(),
        "enforcement/release-impact.schema.json": (ROOT / "skill" / "references" / "release-impact.schema.json").read_bytes(),
        "enforcement/interface-canon.json": json.dumps({"version": "1.0.0"}).encode("utf-8"),
        "enforcement/interface-canon.schema.json": b"{}\n",
        "enforcement/component-recipes.json": json.dumps({"version": "1.0.0"}).encode("utf-8"),
        "enforcement/component-recipes.schema.json": (ROOT / "skill" / "references" / "component-recipes.schema.json").read_bytes(),
        "enforcement/version-policy.json": json.dumps(policy).encode("utf-8"),
        "enforcement/consumer-contract.schema.json": consumer_schema,
        "enforcement/documentation-contract.json": (ROOT / "skill" / "references" / "documentation-contract.json").read_bytes(),
        "enforcement/documentation-contract.schema.json": (ROOT / "skill" / "references" / "documentation-contract.schema.json").read_bytes(),
        "enforcement/documentation-facts.json": b"{}",
        "web/adapter.json": json.dumps({"adapter_version": "1.0.0", "component_recipe_version": "1.0.0"}).encode("utf-8"),
        "web/support-matrix.json": json.dumps({"adapter_version": "1.0.0"}).encode("utf-8"),
        "native/egui/adapter.json": json.dumps({"adapter_version": "1.0.0", "component_recipe_version": "1.0.0"}).encode("utf-8"),
        "native/egui/Cargo.lock": b"# deterministic lockfile\n",
        "native/egui/support-matrix.json": json.dumps({"adapter_version": "1.0.0"}).encode("utf-8"),
        "enforcement/capability-gap.example.json": json.dumps({"submission_authorized": False}).encode("utf-8"),
        distribution: bundle,
    }
    values.update({name: name.encode("utf-8") for name in LICENSES})
    values.update(extra_entries or {})
    provenance_names = [
        "brand.json", "enforcement/AGENTS.md", "enforcement/IMPLEMENTATION.md",
        "enforcement/interface-canon.json", "enforcement/interface-canon.schema.json",
        "enforcement/component-recipes.json", "enforcement/component-recipes.schema.json",
        "enforcement/version-policy.json", "web/adapter.json", "web/support-matrix.json",
        "native/egui/Cargo.lock", "native/egui/adapter.json", "native/egui/support-matrix.json",
        "enforcement/consumer-contract.schema.json", "enforcement/capability-gap.example.json", distribution,
        "enforcement/documentation-contract.json", "enforcement/documentation-contract.schema.json", "enforcement/documentation-facts.json",
        "enforcement/MIGRATION.md", "enforcement/bundle.json", "enforcement/release-impact.json", "enforcement/release-impact.schema.json",
    ]
    consumer = {
        "schema_version": 4,
        "brand": {"slug": slug, "title": slug.title(), "affiliation": None, "brand_version": version},
        "bundle": kit_bundle,
        "versions": versions,
        "version_semantics": {
            "brand_version": "Brand version.", "canon_version": "Brand Canon version.",
            "interface_canon_version": "Interface Canon version.", "component_recipe_version": "Component recipe version.", "web_react_adapter_version": "Web adapter version.", "egui_adapter_version": "egui adapter version.", "compiler_version": "Compiler version.",
        },
        "compatibility": {
            "policy_version": policy["version"], "status": "compatible",
            "validated_versions": {
                "brand_canon": canon, "interface_canon": "1.0.0", "component_recipes": "1.0.0",
                "web_react_adapter": "1.0.0", "egui_adapter": "1.0.0", "compiler": "2.0.0", "brand": version,
            },
            "rules_checked": len(policy["compatibility_rules"]),
        },
        "environment": {
            "renderer": "renderer-neutral", "host": "none", "supported_targets": ["web"],
            "viewport_profiles": ["compact"], "adapter_versions": {"vanilla": "2.0.0"},
        },
        "authority": {
            "brand_source": "brand.json", "bundle": "enforcement/bundle.json", "release_impact": "enforcement/release-impact.json", "migration_summary": "enforcement/MIGRATION.md", "interface_canon": "enforcement/interface-canon.json", "component_recipes": "enforcement/component-recipes.json", "version_policy": "enforcement/version-policy.json", "web_adapter": "web/adapter.json", "support_matrix": "web/support-matrix.json", "egui_adapter": "native/egui/adapter.json", "egui_support_matrix": "native/egui/support-matrix.json",
            "instructions": "enforcement/IMPLEMENTATION.md", "precedence": ["brand.json"],
            "documentation_contract": "enforcement/documentation-contract.json", "documentation_facts": "enforcement/documentation-facts.json",
            "permitted_exceptions": [],
        },
        "verification": {
            "entry_points": ["python3 enforcement/brandbuilder/templates/verify.py .", "python3 enforcement/brandbuilder/templates/validate_glyph.py brand.json"],
            "success": "zero failures",
        },
        "recovery": {
            "distribution": "shruggie-brandbuilder-2.0.0.skill",
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
    values["enforcement/consumer-contract.json"] = json.dumps(consumer).encode("utf-8")
    always_recorded = set(provenance_names) | {"enforcement/consumer-contract.json"}
    files = []
    for name in sorted(always_recorded | set(recorded_entries or ())):
        value = values[name]
        files.append({"path": name, "bytes": len(value),
                      "sha256": hashlib.sha256(value).hexdigest()})
    values["manifest.json"] = json.dumps({
        "name": "%s-brand-kit" % slug,
        "version": version,
        "canon": canon,
        "files": files,
    }).encode("utf-8")
    return values


def replace_consumer(entries, consumer):
    consumer_bytes = json.dumps(consumer).encode("utf-8")
    entries["enforcement/consumer-contract.json"] = consumer_bytes
    manifest = json.loads(entries["manifest.json"].decode("utf-8"))
    for item in manifest["files"]:
        if item["path"] == "enforcement/consumer-contract.json":
            item["bytes"] = len(consumer_bytes)
            item["sha256"] = hashlib.sha256(consumer_bytes).hexdigest()
    entries["manifest.json"] = json.dumps(manifest).encode("utf-8")


class ReleaseContractTests(unittest.TestCase):
    def test_publication_record_distinguishes_candidates_and_exact_releases(self):
        revision = "a" * 40
        metadata = {
            "version": "2.0.0",
            "brands": {
                "fragcap": {"version": "1.1.0"},
                "eso-weave": {"version": "1.0.0"},
            },
        }
        base = {
            "schemaVersion": 1, "status": "candidate", "version": "2.0.0", "tag": "v2.0.0",
            "sourceRevision": revision,
            "releaseUrl": "https://github.com/ShruggieTech/shruggie-brand/releases/tag/v2.0.0",
            "skillFilename": "shruggie-brandbuilder-2.0.0.skill",
            "skillUrl": "https://github.com/ShruggieTech/shruggie-brand/releases/download/v2.0.0/shruggie-brandbuilder-2.0.0.skill",
            "packages": [
                release_contract.package_identity("eso-weave", "1.0.0", "2.0.0"),
                release_contract.package_identity("fragcap", "1.1.0", "2.0.0"),
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "publication.json"
            path.write_text(json.dumps(base), encoding="utf-8")
            self.assertEqual("candidate", release_contract.verify_publication_record(path, metadata, revision)["status"])
            with self.assertRaisesRegex(ValueError, "requires exact release status"):
                release_contract.verify_publication_record(path, metadata, revision, require_release=True)
            released = dict(base, status="release")
            path.write_text(json.dumps(released), encoding="utf-8")
            self.assertEqual("release", release_contract.verify_publication_record(path, metadata, revision, require_release=True)["status"])
            path.write_text(json.dumps(dict(released, releaseUrl="https://github.com/ShruggieTech/shruggie-brand/releases/latest")), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not exact"):
                release_contract.verify_publication_record(path, metadata, revision, require_release=True)
            path.write_text(json.dumps(dict(released, releaseUrl="https://example.com/releases/tag/v2.0.0")), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not exact"):
                release_contract.verify_publication_record(path, metadata, revision, require_release=True)
            path.write_text(json.dumps(dict(released, skillUrl="https://example.com/releases/download/v2.0.0/shruggie-brandbuilder-2.0.0.skill")), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "skill destination disagrees"):
                release_contract.verify_publication_record(path, metadata, revision, require_release=True)

    def test_publication_record_requires_exact_canonical_package_inventory(self):
        revision = "a" * 40
        metadata = {
            "version": "2.0.0",
            "brands": {"fragcap": {"version": "1.1.0"}},
        }
        record = {
            "schemaVersion": 1, "status": "release", "version": "2.0.0", "tag": "v2.0.0",
            "sourceRevision": revision,
            "releaseUrl": "https://github.com/ShruggieTech/shruggie-brand/releases/tag/v2.0.0",
            "skillFilename": "shruggie-brandbuilder-2.0.0.skill",
            "skillUrl": "https://github.com/ShruggieTech/shruggie-brand/releases/download/v2.0.0/shruggie-brandbuilder-2.0.0.skill",
            "packages": [],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "publication.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "package inventory disagrees"):
                release_contract.verify_publication_record(path, metadata, revision, require_release=True)

            record["packages"] = [release_contract.package_identity("fragcap", "1.0.0", "2.0.0")]
            path.write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "package inventory disagrees"):
                release_contract.verify_publication_record(path, metadata, revision, require_release=True)

    def test_production_logo_source_modes_and_identity_fingerprints_are_pinned(self):
        expected = {
            "cueson": ("constructed", "e9731717f34f149f78b221a857d127cad60e09ae1e3c8cf2f09d3de0ae0624f9"),
            "covarity": ("constructed", "b9846d9b00e393092678164a7d5f1c24cfd4186e2d2490b3d8a87be8e3b8e40c"),
            "fragcap": ("constructed", "47877d1667ac44ab6c81ed41ab675cf8831b7644e4926c4df93eeca024805e3b"),
            "glitchpad": ("constructed", "3115a137763ff75ab64a036282f9bc5bf683a3b4d68ffda6d0d5839da030c95e"),
            "go-schedule": ("constructed", "95ce6d68210a79672af6d639a4610070e61269842d414de63194fd0ed25fb5a6"),
            "shruggietech": ("authoritative", "da15b5819b777ff3c1323d801b52333b0fd8015bbe08443bd7bc53085616cad7"),
        }
        for slug, (mode, fingerprint) in expected.items():
            brand = json.loads((ROOT / "brands" / slug / "brand.json").read_text(encoding="utf-8"))
            payload = json.dumps(brand["logo"]["paths"], sort_keys=True, separators=(",", ":")).encode("utf-8")
            self.assertEqual(mode, brand["logo"]["source_mode"], slug)
            self.assertEqual(fingerprint, hashlib.sha256(payload).hexdigest(), slug)
        shruggietech = json.loads((ROOT / "brands" / "shruggietech" / "brand.json").read_text(encoding="utf-8"))
        self.assertEqual({"full": "full-mark-master", "reduced": "reduced-mark-master"},
                         shruggietech["logo"]["authoritative_input_ids"])
        inputs = {item["id"]: item for item in shruggietech["authoritative_inputs"]}
        for input_id in shruggietech["logo"]["authoritative_input_ids"].values():
            path = ROOT / "brands" / "shruggietech" / inputs[input_id]["path"]
            self.assertEqual(inputs[input_id]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(inputs[input_id]["sha256"], inputs[input_id]["mask_source_sha256"])
            self.assertIn(inputs[input_id]["approved_mask"], {"alpha", "luminance"})
            self.assertEqual("Repository owner via S016 approval", inputs[input_id]["mask_approved_by"])
            self.assertEqual("2026-09-07", inputs[input_id]["mask_approved_on"])

    def test_repository_metadata_and_notes_agree_for_2_0_0(self):
        metadata = release_contract.load_metadata(ROOT, "2.0.0")
        notes = release_contract.render_notes(metadata)

        self.assertEqual(metadata["skill_version"], "2.0.0")
        self.assertEqual(metadata["canon_version"], "1.2.1")
        self.assertEqual(metadata["site_version"], "2.0.0")
        self.assertEqual(release_contract.current_version(ROOT), "2.0.0")
        self.assertIn("Skill version: `2.0.0`", notes)
        self.assertIn("Canon version: `1.2.1`", notes)
        self.assertIn("Existing kits need migration: **yes for immutable package and recovery metadata**", notes)
        self.assertIn("dependency-free environment bridge entry", notes)
        self.assertIn("## Governed release impact", notes)
        self.assertIn("No approved identity redesign is included.", notes)
        self.assertIn("Consumers may adopt the generated web, Android, Apple, macOS, and Windows asset suites", notes)
        self.assertNotIn("## [Unreleased]", notes)

    def test_expected_assets_are_exact_and_use_embedded_brand_versions(self):
        metadata = release_contract.load_metadata(ROOT, "2.0.0")

        self.assertEqual(set(release_contract.expected_assets(metadata)), {
            "shruggie-brandbuilder-2.0.0.skill",
            "shruggie-brandbuilder-2.0.0-portable.zip",
            "shruggietech-brand-1.0.0-bb2.0.0.zip",
            "fragcap-brand-1.1.0-bb2.0.0.zip",
            "go-schedule-brand-1.0.0-bb2.0.0.zip",
            "glitchpad-brand-1.1.0-bb2.0.0.zip",
            "covarity-brand-1.0.0-bb2.0.0.zip",
            "eso-weave-brand-1.0.0-bb2.0.0.zip",
            "cueson-brand-1.0.0-bb2.0.0.zip",
        })
        self.assertEqual(
            {slug: values["version"] for slug, values in metadata["brands"].items()},
            {
                "shruggietech": "1.0.0",
                "fragcap": "1.1.0",
                "go-schedule": "1.0.0",
                "glitchpad": "1.1.0",
                "covarity": "1.0.0",
                "eso-weave": "1.0.0",
                "cueson": "1.0.0",
            },
        )

    def test_requested_release_dates_must_agree(self):
        root = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        skill = (ROOT / "skill" / "CHANGELOG.md").read_text(encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "root and skill 1.2.1 release dates disagree"):
            release_contract.require_history(
                root,
                skill.replace("## 1.2.1 - 2026-09-06", "## 1.2.1 - 2026-09-07"),
                "1.2.1",
            )

    def test_build_workflow_discovers_current_release_version(self):
        workflow = (ROOT / ".github" / "workflows" / "build.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("python scripts/release_contract.py current", workflow)
        self.assertNotIn("--version 1.1.2", workflow)

    def test_release_publication_uses_the_verified_candidate_boundary(self):
        workflow = (ROOT / ".github" / "workflows" / "build.yml").read_text(
            encoding="utf-8"
        )

        self.assertFalse((ROOT / ".github" / "workflows" / "release.yml").exists())
        self.assertIn("verified-release-assets-${{ github.sha }}", workflow)
        self.assertIn("SOURCE_COMMIT", workflow)
        self.assertIn("SHA256SUMS", workflow)
        self.assertIn("git merge-base --is-ancestor", workflow)
        self.assertIn("gh release create", workflow)
        self.assertIn("--verify-tag", workflow)

    def test_site_package_version_must_match_release(self):
        original_read_text = release_contract.read_text

        def read_with_stale_site(path):
            if path == ROOT / "site" / "package.json":
                return '{"version": "1.1.2"}'
            return original_read_text(path)

        with mock.patch.object(
            release_contract, "read_text", side_effect=read_with_stale_site
        ):
            with self.assertRaisesRegex(
                ValueError, "site package version 1.1.2 does not match release 2.0.0"
            ):
                release_contract.load_metadata(ROOT, "2.0.0")

    def test_compiler_release_and_brand_canon_versions_can_diverge(self):
        original_read_text = release_contract.read_text

        def read_with_supported_older_canon(path):
            value = original_read_text(path)
            if path == ROOT / "skill" / "SKILL.md":
                return value.replace("  canon: 1.2.1", "  canon: 1.2.0")
            if path == ROOT / "skill" / "references" / "01-canon.json":
                payload = json.loads(value)
                payload["version"] = "1.2.0"
                return json.dumps(payload)
            if path.parent.parent == ROOT / "brands" and path.name == "brand.json":
                payload = json.loads(value)
                payload["canon"] = "1.2.0"
                return json.dumps(payload)
            return value

        with mock.patch.object(
            release_contract, "read_text", side_effect=read_with_supported_older_canon
        ):
            metadata = release_contract.load_metadata(ROOT, "2.0.0")
            self.assertEqual("2.0.0", metadata["skill_version"])
            self.assertEqual("1.2.0", metadata["canon_version"])
            self.assertEqual("2.0.0", release_contract.current_version(ROOT))

    def test_archive_paths_reject_parent_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.zip"
            write_zip(path, {"../outside.txt": b"bad"})

            with self.assertRaisesRegex(ValueError, "unsafe archive path"):
                release_contract.archive_entries(path)

    def test_portable_bundle_requires_agents_and_omits_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "shruggie-brandbuilder-1.2.1-portable.zip"
            entries = {name: name.encode("utf-8") for name in LICENSES}
            entries.update({"AGENTS.md": b"agents", "CHANGELOG.md": b"history",
                            "README.md": b"portable", "SKILL.md": b"forbidden"})
            write_zip(path, entries)

            with self.assertRaisesRegex(ValueError, "must omit SKILL.md"):
                release_contract.verify_skill_archive(path, portable=True)

    def test_production_archive_rejects_manifest_checksum_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fragcap-brand-1.1.0-bb2.0.0.zip"
            recorded = b"correct"
            entries = brand_archive_entries(
                extra_entries={"tokens.css": recorded},
                recorded_entries=("brand.json", "VERIFY.md", "brand-guide.pdf", "tokens.css"),
            )
            entries["tokens.css"] = b"corrupt"
            write_zip(path, entries)

            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                release_contract.verify_brand_archive(path, "fragcap", "1.1.0")

    def test_production_archive_rejects_coordinated_canon_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fragcap-brand-1.1.0-bb2.0.0.zip"
            entries = brand_archive_entries(canon="1.0.0", recorded_entries=(
                "brand.json", "VERIFY.md", "brand-guide.pdf",
            ))
            write_zip(path, entries)

            with self.assertRaisesRegex(ValueError, "authoritative canon"):
                release_contract.verify_brand_archive(
                    path, "fragcap", "1.1.0", expected_canon="1.1.2"
                )

    def test_candidate_archive_rejects_release_checksum_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fragcap-brand-1.1.0-bb2.0.0.zip"
            entries = brand_archive_entries()
            bundle = json.loads(entries["enforcement/bundle.json"].decode("utf-8"))
            bundle["checksum_authority"]["release_checksums"] = "SHA256SUMS"
            bundle_bytes = json.dumps(bundle).encode("utf-8")
            entries["enforcement/bundle.json"] = bundle_bytes
            consumer = json.loads(entries["enforcement/consumer-contract.json"].decode("utf-8"))
            consumer["bundle"] = bundle
            for item in consumer["provenance"]:
                if item["path"] == "enforcement/bundle.json":
                    item["bytes"] = len(bundle_bytes)
                    item["sha256"] = hashlib.sha256(bundle_bytes).hexdigest()
            replace_consumer(entries, consumer)
            manifest = json.loads(entries["manifest.json"].decode("utf-8"))
            for item in manifest["files"]:
                if item["path"] == "enforcement/bundle.json":
                    item["bytes"] = len(bundle_bytes)
                    item["sha256"] = hashlib.sha256(bundle_bytes).hexdigest()
            entries["manifest.json"] = json.dumps(manifest).encode("utf-8")
            write_zip(path, entries)

            with self.assertRaisesRegex(ValueError, "release checksum authority disagrees"):
                release_contract.verify_brand_archive(path, "fragcap", "1.1.0")

    def test_production_archive_rejects_coordinated_recovery_version_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fragcap-brand-1.1.0-bb2.0.0.zip"
            bundle_buffer = io.BytesIO()
            with zipfile.ZipFile(bundle_buffer, "w") as bundle:
                bundle.writestr("SKILL.md", "---\nmetadata:\n  version: 9.9.9\n  canon: 1.1.2\n  interface-canon: 1.0.0\n  component-recipes: 1.0.0\n  web-react-adapter: 1.0.0\n  egui-adapter: 1.0.0\n---\n")
                bundle.writestr("AGENTS.md", "instructions\n")
                bundle.writestr("references/interface-canon.json", json.dumps({"version": "1.0.0"}))
                bundle.writestr("references/component-recipes.json", json.dumps({"version": "1.0.0"}))
                bundle.writestr("references/component-recipes.schema.json", (ROOT / "skill" / "references" / "component-recipes.schema.json").read_bytes())
                bundle.writestr("references/version-policy.json", (ROOT / "skill" / "references" / "version-policy.json").read_bytes())
                bundle.writestr("references/consumer-contract.schema.json", (ROOT / "skill" / "references" / "consumer-contract.schema.json").read_bytes())
                bundle.writestr("references/documentation-contract.json", (ROOT / "skill" / "references" / "documentation-contract.json").read_bytes())
                bundle.writestr("references/documentation-contract.schema.json", (ROOT / "skill" / "references" / "documentation-contract.schema.json").read_bytes())
                bundle.writestr("references/release-impact.json", (ROOT / "skill" / "references" / "release-impact.json").read_bytes())
                bundle.writestr("references/release-impact.schema.json", (ROOT / "skill" / "references" / "release-impact.schema.json").read_bytes())
                bundle.writestr("templates/documentation_contract.py", "# documentation contract\n")
                bundle.writestr("templates/verify.py", "# verifier\n")
                bundle.writestr("templates/validate_glyph.py", "# glyph gate\n")
            distribution = "enforcement/distributions/shruggie-brandbuilder-2.0.0.skill"
            entries = brand_archive_entries(extra_entries={distribution: bundle_buffer.getvalue()})
            consumer = json.loads(entries["enforcement/consumer-contract.json"].decode("utf-8"))
            recovery_bytes = entries[distribution]
            consumer["recovery"]["sha256"] = hashlib.sha256(recovery_bytes).hexdigest()
            for item in consumer["provenance"]:
                if item["path"] == distribution:
                    item["bytes"] = len(recovery_bytes)
                    item["sha256"] = hashlib.sha256(recovery_bytes).hexdigest()
            consumer_bytes = json.dumps(consumer).encode("utf-8")
            entries["enforcement/consumer-contract.json"] = consumer_bytes
            manifest = json.loads(entries["manifest.json"].decode("utf-8"))
            for item in manifest["files"]:
                if item["path"] == "enforcement/consumer-contract.json":
                    item["bytes"] = len(consumer_bytes)
                    item["sha256"] = hashlib.sha256(consumer_bytes).hexdigest()
            entries["manifest.json"] = json.dumps(manifest).encode("utf-8")
            write_zip(path, entries)

            with self.assertRaisesRegex(ValueError, "recovery compiler_version disagrees"):
                release_contract.verify_brand_archive(
                    path, "fragcap", "1.1.0", expected_canon="1.1.2"
                )

    def test_production_archive_rejects_consumer_contract_schema_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fragcap-brand-1.1.0-bb2.0.0.zip"
            entries = brand_archive_entries()
            consumer = json.loads(entries["enforcement/consumer-contract.json"].decode("utf-8"))
            consumer["version_semantics"] = {}
            entries["enforcement/consumer-contract.json"] = json.dumps(consumer).encode("utf-8")
            write_zip(path, entries)

            with self.assertRaisesRegex(ValueError, "consumer contract schema violation"):
                release_contract.verify_brand_archive(path, "fragcap", "1.1.0")

    def test_production_archive_binds_complete_consumer_brand_metadata(self):
        for field, value in (("title", "Impostor"), ("affiliation", {"parent": "false-owner"})):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "fragcap-brand-1.1.0-bb2.0.0.zip"
                entries = brand_archive_entries()
                consumer = json.loads(entries["enforcement/consumer-contract.json"].decode("utf-8"))
                consumer["brand"][field] = value
                replace_consumer(entries, consumer)
                write_zip(path, entries)

                with self.assertRaisesRegex(ValueError, "consumer brand metadata disagrees"):
                    release_contract.verify_brand_archive(path, "fragcap", "1.1.0")

    def test_production_archive_requires_every_contract_declared_authority_path(self):
        cases = (
            ("authority", "brand_source"),
            ("authority", "instructions"),
            ("authority", "interface_canon"),
            ("capability_gap", "template_path"),
        )
        for section, field in cases:
            with self.subTest(section=section, field=field), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "fragcap-brand-1.1.0-bb2.0.0.zip"
                entries = brand_archive_entries()
                consumer = json.loads(entries["enforcement/consumer-contract.json"].decode("utf-8"))
                consumer[section][field] = "enforcement/missing-%s.json" % field
                replace_consumer(entries, consumer)
                write_zip(path, entries)

                with self.assertRaisesRegex(ValueError, "consumer declared .* path is missing"):
                    release_contract.verify_brand_archive(path, "fragcap", "1.1.0")

    def test_production_archive_requires_verification_and_qc_manifest_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fragcap-brand-1.1.0-bb2.0.0.zip"
            entries = brand_archive_entries(
                extra_entries={"qc/contact-sheet.png": b"png"},
                recorded_entries=("brand.json", "brand-guide.pdf"),
            )
            write_zip(path, entries)

            with self.assertRaisesRegex(ValueError, "unrecorded files.*VERIFY.md.*qc/"):
                release_contract.verify_brand_archive(
                    path, "fragcap", "1.1.0", expected_canon="1.1.2"
                )

    def test_production_archive_rejects_tampered_recorded_qc(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fragcap-brand-1.1.0-bb2.0.0.zip"
            entries = brand_archive_entries(
                extra_entries={"qc/contact-sheet.png": b"original"},
                recorded_entries=(
                    "brand.json", "VERIFY.md", "brand-guide.pdf", "qc/contact-sheet.png",
                ),
            )
            entries["qc/contact-sheet.png"] = b"tampered"
            write_zip(path, entries)

            with self.assertRaisesRegex(ValueError, "checksum mismatch.*qc/contact-sheet.png"):
                release_contract.verify_brand_archive(
                    path, "fragcap", "1.1.0", expected_canon="1.1.2"
                )

    def test_production_archive_rejects_recorded_empty_delivery(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fragcap-brand-1.1.0-bb2.0.0.zip"
            entries = brand_archive_entries(
                extra_entries={"logos/empty.svg": b""},
                recorded_entries=(
                    "brand.json", "VERIFY.md", "brand-guide.pdf", "logos/empty.svg",
                ),
            )
            write_zip(path, entries)

            with self.assertRaisesRegex(ValueError, "unexpectedly empty.*logos/empty.svg"):
                release_contract.verify_brand_archive(
                    path, "fragcap", "1.1.0", expected_canon="1.1.2"
                )

    def test_release_directory_rejects_unexpected_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            release_dir = Path(tmp)
            metadata = {"version": "1.2.0", "brands": {}}
            (release_dir / "unexpected.zip").write_bytes(b"stale")

            with self.assertRaisesRegex(ValueError, "unexpected release assets"):
                release_contract.verify_release_directory(release_dir, metadata)


if __name__ == "__main__":
    unittest.main(verbosity=2)
