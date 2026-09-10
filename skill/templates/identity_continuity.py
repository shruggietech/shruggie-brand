#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Source-bound identity approval, proof comparison, and drift validation."""

from __future__ import annotations

import ast
import hashlib
import json
import math
import os
import re
from collections import Counter
from pathlib import Path


PROOF_SIZES = (256, 64, 32, 16)
PROOF_SURFACES = ("dark", "light", "black", "white")
PROOF_VARIANTS = ("full", "reduced")
REQUIRED_APPROVAL_SCOPE = (
    "full-master", "reduced-master", "palette", "framing", "topology", "renderer", "proof-matrix",
)
SOURCE_CLASSES = {"glyphkit-constructed", "legacy-constructed", "authoritative"}
RECORD_STATUSES = {"approved-canonical", "historical-baseline"}
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")
IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PATH_LITERAL = re.compile(r"^\s*[Mm]\s*-?(?:\d|\.)")
ALLOWED_GLYPHKIT_PRIMITIVES = {
    "arc", "ring_band", "ring", "wedge", "disc", "rect", "rounded_rect", "capsule", "polygon",
    "translate", "scale", "center_ink",
}
PALETTE_CHECKS = {
    "contrast", "sibling_separation", "color_vision", "semantic_roles", "surfaces", "single_ink",
    "rendered_color",
}
LIFECYCLE_TRANSITIONS = {
    "exploratory": {"direction-selected", "discarded"},
    "direction-selected": {"canonical-candidate", "discarded"},
    "canonical-candidate": {"canonical-approved", "direction-selected"},
    "canonical-approved": {"promoted", "invalidated"},
    "promoted": {"derivative-approved", "invalidated"},
    "derivative-approved": {"publication-eligible", "invalidated"},
    "publication-eligible": {"invalidated"},
    "historical-baseline": {"invalidated"},
    "invalidated": {"canonical-candidate"},
    "discarded": set(),
}
FRAMING_FIELDS = (
    "grid", "canvas_width", "canvas_height", "artwork_width", "artwork_height",
    "reduced_artwork_width", "reduced_artwork_height", "clear_space_units", "standalone_padding_units",
    "view_box", "crop",
)
PALETTE_FIELDS = (
    "accent", "semantic_colors", "surfaces", "chart_palette", "legacy_palette",
)


class ContinuityError(ValueError):
    """Raised when an identity continuity contract is absent, unsafe, or stale."""


def canonical_bytes(value):
    """Return deterministic UTF-8 JSON bytes, or raw bytes unchanged."""
    if isinstance(value, bytes):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def record_digest(record):
    payload = dict(record)
    payload.pop("record_sha256", None)
    return canonical_digest(payload)


def _require(condition, message):
    if not condition:
        raise ContinuityError(message)


def safe_path(root, relative, required=True):
    """Resolve a forward-slash relative path without traversal or symlink hops."""
    _require(isinstance(relative, str) and relative, "path must be a non-empty string")
    _require(not os.path.isabs(relative), "absolute paths are not permitted: %s" % relative)
    _require("\\" not in relative, "paths must use forward slashes: %s" % relative)
    parts = Path(relative).parts
    _require(parts and all(part not in {"", ".", ".."} for part in parts),
             "path traversal is not permitted: %s" % relative)
    base = Path(root).resolve()
    cursor = base
    for part in parts:
        cursor = cursor / part
        _require(not cursor.is_symlink(), "symbolic-link paths are not permitted: %s" % relative)
    resolved = cursor.resolve()
    try:
        resolved.relative_to(base)
    except ValueError as error:
        raise ContinuityError("path escapes approved root: %s" % relative) from error
    if required:
        _require(resolved.is_file(), "declared file is missing: %s" % relative)
    return resolved


def load_json(path):
    """Load UTF-8 JSON while rejecting duplicate object keys."""
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ContinuityError("duplicate JSON key: %s" % key)
            result[key] = value
        return result

    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle, object_pairs_hook=unique_pairs)
    except ContinuityError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ContinuityError("identity continuity JSON is invalid: %s" % error) from error


