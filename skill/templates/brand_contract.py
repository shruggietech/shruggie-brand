#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared fail-closed contract for affiliation, supplied inputs, and typography."""

from __future__ import annotations

import hashlib
import json
import os
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


OWNED = "shruggietech-owned"
THIRD_PARTY = "third-party"
PROJECT_ENDORSEMENT = "A ShruggieTech project"
SERVICE_CREDIT = "Brand system by ShruggieTech"
ROLES = ("display", "body", "mono")
HOUSE_FAMILIES = {
    "display": {"name": "Space Grotesk", "weights": [500, 700]},
    "body": {"name": "Geist", "weights": [400, 500]},
    "mono": {"name": "Geist Mono", "weights": [400]},
}
HOUSE_FACES = (
    {"role": "display", "path": "fonts/woff2/SpaceGrotesk-Medium.woff2", "weight": 500, "style": "normal", "format": "woff2"},
    {"role": "display", "path": "fonts/woff2/SpaceGrotesk-Bold.woff2", "weight": 700, "style": "normal", "format": "woff2"},
    {"role": "display", "path": "fonts/ttf/SpaceGrotesk-Medium.ttf", "weight": 500, "style": "normal", "format": "ttf"},
    {"role": "display", "path": "fonts/ttf/SpaceGrotesk-Bold.ttf", "weight": 700, "style": "normal", "format": "ttf"},
    {"role": "body", "path": "fonts/woff2/Geist-Regular.woff2", "weight": 400, "style": "normal", "format": "woff2"},
    {"role": "body", "path": "fonts/woff2/Geist-Medium.woff2", "weight": 500, "style": "normal", "format": "woff2"},
    {"role": "body", "path": "fonts/ttf/Geist-Regular.ttf", "weight": 400, "style": "normal", "format": "ttf"},
    {"role": "body", "path": "fonts/ttf/Geist-Medium.ttf", "weight": 500, "style": "normal", "format": "ttf"},
    {"role": "mono", "path": "fonts/woff2/GeistMono-Regular.woff2", "weight": 400, "style": "normal", "format": "woff2"},
    {"role": "mono", "path": "fonts/ttf/GeistMono-Regular.ttf", "weight": 400, "style": "normal", "format": "ttf"},
)
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".jsx", ".md", ".mjs", ".svg", ".ts", ".tsx", ".txt", ".xml", ".yaml", ".yml"}
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")
ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class ContractError(ValueError):
    pass


