#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renderer-neutral interface, routing, and consumer handover contracts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

from schema_validation import SchemaValidationError, validate_json_schema
from process_utils import hidden_process_kwargs
from documentation_contract import (build_documentation_facts, load_documentation_contract,
                                    render_implementation, render_migration_summary,
                                    verify_documentation_facts, verify_migration_summary,
                                    verify_rendered_implementation)

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
REFERENCES = SKILL_ROOT / "references"
INTERFACE_CANON = REFERENCES / "interface-canon.json"
BRAND_CANON = REFERENCES / "01-canon.json"
VERSION_POLICY = REFERENCES / "version-policy.json"
RELEASE_IMPACT = REFERENCES / "release-impact.json"
RELEASE_IMPACT_SCHEMA = REFERENCES / "release-impact.schema.json"
BEGIN_MARKER = "<!-- BEGIN SHRUGGIE-BRANDBUILDER: CONSUMER CONTRACT -->"
END_MARKER = "<!-- END SHRUGGIE-BRANDBUILDER: CONSUMER CONTRACT -->"
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
ROLE = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$")
REFERENCE = re.compile(r"^\$(primitive|alias|brand|brand_canon|resolved)\.([A-Za-z0-9_.-]+)$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SOURCE_REVISION = re.compile(r"^[0-9a-f]{40,64}$")
ZIP_TIME = (2026, 9, 17, 0, 0, 0)
GENERATED_DIRECTORIES = {"__pycache__", "node_modules", ".venv", "venv"}
RELEASE_AUTHORIZED_BRANDS = (
    "shruggietech",
    "fragcap",
    "go-schedule",
    "glitchpad",
    "covarity",
    "eso-weave",
    "cueson",
)
BACKWARD_BRAND_DEFAULTS = {
    "surfaces.base": "#000000",
    "surfaces.card": "#111111",
    "surfaces.popover": "#0A0A0A",
    "accent.dim": "#9A9A9A",
    "accent.accessible": "#666666",
    "light_surfaces.base": "#FFFFFF",
    "light_surfaces.card": "#F8F8F6",
    "light_surfaces.popover": "#FFFFFF",
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


VERSION_DOMAINS = {
    "brand_canon", "interface_canon", "component_recipes", "web_react_adapter",
    "egui_adapter", "compiler", "brand",
}


def load_version_policy(path=None):
    return _read_json(path or VERSION_POLICY)


def validate_version_policy(policy):
    required = {"schema_version", "id", "kind", "version", "domains", "compatibility_rules", "lifecycle_states", "recovery"}
    _require(isinstance(policy, dict) and set(policy) == required,
             "version policy fields are invalid")
    _require(policy["id"] == "shruggie-version-policy" and policy["kind"] == "version-policy",
             "version policy identity is invalid")
    _require(policy["schema_version"] == 1, "version policy schema version is unsupported")
    _require(isinstance(policy["version"], str) and SEMVER.fullmatch(policy["version"]),
             "version policy version must be semantic")
    domains = policy["domains"]
    _require(isinstance(domains, dict) and set(domains) == VERSION_DOMAINS,
             "version policy domains must be exactly %s" % ", ".join(sorted(VERSION_DOMAINS)))
    domain_fields = {"meaning", "patch", "minor", "major", "compatibility_keys", "publication"}
    for name, domain in domains.items():
        _require(isinstance(domain, dict) and set(domain) == domain_fields,
                 "version domain %s fields are invalid" % name)
        _require(all(isinstance(domain[key], str) and domain[key].strip()
                     for key in ("meaning", "publication")),
                 "version domain %s meaning or publication is empty" % name)
        for level in ("patch", "minor", "major"):
            values = domain[level]
            _require(isinstance(values, list) and values and len(values) == len(set(values))
                     and all(isinstance(value, str) and value.strip() for value in values),
                     "version domain %s %s rules are invalid" % (name, level))
        compatibility = domain["compatibility_keys"]
        _require(isinstance(compatibility, list) and len(compatibility) == len(set(compatibility))
                 and set(compatibility).issubset(VERSION_DOMAINS - {name}),
                 "version domain %s compatibility keys are invalid" % name)
    rules = policy["compatibility_rules"]
    _require(isinstance(rules, list) and rules, "version compatibility rules are missing")
    recorded = set()
    for rule in rules:
        _require(isinstance(rule, dict) and set(rule) == {"dependent", "dependent_major", "dependency", "supported"},
                 "version compatibility rule fields are invalid")
        edge = (rule["dependent"], rule["dependency"])
        _require(edge not in recorded, "duplicate version compatibility rule: %s -> %s" % edge)
        recorded.add(edge)
        _require(rule["dependent"] in VERSION_DOMAINS and rule["dependency"] in VERSION_DOMAINS
                 and rule["dependency"] in domains[rule["dependent"]]["compatibility_keys"],
                 "version compatibility rule has an undeclared dependency")
        _require(isinstance(rule["dependent_major"], int) and not isinstance(rule["dependent_major"], bool)
                 and rule["dependent_major"] >= 0,
                 "version compatibility rule has an invalid dependent major")
        _require(isinstance(rule["supported"], list) and rule["supported"]
                 and len(rule["supported"]) == len(set(rule["supported"]))
                 and all(isinstance(value, str) and SEMVER.fullmatch(value) for value in rule["supported"]),
                 "version compatibility rule has invalid supported versions")
    expected_edges = {
        (dependent, dependency)
        for dependent, domain in domains.items()
        for dependency in domain["compatibility_keys"]
    }
    _require(recorded == expected_edges, "version compatibility rules do not cover every declared edge")
    states = policy["lifecycle_states"]
    _require(isinstance(states, list) and {item.get("id") for item in states if isinstance(item, dict)}
             == {"compatible", "candidate", "published"},
             "version lifecycle states must distinguish compatibility, candidate, and published contracts")
    for item in states:
        _require(set(item) == {"id", "meaning"} and isinstance(item["meaning"], str) and item["meaning"].strip(),
                 "version lifecycle state is invalid")
    recovery = policy["recovery"]
    _require(recovery == {
        "pin_exact_versions": True,
        "require_sha256": True,
        "prefer_delivered_offline_bytes": True,
        "allow_latest_substitution": False,
    }, "version recovery policy must require exact checksummed offline recovery")
    return policy


def publication_status(version):
    ref = os.environ.get("GITHUB_REF", "").strip()
    ref_type = os.environ.get("GITHUB_REF_TYPE", "").strip()
    ref_name = os.environ.get("GITHUB_REF_NAME", "").strip()
    exact_tag = "v%s" % version
    return "release" if ref == "refs/tags/%s" % exact_tag or (ref_type == "tag" and ref_name == exact_tag) else "candidate"


def bundle_publication(version, brand):
    affiliation = brand.get("affiliation")
    _require(isinstance(affiliation, dict), "bundle publication requires brand affiliation")
    ownership = affiliation.get("ownership")
    _require(ownership in {"shruggietech-owned", "third-party"},
             "bundle publication requires explicit supported ownership")
    slug = brand.get("slug")
    _require(isinstance(slug, str) and slug, "bundle publication requires a brand slug")
    status = publication_status(version)
    if slug not in RELEASE_AUTHORIZED_BRANDS:
        status = "candidate"
    return (
        {"status": status, "version": version, "tag": "v%s" % version},
        {"algorithm": "sha256", "manifest": "manifest.json",
         "release_checksums": "SHA256SUMS" if status == "release" else None},
    )


def source_revision(root=None):
    explicit = os.environ.get("BRANDBUILDER_SOURCE_REVISION") or os.environ.get("GITHUB_SHA")
    if explicit:
        revision = explicit.strip().lower()
        _require(SOURCE_REVISION.fullmatch(revision), "BrandBuilder source revision must be an exact Git object id")
        return revision
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(root or SKILL_ROOT.parent),
        capture_output=True, text=True, **hidden_process_kwargs()
    )
    revision = completed.stdout.strip().lower()
    _require(completed.returncode == 0 and SOURCE_REVISION.fullmatch(revision),
             "BrandBuilder source revision is unavailable")
    return revision


def package_identity(slug, brand_version, brandbuilder_version):
    package_id = "%s-brand-%s-bb%s" % (slug, brand_version, brandbuilder_version)
    return {"id": package_id, "filename": "%s.zip" % package_id,
            "brand_slug": slug, "brand_version": brand_version,
            "brandbuilder_version": brandbuilder_version}


def load_release_impact(path=None, schema_path=None):
    impact = _read_json(path or RELEASE_IMPACT)
    schema = _read_json(schema_path or RELEASE_IMPACT_SCHEMA)
    try:
        validate_json_schema(impact, schema)
    except SchemaValidationError as error:
        raise InterfaceContractError("release impact schema violation: %s" % error) from error
    prohibited = {"consumer", "adoption", "adopted", "productivity", "utility", "elapsed_time",
                  "correction_rounds", "escaped_defects", "handover_evidence"}
    pending = [impact]
    while pending:
        value = pending.pop()
        if isinstance(value, dict):
            _require(not prohibited.intersection(value),
                     "release impact contains prohibited downstream evidence fields")
            pending.extend(value.values())
        elif isinstance(value, list):
            pending.extend(value)
    return impact


def validate_version_combination(versions, policy=None):
    policy = validate_version_policy(policy or load_version_policy())
    _require(isinstance(versions, dict) and set(versions) == VERSION_DOMAINS,
             "version combination must contain exactly %s" % ", ".join(sorted(VERSION_DOMAINS)))
    _require(all(isinstance(value, str) and SEMVER.fullmatch(value) for value in versions.values()),
             "version combination contains a non-semantic version")
    for rule in policy["compatibility_rules"]:
        dependent_version = versions[rule["dependent"]]
        dependent_major = int(dependent_version.split(".", 1)[0])
        _require(dependent_major == rule["dependent_major"],
                 "%s %s is incompatible with policy major %d; migrate or publish a matching compatibility rule" % (
                     rule["dependent"], dependent_version, rule["dependent_major"]))
        actual = versions[rule["dependency"]]
        _require(actual in rule["supported"],
                 "%s %s is incompatible with %s %s; supported %s" % (
                     rule["dependent"], versions[rule["dependent"]], rule["dependency"], actual,
                     ", ".join(rule["supported"])))
    return {
        "policy_version": policy["version"],
        "status": "compatible",
        "validated_versions": dict(sorted(versions.items())),
        "rules_checked": len(policy["compatibility_rules"]),
    }


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
        "invariants", "permitted_overrides", "state_pairs", "theme_aliases",
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
    theme_aliases = canon["theme_aliases"]
    _require(isinstance(theme_aliases, dict) and set(theme_aliases) == {"dark", "light"},
             "theme_aliases must define dark and light")
    for theme, themed in theme_aliases.items():
        _require(isinstance(themed, dict), "theme aliases must be objects: %s" % theme)
        _require(set(themed).issubset(aliases), "theme %s targets an unknown role" % theme)
        _require(all(isinstance(value, str) and REFERENCE.fullmatch(value) for value in themed.values()),
                 "theme %s contains an invalid reference" % theme)
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


def _legal_muted(brand, background, theme, minimum):
    from coloraide import Color

    candidates = (
        ("accent.accessible", "accent.dim", "accent.deep", "accent.bright")
        if theme == "light"
        else ("accent.dim", "accent.bright", "accent.accessible", "accent.deep")
    )
    seen = set()
    for dotted in candidates:
        candidate = _lookup_brand(brand, dotted)
        contrast = Color(candidate).contrast(background, method="wcag21")
        if candidate not in seen and contrast + 1e-9 >= minimum:
            return candidate
        seen.add(candidate)
    return _legal_foreground(background)


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
    inheritance = ((brand.get("affiliation") or {}).get("inheritance"))
    for role, reference in overrides.items():
        _require(role in canon["permitted_overrides"], "unsupported override role: %s" % role)
        _require(isinstance(reference, str) and any(
            reference.startswith(prefix) for prefix in canon["permitted_overrides"][role]
        ), "unsupported override reference for %s" % role)
        if inheritance == "independent" and reference.startswith("$brand_canon.color.immutable.orange"):
            raise InterfaceContractError("override %s crosses affiliation boundary into house orange" % role)
    if inheritance == "shruggietech-house":
        immutable = brand_canon["color"]["immutable"]
        semantic = {"action": immutable["orange-cta"]["hex"], "emphasis": immutable["orange"]["hex"]}
    else:
        colors = brand.get("semantic_colors") or {}
        _require(set(colors) == {"action", "emphasis"},
                 "independent brand lacks semantic action and emphasis colors")
        semantic = colors
    def resolve_theme(theme):
        aliases = dict(canon["aliases"])
        aliases.update(canon["theme_aliases"][theme])
        aliases.update(overrides)
        surface = "light_surfaces.base" if theme == "light" else "surfaces.base"
        background = _lookup_brand(brand, surface)
        accent = _lookup_brand(brand, "accent.accessible" if theme == "light" else "accent.bright")
        resolved_context = {
            "action": semantic["action"],
            "emphasis": semantic["emphasis"],
            "action_foreground": _legal_foreground(semantic["action"]),
            "destructive_foreground": _legal_foreground(brand_canon["color"]["immutable"]["fault"]["hex"]),
            "accent": accent,
            "accent_foreground": _legal_foreground(accent),
            "muted": _legal_muted(brand, background, theme, canon["invariants"]["minimum_text_contrast"]),
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
                raise InterfaceContractError("%s state pair %s does not resolve to colors" % (theme, pair["id"])) from error
            _require(ratio + 1e-9 >= pair["minimum_contrast"],
                     "%s state pair %s contrast %.2f is below %.2f" %
                     (theme, pair["id"], ratio, pair["minimum_contrast"]))
        return resolved_roles

    roles_by_theme = {theme: resolve_theme(theme) for theme in ("dark", "light")}
    return {
        "interface_canon_version": canon["version"],
        "canon_version": brand_canon_version,
        "units": canon["units"],
        "runtime": canon["runtime"],
        "invariants": canon["invariants"],
        "roles": roles_by_theme["dark"],
        "roles_by_theme": roles_by_theme,
        "system_theme_resolution": ["light", "dark"],
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
    elif signals["consumer_change"] and not signals["pinned_contract_present"]:
        clarification = "Which exact pinned consumer contract should govern this implementation?"
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
    for output, key in (("version", "version"), ("canon", "canon"), ("interface_canon", "interface-canon"),
                        ("component_recipes", "component-recipes"), ("web_react_adapter", "web-react-adapter"),
                        ("egui_adapter", "egui-adapter")):
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

BrandBuilder is mandatory for brand-system authoring, consumer implementation, and conformance audit. This kit pins Brand Canon `{canon}`, Interface Canon `{interface}`, component recipes `{recipes}`, Web/React adapter `{adapter}`, egui adapter `{egui}`, compiler `{compiler}`, and brand `{brand_version}`.

Read `consumer-contract.json`, then `IMPLEMENTATION.md`. The pinned contract outranks screenshots, legacy stylesheets, and inferred local values. Do not reinterpret identity or create a permanent parallel design system.

{affiliation}

If BrandBuilder `{compiler}` is absent, verify SHA-256 `{sha}` and extract `{recovery}` into the empty directory `enforcement/brandbuilder`. Never substitute another version. Run `python3 enforcement/brandbuilder/templates/verify.py .` and `python3 enforcement/brandbuilder/templates/validate_glyph.py brand.json`; both must report zero failures.
{end}""".format(
        begin=BEGIN_MARKER, end=END_MARKER, canon=versions["canon_version"],
        interface=versions["interface_canon_version"], recipes=versions["component_recipe_version"],
        adapter=versions["web_react_adapter_version"], egui=versions["egui_adapter_version"], compiler=versions["compiler_version"],
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
        "component-recipes.json": REFERENCES / "component-recipes.json",
        "component-recipes.schema.json": REFERENCES / "component-recipes.schema.json",
        "version-policy.json": REFERENCES / "version-policy.json",
        "consumer-contract.schema.json": REFERENCES / "consumer-contract.schema.json",
        "documentation-contract.json": REFERENCES / "documentation-contract.json",
        "documentation-contract.schema.json": REFERENCES / "documentation-contract.schema.json",
        "release-impact.json": RELEASE_IMPACT,
        "release-impact.schema.json": RELEASE_IMPACT_SCHEMA,
    }
    for name, source in copied.items():
        (enforcement / name).write_bytes(source.read_bytes())
    distribution_name = "shruggie-brandbuilder-%s.skill" % metadata["version"]
    distribution = enforcement / "distributions" / distribution_name
    recovery_sha = write_deterministic_skill_bundle(distribution)
    web_adapter = kit / "web" / "adapter.json"
    support_matrix = kit / "web" / "support-matrix.json"
    egui_adapter = kit / "native" / "egui" / "adapter.json"
    egui_support = kit / "native" / "egui" / "support-matrix.json"
    _require(web_adapter.is_file(), "Web/React adapter manifest is missing before consumer contract generation")
    _require(support_matrix.is_file(), "Web support matrix is missing before consumer contract generation")
    _require(egui_adapter.is_file(), "egui adapter manifest is missing before consumer contract generation")
    _require(egui_support.is_file(), "egui support matrix is missing before consumer contract generation")
    adapter = _read_json(web_adapter)
    native_adapter = _read_json(egui_adapter)
    recipe_catalog = _read_json(REFERENCES / "component-recipes.json")
    _require(metadata["component_recipes"] == recipe_catalog["version"],
             "skill component recipe metadata does not match the catalog")
    _require(metadata["web_react_adapter"] == adapter["adapter_version"],
             "skill Web/React adapter metadata does not match generated output")
    _require(metadata["egui_adapter"] == native_adapter["adapter_version"],
             "skill egui adapter metadata does not match generated output")
    versions = {
        "canon_version": resolved["canon_version"],
        "interface_canon_version": resolved["interface_canon_version"],
        "component_recipe_version": recipe_catalog["version"],
        "web_react_adapter_version": adapter["adapter_version"],
        "egui_adapter_version": native_adapter["adapter_version"],
        "compiler_version": metadata["version"],
        "brand_version": brand.get("version", "1.0.0"),
    }
    domain_versions = {
        "brand_canon": versions["canon_version"],
        "interface_canon": versions["interface_canon_version"],
        "component_recipes": versions["component_recipe_version"],
        "web_react_adapter": versions["web_react_adapter_version"],
        "egui_adapter": versions["egui_adapter_version"],
        "compiler": versions["compiler_version"],
        "brand": versions["brand_version"],
    }
    compatibility = validate_version_combination(domain_versions)
    gap = {
        "schema_version": 1,
        "consumer": {"brand": brand["slug"], "brand_version": versions["brand_version"]},
        "environment": {"renderer": "renderer-neutral", "host": "none"},
        "requirement": "Describe the reproducible consumer need.",
        "shared_concept": "Name the missing or insufficient shared semantic concept.",
        "evidence": [],
        "classification": "reusable-capability",
        "upstream_resolution": None,
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
    impact = load_release_impact()
    _require(impact["brandbuilder_version"] == metadata["version"],
             "release impact BrandBuilder version disagrees with skill metadata")
    package = package_identity(brand["slug"], versions["brand_version"], metadata["version"])
    publication, checksum_authority = bundle_publication(metadata["version"], brand)
    bundle = {
        "schema_version": 1,
        "package": package,
        "versions": versions,
        "source_revision": source_revision(),
        "publication": publication,
        "checksum_authority": checksum_authority,
    }
    _write_json(enforcement / "bundle.json", bundle)
    consumer_core = {
        "schema_version": 4,
        "brand": {
            "slug": brand["slug"],
            "title": brand["title"],
            "affiliation": brand.get("affiliation"),
            "brand_version": versions["brand_version"],
        },
        "bundle": bundle,
        "versions": versions,
        "version_semantics": {
            "canon_version": "Brand Canon governing identity and inherited brand values.",
            "interface_canon_version": "Interface Canon governing renderer-neutral UI semantics.",
            "component_recipe_version": "Bounded shared component grammar and behavior contract.",
            "web_react_adapter_version": "Generated Web/React implementation contract.",
            "egui_adapter_version": "Generated Rust and egui implementation contract.",
            "compiler_version": "BrandBuilder distribution that generated this contract.",
            "brand_version": "Consumer brand source contract version.",
        },
        "compatibility": compatibility,
        "environment": {
            "renderer": "renderer-neutral",
            "host": "none",
            "supported_targets": ["web", "native"],
            "viewport_profiles": list(load_interface_canon()["runtime"]["window_classes"]),
            "adapter_versions": {"web-tokens": adapter["adapter_version"], "web-react": adapter["adapter_version"], "egui": native_adapter["adapter_version"], "nextjs-compatibility": metadata["version"]},
        },
        "authority": {
            "brand_source": "brand.json",
            "bundle": "enforcement/bundle.json",
            "release_impact": "enforcement/release-impact.json",
            "migration_summary": "enforcement/MIGRATION.md",
            "interface_canon": "enforcement/interface-canon.json",
            "component_recipes": "enforcement/component-recipes.json",
            "version_policy": "enforcement/version-policy.json",
            "web_adapter": "web/adapter.json",
            "support_matrix": "web/support-matrix.json",
            "egui_adapter": "native/egui/adapter.json",
            "egui_support_matrix": "native/egui/support-matrix.json",
            "instructions": "enforcement/IMPLEMENTATION.md",
            "documentation_contract": "enforcement/documentation-contract.json",
            "documentation_facts": "enforcement/documentation-facts.json",
            "precedence": ["brand.json", "enforcement/bundle.json", "enforcement/release-impact.json", "enforcement/interface-canon.json", "enforcement/component-recipes.json", "enforcement/version-policy.json", "enforcement/documentation-contract.json", "enforcement/consumer-contract.json", "human instructions that do not conflict"],
            "permitted_exceptions": ["token definition files may contain governed literals", "renderer metadata may contain documented platform-required literals"],
        },
        "verification": {
            "entry_points": ["python3 enforcement/brandbuilder/templates/verify.py .", "python3 enforcement/brandbuilder/templates/validate_glyph.py brand.json"],
            "success": "zero verifier problems and zero glyph failures",
        },
        "recovery": {
            "distribution": distribution_name,
            "path": recovery_path,
            "sha256": recovery_sha,
            "extract_to": "enforcement/brandbuilder",
            "sources": [
                {"kind": "delivered-bundle", "path": recovery_path, "network_required": False},
                {"kind": "authoritative-release", "version": metadata["version"], "network_requires_authorization": True},
            ],
            "instruction": "Verify the delivered SHA-256, then extract the exact archive into the empty enforcement/brandbuilder directory. Never substitute another version.",
        },
        "capability_gap": {"template_path": gap_path.relative_to(kit).as_posix(), "submission_requires_authorization": True},
    }
    documentation_policy = load_documentation_contract(enforcement / "documentation-contract.json",
                                                        enforcement / "documentation-contract.schema.json",
                                                        REFERENCES)
    facts = build_documentation_facts(documentation_policy, consumer_core, kit)
    _write_json(enforcement / "documentation-facts.json", facts)
    rendered = render_implementation(facts, implementation_text)
    verify_rendered_implementation(rendered, facts)
    _write_text(enforcement / "IMPLEMENTATION.md", rendered)
    migration = render_migration_summary(facts)
    _write_text(enforcement / "MIGRATION.md", migration)
    provenance_paths = [
        brand_source,
        agents_path,
        enforcement / "IMPLEMENTATION.md",
        enforcement / "MIGRATION.md",
        enforcement / "bundle.json",
        enforcement / "release-impact.json",
        enforcement / "release-impact.schema.json",
        enforcement / "interface-canon.json",
        enforcement / "interface-canon.schema.json",
        enforcement / "component-recipes.json",
        enforcement / "component-recipes.schema.json",
        enforcement / "version-policy.json",
        enforcement / "consumer-contract.schema.json",
        enforcement / "documentation-contract.json",
        enforcement / "documentation-contract.schema.json",
        enforcement / "documentation-facts.json",
        web_adapter,
        support_matrix,
        egui_adapter.parent / "Cargo.lock",
        egui_adapter,
        egui_support,
        gap_path,
        distribution,
    ]
    payload = dict(consumer_core)
    payload["provenance"] = [_provenance(path, kit) for path in provenance_paths]
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
        schema_path = kit / "enforcement" / "consumer-contract.schema.json"
        schema = _read_json(schema_path)
        try:
            validate_json_schema(contract, schema)
        except SchemaValidationError as error:
            raise InterfaceContractError("consumer contract schema violation: %s" % error) from error
        brand = _read_json(kit / "brand.json")
        authority = contract["authority"]
        recovery = contract["recovery"]
        declared_authority = {
            authority["brand_source"],
            authority["bundle"],
            authority["release_impact"],
            authority["migration_summary"],
            authority["instructions"],
            authority["interface_canon"],
            authority["component_recipes"],
            authority["version_policy"],
            authority["web_adapter"],
            authority["support_matrix"],
            authority["egui_adapter"],
            authority["egui_support_matrix"],
            authority["documentation_contract"],
            authority["documentation_facts"],
            contract["capability_gap"]["template_path"],
            recovery["path"],
        }
        for relative in declared_authority:
            _contained_kit_file(kit, relative)
        declared_brand = _read_json(_contained_kit_file(kit, authority["brand_source"]))
        _require(declared_brand == brand, "consumer authority brand_source differs from brand.json")
        expected_brand = {
            "slug": brand.get("slug"),
            "title": brand.get("title"),
            "affiliation": brand.get("affiliation"),
            "brand_version": brand.get("version", "1.0.0"),
        }
        _require(contract["brand"] == expected_brand, "consumer contract brand metadata disagrees")
        expected_package = package_identity(brand["slug"], brand.get("version", "1.0.0"), contract["versions"]["compiler_version"])
        _require(contract["bundle"]["package"] == expected_package, "consumer bundle package identity disagrees")
        _require(_read_json(_contained_kit_file(kit, authority["bundle"])) == contract["bundle"],
                 "consumer bundle authority disagrees")
        _require(contract["bundle"]["versions"] == contract["versions"], "consumer bundle versions disagree")
        expected_release_checksums = (
            "SHA256SUMS" if contract["bundle"]["publication"]["status"] == "release" else None
        )
        _require(contract["bundle"]["checksum_authority"]["release_checksums"] == expected_release_checksums,
                 "consumer bundle release checksum authority disagrees with publication status")
        impact = load_release_impact(_contained_kit_file(kit, authority["release_impact"]),
                                     _contained_kit_file(kit, "enforcement/release-impact.schema.json"))
        _require(impact["brandbuilder_version"] == contract["versions"]["compiler_version"],
                 "consumer release impact version disagrees")
        _require(contract["versions"]["brand_version"] == brand.get("version", "1.0.0"), "consumer contract brand_version disagrees")
        _require(contract["versions"]["canon_version"] == brand.get("canon", "1.2.1"), "consumer contract canon_version disagrees")
        copied_canon = _read_json(_contained_kit_file(kit, authority["interface_canon"]))
        _require(contract["versions"]["interface_canon_version"] == copied_canon.get("version"), "consumer contract interface_canon_version disagrees")
        copied_recipes = _read_json(_contained_kit_file(kit, authority["component_recipes"]))
        _require(contract["versions"]["component_recipe_version"] == copied_recipes.get("version"), "consumer contract component_recipe_version disagrees")
        copied_policy = validate_version_policy(_read_json(_contained_kit_file(kit, authority["version_policy"])))
        web_adapter = _read_json(_contained_kit_file(kit, authority["web_adapter"]))
        _require(contract["versions"]["web_react_adapter_version"] == web_adapter.get("adapter_version"), "consumer contract web_react_adapter_version disagrees")
        _require(web_adapter.get("component_recipe_version") == copied_recipes.get("version"), "Web/React adapter recipe version disagrees")
        web_entries = web_adapter.get("entries", {})
        _require(web_entries.get("environment") == "web/react/environment.tsx",
                 "Web/React adapter environment entry disagrees")
        for relative in web_entries.values():
            _contained_kit_file(kit, relative)
        _require(web_adapter.get("environment_exports") == ["AppFrameEnvironmentBridge", "measureImeBlockEnd"],
                 "Web/React adapter environment exports disagree")
        support = _read_json(_contained_kit_file(kit, authority["support_matrix"]))
        _require(support.get("adapter_version") == web_adapter.get("adapter_version"), "Web support matrix adapter version disagrees")
        egui_adapter = _read_json(_contained_kit_file(kit, authority["egui_adapter"]))
        _require(contract["versions"]["egui_adapter_version"] == egui_adapter.get("adapter_version"), "consumer contract egui_adapter_version disagrees")
        _require(egui_adapter.get("component_recipe_version") == copied_recipes.get("version"), "egui adapter recipe version disagrees")
        _require(egui_adapter.get("compiler_version") == contract["versions"]["compiler_version"], "egui adapter compiler version disagrees with consumer contract")
        egui_support = _read_json(_contained_kit_file(kit, authority["egui_support_matrix"]))
        _require(egui_support.get("adapter_version") == egui_adapter.get("adapter_version"), "egui support matrix adapter version disagrees")
        domain_versions = {
            "brand_canon": contract["versions"]["canon_version"],
            "interface_canon": contract["versions"]["interface_canon_version"],
            "component_recipes": contract["versions"]["component_recipe_version"],
            "web_react_adapter": contract["versions"]["web_react_adapter_version"],
            "egui_adapter": contract["versions"]["egui_adapter_version"],
            "compiler": contract["versions"]["compiler_version"],
            "brand": contract["versions"]["brand_version"],
        }
        _require(contract["compatibility"] == validate_version_combination(domain_versions, copied_policy),
                 "consumer compatibility record disagrees with version policy")
        documentation_policy = load_documentation_contract(
            _contained_kit_file(kit, authority["documentation_contract"]),
            _contained_kit_file(kit, "enforcement/documentation-contract.schema.json"),
            REFERENCES,
        )
        documentation_facts = _read_json(_contained_kit_file(kit, authority["documentation_facts"]))
        verify_documentation_facts(documentation_facts, documentation_policy, contract, kit)
        implementation = _contained_kit_file(kit, authority["instructions"]).read_text(encoding="utf-8")
        verify_rendered_implementation(implementation, documentation_facts)
        migration = _contained_kit_file(kit, authority["migration_summary"]).read_text(encoding="utf-8")
        verify_migration_summary(migration, documentation_facts)
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
        expected_entry_points = [
            "python3 %s/templates/verify.py ." % recovery["extract_to"],
            "python3 %s/templates/validate_glyph.py brand.json" % recovery["extract_to"],
        ]
        _require(contract["verification"]["entry_points"] == expected_entry_points,
                 "consumer verification entry points disagree with recovery location")
        required_provenance = {
            "enforcement/AGENTS.md",
            "enforcement/interface-canon.schema.json",
            "enforcement/component-recipes.schema.json",
            "enforcement/version-policy.json",
            "enforcement/consumer-contract.schema.json",
            "enforcement/documentation-contract.schema.json",
            "enforcement/release-impact.schema.json",
        } | declared_authority
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
            _require({"SKILL.md", "AGENTS.md", "references/interface-canon.json",
                      "references/component-recipes.json", "references/component-recipes.schema.json",
                      "references/version-policy.json",
                      "references/consumer-contract.schema.json", "references/documentation-contract.json",
                      "references/documentation-contract.schema.json", "templates/documentation_contract.py", "templates/verify.py",
                      "templates/validate_glyph.py"}.issubset(names),
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
            _require(metadata["component_recipes"] == contract["versions"]["component_recipe_version"],
                     "recovery component recipe metadata disagrees")
            _require(metadata["web_react_adapter"] == contract["versions"]["web_react_adapter_version"],
                     "recovery Web/React adapter metadata disagrees")
            _require(metadata["egui_adapter"] == contract["versions"]["egui_adapter_version"],
                     "recovery egui adapter metadata disagrees")
            bundled_canon = json.loads(archive.read("references/interface-canon.json").decode("utf-8"))
            _require(bundled_canon["version"] == contract["versions"]["interface_canon_version"],
                     "recovery Interface Canon version disagrees")
            bundled_recipes = json.loads(archive.read("references/component-recipes.json").decode("utf-8"))
            _require(bundled_recipes["version"] == contract["versions"]["component_recipe_version"],
                     "recovery component recipe version disagrees")
            bundled_policy = validate_version_policy(json.loads(archive.read("references/version-policy.json").decode("utf-8")))
            _require(bundled_policy["version"] == contract["compatibility"]["policy_version"],
                     "recovery version policy disagrees")
            _require(archive.read("references/consumer-contract.schema.json") == schema_path.read_bytes(),
                     "recovery consumer schema disagrees with delivered schema")
    except (InterfaceContractError, SchemaValidationError, OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, zipfile.BadZipFile) as error:
        problems.append(str(error))
    return problems


def skill_metadata_from_text(text):
    frontmatter = re.match(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", text, re.DOTALL)
    _require(frontmatter is not None, "bundled SKILL.md lacks frontmatter")
    block = re.search(r"^metadata:\s*$\n(?P<body>(?:^[ \t]+.*(?:\n|\Z))+)", frontmatter.group("body"), re.MULTILINE)
    _require(block is not None, "bundled SKILL.md lacks metadata")
    values = {}
    for output, key in (("version", "version"), ("canon", "canon"), ("interface_canon", "interface-canon"),
                        ("component_recipes", "component-recipes"), ("web_react_adapter", "web-react-adapter"),
                        ("egui_adapter", "egui-adapter")):
        match = re.search(r"^\s+%s:\s*([^\s#]+)\s*$" % key, block.group("body"), re.MULTILINE)
        _require(match is not None, "bundled SKILL.md metadata lacks %s" % key)
        values[output] = match.group(1).strip("\"'")
    return values
