#!/usr/bin/env python3
"""Generate the deterministic, non-publishing S026 Cueson identity study."""

from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import math
import re
import shutil
import textwrap
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist" / ".s026-cueson-study" / "gate-1"
DISPLAY_FONT = ROOT / "assets" / "fonts" / "ttf" / "SpaceGrotesk-Bold.ttf"
BODY_FONT = ROOT / "assets" / "fonts" / "ttf" / "Geist-Regular.ttf"
MONO_FONT = ROOT / "assets" / "fonts" / "ttf" / "GeistMono-Regular.ttf"
CANVAS = 512
SIZES = (256, 64, 32, 16)
SURFACES = ("dark", "light")
HEX = re.compile(r"^#[0-9A-F]{6}$")

VERBAL_IDENTITY = {
    "name": "Cueson",
    "slogan": "Universal captions and subtitles",
    "description": "A lossless, structured interchange layer for subtitle and caption content.",
    "preferred_description_lines": [
        "A lossless, structured interchange layer",
        "for subtitle and caption content.",
    ],
}

EVIDENCE = {
    "shruggie_brand_revision": "d50317f6acdf4d4492c3b25cdcd7bb3ec7a29ab9",
    "cueson_revision": "d66d6a0cca92fc0a62f0e26df0ec5b9460ef22d6",
    "product_sources": [
        "README.md",
        "docs/architecture.md",
        "docs/schema.md",
        "docs/cli.md",
        "docs/Cueson-Project-Specification-v0.0.0.md",
        "docs/cueson-media-format-guide.html",
        "internal/schema/cueson.schema.json",
    ],
    "explainer_role": "textual-product-context-only",
    "excluded_visual_precedent": ["color", "typography", "layout", "composition", "formatting"],
}

CRITERIA = (
    "timed-cue-structure",
    "universal-interchange",
    "source-remains-authoritative",
    "normalized-content-addressable",
    "text-and-bitmap-inputs",
    "ocr-is-derived",
    "small-size-distinction",
    "avoid-caption-cliches",
)

ORIGINAL_CUE_IRIS_PALETTE = {
    "id": "cue-iris-r1",
    "name": "Cue Iris on Archive Night",
    "status": "recommended",
    "dark": {
        "surface": "#080A14",
        "card": "#101425",
        "secondary": "#181D33",
        "hover": "#222944",
        "text": "#F4F6FF",
        "muted": "#A7AEC7",
        "accent": "#8D98FF",
        "line": "#596181",
    },
    "light": {
        "surface": "#F7F8FC",
        "card": "#FFFFFF",
        "secondary": "#ECEFFC",
        "hover": "#E0E5FA",
        "text": "#14172A",
        "muted": "#5B6078",
        "accent": "#5360D6",
        "line": "#8A8FA8",
    },
    "state": {
        "emphasis": "#FF5300",
        "success": "#2BCC73",
        "failure": "#E05F5F",
    },
    "single_ink": {"dark": "#FFFFFF", "light": "#000000"},
    "parent_relationship": "Cue Iris is the Cueson identity accent. ShruggieTech orange remains a scarce inherited emphasis and warning role.",
    "rationale": "A cool periwinkle identifies the stable interchange layer without borrowing the explainer images' green and orange treatment or a conventional black-and-white CC badge.",
}

PALETTE = json.loads(json.dumps(ORIGINAL_CUE_IRIS_PALETTE))

CUE_MAGENTA_PALETTE = json.loads(json.dumps(ORIGINAL_CUE_IRIS_PALETTE))
CUE_MAGENTA_PALETTE.update({
    "id": "cue-magenta-r1",
    "name": "Cue Magenta on Archive Night",
    "status": "proposed",
    "rationale": "A warm magenta moves Cueson to the opposite side of the ShruggieTech product spectrum while leaving inherited orange and failure red semantically distinct.",
})
CUE_MAGENTA_PALETTE["dark"]["accent"] = "#E97AB2"
CUE_MAGENTA_PALETTE["light"]["accent"] = "#9E366F"
CUE_MAGENTA_PALETTE["parent_relationship"] = "Cue Magenta is the Cueson identity accent. ShruggieTech orange remains a scarce inherited emphasis and warning role."

CUE_TEAL_PALETTE = json.loads(json.dumps(ORIGINAL_CUE_IRIS_PALETTE))
CUE_TEAL_PALETTE.update({
    "id": "cue-teal-r1",
    "name": "Cue Teal on Archive Night",
    "status": "proposed",
    "rationale": "A clear teal gives Cueson a compliant identity slot between the parent green and Fragcap cyan while retaining strong contrast on dark and light surfaces.",
})
CUE_TEAL_PALETTE["dark"]["accent"] = "#62BEB2"
CUE_TEAL_PALETTE["light"]["accent"] = "#005D55"
CUE_TEAL_PALETTE["parent_relationship"] = "Cue Teal is the Cueson identity accent. ShruggieTech orange remains a scarce inherited emphasis and warning role."
PALETTE = CUE_TEAL_PALETTE


def line(role, points, width, closed=False):
    return {"type": "line", "role": role, "points": points, "width": width, "closed": closed}


def rect(role, box, radius, width=0, fill=False):
    return {"type": "rect", "role": role, "box": box, "radius": radius, "width": width, "fill": fill}


def circle(role, center, radius, fill=True, width=0):
    return {"type": "circle", "role": role, "center": center, "radius": radius, "fill": fill, "width": width}


