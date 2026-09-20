#!/usr/bin/env python3
"""Govern documentation ownership and exact generated documentation facts."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path, PurePosixPath

from schema_validation import SchemaValidationError, validate_json_schema

HERE = Path(__file__).resolve().parent
REFERENCES = HERE.parent / "references"
POLICY_PATH = REFERENCES / "documentation-contract.json"
SCHEMA_PATH = REFERENCES / "documentation-contract.schema.json"
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
HOSTED_MANUAL_ORIGIN = "https://brand.shruggie.tech"
REQUIRED_SURFACES = {"main", "hosted", "bundled"}
REQUIRED_ROUTES = {"docs-index", "docs-page", "guidelines", "guidelines-topic", "downloads"}
REQUIRED_GRAPHICS = {"ownership", "operating-modes", "improvement-loop"}


class DocumentationContractError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise DocumentationContractError(message)


def _read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise DocumentationContractError("invalid UTF-8 JSON at %s: %s" % (path, error)) from error


def load_documentation_contract(path=None, schema_path=None, references=None):
    contract = _read_json(path or POLICY_PATH)
    schema = _read_json(schema_path or SCHEMA_PATH)
    try:
        validate_json_schema(contract, schema)
    except SchemaValidationError as error:
        raise DocumentationContractError("documentation contract schema violation: %s" % error) from error
    return validate_documentation_contract(contract, references or REFERENCES)


def validate_documentation_contract(contract, references):
    pages = contract["manual_pages"]
    slugs = [page["slug"] for page in pages]
    sources = [page["source"] for page in pages]
    _require(len(slugs) == len(set(slugs)), "documentation page slugs must be unique")
    _require(len(sources) == len(set(sources)), "documentation page sources must be unique")
    _require(all(Path(source).name == source and Path(source).stem == slug for source, slug in zip(sources, slugs)),
             "documentation page source must be a safe top-level Markdown file matching its slug")
    expected = {path.name for path in Path(references).glob("*.md")}
    _require(set(sources) == expected, "documentation inventory differs: missing %s; unexpected %s" % (
        ", ".join(sorted(expected - set(sources))) or "none", ", ".join(sorted(set(sources) - expected)) or "none"))
    positions = [(page["section_order"], page["order"]) for page in pages]
    _require(len(positions) == len(set(positions)), "documentation navigation positions must be unique")
    pagination = sorted(page["pagination_order"] for page in pages)
    _require(pagination == list(range(1, len(pages) + 1)), "documentation pagination must be contiguous")
    topics = contract["required_topics"]
    covered = [topic for page in pages for topic in page["topics"]]
    _require(set(covered) == set(topics), "documentation topics are not completely covered")
    _require(len(covered) == len(set(covered)), "documentation topics must have one primary owner")
    _require({item["id"] for item in contract["surfaces"]} == REQUIRED_SURFACES,
             "documentation surfaces must be exactly main, hosted, and bundled")
    _require({item["kind"] for item in contract["route_dispositions"]} == REQUIRED_ROUTES,
             "documentation route dispositions are incomplete")
    _require({item["id"] for item in contract["graphics"]} == REQUIRED_GRAPHICS,
             "documentation overview graphics are incomplete")
    disposition_sources = {item["source"] for item in contract["source_dispositions"]}
    expected_dispositions = {"skill/references/%s" % source for source in sources}
    _require(expected_dispositions.issubset(disposition_sources),
             "documentation source dispositions omit manual pages: %s" %
             ", ".join(sorted(expected_dispositions - disposition_sources)))
    return contract


def manual_catalog(contract=None):
    contract = contract or load_documentation_contract()
    return sorted((copy.deepcopy(page) for page in contract["manual_pages"]), key=lambda page: page["pagination_order"])


def validate_route_dispositions(routes, contract=None):
    contract = contract or load_documentation_contract()
    policies = {item["kind"]: item for item in contract["route_dispositions"]}
    for route in routes:
        if route.get("kind") in REQUIRED_ROUTES:
            policy = policies[route["kind"]]
            _require(policy["action"] == "preserve" and policy["destination"],
                     "documentation route lacks a preserved destination: %s" % route["kind"])
    return routes


def _safe_kit_file(kit, relative):
    _require(isinstance(relative, str) and relative and "\\" not in relative, "documentation fact path is unsafe: %s" % relative)
    pure = PurePosixPath(relative)
    _require(not pure.is_absolute() and ".." not in pure.parts and ":" not in pure.parts[0], "documentation fact path is unsafe: %s" % relative)
    path = Path(kit).joinpath(*pure.parts)
    _require(path.is_file(), "documentation fact path is missing: %s" % relative)
    return path


def build_documentation_facts(contract, consumer, kit):
    authority = consumer["authority"]
    source_brand = _read_json(_safe_kit_file(kit, authority["brand_source"]))
    facts = {
        "schema_version": 1,
        "documentation_contract_version": contract["contract_version"],
        "brand": copy.deepcopy(consumer["brand"]),
        "versions": copy.deepcopy(consumer["versions"]),
        "bindings": {
            "interface_canon": authority["interface_canon"],
            "component_recipes": authority["component_recipes"],
            "web_adapter": authority["web_adapter"],
            "web_support_matrix": authority["support_matrix"],
            "egui_adapter": authority["egui_adapter"],
            "egui_support_matrix": authority["egui_support_matrix"],
        },
        "rules": {
            "inheritance": (source_brand.get("affiliation") or {}).get("inheritance", "independent"),
            "overrides": copy.deepcopy((source_brand.get("interface") or {}).get("overrides") or {}),
        },
        "authority": {"precedence": copy.deepcopy(authority["precedence"]), "permitted_exceptions": copy.deepcopy(authority["permitted_exceptions"])},
        "verification": copy.deepcopy(consumer["verification"]),
        "recovery": copy.deepcopy(consumer["recovery"]),
        "capability_gap": copy.deepcopy(consumer["capability_gap"]),
        "hosted": {"manual_path": "/docs/", "scope": "Current generated kit only. Older pinned kits remain governed by their bundled contracts."},
        "bundled": {"facts_path": "enforcement/documentation-facts.json", "authority": "These pinned delivered bytes remain authoritative offline.", "latest_substitution_allowed": False},
    }
    verify_documentation_facts(facts, contract, consumer, kit)
    return facts


def verify_documentation_facts(facts, contract, consumer, kit):
    expected_fields = {"schema_version"} | set(contract["shared_fact_fields"])
    _require(set(facts) == expected_fields, "documentation fact fields differ from the contract")
    _require(facts["schema_version"] == 1, "documentation fact schema version is unsupported")
    _require(facts["documentation_contract_version"] == contract["contract_version"], "documentation contract version disagrees")
    for field in ("brand", "versions", "verification", "recovery", "capability_gap"):
        _require(facts[field] == consumer[field], "documentation facts disagree with consumer contract: %s" % field)
    authority = consumer["authority"]
    expected_bindings = {
        "interface_canon": authority["interface_canon"], "component_recipes": authority["component_recipes"],
        "web_adapter": authority["web_adapter"], "web_support_matrix": authority["support_matrix"],
        "egui_adapter": authority["egui_adapter"], "egui_support_matrix": authority["egui_support_matrix"],
    }
    _require(facts["bindings"] == expected_bindings, "documentation binding facts disagree")
    source_brand = _read_json(_safe_kit_file(kit, authority["brand_source"]))
    expected_rules = {"inheritance": (source_brand.get("affiliation") or {}).get("inheritance", "independent"),
                      "overrides": (source_brand.get("interface") or {}).get("overrides") or {}}
    _require(facts["rules"] == expected_rules, "documentation inherited or overridden rules disagree")
    _require(facts["authority"] == {"precedence": authority["precedence"], "permitted_exceptions": authority["permitted_exceptions"]},
             "documentation authority facts disagree")
    for relative in list(facts["bindings"].values()) + [facts["recovery"]["path"], facts["capability_gap"]["template_path"]]:
        _safe_kit_file(kit, relative)
    _require(facts["hosted"]["manual_path"] == "/docs/", "documentation manual destination is invalid")
    _require(facts["bundled"]["latest_substitution_allowed"] is False, "documentation recovery cannot allow latest substitution")
    return facts


def render_implementation(facts, governed_rules):
    versions = facts["versions"]
    rows = "\n".join("| %s | `%s` |" % (label, versions[key]) for key, label in (
        ("canon_version", "Brand Canon"), ("interface_canon_version", "Interface Canon"),
        ("component_recipe_version", "Component recipes"), ("web_react_adapter_version", "Web/React adapter"),
        ("egui_adapter_version", "egui adapter"), ("compiler_version", "BrandBuilder"), ("brand_version", "Brand")))
    bindings = "\n".join("- **%s:** `%s`" % (name.replace("_", " ").title(), path) for name, path in facts["bindings"].items())
    overrides = facts["rules"]["overrides"]
    rules = ("Inheritance mode: `%s`.\n\nDeclared interface overrides:\n%s" %
             (facts["rules"]["inheritance"], "\n".join("- `%s`: `%s`" % item for item in sorted(overrides.items())) if overrides else "- None."))
    checks = "\n".join("- `%s`" % command for command in facts["verification"]["entry_points"])
    return """# Implementation Contract: {title}