def _path_topology(entries):
    entries = entries or []
    role_counts = Counter()
    commands = Counter()
    subpaths = 0
    closed = 0
    fill_rules = Counter()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        role_counts[str(entry.get("role", ""))] += 1
        data = entry.get("d", "")
        letters = re.findall(r"[A-Za-z]", data) if isinstance(data, str) else []
        commands.update(letter.upper() for letter in letters if letter.upper() in set("MLCQAHVSTZ"))
        subpaths += sum(1 for letter in letters if letter.upper() == "M")
        closed += sum(1 for letter in letters if letter.upper() == "Z")
        fill_rules[str(entry.get("fill_rule", "nonzero"))] += 1
    return {
        "path_count": len(entries),
        "subpath_count": subpaths,
        "closed_subpaths": closed,
        "role_counts": dict(sorted(role_counts.items())),
        "command_counts": dict(sorted(commands.items())),
        "fill_rules": dict(sorted(fill_rules.items())),
    }


def identity_snapshot(brand, source_class):
    """Create the exact governed identity snapshot without self-referential record data."""
    _require(source_class in SOURCE_CLASSES, "unsupported identity source class: %r" % source_class)
    logo = brand.get("logo") or {}
    paths = logo.get("paths") or {}
    framing = {key: logo.get(key) for key in FRAMING_FIELDS if key in logo}
    palette = {key: brand.get(key) for key in PALETTE_FIELDS if key in brand}
    palette["logo_role_colors"] = logo.get("role_colors")
    topology = {variant: _path_topology(paths.get(variant)) for variant in PROOF_VARIANTS}
    geometry = {
        "source_mode": logo.get("source_mode"),
        "geometry_provenance": logo.get("geometry_provenance"),
        "paths": {variant: paths.get(variant) for variant in PROOF_VARIANTS},
        "authoritative_input_ids": logo.get("authoritative_input_ids"),
    }
    typography = {"wordmark_text": brand.get("wordmark_text"), "typography": brand.get("typography")}
    governed = {
        "source_class": source_class,
        "geometry": geometry,
        "topology": topology,
        "framing": framing,
        "palette": palette,
        "typography": typography,
    }
    governed["sha256"] = canonical_digest(governed)
    return governed


def validate_lifecycle_transition(current, target):
    _require(current in LIFECYCLE_TRANSITIONS, "unknown approval state: %s" % current)
    _require(target in LIFECYCLE_TRANSITIONS[current], "invalid approval transition: %s -> %s" % (current, target))
    return True


