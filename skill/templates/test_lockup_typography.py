#!/usr/bin/env python3
"""Horizontal line-layout regressions using temporary source and SVG inputs."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import xml.etree.ElementTree as ET

import glyphkit as G
import brand_contract as BC
import gen_logo
import identity_continuity as IC
from svgelements import SVG

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


class HorizontalTypographyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.brand = {
            "wordmark_text": "Local Media Gallery",
            "logo": {
                "role_colors": {
                    "color": {"accent": "#69D4BB", "wordmark": "#F3F5FA"},
                    "light": {"accent": "#08745F", "wordmark": "#182137"},
                },
                "lockups": {"horizontal": {
                    "mark_height_units": 160, "canvas_height_units": 216,
                    "padding_units": 28, "gap_units": 36, "line_gap_units": 14,
                    "wordmark_lines": [
                        {"text": "Local Media", "role": "wordmark", "font_size_units": 48},
                        {"text": "Gallery", "role": "accent", "font_size_units": 84},
                    ],
                }},
            },
        }
        self.source = self.folder / "brand.json"
        self.source.write_bytes(json.dumps(self.brand).encode("utf-8"))

    def render(self, brand=None, colourway="color"):
        from lockup_typography import horizontal_lockup
        brand = brand or self.brand
        mark = '<path d="%s" fill="#69D4BB"/>' % G.rect(0, 0, 100, 100)
        return horizontal_lockup(
            brand, str(ROOT / "assets/fonts/ttf/SpaceGrotesk-Bold.ttf"),
            colourway, brand["logo"]["role_colors"]["color"], mark, (0, 0, 100, 100),
            gen_logo.wordmark_outline, gen_logo.path_bbox,
        )

    def bounds(self, body, width=1000, height=1000):
        target = self.folder / "layout.svg"
        target.write_bytes(('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g">%s</svg>'
                            % (width, height, body)).encode("utf-8"))
        return SVG.parse(str(target)).bbox()

    def test_absent_lines_keep_default_contract(self):
        brand = copy.deepcopy(self.brand)
        del brand["logo"]["lockups"]["horizontal"]["wordmark_lines"]
        self.assertIsNone(BC.horizontal_wordmark_lines(brand))

    def test_bad_config_rejects_missing_text_roles_sizes_and_conflicting_sources(self):
        malformed = [[], None, [{"text": "Gallery", "role": "accent", "font_size_units": 84}],
                     [{"text": "Local Media Gallery", "role": "absent", "font_size_units": 48}]]
        for value in malformed:
            brand = copy.deepcopy(self.brand)
            brand["logo"]["lockups"]["horizontal"]["wordmark_lines"] = value
            with self.subTest(value=value), self.assertRaises(BC.ContractError):
                BC.horizontal_wordmark_lines(brand)
        for key, value in (("text", "LocalMedia"), ("role", [])):
            brand = copy.deepcopy(self.brand)
            brand["logo"]["lockups"]["horizontal"]["wordmark_lines"][0][key] = value
            with self.subTest(field=key), self.assertRaises(BC.ContractError):
                BC.horizontal_wordmark_lines(brand)
        for value in (0, -1, True, float("nan"), float("inf")):
            brand = copy.deepcopy(self.brand)
            brand["logo"]["lockups"]["horizontal"]["wordmark_lines"][0]["font_size_units"] = value
            with self.subTest(size=value), self.assertRaises(BC.ContractError):
                BC.horizontal_wordmark_lines(brand)
        brand = copy.deepcopy(self.brand)
        brand["logo"]["paths"] = {"wordmark": [{"d": G.rect(0, 0, 1, 1)}]}
        with self.assertRaisesRegex(BC.ContractError, "supplied"):
            BC.horizontal_wordmark_lines(brand)

    def test_measured_ink_alignment_centres_smaller_text_beside_larger_icon(self):
        body, width, height = self.render()
        root = ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg">%s</svg>' % body)
        rows = [n for n in root.iter() if "data-wordmark-line" in n.attrib]
        self.assertEqual(2, len(rows))
        boxes = [self.bounds(ET.tostring(n, encoding="unicode")) for n in rows]
        self.assertAlmostEqual(boxes[0][0], boxes[1][0], places=5)
        self.assertAlmostEqual(224, boxes[0][0], places=5)
        self.assertAlmostEqual(14, boxes[1][1] - boxes[0][3], places=4)
        self.assertAlmostEqual(height / 2, (boxes[0][1] + boxes[1][3]) / 2, places=3)
        self.assertLess(boxes[1][3] - boxes[0][1], 160)
        self.assertGreater(boxes[1][3] - boxes[1][1], boxes[0][3] - boxes[0][1])
        whole = self.bounds(body, width, height)
        self.assertAlmostEqual(28, whole[0], places=3)
        self.assertAlmostEqual(28, whole[1], places=3)
        self.assertAlmostEqual(width - 28, whole[2], places=3)
        self.assertAlmostEqual(188, whole[3], places=3)
        self.assertNotIn("<text", body)

    def test_oversized_mark_or_text_fails_instead_of_clipping(self):
        for field, value in (("canvas_height_units", 80), ("line_gap_units", 500)):
            brand = copy.deepcopy(self.brand)
            brand["logo"]["lockups"]["horizontal"][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "canvas"):
                self.render(brand)

    def test_single_ink_rows_use_the_declared_single_ink(self):
        for mode, ink in (("black", "#000000"), ("white", "#FFFFFF")):
            body, _, _ = self.render(colourway=mode)
            root = ET.fromstring('<svg>%s</svg>' % body)
            rows = [n for n in root.iter() if "data-wordmark-line" in n.attrib]
            self.assertTrue(all(path.attrib["fill"] == ink for row in rows for path in row.iter("path")))

    def test_only_opt_in_renderer_binding_includes_line_helper(self):
        source = (HERE / "gen_logo.py").read_bytes()
        self.assertEqual(IC.LEGACY_GEN_LOGO_SHA256, IC.proof_gen_logo_digest(source, {}))
        before = IC.proof_gen_logo_digest(source, self.brand)
        read_bytes = Path.read_bytes
        def modified(path):
            payload = read_bytes(path)
            return payload + b"\n# drift" if path.name == "lockup_typography.py" else payload
        with mock.patch.object(Path, "read_bytes", modified):
            self.assertNotEqual(before, IC.proof_gen_logo_digest(source, self.brand))
            self.assertEqual(IC.LEGACY_GEN_LOGO_SHA256, IC.proof_gen_logo_digest(source, {}))
        def changed_contract(path):
            payload = read_bytes(path)
            return payload.replace(b'number(row["font_size_units"], "font_size_units", strict=True)', b'0.9 * number(row["font_size_units"], "font_size_units", strict=True)', 1) if path.name == "brand_contract.py" else payload
        with mock.patch.object(Path, "read_bytes", changed_contract):
            self.assertNotEqual(before, IC.proof_gen_logo_digest(source, self.brand))
            self.assertEqual(IC.LEGACY_GEN_LOGO_SHA256, IC.proof_gen_logo_digest(source, {}))


if __name__ == "__main__":
    unittest.main()
