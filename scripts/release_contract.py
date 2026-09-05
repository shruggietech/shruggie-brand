#!/usr/bin/env python3
"""Generate release notes and certify release metadata and archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath
from typing import Dict, Iterable, Mapping, Optional


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ("shruggietech", "fragcap", "go-schedule", "glitchpad", "covarity")
LICENSES = ("LICENSE", "NOTICE", "LICENSE-BRAND.md")
REQUIRED_HISTORY = {
    "1.1.0": ("glyph construction", "portability tiers", "chart", "generators", "Apache-2.0"),
    "1.1.1": ("WCAG", "AA floor"),
    "1.1.2": ("geometry_provenance", "ShruggieTech", "Python 3.8", "Windows", "stale"),
    "1.2.0": ("third-party", "application-icon", "Fumadocs", "route descriptor"),
}
MIGRATION = (
    "Existing kits need migration: **yes**. Rebuild existing kits with v1.2.0 to receive "
    "ownership-safe third-party inputs, authoritative supplied-mark and fixed-font handling, "
    "native application-icon suites, and the current canon. Rebuild the site from those "
    "verified kits to publish the current portfolio, documentation, and discovery output."
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def changelog_section(text: str, version: str, bracketed: bool) -> Dict[str, str]:
    label = r"\[" + re.escape(version) + r"\]" if bracketed else re.escape(version)
    pattern = re.compile(
        r"^## " + label + r" - (?P<date>\d{4}-\d{2}-\d{2})\s*$\n"
        r"(?P<body>.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise ValueError("expected one %s changelog section for %s, found %d"
                         % ("root" if bracketed else "skill", version, len(matches)))
    return {"date": matches[0].group("date"), "body": matches[0].group("body").strip()}


def skill_metadata(path: Path) -> Dict[str, str]:
    text = read_text(path)
    frontmatter = re.match(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", text, re.DOTALL)
    if not frontmatter:
        raise ValueError("skill/SKILL.md lacks YAML frontmatter")
    metadata = re.search(
        r"^metadata:\s*$\n(?P<body>(?:^[ \t]+.*(?:\n|\Z))+)",
        frontmatter.group("body"),
        re.MULTILINE,
    )
    if not metadata:
        raise ValueError("skill/SKILL.md lacks metadata")
    values = {}
    for key in ("version", "canon"):
        match = re.search(r"^\s+" + key + r":\s*([^\s#]+)\s*$",
                          metadata.group("body"), re.MULTILINE)
        if not match:
            raise ValueError("skill/SKILL.md metadata lacks %s" % key)
        values[key] = match.group(1).strip('"\'')
    return values


def require_history(root_changelog: str, skill_changelog: str, release_version: str) -> None:
    for version, phrases in REQUIRED_HISTORY.items():
        root_section = changelog_section(root_changelog, version, bracketed=True)
        skill_section = changelog_section(skill_changelog, version, bracketed=False)
        combined = root_section["body"] + "\n" + skill_section["body"]
        missing = [phrase for phrase in phrases if phrase.lower() not in combined.lower()]
        if missing:
            raise ValueError("version %s history lacks: %s" % (version, ", ".join(missing)))
    root_release = changelog_section(root_changelog, release_version, bracketed=True)
    skill_release = changelog_section(skill_changelog, release_version, bracketed=False)
    if root_release["date"] != skill_release["date"]:
        raise ValueError("root and skill %s release dates disagree" % release_version)


def load_metadata(root: Path, version: str) -> Dict[str, object]:
    root = root.resolve()
    skill = skill_metadata(root / "skill" / "SKILL.md")
    canon = json.loads(read_text(root / "skill" / "references" / "01-canon.json"))
    site = json.loads(read_text(root / "site" / "package.json"))
    root_changelog = read_text(root / "CHANGELOG.md")
    skill_changelog = read_text(root / "skill" / "CHANGELOG.md")
    require_history(root_changelog, skill_changelog, version)
    release = changelog_section(root_changelog, version, bracketed=True)

    if skill["version"] != version:
        raise ValueError("skill version %s does not match release %s" % (skill["version"], version))
    if skill["canon"] != version or canon.get("version") != version:
        raise ValueError("canon version does not match release %s" % version)
    if site.get("version") != version:
        raise ValueError("site package version %s does not match release %s"
                         % (site.get("version"), version))

    brands = {}
    for slug in PRODUCTION:
        brand = json.loads(read_text(root / "brands" / slug / "brand.json"))
        if brand.get("slug") != slug:
            raise ValueError("brands/%s/brand.json declares slug %r" % (slug, brand.get("slug")))
        brand_version = brand.get("version")
        if not isinstance(brand_version, str) or not brand_version:
            raise ValueError("brands/%s/brand.json lacks a version" % slug)
        if brand.get("canon") != canon["version"]:
            raise ValueError("brands/%s/brand.json canon differs from authoritative canon %s"
                             % (slug, canon["version"]))
        brands[slug] = {"version": brand_version, "canon": brand.get("canon")}

    return {
        "root": root,
        "version": version,
        "skill_version": skill["version"],
        "canon_version": canon["version"],
        "site_version": site["version"],
        "release_date": release["date"],
        "release_changes": release["body"],
        "brands": brands,
    }


def current_version(root: Path) -> str:
    root = root.resolve()
    skill = skill_metadata(root / "skill" / "SKILL.md")
    canon = json.loads(read_text(root / "skill" / "references" / "01-canon.json"))
    version = skill["version"]
    if skill["canon"] != version or canon.get("version") != version:
        raise ValueError("skill and canon current versions disagree")
    load_metadata(root, version)
    return version


def render_notes(metadata: Mapping[str, object]) -> str:
    version = str(metadata["version"])
    return (
        "# shruggie-brandbuilder v%s\n\n"
        "Skill version: `%s`\n\n"
        "Canon version: `%s`\n\n"
        "%s\n\n"
        "## Release changes\n\n%s\n"
        % (version, metadata["skill_version"], metadata["canon_version"],
           MIGRATION, metadata["release_changes"])
    )


def expected_assets(metadata: Mapping[str, object]) -> Dict[str, Dict[str, str]]:
    version = str(metadata["version"])
    assets = {
        "shruggie-brandbuilder-%s.skill" % version: {"kind": "skill", "version": version},
        "shruggie-brandbuilder-%s-portable.zip" % version: {
            "kind": "portable", "version": version,
        },
    }
    brands = metadata.get("brands", {})
    for slug in PRODUCTION:
        if slug not in brands:
            continue
        brand_version = str(brands[slug]["version"])
        assets["%s-brand-%s.zip" % (slug, brand_version)] = {
            "kind": "brand", "slug": slug, "version": brand_version,
        }
    return assets


def archive_entries(path: Path) -> set:
    with zipfile.ZipFile(str(path)) as archive:
        names = archive.namelist()
    if len(names) != len(set(names)):
        raise ValueError("%s contains duplicate archive paths" % path.name)
    for name in names:
        pure = PurePosixPath(name)
        if (not pure.parts or name.startswith(("/", "\\")) or "\\" in name
                or ".." in pure.parts or ":" in pure.parts[0]):
            raise ValueError("%s contains unsafe archive path %s" % (path.name, name))
    return set(names)


def require_entries(path: Path, entries: Iterable[str], required: Iterable[str]) -> None:
    missing = sorted(set(required) - set(entries))
    if missing:
        raise ValueError("%s lacks %s" % (path.name, ", ".join(missing)))


def verify_canonical_files(archive: zipfile.ZipFile, path: Path, names: Iterable[str],
                           source_parent: Path) -> None:
    for name in names:
        if archive.read(name) != (source_parent / name).read_bytes():
            raise ValueError("%s contains noncanonical %s" % (path.name, name))


def verify_skill_archive(path: Path, portable: bool, root: Optional[Path] = None) -> None:
    entries = archive_entries(path)
    required = set(LICENSES) | {"AGENTS.md", "CHANGELOG.md"}
    required.add("README.md" if portable else "SKILL.md")
    require_entries(path, entries, required)
    if portable and "SKILL.md" in entries:
        raise ValueError("%s must omit SKILL.md" % path.name)
    if root is not None:
        with zipfile.ZipFile(str(path)) as archive:
            verify_canonical_files(archive, path, LICENSES, root / "skill")
            verify_canonical_files(archive, path, ("AGENTS.md", "CHANGELOG.md"),
                                   root / "skill")
            if portable:
                expected_readme = (
                    "# shruggie-brandbuilder portable bundle\n\n"
                    "Start with `AGENTS.md`. The skill instructions are adapted there for "
                    "repository vendoring.\n"
                ).encode("utf-8")
                if archive.read("README.md") != expected_readme:
                    raise ValueError("%s contains unexpected portable README.md" % path.name)
            elif archive.read("SKILL.md") != (root / "skill" / "SKILL.md").read_bytes():
                raise ValueError("%s contains noncanonical SKILL.md" % path.name)


def _read_json(archive: zipfile.ZipFile, name: str, archive_name: str) -> Mapping[str, object]:
    try:
        return json.loads(archive.read(name).decode("utf-8"))
    except (KeyError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("%s has invalid %s: %s" % (archive_name, name, error))


def verify_brand_archive(path: Path, slug: str, version: str,
                         expected_canon: Optional[str] = None,
                         root: Optional[Path] = None) -> None:
    entries = archive_entries(path)
    required = set(LICENSES) | {"brand.json", "manifest.json", "VERIFY.md", "brand-guide.pdf"}
    require_entries(path, entries, required)
    with zipfile.ZipFile(str(path)) as archive:
        if root is not None:
            verify_canonical_files(archive, path, LICENSES, root)
        brand = _read_json(archive, "brand.json", path.name)
        manifest = _read_json(archive, "manifest.json", path.name)
        if brand.get("slug") != slug or brand.get("version") != version:
            raise ValueError("%s filename and brand.json metadata disagree" % path.name)
        if expected_canon is not None and brand.get("canon") != expected_canon:
            raise ValueError("%s canon differs from authoritative canon %s"
                             % (path.name, expected_canon))
        if manifest.get("name") != "%s-brand-kit" % slug:
            raise ValueError("%s manifest name disagrees" % path.name)
        if manifest.get("version") != version:
            raise ValueError("%s manifest version disagrees" % path.name)
        if manifest.get("canon") != brand.get("canon"):
            raise ValueError("%s manifest canon disagrees" % path.name)
        if not archive.read("brand-guide.pdf").startswith(b"%PDF-"):
            raise ValueError("%s brand-guide.pdf lacks a PDF signature" % path.name)

        recorded = set()
        for item in manifest.get("files", []):
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                raise ValueError("%s has a malformed manifest file entry" % path.name)
            name = item["path"]
            if name in recorded:
                raise ValueError("%s manifest repeats %s" % (path.name, name))
            recorded.add(name)
            try:
                value = archive.read(name)
            except KeyError:
                raise ValueError("%s manifest path is missing: %s" % (path.name, name))
            if len(value) != item.get("bytes"):
                raise ValueError("%s byte count mismatch: %s" % (path.name, name))
            if hashlib.sha256(value).hexdigest() != item.get("sha256"):
                raise ValueError("%s checksum mismatch: %s" % (path.name, name))

        exempt = set(LICENSES) | {"manifest.json"}
        unrecorded = sorted(
            name for name in entries
            if name not in recorded and name not in exempt and not name.endswith("/")
        )
        if unrecorded:
            raise ValueError("%s contains unrecorded files: %s"
                             % (path.name, ", ".join(unrecorded[:8])))


def verify_release_directory(release_dir: Path, metadata: Mapping[str, object],
                             notes: Optional[Path] = None) -> None:
    release_dir = release_dir.resolve()
    expected = expected_assets(metadata)
    allowed = set(expected)
    if notes is not None and notes.resolve().parent == release_dir:
        allowed.add(notes.name)
    actual = {path.name for path in release_dir.iterdir() if path.is_file()}
    missing = sorted(set(expected) - actual)
    unexpected = sorted(actual - allowed)
    problems = []
    if missing:
        problems.append("missing release assets: %s" % ", ".join(missing))
    if unexpected:
        problems.append("unexpected release assets: %s" % ", ".join(unexpected))
    if problems:
        raise ValueError("; ".join(problems))

    for filename, contract in expected.items():
        path = release_dir / filename
        kind = contract["kind"]
        root = metadata.get("root")
        if kind == "skill":
            verify_skill_archive(path, portable=False, root=root)
        elif kind == "portable":
            verify_skill_archive(path, portable=True, root=root)
        else:
            verify_brand_archive(
                path,
                contract["slug"],
                contract["version"],
                expected_canon=str(metadata["canon_version"]),
                root=root,
            )

    if notes is not None:
        actual_notes = "\n".join(read_text(notes).splitlines()).rstrip() + "\n"
        expected_notes = render_notes(metadata)
        if actual_notes != expected_notes:
            raise ValueError("release notes do not match generated v%s notes" % metadata["version"])


def write_notes(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("current", help="print the validated current release version")
    notes_parser = subparsers.add_parser("notes", help="generate validated release notes")
    notes_parser.add_argument("--version", required=True)
    notes_parser.add_argument("--output", type=Path, required=True)
    verify_parser = subparsers.add_parser("verify", help="verify release notes and archives")
    verify_parser.add_argument("--version", required=True)
    verify_parser.add_argument("--release-dir", type=Path, required=True)
    verify_parser.add_argument("--notes", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "current":
        print(current_version(ROOT))
        return 0

    metadata = load_metadata(ROOT, args.version)
    if args.command == "notes":
        write_notes(args.output, render_notes(metadata))
        print("wrote validated v%s notes to %s" % (args.version, args.output))
    else:
        verify_release_directory(args.release_dir, metadata, args.notes)
        print("verified %d v%s release assets and generated notes"
              % (len(expected_assets(metadata)), args.version))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