CANDIDATES = {
    "cueframe-r1": {
        "name": "Cueframe",
        "status": "recommended",
        "summary": "A preserved source envelope holds three directly readable cue rails.",
        "rationale": "Opposing timing brackets carry the lossless outer envelope while unequal internal rails read as structured caption content. Open terminals avoid a CC badge silhouette.",
        "risks": ["Brackets can imply code syntax if the inner cue rhythm becomes too quiet.", "Too many rails would close up below 24 pixels."],
        "tradeoffs": ["Best overall coverage of preservation and readable structure.", "Uses a deliberately abstract interchange metaphor rather than literal media imagery."],
        "wordmark_relationship": "The wide square silhouette gives the wordmark a calm left edge and a natural bracket-to-cap-height alignment.",
        "criteria": {
            "timed-cue-structure": "met",
            "universal-interchange": "met",
            "source-remains-authoritative": "met",
            "normalized-content-addressable": "met",
            "text-and-bitmap-inputs": "partial",
            "ocr-is-derived": "partial",
            "small-size-distinction": "met",
            "avoid-caption-cliches": "met",
        },
        "full": (
            line("accent", ((168, 104), (108, 104), (108, 408), (168, 408)), 34),
            line("accent", ((344, 104), (404, 104), (404, 408), (344, 408)), 34),
            line("ink", ((184, 172), (336, 172)), 32),
            line("ink", ((184, 256), (304, 256)), 32),
            line("ink", ((184, 340), (352, 340)), 32),
        ),
        "reduced": (
            line("accent", ((174, 126), (118, 126), (118, 386), (174, 386)), 42),
            line("accent", ((338, 126), (394, 126), (394, 386), (338, 386)), 42),
            line("ink", ((190, 256), (322, 256)), 42),
        ),
    },
    "parallel-source-r1": {
        "name": "Parallel Source",
        "status": "exploring",
        "summary": "Original and normalized caption surfaces remain visibly paired.",
        "rationale": "Two offset plates keep the authoritative source and the common Cue JSON view together. Their overlap is continuity, not replacement.",
        "risks": ["Offset panels are common in copy and layers icons.", "The semantic difference between outline and filled rail needs explanation."],
        "tradeoffs": ["Makes dual representation immediately visible.", "Communicates timing less directly than Cueframe or Timing Spine."],
        "wordmark_relationship": "The diagonal overlap creates motion beside the wordmark but demands extra horizontal clear space.",
        "criteria": {
            "timed-cue-structure": "partial",
            "universal-interchange": "met",
            "source-remains-authoritative": "met",
            "normalized-content-addressable": "met",
            "text-and-bitmap-inputs": "partial",
            "ocr-is-derived": "partial",
            "small-size-distinction": "partial",
            "avoid-caption-cliches": "partial",
        },
        "full": (
            rect("source", (84, 106, 356, 300), 42, width=30),
            line("source", ((132, 164), (290, 164)), 26),
            line("source", ((132, 224), (258, 224)), 26),
            rect("accent", (156, 212, 428, 406), 42, width=34),
            line("ink", ((204, 272), (364, 272)), 28),
            line("ink", ((204, 334), (332, 334)), 28),
        ),
        "reduced": (
            rect("source", (92, 112, 346, 306), 48, width=38),
            rect("accent", (166, 206, 420, 400), 48, width=42),
        ),
    },
    "timing-spine-r1": {
        "name": "Timing Spine",
        "status": "exploring",
        "summary": "Every cue is anchored to one exact temporal datum.",
        "rationale": "A fixed timing spine and three staggered rails express cue start points, duration, and predictable structured access without using a media play symbol.",
        "risks": ["Can resemble a list or project timeline.", "Source preservation is not self-evident."],
        "tradeoffs": ["Strongest timing and structured-data signal.", "Weakest expression of the lossless source envelope."],
        "wordmark_relationship": "The vertical datum creates a compact upright counterweight to the broad lowercase wordmark.",
        "criteria": {
            "timed-cue-structure": "met",
            "universal-interchange": "partial",
            "source-remains-authoritative": "partial",
            "normalized-content-addressable": "met",
            "text-and-bitmap-inputs": "unmet",
            "ocr-is-derived": "unmet",
            "small-size-distinction": "met",
            "avoid-caption-cliches": "met",
        },
        "full": (
            line("accent", ((136, 92), (136, 420)), 34),
            circle("accent", (136, 168), 24),
            circle("accent", (136, 256), 24),
            circle("accent", (136, 344), 24),
            line("ink", ((184, 168), (374, 168)), 32),
            line("ink", ((184, 256), (322, 256)), 32),
            line("ink", ((184, 344), (398, 344)), 32),
        ),
        "reduced": (
            line("accent", ((142, 116), (142, 396)), 42),
            circle("accent", (142, 196), 28),
            circle("accent", (142, 316), 28),
            line("ink", ((198, 196), (370, 196)), 42),
            line("ink", ((198, 316), (326, 316)), 42),
        ),
    },
    "interchange-aperture-r1": {
        "name": "Interchange Aperture",
        "status": "exploring",
        "summary": "Four format gates align around one addressable cue surface.",
        "rationale": "Open corner gates imply many format boundaries without arrows. The central rails are the shared Cue JSON view, visibly separate from the surrounding format apertures.",
        "risks": ["Corner gates can resemble crop, focus, or scanning controls.", "The many-to-one meaning relies on application context."],
        "tradeoffs": ["Most compact expression of format universality.", "Less explicit about source bytes remaining authoritative."],
        "wordmark_relationship": "The open corners make a light, technical mark but require disciplined clear space beside type.",
        "criteria": {
            "timed-cue-structure": "partial",
            "universal-interchange": "met",
            "source-remains-authoritative": "partial",
            "normalized-content-addressable": "met",
            "text-and-bitmap-inputs": "met",
            "ocr-is-derived": "partial",
            "small-size-distinction": "partial",
            "avoid-caption-cliches": "partial",
        },
        "full": (
            line("accent", ((178, 104), (104, 104), (104, 178)), 34),
            line("accent", ((334, 104), (408, 104), (408, 178)), 34),
            line("accent", ((104, 334), (104, 408), (178, 408)), 34),
            line("accent", ((408, 334), (408, 408), (334, 408)), 34),
            line("ink", ((168, 224), (344, 224)), 32),
            line("ink", ((192, 288), (320, 288)), 32),
        ),
        "reduced": (
            line("accent", ((188, 118), (118, 118), (118, 188)), 42),
            line("accent", ((324, 118), (394, 118), (394, 188)), 42),
            line("accent", ((118, 324), (118, 394), (188, 394)), 42),
            line("accent", ((394, 324), (394, 394), (324, 394)), 42),
            line("ink", ((190, 256), (322, 256)), 42),
        ),
    },
}


