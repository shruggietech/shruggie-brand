"""Rebuild or check the reviewed eleven-brand S068 sentence disposition."""
import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill" / "templates"))
from brand_essentials import VISUAL_BOUNDARY_BRANDS  # noqa: E402
OUTPUT = Path(__file__).with_name("disposition-inventory.md")
FIELDS = (
    "foundation_title", "foundation", "promises", "in_scope", "out_of_scope",
    "sharp_edge", "written_form", "name_story", "logo", "palette", "personality",
)
LEGACY_SUMMARIES = ("descriptor", "brand_idea", "functional_descriptor")


def sentences(value):
    if not isinstance(value, str):
        return []
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+(?=[A-Z])", value.strip()) if part.strip()]


def disposition(slug, field, value):
    if field in ("logo", "palette", "written_form", "name_story"):
        return "approved identity guidance", "Project in Brand essentials or the detailed identity pages"
    if field == "personality":
        return "voice guidance", "Retain in canonical source and dedicated Voice guidance; omit from the PDF identity opening"
    if field == "sharp_edge" and slug in VISUAL_BOUNDARY_BRANDS:
        return "visual usage boundary", "Project exact source wording in Brand essentials usage limits across all guide formats"
    if field == "sharp_edge":
        return "product or operational boundary", "Retain in source for product documentation review; omit from visual guides"
    if field == "foundation" and slug == "local-companion" and value.startswith("Its product identity"):
        return "identity relationship", "Retain in source; current mark guidance states the workspace/companion distinction"
    if field in ("foundation_title", "foundation", "in_scope", "out_of_scope"):
        return "product or service scope", "Retain in source for product documentation review; omit from visual guides"
    return "unapproved promise or strategy claim", "Retain in source pending an explicit messaging decision; omit from visual guides"


def render():
    rows = []
    sources = sorted((ROOT / "brands").glob("*/brand.json"))
    for source in sources:
        brand = json.loads(source.read_text(encoding="utf-8"))
        slug = brand["slug"]
        identity = [("title", brand["title"], "approved identity name", "Project as the approved name")]
        identity.extend(("affiliation." + key, value, "relationship metadata", "Derive the declared relationship without inventing an endorsement")
                        for key in ("ownership", "parent", "endorsement")
                        for value in [brand.get("affiliation", {}).get(key)] if value)
        identity.extend(("logo.prohibitions[%d]" % index, value, "approved visual usage limit", "Project verbatim in Brand essentials and detailed Logo guidance")
                        for index, value in enumerate(brand.get("logo", {}).get("prohibitions") or []))
        identity.extend((field, sentence, "legacy product or strategy summary", "Retain in source for product or messaging review; omit from visual guides")
                        for field in LEGACY_SUMMARIES for sentence in sentences(brand.get(field)))
        for path, value, category, destination in identity:
            literal = json.dumps(value, ensure_ascii=False).replace("|", "&#124;").replace("`", "&#96;")
            rows.append(f"| {slug} | `{path}` | `{literal}` | {category} | {destination} |")
        guidance = brand.get("guidance") or {}
        for field in FIELDS:
            value = guidance.get(field)
            if not value:
                continue
            if field == "personality":
                items = [(f"guidance.personality[{index}][{column}]", text)
                         for index, row in enumerate(value) for column, text in enumerate(row)]
            elif isinstance(value, list):
                items = [(f"guidance.{field}[{index}]", text)
                         for index, entry in enumerate(value) for text in sentences(entry)]
            else:
                items = [(f"guidance.{field}", text) for text in sentences(value)]
            for path, text in items:
                category, destination = disposition(slug, field, text)
                literal = json.dumps(text, ensure_ascii=False).replace("|", "&#124;").replace("`", "&#96;")
                rows.append(f"| {slug} | `{path}` | `{literal}` | {category} | {destination} |")
        for role, record in (brand.get("messaging") or {}).items():
            if record.get("status") != "approved":
                continue
            text = record["text"]
            uses = ", ".join(record["uses"])
            category = "approved identity words" if "visual-guide" in record["uses"] else "approved for another surface"
            destination = "Project only on the declared surfaces: " + uses
            literal = json.dumps(text, ensure_ascii=False).replace("|", "&#124;").replace("`", "&#96;")
            rows.append(f"| {slug} | `messaging.{role}` | `{literal}` | {category} | {destination} |")
    lead = (
        "# S068 eleven-brand sentence disposition\n\n"
        "Every current first-page legacy field, array item, and sentence is listed below with its exact source text and a reviewed disposition. "
        "The source remains intact for product-documentation or messaging decisions; this slice changes which fields visual guides project. "
        "The current production inventory has eleven brands, superseding the eight-brand issue intake count. "
        "Approval for one surface is not approval for another.\n\n"
        "| Brand | Source path | Exact sentence or item | Classification | Disposition |\n"
        "| --- | --- | --- | --- | --- |\n"
    )
    return lead + "\n".join(rows) + f"\n\nTotal classified items: {len(rows)} across {len(sources)} production brands.\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.write:
        with OUTPUT.open("w", encoding="utf-8", newline="\n") as output:
            output.write(expected)
    elif OUTPUT.read_text(encoding="utf-8") != expected:
        raise SystemExit("S068 disposition inventory differs from source; review and regenerate it")
