#!/usr/bin/env python3
"""Materialize the static site from verified production kits in dist/."""

from __future__ import annotations

import json
import re
import shutil
import sys
import textwrap
from html import escape
from pathlib import Path
from typing import Any, Optional, Set

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SITE = ROOT / "site"
PUBLIC = SITE / "public"
GENERATED = SITE / "generated"
REFERENCES = ROOT / "skill" / "references"
TEMPLATES = ROOT / "skill" / "templates"
SITE_URL = "https://brand.shruggie.tech"
ORGANIZATION_URL = "https://shruggie.tech"
SITE_DESCRIPTION = "Explore ShruggieTech brand identities, standards, assets, and the repeatable system behind them."
SOCIAL_SIZE = (1280, 640)
ALERT_TYPES = {"NOTE": "info", "WARNING": "warn", "CAUTION": "error"}
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


def make_route(key: str, kind: str, pathname: str, title: str, description: str, eyebrow: str,
               breadcrumbs: list[dict[str, str]], brand_slug: Optional[str] = None,
               docs_slug: Optional[str] = None) -> dict[str, Any]:
    canonical = f"{SITE_URL}{pathname}"
    social_path = f"/social/{key}.png"
    return {
        "key": key,
        "kind": kind,
        "pathname": pathname,
        "canonical": canonical,
        "title": title,
        "documentTitle": f"{title} | ShruggieTech",
        "description": description,
        "social": {
            "path": social_path,
            "url": f"{SITE_URL}{social_path}",
            "width": SOCIAL_SIZE[0],
            "height": SOCIAL_SIZE[1],
            "type": "image/png",
            "alt": f"{title} page preview on Brands | ShruggieTech",
            "eyebrow": eyebrow,
        },
        "breadcrumbs": breadcrumbs,
        "brandSlug": brand_slug,
        "docsSlug": docs_slug,
    }


def validate_routes(routes: list[dict[str, Any]]) -> None:
    seen_keys: set[str] = set()
    seen_paths: set[str] = set()
    seen_canonicals: set[str] = set()
    seen_socials: set[str] = set()
    for route in routes:
        key = route.get("key")
        if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", key):
            raise ValueError(f"unsafe route key: {key}")
        if key in seen_keys:
            raise ValueError(f"duplicate route key: {key}")
        seen_keys.add(key)
        pathname = route.get("pathname", "")
        if (not isinstance(pathname, str) or not pathname.startswith("/") or not pathname.endswith("/")
                or ".." in pathname or "\\" in pathname or "?" in pathname or "#" in pathname
                or "//" in pathname[1:]):
            raise ValueError(f"unsafe route pathname: {pathname}")
        if pathname in seen_paths:
            raise ValueError(f"duplicate route pathname: {pathname}")
        seen_paths.add(pathname)
        canonical = route.get("canonical")
        if canonical != f"{SITE_URL}{pathname}":
            raise ValueError(f"invalid canonical URL for {key}: {canonical}")
        if canonical in seen_canonicals:
            raise ValueError(f"duplicate canonical URL: {canonical}")
        seen_canonicals.add(canonical)
        social = route.get("social", {})
        social_path = social.get("path", "")
        if not re.fullmatch(r"/social/[a-z0-9][a-z0-9-]*\.png", social_path):
            raise ValueError(f"unsafe social preview path for {key}: {social_path}")
        if social_path in seen_socials:
            raise ValueError(f"duplicate social preview path: {social_path}")
        seen_socials.add(social_path)
        if social.get("url") != f"{SITE_URL}{social_path}" or social.get("width") != SOCIAL_SIZE[0] or social.get("height") != SOCIAL_SIZE[1] or social.get("type") != "image/png":
            raise ValueError(f"invalid social preview contract for {key}")


