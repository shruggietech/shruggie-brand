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
    def make_brand_source(self, root: Path) -> Path:
        for name in package_release.LICENSES:
            (root / name).write_text(name + "\n", encoding="utf-8")
        source = root / "alpha"
        source.mkdir()
        brand = {"slug": "alpha", "title": "Alpha", "version": "1.0.0", "canon": "1.2.1", "affiliation": {}}
        bundle_buffer = io.BytesIO()
        with zipfile.ZipFile(bundle_buffer, "w") as bundle:
            bundle.writestr("SKILL.md", "---\nmetadata:\n  version: 1.2.1\n  canon: 1.2.1\n  interface-canon: 1.0.0\n---\n")
            bundle.writestr("AGENTS.md", "instructions\n")
            bundle.writestr("references/interface-canon.json", json.dumps({"version": "1.0.0"}))
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
            "enforcement/interface-canon.schema.json": b"{}\n",
            "enforcement/consumer-contract.schema.json": b"{}\n",
            "enforcement/capability-gap.example.json": json.dumps({"submission_authorized": False}).encode(),
            distribution: bundle,
        }
        provenance_names = [
            "brand.json", "enforcement/AGENTS.md", "enforcement/IMPLEMENTATION.md",
            "enforcement/interface-canon.json", "enforcement/interface-canon.schema.json",
            "enforcement/consumer-contract.schema.json", "enforcement/capability-gap.example.json", distribution,
        ]
        consumer = {
            "versions": {"brand_version": "1.0.0", "canon_version": "1.2.1", "interface_canon_version": "1.0.0", "compiler_version": "1.2.1"},
            "recovery": {
                "distribution": "shruggie-brandbuilder-1.2.1.skill",
                "path": distribution,
                "sha256": hashlib.sha256(bundle).hexdigest(),
                "sources": [{"kind": "delivered-bundle", "path": distribution, "network_required": False}],
                "instruction": "Use exact delivered bytes.",
            },
            "provenance": [
                {"path": name, "bytes": len(values[name]), "sha256": hashlib.sha256(values[name]).hexdigest()}
                for name in provenance_names
            ],
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