def load_brand(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require(condition, message):
    if not condition:
        raise ContractError(message)


def contained_path(root, relative, required=True, boundary=None):
    _require(isinstance(relative, str) and relative and not os.path.isabs(relative), "path must be a non-empty relative path: %r" % relative)
    _require("\\" not in relative, "paths must use forward slashes: %s" % relative)
    base = Path(root).resolve()
    allowed = (base / boundary).resolve() if boundary else base
    candidate = base / Path(relative)
    cursor = base
    for part in Path(relative).parts:
        cursor = cursor / part
        _require(not cursor.is_symlink(), "symbolic-link paths are not permitted: %s" % relative)
    resolved = candidate.resolve()
    try:
        resolved.relative_to(allowed)
    except ValueError as error:
        raise ContractError("path escapes allowed boundary: %s" % relative) from error
    if required:
        _require(resolved.is_file(), "declared file is missing: %s" % relative)
    return resolved


def affiliation(brand):
    value = brand.get("affiliation")
    _require(isinstance(value, dict), "affiliation is required")
    required = {"ownership", "showcase", "parent", "inheritance", "endorsement", "service_credit"}
    _require(set(value) == required, "affiliation must contain exactly %s" % ", ".join(sorted(required)))
    ownership = value["ownership"]
    _require(ownership in {OWNED, THIRD_PARTY}, "unsupported affiliation ownership: %r" % ownership)
    _require(value["showcase"] in {"public", "private"}, "unsupported showcase state: %r" % value["showcase"])
    _require(value["inheritance"] in {"shruggietech-house", "independent"}, "unsupported inheritance mode: %r" % value["inheritance"])
    _require(value["endorsement"] in {"shruggietech-project", "none"}, "unsupported endorsement: %r" % value["endorsement"])
    _require(value["service_credit"] in {"brand-system-by-shruggietech", "none"}, "unsupported service credit: %r" % value["service_credit"])
    if ownership == THIRD_PARTY:
        _require(value["parent"] is None, "third-party brands cannot declare a ShruggieTech parent")
        _require(value["endorsement"] == "none", "third-party brands cannot use the owned-project endorsement")
    elif brand.get("kind") == "parent-brand":
        _require(value["inheritance"] == "shruggietech-house", "the ShruggieTech parent brand uses the house inheritance contract")
        _require(value["parent"] is None, "a parent brand cannot be its own parent")
        _require(value["endorsement"] == "none", "a parent brand cannot endorse itself as a project")
        _require(value["service_credit"] == "none", "owned brands cannot use a service credit")
    else:
        _require(value["inheritance"] == "shruggietech-house", "owned child brands must explicitly use ShruggieTech house inheritance")
        _require(value["parent"] == "ShruggieTech", "owned child brands must explicitly declare the ShruggieTech parent")
        _require(value["endorsement"] == "shruggietech-project", "owned child brands must explicitly select the project endorsement")
        _require(value["service_credit"] == "none", "owned brands cannot use a service credit")
    return value


def semantic_colors(brand, canon):
    if affiliation(brand)["inheritance"] == "shruggietech-house":
        immutable = canon["color"]["immutable"]
        return {"emphasis": immutable["orange"]["hex"], "action": immutable["orange-cta"]["hex"]}
    colors = brand.get("semantic_colors")
    _require(isinstance(colors, dict) and set(colors) == {"emphasis", "action"}, "independent inheritance requires semantic_colors.emphasis and semantic_colors.action")
    for name, value in colors.items():
        _require(isinstance(value, str) and HEX.fullmatch(value), "semantic color %s must be a six-digit hex value" % name)
    return colors


def application_icon_profile(brand):
    """Resolve the explicit application-icon presentation contract."""
    logo = brand.get("logo") or {}
    configured = logo.get("application_icon")
    if configured is None:
        configured = {}
    else:
        _require(isinstance(configured, dict), "logo.application_icon must be an object")
        _require(set(configured) == {"background"},
                 "logo.application_icon must contain exactly the supported background field")
    surfaces = brand.get("surfaces") or {}
    background = configured.get("background", surfaces.get("base", "#000000"))
    _require(isinstance(background, str) and HEX.fullmatch(background),
             "application icon background must be a six-digit hex color")
    threshold = logo.get("reduced_below_px", 32)
    _require(isinstance(threshold, int) and not isinstance(threshold, bool)
             and 1 <= threshold <= 1024,
             "reduced mark threshold must be an integer from 1 through 1024")
    return {"background": background.upper(), "reduced_below_px": threshold}


def affiliation_text(brand):
    value = affiliation(brand)
    if value["endorsement"] == "shruggietech-project":
        return PROJECT_ENDORSEMENT
    if value["service_credit"] == "brand-system-by-shruggietech":
        return SERVICE_CREDIT
    return ""


def public_showcase(brand):
    return affiliation(brand)["showcase"] == "public"


def typography_families(brand):
    typography = brand.get("typography")
    _require(isinstance(typography, dict), "typography is required")
    _require(typography.get("mode") in {"house", "fixed"}, "typography.mode must be house or fixed")
    families = typography.get("families")
    _require(isinstance(families, dict) and set(families) == set(ROLES), "typography.families must contain exactly display, body, and mono")
    for role in ROLES:
        family = families[role]
        _require(isinstance(family, dict) and set(family) == {"name", "weights"}, "typography family %s must contain name and weights" % role)
        _require(isinstance(family["name"], str) and family["name"].strip(), "typography family %s needs a name" % role)
        weights = family["weights"]
        _require(isinstance(weights, list) and weights and len(weights) == len(set(weights)), "typography family %s needs unique weights" % role)
        _require(all(isinstance(weight, int) and 1 <= weight <= 1000 for weight in weights), "typography family %s has an invalid weight" % role)
    if typography["mode"] == "house":
        _require(families == HOUSE_FAMILIES, "house typography must explicitly match the approved house families and weights")
        _require("faces" not in typography, "house typography must not override fixed faces")
    return families


def font_faces(brand):
    typography_families(brand)
    if brand["typography"]["mode"] == "house":
        return [dict(face) for face in HOUSE_FACES]
    faces = brand["typography"].get("faces")
    _require(isinstance(faces, list) and faces, "fixed typography requires face records")
    return faces


def font_face_path(brand, kit, role, preferred_weight=None, outline=False):
    families = typography_families(brand)
    wanted = preferred_weight if preferred_weight is not None else max(families[role]["weights"])
    allowed_formats = {"ttf", "otf"} if outline else {"woff2", "ttf", "otf"}
    choices = [face for face in font_faces(brand) if face["role"] == role and face["format"] in allowed_formats]
    _require(choices, "no usable %s font face for %s" % ("outline" if outline else "local", role))
    choices = [face for face in choices if face["weight"] == wanted]
    _require(choices, "no usable %s font face for %s weight %d" % ("outline" if outline else "local", role, wanted))
    choices.sort(key=lambda face: (0 if face["format"] == "woff2" and not outline else 1, face["path"]))
    return contained_path(kit, choices[0]["path"]), choices[0]


def _font_metadata(path):
    try:
        from fontTools.ttLib import TTFont
        font = TTFont(str(path))
    except Exception as error:
        raise ContractError("cannot read font binary %s: %s" % (path.name, error)) from error
    try:
        _require("fvar" not in font, "variable fonts require explicit axis support and are not accepted in S007")
        name = font["name"].getBestFamilyName()
        _require(name, "font binary has no measurable family name")
        _require("OS/2" in font, "font binary has no OS/2 metadata")
        os2 = font["OS/2"]
        flags = int(os2.fsSelection)
        style = "oblique" if flags & (1 << 9) else ("italic" if flags & 1 else "normal")
        fmt = "woff2" if font.flavor == "woff2" else ("otf" if font.sfntVersion == "OTTO" else "ttf")
        return {"family": name, "weight": int(os2.usWeightClass), "style": style, "format": fmt}
    finally:
        font.close()


def validate_typography(brand, kit):
    families = typography_families(brand)
    faces = font_faces(brand)
    if brand["typography"]["mode"] == "house":
        for face in faces:
            contained_path(kit, face["path"])
        return faces
    seen = set()
    for index, face in enumerate(faces):
        required = {"role", "path", "weight", "style", "format", "sha256", "license", "provenance", "usage_status"}
        _require(isinstance(face, dict) and set(face) == required, "fixed face %d must contain exactly the required fields" % index)
        _require(face["role"] in ROLES, "fixed face %d has an unsupported role" % index)
        _require(face["style"] in {"normal", "italic", "oblique"}, "fixed face %d has an unsupported style" % index)
        _require(face["format"] in {"ttf", "otf", "woff2"}, "fixed face %d has an unsupported format" % index)
        _require(face["usage_status"] == "approved", "fixed face %d is not approved" % index)
        _require(isinstance(face["license"], str) and face["license"].strip(), "fixed face %d lacks license evidence" % index)
        _require(isinstance(face["provenance"], str) and face["provenance"].strip(), "fixed face %d lacks provenance" % index)
        _require(DIGEST.fullmatch(face["sha256"] or ""), "fixed face %d has an invalid SHA-256" % index)
        _require(face["weight"] in families[face["role"]]["weights"], "fixed face %d declares a weight outside its family role" % index)
        key = (face["role"], face["weight"], face["style"], face["format"])
        _require(key not in seen, "duplicate fixed face: %r" % (key,))
        seen.add(key)
        path = contained_path(kit, face["path"], boundary="fonts")
        _require(path.suffix.lower().lstrip(".") == face["format"], "fixed face %d extension does not match format" % index)
        _require(sha256_file(path) == face["sha256"], "fixed face %d hash drift: %s" % (index, face["path"]))
        measured = _font_metadata(path)
        _require(measured["family"] == families[face["role"]]["name"], "fixed face %d family mismatch: declared %s, measured %s" % (index, families[face["role"]]["name"], measured["family"]))
        for field in ("weight", "style", "format"):
            _require(measured[field] == face[field], "fixed face %d %s mismatch: declared %r, measured %r" % (index, field, face[field], measured[field]))
    for role in ROLES:
        role_faces = [face for face in faces if face["role"] == role]
        _require(any(face["format"] in {"ttf", "otf"} for face in role_faces), "fixed typography role %s needs an outline-capable ttf or otf face" % role)
        for weight in families[role]["weights"]:
            _require(any(face["weight"] == weight for face in role_faces), "fixed typography role %s lacks weight %d" % (role, weight))
            _require(any(face["weight"] == weight and face["format"] in {"ttf", "otf"} for face in role_faces), "fixed typography role %s lacks outline-capable weight %d" % (role, weight))
    return faces


def _detect_image_format(path):
    data = path.read_bytes()[:32]
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return "webp"
    text = path.read_text(encoding="utf-8-sig", errors="ignore")[:512].lower()
    if "<svg" in text:
        return "svg"
    return None


def _validate_svg(path):
    source = path.read_text(encoding="utf-8-sig", errors="ignore").lower()
    _require("<?xml-stylesheet" not in source, "supplied SVG contains a prohibited stylesheet processing instruction")
    try:
        root = ET.parse(str(path)).getroot()
    except Exception as error:
        raise ContractError("invalid supplied SVG %s: %s" % (path.name, error)) from error
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1].lower()
        _require(tag not in {"script", "style", "text", "foreignobject"}, "supplied SVG contains prohibited <%s> content" % tag)
        for raw_name, raw_value in element.attrib.items():
            name = raw_name.rsplit("}", 1)[-1].lower()
            value = str(raw_value).strip()
            _require(not name.startswith("on"), "supplied SVG contains an event handler")
            if name in {"href", "src"}:
                _require(value.startswith("#"), "supplied SVG contains an external reference")
            lowered = value.lower().replace(" ", "")
            _require("http:" not in lowered and "https:" not in lowered and "@import" not in lowered, "supplied SVG contains a network reference")
            if "url(" in lowered:
                _require("url(#" in lowered, "supplied SVG contains an external paint reference")


