#!/usr/bin/env python3
"""Small offline validator for the JSON Schema vocabulary shipped by BrandBuilder."""

from __future__ import annotations

import json
import re


class SchemaValidationError(ValueError):
    pass


def _fail(path, message):
    raise SchemaValidationError("%s %s" % (path, message))


def _type_matches(value, expected):
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    _fail("$schema", "uses unsupported type %r" % expected)


def _resolve_reference(root, reference):
    if not reference.startswith("#/"):
        _fail("$schema", "uses non-local reference %s" % reference)
    current = root
    for encoded in reference[2:].split("/"):
        key = encoded.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or key not in current:
            _fail("$schema", "has unresolved reference %s" % reference)
        current = current[key]
    return current


def validate_json_schema(instance, schema, root=None, path="$"):
    """Validate an instance against the closed schema subset used by shipped contracts."""
    if not isinstance(schema, dict):
        _fail("$schema", "must be an object")
    root = schema if root is None else root
    if "$ref" in schema:
        return validate_json_schema(instance, _resolve_reference(root, schema["$ref"]), root, path)
    if "oneOf" in schema:
        matches = 0
        for option in schema["oneOf"]:
            try:
                validate_json_schema(instance, option, root, path)
            except SchemaValidationError:
                continue
            matches += 1
        if matches != 1:
            _fail(path, "must match exactly one allowed schema")
        return instance
    if "const" in schema and instance != schema["const"]:
        _fail(path, "must equal %s" % json.dumps(schema["const"], ensure_ascii=False))
    expected = schema.get("type")
    if expected is not None:
        allowed = expected if isinstance(expected, list) else [expected]
        if not any(_type_matches(instance, item) for item in allowed):
            _fail(path, "has invalid type")
    if isinstance(instance, dict):
        required = schema.get("required", [])
        missing = sorted(set(required) - set(instance))
        if missing:
            _fail(path, "is missing required fields: %s" % ", ".join(missing))
        if len(instance) < schema.get("minProperties", 0):
            _fail(path, "has too few properties")
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, value in instance.items():
            child = "%s.%s" % (path, key)
            if key in properties:
                validate_json_schema(value, properties[key], root, child)
            elif additional is False:
                _fail(path, "contains unsupported field %s" % key)
            elif isinstance(additional, dict):
                validate_json_schema(value, additional, root, child)
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            _fail(path, "has too few items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in instance]
            if len(encoded) != len(set(encoded)):
                _fail(path, "contains duplicate items")
        if "items" in schema:
            for index, value in enumerate(instance):
                validate_json_schema(value, schema["items"], root, "%s[%d]" % (path, index))
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            _fail(path, "is too short")
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            _fail(path, "does not match the required pattern")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            _fail(path, "is below the minimum")
        if "exclusiveMinimum" in schema and instance <= schema["exclusiveMinimum"]:
            _fail(path, "is not above the exclusive minimum")
    return instance