def structured_data(route: dict[str, Any], routes: list[dict[str, Any]], brands: list[dict]) -> dict[str, Any]:
    organization = {"@type": "Organization", "@id": ORGANIZATION_URL, "name": "ShruggieTech", "url": ORGANIZATION_URL}
    website_id = f"{SITE_URL}/#website"
    website = {"@type": "WebSite", "@id": website_id, "url": f"{SITE_URL}/", "name": "Brands | ShruggieTech", "publisher": {"@id": ORGANIZATION_URL}}
    kind_types = {"home": "CollectionPage", "brand": "WebPage", "downloads": "CollectionPage", "guidelines": "WebPage", "docs-index": "CollectionPage", "docs-page": "TechArticle"}
    page_id = f"{route['canonical']}#webpage"
    page: dict[str, Any] = {"@type": kind_types[route["kind"]], "@id": page_id, "url": route["canonical"], "name": route["documentTitle"], "description": route["description"], "isPartOf": {"@id": website_id}, "publisher": {"@id": ORGANIZATION_URL}}
    graph: list[dict[str, Any]] = [organization, website, page]
    if route["kind"] == "home":
        brand_urls = [item["canonical"] for item in routes if item["kind"] == "brand"]
        page["mainEntity"] = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": index, "url": url} for index, url in enumerate(brand_urls, 1)]}
    if route["kind"] == "docs-page":
        page["mainEntityOfPage"] = {"@id": page_id}
    if route["kind"] == "brand":
        brand = next(item for item in brands if item["slug"] == route["brandSlug"])
        brand_id = f"{route['canonical']}#brand"
        page["mainEntity"] = {"@id": brand_id}
        graph.append({"@type": "Brand", "@id": brand_id, "name": brand["title"], "description": brand["descriptor"], "url": route["canonical"], "logo": f"{SITE_URL}{brand['icon']}"})
    if route["breadcrumbs"]:
        breadcrumb_id = f"{route['canonical']}#breadcrumb"
        page["breadcrumb"] = {"@id": breadcrumb_id}
        graph.append({"@type": "BreadcrumbList", "@id": breadcrumb_id, "itemListElement": [{"@type": "ListItem", "position": index, "name": item["name"], "item": item["url"]} for index, item in enumerate(route["breadcrumbs"], 1)]})
    return {"@context": "https://schema.org", "@graph": graph}


def build_routes(brands: list[dict], docs: list[dict[str, str]]) -> list[dict[str, Any]]:
    home = {"name": "Brands", "url": f"{SITE_URL}/"}
    docs_root = {"name": "How we build brands", "url": f"{SITE_URL}/docs/"}
    routes = [make_route("home", "home", "/", "Brands", SITE_DESCRIPTION, "Brand portfolio", [])]
    for brand in sorted(brands, key=lambda item: item["slug"]):
        slug = brand["slug"]
        brand_path = f"/{slug}/"
        brand_crumb = {"name": brand["title"], "url": f"{SITE_URL}{brand_path}"}
        routes.extend([
            make_route(f"brand-{slug}", "brand", brand_path, brand["title"], brand["descriptor"], "Brand portfolio", [home, brand_crumb], brand_slug=slug),
            make_route(f"downloads-{slug}", "downloads", f"/{slug}/downloads/", f"{brand['title']} downloads", f"Download the {brand['title']} brand guide and asset collections.", "Brand assets", [home, brand_crumb, {"name": "Downloads", "url": f"{SITE_URL}/{slug}/downloads/"}], brand_slug=slug),
            make_route(f"guidelines-{slug}", "guidelines", f"/{slug}/guidelines/", f"{brand['title']} guidelines", brand["descriptor"], "Brand guidelines", [home, brand_crumb, {"name": "Guidelines", "url": f"{SITE_URL}/{slug}/guidelines/"}], brand_slug=slug),
        ])
    routes.append(make_route("docs", "docs-index", "/docs/", "How we build brands", "The repeatable ShruggieTech system for building complete, usable brand identities.", "Documentation", [home, docs_root]))
    for doc in sorted(docs, key=lambda item: item["slug"]):
        pathname = f"/docs/{doc['slug']}/"
        routes.append(make_route(f"docs-{doc['slug']}", "docs-page", pathname, doc["title"], doc["description"], "Documentation", [home, docs_root, {"name": doc["title"], "url": f"{SITE_URL}{pathname}"}], docs_slug=doc["slug"]))
    validate_routes(routes)
    for route in routes:
        route["structuredData"] = structured_data(route, routes, brands)
    return routes