def authoritative_inputs(brand, kit):
    records = brand.get("authoritative_inputs", [])
    _require(isinstance(records, list), "authoritative_inputs must be an array")
    identifiers = set()
    protected_roles = set()
    by_path = {}
    allowed_transforms = {"embed-unchanged", "recolor-mask", "palette-analysis"}
    normalized = []
    for index, record in enumerate(records):
        required = {"id", "role", "path", "format", "sha256", "color_profile", "usage_status", "license", "approved_transformations"}
        _require(isinstance(record, dict) and set(record) == required, "authoritative input %d must contain exactly the required fields" % index)
        _require(ID.fullmatch(record["id"] or ""), "authoritative input %d has an invalid id" % index)
        _require(record["id"] not in identifiers, "duplicate authoritative input id: %s" % record["id"])
        identifiers.add(record["id"])
        _require(record["role"] in {"mark", "reduced-mark", "wordmark", "reference-art"}, "authoritative input %s has an unsupported role" % record["id"])
        if record["role"] != "reference-art":
            _require(record["role"] not in protected_roles, "duplicate authoritative input role: %s" % record["role"])
            protected_roles.add(record["role"])
        _require(record["format"] in {"svg", "png", "jpeg", "webp"}, "authoritative input %s has an unsupported format" % record["id"])
        _require(record["color_profile"] in {"srgb", "embedded", "none", "unknown"}, "authoritative input %s has an unsupported color-profile state" % record["id"])
        _require(record["usage_status"] in {"approved", "reference-only"}, "authoritative input %s has an unsupported usage state" % record["id"])
        _require(isinstance(record["license"], str) and record["license"].strip(), "authoritative input %s lacks license or usage evidence" % record["id"])
        transforms = record["approved_transformations"]
        _require(isinstance(transforms, list) and len(transforms) == len(set(transforms)) and set(transforms).issubset(allowed_transforms), "authoritative input %s has invalid approved transformations" % record["id"])
        _require(DIGEST.fullmatch(record["sha256"] or ""), "authoritative input %s has an invalid SHA-256" % record["id"])
        path = contained_path(kit, record["path"])
        _require(record["path"] not in by_path, "authoritative input path declared more than once: %s" % record["path"])
        by_path[record["path"]] = record
        _require(_detect_image_format(path) == record["format"], "authoritative input %s format mismatch" % record["id"])
        _require(sha256_file(path) == record["sha256"], "authoritative input %s hash drift" % record["id"])
        if record["format"] == "svg":
            _validate_svg(path)
        normalized.append((record, path))
    for role in ("full", "reduced", "wordmark"):
        for item in ((brand.get("logo") or {}).get("paths") or {}).get(role, []):
            if item.get("element") != "image":
                continue
            record = by_path.get(item.get("source"))
            _require(record is not None, "imported logo image %s must be declared as an authoritative input" % item.get("source"))
            _require(record["usage_status"] == "approved", "imported logo image %s is not approved for generated use" % item.get("source"))
            required_transform = "embed-unchanged" if record["format"] == "svg" else "recolor-mask"
            _require(required_transform in record["approved_transformations"], "imported logo image %s does not approve %s" % (item.get("source"), required_transform))
    return normalized


