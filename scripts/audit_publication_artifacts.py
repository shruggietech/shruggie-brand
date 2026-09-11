#!/usr/bin/env python3
"""Fail closed on unsafe or incomplete publication artifact trees."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, Iterable, Optional, Set


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = (
    "covarity",
    "cueson",
    "eso-weave",
    "fragcap",
    "glitchpad",
    "go-schedule",
    "i-heart-pr-tours",
    "shruggietech",
)


def _contained_directory(root: Path, value: Path, label: str) -> Path:
    root = root.resolve()
    candidate = value if value.is_absolute() else root / value
    if candidate.is_symlink():
        raise ValueError("%s root is a symbolic link: %s" % (label, candidate))
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError as error:
        raise ValueError("%s directory is missing: %s" % (label, candidate)) from error
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise ValueError("%s directory is outside repository root: %s" % (label, resolved)) from error
    if not resolved.is_dir():
        raise ValueError("%s path is not a directory: %s" % (label, resolved))
    return resolved


def _expected_markers(kind: str) -> Set[Path]:
    if kind == "kits":
        return {Path(slug) / "icons" / ".iconkit-generated.json" for slug in PRODUCTION}
    return {
        Path(slug) / "downloads" / "files" / "icons" / ".iconkit-generated.json"
        for slug in PRODUCTION
    }


def _hidden(relative: Path) -> bool:
    return any(part.startswith(".") for part in relative.parts)


def _inspect_tree(path: Path, kind: str) -> int:
    expected = _expected_markers(kind)
    markers: Set[Path] = set()
    problems = []

    for parent, directories, filenames in os.walk(str(path), followlinks=False):
        parent_path = Path(parent)
        for name in directories + filenames:
            item = parent_path / name
            relative = item.relative_to(path)
            if item.is_symlink():
                problems.append("%s contains symbolic link: %s" % (kind, relative.as_posix()))
                continue
            if item.is_file() and item.stat().st_nlink > 1:
                problems.append("%s contains hard link: %s" % (kind, relative.as_posix()))
            if _hidden(relative):
                if item.is_file() and relative in expected:
                    markers.add(relative)
                else:
                    problems.append(
                        "%s contains unexpected hidden path: %s" %
                        (kind, relative.as_posix())
                    )

    missing = sorted(expected - markers, key=lambda item: item.as_posix())
    extra = sorted(markers - expected, key=lambda item: item.as_posix())
    if missing or extra:
        details = []
        if missing:
            details.append("missing %s" % ", ".join(item.as_posix() for item in missing))
        if extra:
            details.append("extra %s" % ", ".join(item.as_posix() for item in extra))
        problems.append("%s marker inventory mismatch: %s" % (kind, "; ".join(details)))

    if problems:
        raise ValueError("; ".join(problems))
    return len(markers)


def audit(root: Path, kits: Path, site: Path) -> Dict[str, int]:
    """Audit both publication trees and return their governed marker counts."""
    root = root.resolve()
    kits_path = _contained_directory(root, kits, "kits")
    site_path = _contained_directory(root, site, "site")
    return {
        "kit_markers": _inspect_tree(kits_path, "kits"),
        "site_markers": _inspect_tree(site_path, "site"),
    }


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kits", type=Path, required=True)
    parser.add_argument("--site", type=Path, required=True)
    args = parser.parse_args(argv)
    result = audit(ROOT, args.kits, args.site)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
