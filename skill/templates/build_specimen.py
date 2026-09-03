#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_specimen.py: the outlined type specimen, generated from brand.json.

DEVIATION from the kit this script was copied out of. That version carried one
product's mark path, palette, slug and sample sentences as literals, so a
second kit generated from it shipped the first kit's specimen. Everything is
read from brand.json now and the file is named for the brand.

Glyphs are outlined from the bundled TTFs, so the specimen never depends on a
font being installed. That defect is item four on the fragcap 1.1.0 list.
"""
import json
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

def outlined_text(text, font_path, size, x, baseline, fill):
    font = TTFont(font_path)
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    cursor, paths = x, []
    for char in text:
        name = cmap.get(ord(char), ".notdef")
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, cursor, baseline)))
        d = pen.getCommands()
        if d:
            paths.append(d)
        cursor += font["hmtx"].metrics[name][0] * scale
    font.close()
    return '<path fill="%s" d="%s"/>' % (fill, " ".join(paths))


def clip(text, n):
    """Truncate on a word boundary. The source kit cut mid-word."""
    if len(text) <= n:
        return text
    return text[:n].rsplit(" ", 1)[0].rstrip(",;:") + "."


def mark(brand, x, y, height):
    """The reduced mark, scaled into the specimen header."""
    lg = brand.get("logo") or {}
    paths = (lg.get("paths") or {}).get("full") or (lg.get("paths") or {}).get("reduced") or []
    if not paths:
        return ""
    grid = float(lg.get("grid", 1000))
    roles = (lg.get("role_colors") or {}).get("color") or {}
    acc = brand["accent"]["bright"]
    s = height / grid
    elements = []
    for item in paths:
        colour = roles.get(item.get("role", "accent"), acc)
        stroked = item.get("fill") == "none" or item.get("stroke_width") is not None
        paint = (' fill="none" stroke="%s"' % colour) if stroked else (' fill="%s"' % colour)
        if item.get("stroke_width") is not None:
            paint += ' stroke-width="%g"' % float(item["stroke_width"])
        if item.get("stroke_linecap"):
            paint += ' stroke-linecap="%s"' % item["stroke_linecap"]
        if item.get("stroke_linejoin"):
            paint += ' stroke-linejoin="%s"' % item["stroke_linejoin"]
        if item.get("element", "path") == "rect":
            shape = '<rect x="%g" y="%g" width="%g" height="%g"' % (
                float(item["x"]), float(item["y"]),
                float(item["width"]), float(item["height"]))
            if item.get("rx") is not None:
                shape += ' rx="%g"' % float(item["rx"])
            elements.append(shape + paint + '/>')
        else:
            elements.append('<path d="%s"%s/>' % (item["d"], paint))
    inner = "".join(elements)
    return '<g transform="translate(%g,%g) scale(%g)">%s</g>' % (x, y, s, inner)


def main():
    spec = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd() / "brand.json"
    kit = spec.parent
    B = json.load(open(spec, encoding="utf-8"))
    out = kit / "specimens"
    out.mkdir(parents=True, exist_ok=True)

    ttf = kit / "fonts" / "ttf"
    display, body, mono = (ttf / "SpaceGrotesk-Bold.ttf",
                           ttf / "Geist-Regular.ttf",
                           ttf / "GeistMono-Regular.ttf")

    surf = B.get("surfaces", {})
    base = surf.get("base", "#000000")
    acc = B["accent"]["bright"]
    dim = B["accent"].get("dim", "#9A9A9A")
    rule = "#262626"
    title = B["title"]
    guide = B.get("guide") or {}
    idea = guide.get("idea") or B.get("brand_idea", title)
    descriptor = guide.get("descriptor") or B.get("descriptor", "")
    fams = B["typography"]["families"]

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000">',
        '<rect width="1600" height="1000" fill="%s"/>' % base,
        mark(B, 66, 66, 170),
        outlined_text("%s TYPE SYSTEM" % title.upper(), mono, 20, 260, 110, dim),
        outlined_text(title, display, 154, 252, 365, "#FFFFFF"),
        outlined_text(clip(guide.get("specimen_line") or descriptor, 86), body, 34, 258, 462, dim),
        '<path fill="%s" d="M80 540H1520V542H80Z"/>' % rule,
        outlined_text("DISPLAY / %s BOLD" % fams["display"]["name"].upper(), mono, 18, 82, 600, acc),
        outlined_text(idea, display, 60, 82, 682, "#FFFFFF"),
        outlined_text("BODY / %s REGULAR" % fams["body"]["name"].upper(), mono, 18, 82, 750, acc),
        outlined_text(clip(guide.get("specimen_body") or B.get("role") or descriptor, 76), body, 30, 82, 810, "#FFFFFF"),
        outlined_text("MONO / %s REGULAR" % fams["mono"]["name"].upper(), mono, 18, 82, 875, acc),
        outlined_text("0O 1lI 8B 5S 2Z   sha256:9f3c   span 412-488   verdict.provisional",
                      mono, 28, 82, 930, dim),
        '</svg>',
    ]
    dest = out / ("%s-type-specimen.svg" % B["slug"])
    dest.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print("wrote %s" % dest)


if __name__ == "__main__":
    main()
