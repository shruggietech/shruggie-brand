#!/usr/bin/env python3
"""Generate release notes and certify release metadata and archives."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Dict, Iterable, Mapping, Optional


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skill" / "templates"))

from schema_validation import SchemaValidationError, validate_json_schema
from interface_contract import (RELEASE_AUTHORIZED_BRANDS, SOURCE_REVISION, load_release_impact, package_identity,
                                validate_version_combination, validate_version_policy)
PRODUCTION = RELEASE_AUTHORIZED_BRANDS
LICENSES = ("LICENSE", "NOTICE", "LICENSE-BRAND.md")
REQUIRED_HISTORY = {
    "1.1.0": ("glyph construction", "portability tiers", "chart", "generators", "Apache-2.0"),
    "1.1.1": ("WCAG", "AA floor"),
    "1.1.2": ("geometry_provenance", "ShruggieTech", "Python 3.8", "Windows", "stale"),
    "1.2.0": ("third-party", "application-icon", "Fumadocs", "route descriptor"),
    "1.2.1": ("black-background", "Brotli"),
    "2.0.0": ("AppFrame", "environment", "immutable kit package", "release-backed", "Web/React adapter"),
    "2.0.1": ("egui", "fine-pointer", "44-point", "iframe"),
    "2.0.2": ("documentation", "preview", "pagination"),
    "2.0.3": ("native", "maskable", "Windows", "egui"),
    "2.1.0": ("light-first", "custom assets", "shadcn registry", "Brand Canon"),
}
MIGRATIONS = {
    "1.2.0": (
        "Existing kits need migration: **yes**. Rebuild existing kits with v1.2.0 to receive "
        "ownership-safe third-party inputs, authoritative supplied-mark and fixed-font handling, "
        "native application-icon suites, and the current canon. Rebuild the site from those "
        "verified kits to publish the current portfolio, documentation, and discovery output."
    ),
    "1.2.1": (
        "Existing kits need migration: **conditional**. Rebuild the ShruggieTech kit and brand "
        "site with v1.2.1 to receive the approved black-background browser icon suite and current "
        "presentation. Other production kits do not require an asset migration unless consumers "
        "need their embedded canon metadata to match v1.2.1."
    ),
    "2.0.0": (
        "Existing kits need migration: **yes for immutable package and recovery metadata**. Rebuild "
        "and repin kits with v2.0.0 to receive canonical brand-plus-BrandBuilder package identities, "
        "exact release-backed publication facts, and generated migration guidance. Web/React and "
        "egui capabilities remain optional when those surfaces do not apply. Approved identity is unchanged."
    ),
    "2.0.1": (
        "Existing kits need migration: **yes for native egui consumers**. Regenerate and repin kits with "
        "v2.0.1 to receive the immutable bb2.0.1 package identity and egui adapter 1.0.1. Fine-pointer "
        "controls use corrected compact density while touch, coarse, mixed, and unknown input profiles "
        "retain 44-point targets. Approved identity is unchanged."
    ),
    "2.0.2": (
        "Existing kits need migration: **yes to adopt corrected public guidance and previews**. Regenerate "
        "and repin kits with v2.0.2 to receive the immutable bb2.0.2 package identity, current "
        "instructions, and readable integration previews. Native egui adapter 1.0.1 and approved "
        "identity remain unchanged."
    ),
    "2.0.3": (
        "Existing kits need migration: **yes for affected native icon and egui consumers**. Regenerate "
        "and repin kits with v2.0.3 to receive distinct maskable web and Android icon roles, "
        "unplated ESO Weave Windows taskbar frames, and egui adapter 1.0.2 status contrast. "
        "Approved logo geometry remains unchanged; downstream applications still own their local call sites."
    ),
    "2.1.0": (
        "Existing kits need migration: **yes to adopt the new capabilities and corrected registry**. "
        "Regenerate and repin kits with v2.1.0 for the light-guide presentation, governed optional "
        "custom assets, and valid shadcn catalog and direct item delivery. Copy bundled local fonts "
        "through the documented manual setup; they are not an installable registry font item. "
        "Approved logo geometry and existing adapter APIs are unchanged."
    ),
}


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
    for key in ("version", "canon", "interface-canon", "component-recipes", "web-react-adapter", "egui-adapter"):
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
    interface = json.loads(read_text(root / "skill" / "references" / "interface-canon.json"))
    recipes = json.loads(read_text(root / "skill" / "references" / "component-recipes.json"))
    policy = validate_version_policy(json.loads(read_text(root / "skill" / "references" / "version-policy.json")))
    impact = load_release_impact(root / "skill" / "references" / "release-impact.json",
                                 root / "skill" / "references" / "release-impact.schema.json")
    site = json.loads(read_text(root / "site" / "package.json"))
    root_changelog = read_text(root / "CHANGELOG.md")
    skill_changelog = read_text(root / "skill" / "CHANGELOG.md")
    require_history(root_changelog, skill_changelog, version)
    release = changelog_section(root_changelog, version, bracketed=True)

    if skill["version"] != version:
        raise ValueError("skill version %s does not match release %s" % (skill["version"], version))
    if skill["canon"] != canon.get("version"):
        raise ValueError("skill canon %s does not match authoritative canon %s"
                         % (skill["canon"], canon.get("version")))
    if site.get("version") != version:
        raise ValueError("site package version %s does not match release %s"
                         % (site.get("version"), version))
    if impact.get("brandbuilder_version") != version:
        raise ValueError("release impact version %s does not match release %s"
                         % (impact.get("brandbuilder_version"), version))
    expected_metadata = {
        "interface-canon": interface["version"],
        "component-recipes": recipes["version"],
    }
    for key, expected in expected_metadata.items():
        if skill[key] != expected:
            raise ValueError("skill %s %s does not match authoritative %s" % (key, skill[key], expected))
    validate_version_combination({
        "brand_canon": canon["version"], "interface_canon": interface["version"],
        "component_recipes": recipes["version"], "web_react_adapter": skill["web-react-adapter"],
        "egui_adapter": skill["egui-adapter"], "compiler": skill["version"], "brand": "1.0.0",
    }, policy)

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
        "interface_canon_version": interface["version"],
        "component_recipe_version": recipes["version"],
        "web_react_adapter_version": skill["web-react-adapter"],
        "egui_adapter_version": skill["egui-adapter"],
        "version_policy_version": policy["version"],
        "release_impact": impact,
        "release_date": release["date"],
        "release_changes": release["body"],
        "brands": brands,
    }


def current_version(root: Path) -> str:
    root = root.resolve()
    skill = skill_metadata(root / "skill" / "SKILL.md")
    canon = json.loads(read_text(root / "skill" / "references" / "01-canon.json"))
    version = skill["version"]
    if skill["canon"] != canon.get("version"):
        raise ValueError("skill canon %s does not match authoritative canon %s"
                         % (skill["canon"], canon.get("version")))
    load_metadata(root, version)
    return version


def render_notes(metadata: Mapping[str, object]) -> str:
    version = str(metadata["version"])
    if version not in MIGRATIONS:
        raise ValueError("release %s lacks migration guidance" % version)
    return (
        "# shruggie-brandbuilder v%s\n\n"
        "Skill version: `%s`\n\n"
        "Canon version: `%s`\n\n"
        "Interface Canon version: `%s`\n\n"
        "Component recipe version: `%s`\n\n"
        "Web/React adapter version: `%s`\n\n"
        "egui adapter version: `%s`\n\n"
        "Version policy: `%s`\n\n"
        "%s\n\n%s\n\n"
        "## Release changes\n\n%s\n"
        % (version, metadata["skill_version"], metadata["canon_version"],
           metadata["interface_canon_version"], metadata["component_recipe_version"],
           metadata["web_react_adapter_version"], metadata["egui_adapter_version"], metadata["version_policy_version"],
           MIGRATIONS[version], render_release_impact(metadata["release_impact"]), metadata["release_changes"])
    )


def render_release_impact(impact: Mapping[str, object]) -> str:
    identity = ("No approved identity redesign is included."
                if not impact["identity_redesign"] else "This release includes an approved identity redesign.")
    rows = ["## Governed release impact", "", identity, "", "| Surface | Classification | Guidance |", "| --- | --- | --- |"]
    for name, item in impact["surfaces"].items():
        rows.append("| %s | %s | %s |" % (name.replace("_", " ").title(), item["classification"], item["summary"]))
    return "\n".join(rows)


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
        assets[package_identity(slug, brand_version, version)["filename"]] = {
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


def verify_skill_archive(path: Path, portable: bool, root: Optional[Path] = None,
                         expected_revision: Optional[str] = None) -> None:
    entries = archive_entries(path)
    required = set(LICENSES) | {"AGENTS.md", "CHANGELOG.md", "SOURCE_REVISION"}
    required.add("README.md" if portable else "SKILL.md")
    require_entries(path, entries, required)
    if portable and "SKILL.md" in entries:
        raise ValueError("%s must omit SKILL.md" % path.name)
    with zipfile.ZipFile(str(path)) as archive:
        revision = archive.read("SOURCE_REVISION").decode("utf-8").strip().lower()
        if SOURCE_REVISION.fullmatch(revision) is None:
            raise ValueError("%s contains an invalid SOURCE_REVISION" % path.name)
        if expected_revision is not None and revision != expected_revision:
            raise ValueError("%s source revision disagrees" % path.name)
        if root is not None:
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
                         expected_filename: Optional[str] = None,
                         expected_canon: Optional[str] = None,
                         expected_revision: Optional[str] = None,
                         expected_release_version: Optional[str] = None,
                         expected_release_impact: Optional[Mapping[str, object]] = None,
                         require_release: bool = False,
                         root: Optional[Path] = None) -> None:
    entries = archive_entries(path)
    required = set(LICENSES) | {
        "brand.json", "manifest.json", "VERIFY.md", "brand-guide.pdf",
        "enforcement/AGENTS.md", "enforcement/IMPLEMENTATION.md", "enforcement/MIGRATION.md",
        "enforcement/bundle.json", "enforcement/release-impact.json", "enforcement/release-impact.schema.json",
        "enforcement/consumer-contract.json", "enforcement/interface-canon.json",
        "enforcement/interface-canon.schema.json", "enforcement/component-recipes.json",
        "enforcement/component-recipes.schema.json", "enforcement/version-policy.json", "enforcement/consumer-contract.schema.json",
        "enforcement/documentation-contract.json", "enforcement/documentation-contract.schema.json", "enforcement/documentation-facts.json",
        "web/adapter.json", "web/support-matrix.json",
        "native/egui/Cargo.lock", "native/egui/adapter.json", "native/egui/support-matrix.json",
        "enforcement/capability-gap.example.json",
    }
    require_entries(path, entries, required)
    with zipfile.ZipFile(str(path)) as archive:
        if root is not None:
            verify_canonical_files(archive, path, LICENSES, root)
            for schema_name in ("interface-canon.schema.json", "component-recipes.schema.json", "consumer-contract.schema.json", "documentation-contract.schema.json", "release-impact.schema.json"):
                if archive.read("enforcement/" + schema_name) != (root / "skill" / "references" / schema_name).read_bytes():
                    raise ValueError("%s contains noncanonical enforcement/%s" % (path.name, schema_name))
            if archive.read("enforcement/version-policy.json") != (root / "skill" / "references" / "version-policy.json").read_bytes():
                raise ValueError("%s contains noncanonical enforcement/version-policy.json" % path.name)
            if archive.read("enforcement/documentation-contract.json") != (root / "skill" / "references" / "documentation-contract.json").read_bytes():
                raise ValueError("%s contains noncanonical enforcement/documentation-contract.json" % path.name)
        brand = _read_json(archive, "brand.json", path.name)
        for item in brand.get("custom_assets", []):
            approval = item.get("approval") or {}
            relative = (item.get("source") or {}).get("path")
            if not approval.get("publication_eligible"):
                raise ValueError("%s contains non-public custom asset declaration %s" % (path.name, item.get("id")))
            if approval.get("status") != "approved":
                raise ValueError("%s publishes unapproved custom asset %s" % (path.name, item.get("id")))
            if relative not in entries:
                raise ValueError("%s lacks public custom asset %s" % (path.name, item.get("id")))
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
        consumer = _read_json(archive, "enforcement/consumer-contract.json", path.name)
        consumer_schema = _read_json(archive, "enforcement/consumer-contract.schema.json", path.name)
        try:
            validate_json_schema(consumer, consumer_schema)
        except SchemaValidationError as error:
            raise ValueError("%s consumer contract schema violation: %s" % (path.name, error)) from error
        authority = consumer.get("authority") or {}
        capability_gap = consumer.get("capability_gap") or {}
        recovery = consumer.get("recovery") or {}
        declared_paths = {
            "brand source": authority.get("brand_source"),
            "bundle": authority.get("bundle"),
            "release impact": authority.get("release_impact"),
            "migration summary": authority.get("migration_summary"),
            "instructions": authority.get("instructions"),
            "Interface Canon": authority.get("interface_canon"),
            "component recipes": authority.get("component_recipes"),
            "version policy": authority.get("version_policy"),
            "Web adapter": authority.get("web_adapter"),
            "support matrix": authority.get("support_matrix"),
            "egui adapter": authority.get("egui_adapter"),
            "egui support matrix": authority.get("egui_support_matrix"),
            "capability-gap template": capability_gap.get("template_path"),
            "recovery distribution": recovery.get("path"),
        }
        for label, declared_path in declared_paths.items():
            if not isinstance(declared_path, str):
                raise ValueError("%s consumer %s path is missing" % (path.name, label))
            pure = PurePosixPath(declared_path)
            if (pure.is_absolute() or ".." in pure.parts or "\\" in declared_path
                    or not pure.parts or ":" in pure.parts[0]):
                raise ValueError("%s consumer %s path is unsafe" % (path.name, label))
            if declared_path not in entries:
                raise ValueError("%s consumer declared %s path is missing: %s"
                                 % (path.name, label, declared_path))
        declared_brand = _read_json(archive, authority["brand_source"], path.name)
        if declared_brand != brand:
            raise ValueError("%s consumer authority brand_source differs from brand.json" % path.name)
        delivered_release_impact = _read_json(archive, authority["release_impact"], path.name)
        canonical_release_impact = expected_release_impact
        if canonical_release_impact is None and root is not None:
            canonical_release_impact = json.loads(read_text(root / "skill" / "references" / "release-impact.json"))
        if canonical_release_impact is not None and delivered_release_impact != canonical_release_impact:
            raise ValueError("%s release impact differs from the canonical release record" % path.name)
        expected_brand = {
            "slug": brand.get("slug"),
            "title": brand.get("title"),
            "affiliation": brand.get("affiliation"),
            "brand_version": brand.get("version", "1.0.0"),
        }
        if consumer.get("brand") != expected_brand:
            raise ValueError("%s consumer brand metadata disagrees with brand.json" % path.name)
        versions = consumer.get("versions") or {}
        if versions.get("brand_version") != version:
            raise ValueError("%s consumer brand_version disagrees" % path.name)
        if versions.get("canon_version") != brand.get("canon"):
            raise ValueError("%s consumer canon_version disagrees" % path.name)
        if expected_canon is not None and versions.get("canon_version") != expected_canon:
            raise ValueError("%s consumer canon differs from authoritative canon %s"
                             % (path.name, expected_canon))
        expected_package = package_identity(slug, version, versions.get("compiler_version"))
        bundle = _read_json(archive, authority["bundle"], path.name)
        if consumer.get("bundle") != bundle:
            raise ValueError("%s consumer and bundle records disagree" % path.name)
        if bundle.get("package") != expected_package:
            raise ValueError("%s bundle package identity disagrees" % path.name)
        if (expected_filename or path.name) != expected_package["filename"]:
            raise ValueError("%s canonical archive filename must be %s" % (path.name, expected_package["filename"]))
        if bundle.get("versions") != versions:
            raise ValueError("%s bundle versions disagree" % path.name)
        publication = bundle.get("publication") or {}
        checksum_authority = bundle.get("checksum_authority") or {}
        compiler_version = versions.get("compiler_version")
        if publication.get("version") != compiler_version:
            raise ValueError("%s bundle publication version disagrees" % path.name)
        if publication.get("tag") != "v%s" % compiler_version:
            raise ValueError("%s bundle publication tag disagrees" % path.name)
        expected_release_checksums = "SHA256SUMS" if publication.get("status") == "release" else None
        if checksum_authority.get("release_checksums") != expected_release_checksums:
            raise ValueError("%s bundle release checksum authority disagrees with publication status" % path.name)
        if require_release and expected_revision is None:
            raise ValueError("%s expected source revision is required" % path.name)
        if expected_revision is not None and bundle.get("source_revision") != expected_revision:
            raise ValueError("%s bundle source revision disagrees" % path.name)
        if require_release:
            if publication.get("status") != "release":
                raise ValueError("%s bundle is not an exact release publication" % path.name)
            if expected_release_version is None:
                raise ValueError("%s expected release version is required" % path.name)
            if publication.get("version") != expected_release_version:
                raise ValueError("%s bundle release publication version disagrees" % path.name)
            if publication.get("tag") != "v%s" % expected_release_version:
                raise ValueError("%s bundle release publication tag disagrees" % path.name)
        interface_canon = _read_json(archive, authority["interface_canon"], path.name)
        if versions.get("interface_canon_version") != interface_canon.get("version"):
            raise ValueError("%s consumer interface_canon_version disagrees" % path.name)
        component_recipes = _read_json(archive, authority["component_recipes"], path.name)
        if versions.get("component_recipe_version") != component_recipes.get("version"):
            raise ValueError("%s consumer component_recipe_version disagrees" % path.name)
        web_adapter = _read_json(archive, authority["web_adapter"], path.name)
        if versions.get("web_react_adapter_version") != web_adapter.get("adapter_version"):
            raise ValueError("%s consumer web_react_adapter_version disagrees" % path.name)
        support_matrix = _read_json(archive, authority["support_matrix"], path.name)
        if support_matrix.get("adapter_version") != web_adapter.get("adapter_version"):
            raise ValueError("%s support matrix adapter version disagrees" % path.name)
        version_policy = validate_version_policy(_read_json(archive, authority["version_policy"], path.name))
        egui_adapter = _read_json(archive, authority["egui_adapter"], path.name)
        if versions.get("egui_adapter_version") != egui_adapter.get("adapter_version"):
            raise ValueError("%s consumer egui_adapter_version disagrees" % path.name)
        if egui_adapter.get("component_recipe_version") != component_recipes.get("version"):
            raise ValueError("%s egui adapter component recipe version disagrees" % path.name)
        egui_support = _read_json(archive, authority["egui_support_matrix"], path.name)
        if egui_support.get("adapter_version") != egui_adapter.get("adapter_version"):
            raise ValueError("%s egui support matrix adapter version disagrees" % path.name)
        domain_versions = {
            "brand_canon": versions.get("canon_version"), "interface_canon": versions.get("interface_canon_version"),
            "component_recipes": versions.get("component_recipe_version"), "web_react_adapter": versions.get("web_react_adapter_version"),
            "egui_adapter": versions.get("egui_adapter_version"), "compiler": versions.get("compiler_version"),
            "brand": versions.get("brand_version"),
        }
        if consumer.get("compatibility") != validate_version_combination(domain_versions, version_policy):
            raise ValueError("%s consumer compatibility record disagrees" % path.name)
        recovery_path = recovery.get("path")
        try:
            recovery_bytes = archive.read(recovery_path)
        except KeyError as error:
            raise ValueError("%s consumer recovery distribution is missing" % path.name) from error
        if hashlib.sha256(recovery_bytes).hexdigest() != recovery.get("sha256"):
            raise ValueError("%s consumer recovery checksum mismatch" % path.name)
        if PurePosixPath(recovery_path).name != recovery.get("distribution"):
            raise ValueError("%s consumer recovery filename disagrees" % path.name)
        recovery_target = recovery.get("extract_to")
        expected_entry_points = [
            "python3 %s/templates/verify.py ." % recovery_target,
            "python3 %s/templates/validate_glyph.py brand.json" % recovery_target,
        ]
        if recovery_target != "enforcement/brandbuilder" or (consumer.get("verification") or {}).get("entry_points") != expected_entry_points:
            raise ValueError("%s consumer verification entry points disagree with recovery location" % path.name)
        sources = recovery.get("sources") or []
        if not sources or sources[0].get("kind") != "delivered-bundle" or sources[0].get("network_required") is not False:
            raise ValueError("%s consumer recovery does not prefer delivered bytes" % path.name)
        if "latest" in json.dumps(recovery).lower():
            raise ValueError("%s consumer recovery recommends an unspecified latest version" % path.name)
        with zipfile.ZipFile(io.BytesIO(recovery_bytes)) as skill_archive:
            skill_names = skill_archive.namelist()
            require_entries(path, skill_names, {
                "SKILL.md", "AGENTS.md", "references/interface-canon.json",
                "references/component-recipes.json", "references/component-recipes.schema.json",
                "references/version-policy.json",
                "references/consumer-contract.schema.json", "references/documentation-contract.json",
                "references/documentation-contract.schema.json", "references/release-impact.json",
                "references/release-impact.schema.json", "SOURCE_REVISION", "templates/documentation_contract.py", "templates/verify.py",
                "templates/validate_glyph.py",
            })
            if len(skill_names) != len(set(skill_names)):
                raise ValueError("%s recovery distribution repeats paths" % path.name)
            recovery_revision = skill_archive.read("SOURCE_REVISION").decode("utf-8").strip().lower()
            if recovery_revision != bundle.get("source_revision"):
                raise ValueError("%s recovery source revision disagrees" % path.name)
            for name in skill_names:
                pure = PurePosixPath(name)
                if (pure.is_absolute() or ".." in pure.parts or "\\" in name
                        or not pure.parts or ":" in pure.parts[0]):
                    raise ValueError("%s recovery distribution contains unsafe path %s" % (path.name, name))
            skill_text = skill_archive.read("SKILL.md").decode("utf-8")
            for metadata_key, version_key in (("version", "compiler_version"),
                                              ("canon", "canon_version"),
                                              ("interface-canon", "interface_canon_version"),
                                              ("component-recipes", "component_recipe_version"),
                                              ("web-react-adapter", "web_react_adapter_version"),
                                              ("egui-adapter", "egui_adapter_version")):
                match = re.search(r"^\s+%s:\s*([^\s#]+)\s*$" % metadata_key,
                                  skill_text, re.MULTILINE)
                if match is None or match.group(1).strip("\"'") != versions.get(version_key):
                    raise ValueError("%s recovery %s disagrees" % (path.name, version_key))
            bundled_interface = json.loads(skill_archive.read("references/interface-canon.json").decode("utf-8"))
            if bundled_interface.get("version") != versions.get("interface_canon_version"):
                raise ValueError("%s recovery Interface Canon version disagrees" % path.name)
            bundled_recipes = json.loads(skill_archive.read("references/component-recipes.json").decode("utf-8"))
            if bundled_recipes.get("version") != versions.get("component_recipe_version"):
                raise ValueError("%s recovery component recipe version disagrees" % path.name)
            if skill_archive.read("references/consumer-contract.schema.json") != archive.read("enforcement/consumer-contract.schema.json"):
                raise ValueError("%s recovery consumer schema disagrees with delivered schema" % path.name)
            if skill_archive.read("references/documentation-contract.json") != archive.read("enforcement/documentation-contract.json"):
                raise ValueError("%s recovery documentation contract disagrees with delivered contract" % path.name)
            if skill_archive.read("references/documentation-contract.schema.json") != archive.read("enforcement/documentation-contract.schema.json"):
                raise ValueError("%s recovery documentation schema disagrees with delivered schema" % path.name)
            if skill_archive.read("references/release-impact.json") != archive.read("enforcement/release-impact.json"):
                raise ValueError("%s recovery release impact disagrees with delivered impact" % path.name)
            if skill_archive.read("references/release-impact.schema.json") != archive.read("enforcement/release-impact.schema.json"):
                raise ValueError("%s recovery release impact schema disagrees with delivered schema" % path.name)
        agents = archive.read("enforcement/AGENTS.md").decode("utf-8")
        begin = "<!-- BEGIN SHRUGGIE-BRANDBUILDER: CONSUMER CONTRACT -->"
        end = "<!-- END SHRUGGIE-BRANDBUILDER: CONSUMER CONTRACT -->"
        if agents.count(begin) != 1 or agents.count(end) != 1 or agents.index(begin) > agents.index(end):
            raise ValueError("%s governed consumer instruction markers are invalid" % path.name)
        gap = _read_json(archive, capability_gap["template_path"], path.name)
        if gap.get("submission_authorized") is not False:
            raise ValueError("%s capability gap grants submission authority" % path.name)
        consumer_recorded = set()
        for item in consumer.get("provenance", []):
            if not isinstance(item, dict) or set(item) != {"path", "bytes", "sha256"}:
                raise ValueError("%s has malformed consumer provenance" % path.name)
            name = item["path"]
            if name in consumer_recorded:
                raise ValueError("%s consumer provenance repeats %s" % (path.name, name))
            consumer_recorded.add(name)
            try:
                value = archive.read(name)
            except KeyError as error:
                raise ValueError("%s consumer provenance path is missing: %s" % (path.name, name)) from error
            if len(value) != item["bytes"] or hashlib.sha256(value).hexdigest() != item["sha256"]:
                raise ValueError("%s consumer provenance mismatch: %s" % (path.name, name))
        required_provenance = {
            "brand.json", "enforcement/AGENTS.md", "enforcement/IMPLEMENTATION.md", "enforcement/MIGRATION.md",
            "enforcement/bundle.json", "enforcement/release-impact.json", "enforcement/release-impact.schema.json",
            "enforcement/interface-canon.json", "enforcement/interface-canon.schema.json",
            "enforcement/component-recipes.json", "enforcement/component-recipes.schema.json",
            "enforcement/consumer-contract.schema.json", "enforcement/capability-gap.example.json",
            "enforcement/documentation-contract.json", "enforcement/documentation-contract.schema.json", "enforcement/documentation-facts.json",
        } | set(declared_paths.values())
        if not required_provenance.issubset(consumer_recorded):
            raise ValueError("%s consumer provenance omits required authority" % path.name)
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
            if not value:
                raise ValueError("%s manifest path is unexpectedly empty: %s" % (path.name, name))
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
                             notes: Optional[Path] = None,
                             expected_revision: Optional[str] = None,
                             require_release: bool = False) -> None:
    if require_release and expected_revision is None:
        raise ValueError("expected source revision is required for exact-release verification")
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
            verify_skill_archive(path, portable=False, root=root, expected_revision=expected_revision)
        elif kind == "portable":
            verify_skill_archive(path, portable=True, root=root, expected_revision=expected_revision)
        else:
            verify_brand_archive(
                path,
                contract["slug"],
                contract["version"],
                expected_filename=filename,
                expected_canon=str(metadata["canon_version"]),
                expected_revision=expected_revision,
                expected_release_version=str(metadata["version"]),
                expected_release_impact=metadata["release_impact"],
                require_release=require_release,
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


def expected_publication_packages(metadata: Mapping[str, object]) -> list[Dict[str, str]]:
    brands = metadata.get("brands", {})
    return [
        package_identity(slug, str(brands[slug]["version"]), str(metadata["version"]))
        for slug in sorted(PRODUCTION)
        if slug in brands
    ]


def verify_publication_record(path: Path, metadata: Mapping[str, object], revision: str,
                              require_release: bool = False) -> Mapping[str, object]:
    record = json.loads(read_text(path))
    version = str(metadata["version"])
    expected_tag = "v%s" % version
    expected_skill = "shruggie-brandbuilder-%s.skill" % version
    expected_release_url = "https://github.com/ShruggieTech/shruggie-brand/releases/tag/%s" % expected_tag
    expected_skill_url = "https://github.com/ShruggieTech/shruggie-brand/releases/download/%s/%s" % (expected_tag, expected_skill)
    required = {"schemaVersion", "status", "version", "tag", "sourceRevision", "releaseUrl", "skillFilename", "skillUrl", "packages"}
    if set(record) != required:
        raise ValueError("publication record fields disagree")
    if record["schemaVersion"] != 1 or record["version"] != version or record["tag"] != expected_tag:
        raise ValueError("publication record release identity disagrees")
    if record["sourceRevision"] != revision:
        raise ValueError("publication record source revision disagrees")
    if record["skillFilename"] != expected_skill or record["skillUrl"] != expected_skill_url:
        raise ValueError("publication record skill destination disagrees")
    if record["releaseUrl"] != expected_release_url:
        raise ValueError("publication record release destination is not exact")
    if record["packages"] != expected_publication_packages(metadata):
        raise ValueError("publication record package inventory disagrees")
    if require_release and record["status"] != "release":
        raise ValueError("production publication requires exact release status")
    if record["status"] not in {"candidate", "release"}:
        raise ValueError("publication record status is invalid")
    return record


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
    verify_parser.add_argument("--revision")
    verify_parser.add_argument("--require-release", action="store_true")
    publication_parser = subparsers.add_parser("publication", help="verify generated site publication metadata")
    publication_parser.add_argument("--version", required=True)
    publication_parser.add_argument("--record", type=Path, required=True)
    publication_parser.add_argument("--revision", required=True)
    publication_parser.add_argument("--require-release", action="store_true")
    args = parser.parse_args()

    if args.command == "current":
        print(current_version(ROOT))
        return 0

    metadata = load_metadata(ROOT, args.version)
    if args.command == "notes":
        write_notes(args.output, render_notes(metadata))
        print("wrote validated v%s notes to %s" % (args.version, args.output))
    elif args.command == "verify":
        verify_release_directory(args.release_dir, metadata, args.notes, args.revision, args.require_release)
        print("verified %d v%s release assets and generated notes"
              % (len(expected_assets(metadata)), args.version))
    else:
        verify_publication_record(args.record, metadata, args.revision, args.require_release)
        print("verified %s publication record for v%s" % ("release" if args.require_release else "candidate", args.version))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