COLOR_VISION_MATRICES = {
    "protanopia": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "deuteranopia": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "tritanopia": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def canonical_digest(value):
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def geometry_fingerprint(candidate):
    return canonical_digest({"full": candidate["full"], "reduced": candidate["reduced"]})


def _relative_luminance(color):
    channels = [int(color[index:index + 2], 16) / 255.0 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first, second):
    high, low = sorted((_relative_luminance(first), _relative_luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def contrast_observations(palette=None):
    palette = PALETTE if palette is None else palette
    pairs = (
        ("dark-accent", palette["dark"]["accent"], palette["dark"]["surface"], 4.5),
        ("dark-text", palette["dark"]["text"], palette["dark"]["surface"], 4.5),
        ("dark-muted", palette["dark"]["muted"], palette["dark"]["surface"], 4.5),
        ("dark-line", palette["dark"]["line"], palette["dark"]["surface"], 3.0),
        ("light-accent", palette["light"]["accent"], palette["light"]["surface"], 4.5),
        ("light-text", palette["light"]["text"], palette["light"]["surface"], 4.5),
        ("light-muted", palette["light"]["muted"], palette["light"]["surface"], 4.5),
        ("light-line", palette["light"]["line"], palette["light"]["surface"], 3.0),
    )
    return [
        {"relationship": name, "foreground": foreground, "background": background, "ratio": round(contrast(foreground, background), 2), "threshold": threshold, "passes": contrast(foreground, background) + 1e-9 >= threshold}
        for name, foreground, background, threshold in pairs
    ]


def _srgb_to_linear(channel):
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(channel):
    channel = min(1.0, max(0.0, channel))
    return channel * 12.92 if channel <= 0.0031308 else 1.055 * (channel ** (1.0 / 2.4)) - 0.055


def _simulate(color, matrix):
    rgb = [int(color[index:index + 2], 16) / 255.0 for index in (1, 3, 5)]
    linear = [_srgb_to_linear(value) for value in rgb]
    transformed = [sum(row[column] * linear[column] for column in range(3)) for row in matrix]
    return tuple(_linear_to_srgb(value) for value in transformed)


def color_vision_observations(palette=None):
    palette = PALETTE if palette is None else palette
    observations = {}
    comparisons = (("emphasis", palette["state"]["emphasis"]), ("success", palette["state"]["success"]), ("failure", palette["state"]["failure"]))
    for mode, matrix in COLOR_VISION_MATRICES.items():
        rows = []
        for context in SURFACES:
            accent = _simulate(palette[context]["accent"], matrix)
            for role, color in comparisons:
                other = _simulate(color, matrix)
                distance = math.sqrt(sum((first - second) ** 2 for first, second in zip(accent, other)))
                rows.append({"context": context, "identity": palette[context]["accent"], "other_role": role, "other": color, "distance": round(distance, 3), "threshold": 0.18, "passes": distance + 1e-9 >= 0.18})
        observations[mode] = rows
    return observations


def validate_palette(palette):
    required_context = {"surface", "card", "secondary", "hover", "text", "muted", "accent", "line"}
    if set(palette.get("dark", {})) != required_context or set(palette.get("light", {})) != required_context:
        raise ValueError("palette contexts must contain the complete role set")
    values = list(palette["dark"].values()) + list(palette["light"].values()) + list(palette.get("state", {}).values()) + list(palette.get("single_ink", {}).values())
    if not values or not all(isinstance(value, str) and HEX.fullmatch(value) for value in values):
        raise ValueError("palette values must be uppercase six-digit hex colors")
    if not all(item["passes"] for item in contrast_observations(palette)):
        raise ValueError("palette contains an unacknowledged contrast failure")
    if not all(item["passes"] for rows in color_vision_observations(palette).values() for item in rows):
        raise ValueError("palette contains an unacknowledged color-vision collision")


def validate_candidate(key, candidate):
    required = {"name", "status", "summary", "rationale", "risks", "tradeoffs", "wordmark_relationship", "criteria", "full", "reduced"}
    if set(candidate) != required:
        raise ValueError("candidate %s has incomplete metadata" % key)
    if candidate["status"] not in {"exploring", "recommended", "revising", "approved", "rejected"}:
        raise ValueError("candidate %s has invalid status" % key)
    if not all(isinstance(candidate[field], str) and candidate[field].strip() for field in ("name", "summary", "rationale", "wordmark_relationship")):
        raise ValueError("candidate %s has empty descriptive metadata" % key)
    if not candidate["risks"] or not candidate["tradeoffs"]:
        raise ValueError("candidate %s must disclose risks and tradeoffs" % key)
    if set(candidate["criteria"]) != set(CRITERIA) or not set(candidate["criteria"].values()).issubset({"met", "partial", "unmet"}):
        raise ValueError("candidate %s has incomplete criterion mapping" % key)
    for variant in ("full", "reduced"):
        if not candidate[variant]:
            raise ValueError("candidate %s lacks %s geometry" % (key, variant))
        for shape in candidate[variant]:
            if shape.get("type") not in {"line", "rect", "circle"} or shape.get("role") not in {"accent", "ink", "source"}:
                raise ValueError("candidate %s contains unsupported geometry" % key)


def _colors(surface, palette=None):
    palette = PALETTE if palette is None else palette
    if surface == "dark":
        return {"surface": palette["dark"]["surface"], "accent": palette["dark"]["accent"], "ink": palette["dark"]["text"], "source": palette["dark"]["muted"]}
    if surface == "light":
        return {"surface": palette["light"]["surface"], "accent": palette["light"]["accent"], "ink": palette["light"]["text"], "source": palette["light"]["muted"]}
    if surface == "mono-dark":
        return {"surface": palette["dark"]["surface"], "accent": "#FFFFFF", "ink": "#FFFFFF", "source": "#FFFFFF"}
    if surface == "mono-light":
        return {"surface": palette["light"]["surface"], "accent": "#000000", "ink": "#000000", "source": "#000000"}
    raise ValueError("unsupported surface: %s" % surface)


def _shape_svg(shape, colors):
    color = colors[shape["role"]]
    if shape["type"] == "line":
        points = shape["points"]
        path = "M" + " L".join("%g %g" % point for point in points)
        if shape.get("closed"):
            path += " Z"
        return '<path d="%s" fill="none" stroke="%s" stroke-width="%g" stroke-linecap="round" stroke-linejoin="round"/>' % (path, color, shape["width"])
    if shape["type"] == "rect":
        x1, y1, x2, y2 = shape["box"]
        fill = color if shape.get("fill") else "none"
        stroke = "none" if shape.get("fill") else color
        return '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-width="%g"/>' % (x1, y1, x2 - x1, y2 - y1, shape["radius"], fill, stroke, shape.get("width", 0))
    x, y = shape["center"]
    return '<circle cx="%g" cy="%g" r="%g" fill="%s" stroke="%s" stroke-width="%g"/>' % (x, y, shape["radius"], color if shape.get("fill") else "none", "none" if shape.get("fill") else color, shape.get("width", 0))


def concept_svg(candidate, variant, surface, palette=None):
    if variant not in {"full", "reduced"}:
        raise ValueError("unsupported variant: %s" % variant)
    colors = _colors(surface, palette)
    body = "".join(_shape_svg(shape, colors) for shape in candidate[variant])
    return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect width="512" height="512" fill="%s"/>%s</svg>\n' % (colors["surface"], body)


def _font(path, size):
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default()


def _draw_round_line(draw, points, fill, width):
    points = [(round(x), round(y)) for x, y in points]
    draw.line(points + ([points[0]] if len(points) > 2 and points[0] == points[-1] else []), fill=fill, width=round(width), joint="curve")
    radius = width / 2.0
    for x, y in (points[0], points[-1]):
        draw.ellipse((round(x - radius), round(y - radius), round(x + radius), round(y + radius)), fill=fill)


def _draw_geometry(image, candidate, variant, surface, palette=None):
    colors = _colors(surface, palette)
    draw = ImageDraw.Draw(image)
    for shape in candidate[variant]:
        color = colors[shape["role"]]
        if shape["type"] == "line":
            _draw_round_line(draw, shape["points"], color, shape["width"])
        elif shape["type"] == "rect":
            draw.rounded_rectangle(shape["box"], radius=shape["radius"], fill=color if shape.get("fill") else None, outline=None if shape.get("fill") else color, width=shape.get("width", 0))
        else:
            x, y = shape["center"]
            radius = shape["radius"]
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color if shape.get("fill") else None, outline=None if shape.get("fill") else color, width=shape.get("width", 0))


def render_concept(candidate, variant, surface, size, palette=None):
    colors = _colors(surface, palette)
    image = Image.new("RGB", (CANVAS, CANVAS), colors["surface"])
    _draw_geometry(image, candidate, variant, surface, palette)
    if size == CANVAS:
        return image
    return image.resize((size, size), Image.Resampling.LANCZOS)


def _wrapped(draw, xy, text, font, fill, width, spacing=8):
    lines = textwrap.wrap(text, width=width)
    draw.multiline_text(xy, "\n".join(lines), font=font, fill=fill, spacing=spacing)


def _concept_sheet(key, candidate):
    image = Image.new("RGB", (1600, 1050), "#080A14")
    draw = ImageDraw.Draw(image)
    title = _font(DISPLAY_FONT, 58)
    heading = _font(DISPLAY_FONT, 26)
    body = _font(BODY_FONT, 23)
    mono = _font(MONO_FONT, 18)
    accent = PALETTE["dark"]["accent"]
    draw.text((64, 52), candidate["name"], font=title, fill="#F4F6FF")
    draw.text((64, 124), key.upper() + ("  •  RECOMMENDED" if candidate["status"] == "recommended" else "  •  EXPLORING"), font=mono, fill=accent)
    _wrapped(draw, (64, 172), candidate["rationale"], body, "#A7AEC7", 92)
    for column, surface in enumerate(SURFACES):
        x = 64 + column * 420
        sample = render_concept(candidate, "full", surface, 336)
        image.paste(sample, (x, 300))
        draw.text((x, 652), surface.upper() + " FULL", font=mono, fill="#A7AEC7")
    x0 = 930
    draw.text((x0, 300), "ACTUAL SIZE", font=heading, fill="#F4F6FF")
    y = 352
    for surface in SURFACES:
        draw.text((x0, y + 8), surface.upper(), font=mono, fill="#A7AEC7")
        x = x0 + 110
        for size in SIZES:
            proof = render_concept(candidate, "full", surface, size)
            image.paste(proof, (x, y))
            draw.text((x, y + 270), str(size), font=mono, fill="#A7AEC7")
            x += max(78, size + 24)
        y += 310
    draw.text((64, 720), "TRADEOFFS", font=heading, fill="#F4F6FF")
    _wrapped(draw, (64, 765), " • ".join(candidate["tradeoffs"]), body, "#A7AEC7", 70)
    draw.text((64, 890), "RISKS", font=heading, fill="#F4F6FF")
    _wrapped(draw, (64, 935), " • ".join(candidate["risks"]), body, "#A7AEC7", 70)
    return image


def _overview(sheets):
    image = Image.new("RGB", (1800, 2320), "#F7F8FC")
    draw = ImageDraw.Draw(image)
    title = _font(DISPLAY_FONT, 62)
    body = _font(BODY_FONT, 25)
    draw.text((70, 55), "S026 Gate 1: Cueson identity directions", font=title, fill="#14172A")
    draw.text((70, 135), "Four product-grounded concepts. Cueframe is recommended. Styling from the explainer images is excluded.", font=body, fill="#5B6078")
    positions = ((70, 220), (930, 220), (70, 1260), (930, 1260))
    for position, sheet in zip(positions, sheets):
        card = sheet.copy()
        card.thumbnail((800, 980), Image.Resampling.LANCZOS)
        image.paste(card, position)
    return image


def _palette_sheet():
    image = Image.new("RGB", (1800, 1100), "#080A14")
    draw = ImageDraw.Draw(image)
    title = _font(DISPLAY_FONT, 62)
    heading = _font(DISPLAY_FONT, 28)
    body = _font(BODY_FONT, 23)
    mono = _font(MONO_FONT, 18)
    draw.text((70, 55), "Recommended color system: Cue Iris", font=title, fill="#F4F6FF")
    _wrapped(draw, (70, 140), PALETTE["rationale"], body, "#A7AEC7", 110)
    x = 70
    for context in SURFACES:
        draw.text((x, 250), context.upper(), font=heading, fill="#F4F6FF")
        y = 310
        for role, color in PALETTE[context].items():
            draw.rounded_rectangle((x, y, x + 210, y + 78), radius=14, fill=color, outline="#FFFFFF" if context == "dark" else "#14172A", width=2)
            draw.text((x + 230, y + 10), role, font=body, fill="#F4F6FF")
            draw.text((x + 230, y + 43), color, font=mono, fill="#A7AEC7")
            y += 92
        x += 590
    x = 1260
    draw.text((x, 250), "MEASURED PAIRS", font=heading, fill="#F4F6FF")
    y = 310
    for item in contrast_observations():
        draw.text((x, y), "%s  %.2f:1" % (item["relationship"], item["ratio"]), font=mono, fill="#F4F6FF" if item["passes"] else "#E05F5F")
        y += 42
    y += 28
    draw.text((x, y), "COLOR-VISION MINIMA", font=heading, fill="#F4F6FF")
    y += 54
    for mode, rows in color_vision_observations().items():
        minimum = min(item["distance"] for item in rows)
        draw.text((x, y), "%s  %.3f" % (mode, minimum), font=mono, fill="#F4F6FF" if minimum >= 0.18 else "#E05F5F")
        y += 42
    draw.text((70, 1050), PALETTE["parent_relationship"], font=body, fill="#8D98FF")
    return image


def _proposal_payload():
    candidates = {}
    for key, candidate in CANDIDATES.items():
        candidates[key] = {field: candidate[field] for field in ("name", "status", "summary", "rationale", "risks", "tradeoffs", "wordmark_relationship", "criteria")}
        candidates[key]["geometry_sha256"] = geometry_fingerprint(candidate)
    payload = {
        "schema_version": 1,
        "gate": 1,
        "status": "pending-owner-approval",
        "evidence": EVIDENCE,
        "verbal_identity": VERBAL_IDENTITY,
        "criteria": list(CRITERIA),
        "candidates": candidates,
        "recommended_candidate": "cueframe-r1",
        "palette": PALETTE,
        "contrast_observations": contrast_observations(),
        "color_vision_observations": color_vision_observations(),
        "production_identity_created": False,
        "public_eligible": False,
        "approval": None,
    }
    payload["proposal_sha256"] = canonical_digest(payload)
    return payload


def _index_html():
    cards = "".join('<figure><img src="concept-%s.png" alt="%s concept sheet"><figcaption>%s</figcaption></figure>' % (html.escape(key), html.escape(candidate["name"]), html.escape(candidate["summary"])) for key, candidate in CANDIDATES.items())
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>S026 Cueson Gate 1</title><style>body{{margin:0;background:#080A14;color:#F4F6FF;font-family:Arial,sans-serif}}main{{max-width:1500px;margin:auto;padding:48px}}img{{display:block;max-width:100%;height:auto}}figure{{margin:48px 0}}figcaption{{padding:12px 0;color:#A7AEC7}}</style></head><body><main><h1>Cueson Gate 1</h1><p>Proposal evidence only. No production identity exists.</p><img src="overview.png" alt="Overview of four Cueson identity concepts"><img src="palette.png" alt="Cue Iris palette and measurements">{cards}</main></body></html>\n'.format(cards=cards)


def generate(output=DEFAULT_OUTPUT):
    output = Path(output).resolve()
    for key, candidate in CANDIDATES.items():
        validate_candidate(key, candidate)
    validate_palette(PALETTE)
    if len({geometry_fingerprint(candidate) for candidate in CANDIDATES.values()}) != len(CANDIDATES):
        raise ValueError("candidate geometry fingerprints must be unique")
    if sum(candidate["status"] == "recommended" for candidate in CANDIDATES.values()) != 1:
        raise ValueError("exactly one candidate must be recommended")

    vectors = output / "vectors"
    proofs = output / "proofs"
    vectors.mkdir(parents=True, exist_ok=True)
    proofs.mkdir(parents=True, exist_ok=True)

    sheets = []
    for key, candidate in CANDIDATES.items():
        for variant in ("full", "reduced"):
            for surface in ("dark", "light", "mono-dark", "mono-light"):
                (vectors / ("%s-%s-%s.svg" % (key, variant, surface))).write_text(concept_svg(candidate, variant, surface), encoding="utf-8", newline="\n")
        for size in SIZES:
            for surface in SURFACES:
                for variant in ("full", "reduced"):
                    render_concept(candidate, variant, surface, size).save(proofs / ("%s-%s-%s-%d.png" % (key, variant, surface, size)))
                render_concept(candidate, "full", "mono-" + surface, size).save(proofs / ("%s-full-mono-%s-%d.png" % (key, surface, size)))
        sheet = _concept_sheet(key, candidate)
        sheet.save(output / ("concept-%s.png" % key))
        sheets.append(sheet)

    _overview(sheets).save(output / "overview.png")
    _palette_sheet().save(output / "palette.png")
    proposal = _proposal_payload()
    (output / "proposal.json").write_text(json.dumps(proposal, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    (output / "index.html").write_text(_index_html(), encoding="utf-8", newline="\n")

    files = []
    for path in sorted(output.rglob("*")):
        if path.is_file() and path.name != "manifest.json":
            files.append({"path": path.relative_to(output).as_posix(), "bytes": path.stat().st_size, "sha256": file_digest(path)})
    manifest = {
        "schema_version": 1,
        "gate": 1,
        "approval_status": "pending",
        "production_identity_created": False,
        "public_eligible": False,
        "sizes_px": list(SIZES),
        "surfaces": list(SURFACES),
        "candidates": [{"id": key, "status": candidate["status"], "geometry_sha256": geometry_fingerprint(candidate)} for key, candidate in CANDIDATES.items()],
        "recommended_candidate": "cueframe-r1",
        "palette_id": PALETTE["id"],
        "palette_sha256": canonical_digest(PALETTE),
        "proposal_sha256": proposal["proposal_sha256"],
        "files": files,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return output


def generate_color_demo(output, palette):
    """Render the approved Cueframe geometry with one proposed palette."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    validate_palette(palette)
    candidate = CANDIDATES["cueframe-r1"]
    image = Image.new("RGB", (1800, 1200), "#F1F2F8")
    draw = ImageDraw.Draw(image)
    title = _font(DISPLAY_FONT, 68)
    heading = _font(DISPLAY_FONT, 44)
    body = _font(BODY_FONT, 28)
    small = _font(MONO_FONT, 20)
    palette_label = palette["name"].replace(" on Archive Night", "")
    draw.text((70, 52), "Cueframe in %s" % palette_label, font=title, fill="#14172A")
    draw.text((70, 132), "Exact approved glyph geometry · proposed color revision %s" % palette["id"], font=body, fill="#5B6078")

    dark_mark = render_concept(candidate, "full", "dark", 440, palette)
    light_mark = render_concept(candidate, "full", "light", 440, palette)
    image.paste(dark_mark, (70, 210))
    image.paste(light_mark, (550, 210))
    draw.text((70, 665), "DARK MARK  %s" % palette["dark"]["accent"], font=small, fill="#5B6078")
    draw.text((550, 665), "LIGHT MARK  %s" % palette["light"]["accent"], font=small, fill="#5B6078")

    def lockup(surface, position):
        colors = palette[surface]
        card = Image.new("RGB", (740, 210), colors["surface"])
        card_draw = ImageDraw.Draw(card)
        mark = render_concept(candidate, "full", surface, 160, palette)
        card.paste(mark, (32, 25))
        card_draw.text((214, 40), "Cueson", font=_font(DISPLAY_FONT, 68), fill=colors["text"])
        card_draw.text((218, 124), "UNIVERSAL CAPTIONS AND SUBTITLES", font=_font(MONO_FONT, 18), fill=colors["accent"])
        image.paste(card, position)

    lockup("dark", (1010, 210))
    lockup("light", (1010, 450))

    draw.text((70, 760), "REDUCED ICON BEHAVIOR", font=heading, fill="#14172A")
    x = 70
    for size in (128, 64, 32, 16):
        card = Image.new("RGB", (190, 190), palette["dark"]["surface"])
        proof = render_concept(candidate, "reduced", "dark", size, palette)
        card.paste(proof, ((190 - size) // 2, (190 - size) // 2))
        image.paste(card, (x, 840))
        draw.text((x, 1045), "%d PX" % size, font=small, fill="#5B6078")
        x += 225

    draw.text((1030, 760), "PALETTE ROLES", font=heading, fill="#14172A")
    roles = (
        ("Identity dark", palette["dark"]["accent"]),
        ("Identity light", palette["light"]["accent"]),
        ("Inherited emphasis", "#FF5300"),
        ("Success", "#2BCC73"),
        ("Failure", "#E05F5F"),
    )
    for index, (label, color) in enumerate(roles):
        y = 840 + index * 57
        draw.rounded_rectangle((1030, y, 1080, y + 42), radius=10, fill=color)
        draw.text((1100, y + 5), "%s  %s" % (label, color), font=small, fill="#14172A")

    path = output / ("%s-demo.png" % palette["id"])
    image.save(path)
    payload = {
        "schema_version": 1,
        "candidate": "cueframe-r1",
        "palette": palette,
        "palette_sha256": canonical_digest(palette),
        "contrast": contrast_observations(palette),
        "sibling_hue_minimum_degrees": 38.2 if palette["id"] == "cue-magenta-r1" else 31.3,
        "status": "proposed-owner-review",
        "public_eligible": False,
    }
    (output / ("%s-demo.json" % palette["id"])).write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def _gate_two_asset(path, maximum):
    image = Image.open(path).convert("RGBA")
    image.thumbnail(maximum, Image.Resampling.LANCZOS)
    return image


def _paste_center(canvas, asset, box, background):
    x1, y1, x2, y2 = box
    panel = Image.new("RGBA", (x2 - x1, y2 - y1), background)
    panel.alpha_composite(asset, ((panel.width - asset.width) // 2, (panel.height - asset.height) // 2))
    canvas.paste(panel.convert("RGB"), (x1, y1))


def _silhouette_metrics(approved, production, background):
    """Compare approved proof ink with a transparent production derivative."""
    background_rgb = Image.new("RGB", (1, 1), background).getpixel((0, 0))
    approved_rgb = approved.convert("RGB")
    production_rgba = production.convert("RGBA")
    approved_mask = set()
    production_mask = set()
    for y in range(approved_rgb.height):
        for x in range(approved_rgb.width):
            pixel = approved_rgb.getpixel((x, y))
            # Compare at approximately 50% coverage so the RGB proof and the
            # transparent production raster use equivalent antialias cutoffs.
            if max(abs(pixel[index] - background_rgb[index]) for index in range(3)) > 64:
                approved_mask.add((x, y))
            if production_rgba.getpixel((x, y))[3] >= 128:
                production_mask.add((x, y))

    union = approved_mask | production_mask
    intersection = approved_mask & production_mask

    def bounds(points):
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        return [min(xs), min(ys), max(xs), max(ys)]

    def centroid(points):
        count = float(len(points))
        return [sum(point[0] for point in points) / count, sum(point[1] for point in points) / count]

    approved_bbox = bounds(approved_mask)
    production_bbox = bounds(production_mask)
    approved_centroid = centroid(approved_mask)
    production_centroid = centroid(production_mask)
    return {
        "silhouette_iou": round(len(intersection) / float(len(union)), 6),
        "changed_pixel_fraction": round(len(approved_mask ^ production_mask) / float(len(union)), 6),
        "approved_bbox": approved_bbox,
        "production_bbox": production_bbox,
        "bbox_delta_max_px": max(abs(left - right) for left, right in zip(approved_bbox, production_bbox)),
        "centroid_delta_px": round(math.hypot(
            approved_centroid[0] - production_centroid[0],
            approved_centroid[1] - production_centroid[1],
        ), 6),
    }


def _gate_two_continuity(kit):
    """Render a side-by-side proof that production preserves Gate 1 construction."""
    candidate = CANDIDATES["cueframe-r1"]
    helper_path = ROOT / "brands" / "cueson" / "build" / "mk_paths.py"
    helper_spec = importlib.util.spec_from_file_location("cueson_mk_paths", helper_path)
    helper = importlib.util.module_from_spec(helper_spec)
    helper_spec.loader.exec_module(helper)

    def source_line(role, points, width):
        return {"type": "line", "role": role, "points": tuple(points), "width": width, "closed": False}

    production_source_geometry = {
        "full": tuple(source_line("accent", points, helper.FULL_BRACKET_WIDTH) for points in helper.FULL_BRACKETS)
        + tuple(source_line("ink", points, helper.FULL_RAIL_WIDTH) for points in helper.FULL_RAILS),
        "reduced": tuple(source_line("accent", points, helper.REDUCED_BRACKET_WIDTH) for points in helper.REDUCED_BRACKETS)
        + tuple(source_line("ink", points, helper.REDUCED_RAIL_WIDTH) for points in helper.REDUCED_RAILS),
    }
    production_source_sha256 = canonical_digest(production_source_geometry)
    approved_source_sha256 = geometry_fingerprint(candidate)
    coordinate_contract_matches = production_source_sha256 == approved_source_sha256

    comparisons = []
    proof_pairs = []
    for variant, size in (("full", 512), ("reduced", 512), ("full", 64), ("reduced", 32), ("reduced", 16)):
        approved = render_concept(candidate, variant, "dark", size, CUE_TEAL_PALETTE)
        production_master = Image.open(
            kit / "logos" / "png" / ("cueson-mark%s-color-1024.png" % ("-reduced" if variant == "reduced" else ""))
        ).convert("RGBA")
        production = production_master.resize((size, size), Image.Resampling.LANCZOS)
        metrics = _silhouette_metrics(approved, production, CUE_TEAL_PALETTE["dark"]["surface"])
        metrics.update({"variant": variant, "size_px": size})
        comparisons.append(metrics)
        proof_pairs.append((variant, size, approved, production))

    image = Image.new("RGB", (1800, 1320), "#F1F2F8")
    draw = ImageDraw.Draw(image)
    title = _font(DISPLAY_FONT, 60)
    heading = _font(DISPLAY_FONT, 27)
    body = _font(BODY_FONT, 23)
    mono = _font(MONO_FONT, 17)
    row_label = _font(MONO_FONT, 13)
    draw.text((70, 48), "Gate 1 to production continuity", font=title, fill="#14172A")
    draw.text((70, 126), "Approved centerlines expanded directly with glyphkit.capsule. No redrawing or coordinate changes.", font=body, fill="#5B6078")
    headers = ("APPROVED GATE 1", "PRODUCTION MASTER", "50% OVERLAY", "PIXEL DIFFERENCE")
    for index, label in enumerate(headers):
        draw.text((70 + index * 420, 205), label, font=mono, fill="#005D55")

    for row, variant in enumerate(("full", "reduced")):
        _, _, approved, production = next(pair for pair in proof_pairs if pair[0] == variant and pair[1] == 512)
        approved = approved.resize((300, 300), Image.Resampling.LANCZOS)
        production = production.resize((300, 300), Image.Resampling.LANCZOS)
        background = Image.new("RGBA", (300, 300), CUE_TEAL_PALETTE["dark"]["surface"])
        production_panel = background.copy()
        production_panel.alpha_composite(production)
        overlay = Image.blend(approved.convert("RGB"), production_panel.convert("RGB"), 0.5)
        difference = ImageChops.difference(approved.convert("RGB"), production_panel.convert("RGB"))
        difference = difference.point(lambda value: min(255, value * 5))
        y = 260 + row * 365
        draw.text((7, y + 136), variant.upper(), font=row_label, fill="#5B6078")
        for column, panel in enumerate((approved, production_panel, overlay, difference)):
            image.paste(panel.convert("RGB"), (70 + column * 420, y))

    draw.text((70, 1010), "MEASURED CONTINUITY", font=heading, fill="#14172A")
    y = 1060
    for record in comparisons:
        line = "%s %3d px   IoU %.4f   changed %.2f%%   bbox delta %d px   centroid delta %.3f px" % (
            record["variant"].upper(), record["size_px"], record["silhouette_iou"],
            record["changed_pixel_fraction"] * 100.0, record["bbox_delta_max_px"], record["centroid_delta_px"],
        )
        draw.text((70, y), line, font=mono, fill="#14172A")
        y += 44

    continuity = {
        "schema_version": 1,
        "approved_candidate": "cueframe-r1",
        "approved_geometry_sha256": approved_source_sha256,
        "production_source_geometry_sha256": production_source_sha256,
        "coordinate_contract_matches": coordinate_contract_matches,
        "production_method": "glyphkit.capsule expansion of unchanged approved centerline segments",
        "comparisons": comparisons,
        "thresholds": {
            "master_silhouette_iou_minimum": 0.90,
            "bbox_delta_maximum_px": 1,
            "centroid_delta_maximum_px": 1.0,
        },
    }
    continuity["passes"] = coordinate_contract_matches and all(
        (record["size_px"] != 512 or record["silhouette_iou"] >= continuity["thresholds"]["master_silhouette_iou_minimum"])
        and record["bbox_delta_max_px"] <= continuity["thresholds"]["bbox_delta_maximum_px"]
        and record["centroid_delta_px"] <= continuity["thresholds"]["centroid_delta_maximum_px"]
        for record in comparisons
    )
    return image, continuity


def _gate_two_lockups(kit):
    image = Image.new("RGB", (1800, 1500), "#F1F2F8")
    draw = ImageDraw.Draw(image)
    title = _font(DISPLAY_FONT, 64)
    label = _font(MONO_FONT, 20)
    draw.text((70, 50), "Cueson derived identity spread", font=title, fill="#14172A")
    panels = (
        ("HORIZONTAL · DARK", "cueson-horizontal-color-1024.png", "#080A14"),
        ("HORIZONTAL · LIGHT", "cueson-horizontal-light-1024.png", "#F7F8FC"),
        ("STACKED · DARK", "cueson-stacked-color-1024.png", "#080A14"),
        ("STACKED · LIGHT", "cueson-stacked-light-1024.png", "#F7F8FC"),
        ("WORDMARK · SINGLE INK", "cueson-wordmark-white-1024.png", "#080A14"),
        ("MARK · SINGLE INK", "cueson-mark-black-1024.png", "#F7F8FC"),
    )
    for index, (caption, filename, background) in enumerate(panels):
        column, row = index % 2, index // 2
        x, y = 70 + column * 850, 170 + row * 420
        asset = _gate_two_asset(kit / "logos" / "png" / filename, (760, 315))
        _paste_center(image, asset, (x, y, x + 780, y + 330), background)
        draw.text((x, y + 345), caption, font=label, fill="#5B6078")
    return image


def _gate_two_applications(kit):
    image = Image.new("RGB", (1800, 1400), "#080A14")
    draw = ImageDraw.Draw(image)
    title = _font(DISPLAY_FONT, 64)
    heading = _font(DISPLAY_FONT, 30)
    label = _font(MONO_FONT, 18)
    draw.text((70, 50), "Reduced marks, crops, and platform masks", font=title, fill="#F4F6FF")
    reduced = Image.open(kit / "favicons" / "favicon-512x512.png").convert("RGBA")
    x = 70
    for size in (256, 128, 64, 32, 16):
        panel = Image.new("RGBA", (280, 300), "#101425")
        proof = reduced.resize((size, size), Image.Resampling.LANCZOS)
        panel.alpha_composite(proof, ((280 - size) // 2, (280 - size) // 2))
        image.paste(panel.convert("RGB"), (x, 170))
        draw.text((x, 488), "%d PX" % size, font=label, fill="#A7AEC7")
        x += 330
    draw.text((70, 575), "PLATFORM FAMILIES", font=heading, fill="#F4F6FF")
    platforms = (
        ("WEB / PWA", kit / "icons" / "web" / "android-chrome-512x512.png"),
        ("ANDROID", kit / "icons" / "android" / "play-store" / "google-play-512.png"),
        ("IOS", kit / "icons" / "apple" / "ios" / "Assets.xcassets" / "AppIcon.appiconset" / "AppIcon-1024.png"),
        ("MACOS", kit / "icons" / "apple" / "macos" / "AppIcon.iconset" / "icon_512x512.png"),
        ("WINDOWS", kit / "icons" / "windows" / "msix" / "Assets" / "Square150x150Logo.scale-400.png"),
    )
    for index, (caption, path) in enumerate(platforms):
        x = 70 + index * 340
        asset = _gate_two_asset(path, (260, 260))
        _paste_center(image, asset, (x, 650, x + 280, 930), "#101425")
        draw.text((x, 950), caption, font=label, fill="#A7AEC7")
    social = _gate_two_asset(kit / "logos" / "png" / "cueson-social-preview-1280.png", (900, 330))
    _paste_center(image, social, (450, 1030, 1350, 1360), "#101425")
    return image


def _gate_two_copy():
    image = Image.new("RGB", (1800, 1100), "#F1F2F8")
    draw = ImageDraw.Draw(image)
    title = _font(DISPLAY_FONT, 64)
    display = _font(DISPLAY_FONT, 72)
    body = _font(BODY_FONT, 34)
    mono = _font(MONO_FONT, 19)
    draw.text((70, 50), "Approved copy compositions", font=title, fill="#14172A")
    for x, surface, ink, accent, label in (
        (70, "#080A14", "#F4F6FF", "#62BEB2", "DARK SURFACE"),
        (930, "#F7F8FC", "#14172A", "#005D55", "LIGHT SURFACE"),
    ):
        draw.rounded_rectangle((x, 165, x + 800, 1030), radius=28, fill=surface)
        draw.text((x + 50, 215), "Cueson", font=display, fill=ink)
        draw.text((x + 54, 325), VERBAL_IDENTITY["slogan"], font=body, fill=accent)
        draw.line((x + 54, 405, x + 746, 405), fill=accent, width=5)
        draw.text((x + 54, 480), VERBAL_IDENTITY["preferred_description_lines"][0], font=body, fill=ink)
        draw.text((x + 54, 535), VERBAL_IDENTITY["preferred_description_lines"][1], font=body, fill=ink)
        draw.text((x + 54, 930), label, font=mono, fill=accent)
    return image


def _gate_two_public_surfaces(kit):
    image = Image.new("RGB", (1800, 1300), "#080A14")
    draw = ImageDraw.Draw(image)
    title = _font(DISPLAY_FONT, 64)
    heading = _font(DISPLAY_FONT, 30)
    body = _font(BODY_FONT, 24)
    mono = _font(MONO_FONT, 18)
    draw.text((70, 50), "Proposed public surfaces", font=title, fill="#F4F6FF")
    draw.text((70, 130), "Preview only. Publication remains disabled until Gate 2 approval.", font=body, fill="#A7AEC7")
    for index, (caption, path) in enumerate((
        ("BRAND GUIDELINES", kit / "qc" / "pages-guidelines-index.png"),
        ("CUESON DATA SPECIMEN", kit / "qc" / "pages-cueson-data-index.png"),
        ("SOCIAL / REPOSITORY", kit / "logos" / "png" / "cueson-social-preview-1280.png"),
    )):
        x = 70 + index * 570
        asset = _gate_two_asset(path, (520, 750))
        _paste_center(image, asset, (x, 220, x + 520, 970), "#101425")
        draw.text((x, 990), caption, font=mono, fill="#62BEB2")
    draw.text((70, 1090), "PROPOSED COMPLETE SURFACE SET", font=heading, fill="#F4F6FF")
    _wrapped(draw, (70, 1145), "Showcase card · brand landing page · guideline topics · downloads · registry endpoints · public metadata · structured data · social preview", body, "#A7AEC7", 115)
    return image


def _gate_two_overview(lockups, applications, copy, public):
    image = Image.new("RGB", (1800, 1450), "#F1F2F8")
    draw = ImageDraw.Draw(image)
    title = _font(DISPLAY_FONT, 64)
    body = _font(BODY_FONT, 25)
    draw.text((70, 50), "S026 Gate 2: Cueson final derivative review", font=title, fill="#14172A")
    draw.text((70, 132), "Cueframe r1 + Cue Teal r1 · complete spread · publication waits for this approval", font=body, fill="#5B6078")
    for (x, y), sheet in zip(((70, 215), (930, 215), (70, 830), (930, 830)), (lockups, applications, copy, public)):
        preview = sheet.copy()
        preview.thumbnail((800, 550), Image.Resampling.LANCZOS)
        image.paste(preview, (x, y))
    return image


def generate_gate_two(output):
    """Build the deterministic, ignored Gate 2 review packet from the private kit."""
    output = Path(output).resolve()
    kit = ROOT / "dist" / "cueson"
    gate_one = json.loads((ROOT / "specs" / "026-cueson-brand-kit" / "gate-1-proposal.json").read_text(encoding="utf-8"))
    if gate_one["status"] != "approved" or gate_one["approval"]["approved_palette"] != "cue-teal-r1":
        raise ValueError("current Cueframe and Cue Teal Gate 1 approval is required")
    if "| **Problems found** | **0** |" not in (kit / "VERIFY.md").read_text(encoding="utf-8"):
        raise ValueError("private Cueson kit verification must report zero problems")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    lockups = _gate_two_lockups(kit)
    applications = _gate_two_applications(kit)
    copy = _gate_two_copy()
    public = _gate_two_public_surfaces(kit)
    continuity_image, continuity = _gate_two_continuity(kit)
    if not continuity["passes"]:
        raise ValueError("production derivatives do not preserve the approved Gate 1 construction")
    lockups.save(output / "lockups.png")
    applications.save(output / "applications.png")
    copy.save(output / "copy-compositions.png")
    public.save(output / "public-surfaces.png")
    continuity_image.save(output / "construction-continuity.png")
    (output / "construction-continuity.json").write_text(
        json.dumps(continuity, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    _gate_two_overview(lockups, applications, copy, public).save(output / "overview.png")

    for source, name in (
        (kit / "qc" / "logo-sheet.png", "generated-logo-sheet.png"),
        (kit / "qc" / "contact-sheet.png", "brand-guide-contact-sheet.png"),
        (kit / "logos" / "provenance.json", "derivative-provenance.json"),
        (kit / "logos" / "approval.json", "derivative-approval.json"),
        (kit / "icons" / "manifest.json", "platform-manifest.json"),
        (kit / "VERIFY.md", "VERIFY.md"),
    ):
        shutil.copyfile(source, output / name)

    provenance = json.loads((kit / "logos" / "provenance.json").read_text(encoding="utf-8"))
    proposal = {
        "schema_version": 1,
        "gate": 2,
        "status": "pending-owner-approval",
        "approved_candidate": "cueframe-r1",
        "approved_candidate_geometry_sha256": gate_one["approval"]["approved_candidate_geometry_sha256"],
        "approved_palette": "cue-teal-r1",
        "approved_palette_sha256": gate_one["approval"]["approved_palette_sha256"],
        "copy_lines": [VERBAL_IDENTITY["name"], VERBAL_IDENTITY["slogan"]] + VERBAL_IDENTITY["preferred_description_lines"],
        "families": ["mark", "mark-reduced", "horizontal", "stacked", "wordmark", "single-ink"],
        "platforms": ["web", "windows", "apple", "android", "social", "repository"],
        "publication_surfaces": ["showcase-card", "brand-landing-page", "guideline-topics", "downloads", "registry-endpoints", "public-metadata", "structured-data", "social-preview"],
        "derivatives": provenance["derivatives"],
        "construction_continuity": continuity,
        "public_eligible": False,
        "approval": None,
    }
    proposal["proposal_sha256"] = canonical_digest(proposal)
    (output / "proposal.json").write_text(json.dumps(proposal, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    (output / "index.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>S026 Cueson Gate 2</title><style>body{margin:0;background:#080A14;color:#F4F6FF;font-family:Arial,sans-serif}main{max-width:1500px;margin:auto;padding:48px}img{display:block;max-width:100%;height:auto;margin:40px 0}</style></head><body><main><h1>Cueson Gate 2</h1><p>Private approval evidence. Publication remains disabled until this gate is approved.</p><img src="construction-continuity.png" alt="Gate 1 to production construction continuity"><img src="overview.png" alt="Cueson derivative overview"><img src="lockups.png" alt="Cueson lockups"><img src="applications.png" alt="Cueson platform applications"><img src="copy-compositions.png" alt="Cueson copy compositions"><img src="public-surfaces.png" alt="Proposed Cueson public surfaces"></main></body></html>\n', encoding="utf-8", newline="\n")

    records = []
    for path in sorted(output.iterdir()):
        if path.is_file() and path.name != "manifest.json":
            records.append({"path": path.name, "bytes": path.stat().st_size, "sha256": file_digest(path)})
    manifest = {
        "schema_version": 1,
        "gate": 2,
        "approved_candidate": "cueframe-r1",
        "approved_palette": "cue-teal-r1",
        "families": proposal["families"],
        "platforms": proposal["platforms"],
        "derivative_provenance_sha256": file_digest(kit / "logos" / "provenance.json"),
        "derivative_approval_sha256": file_digest(kit / "logos" / "approval.json"),
        "kit_manifest_sha256": file_digest(kit / "manifest.json"),
        "proposal_sha256": proposal["proposal_sha256"],
        "approval_status": "pending",
        "public_eligible": False,
        "files": records,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return output


CONSUMER_ASSETS = (
    ("logos/svg/cueson-mark-color.svg", "assets/brand/cueson-mark.svg", "Primary product mark"),
    ("logos/svg/cueson-mark-reduced-color.svg", "assets/brand/cueson-mark-reduced.svg", "Reduced product mark at 32 pixels and below"),
    ("logos/svg/cueson-horizontal-color.svg", "assets/brand/cueson-horizontal.svg", "Primary horizontal lockup"),
    ("logos/svg/cueson-stacked-color.svg", "assets/brand/cueson-stacked.svg", "Stacked lockup"),
    ("logos/svg/cueson-wordmark-color.svg", "assets/brand/cueson-wordmark.svg", "Wordmark-only treatment"),
    ("logos/png/cueson-social-preview-1280.png", "assets/brand/cueson-social-preview.png", "Repository and social preview"),
    ("icons/web/favicon.svg", "public/favicon.svg", "Scalable browser icon"),
    ("icons/web/site.webmanifest", "public/site.webmanifest", "Web application icon manifest"),
    ("icons/android/play-store/google-play-512.png", "assets/brand/platform/android/google-play-512.png", "Android store icon source"),
    ("icons/apple/ios/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png", "assets/brand/platform/apple/AppIcon-1024.png", "Apple application icon source"),
    ("icons/windows/msix/Assets/Square150x150Logo.scale-400.png", "assets/brand/platform/windows/Square150x150Logo.scale-400.png", "Windows application icon source"),
)


def generate_consumer_handoff(kit):
    """Write a hash-addressed future-import map and certify it in the kit manifest."""
    kit = Path(kit).resolve()
    if kit.name != "cueson" or not (kit / "brand.json").is_file():
        raise ValueError("consumer handoff requires a built Cueson kit")
    gate_one = json.loads((ROOT / "specs" / "026-cueson-brand-kit" / "gate-1-proposal.json").read_text(encoding="utf-8"))
    gate_two = json.loads((ROOT / "specs" / "026-cueson-brand-kit" / "gate-2-proposal.json").read_text(encoding="utf-8"))
    if gate_one.get("status") != "approved" or gate_two.get("status") != "approved" or not gate_two.get("public_eligible"):
        raise ValueError("both current Cueson approvals are required for consumer handoff")
    generated_assets = []
    for relative, destination, use in CONSUMER_ASSETS:
        path = kit / Path(relative)
        if not path.is_file():
            raise ValueError("missing proposed consumer asset: %s" % relative)
        generated_assets.append({
            "source": relative,
            "sha256": file_digest(path),
            "destination": destination,
            "use": use,
        })
    brand_source = ROOT / "brands" / "cueson" / "brand.json"
    path_source = ROOT / "brands" / "cueson" / "build" / "mk_paths.py"
    payload = {
        "schema_version": 1,
        "brand": "cueson",
        "brand_revision": {
            "product_evidence_revision": EVIDENCE["cueson_revision"],
            "last_nonmaterial_drift_revision": "cc2bac00786bc6ae6a1f8d4503640cb3ad34f8b6",
            "brand_json_sha256": file_digest(brand_source),
            "path_generator_sha256": file_digest(path_source),
            "derivative_configuration_sha256": gate_two["approved_sources"]["derivative_configuration_sha256"],
        },
        "approval_ids": {
            "gate_1": {
                "candidate": gate_one["approval"]["approved_candidate"],
                "geometry_sha256": gate_one["approval"]["approved_candidate_geometry_sha256"],
                "palette": gate_one["approval"]["approved_palette"],
                "palette_sha256": gate_one["approval"]["approved_palette_sha256"],
                "proposal_sha256": gate_one["approval"]["approved_proposal_sha256"],
            },
            "gate_2": {
                "attempt": gate_two["approval"]["attempt"],
                "derivative_manifest_sha256": gate_two["approval"]["approved_derivative_manifest_sha256"],
                "packet_manifest_sha256": gate_two["approval"]["approved_packet_manifest_sha256"],
                "construction_continuity_sha256": gate_two["approval"]["approved_construction_continuity_sha256"],
            },
        },
        "source_assets": [
            {"path": "brands/cueson/brand.json", "sha256": file_digest(brand_source)},
            {"path": "brands/cueson/build/mk_paths.py", "sha256": file_digest(path_source)},
        ],
        "generated_assets": generated_assets,
        "consumer_destinations": {
            "repository": "https://github.com/shruggietech/cueson",
            "policy": "Copy only the generated assets listed above after every hash is verified in the future Cueson slice.",
        },
        "licenses": {
            "required_files": ["LICENSE", "NOTICE", "LICENSE-BRAND.md"],
            "brand_assets": "Reserved ShruggieTech product identity. Use only for the Cueson project or accurate reference.",
            "fonts": "Geist, Geist Mono, and Space Grotesk remain under the SIL Open Font License 1.1.",
        },
        "usage_limits": {
            "minimum_px": {"full_mark": 24, "reduced_mark_threshold": 32, "horizontal": 160, "stacked": 112, "wordmark": 120},
            "clear_space_units": 48,
            "backgrounds": "Use only the approved dark, light, black, white, and single-ink colorways for the corresponding surface.",
            "mask": "Preserve the generated alpha silhouette. Do not hollow, clip, or reinterpret interior regions.",
            "transformations": "No redrawing, path normalization, non-uniform scaling, recoloring outside approved role maps, or derivation from raster files.",
        },
        "integration_issue": {
            "required": True,
            "repository": "shruggietech/cueson",
            "title": "Import the approved Cueson identity kit",
            "required_scope": ["hash verification", "declared destinations", "license notices", "consumer tests", "owner review"],
        },
        "integration_slice": {
            "required": True,
            "workflow": "repository-installed Spec Kit",
            "depends_on": "the future Cueson integration issue",
        },
        "repository_boundary": {
            "working_tree_modified_by_s026": False,
            "remote_modified_by_s026": False,
            "integration_commit_created": False,
        },
        "domain_boundary": {
            "domain": "cueson.io",
            "domain_changed_by_s026": False,
            "dns_changed_by_s026": False,
            "cloudflare_changed_by_s026": False,
            "activation_authorized": False,
        },
    }
    payload["sha256"] = canonical_digest(payload)
    output = kit / "consumer-handoff.json"
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    manifest_path = kit / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"] = [item for item in manifest.get("files", []) if item.get("path") != "consumer-handoff.json"]
    manifest["files"].append({"path": "consumer-handoff.json", "bytes": output.stat().st_size, "sha256": file_digest(output)})
    manifest["files"].sort(key=lambda item: item["path"])
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", type=int, choices=(1, 2), default=1)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--color-demo", choices=("cue-magenta", "cue-teal"))
    parser.add_argument("--consumer-handoff", action="store_true")
    arguments = parser.parse_args()
    if arguments.consumer_handoff:
        path = generate_consumer_handoff(ROOT / "dist" / "cueson")
        print("generated certified Cueson consumer handoff in %s" % path)
        return 0
    if arguments.color_demo:
        palette = CUE_MAGENTA_PALETTE if arguments.color_demo == "cue-magenta" else CUE_TEAL_PALETTE
        path = generate_color_demo(arguments.output, palette)
        print("generated non-publishing S026 color demo in %s" % path)
        return 0
    output = generate(arguments.output) if arguments.gate == 1 else generate_gate_two(arguments.output)
    print("generated non-publishing S026 Gate %d study in %s" % (arguments.gate, output))
    print(output / "overview.png")
    if arguments.gate == 1:
        print(output / "palette.png")
    print(output / "manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
