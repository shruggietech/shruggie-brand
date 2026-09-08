#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate lockups, raster exports and favicons around hand-authored paths.

This runtime copy extends the stock builder with optional rectangular mark
canvases, filled compound paths and explicit per-colourway role mappings. The
fallback remains fully compatible with the stock scalar ``logo.grid`` schema.
"""
import binascii
import base64
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import zlib

from svgelements import Path
from brand_contract import font_face_path, logo_source_contract, semantic_colors, square_enclosure_profile, typography_families
from capabilities import load_capabilities
from iconkit import contain_visible, generate_icon_suites
from process_utils import hidden_process_kwargs

NODE = os.environ.get("GP_NODE") or shutil.which("node")
RESVG = os.environ.get("GP_RESVG_RENDERER") or os.path.join(os.path.dirname(__file__), "rsvg-convert.js")


def standalone_mark_ratio(brand):
    """Return the visible long-edge occupancy that preserves declared clear space."""
    enclosure = square_enclosure_profile(brand)
    if enclosure:
        visible = enclosure["size"] + enclosure["stroke_width"]
        return visible / enclosure["canvas_size"]
    logo = brand.get("logo") or {}
    width = float(logo.get("artwork_width", logo.get("grid", 1000)))
    height = float(logo.get("artwork_height", logo.get("grid", 1000)))
    clear_space = float(logo.get("clear_space_units", 0))
    long_edge = max(width, height)
    if long_edge <= 0 or clear_space < 0:
        raise ValueError("standalone mark dimensions and clear space must be non-negative")
    return long_edge / (long_edge + 2.0 * clear_space)


def measured_ico_converter(capabilities):
    """Return only an ImageMagick executable accepted by the capability probe."""
    cli = capabilities.get("cli") or {}
    if cli.get("magick"):
        return "magick"
    if cli.get("convert"):
        return "convert"
    return None


def reset_generated_dir(kit, directory):
    root = os.path.abspath(kit)
    target = os.path.abspath(directory)
    allowed = {
        os.path.join(root, "logos", "png"),
        os.path.join(root, "favicons"),
    }
    if target not in allowed:
        raise ValueError("refusing to clear non-generated directory %s" % target)
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target, exist_ok=True)


def png_chunk(kind, data):
    return (struct.pack(">I", len(data)) + kind + data
            + struct.pack(">I", binascii.crc32(kind + data) & 0xffffffff))


def paeth(left, above, upper_left):
    estimate = left + above - upper_left
    left_distance = abs(estimate - left)
    above_distance = abs(estimate - above)
    upper_left_distance = abs(estimate - upper_left)
    if left_distance <= above_distance and left_distance <= upper_left_distance:
        return left
    return above if above_distance <= upper_left_distance else upper_left


def recolour_rgba_png(source, target, colour, luminance_mask):
    """Recolour an RGBA8 PNG using only the Python standard library."""
    with open(source, "rb") as handle:
        payload = handle.read()
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("image-backed logo source is not a PNG: %s" % source)
    position = 8
    header = None
    compressed = []
    while position < len(payload):
        length = struct.unpack(">I", payload[position:position + 4])[0]
        kind = payload[position + 4:position + 8]
        data = payload[position + 8:position + 8 + length]
        expected = struct.unpack(">I", payload[position + 8 + length:position + 12 + length])[0]
        if (binascii.crc32(kind + data) & 0xffffffff) != expected:
            raise ValueError("image-backed logo source has an invalid PNG checksum: %s" % source)
        if kind == b"IHDR":
            header = data
        elif kind == b"IDAT":
            compressed.append(data)
        elif kind == b"IEND":
            break
        position += 12 + length
    if header is None or not compressed:
        raise ValueError("image-backed logo source is incomplete: %s" % source)
    width, height, depth, colour_type, compression, filtering, interlace = struct.unpack(">IIBBBBB", header)
    if (depth, colour_type, compression, filtering, interlace) != (8, 6, 0, 0, 0):
        raise ValueError("image-backed logo source must be a non-interlaced RGBA8 PNG: %s" % source)
    stride = width * 4
    raw = zlib.decompress(b"".join(compressed))
    if len(raw) != height * (stride + 1):
        raise ValueError("image-backed logo source has an unexpected data length: %s" % source)
    decoded = []
    previous = bytearray(stride)
    offset = 0
    for _row in range(height):
        filter_type = raw[offset]
        scanline = bytearray(raw[offset + 1:offset + stride + 1])
        offset += stride + 1
        for index in range(stride):
            left = scanline[index - 4] if index >= 4 else 0
            above = previous[index]
            upper_left = previous[index - 4] if index >= 4 else 0
            if filter_type == 1:
                scanline[index] = (scanline[index] + left) & 0xff
            elif filter_type == 2:
                scanline[index] = (scanline[index] + above) & 0xff
            elif filter_type == 3:
                scanline[index] = (scanline[index] + ((left + above) // 2)) & 0xff
            elif filter_type == 4:
                scanline[index] = (scanline[index] + paeth(left, above, upper_left)) & 0xff
            elif filter_type != 0:
                raise ValueError("image-backed logo source uses an unknown PNG filter: %s" % source)
        decoded.append(scanline)
        previous = scanline
    rgb = tuple(int(colour[index:index + 2], 16) for index in (1, 3, 5))
    encoded = bytearray()
    for scanline in decoded:
        for index in range(0, stride, 4):
            if luminance_mask:
                scanline[index + 3] = round(scanline[index + 3] * max(scanline[index:index + 3]) / 255)
            scanline[index:index + 3] = bytes(rgb)
        encoded.append(0)
        encoded.extend(scanline)
    output = (b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", header)
              + png_chunk(b"IDAT", zlib.compress(bytes(encoded), 9)) + png_chunk(b"IEND", b""))
    with open(target, "wb") as handle:
        handle.write(output)


def recolour_raster(source, target, colour, luminance_mask):
    """Recolour any contract-supported raster master into an RGBA PNG."""
    with open(source, "rb") as handle:
        signature = handle.read(8)
    if signature == b"\x89PNG\r\n\x1a\n":
        recolour_rgba_png(source, target, colour, luminance_mask)
        return
    from PIL import Image
    rgb = tuple(int(colour[index:index + 2], 16) for index in (1, 3, 5))
    with Image.open(source) as image:
        rgba = image.convert("RGBA")
        pixels = rgba.load()
        for y in range(rgba.height):
            for x in range(rgba.width):
                red, green, blue, alpha = pixels[x, y]
                if luminance_mask:
                    alpha = round(alpha * max(red, green, blue) / 255)
                pixels[x, y] = (rgb[0], rgb[1], rgb[2], alpha)
        rgba.save(target, format="PNG")


def raster(args):
    width = args[args.index("-w") + 1] if "-w" in args else None
    height = args[args.index("-h") + 1] if "-h" in args else None
    source = args[-3] if "-o" in args else args[-2]
    output = args[args.index("-o") + 1]
    native = shutil.which("rsvg-convert")
    if native:
        command = [native] + args
    elif shutil.which("resvg"):
        command = [shutil.which("resvg")]
        if width: command += ["--width", width]
        if height: command += ["--height", height]
        command += [source, output]
    elif shutil.which("inkscape"):
        command = [shutil.which("inkscape"), source, "--export-type=png",
                   "--export-filename=" + output]
        if width: command.append("--export-width=" + width)
        if height: command.append("--export-height=" + height)
    elif NODE and os.path.exists(RESVG):
        command = [NODE, RESVG] + args
    else:
        raise RuntimeError("SVG rasterizer unavailable. Install rsvg-convert, resvg, Inkscape, or set GP_NODE and GP_RESVG_RENDERER.")
    subprocess.run(command, check=True, **hidden_process_kwargs())


def path_bbox(d):
    box = Path(d).bbox()
    if box is None:
        raise ValueError("empty logo path")
    return tuple(float(v) for v in box)


def element_bbox(element):
    kind = element.get("element", "path")
    stroke = float(element.get("stroke_width", 0)) / 2.0
    if kind == "path":
        x0, y0, x1, y1 = path_bbox(element["d"])
    elif kind == "rect":
        x0 = float(element["x"])
        y0 = float(element["y"])
        x1 = x0 + float(element["width"])
        y1 = y0 + float(element["height"])
    elif kind == "image":
        x0 = float(element.get("x", 0))
        y0 = float(element.get("y", 0))
        x1 = x0 + float(element["width"])
        y1 = y0 + float(element["height"])
    else:
        raise ValueError("unsupported imported SVG element %r" % kind)
    return (x0 - stroke, y0 - stroke, x1 + stroke, y1 + stroke)


def paths_bbox(paths):
    boxes = [element_bbox(element) for element in paths]
    return (
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    )


def svg(width, height, body, metadata=None):
    attributes = ""
    for name, value in sorted((metadata or {}).items()):
        if value is not None:
            attributes += ' data-%s="%s"' % (name.replace("_", "-"), value)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 %g %g" '
        'width="%g" height="%g" fill="none"%s>\n%s\n</svg>\n'
        % (width, height, width, height, attributes, body)
    )


def wordmark_outline(text, ttf, size=200, x_offset=0.0):
    from fontTools.misc.transform import Transform
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont

    font = TTFont(ttf)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    units = font["head"].unitsPerEm
    scale = size / units
    metrics = font["hmtx"]
    commands = []
    advance = 0.0
    for character in text:
        name = cmap.get(ord(character))
        if name is None:
            continue
        pen = SVGPathPen(glyphs)
        transform = Transform(scale, 0, 0, -scale, x_offset + advance * scale, 0)
        glyphs[name].draw(TransformPen(pen, transform))
        if pen.getCommands():
            commands.append(pen.getCommands())
        advance += metrics[name][0]
    return " ".join(commands), advance * scale


def main():
    spec_path, kit = sys.argv[1], sys.argv[2]
    with open(spec_path, encoding="utf-8") as handle:
        brand = json.load(handle)
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "..", "references", "01-canon.json"), encoding="utf-8") as handle:
        canon = json.load(handle)
    logo = brand.get("logo") or {}
    paths = logo.get("paths") or {}
    if not paths.get("full"):
        sys.exit("brand.json logo.paths.full is empty; hand-author the mark first")
    authority = logo_source_contract(brand, kit)

    # The geometry gate runs FIRST and blocks. Producing twenty colourways and a
    # favicon set from a mark that is clipped or off-centre wastes the run and
    # buries the defect under output. See references/08-glyph-construction.md.
    gate = subprocess.run([sys.executable,
                           os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "validate_glyph.py"), spec_path],
                          capture_output=True, text=True, **hidden_process_kwargs())
    sys.stdout.write(gate.stdout)
    if gate.returncode:
        sys.exit("glyph gate failed with %d problem(s). Fix build/mk_paths.py and "
                 "regenerate logo.paths before exporting anything."
                 % gate.returncode)

    grid = logo.get("grid", 512)
    enclosure = square_enclosure_profile(brand)
    canvas_width = enclosure["canvas_size"] if enclosure else logo.get("canvas_width", grid)
    canvas_height = enclosure["canvas_size"] if enclosure else logo.get("canvas_height", grid)
    clear_space = (enclosure["inset"] - enclosure["stroke_width"] / 2.0
                   if enclosure else logo.get("clear_space_units", int(min(canvas_width, canvas_height) * 0.11)))
    artwork_width = (enclosure["size"] + enclosure["stroke_width"]
                     if enclosure else logo.get("artwork_width", canvas_width))
    reduced_below = logo.get("reduced_below_px", 32)
    slug = brand["slug"]
    accent = brand["accent"]["bright"]
    accent_light = brand["accent"]["accessible"]
    dim = brand["accent"].get("dim") or brand["accent"]["deep"]
    base = brand.get("surfaces", {}).get("base", "#000000")
    semantic = semantic_colors(brand, canon)

    role_maps = {
        "color": {"accent": accent, "dim": dim, "neutral": dim, "emphasis": semantic["emphasis"]},
        "light": {"accent": accent_light, "dim": "#0A0A0A", "neutral": "#0A0A0A", "emphasis": semantic["action"]},
        "white": {"accent": "#FFFFFF", "dim": "#FFFFFF", "neutral": "#FFFFFF", "emphasis": "#FFFFFF"},
        "black": {"accent": "#000000", "dim": "#000000", "neutral": "#000000", "emphasis": "#000000"},
    }
    for colourway, mapping in (logo.get("role_colors") or {}).items():
        role_maps.setdefault(colourway, {}).update(mapping)
    if brand["affiliation"]["inheritance"] == "independent":
        role_maps["color"]["emphasis"] = semantic["emphasis"]
        role_maps["light"]["emphasis"] = semantic["action"]

    svg_dir = os.path.join(kit, "logos", "svg")
    png_dir = os.path.join(kit, "logos", "png")
    favicon_dir = os.path.join(kit, "favicons")
    os.makedirs(svg_dir, exist_ok=True)
    reset_generated_dir(kit, png_dir)
    reset_generated_dir(kit, favicon_dir)

    def write(path, value):
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(value)

    def raster_mask_file(item, colour):
        source = os.path.join(kit, item["source"])
        if os.path.splitext(source)[1].lower() == ".svg":
            with open(source, "rb") as handle:
                return "data:image/svg+xml;base64," + base64.b64encode(handle.read()).decode("ascii")
        luminance_mask = item.get("mask") == "luminance"
        stem = os.path.splitext(os.path.basename(source))[0]
        filename = "_%s-mask-%s-%s.png" % (slug, colour.lstrip("#").lower(), stem)
        target = os.path.join(svg_dir, filename)
        recolour_raster(source, target, colour, luminance_mask)
        try:
            with open(target, "rb") as handle:
                return "data:image/png;base64," + base64.b64encode(handle.read()).decode("ascii")
        finally:
            os.remove(target)

    def render_paths(path_list, roles, indent="  ", asset_prefix=""):
        output = []
        for item in path_list:
            colour = roles.get(item.get("role", "accent"), accent)
            kind = item.get("element", "path")
            stroke_width = item.get("stroke_width")
            stroked = item.get("fill") == "none" or stroke_width is not None
            paint = (' fill="none" stroke="%s"' % colour) if stroked else (' fill="%s"' % colour)
            if stroke_width is not None:
                paint += ' stroke-width="%g"' % float(stroke_width)
            if item.get("stroke_linecap"):
                paint += ' stroke-linecap="%s"' % item["stroke_linecap"]
            if item.get("stroke_linejoin"):
                paint += ' stroke-linejoin="%s"' % item["stroke_linejoin"]
            if kind == "rect":
                shape = '<rect x="%g" y="%g" width="%g" height="%g"' % (
                    float(item["x"]), float(item["y"]),
                    float(item["width"]), float(item["height"]))
                if item.get("rx") is not None:
                    shape += ' rx="%g"' % float(item["rx"])
                output.append('%s%s%s/>' % (indent, shape, paint))
                continue
            if kind == "image":
                source = raster_mask_file(item, colour)
                output.append(
                    '%s<image x="%g" y="%g" width="%g" height="%g" '
                    'preserveAspectRatio="xMidYMid meet" href="%s" xlink:href="%s"/>' % (
                        indent, float(item.get("x", 0)), float(item.get("y", 0)),
                        float(item["width"]), float(item["height"]), source, source))
                continue
            if kind != "path":
                raise ValueError("unsupported imported SVG element %r" % kind)
            rule = item.get("fill_rule")
            extra = '' if not rule else ' fill-rule="%s" clip-rule="%s"' % (rule, rule)
            output.append('%s<path d="%s"%s%s/>' % (indent, item["d"], paint, extra))
        return "\n".join(output)

    def square_content_geometry(path_list):
        source_box = paths_bbox(path_list)
        source_width = source_box[2] - source_box[0]
        source_height = source_box[3] - source_box[1]
        scale = enclosure["content_scale"]
        x = (enclosure["canvas_size"] - source_width * scale) / 2.0
        y = (enclosure["canvas_size"] - source_height * scale) / 2.0
        safe_min = enclosure["inset"] + enclosure["stroke_width"] / 2.0
        safe_max = enclosure["canvas_size"] - safe_min
        if (x < safe_min - 0.5 or y < safe_min - 0.5
                or x + source_width * scale > safe_max + 0.5
                or y + source_height * scale > safe_max + 0.5):
            raise ValueError("square enclosure content exceeds the validated safe area")
        return source_box, x, y, scale

    def render_mark(path_list, roles, colourway, indent="  "):
        if not enclosure:
            return render_paths(path_list, roles, indent)
        source_box, x, y, scale = square_content_geometry(path_list)
        frame_role = enclosure["frame_role"]
        stroke_role = enclosure["stroke_role"]
        if colourway in ("black", "white") and enclosure["monochrome_knockout"]:
            knockout = [item for item in path_list
                        if item.get("role", "accent") == enclosure["knockout_role"]]
            if not knockout:
                knockout = path_list
            mask_id = "%s-%s-square-knockout" % (slug, colourway)
            mask_roles = {item.get("role", "accent"): "#000000" for item in knockout}
            knocked_out = render_paths(knockout, mask_roles, indent + "      ")
            return (
                '%s<g data-square-enclosure="true" data-lockup-component="mark">\n'
                '%s  <defs><mask id="%s" maskUnits="userSpaceOnUse" maskContentUnits="userSpaceOnUse" x="0" y="0" width="%g" height="%g">\n'
                '%s    <rect width="%g" height="%g" fill="#000000"/>\n'
                '%s    <rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="#FFFFFF"/>\n'
                '%s    <g transform="translate(%g,%g) scale(%g) translate(%g,%g)">\n%s\n%s    </g>\n'
                '%s  </mask></defs>\n'
                '%s  <rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" mask="url(#%s)"/>\n'
                '%s</g>'
                % (indent, indent, mask_id, canvas_width, canvas_height,
                   indent, canvas_width, canvas_height,
                   indent, enclosure["inset"], enclosure["inset"], enclosure["size"],
                   enclosure["size"], enclosure["corner_radius"], indent, x, y, scale,
                   -source_box[0], -source_box[1], knocked_out, indent, indent, indent,
                   enclosure["inset"], enclosure["inset"], enclosure["size"],
                   enclosure["size"], enclosure["corner_radius"], roles["accent"],
                   mask_id, indent)
            )
        content = render_paths(path_list, roles, indent + "    ")
        return (
            '%s<g data-square-enclosure="true" data-lockup-component="mark">\n'
            '%s  <rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-width="%g"/>\n'
            '%s  <g transform="translate(%g,%g) scale(%g) translate(%g,%g)">\n%s\n%s  </g>\n'
            '%s</g>'
            % (indent, indent, enclosure["inset"], enclosure["inset"],
               enclosure["size"], enclosure["size"], enclosure["corner_radius"],
               roles[frame_role], roles[stroke_role], enclosure["stroke_width"],
               indent, x, y, scale, -source_box[0], -source_box[1], content, indent, indent)
        )

    written = []
    derivatives = []
    svg_records = {}

    def derivative_record(filename, kind, variant, colourway, is_svg=True):
        source = authority.get(variant) if variant else None
        if source:
            record = source["record"]
            base_transform = "embed-unchanged" if record["format"] == "svg" else "recolor-mask"
            transformations = [base_transform, "resize"]
            if kind == "lockup":
                transformations.append("place-in-lockup")
            input_id = record["id"]
            source_sha256 = record["sha256"]
        else:
            transformations = []
            input_id = None
            source_sha256 = None
        relative = "logos/svg/%s" % filename if is_svg else "logos/png/%s" % filename
        item = {
            "path": relative,
            "kind": kind,
            "variant": variant,
            "colourway": colourway,
            "source_mode": authority["source_mode"] if variant else "constructed",
            "input_id": input_id,
            "source_sha256": source_sha256,
            "transformations": transformations,
            "embedded_metadata": bool(is_svg),
        }
        derivatives.append(item)
        if is_svg:
            svg_records[filename] = item
        return item

    def svg_metadata(record):
        values = {
            "logo_source_mode": record["source_mode"],
            "logo_variant": record["variant"],
        }
        if record["input_id"]:
            values["authoritative_input_id"] = record["input_id"]
            values["authoritative_source_sha256"] = record["source_sha256"]
        return values

    def write_provenance():
        for item in derivatives:
            output = os.path.join(kit, item["path"].replace("/", os.sep))
            digest = hashlib.sha256()
            with open(output, "rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            item["sha256"] = digest.hexdigest()
        payload = {
            "schema_version": 1,
            "brand": slug,
            "source_mode": authority["source_mode"],
            "derivatives": sorted(derivatives, key=lambda item: item["path"]),
        }
        write(os.path.join(kit, "logos", "provenance.json"), json.dumps(payload, indent=2, sort_keys=True) + "\n")
        by_path = {item["path"]: item for item in derivatives}
        approval_records = []
        for item in sorted(derivatives, key=lambda record: record["path"]):
            if item["path"].endswith(".svg"):
                approval_records.append({"path": item["path"], "sha256": item["sha256"]})
                continue
            match = re.match(r"logos/png/(.+)-[0-9]+\.png$", item["path"])
            if not match:
                raise ValueError("raster derivative lacks a deterministic SVG master: %s" % item["path"])
            source_path = "logos/svg/%s.svg" % match.group(1)
            source = by_path.get(source_path)
            if source is None:
                raise ValueError("raster derivative source is absent from provenance: %s" % source_path)
            approval_records.append({
                "path": item["path"],
                "rendered_from": source_path,
                "rendered_from_sha256": source["sha256"],
            })
        approval = {"schema_version": 1, "brand": slug, "derivatives": approval_records}
        write(os.path.join(kit, "logos", "approval.json"), json.dumps(approval, indent=2, sort_keys=True) + "\n")

    contextual = logo.get("contextual_variants") or {}

    def contextual_mark(colourway, reduced=False):
        selected = contextual.get(colourway)
        if colourway in {"white", "black"} and selected == "single-ink":
            single = paths.get("single-ink") or []
            if not single:
                raise ValueError("contextual single-ink output requires logo.paths.single-ink")
            return single, None
        if reduced or selected == "reduced":
            return paths.get("reduced") or paths["full"], "reduced"
        return paths["full"], "full"

    variants = (("mark", False), ("mark-reduced", True))
    for variant, force_reduced in variants:
        for colourway, roles in role_maps.items():
            path_list, source_variant = contextual_mark(colourway, force_reduced)
            box = paths_bbox(path_list)
            if enclosure:
                square_content_geometry(path_list)
            else:
                assert box[0] >= -0.5 and box[1] >= -0.5
                assert box[2] <= canvas_width + 0.5 and box[3] <= canvas_height + 0.5
            filename = "%s-%s-%s.svg" % (slug, variant, colourway)
            record = derivative_record(filename, "mark", source_variant, colourway)
            write(os.path.join(svg_dir, filename), svg(canvas_width, canvas_height, render_mark(path_list, roles, colourway), svg_metadata(record)))
            written.append(filename)

    mark_box = ((enclosure["inset"] - enclosure["stroke_width"] / 2.0,) * 2
                + (enclosure["canvas_size"] - enclosure["inset"] + enclosure["stroke_width"] / 2.0,) * 2
                if enclosure else paths_bbox(paths["full"]))
    mark_width = mark_box[2] - mark_box[0]
    mark_height = mark_box[3] - mark_box[1]

    families = typography_families(brand)
    ttf_path, _ = font_face_path(brand, kit, "display", max(families["display"]["weights"]), outline=True)
    ttf = str(ttf_path)

    wordmark_d = ""
    wordmark_advance = 0
    wordmark_parts = []
    supplied_wordmark = paths.get("wordmark") or []
    if supplied_wordmark:
        wordmark_box = paths_bbox(supplied_wordmark)
        wordmark_ink_width_raw = wordmark_box[2] - wordmark_box[0]
        wordmark_ink_height_raw = wordmark_box[3] - wordmark_box[1]
        wordmark_cap_raw = max(1.0, wordmark_ink_height_raw)
        wordmark_advance = wordmark_ink_width_raw
    elif ttf:
        configured_segments = logo.get("wordmark_segments") or []
        if configured_segments:
            cursor = 0.0
            for index, segment in enumerate(configured_segments):
                if index:
                    cursor += float(segment.get("gap_units", 0))
                segment_d, segment_advance = wordmark_outline(segment["text"], ttf, 200, cursor)
                wordmark_parts.append((segment_d, segment.get("role", "wordmark")))
                cursor += segment_advance
            wordmark_d = " ".join(item[0] for item in wordmark_parts)
            wordmark_advance = cursor
        else:
            wordmark_d, wordmark_advance = wordmark_outline(brand.get("wordmark_text", slug), ttf, 200)
        wordmark_box = tuple(float(v) for v in Path(wordmark_d).bbox())
        wordmark_cap_raw = max(1.0, -wordmark_box[1])
        wordmark_ink_width_raw = wordmark_box[2] - wordmark_box[0]
        wordmark_ink_height_raw = wordmark_box[3] - wordmark_box[1]
    if wordmark_d or supplied_wordmark:
        lockup_specs = logo.get("lockups") or {}

        def word_ink(colourway, roles):
            if colourway in ("white", "black"):
                return roles["accent"]
            return roles.get("wordmark", "#F2F5FA" if colourway == "color" else "#0A0A0A")

        def word_group(colourway, roles, x, y, scale, indent="  "):
            if supplied_wordmark:
                content = render_paths(supplied_wordmark, roles, indent + "  ")
                return ('%s<g data-lockup-component="wordmark" transform="translate(%g,%g) scale(%g) translate(%g,%g)">\n%s\n%s</g>'
                        % (indent, x, y, scale, -wordmark_box[0], -wordmark_box[1], content, indent))
            if wordmark_parts:
                content = "".join('<path d="%s" fill="%s"/>' %
                                  (part, roles.get(role, word_ink(colourway, roles)))
                                  for part, role in wordmark_parts)
                return '%s<g data-lockup-component="wordmark" transform="translate(%g,%g) scale(%g)">%s</g>' % (
                    indent, x, y, scale, content)
            return '%s<g data-lockup-component="wordmark" transform="translate(%g,%g) scale(%g)"><path d="%s" fill="%s"/></g>' % (
                indent, x, y, scale, wordmark_d, word_ink(colourway, roles))

        pad = 12
        wordmark_width = (wordmark_ink_width_raw if supplied_wordmark else wordmark_advance) + pad * 2
        wordmark_height = wordmark_ink_height_raw + pad * 2 if supplied_wordmark else 260
        for colourway, roles in role_maps.items():
            body = word_group(colourway, roles, pad, pad if supplied_wordmark else 200, 1.0)
            filename = "%s-wordmark-%s.svg" % (slug, colourway)
            record = derivative_record(filename, "wordmark", None, colourway)
            write(os.path.join(svg_dir, filename), svg(wordmark_width, wordmark_height, body, svg_metadata(record)))
            written.append(filename)

        for colourway, roles in role_maps.items():
            horizontal_spec = lockup_specs.get("horizontal") or {}
            word_scale = float(horizontal_spec.get("wordmark_scale", 0.62))
            mark_render_height = float(horizontal_spec.get("mark_height_units", 160.0))
            mark_scale = mark_render_height / mark_height
            mark_render_width = mark_width * mark_scale
            gap = float(horizontal_spec.get("gap_units", 34.0))
            horizontal_height = float(horizontal_spec.get("canvas_height_units", 200.0))
            lockup_pad = 24.0
            mark_y = (horizontal_height - mark_render_height) / 2.0
            word_baseline = float(horizontal_spec.get(
                "wordmark_baseline_units",
                horizontal_height / 2.0 + 200.0 * word_scale * 0.36,
            ))
            word_y = (horizontal_height - wordmark_ink_height_raw * word_scale) / 2.0 if supplied_wordmark else word_baseline
            word_x = lockup_pad + mark_render_width + gap
            lockup_width = mark_render_width + gap + wordmark_advance * word_scale + lockup_pad * 2.0
            lockup_paths, lockup_variant = contextual_mark(colourway)
            lockup_box = paths_bbox(lockup_paths)
            lockup_mark_width = lockup_box[2] - lockup_box[0]
            lockup_mark_height = lockup_box[3] - lockup_box[1]
            mark_scale = mark_render_height / lockup_mark_height
            mark_render_width = lockup_mark_width * mark_scale
            word_x = lockup_pad + mark_render_width + gap
            lockup_width = mark_render_width + gap + wordmark_advance * word_scale + lockup_pad * 2.0
            mark_group = render_mark(lockup_paths, roles, colourway, "    ")
            body = (
                '  <g transform="translate(%g,%g) scale(%g) translate(%g,%g)">\n%s\n  </g>\n'
                '%s'
                % (
                    lockup_pad,
                    mark_y,
                    mark_scale,
                    -lockup_box[0],
                    -lockup_box[1],
                    mark_group,
                    word_group(colourway, roles, word_x, word_y, word_scale),
                )
            )
            filename = "%s-horizontal-%s.svg" % (slug, colourway)
            record = derivative_record(filename, "lockup", lockup_variant, colourway)
            write(os.path.join(svg_dir, filename), svg(lockup_width, horizontal_height, body, svg_metadata(record)))
            written.append(filename)

            stacked_spec = lockup_specs.get("stacked") or {}
            stacked_word_scale = float(stacked_spec.get("wordmark_scale", 0.62))
            stacked_cap_height = wordmark_cap_raw * stacked_word_scale
            ratio_by_colourway = stacked_spec.get("mark_height_c_by_colourway") or {}
            stacked_mark_height = stacked_cap_height * float(ratio_by_colourway.get(colourway, stacked_spec.get("mark_height_c", 1.8)))
            stacked_mark_scale = stacked_mark_height / lockup_mark_height
            stacked_mark_width = lockup_mark_width * stacked_mark_scale
            stacked_word_width = wordmark_ink_width_raw * stacked_word_scale
            stacked_word_height = wordmark_ink_height_raw * stacked_word_scale
            stacked_gap = stacked_cap_height * float(stacked_spec.get("gap_c", 0.45))
            stacked_pad = max(20.0, stacked_cap_height * 0.35)
            stacked_width = max(stacked_mark_width, stacked_word_width) + stacked_pad * 2
            stacked_word_top = stacked_pad + stacked_mark_height + stacked_gap
            stacked_word_baseline = stacked_word_top - wordmark_box[1] * stacked_word_scale
            stacked_height = stacked_word_top + stacked_word_height + stacked_pad
            mark_x = (stacked_width - stacked_mark_width) / 2
            word_x = (stacked_width - stacked_word_width) / 2
            stacked = (
                '  <g transform="translate(%g,%g) scale(%g) translate(%g,%g)">\n%s\n  </g>\n'
                '%s'
                % (
                    mark_x,
                    stacked_pad,
                    stacked_mark_scale,
                    -lockup_box[0],
                    -lockup_box[1],
                    mark_group,
                    word_group(
                        colourway,
                        roles,
                        word_x if supplied_wordmark else word_x - wordmark_box[0] * stacked_word_scale,
                        stacked_word_top if supplied_wordmark else stacked_word_baseline,
                        stacked_word_scale,
                    ),
                )
            )
            filename = "%s-stacked-%s.svg" % (slug, colourway)
            record = derivative_record(filename, "lockup", lockup_variant, colourway)
            write(os.path.join(svg_dir, filename), svg(stacked_width, stacked_height, stacked, svg_metadata(record)))
            written.append(filename)

    if wordmark_d or supplied_wordmark:
        roles = role_maps["color"]
        preview_width, preview_height = 1280, 640
        preview_lockup_center_y = 245.0
        preview_word_scale = 1.0
        horizontal_spec = lockup_specs.get("horizontal") or {}
        horizontal_word_scale = float(horizontal_spec.get("wordmark_scale", 0.62))
        preview_mark_height = float(horizontal_spec.get("mark_height_units", 160.0)) / horizontal_word_scale
        mark_scale = preview_mark_height / mark_height
        preview_mark_width = mark_width * mark_scale
        preview_gap = float(horizontal_spec.get("gap_units", 34.0)) / horizontal_word_scale
        preview_word_width = wordmark_ink_width_raw * preview_word_scale
        preview_word_height = wordmark_ink_height_raw * preview_word_scale
        preview_lockup_width = preview_mark_width + preview_gap + preview_word_width
        preview_fit = min(1.0, (preview_width - 128.0) / preview_lockup_width)
        if preview_fit < 1.0:
            preview_word_scale *= preview_fit
            preview_mark_height *= preview_fit
            mark_scale *= preview_fit
            preview_mark_width *= preview_fit
            preview_gap *= preview_fit
            preview_word_width *= preview_fit
            preview_word_height *= preview_fit
            preview_lockup_width = preview_mark_width + preview_gap + preview_word_width
        preview_x = (preview_width - preview_lockup_width) / 2
        preview_mark_top = preview_lockup_center_y - preview_mark_height / 2.0
        horizontal_height = float(horizontal_spec.get("canvas_height_units", 200.0))
        horizontal_baseline = float(horizontal_spec.get(
            "wordmark_baseline_units",
            horizontal_height / 2.0 + 200.0 * horizontal_word_scale * 0.36,
        ))
        normalized_baseline_offset = (
            horizontal_baseline - horizontal_height / 2.0
        ) / horizontal_word_scale
        preview_baseline = preview_lockup_center_y + normalized_baseline_offset * preview_word_scale
        preview_word_top = preview_lockup_center_y - preview_word_height / 2.0
        tagline_ttf, _ = font_face_path(brand, kit, "display", min(families["display"]["weights"]), outline=True)
        tagline_ttf = str(tagline_ttf)
        tagline_d, _ = wordmark_outline(brand.get("brand_idea", "View your files."), tagline_ttf, 56)
        tagline_box = tuple(float(v) for v in Path(tagline_d).bbox())
        tagline_top = preview_lockup_center_y + preview_mark_height / 2.0 + 38.0
        tagline_left = preview_x + preview_mark_width + preview_gap
        tagline_width = tagline_box[2] - tagline_box[0]
        tagline_scale = min(1.0, (preview_width - 64.0 - tagline_left) / tagline_width)
        tagline_baseline = tagline_top - tagline_box[1] * tagline_scale
        tagline_x = tagline_left - tagline_box[0] * tagline_scale
        mark_group = render_mark(paths["full"], roles, "color", "      ")
        preview_word = word_group(
            "color",
            roles,
            preview_x + preview_mark_width + preview_gap if supplied_wordmark else preview_x + preview_mark_width + preview_gap - wordmark_box[0] * preview_word_scale,
            preview_word_top if supplied_wordmark else preview_baseline,
            preview_word_scale,
        )
        preview = (
            '  <rect width="1280" height="640" fill="%s"/>\n'
            '  <g transform="translate(%g,%g) scale(%g) translate(%g,%g)">\n%s\n  </g>\n'
            '%s\n'
            '  <g transform="translate(%g,%g) scale(%g)"><path d="%s" fill="%s"/></g>'
            % (base, preview_x, preview_mark_top, mark_scale, -mark_box[0], -mark_box[1], mark_group,
               preview_word,
               tagline_x, tagline_baseline, tagline_scale, tagline_d, roles["neutral"])
        )
        filename = "%s-social-preview.svg" % slug
        record = derivative_record(filename, "lockup", "full", "color")
        write(os.path.join(svg_dir, filename), svg(preview_width, preview_height, preview, svg_metadata(record)))
        written.append(filename)

    capabilities = load_capabilities(kit)
    icon_full_svg = os.path.join(svg_dir, "%s-mark-color.svg" % slug)
    icon_reduced_svg = os.path.join(svg_dir, "%s-mark-reduced-color.svg" % slug)

    def render_icon_source(source, output, size):
        from PIL import Image
        temporary = output.with_name(output.stem + "-rendered.png")
        if canvas_width >= canvas_height:
            raster(["-w", str(size), str(source), "-o", str(temporary)])
        else:
            raster(["-h", str(size), str(source), "-o", str(temporary)])
        try:
            with Image.open(str(temporary)) as rendered:
                rgba = rendered.convert("RGBA")
                rgba.thumbnail((size, size), Image.Resampling.LANCZOS)
                square_image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
                square_image.alpha_composite(
                    rgba,
                    ((size - rgba.width) // 2, (size - rgba.height) // 2),
                )
                square_image.save(str(output), format="PNG")
        finally:
            if temporary.exists():
                temporary.unlink()

    if not capabilities.get("svg_raster"):
        write_provenance()
        generate_icon_suites(
            brand, kit, icon_full_svg, icon_reduced_svg, render_icon_source,
            capabilities, monochrome_svg=os.path.join(svg_dir, "%s-mark-white.svg" % slug),
        )
        print("SKIP raster exports and native icon binaries: %s at core tier"
              % capabilities.get("raster_reason", "required raster capability unavailable"))
        print("wrote %d vector SVG masters and a vector-only icon index" % len(written))
        return 0

    from PIL import Image

    def assert_visible_raster(path):
        with Image.open(path) as rendered:
            alpha = rendered.convert("RGBA").getchannel("A")
            if alpha.getbbox() is None:
                raise ValueError("rasterized identity asset has no visible pixels: %s" % path)

    for filename in written:
        width = 1280 if "social-preview" in filename else 1024
        source = os.path.join(svg_dir, filename)
        output = os.path.join(png_dir, filename[:-4] + "-%d.png" % width)
        standalone_mark = filename.startswith(slug + "-mark-")
        if standalone_mark:
            raster(["-h", str(width), source, "-o", output])
            with Image.open(output) as rendered:
                mark_image = rendered.convert("RGBA")
                square_image = contain_visible(mark_image, width, standalone_mark_ratio(brand))
                square_image.save(output)
            with Image.open(output) as squared:
                assert squared.size == (width, width), "%s is not square" % output
        else:
            raster(["-w", str(width), source, "-o", output])
        assert_visible_raster(output)
        svg_record = svg_records[filename]
        png_record = dict(svg_record)
        png_record["path"] = "logos/png/%s" % os.path.basename(output)
        png_record["embedded_metadata"] = False
        derivatives.append(png_record)

    write_provenance()

    generate_icon_suites(
        brand, kit, icon_full_svg, icon_reduced_svg, render_icon_source,
        capabilities, monochrome_svg=os.path.join(svg_dir, "%s-mark-white.svg" % slug),
    )

    print("canvas %g x %g; artwork width %g" % (canvas_width, canvas_height, artwork_width))
    print("clear space %d units = %.1f%% of artwork width" % (clear_space, 100.0 * clear_space / artwork_width))
    print("mark bbox %s inside canvas" % (tuple(round(v, 1) for v in mark_box),))
    print("wrote %d SVGs, rasters, and categorized platform icon suites" % len(written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
