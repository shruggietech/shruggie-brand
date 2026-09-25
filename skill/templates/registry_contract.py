#!/usr/bin/env python3
"""Offline shadcn schema and delivery checks for generated registry items."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

from jsonschema import Draft7Validator


REFERENCES = Path(__file__).resolve().parents[1] / "references" / "shadcn"
CATALOG_SCHEMA_URL = "https://ui.shadcn.com/schema/registry.json"
ITEM_SCHEMA_URL = "https://ui.shadcn.com/schema/registry-item.json"
NAME = re.compile(r"[a-z0-9][a-z0-9-]*\Z")
PATH = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]*\Z")
TARGET = re.compile(r"@(components|ui|lib|hooks)/[A-Za-z0-9][A-Za-z0-9._/-]*\Z")


def _schemas():
    catalog = json.loads((REFERENCES / "registry.json").read_text(encoding="utf-8"))
    item = json.loads((REFERENCES / "registry-item.json").read_text(encoding="utf-8"))
    Draft7Validator.check_schema(catalog)
    Draft7Validator.check_schema(item)
    offline_catalog = copy.deepcopy(catalog)
    offline_catalog["properties"]["items"]["items"] = item
    offline_catalog["definitions"] = item.get("definitions", {})
    return Draft7Validator(offline_catalog), Draft7Validator(item)


def _check_schema(validator, data, label):
    errors = sorted(validator.iter_errors(data), key=lambda error: (list(map(str, error.absolute_path)), error.message))
    if errors:
        first = errors[0]
        location = ".".join(map(str, first.absolute_path)) or "root"
        raise ValueError("%s schema invalid at %s: %s" % (label, location, first.message))


def _safe_path(value, expression):
    return (isinstance(value, str) and expression.fullmatch(value) is not None
            and all(part not in ("", ".", "..") for part in value.split("/"))
            and not value.startswith("/") and "\\" not in value)


def validate_registry(directory: Path, slug: str) -> None:
    """Validate one generated catalog, all direct endpoints, and their parity."""
    directory = Path(directory)
    catalog_path = directory / "registry.json"
    if not catalog_path.is_file():
        raise ValueError("%s: registry catalog is missing" % slug)
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ValueError("%s: registry catalog is unreadable: %s" % (slug, error)) from error
    if not isinstance(catalog, dict):
        raise ValueError("%s: registry catalog must be an object" % slug)
    catalog_validator, item_validator = _schemas()
    if catalog.get("$schema") != CATALOG_SCHEMA_URL:
        raise ValueError("%s: registry catalog schema URL is invalid" % slug)
    if catalog.get("name") != slug or not NAME.fullmatch(slug):
        raise ValueError("%s: registry catalog name mismatch" % slug)
    items = catalog.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("%s: registry catalog is empty" % slug)
    if any(not isinstance(item, dict) for item in items):
        raise ValueError("%s: registry catalog contains a non-object item" % slug)
    names = [item.get("name") for item in items]
    if any(not isinstance(name, str) or not NAME.fullmatch(name) for name in names):
        raise ValueError("%s: registry catalog contains an unsafe item" % slug)
    if len(names) != len(set(names)):
        raise ValueError("%s: registry catalog contains a duplicate item" % slug)
    if "theme" not in names:
        raise ValueError("%s: registry theme item is missing" % slug)
    expected_files = {"registry.json"} | {name + ".json" for name in names}
    actual_files = {path.name for path in directory.glob("*.json")}
    undeclared = sorted(actual_files - expected_files)
    if undeclared:
        raise ValueError("%s: undeclared registry endpoint: %s" % (slug, undeclared[0]))
    targets = set()
    paths = set()
    for item in items:
        name = item["name"]
        label = "%s/%s" % (slug, name)
        if item.get("$schema") != ITEM_SCHEMA_URL:
            raise ValueError("%s schema URL is invalid" % label)
        _check_schema(item_validator, item, label)
        if not all(isinstance(item.get(field), str) and item[field].strip() for field in ("title", "description")):
            raise ValueError("%s title or description is empty" % label)
        direct_path = directory / (name + ".json")
        if not direct_path.is_file():
            raise ValueError("%s advertised endpoint is missing" % label)
        try:
            direct = json.loads(direct_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise ValueError("%s direct endpoint is unreadable: %s" % (label, error)) from error
        _check_schema(item_validator, direct, label + " direct")
        if item != direct:
            raise ValueError("%s catalog and direct payload mismatch" % label)
        if item.get("type") == "registry:theme":
            css_vars = item.get("cssVars") or {}
            if name != "theme" or not all(isinstance(css_vars.get(mode), dict) and css_vars[mode] for mode in ("light", "dark")):
                raise ValueError("%s theme variables are incomplete" % label)
        elif item.get("type") == "registry:ui":
            files = item.get("files")
            if not isinstance(files, list) or not files:
                raise ValueError("%s UI files are empty" % label)
            for source in files:
                if not _safe_path(source.get("path"), PATH):
                    raise ValueError("%s file path is unsafe" % label)
                if source["path"] in paths:
                    raise ValueError("%s file path is duplicated" % label)
                paths.add(source["path"])
                target = source.get("target")
                if not _safe_path(target, TARGET):
                    raise ValueError("%s file target is unsafe or missing" % label)
                if target in targets:
                    raise ValueError("%s file target is duplicated" % label)
                targets.add(target)
                if source.get("type") != "registry:ui" or not isinstance(source.get("content"), str) or not source["content"].strip():
                    raise ValueError("%s UI file content is empty or invalid" % label)
        else:
            raise ValueError("%s unsupported registry item type: %s" % (label, item.get("type")))
        for dependency in item.get("registryDependencies", []):
            if not dependency.strip():
                raise ValueError("%s registry dependency is empty" % label)
            if dependency not in names and not (dependency.startswith("https://") or dependency.startswith("@")):
                raise ValueError("%s registry dependency is missing: %s" % (label, dependency))
        for dependency in item.get("dependencies", []):
            if not dependency.strip():
                raise ValueError("%s package dependency is empty" % label)
    _check_schema(catalog_validator, catalog, "%s catalog" % slug)
