#!/usr/bin/env python3
"""Fail closed on unsafe or incomplete publication artifact trees."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, Iterable, Optional, Set, Tuple


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skill" / "templates"))
from interface_contract import RELEASE_AUTHORIZED_BRANDS
from package_release import write_brand_archive
PRODUCTION = (
    "covarity",
    "cueson",
    "eso-weave",
    "fragcap",
    "glitchpad",
    "go-schedule",
    "i-heart-pr-tours",
    "local-companion",
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


def _json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as error:
        raise ValueError("unreadable required JSON %s: %s" % (path, error)) from error


def _safe_file(base: Path, relative: str) -> Path:
    if (not isinstance(relative, str) or not relative or "\\" in relative
            or relative.startswith("/") or ":" in relative.split("/")[0]
            or any(part in ("", ".", "..") for part in relative.split("/"))):
        raise ValueError("unsafe artifact reference: %r" % relative)
    path = base / relative
    if any(part.is_symlink() for part in (path, *path.parents) if part != base and base in part.parents):
        raise ValueError("symbolic link in artifact reference: %s" % relative)
    try:
        path.resolve(strict=True).relative_to(base.resolve())
    except (OSError, ValueError) as error:
        raise ValueError("missing or escaped artifact reference: %s" % relative) from error
    if not path.is_file():
        raise ValueError("artifact reference is not a file: %s" % relative)
    return path


def _fingerprint(path: Path) -> Tuple[int, str]:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return path.stat().st_size, digest.hexdigest()


def _tree_fingerprints(path: Path) -> Dict[str, Tuple[int, str]]:
    if not path.is_dir() or path.is_symlink():
        raise ValueError("required artifact directory is missing or linked: %s" % path)
    result = {}
    for item in path.rglob("*"):
        if item.is_symlink():
            raise ValueError("symbolic link in artifact tree: %s" % item)
        if item.is_file():
            if item.stat().st_nlink > 1:
                raise ValueError("hard link in artifact tree: %s" % item)
            result[item.relative_to(path).as_posix()] = _fingerprint(item)
    return result


def _same_tree(source: Path, published: Path, label: str) -> int:
    original = _tree_fingerprints(source)
    copied = _tree_fingerprints(published)
    if not original or original != copied:
        missing = sorted(set(original) - set(copied))
        extra = sorted(set(copied) - set(original))
        changed = sorted(name for name in original.keys() & copied.keys() if original[name] != copied[name])
        raise ValueError("%s inventory or bytes differ: missing=%s extra=%s changed=%s" %
                         (label, missing[:5], extra[:5], changed[:5]))
    return len(original)


def _download_sources(source: Path, brand: dict) -> Dict[str, Path]:
    slug = brand["slug"]
    expected = {
        "%s-brand-guide.pdf" % slug: _safe_file(source, "brand-guide.pdf"),
        "%s-portable-guidelines.html" % slug: _safe_file(source, "guidelines/index.html"),
        "wordpress/%s-stbb-theme.zip" % slug: _safe_file(source, "wordpress/%s-stbb-theme.zip" % slug),
    }
    for family in ("logos", "favicons", "icons", "specimens"):
        tree = source / family
        for relative in _tree_fingerprints(tree):
            expected[family + "/" + relative] = tree / relative
    handoff = source / "consumer-handoff.json"
    if handoff.is_file():
        expected[handoff.name] = handoff
    for item in brand.get("custom_assets", []):
        approval = item.get("approval") or {}
        if approval.get("status") == "approved" and approval.get("publication_eligible") is True:
            relative = (item.get("source") or {}).get("path")
            if relative in expected:
                raise ValueError("custom asset collides with a generated download: %s" % relative)
            expected[relative] = _safe_file(source, relative)
    return expected


def audit_semantics(root: Path, kits: Path, site: Path, release: Optional[Path] = None,
                    candidate: Optional[Path] = None,
                    production: Iterable[str] = PRODUCTION,
                    release_authorized: Iterable[str] = RELEASE_AUTHORIZED_BRANDS,
                    expected_revision: Optional[str] = None) -> Dict[str, int]:
    """Bind public indexes, copied files, and staged archives to one kit candidate."""
    root = root.resolve()
    kits = _contained_directory(root, kits, "kits")
    site = _contained_directory(root, site, "site")
    slugs = tuple(production)
    release_slugs = set(release_authorized)
    if expected_revision is not None and not re.fullmatch(r"[0-9a-f]{40}", expected_revision):
        raise ValueError("expected source revision must be a full lowercase commit SHA")
    if (not slugs or len(slugs) != len(set(slugs))
            or any(not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug)
                   for slug in slugs)
            or not release_slugs.issubset(set(slugs))):
        raise ValueError("invalid production or release-authorized brand inventory")
    generated = root / "site" / "generated"
    brands = _json(generated / "brands.json")
    guidelines = _json(generated / "guidelines.json")
    conformance = _json(generated / "conformance.json")
    publication = _json(generated / "publication.json")
    if any(not isinstance(value, list) or len(value) != len(slugs)
           for value in (brands, guidelines, conformance)):
        raise ValueError("generated site brand, guideline, or conformance inventory is empty or incomplete")
    if any({item.get("slug") for item in value} != set(slugs)
           for value in (brands, conformance)):
        raise ValueError("generated site brand or conformance identity inventory differs")
    if {item.get("brand", {}).get("slug") for item in guidelines} != set(slugs):
        raise ValueError("generated guideline identity inventory differs")
    packages = []
    file_count = 0
    for slug in slugs:
        source = kits / slug
        target = site / slug
        brand = _json(_safe_file(source, "brand.json"))
        bundle = _json(_safe_file(source, "enforcement/bundle.json"))
        consumer = _json(_safe_file(source, "enforcement/consumer-contract.json"))
        facts = _json(_safe_file(source, "enforcement/documentation-facts.json"))
        portal = _json(_safe_file(source, "guidelines/portal.json"))
        manifest = _json(_safe_file(source, "manifest.json"))
        if brand.get("slug") != slug or not manifest.get("files"):
            raise ValueError("%s kit identity or required manifest inventory is incomplete" % slug)
        if (manifest.get("version") != brand.get("version") or manifest.get("canon") != brand.get("canon")
                or bundle.get("versions") != consumer.get("versions")
                or bundle.get("package") != consumer.get("bundle", {}).get("package")):
            raise ValueError("%s kit version or package identity differs" % slug)
        if (facts.get("bundle") != bundle or facts.get("versions") != consumer.get("versions")
                or facts.get("brand") != consumer.get("brand") or portal.get("implementation") != facts):
            raise ValueError("%s documentation facts differ from kit authority" % slug)
        if _fingerprint(_safe_file(target, "facts/documentation.json")) != _fingerprint(
                _safe_file(source, "enforcement/documentation-facts.json")):
            raise ValueError("%s public documentation facts differ from verified kit" % slug)
        indexed_brand = next(item for item in brands if item["slug"] == slug)
        indexed_portal = next(item for item in guidelines if item["brand"]["slug"] == slug)
        indexed_conformance = next(item for item in conformance if item["slug"] == slug)
        conformance_manifest = _json(_safe_file(source, "conformance/manifest.json"))
        if expected_revision is not None and conformance_manifest.get("source_revision") != expected_revision:
            raise ValueError("%s source revision differs from candidate" % slug)
        if (indexed_brand.get("version") != brand.get("version")
                or indexed_brand.get("packageId") != bundle["package"]["id"]
                or indexed_brand.get("kitArchiveFilename") != bundle["package"]["filename"]
                or indexed_brand.get("brandbuilderVersion") != bundle["versions"]["compiler_version"]
                or indexed_portal.get("implementation") != facts
                or indexed_portal.get("topics") != portal.get("topics")
                or indexed_conformance.get("brandVersion") != brand.get("version")
                or indexed_conformance.get("versions") != conformance_manifest.get("versions")
                or indexed_conformance.get("sourceRevision") != conformance_manifest.get("source_revision")):
            raise ValueError("%s generated site projection differs from verified kit" % slug)
        registry = source / "nextjs" / "registry"
        file_count += _same_tree(registry, target / "brand" / "r", "%s registry" % slug)
        catalog = _json(registry / "registry.json")
        names = [item.get("name") for item in catalog.get("items", [])]
        if (not names or any(not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name)
                             for name in names)
                or len(names) != len(set(names)) or "theme" not in names):
            raise ValueError("%s registry has an empty or duplicate required catalog" % slug)
        if set(_tree_fingerprints(registry)) != {"registry.json"} | {name + ".json" for name in names}:
            raise ValueError("%s registry catalog endpoints differ" % slug)
        downloads = target / "downloads" / "files"
        actual_downloads = _tree_fingerprints(downloads)
        expected_downloads = {name: _fingerprint(path) for name, path in _download_sources(source, brand).items()}
        if actual_downloads != expected_downloads:
            missing = sorted(set(expected_downloads) - set(actual_downloads))
            changed = sorted(name for name in actual_downloads.keys() & expected_downloads.keys()
                             if actual_downloads[name] != expected_downloads[name])
            extra = sorted(set(actual_downloads) - set(expected_downloads))
            raise ValueError("%s hosted download inventory or bytes differ: missing=%s changed=%s extra=%s" %
                             (slug, missing[:5], changed[:5], extra[:5]))
        file_count += len(actual_downloads)
        fixtures = site / "conformance-fixtures" / slug
        for name, relative in (("manifest.json", "conformance/manifest.json"),
                               ("specimen.html", "conformance/browser/specimen.html")):
            if _fingerprint(_safe_file(fixtures, name)) != _fingerprint(_safe_file(source, relative)):
                raise ValueError("%s hosted conformance fixture differs: %s" % (slug, name))
        package = bundle["package"]
        archive = _safe_file(target / "downloads", package["filename"])
        if indexed_brand.get("kitArchive") != "/%s/downloads/%s" % (slug, package["filename"]):
            raise ValueError("%s advertised archive URL differs" % slug)
        if release is not None and slug in release_slugs:
            if _fingerprint(archive) != _fingerprint(_safe_file(release, package["filename"])):
                raise ValueError("%s hosted archive differs from release candidate" % slug)
        elif slug not in release_slugs:
            # Independently owned brands are hosted, but absent from formal release assets.
            # Regenerate their deterministic archive to bind the advertised download to this kit.
            with tempfile.TemporaryDirectory(prefix="brand-archive-audit-") as temporary:
                expected_archive = Path(temporary) / package["filename"]
                write_brand_archive(source, expected_archive, root=root)
                if _fingerprint(archive) != _fingerprint(expected_archive):
                    raise ValueError("%s hosted archive differs from certified kit" % slug)
        packages.append(package)
    released = [item for item in packages if item["brand_slug"] in release_slugs]
    if (release_slugs != {item["brand_slug"] for item in released}
            or publication.get("packages") != released
            or publication.get("version") != packages[0]["brandbuilder_version"]):
        raise ValueError("publication package inventory or version differs from kits")
    if expected_revision is not None:
        documentation = _json(generated / "documentation-publication.json")
        if (publication.get("sourceRevision") != expected_revision
                or documentation.get("sourceRevision") != expected_revision):
            raise ValueError("publication source revision differs from candidate")
    if _fingerprint(_safe_file(site, "docs/publication.json")) != _fingerprint(_safe_file(generated, "documentation-publication.json")):
        raise ValueError("exported documentation publication record differs")
    if candidate is not None:
        if release is None:
            raise ValueError("staged candidate requires a release directory")
        staged = candidate.resolve(strict=True)
        if candidate.is_symlink() or not staged.is_dir():
            raise ValueError("staged candidate is missing or linked: %s" % candidate)
        if expected_revision is not None and _safe_file(staged, "SOURCE_COMMIT").read_text(encoding="utf-8").strip() != expected_revision:
            raise ValueError("staged source revision differs from candidate")
        _same_tree(release, staged / "files", "staged release files")
        for name, source_path in (
            ("PUBLICATION.json", generated / "publication.json"),
            ("DOCUMENTATION.json", generated / "documentation-publication.json"),
            ("SITE-DOCUMENTATION.json", site / "docs" / "publication.json"),
        ):
            if _fingerprint(_safe_file(staged, name)) != _fingerprint(source_path):
                raise ValueError("staged candidate record differs: %s" % name)
        _same_tree(generated / "docs", staged / "docs", "staged documentation")
        checksums = (staged / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        expected = {name: digest for name, (_, digest) in _tree_fingerprints(staged / "files").items()
                    if name.endswith((".skill", ".zip"))}
        observed = {}
        for line in checksums:
            match = re.fullmatch(r"([0-9a-f]{64})  (\S+)", line)
            if not match or not match.group(2).startswith("./") or match.group(2)[2:] in observed:
                raise ValueError("staged SHA256SUMS is malformed or duplicate")
            observed[match.group(2)[2:]] = match.group(1)
        if not expected or observed != expected:
            raise ValueError("staged SHA256SUMS inventory or digest differs")
    return {"brands": len(slugs), "public_files": file_count, "packages": len(packages)}


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kits", type=Path, required=True)
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--semantic", action="store_true")
    parser.add_argument("--release", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--revision")
    args = parser.parse_args(argv)
    result = audit(ROOT, args.kits, args.site)
    if args.semantic:
        if args.candidate is not None and args.revision is None:
            parser.error("--candidate requires --revision")
        result.update(audit_semantics(ROOT, args.kits, args.site, args.release, args.candidate,
                                      expected_revision=args.revision))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
