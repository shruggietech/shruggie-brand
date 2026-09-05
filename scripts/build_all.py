#!/usr/bin/env python3
"""Stage source-only brand definitions and build every requested kit."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = (ROOT / "dist").resolve()
FONTS = ROOT / "assets" / "fonts"
TEMPLATES = ROOT / "skill" / "templates"
BUILDER = TEMPLATES / "build_kit.py"
sys.path.insert(0, str(TEMPLATES))
from process_utils import hidden_process_kwargs


def sources() -> dict[str, Path]:
    found: dict[str, Path] = {}
    for parent in (ROOT / "brands",):
        if not parent.exists():
            continue
        for child in sorted(parent.iterdir()):
            if child.is_dir() and (child / "brand.json").is_file():
                slug = child.name[:-6] if child.name.endswith("-brand") else child.name
                if slug in found:
                    raise ValueError(f"duplicate build slug: {slug}")
                found[slug] = child
    return found


def clean_destination(destination: Path) -> None:
    resolved = destination.resolve()
    if resolved.parent != DIST:
        raise ValueError(f"refusing to remove path outside dist: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def stage(source: Path, destination: Path) -> None:
    clean_destination(destination)
    shutil.copytree(source, destination)
    shutil.copytree(FONTS, destination / "fonts")


def build(slug: str, source: Path) -> int:
    destination = DIST / slug
    print(f"\n=== {slug} ===", flush=True)
    stage(source, destination)
    completed = subprocess.run(
        [sys.executable, str(BUILDER), str(destination)],
        cwd=ROOT,
        check=False,
        **hidden_process_kwargs(),
    )
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slugs", nargs="*", help="Build only these slugs")
    parser.add_argument("--list", action="store_true", help="List discovered slugs")
    args = parser.parse_args()

    available = sources()
    if args.list:
        print("\n".join(available))
        return 0

    selected = args.slugs or list(available)
    unknown = sorted(set(selected) - set(available))
    if unknown:
        parser.error("unknown slug(s): " + ", ".join(unknown))

    DIST.mkdir(parents=True, exist_ok=True)
    if not args.slugs:
        for stale in DIST.iterdir():
            if stale.is_dir() and (stale / "brand.json").is_file() and stale.name not in available:
                clean_destination(stale)
    failures = {slug: build(slug, available[slug]) for slug in selected}
    failed = {slug: code for slug, code in failures.items() if code}
    if failed:
        print("\nFAILED: " + ", ".join(f"{slug} ({code})" for slug, code in failed.items()))
        return 1
    print(f"\nBuilt {len(selected)} kit(s) with zero reported problems.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