def analyze_input(record, path):
    if "palette-analysis" not in record["approved_transformations"]:
        return None
    if record["format"] == "svg":
        _validate_svg(path)
        root = ET.parse(str(path)).getroot()
        colors = Counter()
        unsupported = set()
        for element in root.iter():
            values = [element.attrib.get("fill"), element.attrib.get("stroke")]
            style = element.attrib.get("style", "")
            values.extend(match.group(1) for match in re.finditer(r"(?:fill|stroke)\s*:\s*([^;]+)", style, re.I))
            for value in values:
                if not value or value.lower() in {"none", "transparent", "currentcolor"} or value.startswith("url("):
                    continue
                if re.fullmatch(r"#[0-9A-Fa-f]{3}", value):
                    value = "#" + "".join(character * 2 for character in value[1:])
                if HEX.fullmatch(value):
                    colors[value.upper()] += 1
                else:
                    unsupported.add(value)
        _require(colors, "authoritative input %s has no analyzable solid SVG colors" % record["id"])
        limitations = ["Gradients, opacity blending, CSS variables, and rendered area are not weighted."]
        if unsupported:
            limitations.append("Unsupported paint expressions were excluded: %s" % ", ".join(sorted(unsupported)))
        method = "svg-solid-paints-v1"
        visible = sum(colors.values())
        transparent = 0
    else:
        try:
            from PIL import Image
            with Image.open(path) as image:
                rgba = image.convert("RGBA")
                colors = Counter()
                transparent = 0
                pixels = rgba.load()
                for y in range(rgba.height):
                    for x in range(rgba.width):
                        red, green, blue, alpha = pixels[x, y]
                        if alpha == 0:
                            transparent += 1
                        else:
                            colors["#%02X%02X%02X" % (red, green, blue)] += 1
                profile = sorted(key for key in image.info if key.lower() in {"icc_profile", "srgb", "gamma"})
        except Exception as error:
            raise ContractError("cannot analyze supplied raster %s: %s" % (record["id"], error)) from error
        _require(colors, "authoritative input %s has no visible pixels" % record["id"])
        method = "raster-exact-rgba-v1"
        visible = sum(colors.values())
        limitations = ["Exact pixel counts include antialiasing and do not infer semantic regions.", "Detected profile signals: %s." % (", ".join(profile) if profile else "none")]
    candidates = [{"hex": color, "count": count} for color, count in sorted(colors.items(), key=lambda item: (-item[1], item[0]))[:12]]
    return {
        "input_id": record["id"],
        "source_sha256": record["sha256"],
        "method": method,
        "visible_samples": visible,
        "transparent_samples_ignored": transparent,
        "candidates": candidates,
        "limitations": limitations,
    }