def generate_social_previews(routes: list[dict[str, Any]], public: Path, mark_path: Path,
                             display_font_path: Path, body_font_path: Path) -> None:
    social_root = public / "social"
    resolved = social_root.resolve()
    try:
        resolved.relative_to(public.resolve())
    except ValueError as error:
        raise ValueError(f"refusing to replace social previews outside site/public: {resolved}") from error
    if social_root.exists():
        shutil.rmtree(social_root)
    social_root.mkdir(parents=True)
    with Image.open(mark_path) as source_mark:
        mark = source_mark.convert("RGBA")
    mark.thumbnail((300, 210), Image.Resampling.LANCZOS)
    eyebrow_font = ImageFont.truetype(str(body_font_path), 28)
    title_font = ImageFont.truetype(str(display_font_path), 68)
    body_font = ImageFont.truetype(str(body_font_path), 28)
    footer_font = ImageFont.truetype(str(body_font_path), 22)
    for route in routes:
        destination = public / route["social"]["path"].lstrip("/")
        try:
            destination.resolve().relative_to(social_root.resolve())
        except ValueError as error:
            raise ValueError(f"unsafe social preview destination: {destination}") from error
        canvas = Image.new("RGBA", SOCIAL_SIZE, (0, 0, 0, 255))
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle((38, 38, 1242, 602), radius=28, fill=(13, 15, 18, 255), outline=(38, 38, 38, 255), width=2)
        draw.rectangle((72, 86, 82, 554), fill=(43, 204, 115, 255))
        draw.text((120, 92), route["social"]["eyebrow"].upper(), font=eyebrow_font, fill=(43, 204, 115, 255))
        y = 150
        for line in textwrap.wrap(route["title"], width=27, break_long_words=False)[:3]:
            draw.text((120, y), line, font=title_font, fill=(245, 245, 245, 255))
            y += 78
        y += 12
        for line in textwrap.wrap(route["description"], width=58, break_long_words=False)[:3]:
            draw.text((120, y), line, font=body_font, fill=(209, 211, 212, 255))
            y += 39
        mark_x = 1160 - mark.width
        mark_y = 92
        canvas.alpha_composite(mark, (mark_x, mark_y))
        draw.text((120, 530), "brand.shruggie.tech", font=footer_font, fill=(154, 154, 154, 255))
        canvas.save(destination, format="PNG", optimize=False)


