#!/usr/bin/env python3
"""Enforce single-physical-line prose in public planning records."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = (
    ROOT / "docs" / "decisions.md",
    ROOT / "docs" / "disposition.md",
    ROOT / "specs" / "001-brand-system-foundation" / "work-order.md",
    ROOT / "specs" / "002-publication-completion" / "spec.md",
    ROOT / "specs" / "002-publication-completion" / "plan.md",
    ROOT / "specs" / "002-publication-completion" / "tasks.md",
)
BLOCK_START = re.compile(r"^\s*(```|~~~)")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]\s|\d+\.\s)")
INDENTED_CODE = re.compile(r"^(?: {4}|\t)")
STRUCTURE = re.compile(r"^(?:#{1,6}\s|>|\||<!--|-->)")


def wrapped_prose(path):
    """Return line pairs that look like manually wrapped prose paragraphs."""
    problems = []
    previous_prose = None
    fence = None
    indented_code = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = BLOCK_START.match(line)
        if match:
            marker = match.group(1)
            fence = None if fence == marker else marker
            previous_prose = None
            continue
        if fence:
            continue
        if not line.strip():
            previous_prose = None
            indented_code = False
            continue
        if LIST_ITEM.match(line):
            previous_prose = number
            indented_code = False
            continue
        if INDENTED_CODE.match(line) and previous_prose is None:
            indented_code = True
            continue
        if indented_code and INDENTED_CODE.match(line):
            continue
        indented_code = False
        if STRUCTURE.match(line):
            previous_prose = None
            continue
        if previous_prose is not None:
            problems.append((previous_prose, number))
        previous_prose = number
    return problems


def main():
    failures = []
    for path in TARGETS:
        if not path.exists():
            continue
        for first, second in wrapped_prose(path):
            failures.append(f"{path.relative_to(ROOT)}:{first}-{second}: prose must remain on one physical line")
    if failures:
        raise SystemExit("\n".join(failures))
    print("Markdown prose line policy: passed")


if __name__ == "__main__":
    main()
