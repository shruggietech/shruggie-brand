#!/usr/bin/env python3
"""Isolated contract tests for the evergreen README audit."""

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
[Brand site](https://brand.shruggie.tech/)
[License](LICENSE#terms)
"""

    def problems(self, readme: str):
        return audit(self.root, readme, ROUTES)

    def test_valid_front_door_does_not_require_each_brand(self) -> None:
        self.assertEqual([], self.problems(self.valid))

    def test_portfolio_snapshots_are_rejected(self) -> None:
        for addition in ("Eight production brand kits exist.\n", "8 brands are published.\n",
                         "## Brand kits\n", "[Alpha](https://brand.shruggie.tech/alpha/guidelines/)\n",
                         "python scripts/build_all.py alpha\n", "Beta is a sample brand.\n"):
            with self.subTest(addition=addition):
                self.assertIn("portfolio snapshot", "\n".join(self.problems(self.valid + addition)))

    def test_technical_counts_and_project_identity_are_allowed(self) -> None:
        self.assertEqual([], self.problems(self.valid + "WCAG 2.1 AA, 4px spacing, and ShruggieTech identity.\n"))

    def test_local_paths_and_traversal(self) -> None:
        self.assertIn("missing local target", "\n".join(self.problems(self.valid + "[Missing](gone.md)\n")))
        self.assertIn("unsafe local target", "\n".join(self.problems(self.valid + "[Escape](%2e%2e/secret.txt)\n")))
        self.assertIn("unsafe local target", "\n".join(self.problems(self.valid + "[License](LICENSE?raw=1)\n")))
        self.assertEqual([], self.problems(self.valid + "[Top](#front-door)\n"))

    def test_site_route_and_host(self) -> None:
        self.assertIn("undeclared site route", "\n".join(self.problems(self.valid + "[Bad](https://brand.shruggie.tech/alpha/)\n")))
        self.assertIn("untrusted site host", "\n".join(self.problems(self.valid + "[Bad](https://brand.shruggie.tech.evil/alpha/)\n")))
        self.assertIn("unsupported URL scheme", "\n".join(self.problems(self.valid + "[Bad](javascript:alert)\n")))
        self.assertIn("unsupported URL scheme or authority", "\n".join(self.problems(self.valid + "[Bad](https://%62rand.shruggie.tech/not-a-route/)\n")))

    def test_authoritative_destinations_are_navigable(self) -> None:
        self.assertIn("missing brand site", "\n".join(self.problems(self.valid.replace("[Brand site](https://brand.shruggie.tech/)", "![Brand site](https://brand.shruggie.tech/)"))))
        self.assertIn("missing latest official release", "\n".join(self.problems(self.valid.replace("[Latest official release](https://github.com/shruggietech/shruggie-brand/releases/latest)", "![Release](https://github.com/shruggietech/shruggie-brand/releases/latest)"))))
        self.assertEqual([], self.problems(self.valid.replace("[Brand site](https://brand.shruggie.tech/)", '<a href="https://brand.shruggie.tech/">Brand site</a>')))
        self.assertEqual([], self.problems(self.valid.replace("[Brand site](https://brand.shruggie.tech/)", "[Site][site]\n\n[site]: https://brand.shruggie.tech/")))

    def test_images_require_alt_and_valid_targets(self) -> None:
        self.assertIn("missing image alt", "\n".join(self.problems(self.valid + '<img src="brand.png">\n')))
        self.assertIn("missing image alt", "\n".join(self.problems(self.valid + '![](brand.png)\n')))
        self.assertIn("missing image alt", "\n".join(self.problems(self.valid + '![][logo]\n[logo]: brand.png\n')))
        self.assertIn("missing image alt", "\n".join(self.problems(self.valid + '![   ][logo]\n[logo]: brand.png\n')))
        self.assertEqual([], self.problems(self.valid + '![Brand mark][logo]\n[logo]: brand.png\n'))
        self.assertIn("missing local target", "\n".join(self.problems(self.valid + '<img src="missing.png" alt="Brand">\n')))
        self.assertIn("missing local target", "\n".join(self.problems(self.valid.replace('srcset="brand.png"', 'srcset="brand.png 1x, missing.png 2x"'))))

    def test_autolinks_and_fenced_examples(self) -> None:
        self.assertIn("undeclared site route", "\n".join(self.problems(self.valid + "<https://brand.shruggie.tech/not-a-route/>\n")))
        self.assertIn("undeclared site route", "\n".join(self.problems(self.valid + "See https://brand.shruggie.tech/not-a-route/.\n")))
        self.assertEqual([], self.problems(self.valid + "\n```md\n[Example](missing.md)\n![](example.png)\n![][logo]\n<img src=\"example.png\">\n```\n"))

    def test_versioned_builder_asset_rejected(self) -> None:
        self.assertIn("versioned BrandBuilder asset", "\n".join(self.problems(self.valid + "Get shruggie-brandbuilder-2.0.0.skill\n")))


if __name__ == "__main__":
    unittest.main()
