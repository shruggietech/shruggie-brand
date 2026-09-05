#!/usr/bin/env python3
"""Create deterministic release archives from a verified dist/ tree."""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path

from release_contract import current_version, load_metadata, verify_release_directory


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill"
OUTPUT = ROOT / "release"
PRODUCTION = ("shruggietech", "fragcap", "go-schedule", "glitchpad", "covarity")
LICENSES = ("LICENSE", "NOTICE", "LICENSE-BRAND.md")
ZIP_TIME = (2026, 9, 3, 0, 0, 0)


def add_bytes(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data)


def add_tree(archive: zipfile.ZipFile, root: Path, *, omit: set[str] | None = None) -> None:
    omit = omit or set()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        if relative in omit or "__pycache__" in path.parts:
            continue
        add_bytes(archive, relative, path.read_bytes())


def assert_licenses(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        missing = [name for name in LICENSES if name not in archive.namelist()]
    if missing:
        raise ValueError(f"{path.name} lacks {', '.join(missing)}")


def resolve_version(root: Path, requested: str | None) -> str:
    return requested if requested is not None else current_version(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version")
    args = parser.parse_args()
    version = resolve_version(ROOT, args.version)
    metadata = load_metadata(ROOT, version)
    resolved_output = OUTPUT.resolve()
    if resolved_output.parent != ROOT.resolve():
        raise ValueError("refusing to clean release output outside repository root")
    if resolved_output.exists():
        shutil.rmtree(resolved_output)
    resolved_output.mkdir()

    skill_bundle = OUTPUT / f"shruggie-brandbuilder-{version}.skill"
    with zipfile.ZipFile(skill_bundle, "w") as archive:
        add_tree(archive, SKILL)

    portable = OUTPUT / f"shruggie-brandbuilder-{version}-portable.zip"
    with zipfile.ZipFile(portable, "w") as archive:
        add_tree(archive, SKILL, omit={"SKILL.md"})
        add_bytes(
            archive,
            "README.md",
            ("# shruggie-brandbuilder portable bundle\n\n"
             "Start with `AGENTS.md`. The skill instructions are adapted there for repository vendoring.\n").encode(),
        )

    for slug in PRODUCTION:
        source = ROOT / "dist" / slug
        if not (source / "brand.json").is_file():
            raise ValueError(f"missing built kit: {slug}")
        if not (source / "brand-guide.pdf").is_file():
            raise ValueError(f"missing required brand guide PDF: {slug}")
        brand = json.loads((source / "brand.json").read_text(encoding="utf-8"))
        archive_path = OUTPUT / f"{slug}-brand-{brand['version']}.zip"
        with zipfile.ZipFile(archive_path, "w") as archive:
            add_tree(archive, source)
            for name in LICENSES:
                if name not in archive.namelist():
                    add_bytes(archive, name, (ROOT / name).read_bytes())
        assert_licenses(archive_path)

    for path in (skill_bundle, portable):
        assert_licenses(path)
    verify_release_directory(OUTPUT, metadata)
    print("\n".join(path.name for path in sorted(OUTPUT.iterdir()) if path.is_file()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
