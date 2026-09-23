#!/usr/bin/env python3
"""Create deterministic release archives from a verified dist/ tree."""

from __future__ import annotations

import argparse
import hashlib
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
from interface_contract import package_identity, source_revision
from brand_contract import custom_assets


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill"
OUTPUT = ROOT / "release"
ZIP_TIME = (2026, 9, 3, 0, 0, 0)
GENERATED_DIRECTORIES = {"__pycache__", "node_modules", ".venv", "venv"}


def add_bytes(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data)


def add_tree(archive: zipfile.ZipFile, root: Path, *, omit: set[str] | None = None) -> None:
    omit = omit or set()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        if (relative in omit or GENERATED_DIRECTORIES.intersection(path.relative_to(root).parts)
                or path.suffix == ".pyc"):
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
    eligible = {item["id"] for item in custom_assets(brand, source, public_only=True)}
    withheld_paths = {item["source"]["path"] for item in brand.get("custom_assets", [])
                      if item["id"] not in eligible}
    shared_sources = withheld_paths & {item.get("path") for item in brand.get("authoritative_inputs", [])}
    if shared_sources:
        raise ValueError("non-public custom source is also required by canonical identity: %s" % ", ".join(sorted(shared_sources)))
    slug = brand.get("slug")
    version = brand.get("version")
    if slug != source.name or not isinstance(version, str) or not version:
        raise ValueError(f"built kit identity does not match source directory: {source.name}")
    bundle_path = source / "enforcement" / "bundle.json"
    if not bundle_path.is_file():
        raise ValueError(f"missing immutable bundle record: {source.name}")
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    compiler_version = (bundle.get("versions") or {}).get("compiler_version")
    expected_package = package_identity(slug, version, compiler_version)
    if bundle.get("package") != expected_package:
        raise ValueError(f"bundle package identity disagrees for {source.name}")
    expected_name = expected_package["filename"]
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
            replacements = {}
            if withheld_paths:
                public_brand = dict(brand)
                public_brand["custom_assets"] = [item for item in brand["custom_assets"] if item["id"] in eligible]
                if not public_brand["custom_assets"]:
                    del public_brand["custom_assets"]
                replacements["brand.json"] = (json.dumps(public_brand, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
                consumer = json.loads((source / "enforcement" / "consumer-contract.json").read_text(encoding="utf-8"))
                provenance = [item for item in consumer.get("provenance", []) if item.get("path") == "brand.json"]
                if len(provenance) != 1:
                    raise ValueError("consumer provenance must bind brand.json exactly once")
                provenance[0]["bytes"] = len(replacements["brand.json"])
                provenance[0]["sha256"] = hashlib.sha256(replacements["brand.json"]).hexdigest()
                replacements["enforcement/consumer-contract.json"] = (json.dumps(consumer, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
                manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
                manifest["files"] = [item for item in manifest["files"] if item["path"] not in withheld_paths]
                for name, data in replacements.items():
                    records = [item for item in manifest["files"] if item["path"] == name]
                    if len(records) != 1:
                        raise ValueError("manifest must bind %s exactly once" % name)
                    records[0]["bytes"] = len(data)
                    records[0]["sha256"] = hashlib.sha256(data).hexdigest()
                replacements["manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
            add_tree(archive, source, omit=withheld_paths | set(replacements))
            for name, data in sorted(replacements.items()):
                add_bytes(archive, name, data)
            existing = set(archive.namelist())
            for name in LICENSES:
                if name not in existing:
                    add_bytes(archive, name, (root / name).read_bytes())
        verify_brand_archive(
            staged,
            slug,
            version,
            expected_filename=expected_name,
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
    revision = source_revision(SKILL)
    resolved_output = OUTPUT.resolve()
    if resolved_output.parent != ROOT.resolve():
        raise ValueError("refusing to clean release output outside repository root")
    if resolved_output.exists():
        shutil.rmtree(resolved_output)
    resolved_output.mkdir()

    skill_bundle = OUTPUT / f"shruggie-brandbuilder-{version}.skill"
    with zipfile.ZipFile(skill_bundle, "w") as archive:
        add_tree(archive, SKILL, omit={"SOURCE_REVISION"})
        add_bytes(archive, "SOURCE_REVISION", (revision + "\n").encode("utf-8"))

    portable = OUTPUT / f"shruggie-brandbuilder-{version}-portable.zip"
    with zipfile.ZipFile(portable, "w") as archive:
        add_tree(archive, SKILL, omit={"SKILL.md", "SOURCE_REVISION"})
        add_bytes(archive, "SOURCE_REVISION", (revision + "\n").encode("utf-8"))
        add_bytes(
            archive,
            "README.md",
            ("# shruggie-brandbuilder portable bundle\n\n"
             "Start with `AGENTS.md`. The skill instructions are adapted there for repository vendoring.\n").encode(),
        )

    for slug in PRODUCTION:
        source = ROOT / "dist" / slug
        brand = json.loads((source / "brand.json").read_text(encoding="utf-8"))
        archive_path = OUTPUT / package_identity(slug, brand["version"], version)["filename"]
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
