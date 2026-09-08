#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the ignored S020 owner proof packet from unchanged ESO Weave sources."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "skill" / "templates"
sys.path.insert(0, str(TEMPLATES))

from gen_logo import raster  # noqa: E402


SOURCE = ROOT / "brands" / "eso-weave"
OUTPUT = ROOT / "dist" / "eso-weave-approval" / "gate-1"
MARK = SOURCE / "assets" / "source" / "eso-weave-mark.svg"
GLYPH = SOURCE / "assets" / "source" / "eso-weave-glyph.svg"
FONT = SOURCE / "fonts" / "Inter-SemiBold.ttf"
REFERENCE = SOURCE / "assets" / "reference" / "banner.png"
PROPOSAL = ROOT / "specs" / "020-eso-weave-provenance-kit" / "gate-1-proposal.json"
SIZES = (256, 64, 32, 16)
SURFACES = {"dark": "#0E1116", "light": "#F7F5F0"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_png(source: Path, name: str) -> Image.Image:
    target = OUTPUT / (name + "-256.png")
    raster(["-w", "256", str(source), "-o", str(target)])
    return Image.open(target).convert("RGBA")


def fit(source: Image.Image, size: int) -> Image.Image:
    return source.resize((size, size), Image.Resampling.LANCZOS)


def fit_visible(source: Image.Image, size: int) -> Image.Image:
    bounds = source.getchannel("A").getbbox()
    visible = source.crop(bounds) if bounds else source
    visible.thumbnail((size, size), Image.Resampling.LANCZOS)
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    image.alpha_composite(visible, ((size - visible.width) // 2, (size - visible.height) // 2))
    return image


def wordmark(height: int, light: bool) -> Image.Image:
    font = ImageFont.truetype(str(FONT), max(8, int(height * 1.2)))
    spacing = max(1, int(height * 0.035))
    parts = (("ESO", "#14110B" if light else "#E6EDF3"), ("Weave", "#986000" if light else "#F2B03C"))
    boxes = [font.getbbox(text) for text, _color in parts]
    widths = [sum(font.getlength(char) for char in text) + spacing * max(0, len(text) - 1) for text, _color in parts]
    top = min(box[1] for box in boxes)
    bottom = max(box[3] for box in boxes)
    gap = max(1, int(height * 0.08))
    width = round(sum(widths) + gap)
    image = Image.new("RGBA", (max(1, width + 4), max(1, bottom - top + 8)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    x = 2
    for part_index, ((text, color), part_width) in enumerate(zip(parts, widths)):
        for char in text:
            draw.text((x, 4 - top), char, font=font, fill=color)
            x += font.getlength(char) + spacing
        if part_index == 0:
            x += gap
    cropped = image.crop(image.getbbox())
    pad = max(1, round(height * 0.05))
    ink_height = max(1, height - pad * 2)
    ink_width = max(1, round(cropped.width * ink_height / cropped.height))
    ink = cropped.resize((ink_width, ink_height), Image.Resampling.LANCZOS)
    result = Image.new("RGBA", (ink_width + pad * 2, height), (0, 0, 0, 0))
    result.alpha_composite(ink, (pad, pad))
    return result


def mono_glyph(size: int, surface: str, foreground: str) -> Image.Image:
    scale = size / 100.0
    image = Image.new("RGBA", (size, size), surface)
    draw = ImageDraw.Draw(image)
    width = max(1, round(11 * scale))
    def line(points, fill, stroke):
        points = [(round(x * scale), round(y * scale)) for x, y in points]
        draw.line(points, fill=fill, width=stroke, joint="curve")
        radius = stroke / 2
        for x, y in (points[0], points[-1]):
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=fill)

    line(((24, 74), (50, 42), (76, 74)), foreground, width)
    line(((24, 30), (50, 62), (76, 30)), foreground, width)
    return image


def horizontal(mark: Image.Image, size: int, surface: str, light: bool) -> Image.Image:
    logo = fit(mark, size)
    words = wordmark(max(8, round(size * 0.72)), light)
    gap = max(2, round(size * 0.22))
    width = logo.width + gap + words.width
    image = Image.new("RGBA", (width, size), surface)
    image.alpha_composite(logo, (0, 0))
    image.alpha_composite(words, (logo.width + gap, (size - words.height) // 2))
    return image


def stacked(mark: Image.Image, size: int, surface: str, light: bool) -> Image.Image:
    logo = fit_visible(mark, max(1, round(size * 1.6)))
    words = wordmark(max(8, round(size * 0.65)), light)
    gap = max(2, round(size * 0.16))
    width = max(logo.width, words.width)
    image = Image.new("RGBA", (width, logo.height + gap + words.height), surface)
    image.alpha_composite(logo, ((width - logo.width) // 2, 0))
    image.alpha_composite(words, ((width - words.width) // 2, logo.height + gap))
    return image


def wordmark_on_surface(height: int, surface: str, light: bool) -> Image.Image:
    words = wordmark(height, light)
    image = Image.new("RGBA", words.size, surface)
    image.alpha_composite(words)
    return image


def source_reference(mark: Image.Image, glyph: Image.Image, size: int, surface: str) -> Image.Image:
    gap = max(8, size // 3)
    image = Image.new("RGBA", (size * 2 + gap, size), surface)
    image.alpha_composite(fit(mark, size), (0, 0))
    image.alpha_composite(fit(glyph, size), (size + gap, 0))
    return image


def contact_sheet(files: dict[tuple[str, str], Path], mark: Image.Image, glyph: Image.Image, size: int) -> Path:
    thumb_w, thumb_h = 540, 220
    margin = 36
    title_h = 150
    proposals = ("reduced-and-platform", "horizontal-lockup", "stacked-lockup", "wordmark-only", "single-ink")
    rows = len(proposals) + 1
    row_height = thumb_h + 58
    sheet = Image.new("RGB", (thumb_w * 2 + margin * 3, title_h + rows * row_height + margin), "#F2F3F5")
    draw = ImageDraw.Draw(sheet)
    heading = ImageFont.truetype(str(FONT), 38)
    label = ImageFont.truetype(str(SOURCE / "fonts" / "Inter-Regular.ttf"), 18)
    draw.text((margin, 28), f"S020 Gate 1: source vs proposal at {size} px", font=heading, fill="#14110B")
    draw.text((margin, 78), "Source files are isolated in the first row. Every proposal below is one complete output.", font=label, fill="#4B5563")
    draw.text((margin, 112), "DARK SURFACE", font=label, fill="#14110B")
    draw.text((margin * 2 + thumb_w, 112), "LIGHT SURFACE", font=label, fill="#14110B")
    for row, proposal_id in enumerate(("source-reference",) + proposals):
        for column, surface_name in enumerate(("dark", "light")):
            x0 = margin + column * (thumb_w + margin)
            y0 = title_h + row * row_height
            name = "authoritative sources: badged mark | badge-less glyph" if proposal_id == "source-reference" else proposal_id
            draw.text((x0, y0), name, font=label, fill="#14110B")
            if proposal_id == "source-reference":
                image = source_reference(mark, glyph, size, SURFACES[surface_name])
            else:
                image = Image.open(files[(surface_name, proposal_id)]).convert("RGBA")
            image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            x = x0 + (thumb_w - image.width) // 2
            y = y0 + 30 + (thumb_h - image.height) // 2
            sheet.paste(image.convert("RGB"), (x, y), image if image.mode == "RGBA" else None)
    target = OUTPUT / f"gate-1-overview-{size}.png"
    sheet.save(target)
    return target


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    expected = {key: value["sha256"] for key, value in proposal["authoritative_sources"].items()}
    actual = {"mark": digest(MARK), "glyph": digest(GLYPH)}
    if actual != expected:
        raise SystemExit("authoritative source hash drift blocks Gate 1 proof generation")
    mark = source_png(MARK, "source-mark")
    glyph = source_png(GLYPH, "source-glyph")
    reference = Image.open(REFERENCE).convert("RGBA")
    proof_files = {size: {} for size in SIZES}
    manifest = []
    for surface_name, surface in SURFACES.items():
        light = surface_name == "light"
        contextual = mark if light else glyph
        foreground = "#14110B" if light else "#FFFFFF"
        for size in SIZES:
            candidates = {
                "reduced-and-platform": fit(mark, size),
                "horizontal-lockup": horizontal(contextual, size, surface, light),
                "stacked-lockup": stacked(contextual, size, surface, light),
                "wordmark-only": wordmark_on_surface(size, surface, light),
                "single-ink": mono_glyph(size, surface, foreground),
            }
            for proposal_id, image in candidates.items():
                target = OUTPUT / f"{proposal_id}-{surface_name}-{size}.png"
                image.convert("RGB").save(target)
                manifest.append({"proposal": proposal_id, "surface": surface_name, "size_px": size, "path": target.name, "sha256": digest(target)})
                proof_files[size][(surface_name, proposal_id)] = target
    overviews = [contact_sheet(proof_files[size], mark, glyph, size) for size in SIZES]
    manifest_path = OUTPUT / "manifest.json"
    manifest_path.write_text(json.dumps({"source_hashes": actual, "production_derivative_geometry_created": False, "proofs": manifest, "overviews": [path.name for path in overviews]}, indent=2) + "\n", encoding="utf-8", newline="\n")
    for overview in overviews:
        print(overview)
    print(manifest_path)
    print(f"{len(manifest)} exact proof contexts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