def add_guideline_metadata(path: Path, route: dict[str, Any]) -> None:
    canonical = route["canonical"]
    title = route["documentTitle"]
    description = route["description"]
    preview = route["social"]
    preview_url = preview["url"]
    preview_width = preview["width"]
    preview_height = preview["height"]
    preview_type = preview["type"]
    preview_alt = escape(preview["alt"], quote=True)
    json_ld = json.dumps(route["structuredData"], ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    tags = (
        f'<meta name="description" content="{escape(description, quote=True)}">'
        f'<link rel="canonical" href="{canonical}">'
        f'<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
        f'<meta property="og:type" content="website"><meta property="og:title" content="{escape(title, quote=True)}">'
        f'<meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{canonical}">'
        f'<meta property="og:image" content="{preview_url}"><meta property="og:image:width" content="{preview_width}">'
        f'<meta property="og:image:height" content="{preview_height}"><meta property="og:image:type" content="{preview_type}">'
        f'<meta property="og:image:alt" content="{preview_alt}"><meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{escape(title, quote=True)}"><meta name="twitter:description" content="{escape(description, quote=True)}">'
        f'<meta name="twitter:image" content="{preview_url}"><meta name="twitter:image:alt" content="{preview_alt}">'
        f'<script type="application/ld+json">{json_ld}</script>'
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
    replace_tree(source / "nextjs" / "registry", target / "brand" / "r")
    downloads = target / "downloads" / "files"
    downloads.mkdir(parents=True)
    shutil.copy2(guide, downloads / f"{slug}-brand-guide.pdf")
    for name in ("logos", "favicons", "icons", "specimens"):
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


def convert_documentation_alerts(content: str) -> str:
    """Convert explicit GitHub alert blockquotes into Fumadocs callouts."""
    lines = content.splitlines()
    output: list[str] = []
    index = 0
    fenced = False
    marker = re.compile(r"^>\s*\[!([A-Z]+)\]\s*$")
    while index < len(lines):
        line = lines[index]
        if line.lstrip().startswith("```"):
            fenced = not fenced
            output.append(line)
            index += 1
            continue
        match = marker.match(line) if not fenced else None
        if not match:
            output.append(line)
            index += 1
            continue
        name = match.group(1)
        if name not in ALERT_TYPES:
            raise ValueError(f"unsupported documentation alert: {name}")
        body: list[str] = []
        index += 1
        while index < len(lines) and lines[index].startswith(">"):
            quoted = lines[index][1:]
            if quoted.startswith(" "):
                quoted = quoted[1:]
            body.append(quoted)
            index += 1
        if not any(part.strip() for part in body):
            raise ValueError(f"documentation alert {name} has no body")
        output.extend([f'<Callout type="{ALERT_TYPES[name]}">', *body, "</Callout>"])
    return "\n".join(output)


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
    return title, convert_documentation_alerts("\n".join(normalized)).strip() + "\n"


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


def copy_site_identity(source: Path, public: Path = PUBLIC) -> None:
    web = source / "icons" / "web"
    source_manifest = web / "site.webmanifest"
    files = {
        public / "favicon.svg": web / "favicon.svg",
        public / "favicon-16x16.png": web / "favicon-16x16.png",
        public / "favicon-32x32.png": web / "favicon-32x32.png",
        public / "favicon.ico": web / "favicon.ico",
        public / "apple-touch-icon.png": web / "apple-touch-icon.png",
        public / "android-chrome-192x192.png": web / "android-chrome-192x192.png",
        public / "android-chrome-512x512.png": web / "android-chrome-512x512.png",
        public / "shruggietech-logo.svg": source / "logos" / "svg" / "shruggietech-horizontal-white.svg",
        public / "shruggietech-logo-dark.svg": source / "logos" / "svg" / "shruggietech-horizontal-white.svg",
        public / "shruggietech-logo-light.svg": source / "logos" / "svg" / "shruggietech-horizontal-black.svg",
        public / "social-preview.png": source / "logos" / "png" / "shruggietech-social-preview-1280.png",
    }
    missing = [origin for origin in [*files.values(), source_manifest] if not origin.is_file()]
    if missing:
        raise ValueError(f"required generated site identity asset is missing: {missing[0]}")
    manifest = json.loads(source_manifest.read_text(encoding="utf-8"))
    for destination, origin in files.items():
        shutil.copy2(origin, destination)
    manifest.update({"name": "Brands | ShruggieTech", "short_name": "ShruggieTech Brands", "start_url": "/"})
    write_utf8(public / "site.webmanifest", json.dumps(manifest, indent=2) + "\n")


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
    routes = build_routes(brands, docs)
    for brand in brands:
        route = next(item for item in routes if item["kind"] == "guidelines" and item["brandSlug"] == brand["slug"])
        add_guideline_metadata(PUBLIC / brand["slug"] / "guidelines" / "index.html", route)
    write_utf8(GENERATED / "routes.json", json.dumps({"siteUrl": SITE_URL, "routes": routes}, indent=2, ensure_ascii=False) + "\n")
    generate_social_previews(
        routes,
        PUBLIC,
        ROOT / "brands" / "shruggietech" / "assets" / "socialmedia_logo.png",
        ROOT / "assets" / "fonts" / "ttf" / "SpaceGrotesk-Bold.ttf",
        ROOT / "assets" / "fonts" / "ttf" / "Geist-Medium.ttf",
    )
    copy_site_identity(parent)
    print(f"prepared {len(brands)} kits and {len(docs)} reference documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
