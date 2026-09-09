#!/usr/bin/env python3
"""Create deterministic release archives from a verified dist/ tree."""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path

from release_contract import (
    LICENSES,
    PRODUCTION,
    current_version,
    load_metadata,
    verify_brand_archive,
    verify_release_directory,
)


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill"
OUTPUT = ROOT / "release"
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


def write_brand_archive(
    source: Path,
    archive_path: Path,
    *,
    root: Path = ROOT,
    expected_canon: str | None = None,
) -> Path:
    """Write and certify a complete brand archive before atomically publishing it."""
    source = source.resolve()
    archive_path = archive_path.resolve()
    if not source.is_dir():
        raise ValueError(f"missing built kit: {source.name}")
    brand_path = source / "brand.json"
    if not brand_path.is_file():
        raise ValueError(f"missing built kit metadata: {source.name}")
    brand = json.loads(brand_path.read_text(encoding="utf-8"))
    slug = brand.get("slug")
    version = brand.get("version")
    if slug != source.name or not isinstance(version, str) or not version:
        raise ValueError(f"built kit identity does not match source directory: {source.name}")
    expected_name = f"{slug}-brand-{version}.zip"
    if archive_path.name != expected_name:
        raise ValueError(f"brand archive filename must be {expected_name}")
    try:
        archive_path.relative_to(source)
    except ValueError:
        pass
    else:
        raise ValueError("brand archive destination must be outside its source kit")

    archive_path.parent.mkdir(parents=True, exist_ok=True)
    staged = archive_path.with_name(f".{archive_path.name}.tmp")
    staged.unlink(missing_ok=True)
    try:
        with zipfile.ZipFile(staged, "w") as archive:
            add_tree(archive, source)
            existing = set(archive.namelist())
            for name in LICENSES:
                if name not in existing:
                    add_bytes(archive, name, (root / name).read_bytes())
        verify_brand_archive(
            staged,
            slug,
            version,
            expected_canon=expected_canon,
            root=root,
        )
        staged.replace(archive_path)
    except Exception:
        staged.unlink(missing_ok=True)
        raise
    return archive_path


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
        brand = json.loads((source / "brand.json").read_text(encoding="utf-8"))
        archive_path = OUTPUT / f"{slug}-brand-{brand['version']}.zip"
        write_brand_archive(
            source,
            archive_path,
            expected_canon=str(metadata["canon_version"]),
        )

    for path in (skill_bundle, portable):
        assert_licenses(path)
    verify_release_directory(OUTPUT, metadata)
    print("\n".join(path.name for path in sorted(OUTPUT.iterdir()) if path.is_file()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
