"""Check the built portable and PDF Brand essentials openings for every brand."""
import json
import re
import sys
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skill" / "templates"))
from brand_essentials import essentials_projection  # noqa: E402


def main():
    sources = sorted((ROOT / "brands").glob("*/brand.json"))
    assert len(sources) == 11, "production brand inventory changed"
    for source in sources:
        brand = json.loads(source.read_text(encoding="utf-8"))
        slug = brand["slug"]
        kit = ROOT / "dist" / slug
        portal = json.loads((kit / "guidelines" / "portal.json").read_text(encoding="utf-8"))
        expected = essentials_projection(brand)
        assert portal["essentials"] == expected, "%s portal essentials drift from source" % slug
        page = (kit / "guidelines" / "index.html").read_text(encoding="utf-8")
        assert 'id="brand-essentials"' in page, "%s portable guide lacks Brand essentials" % slug
        for section in expected["sections"]:
            anchor = section["id"]
            assert 'id="%s"' % anchor in page and 'href="#%s"' % anchor in page, "%s has an unlinked essentials heading %s" % (slug, anchor)
            assert '<h3>%s</h3>' % section["title"] in page, "%s portable heading %s differs" % (slug, anchor)
        for optional in ("approved-words", "brand-strategy"):
            assert ('id="%s"' % optional in page) == (optional in {part["id"] for part in expected["sections"]}), "%s optional section %s differs" % (slug, optional)
        with fitz.open(kit / "brand-guide.pdf") as pdf:
            assert len(pdf) >= 2, "%s guide has no essentials sheet" % slug
            opening = pdf[1].get_text()
            assert "BRAND ESSENTIALS" in opening.upper() and brand["title"] in opening, "%s PDF opening differs" % slug
            assert not re.search(r"\b(?:FOUNDATIONS|PROMISES|BOUNDARIES)\b", opening, re.I), "%s PDF retains legacy opening" % slug
            full_text = re.sub(r"\s+", " ", " ".join(page.get_text() for page in pdf))
            for limit in expected["usage_limits"]:
                assert re.sub(r"\s+", " ", limit) in full_text, "%s PDF omits exact source usage limit: %s" % (slug, limit)
            if expected["visual_boundary"]:
                assert re.sub(r"\s+", " ", expected["visual_boundary"]) in full_text, "%s PDF omits its visual boundary" % slug
    print("Brand essentials delivery: %d portal, portable, and PDF openings checked" % len(sources))


if __name__ == "__main__":
    main()