def validate_glyphkit_helper(path):
    """Inspect a construction helper without executing it."""
    helper = Path(path)
    _require(helper.is_file() and not helper.is_symlink(), "glyphkit construction helper is missing or unsafe")
    try:
        source = helper.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(helper))
    except (OSError, UnicodeError, SyntaxError) as error:
        raise ContinuityError("glyphkit construction helper is invalid: %s" % error) from error

    aliases = set()
    primitive_calls = set()
    forbidden_calls = set()
    forbidden_names = {"eval", "exec", "compile", "__import__"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for item in node.names:
                if item.name == "glyphkit":
                    aliases.add(item.asname or "glyphkit")
        elif isinstance(node, ast.ImportFrom) and node.module == "glyphkit":
            for item in node.names:
                if item.name in ALLOWED_GLYPHKIT_PRIMITIVES:
                    aliases.add(item.asname or item.name)
        elif isinstance(node, ast.Constant):
            value = node.value
            if isinstance(value, str) and PATH_LITERAL.match(value):
                raise ContinuityError("glyphkit construction helper contains literal SVG path data")
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in forbidden_names:
                    forbidden_calls.add(node.func.id)
                if node.func.id in aliases and node.func.id in ALLOWED_GLYPHKIT_PRIMITIVES:
                    primitive_calls.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id in aliases:
                    if node.func.attr in ALLOWED_GLYPHKIT_PRIMITIVES:
                        primitive_calls.add(node.func.attr)
                    elif node.func.attr not in {"fmt", "bbox", "flatten", "path_commands_ok"}:
                        forbidden_calls.add(node.func.attr)
                if node.func.attr in {"system", "popen", "run", "Popen"}:
                    forbidden_calls.add(node.func.attr)
    _require(aliases, "construction helper must import glyphkit")
    _require(primitive_calls, "construction helper must call an approved glyphkit primitive")
    _require(not forbidden_calls, "construction helper uses forbidden calls: %s" % ", ".join(sorted(forbidden_calls)))
    return {"engine": "glyphkit", "primitives": sorted(primitive_calls), "source_sha256": canonical_digest(helper.read_bytes())}


def validate_palette_qualification(value):
    _require(isinstance(value, dict), "palette qualification is required")
    required = {"status", "srgb_roles", "oklch_roles", "checks", "evidence_sha256"}
    _require(set(value) == required, "palette qualification must contain exactly the required fields")
    _require(value["status"] == "passed", "palette qualification must pass before canonical approval")
    roles = value["srgb_roles"]
    oklch = value["oklch_roles"]
    _require(isinstance(roles, dict) and roles, "palette qualification needs sRGB roles")
    _require(isinstance(oklch, dict) and set(oklch) == set(roles), "OKLCH roles must match sRGB roles")
    for role, color in roles.items():
        _require(isinstance(role, str) and role and isinstance(color, str) and HEX.fullmatch(color),
                 "palette qualification contains an invalid sRGB role")
        triplet = oklch[role]
        _require(isinstance(triplet, list) and len(triplet) == 3 and all(isinstance(item, (int, float)) for item in triplet),
                 "palette qualification contains an invalid OKLCH role")
        lightness, chroma, hue = triplet
        _require(0 <= lightness <= 1 and chroma >= 0 and 0 <= hue <= 360,
                 "palette qualification contains an out-of-range OKLCH role")
    checks = value["checks"]
    _require(isinstance(checks, dict) and set(checks) == PALETTE_CHECKS,
             "palette qualification checks are incomplete")
    _require(all(item is True for item in checks.values()), "every palette qualification check must pass")
    expected = dict(value)
    expected.pop("evidence_sha256")
    _require(isinstance(value["evidence_sha256"], str) and DIGEST.fullmatch(value["evidence_sha256"] or ""),
             "palette qualification evidence SHA-256 is invalid")
    _require(value["evidence_sha256"] == canonical_digest(expected), "palette qualification evidence is stale")
    return value


def _validate_source_files(root, records):
    _require(isinstance(records, list), "source_files must be an array")
    seen = set()
    for index, item in enumerate(records):
        _require(isinstance(item, dict), "source file %d must be an object" % index)
        _require(set(item) == {"path", "purpose", "bytes", "sha256"},
                 "source file %d has unsupported or missing fields" % index)
        relative = item["path"]
        _require(relative not in seen, "duplicate source file path: %s" % relative)
        seen.add(relative)
        path = safe_path(root, relative)
        _require(isinstance(item["purpose"], str) and item["purpose"].strip(), "source file purpose is required")
        _require(isinstance(item["bytes"], int) and item["bytes"] >= 0 and path.stat().st_size == item["bytes"],
                 "source file byte count drift: %s" % relative)
        _require(isinstance(item["sha256"], str) and DIGEST.fullmatch(item["sha256"] or ""),
                 "source file SHA-256 is invalid: %s" % relative)
        _require(canonical_digest(path.read_bytes()) == item["sha256"], "source file hash drift: %s" % relative)


def _validate_approval(record, root):
    approval = record.get("approval")
    _require(isinstance(approval, dict), "approved-canonical record needs owner approval")
    required = {"bundle_id", "approved_by", "approved_on", "owner_wording", "scope", "proposal_sha256", "source_snapshot_sha256"}
    _require(set(approval) == required, "canonical approval has unsupported or missing fields")
    _require(IDENTIFIER.fullmatch(approval["bundle_id"] or ""), "canonical approval bundle id is invalid")
    _require(isinstance(approval["approved_by"], str) and approval["approved_by"].strip(), "canonical approval needs a human approver")
    _require(DATE.fullmatch(approval["approved_on"] or ""), "canonical approval date is invalid")
    _require(isinstance(approval["owner_wording"], str) and approval["owner_wording"].strip(), "canonical approval needs exact owner wording")
    _require(isinstance(approval["scope"], list) and set(approval["scope"]) == set(REQUIRED_APPROVAL_SCOPE),
             "canonical approval scope is incomplete")
    for key in ("proposal_sha256", "source_snapshot_sha256"):
        _require(isinstance(approval[key], str) and DIGEST.fullmatch(approval[key] or ""),
                 "canonical approval %s is invalid" % key)
    _require(approval["source_snapshot_sha256"] == record["identity_snapshot"]["sha256"],
             "canonical approval is stale because the source snapshot changed")
    validate_palette_qualification(record.get("palette_qualification"))
    renderer = record.get("renderer")
    _require(isinstance(renderer, dict) and set(renderer) == {"id", "version", "settings_sha256"},
             "canonical approval needs deterministic renderer identity")
    _require(all(isinstance(renderer[key], str) and renderer[key].strip() for key in ("id", "version")),
             "renderer identity and version are required")
    _require(DIGEST.fullmatch(renderer["settings_sha256"] or ""), "renderer settings SHA-256 is invalid")
    proofs = record.get("proofs")
    _require(isinstance(proofs, list) and len(proofs) == 32, "canonical approval needs the complete 32-proof matrix")
    expected = {(variant, size, surface) for variant in PROOF_VARIANTS for size in PROOF_SIZES for surface in PROOF_SURFACES}
    actual = set()
    for item in proofs:
        _require(isinstance(item, dict) and set(item) == {"variant", "size_px", "surface", "path", "sha256"},
                 "canonical proof record has unsupported or missing fields")
        coordinate = (item["variant"], item["size_px"], item["surface"])
        _require(coordinate not in actual, "duplicate canonical proof coordinate")
        actual.add(coordinate)
        path = safe_path(root, item["path"])
        _require(DIGEST.fullmatch(item["sha256"] or "") and canonical_digest(path.read_bytes()) == item["sha256"],
                 "canonical proof hash drift: %s" % item["path"])
        try:
            from PIL import Image

            with Image.open(path) as image:
                _require(image.format == "PNG", "canonical proof must be a PNG: %s" % item["path"])
                _require(image.size == (item["size_px"], item["size_px"]),
                         "canonical proof dimensions do not match its coordinate: %s" % item["path"])
                image.verify()
        except ContinuityError:
            raise
        except Exception as exc:
            raise ContinuityError("canonical proof is not a valid PNG: %s (%s)" % (item["path"], exc)) from exc
    _require(actual == expected, "canonical proof matrix is incomplete")


def validate_record(brand, root, record):
    """Validate one committed or provisional identity continuity record."""
    required = {
        "schema_version", "brand", "status", "source_class", "recorded_on", "source_revision", "source_files",
        "identity_snapshot", "topology", "framing", "palette", "renderer", "proofs", "approval",
        "historical_evidence", "record_sha256",
    }
    optional = {"palette_qualification"}
    _require(isinstance(record, dict) and required.issubset(set(record)) and set(record).issubset(required | optional),
             "identity continuity record has unsupported or missing fields")
    _require(record["schema_version"] == 1, "identity continuity schema_version must be 1")
    _require(record["brand"] == brand.get("slug") and IDENTIFIER.fullmatch(record["brand"] or ""),
             "identity continuity brand does not match source")
    _require(record["status"] in RECORD_STATUSES, "unsupported identity continuity status")
    _require(record["source_class"] in SOURCE_CLASSES, "unsupported identity continuity source class")
    _require(DATE.fullmatch(record["recorded_on"] or ""), "identity continuity date is invalid")
    _require(isinstance(record["source_revision"], str) and record["source_revision"].strip(), "source revision is required")
    _require(isinstance(record["record_sha256"], str) and DIGEST.fullmatch(record["record_sha256"] or ""),
             "identity continuity record SHA-256 is invalid")
    _require(record["record_sha256"] == record_digest(record), "identity continuity record is stale")
    _validate_source_files(root, record["source_files"])
    expected = identity_snapshot(brand, record["source_class"])
    _require(record["identity_snapshot"] == expected, "identity continuity source snapshot drift")
    _require(record["topology"] == expected["topology"], "identity continuity topology drift")
    _require(record["framing"] == expected["framing"], "identity continuity framing drift")
    _require(record["palette"] == expected["palette"], "identity continuity palette drift")

    mode = (brand.get("logo") or {}).get("source_mode")
    if record["source_class"] == "authoritative":
        _require(mode == "authoritative", "authoritative continuity requires authoritative logo mode")
        _require(not (Path(root) / "build" / "mk_paths.py").exists(), "authoritative identity cannot have a construction helper")
    else:
        _require(mode == "constructed", "constructed continuity requires constructed logo mode")
    if record["source_class"] == "glyphkit-constructed":
        validate_glyphkit_helper(Path(root) / "build" / "mk_paths.py")
    if record["source_class"] == "legacy-constructed":
        _require(record["status"] == "historical-baseline", "legacy construction cannot receive new canonical approval")

    if record["status"] == "historical-baseline":
        _require(record["approval"] is None and record["renderer"] is None and record["proofs"] == [],
                 "historical baseline cannot claim canonical approval or proofs")
        _require(record.get("palette_qualification") in (None, {}), "historical baseline cannot claim new palette qualification")
        evidence = record["historical_evidence"]
        required_evidence = {"basis", "baseline_revision", "approval_completeness", "limitation", "migration_issue"}
        _require(isinstance(evidence, dict) and set(evidence) == required_evidence,
                 "historical baseline evidence is incomplete")
        _require(evidence["basis"] == "current-authoritative-source" and evidence["migration_issue"] == 185,
                 "historical baseline basis is invalid")
        _require(evidence["baseline_revision"] == record["source_revision"], "historical baseline revision is inconsistent")
        _require(evidence["approval_completeness"] in {"complete", "partial", "unknown"},
                 "historical approval completeness is invalid")
        _require(isinstance(evidence["limitation"], str) and "not" in evidence["limitation"].lower(),
                 "historical baseline must deny retrospective approval")
    else:
        _require(record["historical_evidence"] is None, "approved canonical record cannot use historical evidence")
        _validate_approval(record, root)
    return {"brand": record["brand"], "status": record["status"], "source_class": record["source_class"],
            "snapshot_sha256": expected["sha256"], "record_sha256": record["record_sha256"]}


def validate_brand_continuity(brand, root):
    reference = brand.get("identity_continuity")
    _require(isinstance(reference, dict) and set(reference) == {"record", "status"},
             "identity_continuity must contain exactly record and status")
    _require(reference["status"] in RECORD_STATUSES, "identity_continuity status is invalid")
    path = safe_path(root, reference["record"])
    record = load_json(path)
    _require(record.get("status") == reference["status"], "identity continuity reference status drift")
    return validate_record(brand, root, record)


def continuity_report(brand, root):
    """Measure the committed continuity source and bind the result to its bytes."""
    result = validate_brand_continuity(brand, root)
    record_path = safe_path(root, brand["identity_continuity"]["record"])
    report = {
        "schema_version": 1,
        "brand": brand["slug"],
        "status": result["status"],
        "source_class": result["source_class"],
        "record_path": brand["identity_continuity"]["record"],
        "record_file_sha256": canonical_digest(record_path.read_bytes()),
        "record_sha256": result["record_sha256"],
        "snapshot_sha256": result["snapshot_sha256"],
        "validation": "passed",
    }
    report["report_sha256"] = canonical_digest(report)
    return report


def write_continuity_report(brand, root, output=None):
    report = continuity_report(brand, root)
    path = Path(output) if output else Path(root) / "identity-continuity-report.json"
    with open(str(path), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


def validate_continuity_report(brand, root):
    path = safe_path(root, "identity-continuity-report.json")
    report = load_json(path)
    expected = continuity_report(brand, root)
    _require(report == expected, "generated identity continuity report is absent or stale")
    return report


def _mask(image):
    rgba = image.convert("RGBA")
    width, height = rgba.size
    pixels = rgba.load()
    alphas = [pixels[x, y][3] for y in range(height) for x in range(width)]
    if min(alphas) < max(alphas):
        return {(x, y) for y in range(height) for x in range(width) if pixels[x, y][3] >= 128}
    background = pixels[0, 0][:3]
    return {(x, y) for y in range(height) for x in range(width)
            if max(abs(pixels[x, y][i] - background[i]) for i in range(3)) >= 8}


def _components(mask, width, height, foreground=True):
    universe = {(x, y) for y in range(height) for x in range(width)}
    points = set(mask if foreground else universe - mask)
    components = []
    while points:
        start = points.pop()
        queue = [start]
        group = {start}
        while queue:
            x, y = queue.pop()
            for point in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if point in points:
                    points.remove(point)
                    group.add(point)
                    queue.append(point)
        components.append(group)
    return components


def _topology(mask, width, height):
    components = len(_components(mask, width, height, True)) if mask else 0
    holes = 0
    for group in _components(mask, width, height, False):
        if not any(x in {0, width - 1} or y in {0, height - 1} for x, y in group):
            holes += 1
    return {"components": components, "holes": holes}


def _edge_band(mask, width, height, radius=1):
    edges = set()
    for x, y in mask:
        if any((nx, ny) not in mask for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))):
            edges.add((x, y))
    for y in range(height):
        for x in range(width):
            if (x, y) not in mask and any((nx, ny) in mask for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))):
                edges.add((x, y))
    band = set()
    for x, y in edges:
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                point = (x + dx, y + dy)
                if 0 <= point[0] < width and 0 <= point[1] < height:
                    band.add(point)
    return band


