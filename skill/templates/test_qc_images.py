"""Regression for overlap between a tall horizontal lockup and its wordmark in QC."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from PIL import Image
import qc_images


class LogoSheetTests(unittest.TestCase):
    def test_tall_pairing_and_wordmark_have_separate_visible_rows(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            (kit / "brand.json").write_text(json.dumps({}), encoding="utf-8")
            svg = kit / "logos" / "svg"
            svg.mkdir(parents=True)
            for name in ("example-horizontal-color.svg", "example-wordmark-color.svg"):
                (svg / name).write_text("fixture", encoding="utf-8")

            def render(source, width):
                wordmark = "wordmark" in source
                return Image.new("RGBA", (width, 70 if wordmark else 220),
                                 (0, 0, 255, 255) if wordmark else (255, 0, 0, 255))

            output = kit / "sheet.png"
            with mock.patch.object(qc_images, "rsvg", side_effect=render):
                qc_images.logo_sheet(str(kit), str(output), "#10151E", "#F7F8FC")
            with Image.open(output) as sheet:
                for half in (0, 1):
                    panel = sheet.crop((0, half * sheet.height // 2, 650, (half + 1) * sheet.height // 2))
                    pairing = panel.getchannel("R").point(lambda v: 255 if v == 255 else 0).getbbox()
                    wordmark = panel.getchannel("B").point(lambda v: 255 if v == 255 else 0).getbbox()
                    self.assertGreaterEqual(wordmark[1] - pairing[3], 24)
                    self.assertLess(wordmark[3], panel.height)

    def test_tall_supplied_lockup_without_wordmark_fits_each_panel(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            (kit / "brand.json").write_text("{}", encoding="utf-8")
            svg = kit / "logos" / "svg"
            svg.mkdir(parents=True)
            (svg / "example-horizontal-color.svg").write_text("fixture", encoding="utf-8")
            output = kit / "sheet.png"
            with mock.patch.object(qc_images, "rsvg", return_value=Image.new("RGBA", (540, 400), "red")):
                qc_images.logo_sheet(str(kit), str(output), "#10151E", "#F7F8FC")
            with Image.open(output) as sheet:
                for half in (0, 1):
                    panel = sheet.crop((0, half * sheet.height // 2, 650, (half + 1) * sheet.height // 2))
                    ink = panel.getchannel("R").point(lambda v: 255 if v == 255 else 0).getbbox()
                    self.assertEqual(400, ink[3] - ink[1])
                    self.assertGreaterEqual(panel.height - ink[3], 48)

    def test_nonsquare_mark_samples_fit_the_declared_square_slot(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            (kit / "brand.json").write_text("{}", encoding="utf-8")
            svg = kit / "logos" / "svg"
            svg.mkdir(parents=True)
            (svg / "example-mark-color.svg").write_text("fixture", encoding="utf-8")
            output = kit / "sheet.png"
            with mock.patch.object(qc_images, "rsvg", side_effect=lambda source, width: Image.new("RGBA", (width, width * 2), (0, 255, 0, 255))):
                qc_images.logo_sheet(str(kit), str(output), "#10151E", "#F7F8FC")
            with Image.open(output) as sheet:
                sample = sheet.crop((700, 40, 840, sheet.height // 2))
                ink = sample.getchannel("G").point(lambda v: 255 if v == 255 else 0).getbbox()
                self.assertLessEqual(ink[2] - ink[0], 128)
                self.assertLessEqual(ink[3] - ink[1], 128)


if __name__ == "__main__":
    unittest.main()
