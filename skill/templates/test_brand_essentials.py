"""Source-bound S068 Brand essentials projection checks."""
import copy
import json
import pathlib
import tempfile
import unittest

from brand_essentials import essentials_projection, essentials_sections
from gen_guidelines import portable_essentials_html
from verify import c_rhetoric


ROOT = pathlib.Path(__file__).resolve().parents[2]


class BrandEssentialsTests(unittest.TestCase):
    def brand(self, slug="shruggietech"):
        return json.loads((ROOT / "brands" / slug / "brand.json").read_text(encoding="utf-8"))

    def test_only_visual_guide_approved_words_project(self):
        brand = self.brand()
        brand["messaging"]["short_description"] = {
            "status": "approved", "text": "Metadata only", "uses": ["site-metadata"],
            "source": "test", "approved_by": "test", "approved_on": "2026-09-29",
        }
        result = essentials_projection(brand)
        self.assertEqual({"slogan": "We’ll figure it out."}, result["approved_words"])
        self.assertNotIn("Metadata only", str(result))

    def test_strategy_is_separate_and_optional(self):
        brand = self.brand()
        brand["messaging"]["mission"] = {
            "status": "approved", "text": "Exact mission.", "uses": ["visual-guide"],
            "source": "test", "approved_by": "test", "approved_on": "2026-09-29",
        }
        result = essentials_projection(brand)
        self.assertEqual({"mission": "Exact mission."}, result["strategy"])
        self.assertNotIn("mission", result["approved_words"])
        self.assertIn("Brand strategy", [name for name, _ in essentials_sections(result)])
        brand["messaging"].pop("mission")
        self.assertNotIn("Brand strategy", [name for name, _ in essentials_sections(essentials_projection(brand))])

    def test_source_visual_fields_and_sparse_brand(self):
        rich = self.brand("covarity")
        projection = essentials_projection(rich)
        self.assertEqual(rich["title"], projection["name"])
        self.assertEqual(rich["guidance"]["logo"], projection["mark_guidance"])
        self.assertEqual(rich["logo"]["prohibitions"], projection["usage_limits"])
        self.assertIn("Covarity", projection["written_form"])
        self.assertNotIn("<span", projection["written_form"])
        self.assertNotIn(rich["guidance"]["sharp_edge"], str(projection))
        sparse = essentials_projection(self.brand("dancewithme865"))
        self.assertEqual({}, sparse["approved_words"])
        self.assertEqual([], sparse["usage_limits"])
        self.assertNotIn("Approved words", [name for name, _ in essentials_sections(sparse)])

    def test_all_production_brands_have_source_bound_essentials(self):
        sources = sorted((ROOT / "brands").glob("*/brand.json"))
        self.assertEqual(11, len(sources))
        for source in sources:
            with self.subTest(source=source):
                brand = json.loads(source.read_text(encoding="utf-8"))
                result = essentials_projection(brand)
                self.assertEqual(brand["title"], result["name"])
                self.assertEqual(brand["logo"].get("prohibitions", []), result["usage_limits"])
                self.assertNotIn("foundation", result)
                self.assertNotIn("promises", result)
                self.assertNotIn("sharp_edge", result)

    def test_reviewed_visual_boundaries_keep_exact_source_text(self):
        for slug in ("i-heart-pr-tours", "local-companion", "scruggs-tire-alignment"):
            brand = self.brand(slug)
            projection = essentials_projection(brand)
            self.assertEqual(brand["guidance"]["sharp_edge"], projection["visual_boundary"])
            self.assertIn(projection["visual_boundary"], portable_essentials_html(projection))
        self.assertEqual("", essentials_projection(self.brand("covarity"))["visual_boundary"])

    def test_portable_headings_and_roles_match_projection(self):
        for slug in ("shruggietech", "dancewithme865"):
            with self.subTest(slug=slug):
                projection = essentials_projection(self.brand(slug))
                rendered = portable_essentials_html(projection)
                for section in projection["sections"]:
                    self.assertIn('<section id="%s">' % section["id"], rendered)
                    self.assertIn('<h3>%s</h3>' % section["title"], rendered)
                self.assertEqual('id="approved-words"' in rendered, bool(projection["approved_words"]))
                self.assertEqual('id="brand-strategy"' in rendered, bool(projection["strategy"]))
                for role in projection["approved_words"]:
                    self.assertIn('data-message-role="%s"' % role.replace("_", "-"), rendered)

    def test_verifier_keeps_authored_prose_lint_while_allowing_exact_source(self):
        brand = self.brand("shruggietech")

        class Reporter:
            def __init__(self):
                self.problems = []
            def ok(self, _name, _detail):
                pass
            def bad(self, _name, detail):
                self.problems.append(detail)
            def skip(self, _name, _detail):
                pass

        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            (root / "brand.json").write_text(json.dumps(brand), encoding="utf-8")
            guide = root / "guidelines" / "index.html"
            guide.parent.mkdir()
            source_rule = brand["guidance"]["logo"]
            from html import escape
            guide.write_text(escape(source_rule), encoding="utf-8")
            reporter = Reporter()
            c_rhetoric(root, reporter)
            self.assertEqual([], reporter.problems)
            guide.write_text(escape(source_rule) + " Seamless branding.", encoding="utf-8")
            c_rhetoric(root, reporter)
            self.assertTrue(any("corporate filler" in problem for problem in reporter.problems))


if __name__ == "__main__":
    unittest.main()
