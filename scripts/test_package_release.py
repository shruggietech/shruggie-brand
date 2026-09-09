#!/usr/bin/env python3
"""Regression tests for release packaging version selection."""

import hashlib
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
        values = {
            "brand.json": json.dumps({"slug": "alpha", "version": "1.0.0", "canon": "1.2.1"}).encode(),
            "VERIFY.md": b"verified\n",
            "brand-guide.pdf": b"%PDF-1.4\n",
            "logos/mark.svg": b"<svg/>\n",
        }
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
                self.assertEqual(
                    set(archive.namelist()),
                    {"brand.json", "manifest.json", "VERIFY.md", "brand-guide.pdf", "logos/mark.svg", *package_release.LICENSES},
                )

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
