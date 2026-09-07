#!/usr/bin/env python3
"""Generate the non-publishing S015 Glitchpad identity-color comparison."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAND_PATH = ROOT / "brands" / "glitchpad" / "brand.json"
GENERATOR_PATH = ROOT / "skill" / "templates" / "gen_logo.py"
FONT_PATH = ROOT / "assets" / "fonts" / "ttf" / "SpaceGrotesk-Bold.ttf"
EXPECTED_PATH_FINGERPRINT = "ec36a47b2b39d00501163fc189b8dfe8d780580496f013771ccc2301548fb843"
EXPECTED_LAYOUT_FINGERPRINT = "8d5ca8d2a54e56831a20735d4f374ffd824e0f2e5f5f79b8c05a8a78f4bfb1ad"
REQUIRED_ROLES = ("surface", "frame", "frame_stroke", "paper", "fold", "wordmark")
REQUIRED_SIZES = [16, 24, 32, 48]
REQUIRED_FORMS = ["full-mark", "reduced-mark", "horizontal", "stacked", "desktop", "android-launcher", "store-artwork"]

CANDIDATES = {
    "context-switch": {
        "name": "Revision 3 · Context Switch",
        "summary": "Owner-proposed pairing: Sulfur Square in dark mode, Charcoal Square in light mode.",
        "dark": {"surface": "#121416", "frame": "#FFD900", "frame_stroke": "#FFD900", "paper": "#0B0C0D", "fold": "#667788", "wordmark": "#F2F5FA"},
        "light": {"surface": "#F8F8F6", "frame": "#0B0C0D", "frame_stroke": "#0B0C0D", "paper": "#FFD900", "fold": "#667788", "wordmark": "#0A0A0A"},
    },
}


def load_brand():
    return json.loads(BRAND_PATH.read_text(encoding="utf-8"))


def _digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode("utf-8")).hexdigest()


def path_fingerprint(brand):
    paths = brand["logo"]["paths"]
    protected = {
        form: [{key: item[key] for key in ("d", "fill_rule") if key in item}
               for item in paths[form]]
        for form in ("full", "reduced")
    }
    return _digest(protected)


def layout_fingerprint(brand):
    logo = brand["logo"]
    keys = ("grid", "canvas_width", "canvas_height", "artwork_width", "artwork_height", "clear_space_units", "g_thickness_units", "g_to_paper_clearance_units", "lockups", "min_px", "reduced_below_px")
    return _digest({key: logo[key] for key in keys})


def validate_candidate(candidate):
    for context in ("dark", "light"):
        mapping = candidate.get(context)
        if not isinstance(mapping, dict) or set(mapping) != set(REQUIRED_ROLES):
            raise ValueError("candidate %s mapping must contain exactly the required roles" % context)
        for role, value in mapping.items():
            if not isinstance(value, str) or not re.fullmatch(r"#[0-9A-F]{6}", value):
                raise ValueError("candidate %s.%s must be an uppercase six-digit hex" % (context, role))
            if value == "#867100":
                raise ValueError("rejected muddy gold must never appear in a candidate")


def _relative_luminance(color):
    channels = [int(color[index:index + 2], 16) / 255.0 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first, second):
    high, low = sorted((_relative_luminance(first), _relative_luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def contrast_observations():
    observations = []
    for key, candidate in CANDIDATES.items():
        for context in ("dark", "light"):
            mapping = candidate[context]
            relationships = (("square-edge-to-surface", "frame_stroke", "surface", 3.0), ("paper-to-square", "paper", "frame", 3.0), ("fold-to-square", "fold", "frame", 3.0), ("wordmark-to-surface", "wordmark", "surface", 4.5))
            for name, foreground, background, threshold in relationships:
                ratio = contrast(mapping[foreground], mapping[background])
                observations.append({"candidate": key, "context": context, "relationship": name, "foreground": mapping[foreground], "background": mapping[background], "ratio": round(ratio, 2), "threshold": threshold, "passes": ratio + 1e-9 >= threshold})
    return observations


def _path_bbox(path_list):
    from svgelements import Path as SvgPath
    boxes = [SvgPath(item["d"]).bbox() for item in path_list]
    return min(box[0] for box in boxes), min(box[1] for box in boxes), max(box[2] for box in boxes), max(box[3] for box in boxes)


def _wordmark_geometry():
    import sys
    template_dir = str(ROOT / "skill" / "templates")
    if template_dir not in sys.path:
        sys.path.insert(0, template_dir)
    from gen_logo import wordmark_outline
    from svgelements import Path as SvgPath
    path, advance = wordmark_outline("Glitchpad", str(FONT_PATH), 200)
    return path, float(advance), tuple(float(value) for value in SvgPath(path).bbox())


def _mark_paths(brand, mapping, reduced=False):
    source = brand["logo"]["paths"]["reduced" if reduced else "full"]
    result = []
    for item in source:
        fill = mapping["paper"] if reduced or item.get("role") == "neutral" else mapping["fold"]
        extra = ""
        if item.get("fill_rule"):
            extra = ' fill-rule="%s" clip-rule="%s"' % (item["fill_rule"], item["fill_rule"])
        result.append('<path data-role="%s" d="%s" fill="%s"%s/>' % ("page" if reduced or item.get("role") == "neutral" else "fold", html.escape(item["d"], quote=True), fill, extra))
    return "".join(result)


def _square_mark_body(brand, mapping, reduced=False):
    page_box = _path_bbox(brand["logo"]["paths"]["full"])
    page_width = page_box[2] - page_box[0]
    page_height = page_box[3] - page_box[1]
    page_scale = 0.72
    page_x = (1000.0 - page_width * page_scale) / 2.0
    page_y = (1000.0 - page_height * page_scale) / 2.0
    frame = '<rect data-role="square" x="62" y="62" width="876" height="876" rx="142" fill="%s" stroke="%s" stroke-width="24"/>' % (mapping["frame"], mapping["frame_stroke"])
    page = '<g transform="translate(%g,%g) scale(%g) translate(%g,%g)">%s</g>' % (page_x, page_y, page_scale, -page_box[0], -page_box[1], _mark_paths(brand, mapping, reduced))
    return frame + page


def _asset(brand, candidate, context, form):
    mapping = candidate[context]
    logo = brand["logo"]
    mark_width = 1000.0
    mark_height = 1000.0
    if form in {"full-mark", "reduced-mark"}:
        return mark_width, mark_height, _square_mark_body(brand, mapping, form == "reduced-mark")
    wordmark, advance, word_box = _wordmark_geometry()
    word_width = word_box[2] - word_box[0]
    word_height = word_box[3] - word_box[1]
    mark_body = _square_mark_body(brand, mapping, False)
    lockups = logo["lockups"]
    if form == "horizontal":
        spec = lockups["horizontal"]
        word_scale = float(spec["wordmark_scale"])
        mark_render_height = float(spec["mark_height_units"])
        mark_scale = mark_render_height / mark_height
        mark_render_width = mark_width * mark_scale
        gap = float(spec["gap_units"])
        height = float(spec["canvas_height_units"])
        pad = 24.0
        mark_y = (height - mark_render_height) / 2.0
        word_x = pad + mark_render_width + gap
        width = mark_render_width + gap + advance * word_scale + pad * 2.0
        body = '<g transform="translate(%g,%g) scale(%g)">%s</g><g transform="translate(%g,%g) scale(%g)"><path d="%s" fill="%s"/></g>' % (pad, mark_y, mark_scale, mark_body, word_x, float(spec["wordmark_baseline_units"]), word_scale, html.escape(wordmark, quote=True), mapping["wordmark"])
        return width, height, body
    if form != "stacked":
        raise ValueError("unsupported form: %s" % form)
    spec = lockups["stacked"]
    word_scale = float(spec["wordmark_scale"])
    cap_height = max(1.0, -word_box[1]) * word_scale
    mark_render_height = cap_height * float(spec["mark_height_c"])
    mark_scale = mark_render_height / mark_height
    mark_render_width = mark_width * mark_scale
    rendered_word_width = word_width * word_scale
    rendered_word_height = word_height * word_scale
    gap = cap_height * float(spec["gap_c"])
    pad = max(20.0, cap_height * 0.35)
    width = max(mark_render_width, rendered_word_width) + pad * 2.0
    word_top = pad + mark_render_height + gap
    height = word_top + rendered_word_height + pad
    mark_x = (width - mark_render_width) / 2.0
    word_x = (width - rendered_word_width) / 2.0 - word_box[0] * word_scale
    body = '<g transform="translate(%g,%g) scale(%g)">%s</g><g transform="translate(%g,%g) scale(%g)"><path d="%s" fill="%s"/></g>' % (mark_x, pad, mark_scale, mark_body, word_x, word_top - word_box[1] * word_scale, word_scale, html.escape(wordmark, quote=True), mapping["wordmark"])
    return width, height, body


def _nested_asset(brand, key, candidate, context, form, x, y, width, height, attrs=""):
    source_width, source_height, body = _asset(brand, candidate, context, form)
    return '<svg x="%g" y="%g" width="%g" height="%g" viewBox="0 0 %g %g" preserveAspectRatio="xMidYMid meet" data-candidate="%s" data-context="%s" data-form="%s" %s>%s</svg>' % (x, y, width, height, source_width, source_height, key, context, form, attrs, body)


def _label(x, y, text, size=18, fill="#A8ADB4", weight=500):
    return '<text x="%g" y="%g" fill="%s" font-family="Arial, sans-serif" font-size="%g" font-weight="%d">%s</text>' % (x, y, fill, size, weight, html.escape(text))


def _context_panel(brand, key, candidate, context, x, y):
    mapping = candidate[context]
    foreground = "#F2F5FA" if context == "dark" else "#0A0A0A"
    muted = "#A8ADB4" if context == "dark" else "#525961"
    parts = ['<g data-candidate="%s" data-context="%s">' % (key, context), '<rect x="%g" y="%g" width="820" height="600" rx="22" fill="%s" stroke="%s"/>' % (x, y, mapping["surface"], "#30343A" if context == "dark" else "#D4D7DA")]
    parts.append(_label(x + 28, y + 38, context.upper() + " CONTEXT", 15, muted, 700))
    parts.append(_nested_asset(brand, key, candidate, context, "horizontal", x + 28, y + 56, 500, 125))
    parts.append(_nested_asset(brand, key, candidate, context, "stacked", x + 595, y + 45, 185, 160))
    parts.append(_label(x + 28, y + 224, "Full", 14, muted, 600))
    parts.append(_nested_asset(brand, key, candidate, context, "full-mark", x + 28, y + 238, 105, 132))
    parts.append(_label(x + 158, y + 224, "Reduced", 14, muted, 600))
    parts.append(_nested_asset(brand, key, candidate, context, "reduced-mark", x + 158, y + 238, 105, 132))
    parts.append(_label(x + 292, y + 224, "Actual-size full / reduced", 14, muted, 600))
    cursor = x + 292
    for size in REQUIRED_SIZES:
        parts.append('<g data-sample="actual-size-full" data-size="%d">%s</g>' % (size, _nested_asset(brand, key, candidate, context, "full-mark", cursor, y + 240, size, size, 'data-size="%d"' % size)))
        parts.append('<g data-sample="actual-size-reduced" data-size="%d">%s%s</g>' % (size, _nested_asset(brand, key, candidate, context, "reduced-mark", cursor, y + 296, size, size, 'data-size="%d"' % size), _label(cursor, y + 370, "%d" % size, 12, muted, 500)))
        cursor += 72
    parts.append(_label(x + 28, y + 410, "Desktop", 14, muted, 600))
    parts.append('<g data-form="desktop"><rect x="%g" y="%g" width="250" height="88" rx="12" fill="%s" stroke="%s"/>' % (x + 28, y + 424, "#181A1D" if context == "dark" else "#FFFFFF", "#33363B" if context == "dark" else "#D7D9DC"))
    parts.append(_nested_asset(brand, key, candidate, context, "reduced-mark", x + 42, y + 438, 60, 60))
    parts.append(_label(x + 116, y + 460, "notes.md", 15, foreground, 600))
    parts.append(_label(x + 116, y + 484, "Local file", 12, muted, 400) + "</g>")
    parts.append(_label(x + 320, y + 410, "Android launcher", 14, muted, 600))
    parts.append('<g data-form="android-launcher">' + _nested_asset(brand, key, candidate, context, "reduced-mark", x + 320, y + 424, 88, 88) + "</g>")
    parts.append(_label(x + 452, y + 410, "Store artwork", 14, muted, 600))
    parts.append('<g data-form="store-artwork">' + _nested_asset(brand, key, candidate, context, "full-mark", x + 452, y + 424, 144, 144) + "</g>")
    roles = "Square %s   Paper %s   Fold %s   Word %s" % (mapping["frame"], mapping["paper"], mapping["fold"], mapping["wordmark"])
    parts.append(_label(x + 28, y + 575, roles, 13, muted, 500))
    parts.append("</g>")
    return "".join(parts)


def _comparison_svg(brand):
    width = 1800
    section_height = 790
    height = 240 + section_height * len(CANDIDATES)
    body = ['<rect width="100%%" height="100%%" fill="#090A0B"/>', _label(60, 66, "GLITCHPAD COLOR SYSTEM STUDY · REVISION 3", 18, "#FFD900", 700), _label(60, 120, "Focused proposal: contextual square and page inversion", 38, "#F2F5FA", 700), _label(60, 158, "Exploratory decision evidence. Rejected muddy gold is prohibited.", 19, "#A8ADB4", 400), _label(60, 202, "Proposed: A dark mode + B light mode", 21, "#FFD900", 700)]
    y = 240
    for key, candidate in CANDIDATES.items():
        body.append('<g data-candidate="%s">' % key)
        body.append(_label(60, y + 38, candidate["name"], 30, "#F2F5FA", 700))
        body.append(_label(60, y + 72, candidate["summary"], 17, "#A8ADB4", 400))
        body.append(_context_panel(brand, key, candidate, "dark", 40, y + 100))
        body.append(_context_panel(brand, key, candidate, "light", 940, y + 100))
        body.append("</g>")
        y += section_height
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>\n' % (width, height, width, height, "".join(body))


def generate(output):
    output = Path(output).resolve()
    brand = load_brand()
    if path_fingerprint(brand) != EXPECTED_PATH_FINGERPRINT:
        raise ValueError("protected Glitchpad path fingerprint changed")
    if layout_fingerprint(brand) != EXPECTED_LAYOUT_FINGERPRINT:
        raise ValueError("protected Glitchpad layout fingerprint changed")
    for candidate in CANDIDATES.values():
        validate_candidate(candidate)
    observations = contrast_observations()
    if not all(item["passes"] for item in observations):
        raise ValueError("candidate matrix contains an unacknowledged contrast failure")
    output.mkdir(parents=True, exist_ok=True)
    svg = _comparison_svg(brand)
    (output / "comparison.svg").write_text(svg, encoding="utf-8", newline="\n")
    document = '<!doctype html><html><head><meta charset="utf-8"><title>S015 Glitchpad color study</title><style>html,body{margin:0;background:#090A0B}svg{display:block;width:1800px;height:auto}</style></head><body>%s</body></html>\n' % svg
    (output / "comparison.html").write_text(document, encoding="utf-8", newline="\n")
    payload = {"status": "owner-approved", "path_fingerprint": path_fingerprint(brand), "layout_fingerprint": layout_fingerprint(brand), "required_sizes": REQUIRED_SIZES, "required_forms": REQUIRED_FORMS, "candidates": CANDIDATES, "observations": observations}
    (output / "measurements.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / ".s015-color-study")
    arguments = parser.parse_args()
    output = generate(arguments.output)
    print("generated exploratory S015 study in %s" % output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