def analyze_authoritative_inputs(brand, kit):
    return [evidence for record, path in authoritative_inputs(brand, kit) for evidence in [analyze_input(record, path)] if evidence is not None]


def _token_value(brand, token):
    value = brand
    for part in token.split("."):
        _require(isinstance(value, dict) and part in value, "palette approval names an unknown canonical token: %s" % token)
        value = value[part]
    return value


def validate_palette_approvals(brand, evidence):
    approvals = brand.get("palette_approvals", [])
    _require(isinstance(approvals, list), "palette_approvals must be an array")
    evidence_by_id = {item["input_id"]: item for item in evidence}
    used_tokens = set()
    for index, approval in enumerate(approvals):
        required = {"input_id", "source_sha256", "selected_candidate", "canonical_tokens", "approved_by", "approved_on"}
        _require(isinstance(approval, dict) and set(approval) == required, "palette approval %d must contain exactly the required fields" % index)
        item = evidence_by_id.get(approval["input_id"])
        _require(item is not None, "palette approval %d references input without current analysis evidence" % index)
        _require(approval["source_sha256"] == item["source_sha256"], "palette approval %d is stale because the source hash changed" % index)
        selected = approval["selected_candidate"].upper()
        _require(HEX.fullmatch(selected), "palette approval %d has an invalid selected color" % index)
        _require(selected in {candidate["hex"] for candidate in item["candidates"]}, "palette approval %d selects a color absent from current evidence" % index)
        tokens = approval["canonical_tokens"]
        _require(isinstance(tokens, list) and tokens and len(tokens) == len(set(tokens)), "palette approval %d needs unique canonical tokens" % index)
        for token in tokens:
            _require(token not in used_tokens, "canonical token is approved more than once: %s" % token)
            used_tokens.add(token)
            current = _token_value(brand, token)
            _require(isinstance(current, str) and current.upper() == selected, "palette approval %d does not match canonical token %s" % (index, token))
        _require(isinstance(approval["approved_by"], str) and approval["approved_by"].strip(), "palette approval %d lacks a human approver" % index)
        _require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", approval["approved_on"] or ""), "palette approval %d has an invalid approval date" % index)
    return approvals


