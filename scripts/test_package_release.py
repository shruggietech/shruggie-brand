#!/usr/bin/env python3
"""Regression tests for release packaging version selection."""

import unittest
from pathlib import Path
from unittest import mock

import package_release


ROOT = Path(__file__).resolve().parents[1]


class PackageReleaseTests(unittest.TestCase):
    def test_omitted_version_uses_validated_current_metadata(self):
        with mock.patch.object(package_release, "current_version", return_value="1.2.0") as current:
            self.assertEqual(package_release.resolve_version(ROOT, None), "1.2.0")
        current.assert_called_once_with(ROOT)

    def test_explicit_version_does_not_rediscover_current_metadata(self):
        with mock.patch.object(package_release, "current_version") as current:
            self.assertEqual(package_release.resolve_version(ROOT, "1.2.0"), "1.2.0")
        current.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
