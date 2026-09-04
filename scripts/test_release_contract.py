#!/usr/bin/env python3
"""Regression tests for release metadata and archive certification."""

import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import release_contract


ROOT = Path(__file__).resolve().parents[1]
LICENSES = ("LICENSE", "NOTICE", "LICENSE-BRAND.md")


def write_zip(path, entries):
    with zipfile.ZipFile(str(path), "w") as archive:
        for name, value in entries.items():
            archive.writestr(name, value)


def brand_archive_entries(slug="fragcap", version="1.1.0", canon="1.1.2",
                          extra_entries=None, recorded_entries=None):
    brand = {"slug": slug, "version": version, "canon": canon}
    values = {
        "brand.json": json.dumps(brand).encode("utf-8"),
        "VERIFY.md": b"verification",
        "brand-guide.pdf": b"%PDF-1.4\n",
    }
    values.update({name: name.encode("utf-8") for name in LICENSES})
    values.update(extra_entries or {})
    files = []
    for name in recorded_entries or ():
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


class ReleaseContractTests(unittest.TestCase):
    def test_repository_metadata_and_notes_agree_for_1_1_2(self):
        metadata = release_contract.load_metadata(ROOT, "1.1.2")
        notes = release_contract.render_notes(metadata)

        self.assertEqual(metadata["skill_version"], "1.1.2")
        self.assertEqual(metadata["canon_version"], "1.1.2")
        self.assertIn("Skill version: `1.1.2`", notes)
        self.assertIn("Canon version: `1.1.2`", notes)
        self.assertIn("Existing kits need migration: **yes**", notes)
        self.assertIn("Aligned SVG-renderer capability reporting", notes)
        self.assertNotIn("## [Unreleased]", notes)

    def test_expected_assets_are_exact_and_use_embedded_brand_versions(self):
        metadata = release_contract.load_metadata(ROOT, "1.1.2")

        self.assertEqual(set(release_contract.expected_assets(metadata)), {
            "shruggie-brandbuilder-1.1.2.skill",
            "shruggie-brandbuilder-1.1.2-portable.zip",
            "shruggietech-brand-1.0.0.zip",
            "fragcap-brand-1.1.0.zip",
            "go-schedule-brand-1.0.0.zip",
            "glitchpad-brand-1.0.0.zip",
            "covarity-brand-1.0.0.zip",
        })

    def test_archive_paths_reject_parent_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.zip"
            write_zip(path, {"../outside.txt": b"bad"})

            with self.assertRaisesRegex(ValueError, "unsafe archive path"):
                release_contract.archive_entries(path)

    def test_portable_bundle_requires_agents_and_omits_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "shruggie-brandbuilder-1.1.2-portable.zip"
            entries = {name: name.encode("utf-8") for name in LICENSES}
            entries.update({"AGENTS.md": b"agents", "CHANGELOG.md": b"history",
                            "README.md": b"portable", "SKILL.md": b"forbidden"})
            write_zip(path, entries)

            with self.assertRaisesRegex(ValueError, "must omit SKILL.md"):
                release_contract.verify_skill_archive(path, portable=True)

    def test_production_archive_rejects_manifest_checksum_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fragcap-brand-1.1.0.zip"
            brand = {"slug": "fragcap", "version": "1.1.0", "canon": "1.1.2"}
            recorded = b"correct"
            manifest = {
                "name": "fragcap-brand-kit",
                "version": "1.1.0",
                "canon": "1.1.2",
                "files": [{"path": "tokens.css", "bytes": len(recorded),
                           "sha256": hashlib.sha256(recorded).hexdigest()}],
            }
            entries = {name: name.encode("utf-8") for name in LICENSES}
            entries.update({
                "brand.json": json.dumps(brand).encode("utf-8"),
                "manifest.json": json.dumps(manifest).encode("utf-8"),
                "VERIFY.md": b"verification",
                "brand-guide.pdf": b"%PDF-1.4\n",
                "tokens.css": b"corrupt",
            })
            write_zip(path, entries)

            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                release_contract.verify_brand_archive(path, "fragcap", "1.1.0")

    def test_production_archive_rejects_coordinated_canon_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fragcap-brand-1.1.0.zip"
            entries = brand_archive_entries(canon="1.0.0", recorded_entries=(
                "brand.json", "VERIFY.md", "brand-guide.pdf",
            ))
            write_zip(path, entries)

            with self.assertRaisesRegex(ValueError, "authoritative canon"):
                release_contract.verify_brand_archive(
                    path, "fragcap", "1.1.0", expected_canon="1.1.2"
                )

    def test_production_archive_requires_verification_and_qc_manifest_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fragcap-brand-1.1.0.zip"
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
            path = Path(tmp) / "fragcap-brand-1.1.0.zip"
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

    def test_release_directory_rejects_unexpected_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            release_dir = Path(tmp)
            metadata = {"version": "1.1.2", "brands": {}}
            (release_dir / "unexpected.zip").write_bytes(b"stale")

            with self.assertRaisesRegex(ValueError, "unexpected release assets"):
                release_contract.verify_release_directory(release_dir, metadata)


if __name__ == "__main__":
    unittest.main(verbosity=2)
