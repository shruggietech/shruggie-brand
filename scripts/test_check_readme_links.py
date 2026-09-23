#!/usr/bin/env python3
"""Isolated contract tests for the README publication-link audit."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_readme_links import audit  # noqa: E402


ROUTES = {
    "siteUrl": "https://brand.shruggie.tech",
    "routes": [
        {"kind": "home", "pathname": "/", "canonical": "https://brand.shruggie.tech/", "brandSlug": None},
        {"kind": "guidelines", "pathname": "/alpha/guidelines/", "canonical": "https://brand.shruggie.tech/alpha/guidelines/", "brandSlug": "alpha"},
        {"kind": "guidelines", "pathname": "/beta/guidelines/", "canonical": "https://brand.shruggie.tech/beta/guidelines/", "brandSlug": "beta"},
    ],
}


class ReadmeLinkAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "LICENSE").write_text("code license\n", encoding="utf-8")
        (self.root / "brand.png").write_bytes(b"approved")
        self.valid = """# Front door
<picture><source media="(prefers-color-scheme: dark)" srcset="brand.png"><img src="brand.png" alt="Brand"></picture>
[![Build status](https://github.com/example/repo/actions/workflows/build.yml/badge.svg)](https://github.com/example/repo/actions/workflows/build.yml)
[Latest official release](https://github.com/shruggietech/shruggie-brand/releases/latest)
[Alpha](https://brand.shruggie.tech/alpha/guidelines/)
[Beta](https://brand.shruggie.tech/beta/guidelines/)
[License](LICENSE#terms)
"""

    def problems(self, readme: str):
        return audit(self.root, readme, ROUTES)

    def test_valid_links_images_and_badge(self) -> None:
        self.assertEqual([], self.problems(self.valid))

    def test_missing_local_target_fails(self) -> None:
        self.assertIn("missing local target", "\n".join(self.problems(self.valid + "[Missing](gone.md)\n")))

    def test_encoded_traversal_fails(self) -> None:
        self.assertIn("unsafe local target", "\n".join(self.problems(self.valid + "[Escape](%2e%2e/secret.txt)\n")))

    def test_noncanonical_brand_route_fails(self) -> None:
        text = self.valid.replace("/alpha/guidelines/", "/alpha/")
        self.assertIn("undeclared site route", "\n".join(self.problems(text)))

    def test_lookalike_host_fails(self) -> None:
        text = self.valid.replace("brand.shruggie.tech/alpha", "brand.shruggie.tech.evil/alpha")
        self.assertIn("untrusted site host", "\n".join(self.problems(text)))

    def test_omitted_brand_fails(self) -> None:
        text = self.valid.replace("[Beta](https://brand.shruggie.tech/beta/guidelines/)\n", "")
        self.assertIn("missing brand overview", "\n".join(self.problems(text)))

    def test_html_image_target_is_checked(self) -> None:
        text = self.valid.replace('src="brand.png"', 'src="missing.png"')
        self.assertIn("missing local target", "\n".join(self.problems(text)))

    def test_unsafe_scheme_fails(self) -> None:
        self.assertIn("unsupported URL scheme", "\n".join(self.problems(self.valid + "[Bad](javascript:alert)\n")))

    def test_reference_definition_target_is_checked(self) -> None:
        self.assertIn("missing local target", "\n".join(self.problems(self.valid + "[Guide][manual]\n\n[manual]: missing.md\n")))

    def test_local_query_is_not_treated_as_a_file(self) -> None:
        self.assertIn("unsafe local target", "\n".join(self.problems(self.valid + "[License](LICENSE?raw=1)\n")))

    def test_same_document_fragment_is_allowed(self) -> None:
        self.assertEqual([], self.problems(self.valid + "[Top](#front-door)\n"))

    def test_second_srcset_candidate_is_checked(self) -> None:
        text = self.valid.replace('srcset="brand.png"', 'srcset="brand.png 1x, missing.png 2x"')
        self.assertIn("missing local target", "\n".join(self.problems(text)))

    def test_latest_official_release_destination_is_required(self) -> None:
        text = self.valid.replace("https://github.com/shruggietech/shruggie-brand/releases/latest", "https://github.com/shruggietech/shruggie-brand/releases")
        self.assertIn("missing latest official release", "\n".join(self.problems(text)))

    def test_versioned_builder_artifact_name_fails(self) -> None:
        self.assertIn("versioned BrandBuilder asset", "\n".join(self.problems(self.valid + "Get shruggie-brandbuilder-2.0.0.skill\n")))

    def test_fenced_example_links_are_not_public_destinations(self) -> None:
        self.assertEqual([], self.problems(self.valid + "\n```md\n[Example](missing.md)\n```\n"))


if __name__ == "__main__":
    unittest.main()
