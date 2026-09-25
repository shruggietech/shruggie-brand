#!/usr/bin/env python3
"""Deterministic, dependency-free transforms for the published main manual."""

from __future__ import annotations

import json
import re
from typing import Any, Mapping


ALERT_TYPES = {"NOTE": "info", "WARNING": "warn", "CAUTION": "error"}
OVERVIEW_DESCRIPTION = "The repeatable ShruggieTech system for building complete, usable brand identities."


def convert_documentation_alerts(content: str) -> str:
    lines = content.splitlines()
    output: list[str] = []
    index = 0
    fenced = False
    marker = re.compile(r"^>\s*\[!([A-Z]+)\]\s*$")
    while index < len(lines):
        line = lines[index]
        if line.lstrip().startswith("```"):
            fenced = not fenced
            output.append(line)
            index += 1
            continue
        match = marker.match(line) if not fenced else None
        if not match:
            output.append(line)
            index += 1
            continue
        name = match.group(1)
        if name not in ALERT_TYPES:
            raise ValueError(f"unsupported documentation alert: {name}")
        body: list[str] = []
        index += 1
        while index < len(lines) and lines[index].startswith(">"):
            quoted = lines[index][1:]
            if quoted.startswith(" "):
                quoted = quoted[1:]
            body.append(quoted)
            index += 1
        if not any(part.strip() for part in body):
            raise ValueError(f"documentation alert {name} has no body")
        output.extend([f'<Callout type="{ALERT_TYPES[name]}">', *body, "</Callout>"])
    return "\n".join(output)


def derive_public_markdown(content: str) -> tuple[str, str]:
    lines = content.splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), "Brand system")
    pattern = re.compile(r"\b(?:Brand|Interface) Canon\b|\bcanon\b", re.IGNORECASE)

    def public_term(match: re.Match[str]) -> str:
        value = match.group(0)
        if value.lower() in {"brand canon", "interface canon"}:
            return value
        return "Brand system" if value[0].isupper() else "brand system"

    title = pattern.sub(public_term, title)
    removed_heading = False
    fenced = False
    output: list[str] = []
    retired_endorsement = re.compile(r"a shruggietech project", re.IGNORECASE)
    for line in lines:
        if not removed_heading and line.startswith("# "):
            removed_heading = True
            continue
        if line.lstrip().startswith("```"):
            fenced = not fenced
            output.append(line)
            continue
        if fenced:
            output.append(line)
            continue
        parts = re.split(r"(`[^`]*`)", line)
        for index in range(0, len(parts), 2):
            parts[index] = pattern.sub(public_term, parts[index])
            parts[index] = retired_endorsement.sub("Brand system by ShruggieTech", parts[index])
        output.append("".join(parts))
    normalized: list[str] = []
    index = 0
    fenced = False
    while index < len(output):
        line = output[index]
        if line.lstrip().startswith("```"):
            fenced = not fenced
            normalized.append(line)
            index += 1
            continue
        if not fenced and line.startswith("    "):
            block: list[str] = []
            while index < len(output):
                candidate = output[index]
                if candidate.startswith("    "):
                    block.append(candidate[4:])
                    index += 1
                elif not candidate.strip() and index + 1 < len(output) and output[index + 1].startswith("    "):
                    block.append("")
                    index += 1
                else:
                    break
            normalized.extend(["```text", *block, "```"])
            continue
        if not fenced:
            parts = re.split(r"(`[^`]*`)", line)
            for part_index in range(0, len(parts), 2):
                parts[part_index] = re.sub(r"<([^>]+)>", r"&lt;\1&gt;", parts[part_index])
            line = "".join(parts)
        normalized.append(line)
        index += 1
    return title, convert_documentation_alerts("\n".join(normalized)).strip() + "\n"


def identity_line(publication: Mapping[str, Any]) -> str:
    version = publication["version"]
    release_url = publication["releaseUrl"]
    skill_url = publication["skillUrl"]
    if publication["status"] == "release":
        return f"Documentation for BrandBuilder {version}. [Official release]({release_url}) and [exact skill asset]({skill_url})."
    if publication["status"] == "candidate":
        return f"Documentation for BrandBuilder {version}. Review candidate (not yet published). Planned [release]({release_url}) and [skill asset]({skill_url})."
    raise ValueError("unsupported documentation publication status")


def render_page(source: str, description: str, publication: Mapping[str, Any]) -> str:
    title, body = derive_public_markdown(source)
    frontmatter = f"---\ntitle: {json.dumps(title)}\ndescription: {json.dumps(description)}\n---\n\n"
    return frontmatter + identity_line(publication) + "\n\n" + body


def render_index(publication: Mapping[str, Any]) -> str:
    return ("---\ntitle: \"Documentation\"\ndescription: " + json.dumps(OVERVIEW_DESCRIPTION) + "\n---\n\n"
            "We turn strategy into a complete identity, then package the standards, assets, and implementation tools that keep it coherent in real work.\n\n"
            + identity_line(publication) + "\n\nExplore each part of the system below.\n")