def validate_brand(brand, kit):
    _require(isinstance(brand.get("slug"), str) and ID.fullmatch(brand["slug"]), "brand slug is missing or invalid")
    aff = affiliation(brand)
    if aff["inheritance"] == "independent":
        colors = brand.get("semantic_colors")
        _require(isinstance(colors, dict) and set(colors) == {"emphasis", "action"}, "independent inheritance requires semantic_colors.emphasis and semantic_colors.action")
        _require(all(isinstance(value, str) and HEX.fullmatch(value) for value in colors.values()), "independent semantic colors must be six-digit hex values")
    validate_typography(brand, kit)
    application_icon_profile(brand)
    evidence = analyze_authoritative_inputs(brand, kit)
    validate_palette_approvals(brand, evidence)
    return evidence


def validate_brand_file(path):
    path = Path(path).resolve()
    brand = load_brand(path)
    return brand, validate_brand(brand, path.parent)


def scan_affiliation_output(brand, kit):
    aff = affiliation(brand)
    if aff["ownership"] != THIRD_PARTY:
        return []
    problems = []
    root = Path(kit).resolve()
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if PROJECT_ENDORSEMENT.lower() in text.lower():
            problems.append("%s contains the owned-project endorsement" % path.relative_to(root).as_posix())
        if aff["service_credit"] == "none" and SERVICE_CREDIT.lower() in text.lower():
            problems.append("%s contains an undeclared ShruggieTech service credit" % path.relative_to(root).as_posix())
        if re.search(r'"parent"\s*:\s*"ShruggieTech"', text, re.I):
            problems.append("%s contains false ShruggieTech parentage" % path.relative_to(root).as_posix())
    return problems
