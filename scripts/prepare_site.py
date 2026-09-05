#!/usr/bin/env python3
"""Materialize the static site from verified production kits in dist/."""

from __future__ import annotations

import json
import re
import shutil
import sys
from html import escape
from pathlib import Path
from typing import Optional, Set

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SITE = ROOT / "site"
PUBLIC = SITE / "public"
GENERATED = SITE / "generated"
REFERENCES = ROOT / "skill" / "references"
TEMPLATES = ROOT / "skill" / "templates"
sys.path.insert(0, str(TEMPLATES))
from brand_contract import affiliation, public_showcase
DOC_DESCRIPTIONS = {
    "00-variance-contract": "The rules that keep every identity distinct while preserving a shared standard.",
    "01-canon": "Machine-readable defaults and constraints used by the brand generator.",
    "02-kit-anatomy": "The files, formats, and structure delivered in every brand kit.",
    "03-interview": "The discovery questions that turn business context into brand direction.",
    "04-toolchain": "The tools and validation stages behind a production-ready kit.",
    "05-shadcn-binding": "How brand tokens become installable shadcn registry resources.",
    "06-logo-protocol": "Requirements for supplied marks and rules for creating new logo systems.",
    "07-voice": "How strategy becomes a consistent verbal identity.",
    "08-glyph-construction": "Geometry and validation rules for constructing brand marks.",
    "09-portability": "Requirements that keep brand assets useful across platforms and teams.",
}


def write_utf8(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def production_slugs(root: Path = ROOT) -> set[str]:
    return {path.parent.name for path in (root / "brands").glob("*/brand.json")}


def source_dirs(dist: Path = DIST, expected: Optional[Set[str]] = None) -> list[Path]:
    expected = production_slugs() if expected is None else expected
    found = {path.parent.name: path.parent for path in dist.glob("*/brand.json")}
    missing = sorted(expected - set(found))
    unexpected = sorted(set(found) - expected)
    if missing or unexpected:
        details = []
        if missing:
            details.append(f"missing {missing}")
        if unexpected:
            details.append(f"unexpected {unexpected}")
        raise ValueError("dist output does not match production brands: " + "; ".join(details))
    return [found[slug] for slug in sorted(found)]


def replace_tree(source: Path, destination: Path) -> None:
    resolved = destination.resolve()
    try:
        resolved.relative_to(PUBLIC.resolve())
    except ValueError as error:
        raise ValueError(f"refusing to replace path outside site/public: {resolved}") from error
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def load_brand(source: Path) -> dict:
    return json.loads((source / "brand.json").read_text(encoding="utf-8"))


def validate_registry(source: Path, brand: dict) -> None:
    registry_dir = source / "nextjs" / "registry"
    catalog = json.loads((registry_dir / "registry.json").read_text(encoding="utf-8"))
    if catalog.get("$schema") != "https://ui.shadcn.com/schema/registry.json":
        raise ValueError(f"{brand['slug']}: registry schema is missing")
    names = {item["name"] for item in catalog.get("items", [])}
    if not {"theme", "fonts"}.issubset(names) or not (registry_dir / "theme.json").is_file() or not (registry_dir / "fonts.json").is_file():
        raise ValueError(f"{brand['slug']}: registry theme or fonts item is missing")
    expected = f"https://brand.shruggie.tech/{brand['slug']}/brand"
    if brand.get("registry_base") != expected:
        raise ValueError(f"{brand['slug']}: registry_base must be {expected}")
    for path in registry_dir.glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))


def validate_source_identity(source: Path, brand: dict, seen: set[str]) -> None:
    slug = brand.get("slug")
    if slug != source.name:
        raise ValueError(f"brand slug {slug!r} must match source directory {source.name!r}")
    if slug in seen:
        raise ValueError(f"duplicate brand slug: {slug}")
    seen.add(slug)


def remove_stale_public_brands(public: Path, expected: set[str]) -> list[str]:
    removed = []
    for child in public.iterdir():
        generated = (child / "brand" / "r" / "registry.json").is_file() and (child / "downloads" / "files").is_dir()
        if child.is_dir() and child.name not in expected and generated:
            resolved = child.resolve()
            try:
                resolved.relative_to(public.resolve())
            except ValueError as error:
                raise ValueError(f"refusing to remove path outside site/public: {resolved}") from error
            shutil.rmtree(child)
            removed.append(child.name)
    return removed


