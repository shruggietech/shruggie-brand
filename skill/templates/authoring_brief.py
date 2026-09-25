#!/usr/bin/env python3
"""Validate private authoring briefs and pre-approval Gate 2 review packets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


TOPICS = {
    "purpose", "audience", "positioning", "voice", "references", "identity",
    "lockups", "social_copy", "formal_palette", "interface_cues",
    "typography", "deliverables", "affiliation",
}
REVIEW_ASSETS = {
    "full-mark", "reduced-mark", "wide-lockup", "stacked-lockup",
    "social-share-image", "formal-palette", "interface-cues", "typography",
    "representative-application", "derivative-manifest",
}
VISUAL_ASSETS = {
    "full-mark", "reduced-mark", "wide-lockup", "stacked-lockup",
    "social-share-image", "representative-application",
}
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")


class BriefError(ValueError):
    """A private authoring record is incomplete or inconsistent."""


def require(condition, message):
    if not condition:
        raise BriefError(message)


def _text(value):
    return isinstance(value, str) and bool(value.strip()) and value == value.strip()


def _lines(value, text):
    return (isinstance(value, list) and bool(value)
            and all(_text(item) and "\n" not in item for item in value)
            and " ".join(value) == text)


def validate_brief(brief):
    """Allow a draft with unresolved choices, but never synthesize approval."""
    require(isinstance(brief, dict) and set(brief) == {"schema_version", "topics", "social_copy"},
            "brief fields are incomplete or unsupported")
    require(brief["schema_version"] == 1, "unsupported brief schema")
    topics = brief["topics"]
    require(isinstance(topics, dict) and set(topics) == TOPICS, "brief topics are incomplete")
    for name, value in topics.items():
        require(isinstance(value, dict) and set(value) == {"facts", "constraints", "proposals", "unresolved"},
                "brief topic %s needs facts, constraints, proposals, and unresolved" % name)
        for category, entries in value.items():
            require(isinstance(entries, list) and all(_text(item) for item in entries),
                    "brief topic %s has invalid %s" % (name, category))
    social = brief["social_copy"]
    require(isinstance(social, dict) and social.get("status") in {"unresolved", "approved"},
            "social copy status must be unresolved or approved")
    if social["status"] == "unresolved":
        require(set(social) == {"status"}, "unresolved social copy cannot carry approval")
        return brief
    require(set(social) == {"status", "slogan", "description", "layout", "slogan_lines",
                            "description_lines", "approved_source", "approved_by", "approved_on"},
            "approved social copy fields are incomplete")
    require(_text(social["slogan"]) and _lines(social["slogan_lines"], social["slogan"]),
            "approved slogan or line breaks are invalid")
    require(_text(social["approved_source"]) and _text(social["approved_by"])
            and isinstance(social["approved_on"], str)
            and DATE.fullmatch(social["approved_on"]), "social copy lacks approval source, approver, or date")
    if social["layout"] == "slogan-only":
        require(social["description"] is None and social["description_lines"] == [],
                "slogan-only social image cannot include a description")
    else:
        require(social["layout"] == "slogan-and-description" and _text(social["description"])
                and _lines(social["description_lines"], social["description"]),
                "two-line social image needs exact approved description and line breaks")
    return brief


def _contained_file(root, relative):
    require(isinstance(relative, str) and relative and "\\" not in relative,
            "review asset path is invalid")
    candidate = Path(relative)
    require(not candidate.is_absolute() and ".." not in candidate.parts,
            "review asset path escapes private packet")
    cursor = root
    for part in candidate.parts:
        cursor = cursor / part
        require(not cursor.is_symlink(), "review asset path contains a symlink")
    resolved = cursor.resolve()
    require(resolved.is_file() and (root == resolved or root in resolved.parents),
            "review asset is missing or outside private packet")
    return resolved


def validate_gate_2_packet(brief, packet, root):
    """Require a complete, checksummed, private review packet before Gate 2."""
    validate_brief(brief)
    require(brief["social_copy"]["status"] == "approved", "social copy is unresolved")
    require(not brief["topics"]["social_copy"]["unresolved"],
            "social copy still has unresolved questions")
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), "private review root is missing or unsafe")
    root = root.resolve()
    require(isinstance(packet, dict) and set(packet) == {"schema_version", "gate_1", "gate_2",
                                                      "public_projection_enabled", "social_copy", "assets"},
            "Gate 2 packet fields are incomplete")
    require(packet["schema_version"] == 1 and packet["public_projection_enabled"] is False,
            "Gate 2 review must remain private")
    require(packet["social_copy"] == brief["social_copy"],
            "Gate 2 social copy differs from the approved brief")
    gate_1 = packet["gate_1"]
    require(isinstance(gate_1, dict) and set(gate_1) == {"status", "source_sha256"}
            and gate_1["status"] == "approved" and isinstance(gate_1["source_sha256"], str)
            and DIGEST.fullmatch(gate_1["source_sha256"]),
            "Gate 2 requires approved source-bound Gate 1 evidence")
    require(packet["gate_2"] == {"status": "pending"},
            "pre-approval Gate 2 packet must remain pending")
    assets = packet["assets"]
    require(isinstance(assets, dict) and REVIEW_ASSETS.issubset(set(assets)),
            "Gate 2 packet lacks a required review asset")
    paths = {}
    for role, item in assets.items():
        require(isinstance(item, dict) and set(item) == {"path", "sha256"}
                and isinstance(item["sha256"], str) and DIGEST.fullmatch(item["sha256"]),
                "Gate 2 review asset record is invalid: %s" % role)
        path = _contained_file(root, item["path"])
        require(hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"],
                "Gate 2 review asset hash differs: %s" % role)
        if role in VISUAL_ASSETS:
            require(path.suffix.lower() in {".png", ".svg"},
                    "Gate 2 visual asset must be a PNG or SVG: %s" % role)
            try:
                if path.suffix.lower() == ".svg":
                    from brand_contract import _validate_svg
                    _validate_svg(str(path))
                else:
                    from PIL import Image
                    with Image.open(path) as image:
                        image.verify()
                        require(image.format == "PNG", "Gate 2 PNG format differs: %s" % role)
            except (OSError, ValueError) as error:
                raise BriefError("Gate 2 visual asset is invalid: %s" % role) from error
        paths[role] = path
    require(len({paths["wide-lockup"], paths["stacked-lockup"], paths["social-share-image"]}) == 3,
            "wide, stacked, and social review images must be separate compositions")
    return packet


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="private authoring brief JSON")
    parser.add_argument("--gate-2", dest="packet", type=Path, help="private pending Gate 2 packet JSON")
    args = parser.parse_args()
    brief = json.loads(args.brief.read_text(encoding="utf-8"))
    validate_brief(brief)
    if args.packet:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        validate_gate_2_packet(brief, packet, args.packet.parent)
    print("private authoring evidence valid")


if __name__ == "__main__":
    main()