def _bounds(mask):
    if not mask:
        return None
    xs = [point[0] for point in mask]
    ys = [point[1] for point in mask]
    return [min(xs), min(ys), max(xs) + 1, max(ys) + 1]


def _centroid(mask):
    if not mask:
        return None
    return (sum(point[0] for point in mask) / float(len(mask)),
            sum(point[1] for point in mask) / float(len(mask)))


def _average_color(image, points):
    if not points:
        return None
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    return tuple(sum(pixels[x, y][channel] for x, y in points) / float(len(points)) for channel in range(3))


def _delta_e(left, right):
    if left is None or right is None:
        return float("inf")
    try:
        from coloraide import Color
        a = Color("srgb", [item / 255.0 for item in left])
        b = Color("srgb", [item / 255.0 for item in right])
        return float(a.delta_e(b, method="2000"))
    except ImportError:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right))) * 100.0 / (255.0 * math.sqrt(3.0))


def _write_evidence(approved, production, approved_mask, production_mask, output, prefix):
    from PIL import Image, ImageChops
    output.mkdir(parents=True, exist_ok=True)
    width, height = approved.size
    paths = {}
    side = Image.new("RGBA", (width * 2, height), (0, 0, 0, 0))
    side.alpha_composite(approved.convert("RGBA"), (0, 0))
    side.alpha_composite(production.convert("RGBA"), (width, 0))
    paths["side_by_side"] = output / (prefix + "-side-by-side.png")
    side.save(paths["side_by_side"])
    overlay = Image.blend(approved.convert("RGBA"), production.convert("RGBA"), 0.5)
    paths["overlay"] = output / (prefix + "-overlay.png")
    overlay.save(paths["overlay"])
    xor = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    xor_pixels = xor.load()
    for x, y in approved_mask ^ production_mask:
        xor_pixels[x, y] = (255, 0, 80, 255)
    paths["silhouette_xor"] = output / (prefix + "-silhouette-xor.png")
    xor.save(paths["silhouette_xor"])
    difference = ImageChops.difference(approved.convert("RGB"), production.convert("RGB")).convert("RGBA")
    paths["color_difference"] = output / (prefix + "-color-difference.png")
    difference.save(paths["color_difference"])
    return {key: value.name for key, value in paths.items()}


