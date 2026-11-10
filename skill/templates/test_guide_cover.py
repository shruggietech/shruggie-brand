"""Rendered S075 cover hierarchy, exact-copy and bounded-pagination regressions."""
import copy
from contextlib import redirect_stdout
from io import BytesIO, StringIO
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
from playwright.sync_api import sync_playwright

import gen_guide_pdf
import gen_nextjs
from brand_contract import font_faces
from messaging import approved_messages
from verify import message_projection_problems


ROOT = Path(__file__).resolve().parents[2]


class GuideCoverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.kit = Path(cls.temporary.name)
        cls.brand = json.loads((ROOT / "brands/localmedia-gallery/brand.json").read_text(encoding="utf-8"))
        spec = cls.kit / "brand.json"
        spec.write_text(json.dumps(cls.brand), encoding="utf-8")
        for face in font_faces(cls.brand):
            target = cls.kit / face["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / "assets" / face["path"], target)
        with patch("sys.argv", ["gen_nextjs.py", str(spec), str(cls.kit)]), redirect_stdout(StringIO()):
            gen_nextjs.main()
        logos = cls.kit / "logos/png"
        logos.mkdir(parents=True)
        for color in ("color", "light"):
            Image.new("RGBA", (640, 110), (120, 120, 120, 255)).save(
                logos / (cls.brand["slug"] + "-horizontal-" + color + "-1024.png"))
        cls.playwright = sync_playwright().start()
        try:
            cls.browser = cls.playwright.chromium.launch()
        except Exception as error:
            cls.playwright.stop()
            cls.temporary.cleanup()
            raise unittest.SkipTest("Chromium unavailable: %s" % error)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.temporary.cleanup()

    def render(self, messages, light=False):
        brand = copy.deepcopy(self.brand)
        brand["guidance"]["surface_mode"] = "light" if light else "dark"
        brand["messaging"] = {role: {"status": "absent"}
                              for role in ("slogan", "short_description", "long_description")}
        for role, text in messages.items():
            brand["messaging"][role] = {
                "status": "approved", "text": text, "uses": ["visual-guide"],
                "source": "isolated test", "approved_by": "test", "approved_on": "2026-11-09"}
        html = gen_guide_pdf.build(brand, self.kit)
        if messages:
            self.assertTrue("data-message-value" in html, "Cover must identify exact message-value content")
        source = self.kit / "cover.print.html"
        source.write_text(html, encoding="utf-8")
        page = self.browser.new_page()
        self.addCleanup(page.close)
        page.goto(source.as_uri())
        page.wait_for_function("window.__coverReady === true", timeout=10000)
        errors = page.evaluate("window.__coverErrors")
        self.assertEqual([], errors)
        expected = approved_messages(brand, "visual-guide")
        actual = page.evaluate("""() => {
            const result = {};
            for (const el of document.querySelectorAll('.cover [data-message-role]')) {
                const role = el.dataset.messageRole.replaceAll('-', '_');
                result[role] = (result[role] || '') + el.querySelector('[data-message-value]').textContent;
            }
            return result;
        }""")
        self.assertEqual(expected, actual)
        self.assertEqual(0, page.locator('.cover .tag').count())
        return page

    def test_typography_is_on_actual_copy_in_both_surface_modes(self):
        for light in (False, True):
            with self.subTest(light=light):
                page = self.render({"slogan": "Actual approved slogan.", "short_description": "Readable supporting copy."}, light)
                styles = page.locator('.cover [data-message-value]').evaluate_all(
                    "els => els.map(el => ({size:parseFloat(getComputedStyle(el).fontSize), line:parseFloat(getComputedStyle(el).lineHeight)}))")
                self.assertAlmostEqual(23 * 96 / 72, styles[0]["size"], places=2)
                self.assertAlmostEqual(13.5 * 96 / 72, styles[1]["size"], places=2)
                self.assertAlmostEqual(27, styles[1]["line"], places=2)
                self.assertEqual(1, page.locator('.cover').count())

    def test_sparse_states_and_wrapping_slogan_do_not_leave_orphans(self):
        for messages in ({}, {"slogan": "Only slogan."}, {"short_description": "Only description."},
                         {"slogan": "A wrapping slogan with enough approved words to span more than one display line."}):
            with self.subTest(messages=messages):
                page = self.render(messages)
                self.assertEqual(bool(messages), bool(page.locator('.cover .message').count()))

    def test_rich_copy_continues_without_shrinking_or_losing_exact_words(self):
        messages = {
            "slogan": "Readable rich-message cover.",
            "short_description": "Supporting description.",
            "long_description": ("Exact long-form copy retains its punctuation & spacing. " * 130).rstrip(),
            "introductory_statement": "An independent introduction remains in its own role.",
        }
        page = self.render(messages)
        self.assertGreater(page.locator('.cover').count(), 1)
        self.assertGreater(page.locator('.cover-continuation').count(), 0)
        sizes = page.locator('.cover [data-message-role="long-description"] [data-message-value]').evaluate_all(
            "els => els.map(el => parseFloat(getComputedStyle(el).fontSize))")
        self.assertTrue(all(abs(size - 18) < 0.01 for size in sizes))
        self.assertEqual([], page.evaluate("window.__coverErrors"))
        (self.kit / "build").mkdir(exist_ok=True)
        shutil.copy2(self.kit / "cover.print.html", self.kit / "build/brand-guide.print.html")
        (self.kit / "guidelines").mkdir(exist_ok=True)
        from html import escape
        labels = {"slogan": "Slogan", "short_description": "Short description",
                  "long_description": "Long description", "introductory_statement": "Introduction"}
        reference = "".join('<p data-message-role="%s"><strong>%s:</strong> %s</p>' %
                            (role.replace("_", "-"), labels[role], escape(value))
                            for role, value in messages.items())
        (self.kit / "guidelines/index.html").write_text(reference, encoding="utf-8")
        (self.kit / "guidelines/portal.json").write_text(
            json.dumps({"brand": {"messaging": messages}}), encoding="utf-8")
        page.pdf(path=str(self.kit / "brand-guide.pdf"), format="A4", print_background=True,
                 margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        brand = {"messaging": {role: {"status": "approved", "text": text, "uses": ["visual-guide"],
                                     "source": "test", "approved_by": "test", "approved_on": "2026-11-09"}
                                for role, text in messages.items()}}
        self.assertEqual([], message_projection_problems(self.kit, brand))


if __name__ == "__main__":
    unittest.main()
