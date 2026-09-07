#!/usr/bin/env python3
"""Contract tests for the non-publishing S015 identity-color study."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import glitchpad_color_study as study


class GlitchpadColorStudyTests(unittest.TestCase):
    def test_candidate_matrices_are_complete_and_hex_only(self):
        self.assertEqual({"context-switch"}, set(study.CANDIDATES))
        for candidate in study.CANDIDATES.values():
            study.validate_candidate(candidate)
            for context in ("dark", "light"):
                mapping = candidate[context]
                self.assertEqual(set(study.REQUIRED_ROLES), set(mapping))
                for role in study.REQUIRED_ROLES:
                    self.assertRegex(mapping[role], r"^#[0-9A-F]{6}$")
                    self.assertNotEqual("#867100", mapping[role])

    def test_protected_geometry_fingerprints_match_merged_source(self):
        brand = study.load_brand()
        self.assertEqual("ec36a47b2b39d00501163fc189b8dfe8d780580496f013771ccc2301548fb843", study.path_fingerprint(brand))
        self.assertEqual("8d5ca8d2a54e56831a20735d4f374ffd824e0f2e5f5f79b8c05a8a78f4bfb1ad", study.layout_fingerprint(brand))

    def test_contrast_observations_cover_every_candidate_context(self):
        observations = study.contrast_observations()
        pairs = {(item["candidate"], item["context"]) for item in observations}
        self.assertEqual({(candidate, context) for candidate in study.CANDIDATES for context in ("dark", "light")}, pairs)
        self.assertTrue(all(item["ratio"] > 0 and item["threshold"] in (3.0, 4.5) for item in observations))
        self.assertTrue(all(item["passes"] for item in observations))

    def test_every_mark_is_a_safe_square_containing_the_protected_page(self):
        brand = study.load_brand()
        for candidate in study.CANDIDATES.values():
            for context in ("dark", "light"):
                mapping = candidate[context]
                for form in ("full-mark", "reduced-mark"):
                    width, height, mark = study._asset(brand, candidate, context, form)
                    self.assertEqual((1000.0, 1000.0), (width, height))
                    self.assertIn('data-role="square"', mark)
                    self.assertIn('fill="%s"' % mapping["frame"], mark)
                    self.assertIn('stroke="%s"' % mapping["frame_stroke"], mark)
                    self.assertIn('data-role="page"', mark)
                    self.assertNotIn('x="0" y="100" width="800" height="800"', mark)

    def test_generate_writes_only_to_requested_ignored_output(self):
        protected = [study.BRAND_PATH, study.GENERATOR_PATH]
        before = {path: path.read_bytes() for path in protected}
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "study"
            result = study.generate(output)
            self.assertEqual(output.resolve(), result.resolve())
            self.assertEqual({"comparison.html", "comparison.svg", "measurements.json"}, {path.name for path in output.iterdir()})
            self.assertEqual(before, {path: path.read_bytes() for path in protected})

    def test_generated_evidence_contains_every_required_sample(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = study.generate(Path(temporary) / "study")
            measurements = json.loads((output / "measurements.json").read_text(encoding="utf-8"))
            self.assertEqual("owner-approved", measurements["status"])
            self.assertEqual([16, 24, 32, 48], measurements["required_sizes"])
            self.assertEqual(["full-mark", "reduced-mark", "horizontal", "stacked", "desktop", "android-launcher", "store-artwork"], measurements["required_forms"])
            svg = (output / "comparison.svg").read_text(encoding="utf-8")
            for candidate in study.CANDIDATES:
                self.assertIn('data-candidate="%s"' % candidate, svg)
            for context in ("dark", "light"):
                self.assertIn('data-context="%s"' % context, svg)
            for size in measurements["required_sizes"]:
                self.assertIn('data-size="%d"' % size, svg)
                self.assertIn('data-sample="actual-size-full" data-size="%d"' % size, svg)
                self.assertIn('data-sample="actual-size-reduced" data-size="%d"' % size, svg)


if __name__ == "__main__":
    unittest.main()