def add_guideline_metadata(path: Path, brand: dict) -> None:
    canonical = f"https://brand.shruggie.tech/{brand['slug']}/guidelines/"
    title = f"{brand['title']} guidelines | ShruggieTech"
    description = brand["descriptor"]
    preview = "https://brand.shruggie.tech/social-preview.png"
    tags = (
        f'<meta name="description" content="{escape(description, quote=True)}">'
        f'<link rel="canonical" href="{canonical}">'
        f'<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
        f'<meta property="og:type" content="website"><meta property="og:title" content="{escape(title, quote=True)}">'
        f'<meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{canonical}">'
        f'<meta property="og:image" content="{preview}"><meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{escape(title, quote=True)}"><meta name="twitter:description" content="{escape(description, quote=True)}">'
        f'<meta name="twitter:image" content="{preview}">'
    )
    content = path.read_text(encoding="utf-8")
    if "<head>" not in content:
        raise ValueError(f"guideline page lacks a head element: {path}")
    content, title_count = re.subn(r"<title>.*?</title>", f"<title>{escape(title)}</title>", content, count=1, flags=re.DOTALL)
    if title_count != 1:
        raise ValueError(f"guideline page lacks exactly one title element: {path}")
    write_utf8(path, content.replace("<head>", "<head>" + tags, 1))


def copy_kit(source: Path, brand: dict) -> dict:
    slug = brand["slug"]
    guide = source / "brand-guide.pdf"
    if not guide.is_file():
        raise ValueError(f"{slug}: verified public brand guide is missing")
    target = PUBLIC / slug
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    replace_tree(source / "guidelines", target / "guidelines")
    add_guideline_metadata(target / "guidelines" / "index.html", brand)
    replace_tree(source / "nextjs" / "registry", target / "brand" / "r")
    downloads = target / "downloads" / "files"
    downloads.mkdir(parents=True)
    shutil.copy2(guide, downloads / f"{slug}-brand-guide.pdf")
    for name in ("logos", "favicons", "specimens"):
        replace_tree(source / name, downloads / name)
    specimen_name = next((source / "specimens").glob("*.svg")).name
    logo_root = f"/{slug}/downloads/files/logos/svg"
    aff = affiliation(brand)
    return {
        "slug": slug,
        "title": brand["title"],
        "kind": brand.get("kind", "sub-brand"),
        "descriptor": brand["descriptor"],
        "idea": brand["brand_idea"],
        "version": brand["version"],
        "accent": brand["accent"]["bright"],
        "accentAccessible": brand["accent"]["accessible"],
        "logo": f"{logo_root}/{slug}-horizontal-color.svg",
        "icon": f"{logo_root}/{slug}-mark-color.svg",
        "specimen": f"/{slug}/downloads/files/specimens/{specimen_name}",
        "ownership": aff["ownership"],
        "showcase": aff["showcase"],
        "inheritance": aff["inheritance"],
        "parent": aff["parent"],
        "endorsement": aff["endorsement"],
        "serviceCredit": aff["service_credit"],
    }


def derive_public_markdown(content: str) -> tuple[str, str]:
    lines = content.splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), "Brand system")
    title = re.sub(r"\bCanon\b", "Brand system", title)
    title = re.sub(r"\bcanon\b", "brand system", title)
    removed_heading = False
    fenced = False
    output: list[str] = []
    pattern = re.compile(r"\bcanon\b", re.IGNORECASE)
    retired_endorsement = re.compile(r"a shruggietech project", re.IGNORECASE)
    for line in lines:
        if not removed_heading and line.startswith("# "):
            removed_heading = True
            continue
        if line.lstrip().startswith("```"):
            fenced = not fenced
            output.append(line)
            continue
        if fenced:
            output.append(line)
            continue
        parts = re.split(r"(`[^`]*`)", line)
        for index in range(0, len(parts), 2):
            parts[index] = pattern.sub(lambda match: "Brand system" if match.group(0)[0].isupper() else "brand system", parts[index])
            parts[index] = retired_endorsement.sub("Brand system by ShruggieTech", parts[index])
        output.append("".join(parts))
    normalized: list[str] = []
    index = 0
    fenced = False
    while index < len(output):
        line = output[index]
        if line.lstrip().startswith("```"):
            fenced = not fenced
            normalized.append(line)
            index += 1
            continue
        if not fenced and line.startswith("    "):
            block: list[str] = []
            while index < len(output):
                candidate = output[index]
                if candidate.startswith("    "):
                    block.append(candidate[4:])
                    index += 1
                elif not candidate.strip() and index + 1 < len(output) and output[index + 1].startswith("    "):
                    block.append("")
                    index += 1
                else:
                    break
            normalized.extend(["```text", *block, "```"])
            continue
        if not fenced:
            parts = re.split(r"(`[^`]*`)", line)
            for part_index in range(0, len(parts), 2):
                parts[part_index] = re.sub(r"<([^>]+)>", r"&lt;\1&gt;", parts[part_index])
            line = "".join(parts)
        normalized.append(line)
        index += 1
    return title, "\n".join(normalized).strip() + "\n"