Generated from `enforcement/documentation-facts.json` under documentation contract `{documentation}`. This file describes the exact delivered kit and remains authoritative offline.

## Exact versions

| Domain | Version |
| --- | --- |
{rows}

## Bindings

{bindings}

## Inheritance and overrides

{interface_rules}

Follow authority in this order: {precedence}.

## Verification

{checks}

Success means {success}.

## Offline recovery

Verify `{sha}` for `{distribution}`, then extract it to `{extract}`. Use the delivered bundle and never substitute an unspecified latest release.

Capability gaps stay local at `{gap}` until a human explicitly authorizes upstream submission.

For shared architecture and extension guidance, read [{manual}]({manual_url}). The hosted reference describes only the current generated kit. This bundled contract continues to govern these pinned delivered bytes.

## Brand-specific governed rules

{rules}
""".format(title=facts["brand"]["title"], documentation=facts["documentation_contract_version"], rows=rows,
           bindings=bindings, interface_rules=rules, precedence=" -> ".join("`%s`" % item for item in facts["authority"]["precedence"]),
           checks=checks, success=facts["verification"]["success"], sha=facts["recovery"]["sha256"],
           distribution=facts["recovery"]["path"], extract=facts["recovery"]["extract_to"],
           gap=facts["capability_gap"]["template_path"], manual=facts["hosted"]["manual_path"],
           manual_url=HOSTED_MANUAL_ORIGIN + facts["hosted"]["manual_path"], rules=governed_rules.strip())


def verify_rendered_implementation(text, facts):
    _require("documentation-facts.json" in text and facts["documentation_contract_version"] in text,
             "implementation guidance does not identify its documentation facts")
    for version in facts["versions"].values():
        _require("`%s`" % version in text, "implementation guidance omits version %s" % version)
    for path in facts["bindings"].values():
        _require("`%s`" % path in text, "implementation guidance omits binding %s" % path)
    _require(facts["recovery"]["sha256"] in text and "latest" in text.lower(), "implementation recovery guidance is incomplete")
    manual_url = HOSTED_MANUAL_ORIGIN + facts["hosted"]["manual_path"]
    _require("[%s](%s)" % (facts["hosted"]["manual_path"], manual_url) in text,
             "implementation guidance does not use the portable hosted-manual URL")
    return text
