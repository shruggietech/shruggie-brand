#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renderer-neutral interface, routing, and consumer handover contracts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import zipfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
REFERENCES = SKILL_ROOT / "references"
INTERFACE_CANON = REFERENCES / "interface-canon.json"
BRAND_CANON = REFERENCES / "01-canon.json"
BEGIN_MARKER = "<!-- BEGIN SHRUGGIE-BRANDBUILDER: CONSUMER CONTRACT -->"
END_MARKER = "<!-- END SHRUGGIE-BRANDBUILDER: CONSUMER CONTRACT -->"
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
ROLE = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$")
REFERENCE = re.compile(r"^\$(primitive|alias|brand|brand_canon|resolved)\.([A-Za-z0-9_.-]+)$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
ZIP_TIME = (2026, 9, 17, 0, 0, 0)
GENERATED_DIRECTORIES = {"__pycache__", "node_modules", ".venv", "venv"}
BACKWARD_BRAND_DEFAULTS = {
    "surfaces.base": "#000000",
    "surfaces.card": "#111111",
    "surfaces.popover": "#0A0A0A",
    "accent.dim": "#9A9A9A",
}


class InterfaceContractError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise InterfaceContractError(message)


def _read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise InterfaceContractError("invalid UTF-8 JSON at %s: %s" % (path, error)) from error


def load_interface_canon(path=None):
    return _read_json(path or INTERFACE_CANON)


def load_brand_canon(path=None):
    return _read_json(path or BRAND_CANON)


def _lookup(value, dotted, label):
    current = value
    for part in dotted.split("."):
        if isinstance(current, list) and part.isdigit():
            index = int(part)
            _require(index < len(current), "%s path is missing: %s" % (label, dotted))
            current = current[index]
        else:
            _require(isinstance(current, dict) and part in current,
                     "%s path is missing: %s" % (label, dotted))
            current = current[part]
    return current


def _lookup_brand(brand, dotted):
    try:
        return _lookup(brand, dotted, "brand")
    except InterfaceContractError:
        if dotted in BACKWARD_BRAND_DEFAULTS:
            return BACKWARD_BRAND_DEFAULTS[dotted]
        raise


def _validate_alias_graph(canon):
    aliases = canon["aliases"]
    visiting = []
    complete = set()

    def visit(role):
        if role in complete:
            return
        if role in visiting:
            cycle = visiting[visiting.index(role):] + [role]
            raise InterfaceContractError("alias cycle: %s" % " -> ".join(cycle))
        visiting.append(role)
        match = REFERENCE.fullmatch(aliases[role])
        _require(match is not None, "alias %s has an invalid reference root" % role)
        if match.group(1) == "alias":
            target = match.group(2)
            _require(target in aliases, "alias %s targets unknown role %s" % (role, target))
            visit(target)
        visiting.pop()
        complete.add(role)

    for role in sorted(aliases):
        visit(role)


def validate_interface_canon(canon):
    required = {
        "$schema", "id", "kind", "version", "brand_canon_compatibility", "summary",
        "units", "primitives", "role_catalog", "required_roles", "aliases", "runtime",
        "invariants", "permitted_overrides", "state_pairs",
    }
    _require(isinstance(canon, dict) and set(canon) == required,
             "Interface Canon must contain exactly %s" % ", ".join(sorted(required)))
    _require(canon["id"] == "shruggie-interface-canon" and canon["kind"] == "interface-canon",
             "Interface Canon identity is invalid")
    _require(isinstance(canon["version"], str) and SEMVER.fullmatch(canon["version"]),
             "Interface Canon version must be semantic")
    compatibility = canon["brand_canon_compatibility"]
    _require(isinstance(compatibility, list) and compatibility and len(compatibility) == len(set(compatibility)),
             "brand_canon_compatibility must contain unique versions")
    _require(all(isinstance(item, str) and SEMVER.fullmatch(item) for item in compatibility),
             "brand_canon_compatibility contains an invalid version")
    units = canon["units"]
    _require(isinstance(units, dict) and units.get("logical_ui_unit") == "lu",
             "logical UI unit must be lu")
    transforms = units.get("transforms") or {}
    _require(set(transforms) >= {"web", "egui", "native"},
             "logical unit transforms must cover web, egui, and native")
    for name, transform in transforms.items():
        _require(isinstance(transform, dict) and isinstance(transform.get("factor"), (int, float))
                 and transform["factor"] > 0, "invalid logical unit transform: %s" % name)
    catalog = canon["role_catalog"]
    aliases = canon["aliases"]
    _require(isinstance(catalog, list) and catalog and len(catalog) == len(set(catalog)),
             "role_catalog must contain unique roles")
    _require(all(isinstance(role, str) and ROLE.fullmatch(role) for role in catalog),
             "role_catalog contains an invalid role")
    unknown = sorted(set(aliases) - set(catalog))
    _require(not unknown, "unknown role in aliases: %s" % ", ".join(unknown))
    required_roles = canon["required_roles"]
    _require(isinstance(required_roles, list) and required_roles,
             "required_roles must be a non-empty list")
    missing = sorted(set(required_roles) - set(aliases))
    _require(not missing, "missing required role: %s" % ", ".join(missing))
    absent = sorted(set(catalog) - set(aliases))
    _require(not absent, "catalog role lacks an alias: %s" % ", ".join(absent))
    _validate_alias_graph(canon)
    invariants = canon["invariants"]
    invariant_roles = invariants.get("roles") if isinstance(invariants, dict) else None
    _require(isinstance(invariant_roles, list) and set(invariant_roles).issubset(aliases),
             "invariant roles must reference declared aliases")
    overrides = canon["permitted_overrides"]
    _require(isinstance(overrides, dict), "permitted_overrides must be an object")
    for role, prefixes in overrides.items():
        _require(role in aliases, "override targets unknown role: %s" % role)
        _require(role not in invariant_roles, "invariant role cannot be overridden: %s" % role)
        _require(isinstance(prefixes, list) and prefixes and all(
            isinstance(prefix, str) and REFERENCE.match(prefix + "placeholder") for prefix in prefixes
        ), "override %s has an invalid allowed reference prefix" % role)
    pairs = canon["state_pairs"]
    _require(isinstance(pairs, list) and pairs, "state_pairs must be a non-empty list")
    identifiers = set()
    for pair in pairs:
        _require(isinstance(pair, dict) and set(pair) == {"id", "foreground", "background", "minimum_contrast"},
                 "state pair has invalid fields")
        _require(pair["id"] not in identifiers, "duplicate state pair: %s" % pair["id"])
        identifiers.add(pair["id"])
        _require(pair["foreground"] in aliases and pair["background"] in aliases,
                 "state pair %s references an unknown role" % pair["id"])
        _require(isinstance(pair["minimum_contrast"], (int, float)) and pair["minimum_contrast"] >= 3,
                 "state pair %s has an invalid contrast floor" % pair["id"])
    runtime = canon["runtime"]
    expected_runtime = {"required_inputs", "window_classes", "pointer_precisions", "themes", "mixed_profile_examples"}
    _require(isinstance(runtime, dict) and set(runtime) == expected_runtime,
             "runtime contract fields are invalid")
    _require("operating_system" not in runtime["required_inputs"],
             "runtime inputs cannot include an operating-system name")
    for profile in runtime["mixed_profile_examples"]:
        _validate_runtime_profile(profile, canon)
    return canon


def _rect(value, label, nullable=False, kind=False):
    if nullable and value is None:
        return
    required = {"x", "y", "width", "height"} | ({"kind"} if kind else set())
    _require(isinstance(value, dict) and set(value) == required, "%s has invalid fields" % label)
    for key in ("x", "y", "width", "height"):
        _require(isinstance(value[key], (int, float)), "%s.%s must be numeric" % (label, key))
    _require(value["width"] >= 0 and value["height"] >= 0,
             "%s dimensions cannot be negative" % label)
    if kind:
        _require(value["kind"] in {"drag", "controls", "reserved"},
                 "%s.kind is invalid" % label)


def _validate_runtime_profile(profile, canon):
    required = set(canon["runtime"]["required_inputs"])
    _require(isinstance(profile, dict), "runtime profile must be an object")
    if "operating_system" in profile or "os" in profile:
        raise InterfaceContractError("runtime profile cannot infer capabilities from an operating-system name")
    _require(set(profile) == required,
             "runtime profile must contain exactly %s" % ", ".join(sorted(required)))
    viewport = profile["viewport"]
    _require(isinstance(viewport, dict) and set(viewport) == {"width", "height"}
             and all(isinstance(viewport[key], (int, float)) and viewport[key] > 0 for key in viewport),
             "runtime viewport must have positive logical width and height")
    safe = profile["safe_area"]
    _require(isinstance(safe, dict) and set(safe) == {"top", "right", "bottom", "left"}
             and all(isinstance(safe[key], (int, float)) and safe[key] >= 0 for key in safe),
             "runtime safe_area must contain non-negative logical insets")
    _require(profile["window_class"] in canon["runtime"]["window_classes"], "unsupported window_class")
    _require(profile["pointer_precision"] in canon["runtime"]["pointer_precisions"], "unsupported pointer_precision")
    for key in ("hover", "hardware_keyboard", "touch", "reduced_motion", "forced_colors"):
        _require(isinstance(profile[key], bool), "runtime %s must be boolean" % key)
    _require(isinstance(profile["text_scale"], (int, float)) and profile["text_scale"] > 0,
             "runtime text_scale must be positive")
    _require(profile["theme"] in canon["runtime"]["themes"], "unsupported runtime theme")
    _rect(profile["ime_obstruction"], "ime_obstruction", nullable=True)
    _require(isinstance(profile["titlebar_regions"], list), "titlebar_regions must be a list")
    for index, region in enumerate(profile["titlebar_regions"]):
        _rect(region, "titlebar_regions[%d]" % index, kind=True)
    return profile


def validate_runtime_profile(profile, canon=None):
    canon = canon or load_interface_canon()
    validate_interface_canon(canon)
    return _validate_runtime_profile(profile, canon)


def _legal_foreground(fill):
    from coloraide import Color

    black = Color("#000000").contrast(fill, method="wcag21")
    white = Color("#FFFFFF").contrast(fill, method="wcag21")
    return "#000000" if black >= white else "#FFFFFF"


def resolve_interface_contract(brand, canon=None, brand_canon=None):
    canon = validate_interface_canon(canon or load_interface_canon())
    brand_canon = brand_canon or load_brand_canon()
    brand_canon_version = brand.get("canon") or brand_canon.get("version")
    _require(brand_canon_version in canon["brand_canon_compatibility"],
             "Brand Canon %s is not compatible with Interface Canon %s" % (brand_canon_version, canon["version"]))
    interface = brand.get("interface") or {}
    _require(isinstance(interface, dict) and set(interface).issubset({"canon", "overrides"}),
             "brand interface declaration has unsupported fields")
    if "canon" in interface:
        _require(interface["canon"] == canon["version"],
                 "brand interface canon %s does not match %s" % (interface["canon"], canon["version"]))
    overrides = interface.get("overrides") or {}
    _require(isinstance(overrides, dict), "brand interface overrides must be an object")
    aliases = dict(canon["aliases"])
    inheritance = ((brand.get("affiliation") or {}).get("inheritance"))
    for role, reference in overrides.items():
        _require(role in canon["permitted_overrides"], "unsupported override role: %s" % role)
        _require(isinstance(reference, str) and any(
            reference.startswith(prefix) for prefix in canon["permitted_overrides"][role]
        ), "unsupported override reference for %s" % role)
        if inheritance == "independent" and reference.startswith("$brand_canon.color.immutable.orange"):
            raise InterfaceContractError("override %s crosses affiliation boundary into house orange" % role)
        aliases[role] = reference
    if inheritance == "shruggietech-house":
        immutable = brand_canon["color"]["immutable"]
        semantic = {"action": immutable["orange-cta"]["hex"], "emphasis": immutable["orange"]["hex"]}
    else:
        colors = brand.get("semantic_colors") or {}
        _require(set(colors) == {"action", "emphasis"},
                 "independent brand lacks semantic action and emphasis colors")
        semantic = colors
    accent = _lookup(brand, "accent.bright", "brand")
    resolved_context = {
        "action": semantic["action"],
        "emphasis": semantic["emphasis"],
        "action_foreground": _legal_foreground(semantic["action"]),
        "accent_foreground": _legal_foreground(accent),
    }
    resolved_roles = {}
    visiting = []

    def resolve(role):
        if role in resolved_roles:
            return resolved_roles[role]
        if role in visiting:
            raise InterfaceContractError("alias cycle while resolving %s" % role)
        visiting.append(role)
        reference = aliases[role]
        match = REFERENCE.fullmatch(reference)
        _require(match is not None, "alias %s has an invalid reference root" % role)
        root, dotted = match.groups()
        if root == "alias":
            _require(dotted in aliases, "alias %s targets unknown role %s" % (role, dotted))
            value = resolve(dotted)
        elif root == "primitive":
            value = _lookup(canon["primitives"], dotted, "primitive")
        elif root == "brand":
            value = _lookup_brand(brand, dotted)
        elif root == "brand_canon":
            value = _lookup(brand_canon, dotted, "Brand Canon")
        else:
            value = _lookup(resolved_context, dotted, "resolved context")
        visiting.pop()
        resolved_roles[role] = value
        return value

    for role in sorted(aliases):
        resolve(role)
    for pair in canon["state_pairs"]:
        from coloraide import Color

        foreground = resolved_roles[pair["foreground"]]
        background = resolved_roles[pair["background"]]
        try:
            ratio = Color(foreground).contrast(background, method="wcag21")
        except Exception as error:
            raise InterfaceContractError("state pair %s does not resolve to colors" % pair["id"]) from error
        _require(ratio + 1e-9 >= pair["minimum_contrast"],
                 "state pair %s contrast %.2f is below %.2f" % (pair["id"], ratio, pair["minimum_contrast"]))
    return {
        "interface_canon_version": canon["version"],
        "canon_version": brand_canon_version,
        "units": canon["units"],
        "runtime": canon["runtime"],
        "invariants": canon["invariants"],
        "roles": resolved_roles,
    }


ROUTING_SIGNALS = {
    "governed_source_change", "consumer_change", "assessment", "mutation_authorized",
    "remediation_authorized", "identity_redesign", "upstream_submission",
    "pinned_contract_present", "skill_present",
}


def route_operating_mode(signals):
    _require(isinstance(signals, dict) and set(signals) == ROUTING_SIGNALS,
             "routing signals must contain exactly %s" % ", ".join(sorted(ROUTING_SIGNALS)))
    _require(all(isinstance(value, bool) for value in signals.values()),
             "routing signals must be boolean")
    evidence = sorted(key for key, value in signals.items() if value)
    clarification = None
    mode = None
    if signals["upstream_submission"] and not signals["mutation_authorized"]:
        clarification = "Is submitting or changing the upstream record authorized for this task?"
    elif signals["identity_redesign"] and not signals["governed_source_change"]:
        clarification = "Is the requested identity redesign separately authorized as governed Author work?"
    elif signals["assessment"] and (signals["consumer_change"] or signals["governed_source_change"]) and not signals["remediation_authorized"]:
        clarification = "Should this remain a read-only audit, or is remediation separately authorized?"
    elif signals["governed_source_change"]:
        if signals["mutation_authorized"]:
            mode = "author"
        else:
            clarification = "Is modification of the governed BrandBuilder source authorized?"
    elif signals["consumer_change"]:
        if signals["mutation_authorized"]:
            mode = "implementation"
        else:
            clarification = "Is modification of the consumer repository authorized?"
    elif signals["assessment"]:
        mode = "audit"
    else:
        clarification = "Is this task changing governed source, applying a pinned contract, or auditing conformance?"
    return {
        "mode": mode,
        "evidence": evidence,
        "requires_clarification": clarification is not None,
        "clarification": clarification,
        "authority_preserved": True,
    }


def skill_metadata(path=None):
    path = Path(path or (SKILL_ROOT / "SKILL.md"))
    text = path.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", text, re.DOTALL)
    _require(frontmatter is not None, "%s lacks skill frontmatter" % path)
    block = re.search(r"^metadata:\s*$\n(?P<body>(?:^[ \t]+.*(?:\n|\Z))+)",
                      frontmatter.group("body"), re.MULTILINE)
    _require(block is not None, "%s lacks skill metadata" % path)
    values = {}
    for output, key in (("version", "version"), ("canon", "canon"), ("interface_canon", "interface-canon")):
        match = re.search(r"^\s+%s:\s*([^\s#]+)\s*$" % key, block.group("body"), re.MULTILINE)
        _require(match is not None, "%s metadata lacks %s" % (path, key))
        values[output] = match.group(1).strip("\"'")
    return values


def merge_governed_block(existing, block):
    _require(block.count(BEGIN_MARKER) == 1 and block.count(END_MARKER) == 1
             and block.index(BEGIN_MARKER) < block.index(END_MARKER),
             "new governed block has invalid markers")
    begins = existing.count(BEGIN_MARKER)
    ends = existing.count(END_MARKER)
    if begins == 0 and ends == 0:
        separator = "" if not existing else ("\n" if existing.endswith("\n") else "\n\n")
        if existing and existing.endswith("\n") and not existing.endswith("\n\n"):
            separator = "\n"
        return existing + separator + block.rstrip("\n") + "\n"
    _require(begins == 1 and ends == 1, "existing governed block has malformed or duplicate markers")
    start = existing.index(BEGIN_MARKER)
    end = existing.index(END_MARKER)
    _require(start < end, "existing governed block has reversed markers")
    end += len(END_MARKER)
    return existing[:start] + block.rstrip("\n") + existing[end:]


def _zip_add(archive, name, data):
    info = zipfile.ZipInfo(name, ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data)


def write_deterministic_skill_bundle(destination, skill_root=None):
    skill_root = Path(skill_root or SKILL_ROOT).resolve()
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(destination), "w") as archive:
        for path in sorted(item for item in skill_root.rglob("*") if item.is_file()):
            relative = path.relative_to(skill_root).as_posix()
            if GENERATED_DIRECTORIES.intersection(path.relative_to(skill_root).parts) or path.suffix == ".pyc":
                continue
            _zip_add(archive, relative, path.read_bytes())
    return hashlib.sha256(destination.read_bytes()).hexdigest()