def compare_proofs(approved_path, production_path, same_renderer, evidence_dir=None, prefix="continuity"):
    """Compare two square PNG proofs under exact or edge-aware policy."""
    from PIL import Image
    approved_file = Path(approved_path)
    production_file = Path(production_path)
    with Image.open(approved_file) as source:
        _require(source.format == "PNG", "approved continuity proof must be a PNG")
        approved = source.convert("RGBA")
    with Image.open(production_file) as source:
        _require(source.format == "PNG", "production continuity proof must be a PNG")
        production = source.convert("RGBA")
    _require(approved.size == production.size, "continuity proofs must have identical dimensions")
    width, height = approved.size
    _require(width == height, "continuity proofs must be square")
    approved_mask = _mask(approved)
    production_mask = _mask(production)
    union = approved_mask | production_mask
    intersection = approved_mask & production_mask
    xor = approved_mask ^ production_mask
    edge_band = _edge_band(approved_mask, width, height) | _edge_band(production_mask, width, height)
    changed_outside = xor - edge_band
    approved_bbox = _bounds(approved_mask)
    production_bbox = _bounds(production_mask)
    if approved_bbox is None or production_bbox is None:
        bbox_delta = width + height
    else:
        bbox_delta = max(abs(left - right) for left, right in zip(approved_bbox, production_bbox))
    approved_centroid = _centroid(approved_mask)
    production_centroid = _centroid(production_mask)
    if approved_centroid is None or production_centroid is None:
        centroid_delta = float("inf")
    else:
        centroid_delta = math.hypot(approved_centroid[0] - production_centroid[0],
                                    approved_centroid[1] - production_centroid[1])
    interior = intersection - edge_band
    delta_e = _delta_e(_average_color(approved, interior), _average_color(production, interior))
    approved_topology = _topology(approved_mask, width, height)
    production_topology = _topology(production_mask, width, height)
    exact = canonical_digest(approved_file.read_bytes()) == canonical_digest(production_file.read_bytes())
    changed_fraction = len(changed_outside) / float(max(1, len(union)))
    iou = len(intersection) / float(max(1, len(union)))
    if same_renderer:
        passes = exact
    else:
        passes = (approved_topology == production_topology and changed_fraction <= 0.005 and
                  bbox_delta <= 1 and centroid_delta <= 1.0 and delta_e <= 1.0)
    evidence_paths = {}
    if evidence_dir is not None:
        evidence_paths = _write_evidence(approved, production, approved_mask, production_mask,
                                         Path(evidence_dir), prefix)
    return {
        "passes": passes,
        "same_renderer": bool(same_renderer),
        "exact_sha256": exact,
        "approved_sha256": canonical_digest(approved_file.read_bytes()),
        "production_sha256": canonical_digest(production_file.read_bytes()),
        "approved_topology": approved_topology,
        "production_topology": production_topology,
        "silhouette_iou": round(iou, 6),
        "changed_outside_edge_fraction": round(changed_fraction, 6),
        "approved_bbox": approved_bbox,
        "production_bbox": production_bbox,
        "bbox_delta_max_px": bbox_delta,
        "centroid_delta_px": round(centroid_delta, 6) if math.isfinite(centroid_delta) else None,
        "interior_delta_e_2000": round(delta_e, 6) if math.isfinite(delta_e) else None,
        "evidence_paths": evidence_paths,
    }