def write_docs(references: Path, output: Path, descriptions: dict[str, str] = DOC_DESCRIPTIONS) -> list[dict[str, str]]:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    records = []
    pages = ["index"]
    for path in sorted(references.glob("*.md")):
        title, body = derive_public_markdown(path.read_text(encoding="utf-8"))
        description = descriptions.get(path.stem, f"ShruggieTech guidance for {title.lower()}.")
        frontmatter = f"---\ntitle: {json.dumps(title)}\ndescription: {json.dumps(description)}\n---\n\n"
        write_utf8(output / f"{path.stem}.mdx", frontmatter + body)
        records.append({"slug": path.stem, "title": title, "description": description})
        pages.append(path.stem)
    index = """---
title: "How we build brands"
description: "The repeatable ShruggieTech system for building complete, usable brand identities."
---

We turn strategy into a complete identity, then package the standards, assets, and implementation tools that keep it coherent in real work.

[Download the ShruggieTech brand skill](https://github.com/ShruggieTech/shruggie-brand/releases/latest) or explore each part of the system below.
"""
    write_utf8(output / "index.mdx", index)
    write_utf8(output / "meta.json", json.dumps({"title": "How we build brands", "pages": pages}, indent=2) + "\n")
    return records


def install_registry_theme(source: Path) -> str:
    item = json.loads((source / "nextjs" / "registry" / "theme.json").read_text(encoding="utf-8"))
    variables = item.get("cssVars", {})
    sections = []
    for selector, key in ((":root", "light"), (".dark", "dark")):
        declarations = "\n".join(f"  --{name}: {value};" for name, value in variables.get(key, {}).items())
        sections.append(f"{selector} {{\n{declarations}\n}}")
    declarations = "\n".join(f"  --{name}: {value};" for name, value in variables.get("theme", {}).items())
    sections.insert(1, f":root {{\n{declarations}\n}}")
    return "/* Installed from the generated ShruggieTech shadcn registry theme. */\n" + "\n".join(sections) + "\n"


def copy_site_identity(source: Path) -> None:
    source_assets = ROOT / "brands" / "shruggietech" / "assets"
    files = {
        PUBLIC / "favicon.svg": [source / "favicons" / "favicon.svg", source / "logos" / "svg" / "shruggietech-mark-reduced-color.svg"],
        PUBLIC / "favicon-16x16.png": [source / "favicons" / "favicon-16x16.png", source_assets / "logo-icon-only-green.png"],
        PUBLIC / "favicon-32x32.png": [source / "favicons" / "favicon-32x32.png", source_assets / "logo-icon-only-green.png"],
        PUBLIC / "apple-touch-icon.png": [source / "favicons" / "apple-touch-icon.png", source_assets / "logo-icon-only-green.png"],
        PUBLIC / "android-chrome-192x192.png": [source / "favicons" / "android-chrome-192x192.png", source_assets / "logo-icon-only-green.png"],
        PUBLIC / "android-chrome-512x512.png": [source / "favicons" / "android-chrome-512x512.png", source_assets / "logo-icon-only-green.png"],
        PUBLIC / "shruggietech-logo.svg": [source / "logos" / "svg" / "shruggietech-horizontal-white.svg"],
        PUBLIC / "social-preview.png": [source / "logos" / "png" / "shruggietech-social-preview-1280.png", source_assets / "socialmedia_logo.png"],
    }
    for destination, candidates in files.items():
        origin = next((candidate for candidate in candidates if candidate.is_file()), None)
        if origin is None:
            raise ValueError(f"required site identity asset is missing: {candidates}")
        shutil.copy2(origin, destination)
    manifest = {"name": "Brands | ShruggieTech", "short_name": "ShruggieTech Brands", "start_url": "/", "display": "standalone", "background_color": "#080B0D", "theme_color": "#080B0D", "icons": [{"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}]}
    write_utf8(PUBLIC / "site.webmanifest", json.dumps(manifest, indent=2) + "\n")


def main() -> int:
    if not DIST.is_dir():
        raise SystemExit("dist/ is missing; run python scripts/build_all.py first")
    PUBLIC.mkdir(parents=True, exist_ok=True)
    GENERATED.mkdir(parents=True, exist_ok=True)
    brands = []
    seen: set[str] = set()
    sources = source_dirs()
    loaded = []
    for source in sources:
        brand = load_brand(source)
        validate_source_identity(source, brand, seen)
        validate_registry(source, brand)
        loaded.append((source, brand))
    public_sources = [(source, brand) for source, brand in loaded if public_showcase(brand)]
    remove_stale_public_brands(PUBLIC, {source.name for source, _ in public_sources})
    for source, brand in public_sources:
        brands.append(copy_kit(source, brand))
    parent = DIST / "shruggietech"
    parent_css = "\n".join((parent / "tokens" / name).read_text(encoding="utf-8") for name in ("colors.css", "spacing.css", "typography.css", "base.css"))
    write_utf8(GENERATED / "parent.css", parent_css)
    write_utf8(GENERATED / "registry-theme.css", install_registry_theme(parent))
    generated_fonts = GENERATED / "fonts"
    if generated_fonts.exists():
        shutil.rmtree(generated_fonts)
    shutil.copytree(ROOT / "assets" / "fonts" / "woff2", generated_fonts)
    write_utf8(GENERATED / "brands.json", json.dumps(brands, indent=2) + "\n")
    docs = write_docs(REFERENCES, GENERATED / "docs")
    copy_site_identity(parent)
    print(f"prepared {len(brands)} kits and {len(docs)} reference documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