def _write_text(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value.rstrip("\n") + "\n")


def _write_exact_text(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(value)


def _write_json(path, value):
    _write_text(path, json.dumps(value, indent=2, ensure_ascii=False))


def _provenance(path, kit):
    path = Path(path)
    payload = path.read_bytes()
    return {
        "path": path.relative_to(kit).as_posix(),
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def _governed_block(brand, versions, recovery_path, recovery_sha):
    affiliation = brand.get("affiliation") or {}
    boundary = brand.get("vendor_boundary") or {}
    if boundary.get("notice"):
        affiliation_line = "Affiliation boundary: %s" % boundary["notice"]
    elif affiliation.get("parent"):
        affiliation_line = "Affiliation boundary: this is a ShruggieTech-owned child brand with declared parent `%s`." % affiliation["parent"]
    else:
        affiliation_line = "Affiliation boundary: this identity has no inferred ShruggieTech parent or endorsement."
    return """{begin}
## Governed BrandBuilder contract

BrandBuilder is mandatory for brand-system authoring, consumer implementation, and conformance audit. This kit pins Brand Canon `{canon}`, Interface Canon `{interface}`, compiler `{compiler}`, and brand `{brand_version}`.

Read `consumer-contract.json`, then `IMPLEMENTATION.md`. The pinned contract outranks screenshots, legacy stylesheets, and inferred local values. Do not reinterpret identity or create a permanent parallel design system.

{affiliation}

If BrandBuilder `{compiler}` is absent, verify SHA-256 `{sha}` and recover from `{recovery}`. Never substitute another version. Run `python3 build/verify.py .` and `python3 build/validate_glyph.py brand.json`; both must report zero failures.
{end}""".format(
        begin=BEGIN_MARKER, end=END_MARKER, canon=versions["canon_version"],
        interface=versions["interface_canon_version"], compiler=versions["compiler_version"],
        brand_version=versions["brand_version"], sha=recovery_sha, recovery=recovery_path,
        affiliation=affiliation_line,
    )


def emit_consumer_contract(brand, brand_source, kit, implementation_text):
    kit = Path(kit).resolve()
    brand_source = Path(brand_source).resolve()
    try:
        brand_source.relative_to(kit)
    except ValueError as error:
        raise InterfaceContractError("consumer brand source must be inside the generated kit") from error
    resolved = resolve_interface_contract(brand)
    metadata = skill_metadata()
    _require(metadata["canon"] == resolved["canon_version"],
             "skill Brand Canon metadata does not match the resolved brand")
    _require(metadata["interface_canon"] == resolved["interface_canon_version"],
             "skill Interface Canon metadata does not match the resolved contract")
    enforcement = kit / "enforcement"
    enforcement.mkdir(parents=True, exist_ok=True)
    copied = {
        "interface-canon.json": REFERENCES / "interface-canon.json",
        "interface-canon.schema.json": REFERENCES / "interface-canon.schema.json",
        "consumer-contract.schema.json": REFERENCES / "consumer-contract.schema.json",
    }
    for name, source in copied.items():
        (enforcement / name).write_bytes(source.read_bytes())
    _write_text(enforcement / "IMPLEMENTATION.md", implementation_text)
    distribution_name = "shruggie-brandbuilder-%s.skill" % metadata["version"]
    distribution = enforcement / "distributions" / distribution_name
    recovery_sha = write_deterministic_skill_bundle(distribution)
    versions = {
        "canon_version": resolved["canon_version"],
        "interface_canon_version": resolved["interface_canon_version"],
        "compiler_version": metadata["version"],
        "brand_version": brand.get("version", "1.0.0"),
    }
    gap = {
        "schema_version": 1,
        "consumer": {"brand": brand["slug"], "brand_version": versions["brand_version"]},
        "environment": {"renderer": "renderer-neutral", "host": "none"},
        "requirement": "Describe the reproducible consumer need.",
        "shared_concept": "Name the missing or insufficient shared semantic concept.",
        "evidence": [],
        "classification": "reusable-capability",
        "upstream_resolution": None,
        "adopted_version": None,
        "submission_authorized": False,
    }
    gap_path = enforcement / "capability-gap.example.json"
    _write_json(gap_path, gap)
    recovery_path = distribution.relative_to(kit).as_posix()
    block = _governed_block(brand, versions, recovery_path, recovery_sha)
    agents_path = enforcement / "AGENTS.md"
    existing = agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    merged = merge_governed_block(existing, block)
    _write_exact_text(agents_path, merged)
    provenance_paths = [
        brand_source,
        agents_path,
        enforcement / "IMPLEMENTATION.md",
        enforcement / "interface-canon.json",
        enforcement / "interface-canon.schema.json",
        enforcement / "consumer-contract.schema.json",
        gap_path,
        distribution,
    ]
    payload = {
        "schema_version": 1,
        "brand": {
            "slug": brand["slug"],
            "title": brand["title"],
            "affiliation": brand.get("affiliation"),
            "brand_version": versions["brand_version"],
        },
        "versions": versions,
        "version_semantics": {
            "canon_version": "Brand Canon governing identity and inherited brand values.",
            "interface_canon_version": "Interface Canon governing renderer-neutral UI semantics.",
            "compiler_version": "BrandBuilder distribution that generated this contract.",
            "brand_version": "Consumer brand source contract version.",
        },
        "environment": {
            "renderer": "renderer-neutral",
            "host": "none",
            "supported_targets": ["web", "native"],
            "viewport_profiles": list(load_interface_canon()["runtime"]["window_classes"]),
            "adapter_versions": {"vanilla": metadata["version"], "nextjs": metadata["version"], "enforcement": metadata["version"]},
        },
        "authority": {
            "brand_source": "brand.json",
            "interface_canon": "enforcement/interface-canon.json",
            "instructions": "enforcement/IMPLEMENTATION.md",
            "precedence": ["brand.json", "enforcement/interface-canon.json", "enforcement/consumer-contract.json", "human instructions that do not conflict"],
            "permitted_exceptions": ["token definition files may contain governed literals", "renderer metadata may contain documented platform-required literals"],
        },
        "verification": {
            "entry_points": ["python3 build/verify.py .", "python3 build/validate_glyph.py brand.json"],
            "success": "zero verifier problems and zero glyph failures",
        },
        "recovery": {
            "distribution": distribution_name,
            "path": recovery_path,
            "sha256": recovery_sha,
            "sources": [
                {"kind": "delivered-bundle", "path": recovery_path, "network_required": False},
                {"kind": "authoritative-release", "version": metadata["version"], "network_requires_authorization": True},
            ],
            "instruction": "Verify the delivered SHA-256, then use the host's local skill installation workflow. Never substitute another version.",
        },
        "provenance": [_provenance(path, kit) for path in provenance_paths],
        "capability_gap": {"template_path": gap_path.relative_to(kit).as_posix(), "submission_requires_authorization": True},
    }
    _write_json(enforcement / "consumer-contract.json", payload)
    return payload


def _contained_kit_file(kit, relative):
    _require(isinstance(relative, str) and relative and "\\" not in relative,
             "consumer contract path must be a forward-slash relative path")
    pure = PurePosixPath(relative)
    _require(not pure.is_absolute() and ".." not in pure.parts and ":" not in pure.parts[0],
             "consumer contract path is unsafe: %s" % relative)
    path = kit.joinpath(*pure.parts)
    cursor = kit
    for part in pure.parts:
        cursor = cursor / part
        _require(not cursor.is_symlink(), "consumer contract path uses a symlink: %s" % relative)
    _require(path.is_file(), "consumer contract file is missing: %s" % relative)
    return path


def verify_consumer_contract(kit):
    kit = Path(kit).resolve()
    problems = []
    contract_path = kit / "enforcement" / "consumer-contract.json"
    if not contract_path.is_file():
        return ["consumer contract is missing: enforcement/consumer-contract.json"]
    try:
        contract = _read_json(contract_path)
        required = {"schema_version", "brand", "versions", "version_semantics", "environment", "authority", "verification", "recovery", "provenance", "capability_gap"}
        _require(set(contract) == required and contract["schema_version"] == 1,
                 "consumer contract top-level fields are invalid")
        brand = _read_json(kit / "brand.json")
        _require(contract["brand"]["slug"] == brand.get("slug"), "consumer contract brand slug disagrees")
        _require(contract["versions"]["brand_version"] == brand.get("version", "1.0.0"), "consumer contract brand_version disagrees")
        _require(contract["versions"]["canon_version"] == brand.get("canon", "1.2.1"), "consumer contract canon_version disagrees")
        copied_canon = _read_json(_contained_kit_file(kit, contract["authority"]["interface_canon"]))
        _require(contract["versions"]["interface_canon_version"] == copied_canon.get("version"), "consumer contract interface_canon_version disagrees")
        environment = contract["environment"]
        _require("operating_system" not in environment and "os" not in environment,
                 "consumer environment cannot contain an operating-system route")
        recorded = set()
        for item in contract["provenance"]:
            _require(isinstance(item, dict) and set(item) == {"path", "bytes", "sha256"},
                     "consumer provenance entry is malformed")
            _require(item["path"] not in recorded, "consumer provenance repeats %s" % item["path"])
            recorded.add(item["path"])
            path = _contained_kit_file(kit, item["path"])
            payload = path.read_bytes()
            _require(hashlib.sha256(payload).hexdigest() == item["sha256"], "consumer provenance checksum mismatch: %s" % item["path"])
            _require(len(payload) == item["bytes"], "consumer provenance byte count mismatch: %s" % item["path"])
        recovery = contract["recovery"]
        required_provenance = {
            contract["authority"]["brand_source"],
            "enforcement/AGENTS.md",
            contract["authority"]["instructions"],
            contract["authority"]["interface_canon"],
            "enforcement/interface-canon.schema.json",
            "enforcement/consumer-contract.schema.json",
            contract["capability_gap"]["template_path"],
            recovery["path"],
        }
        _require(required_provenance.issubset(recorded),
                 "consumer provenance omits required authority: %s" %
                 ", ".join(sorted(required_provenance - recorded)))
        distribution = _contained_kit_file(kit, recovery["path"])
        _require(distribution.name == recovery["distribution"], "recovery distribution filename disagrees")
        _require(SHA256.fullmatch(recovery["sha256"] or "") and hashlib.sha256(distribution.read_bytes()).hexdigest() == recovery["sha256"],
                 "recovery distribution checksum mismatch")
        _require(recovery["sources"][0].get("kind") == "delivered-bundle"
                 and recovery["sources"][0].get("network_required") is False,
                 "recovery must prefer delivered offline bytes")
        _require("latest" not in json.dumps(recovery).lower(), "recovery cannot recommend an unspecified latest version")
        agents = _contained_kit_file(kit, "enforcement/AGENTS.md").read_text(encoding="utf-8")
        _require(agents.count(BEGIN_MARKER) == 1 and agents.count(END_MARKER) == 1
                 and agents.index(BEGIN_MARKER) < agents.index(END_MARKER),
                 "governed instruction markers are malformed")
        gap = _read_json(_contained_kit_file(kit, contract["capability_gap"]["template_path"]))
        _require(gap.get("submission_authorized") is False
                 and contract["capability_gap"]["submission_requires_authorization"] is True,
                 "capability-gap submission authority is invalid")
        with zipfile.ZipFile(str(distribution)) as archive:
            names = archive.namelist()
            _require(len(names) == len(set(names)), "recovery distribution has duplicate paths")
            _require({"SKILL.md", "AGENTS.md", "references/interface-canon.json"}.issubset(names),
                     "recovery distribution lacks governed entry points")
            for name in names:
                pure = PurePosixPath(name)
                _require(pure.parts and not pure.is_absolute() and ".." not in pure.parts
                         and "\\" not in name and ":" not in pure.parts[0],
                         "recovery distribution contains an unsafe path: %s" % name)
            metadata = skill_metadata_from_text(archive.read("SKILL.md").decode("utf-8"))
            _require(metadata["version"] == contract["versions"]["compiler_version"],
                     "recovery compiler version disagrees")
            _require(metadata["canon"] == contract["versions"]["canon_version"],
                     "recovery Brand Canon version disagrees")
            _require(metadata["interface_canon"] == contract["versions"]["interface_canon_version"],
                     "recovery Interface Canon metadata disagrees")
            bundled_canon = json.loads(archive.read("references/interface-canon.json").decode("utf-8"))
            _require(bundled_canon["version"] == contract["versions"]["interface_canon_version"],
                     "recovery Interface Canon version disagrees")
    except (InterfaceContractError, OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, zipfile.BadZipFile) as error:
        problems.append(str(error))
    return problems


def skill_metadata_from_text(text):
    frontmatter = re.match(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", text, re.DOTALL)
    _require(frontmatter is not None, "bundled SKILL.md lacks frontmatter")
    block = re.search(r"^metadata:\s*$\n(?P<body>(?:^[ \t]+.*(?:\n|\Z))+)", frontmatter.group("body"), re.MULTILINE)
    _require(block is not None, "bundled SKILL.md lacks metadata")
    values = {}
    for output, key in (("version", "version"), ("canon", "canon"), ("interface_canon", "interface-canon")):
        match = re.search(r"^\s+%s:\s*([^\s#]+)\s*$" % key, block.group("body"), re.MULTILINE)
        _require(match is not None, "bundled SKILL.md metadata lacks %s" % key)
        values[output] = match.group(1).strip("\"'")
    return values
