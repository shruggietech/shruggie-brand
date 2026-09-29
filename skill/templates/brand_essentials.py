"""Literal, source-bound Brand essentials shared by guide generators."""
import html
import re

from brand_contract import affiliation_text, typography_families
from messaging import approved_messages


WORD_ROLES = ("slogan", "short_description", "long_description", "introductory_statement")
STRATEGY_ROLES = ("positioning", "mission", "vision", "values", "brand_promise")
VISUAL_BOUNDARY_BRANDS = frozenset(("i-heart-pr-tours", "local-companion", "scruggs-tire-alignment"))
ROLE_LABELS = {
    "slogan": "Slogan",
    "short_description": "Short description",
    "long_description": "Long description",
    "introductory_statement": "Introduction",
    "positioning": "Positioning",
    "mission": "Mission",
    "vision": "Vision",
    "values": "Values",
    "brand_promise": "Brand promise",
}


def _plain_source(value):
    """Remove the legacy inline span markup without rewriting its text."""
    return html.unescape(re.sub(r"<[^>]+>", "", value or "")).strip()


def essentials_projection(brand):
    guidance = brand.get("guidance") or {}
    messages = approved_messages(brand, "visual-guide")
    families = typography_families(brand)
    logo = brand.get("logo") or {}
    result = {
        "name": brand["title"],
        "relationship": affiliation_text(brand),
        "written_form": _plain_source(guidance.get("written_form")),
        "name_story": [_plain_source(value) for value in guidance.get("name_story") or []],
        "approved_words": {role: messages[role] for role in WORD_ROLES if role in messages},
        "strategy": {role: messages[role] for role in STRATEGY_ROLES if role in messages},
        "mark_guidance": guidance.get("logo") or "",
        "palette_guidance": guidance.get("palette") or "",
        "type_families": {role: families[role]["name"] for role in ("display", "body", "mono")},
        "usage_limits": list(logo.get("prohibitions") or []),
        "visual_boundary": (guidance.get("sharp_edge") or "") if brand["slug"] in VISUAL_BOUNDARY_BRANDS else "",
        "reduced_below_px": logo.get("reduced_below_px"),
        "standalone_mark_variant": logo.get("standalone_mark_variant") or "full",
    }
    result["sections"] = [{"title": title, "id": section_id}
                          for title, section_id in essentials_sections(result)]
    return result


def essentials_sections(essentials):
    sections = [("Name and relationship", "name-and-relationship")]
    if essentials["approved_words"]:
        sections.append(("Approved words", "approved-words"))
    sections.extend([
        ("Visual signatures", "visual-signatures"),
        ("Where each asset belongs", "where-each-asset-belongs"),
        ("Usage limits", "usage-limits"),
    ])
    if essentials["strategy"]:
        sections.append(("Brand strategy", "brand-strategy"))
    return sections
