#!/usr/bin/env python3
"""Validate the offline reference library and local manual citations."""

from __future__ import annotations

import re
from pathlib import Path


REFERENCE_HEADING = re.compile(r"^### (REF-[A-Z0-9-]+)$", re.MULTILINE)
LOCAL_LINK = re.compile(r"(?<!!)\]\((?:\./)?([a-z0-9-]+\.md)(?:#([a-z0-9-]+))?\)")
ENTRY_FIELDS = ("**Source:**", "**Class:**", "**Use:**", "**Limit:**")


def validate_references(root: Path) -> set[str]:
    """Return stable reference IDs or raise on malformed entries/citations."""
    root = Path(root)
    library = root / "references.md"
    if not library.is_file():
        raise ValueError("reference library is missing")
    text = library.read_text(encoding="utf-8")
    headings = list(REFERENCE_HEADING.finditer(text))
    if not headings:
        raise ValueError("reference library has no stable IDs")
    ids = [match.group(1).lower() for match in headings]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate reference ID")
    for index, heading in enumerate(headings):
        section = text[heading.end():headings[index + 1].start() if index + 1 < len(headings) else len(text)]
        # The maintenance section follows the final entry and does not affect its fields.
        missing = [field for field in ENTRY_FIELDS if field not in section]
        if missing:
            raise ValueError("%s omits %s" % (heading.group(1), ", ".join(missing)))
    for page in root.glob("*.md"):
        source = page.read_text(encoding="utf-8")
        for match in LOCAL_LINK.finditer(source):
            target, anchor = match.groups()
            if not (root / target).is_file():
                raise ValueError("%s links missing manual %s" % (page.name, target))
            if target == "references.md" and anchor and anchor not in ids:
                raise ValueError("%s cites unknown reference %s" % (page.name, anchor))
    return set(ids)


if __name__ == "__main__":
    validate_references(Path(__file__).resolve().parents[1] / "skill" / "references")
    print("Reference IDs and local citations verified")
