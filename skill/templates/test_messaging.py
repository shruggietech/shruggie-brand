#!/usr/bin/env python3
"""Focused exact-copy and approval-state contract regressions for S067."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from messaging import MessageError, approved_messages, validate_messaging
from brand_contract import ContractError, validate_brand
from authoring_brief import TOPICS, BriefError, validate_brief
from verify import Report, c_messaging, message_projection_problems
from schema_validation import validate_json_schema
import gen_nextjs
from gen_wordpress import patterns


ROOT = Path(__file__).resolve().parents[2]


def message(text, *uses):
    return {
        "status": "approved", "text": text, "uses": list(uses),
        "source": "Owner decision", "approved_by": "owner", "approved_on": "2026-09-29",
    }


def sparse():
    return {"messaging": {
        "slogan": {"status": "unresolved"},
        "short_description": {"status": "unresolved"},
        "long_description": {"status": "unresolved"},
    }}


class MessagingContractTests(unittest.TestCase):
    def test_wordpress_hero_respects_canonical_description_and_uses(self):
        brand = sparse()
        brand.update(slug="alpha", title="Alpha", descriptor="Rejected legacy sentence.",
                     functional_descriptor="Unapproved fallback.")
        for state in ("absent", "unresolved", "wrong-use", "approved"):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as temporary:
                theme = Path(temporary)
                (theme / "patterns").mkdir()
                record = ({"status": state} if state in ("absent", "unresolved") else
                          message('Exact "owner" words & meaning.',
                                  "site-metadata" if state == "approved" else "visual-guide"))
                brand["messaging"]["short_description"] = record
                patterns(theme, brand, "alpha-mark.png")
                hero = (theme / "patterns" / "hero.php").read_text(encoding="utf-8")
                self.assertNotIn("Rejected legacy sentence.", hero)
                self.assertNotIn("Unapproved fallback.", hero)
                self.assertNotIn("Explore our work.", hero)
                if state == "approved":
                    self.assertIn("Exact &quot;owner&quot; words &amp; meaning.", hero)
                else:
                    self.assertNotIn("<!-- wp:paragraph", hero)

    def test_nextjs_og_alt_uses_exact_canonical_copy_or_title_only(self):
        import re
        source = ROOT / "brands" / "covarity" / "brand.json"
        brand = json.loads(source.read_text(encoding="utf-8"))
        brand["title"] = 'Alpha "quoted" & clear'
        brand["descriptor"] = "Rejected legacy sentence."
        brand["functional_descriptor"] = "Unapproved fallback."
        for state in ("absent", "unresolved", "wrong-use", "approved"):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                record = ({"status": state} if state in ("absent", "unresolved") else
                          message('Exact "owner" words & meaning.',
                                  "site-metadata" if state == "approved" else "visual-guide"))
                brand["messaging"]["short_description"] = record
                spec = root / "brand.json"
                spec.write_text(json.dumps(brand), encoding="utf-8")
                with patch("sys.argv", ["gen_nextjs.py", str(spec), str(root)]), patch("builtins.print"):
                    gen_nextjs.main()
                output = (root / "nextjs" / "opengraph-image.tsx").read_text(encoding="utf-8")
                self.assertNotIn("Rejected legacy sentence.", output)
                self.assertNotIn("Unapproved fallback.", output)
                match = re.search(r'alt=\{("(?:[^"\\]|\\.)*")\}', output)
                self.assertIsNotNone(match, "alt must be a safely serialized TSX string expression")
                expected = brand["title"]
                if state == "approved":
                    expected += ', Exact "owner" words & meaning.'
                self.assertEqual(expected, json.loads(match.group(1)))

    def test_sparse_and_absent_never_cross_fill(self):
        brand = sparse()
        brand["descriptor"] = "Legacy description."
        brand["brand_idea"] = "Legacy idea."
        self.assertEqual({}, approved_messages(brand, "visual-guide"))
        brand["messaging"]["short_description"] = {"status": "absent"}
        self.assertEqual({}, approved_messages(brand, "visual-guide"))

    def test_approved_exact_text_and_uses(self):
        brand = sparse()
        brand["messaging"]["slogan"] = message("We’ll figure it out.", "visual-guide", "site-metadata")
        self.assertEqual({"slogan": "We’ll figure it out."}, approved_messages(brand, "visual-guide"))
        self.assertEqual({}, approved_messages(brand, "social-image"))

    def test_conflicting_social_slogan_rejected(self):
        brand = sparse()
        brand["messaging"]["slogan"] = message("Wrong.", "social-image")
        brand["social_copy"] = {"slogan": "Right."}
        with self.assertRaisesRegex(MessageError, "social"):
            validate_messaging(brand)

    def test_unresolved_or_absent_cannot_publish_text(self):
        brand = sparse()
        for state in ("unresolved", "absent"):
            brand["messaging"]["slogan"] = {"status": state, "text": "Unapproved."}
            with self.subTest(state=state), self.assertRaises(MessageError):
                validate_messaging(brand)

    def test_approved_roles_are_independent(self):
        brand = sparse()
        brand["messaging"]["short_description"] = message("Short.", "visual-guide")
        brand["messaging"]["long_description"] = message("Long.", "consumer-data")
        self.assertEqual({"short_description": "Short."}, approved_messages(brand, "visual-guide"))
        self.assertEqual({"long_description": "Long."}, approved_messages(brand, "consumer-data"))

    def test_current_brands_classify_core_roles(self):
        sources = sorted(ROOT.glob("brands/*/brand.json"))
        self.assertEqual(13, len(sources))
        schema = json.loads((ROOT / "skill/references/canon.schema.json").read_text(encoding="utf-8"))
        for source in sources:
            with self.subTest(source=source.parent.name):
                brand = json.loads(source.read_text(encoding="utf-8"))
                validate_messaging(brand)
                validate_json_schema(brand, schema)

    def test_canon_two_preflight_rejects_missing_messaging(self):
        source = ROOT / "brands" / "shruggietech" / "brand.json"
        brand = json.loads(source.read_text(encoding="utf-8"))
        del brand["messaging"]
        with self.assertRaisesRegex(ContractError, "requires messaging"):
            validate_brand(brand, source.parent)

    def test_named_regressions_do_not_promote_legacy_idea(self):
        for slug in ("fragcap", "go-schedule", "glitchpad", "shruggietech"):
            source = ROOT / "brands" / slug / "brand.json"
            brand = json.loads(source.read_text(encoding="utf-8"))
            if slug != "shruggietech":
                # Later owner approvals must not remove unresolved-state coverage.
                brand["messaging"]["slogan"] = {"status": "unresolved"}
            visual = approved_messages(brand, "visual-guide")
            if slug == "shruggietech":
                self.assertEqual("We’ll figure it out.", visual["slogan"])
                self.assertNotEqual(brand["brand_idea"], visual["slogan"])
            else:
                self.assertNotIn("slogan", visual)
                self.assertNotIn(brand.get("brand_idea"), visual.values())

    def test_current_authoring_brief_requires_independent_roles(self):
        brief = {
            "schema_version": 2,
            "topics": {name: {key: [] for key in ("facts", "constraints", "proposals", "unresolved")}
                       for name in TOPICS},
            "social_copy": {"status": "unresolved"},
            "messaging": sparse()["messaging"],
        }
        self.assertEqual(brief, validate_brief(brief))
        bad = copy.deepcopy(brief)
        del bad["messaging"]["long_description"]
        with self.assertRaises(BriefError):
            validate_brief(bad)

    def test_rendered_projection_rejects_wrong_role_and_text(self):
        brand = sparse()
        brand["messaging"]["slogan"] = message("We’ll figure it out.", "visual-guide")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "guidelines").mkdir()
            (root / "build").mkdir()
            (root / "guidelines" / "portal.json").write_text(
                json.dumps({"brand": {"messaging": {"slogan": "We’ll figure it out."}}}),
                encoding="utf-8")
            correct = '<p data-message-role="slogan"><strong>Slogan:</strong> We’ll figure it out.</p>'
            (root / "guidelines" / "index.html").write_text(correct, encoding="utf-8")
            (root / "build" / "brand-guide.print.html").write_text(correct, encoding="utf-8")
            self.assertEqual([], message_projection_problems(root, brand))
            (root / "brand.json").write_text(json.dumps(brand), encoding="utf-8")
            (root / "brand-guide.pdf").write_bytes(b"%PDF-test-fixture")
            with patch("verify.importlib.util.find_spec", return_value=None):
                report = Report()
                c_messaging(root, report)
            self.assertEqual([], report.problems)
            self.assertTrue(any("PyMuPDF is unavailable" in skip for skip in report.skips))
            (root / "brand-guide.pdf").unlink()
            (root / "guidelines" / "index.html").write_text(correct.replace("We’ll", "We will"),
                                                              encoding="utf-8")
            self.assertTrue(any("exact approved" in item for item in message_projection_problems(root, brand)))


if __name__ == "__main__":
    unittest.main()
