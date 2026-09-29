#!/usr/bin/env python3
"""Approved message roles and literal public projections."""

import re


CORE_ROLES = ("slogan", "short_description", "long_description")
OPTIONAL_ROLES = ("introductory_statement", "positioning", "mission", "vision", "values", "brand_promise")
USES = {"visual-guide", "strategy-reference", "social-image", "site-metadata", "consumer-data"}
DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")


class MessageError(ValueError):
    """A message has no valid independent owner decision."""


def _require(condition, detail):
    if not condition:
        raise MessageError(detail)


def validate_messaging(brand):
    """Validate approval and intended use without promoting another field."""
    records = brand.get("messaging")
    _require(isinstance(records, dict), "messaging must be an object")
    _require(set(CORE_ROLES).issubset(records), "messaging lacks a core role")
    _require(set(records).issubset(set(CORE_ROLES + OPTIONAL_ROLES)), "messaging has an unknown role")
    for role, record in records.items():
        _require(isinstance(record, dict), "messaging.%s must be an object" % role)
        status = record.get("status")
        _require(status in {"approved", "absent", "unresolved"}, "messaging.%s has invalid status" % role)
        if status != "approved":
            _require(set(record) == {"status"}, "messaging.%s %s cannot publish text" % (role, status))
            continue
        _require(set(record) == {"status", "text", "uses", "source", "approved_by", "approved_on"},
                 "messaging.%s approval fields are incomplete" % role)
        text = record["text"]
        _require(isinstance(text, str) and text and text.strip() == text and "\r" not in text
                 and "\n" not in text, "messaging.%s approved text is invalid" % role)
        uses = record["uses"]
        _require(isinstance(uses, list) and bool(uses) and all(isinstance(use, str) for use in uses)
                 and len(uses) == len(set(uses))
                 and set(uses).issubset(USES), "messaging.%s uses are invalid" % role)
        _require(all(isinstance(record[key], str) and record[key].strip() == record[key]
                     and record[key] for key in ("source", "approved_by")),
                 "messaging.%s approval provenance is incomplete" % role)
        _require(isinstance(record["approved_on"], str) and DATE.fullmatch(record["approved_on"]),
                 "messaging.%s approval date is invalid" % role)
        if role == "slogan" and "social-image" in uses:
            social = brand.get("social_copy") or {}
            _require(social.get("slogan") == text, "messaging.slogan differs from approved social copy")
    return records


def approved_messages(brand, use):
    """Return only exact owner-approved text allowed for the named surface."""
    _require(use in USES, "unknown message use")
    records = validate_messaging(brand)
    return {role: record["text"] for role, record in records.items()
            if record["status"] == "approved" and use in record["uses"]}
