#!/usr/bin/env python3
"""Materialize the static site from verified production kits in dist/."""

from __future__ import annotations

import copy
import hashlib
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
sys.path.insert(0, str(TEMPLATES))
from brand_contract import affiliation, custom_assets, guide_surface_mode, public_showcase, showcase_surface, social_copy, vendor_boundary
from documentation_contract import load_documentation_contract, manual_catalog, validate_route_dispositions
from gen_conformance import verify_conformance
from package_release import write_brand_archive
from release_contract import PRODUCTION
from documentation_publication import build_record as documentation_publication_record
from documentation_render import (OVERVIEW_DESCRIPTION, convert_documentation_alerts,
                                  derive_public_markdown, render_index, render_page)
from interface_contract import package_identity
from registry_contract import validate_registry as validate_registry_delivery
DOCUMENTATION_CONTRACT = load_documentation_contract()
DOCUMENTATION_CATALOG = manual_catalog(DOCUMENTATION_CONTRACT)
DOC_DESCRIPTIONS = {page["slug"]: page["description"] for page in DOCUMENTATION_CATALOG}
DOC_NAVIGATION = {page["slug"]: (page["section"], page["section_order"], page["label"], page["order"]) for page in DOCUMENTATION_CATALOG}
BRAND_TOPIC_CONTRACT = [
    ("overview", "Overview", "Overview", 0),
    ("voice", "Voice", "Voice", 0),
    ("logos", "Logo", "Identity", 0),
    ("color", "Color", "Identity", 1),
    ("typography", "Typography", "Identity", 2),
    ("components", "Components", "Components", 0),
    ("assets", "Assets", "Assets", 0),
    ("integration", "Integration", "Integration", 0),
]


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


def copy_verified_specimens(source: Path, destination: Path) -> str:
    """Copy the verified specimen tree and prove the hosted bytes are identical."""
    specimens = sorted(path for path in source.rglob("*") if path.is_file())
    svg_specimens = [path for path in specimens if path.suffix.lower() == ".svg"]
    if len(svg_specimens) != 1:
        raise ValueError(f"expected one verified SVG specimen, found {len(svg_specimens)}")
    replace_tree(source, destination)
    source_inventory = {path.relative_to(source).as_posix(): path.read_bytes() for path in specimens}
    hosted_inventory = {
        path.relative_to(destination).as_posix(): path.read_bytes()
        for path in destination.rglob("*") if path.is_file()
    }
    if hosted_inventory != source_inventory:
        raise ValueError("hosted specimen differs from the verified kit specimen")
    return svg_specimens[0].name


def load_brand(source: Path) -> dict:
    return json.loads((source / "brand.json").read_text(encoding="utf-8"))


def validate_registry(source: Path, brand: dict) -> None:
    registry_dir = source / "nextjs" / "registry"
    expected = f"https://brand.shruggie.tech/{brand['slug']}/brand"
    if brand.get("registry_base") != expected:
        raise ValueError(f"{brand['slug']}: registry_base must be {expected}")
    validate_registry_delivery(registry_dir, brand["slug"])
    catalog = json.loads((registry_dir / "registry.json").read_text(encoding="utf-8"))
    declared = {"theme"} | {
        re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()
        for name in (brand.get("domain_components") or {})
    }
    advertised = {item["name"] for item in catalog["items"]}
    if advertised != declared:
        raise ValueError(f"{brand['slug']}: registry catalog differs from declared components")


def validate_portal_navigation(portal: dict[str, Any], slug: str) -> None:
    topics = portal.get("topics")
    if not isinstance(topics, list):
        raise ValueError(f"{slug}: guideline topics are missing")
    actual = [(topic.get("key"), topic.get("label"), topic.get("section"), topic.get("order")) for topic in topics]
    has_expressions = any(family.get("key") == "expressions" and family.get("assets") for family in portal.get("asset_families", []))
    expected_topics = BRAND_TOPIC_CONTRACT.copy()
    if has_expressions:
        expected_topics.insert(6, ("expressions", "Expressions", "Identity", 3))
    if actual != expected_topics:
        raise ValueError(f"{slug}: guideline navigation differs from the authoritative hierarchy")
    expected_paths = {
        key: f"/{slug}/downloads/" if key == "assets" else f"/{slug}/guidelines/" if key == "overview" else f"/{slug}/guidelines/{key}/"
        for key, _, _, _ in expected_topics
    }
    paths = [topic.get("path") for topic in topics]
    if paths != [expected_paths[topic["key"]] for topic in topics] or len(paths) != len(set(paths)):
        raise ValueError(f"{slug}: guideline navigation contains an invalid or duplicate destination")


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
               docs_slug: Optional[str] = None, guide_topic: Optional[str] = None,
               vendor_notice: Optional[str] = None, social_alt: Optional[str] = None) -> dict[str, Any]:
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
            "alt": (social_alt or f"{title} page preview on Brands | ShruggieTech") + (", independent third-party project" if vendor_notice else ""),
            "eyebrow": eyebrow,
        },
        "breadcrumbs": breadcrumbs,
        "brandSlug": brand_slug,
        "docsSlug": docs_slug,
        "guideTopic": guide_topic,
        "vendorBoundary": vendor_notice,
        "vendorBoundaryUrl": f"{SITE_URL}/{brand_slug}/guidelines/" if vendor_notice and brand_slug else None,
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
    kind_types = {"home": "CollectionPage", "downloads": "CollectionPage", "guidelines": "WebPage", "guidelines-topic": "WebPage", "docs-index": "CollectionPage", "docs-page": "TechArticle", "conformance-index": "CollectionPage", "conformance": "WebPage"}
    page_id = f"{route['canonical']}#webpage"
    page: dict[str, Any] = {"@type": kind_types[route["kind"]], "@id": page_id, "url": route["canonical"], "name": route["documentTitle"], "description": route["description"], "isPartOf": {"@id": website_id}, "publisher": {"@id": ORGANIZATION_URL}}
    graph: list[dict[str, Any]] = [organization, website, page]
    if route["kind"] == "home":
        brand_urls = [item["canonical"] for item in routes if item["kind"] == "guidelines"]
        page["mainEntity"] = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": index, "url": url} for index, url in enumerate(brand_urls, 1)]}
    if route["kind"] == "docs-page":
        page["mainEntityOfPage"] = {"@id": page_id}
    if route["kind"] == "guidelines":
        brand = next(item for item in brands if item["slug"] == route["brandSlug"])
        brand_id = f"{route['canonical']}#brand"
        page["mainEntity"] = {"@id": brand_id}
        entity = {"@type": "Brand", "@id": brand_id, "name": brand["title"], "description": brand["descriptor"], "url": route["canonical"], "logo": f"{SITE_URL}{brand['icon']}"}
        if route.get("vendorBoundary"):
            entity["disambiguatingDescription"] = route["vendorBoundary"]
            entity["usageInfo"] = route["vendorBoundaryUrl"]
        graph.append(entity)
    if route["breadcrumbs"]:
        breadcrumb_id = f"{route['canonical']}#breadcrumb"
        page["breadcrumb"] = {"@id": breadcrumb_id}
        graph.append({"@type": "BreadcrumbList", "@id": breadcrumb_id, "itemListElement": [{"@type": "ListItem", "position": index, "name": item["name"], "item": item["url"]} for index, item in enumerate(route["breadcrumbs"], 1)]})
    return {"@context": "https://schema.org", "@graph": graph}


def build_routes(brands: list[dict], docs: list[dict[str, str]], portals: Optional[list[dict[str, Any]]] = None) -> list[dict[str, Any]]:
    home = {"name": "Brands", "url": f"{SITE_URL}/"}
    docs_root = {"name": "Documentation", "url": f"{SITE_URL}/docs/"}
    conformance_root = {"name": "Conformance", "url": f"{SITE_URL}/conformance/"}
    routes = [make_route("home", "home", "/", "Brands", SITE_DESCRIPTION, "Brand portfolio", [])]
    routes.append(make_route("conformance", "conformance-index", "/conformance/", "Interface conformance", "Inspect generated browser reference specimens and exact cross-host evidence boundaries for every production brand.", "Interface conformance", [home, conformance_root]))
    portal_by_slug = {portal["brand"]["slug"]: portal for portal in (portals or [])}
    for brand in sorted(brands, key=lambda item: item["slug"]):
        slug = brand["slug"]
        guidelines_path = f"/{slug}/guidelines/"
        brand_crumb = {"name": brand["title"], "url": f"{SITE_URL}{guidelines_path}"}
        portal = portal_by_slug.get(slug)
        vendor_notice = brand.get("vendorBoundary")
        topics = portal["topics"] if portal else [{"key": "overview", "title": "Guidelines", "description": brand["descriptor"]}]
        if portal:
            validate_portal_navigation(portal, slug)
        overview = topics[0]
        routes.extend([
            make_route(f"downloads-{slug}", "downloads", f"/{slug}/downloads/", f"{brand['title']} assets", f"Browse and download the complete {brand['title']} brand asset collection.", "Brand assets", [home, brand_crumb, {"name": "Assets", "url": f"{SITE_URL}/{slug}/downloads/"}], brand_slug=slug, guide_topic="assets", vendor_notice=vendor_notice),
            make_route(f"guidelines-{slug}", "guidelines", guidelines_path, f"{brand['title']} guidelines", overview["description"], "Brand guidelines", [home, brand_crumb], brand_slug=slug, guide_topic=overview["key"], vendor_notice=vendor_notice, social_alt=(f"{brand['title']} logo with slogan: {brand['socialSlogan']}" if brand.get("socialSlogan") else None)),
            make_route(f"conformance-{slug}", "conformance", f"/conformance/{slug}/", f"{brand['title']} interface conformance", f"Inspect the generated browser reference and cross-host evidence boundary for {brand['title']}.", "Interface conformance", [home, conformance_root, {"name": brand["title"], "url": f"{SITE_URL}/conformance/{slug}/"}], brand_slug=slug, vendor_notice=vendor_notice),
        ])
        for topic in topics[1:]:
            if topic["key"] == "assets":
                continue
            pathname = topic.get("path", f"/{slug}/guidelines/{topic['key']}/")
            routes.append(make_route(f"guidelines-{slug}-{topic['key']}", "guidelines-topic", pathname, f"{topic['title']} | {brand['title']}", topic["description"], "Brand guidelines", [home, brand_crumb, {"name": topic.get("label", topic["title"]), "url": f"{SITE_URL}{pathname}"}], brand_slug=slug, guide_topic=topic["key"], vendor_notice=vendor_notice))
    routes.append(make_route("docs", "docs-index", "/docs/", "Documentation", "The repeatable ShruggieTech system for building complete, usable brand identities.", "Documentation", [home, docs_root]))
    for doc in sorted(docs, key=lambda item: item["slug"]):
        pathname = f"/docs/{doc['slug']}/"
        routes.append(make_route(f"docs-{doc['slug']}", "docs-page", pathname, doc["title"], doc["description"], "Documentation", [home, docs_root, {"name": doc["title"], "url": f"{SITE_URL}{pathname}"}], docs_slug=doc["slug"]))
    validate_routes(routes)
    validate_route_dispositions(routes, DOCUMENTATION_CONTRACT)
    for route in routes:
        route["structuredData"] = structured_data(route, routes, brands)
    return routes


def inline_segments(value: str) -> list[dict[str, str]]:
    segments: list[dict[str, str]] = []
    cursor = 0
    pattern = re.compile(r"`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)")
    for match in pattern.finditer(value):
        if match.start() > cursor:
            segments.append({"type": "text", "text": value[cursor:match.start()]})
        if match.group(1) is not None:
            segments.append({"type": "code", "text": match.group(1)})
        else:
            href = match.group(3)
            safe_relative = bool(re.fullmatch(r"[A-Za-z0-9._@/-]+", href)) and ".." not in href.split("/")
            if not (href.startswith("https://") or href.startswith("http://") or href.startswith("#") or safe_relative):
                raise ValueError(f"unsafe Markdown link: {href}")
            segments.append({"type": "link", "text": match.group(2), "href": href})
        cursor = match.end()
    if cursor < len(value):
        segments.append({"type": "text", "text": value[cursor:]})
    return segments or [{"type": "text", "text": ""}]


def markdown_blocks(content: str) -> list[dict[str, Any]]:
    """Convert the generated integration subset into safe semantic blocks."""
    lines = content.splitlines()
    blocks: list[dict[str, Any]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("```"):
            language = line[3:].strip()
            code: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code.append(lines[index]); index += 1
            if index >= len(lines):
                raise ValueError("unterminated instruction code fence")
            blocks.append({"type": "code", "language": language, "text": "\n".join(code)})
            index += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            blocks.append({"type": "heading", "depth": len(heading.group(1)), "segments": inline_segments(heading.group(2))})
            index += 1
            continue
        if line.startswith("|") and index + 1 < len(lines) and re.fullmatch(r"\|?[\s:|-]+\|?", lines[index + 1]):
            split = lambda row: [cell.strip() for cell in row.strip().strip("|").split("|")]
            headers = split(line)
            rows: list[list[list[dict[str, str]]]] = []
            index += 2
            while index < len(lines) and lines[index].startswith("|"):
                rows.append([inline_segments(cell) for cell in split(lines[index])]); index += 1
            blocks.append({"type": "table", "headers": headers, "rows": rows})
            continue
        list_match = re.match(r"^\s*([-*]|\d+\.)\s+(.+)$", line)
        if list_match:
            ordered = list_match.group(1).endswith(".")
            items = []
            while index < len(lines):
                item = re.match(r"^\s*([-*]|\d+\.)\s+(.+)$", lines[index])
                if not item or item.group(1).endswith(".") != ordered:
                    break
                items.append(inline_segments(item.group(2))); index += 1
            blocks.append({"type": "list", "ordered": ordered, "items": items})
            continue
        paragraph = [line.strip()]
        index += 1
        while index < len(lines) and lines[index].strip() and not re.match(r"^(#{1,6})\s+|^```|^\s*([-*]|\d+\.)\s+|^\|", lines[index]):
            paragraph.append(lines[index].strip()); index += 1
        blocks.append({"type": "paragraph", "segments": inline_segments(" ".join(paragraph))})
    return blocks


def project_portal(source: Path, payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("schema_version") != "1.0":
        raise ValueError(f"{source.name}: unsupported portal schema")
    if payload.get("brand", {}).get("slug") != source.name:
        raise ValueError(f"{source.name}: portal brand slug must match kit")
    implementation = payload.get("implementation")
    if not isinstance(implementation, dict) or implementation.get("schema_version") != 1:
        raise ValueError(f"{source.name}: portal implementation facts are missing or invalid")
    facts_path = source / "enforcement" / "documentation-facts.json"
    if not facts_path.is_file():
        raise ValueError(f"{source.name}: generated documentation facts are missing")
    expected_facts = json.loads(facts_path.read_text(encoding="utf-8"))
    if implementation != expected_facts:
        raise ValueError(f"{source.name}: hosted documentation facts differ from bundled facts")
    topics = payload.get("topics")
    if not isinstance(topics, list) or not topics or topics[0].get("key") != "overview":
        raise ValueError(f"{source.name}: portal must begin with overview")
    topic_keys = [topic.get("key") for topic in topics]
    if any(not isinstance(key, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", key) for key in topic_keys) or len(topic_keys) != len(set(topic_keys)):
        raise ValueError(f"{source.name}: portal topic keys must be unique and URL-safe")
    projected = copy.deepcopy(payload)
    governed = custom_assets(load_brand(source), source, public_only=True)
    expression_families = [family for family in projected.get("asset_families", []) if family.get("key") == "expressions"]
    if len(expression_families) != (1 if governed else 0):
        raise ValueError(f"{source.name}: expression family differs from eligible custom assets")
    if governed:
        records = expression_families[0].get("assets", [])
        if [item.get("id") for item in records] != [item["id"] for item in governed]:
            raise ValueError(f"{source.name}: expression inventory differs from eligible custom assets")
        for declared, record in zip(governed, records):
            if (record.get("title") != declared["title"] or record.get("summary") != declared["description"]
                    or record.get("role") != declared["role"] or record.get("preview_well") != declared["preview"]["well"]
                    or record.get("usage") != declared["usage"] or record.get("credit") != declared["credit"]
                    or record.get("accessibility") != declared["accessibility"]
                    or [item.get("path") for item in record.get("deliveries", [])] != [declared["source"]["path"]]
                    or record.get("preview", {}).get("sha256") != declared["source"]["sha256"]):
                raise ValueError(f"{source.name}: expression metadata differs from governed custom asset {declared['id']}")
    seen: set[str] = set()

    def add_url(record: dict[str, Any], count: bool = True) -> None:
        relative = record.get("path")
        if not isinstance(relative, str) or not re.fullmatch(r"[A-Za-z0-9._@/-]+", relative) or ".." in relative.split("/"):
            raise ValueError(f"{source.name}: unsafe portal delivery path: {relative}")
        path = source / relative
        if not path.is_file():
            raise ValueError(f"{source.name}: portal delivery is missing: {relative}")
        digest = record.get("sha256")
        if digest and digest != hashlib.sha256(path.read_bytes()).hexdigest():
            raise ValueError(f"{source.name}: portal delivery hash mismatch: {relative}")
        if count:
            if relative in seen:
                raise ValueError(f"{source.name}: duplicate portal delivery: {relative}")
            seen.add(relative)
        record["url"] = f"/{source.name}/downloads/files/{relative}"

    for family in projected.get("asset_families", []):
        for item in family.get("assets", []):
            for delivery in item.get("deliveries", []):
                add_url(delivery)
            add_url(item["preview"], count=False)
    for resource in projected.get("resources", []):
        add_url(resource)
    for instruction in projected.get("instructions", []):
        instruction["blocks"] = markdown_blocks(instruction.pop("markdown"))
        matching = next((resource for resource in projected.get("resources", []) if resource["path"] == instruction["source_path"]), None)
        if matching is None:
            raise ValueError(f"{source.name}: instruction source is not a resource")
        instruction["source_url"] = matching["url"]
    projected["portable_guide"] = f"/{source.name}/downloads/files/{source.name}-portable-guidelines.html"
    return projected


def generate_social_previews(routes: list[dict[str, Any]], public: Path, mark_path: Path,
                             display_font_path: Path, body_font_path: Path,
                             kits_root: Path = DIST) -> None:
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
        if route["kind"] == "guidelines":
            slug = route["brandSlug"]
            source = kits_root / slug / "logos" / "png" / f"{slug}-social-image-1280.png"
            if not source.is_file():
                raise ValueError(f"verified kit social image is missing: {source}")
            with Image.open(source) as image:
                if image.size != SOCIAL_SIZE:
                    raise ValueError(f"kit social image has wrong dimensions: {source}")
            if source.stat().st_size >= 1000000:
                raise ValueError(f"kit social image exceeds 1 MB: {source}")
            shutil.copyfile(source, destination)
            if hashlib.sha256(destination.read_bytes()).digest() != hashlib.sha256(source.read_bytes()).digest():
                raise ValueError(f"site social image bytes differ from kit: {slug}")
            continue
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
        footer = "brand.shruggie.tech"
        if route.get("vendorBoundary"):
            footer = f"Independent third-party project. Vendor notice: brand.shruggie.tech/{route['brandSlug']}/guidelines/"
        draw.text((120, 530), footer, font=footer_font, fill=(154, 154, 154, 255))
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
    boundary_tags = ""
    if route.get("vendorBoundary"):
        boundary_tags = (
            f'<meta name="brand-vendor-boundary" content="{escape(route["vendorBoundary"], quote=True)}">'
            f'<link rel="help" href="{route["vendorBoundaryUrl"]}" title="Vendor and trademark notice">'
        )
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
        f'{boundary_tags}<script type="application/ld+json">{json_ld}</script>'
    )
    content = path.read_text(encoding="utf-8")
    if "<head>" not in content:
        raise ValueError(f"guideline page lacks a head element: {path}")
    content, title_count = re.subn(r"<title>.*?</title>", f"<title>{escape(title)}</title>", content, count=1, flags=re.DOTALL)
    if title_count != 1:
        raise ValueError(f"guideline page lacks exactly one title element: {path}")
    slug = route.get("brandSlug")
    if not slug:
        raise ValueError("guideline publication route lacks a brand slug")

    def rewrite_asset(match: re.Match[str]) -> str:
        href = match.group(1)
        if (not href.startswith("../") or "\\" in href or "?" in href or "#" in href
                or ".." in href[3:].split("/") or not re.fullmatch(r"(?:logos|icons|favicons|specimens)/[A-Za-z0-9._@/-]+", href[3:])):
            raise ValueError(f"unsafe guideline asset link: {href}")
        relative = href[3:]
        target = path.parents[1] / "downloads" / "files" / Path(relative)
        if not target.is_file():
            raise ValueError(f"guideline asset link target is missing: {relative}")
        return f'<a data-kit-asset href="/{slug}/downloads/files/{relative}"'

    content = re.sub(r'<a data-kit-asset href="([^"]+)"', rewrite_asset, content)
    placeholder = '<span data-host-exit></span>'
    if content.count(placeholder) != 1:
        raise ValueError("guideline host exit placeholder must occur exactly once")
    content = content.replace(placeholder, '<span data-host-exit><a class="host-exit" href="/">All brands</a></span>')
    write_utf8(path, content.replace("<head>", "<head>" + tags, 1))


def contrast_foreground(color: str) -> str:
    """Return the higher-contrast black or white foreground for a hex surface."""
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    luminance = 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    white_contrast = 1.05 / (luminance + 0.05)
    black_contrast = (luminance + 0.05) / 0.05
    return "#FFFFFF" if white_contrast >= black_contrast else "#000000"


def authoritative_canon(root: Path = ROOT) -> str:
    canon = json.loads((root / "skill" / "references" / "01-canon.json").read_text(encoding="utf-8"))
    version = canon.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("authoritative canon lacks a version")
    return version


def publication_record(sources: list[Path], release_slugs: Optional[Set[str]] = None) -> dict[str, Any]:
    if release_slugs is not None:
        by_slug = {source.name: source for source in sources}
        missing = sorted(release_slugs - set(by_slug))
        if missing:
            raise ValueError(f"publication record lacks release kits: {missing}")
        sources = [by_slug[slug] for slug in sorted(release_slugs)]
    bundles = [json.loads((source / "enforcement" / "bundle.json").read_text(encoding="utf-8")) for source in sources]
    if not bundles:
        raise ValueError("publication record requires at least one production kit")
    versions = {bundle["publication"]["version"] for bundle in bundles}
    tags = {bundle["publication"]["tag"] for bundle in bundles}
    statuses = {bundle["publication"]["status"] for bundle in bundles}
    revisions = {bundle["source_revision"] for bundle in bundles}
    if any(len(values) != 1 for values in (versions, tags, statuses, revisions)):
        raise ValueError("production kit bundle publication facts disagree")
    version = versions.pop()
    tag = tags.pop()
    status = statuses.pop()
    revision = revisions.pop()
    return {
        "schemaVersion": 1,
        "status": status,
        "version": version,
        "tag": tag,
        "sourceRevision": revision,
        "releaseUrl": f"https://github.com/ShruggieTech/shruggie-brand/releases/tag/{tag}",
        "skillFilename": f"shruggie-brandbuilder-{version}.skill",
        "skillUrl": f"https://github.com/ShruggieTech/shruggie-brand/releases/download/{tag}/shruggie-brandbuilder-{version}.skill",
        "packages": [bundle["package"] for bundle in bundles],
    }


def copy_kit(source: Path, brand: dict) -> dict:
    slug = brand["slug"]
    portfolio_surface = (brand.get("surfaces") or {}).get("card")
    if not isinstance(portfolio_surface, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", portfolio_surface):
        raise ValueError(f"{slug}: portfolio card requires a valid dark card surface")
    if contrast_foreground(portfolio_surface) != "#FFFFFF":
        raise ValueError(f"{slug}: portfolio card surface must support accessible white text")
    if not (source / "logos" / "svg" / f"{slug}-mark-reduced-color.svg").is_file():
        raise ValueError(f"{slug}: verified reduced-color mark is missing")
    validate_registry(source, brand)
    governed = custom_assets(brand, source, public_only=True)
    guide = source / "brand-guide.pdf"
    if not guide.is_file():
        raise ValueError(f"{slug}: verified public brand guide is missing")
    target = PUBLIC / slug
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    replace_tree(source / "nextjs" / "registry", target / "brand" / "r")
    source_registry = source / "nextjs" / "registry"
    hosted_registry = target / "brand" / "r"
    source_bytes = {path.name: path.read_bytes() for path in source_registry.glob("*.json")}
    hosted_bytes = {path.name: path.read_bytes() for path in hosted_registry.glob("*.json")}
    if source_bytes != hosted_bytes:
        raise ValueError(f"{slug}: hosted registry differs from the verified kit")
    downloads = target / "downloads" / "files"
    downloads.mkdir(parents=True)
    shutil.copy2(guide, downloads / f"{slug}-brand-guide.pdf")
    portable_guide = source / "guidelines" / "index.html"
    portal_payload_path = source / "guidelines" / "portal.json"
    if not portable_guide.is_file() or not portal_payload_path.is_file():
        raise ValueError(f"{slug}: verified guideline portal output is missing")
    portal = json.loads(portal_payload_path.read_text(encoding="utf-8"))
    guide_mode = guide_surface_mode(brand)
    if (portal.get("brand") or {}).get("surface_mode") != guide_mode:
        raise ValueError(f"{slug}: guideline portal presentation disagrees with source")
    shutil.copy2(portable_guide, downloads / f"{slug}-portable-guidelines.html")
    for name in ("logos", "favicons", "icons"):
        replace_tree(source / name, downloads / name)
    for item in governed:
        relative = Path(item["source"]["path"])
        destination = downloads / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, destination)
        if hashlib.sha256(destination.read_bytes()).hexdigest() != item["source"]["sha256"]:
            raise ValueError(f"{slug}: hosted custom asset bytes differ: {item['id']}")
    specimen_name = copy_verified_specimens(source / "specimens", downloads / "specimens")
    handoff = source / "consumer-handoff.json"
    if handoff.is_file():
        shutil.copy2(handoff, downloads / handoff.name)
    bundle = json.loads((source / "enforcement" / "bundle.json").read_text(encoding="utf-8"))
    archive_filename = package_identity(slug, brand["version"], bundle["versions"]["compiler_version"])["filename"]
    if bundle.get("package", {}).get("filename") != archive_filename:
        raise ValueError(f"{slug}: bundle package filename disagrees")
    archive_path = target / "downloads" / archive_filename
    write_brand_archive(
        source,
        archive_path,
        root=ROOT,
        expected_canon=authoritative_canon(),
    )
    logo_root = f"/{slug}/downloads/files/logos/svg"
    aff = affiliation(brand)
    boundary = vendor_boundary(brand)
    record = {
        "slug": slug,
        "title": brand["title"],
        "kind": brand.get("kind", "sub-brand"),
        "descriptor": brand["descriptor"],
        "idea": brand["brand_idea"],
        "socialSlogan": social_copy(brand)["slogan"],
        "version": brand["version"],
        "accent": brand["accent"]["bright"],
        "accentAccessible": brand["accent"]["accessible"],
        "logo": f"{logo_root}/{slug}-horizontal-color.svg",
        "icon": f"{logo_root}/{slug}-mark-reduced-color.svg",
        "specimen": f"/{slug}/downloads/files/specimens/{specimen_name}",
        "portableGuide": f"/{slug}/downloads/files/{slug}-portable-guidelines.html",
        "guidelinesPath": f"/{slug}/guidelines/",
        "kitArchive": f"/{slug}/downloads/{archive_filename}",
        "kitArchiveFilename": archive_filename,
        "packageId": bundle["package"]["id"],
        "brandbuilderVersion": bundle["versions"]["compiler_version"],
        "migration": json.loads((source / "enforcement" / "release-impact.json").read_text(encoding="utf-8")),
        "ownership": aff["ownership"],
        "showcase": aff["showcase"],
        "inheritance": aff["inheritance"],
        "parent": aff["parent"],
        "endorsement": aff["endorsement"],
        "serviceCredit": aff["service_credit"],
        "vendorBoundary": boundary["notice"] if boundary else None,
        "guideSurfaceMode": guide_mode,
    }
    record["portfolioSurface"] = portfolio_surface.upper()
    surface = showcase_surface(brand)
    if surface is not None:
        record["showcaseSurface"] = surface
        record["showcaseForeground"] = contrast_foreground(surface)
        showcase_mode = "light" if brand["showcase_surface"].startswith("light.") else "dark"
        record["showcaseMode"] = showcase_mode
        tokens = (portal.get("presentations") or {}).get(showcase_mode) or {}
        required = ("foreground", "muted-foreground", "secondary", "border", "ring",
                    "brand-cta", "brand-cta-foreground")
        if any(not re.fullmatch(r"#[0-9A-Fa-f]{6}", tokens.get(key, "")) for key in required):
            raise ValueError(f"{slug}: showcase palette lacks valid {showcase_mode} semantic tokens")
        record["showcaseTokens"] = {key: tokens[key].upper() for key in required}
    return record


def write_docs(references: Path, output: Path, descriptions: dict[str, str] = DOC_DESCRIPTIONS,
               navigation: dict[str, tuple[str, int, str, int]] = DOC_NAVIGATION,
               publication: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    records = []
    pages = ["index"]
    expected_sources = ([page["source"] for page in DOCUMENTATION_CATALOG]
                        if descriptions is DOC_DESCRIPTIONS and navigation is DOC_NAVIGATION
                        else [path.name for path in sorted(references.glob("*.md"))])
    actual_sources = {path.name for path in references.glob("*.md")}
    if set(expected_sources) != actual_sources:
        raise ValueError(f"documentation source inventory differs: missing {sorted(set(expected_sources) - actual_sources)}, unexpected {sorted(actual_sources - set(expected_sources))}")
    release_version = (publication or {}).get("version") or json.loads((REFERENCES / "release-impact.json").read_text(encoding="utf-8"))["brandbuilder_version"]
    publication = publication or {
        "version": release_version,
        "status": "candidate",
        "skillUrl": f"https://github.com/ShruggieTech/shruggie-brand/releases/download/v{release_version}/shruggie-brandbuilder-{release_version}.skill",
        "releaseUrl": f"https://github.com/ShruggieTech/shruggie-brand/releases/tag/v{release_version}",
    }
    for pagination_order, source_name in enumerate(expected_sources, 1):
        path = references / source_name
        title, _ = derive_public_markdown(path.read_text(encoding="utf-8"))
        description = descriptions.get(path.stem, f"ShruggieTech guidance for {title.lower()}.")
        write_utf8(output / f"{path.stem}.mdx", render_page(path.read_text(encoding="utf-8"), description, publication))
        if path.stem not in navigation:
            raise ValueError(f"documentation page lacks a navigation assignment: {path.stem}")
        section, section_order, label, order = navigation[path.stem]
        records.append({"slug": path.stem, "title": title, "description": description, "navigation": {"section": section, "sectionOrder": section_order, "label": label, "order": order, "path": f"/docs/{path.stem}/", "paginationOrder": pagination_order}})
        pages.append(path.stem)
    write_utf8(output / "index.mdx", render_index(publication))
    write_utf8(output / "meta.json", json.dumps({"title": "Documentation", "pages": pages}, indent=2) + "\n")
    overview = {"slug": "index", "title": "Documentation", "description": OVERVIEW_DESCRIPTION, "navigation": {"section": "Overview", "sectionOrder": 0, "label": "Overview", "order": 0, "path": "/docs/", "paginationOrder": 0}}
    navigation_records = sorted([overview, *records], key=lambda record: (record["navigation"]["sectionOrder"], record["navigation"]["order"]))
    identities = [(record["navigation"]["sectionOrder"], record["navigation"]["order"]) for record in navigation_records]
    if len(identities) != len(set(identities)):
        raise ValueError("documentation navigation contains duplicate positions")
    write_utf8(output.parent / "documentation.json", json.dumps(navigation_records, ensure_ascii=False, indent=2) + "\n")
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
        public / "maskable-icon-192x192.png": web / "maskable-icon-192x192.png",
        public / "maskable-icon-512x512.png": web / "maskable-icon-512x512.png",
        public / "shruggietech-logo.svg": source / "logos" / "svg" / "shruggietech-horizontal-color.svg",
        public / "shruggietech-logo-dark.svg": source / "logos" / "svg" / "shruggietech-horizontal-color.svg",
        public / "shruggietech-logo-light.svg": source / "logos" / "svg" / "shruggietech-horizontal-light.svg",
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


def stage_web_adapters(sources: list[Path], generated: Path = GENERATED) -> None:
    """Copy verified generated TSX into the ignored site tree for compiler smoke checks."""
    target = generated / "adapters"
    if target.exists():
        shutil.rmtree(target)
    for source in sources:
        adapter = json.loads((source / "web" / "adapter.json").read_text(encoding="utf-8"))
        slug = adapter["brand"]
        if slug != source.name or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
            raise ValueError(f"{source.name}: Web adapter brand must match its source directory")
        destination = target / slug
        destination.mkdir(parents=True, exist_ok=True)
        for name in ("server.tsx", "client.tsx", "environment.tsx", "index.ts"):
            shutil.copy2(source / "web" / "react" / name, destination / name)
        write_utf8(destination / "next-smoke.tsx", 'import { AppFrame, Button } from "./server";\nimport { Tabs } from "./client";\nexport const NextSmoke = () => <AppFrame><Button>OK</Button><Tabs label="Smoke" defaultValue="one" items={[{ value: "one", label: "One", content: "One" }]} /></AppFrame>;\n')
        write_utf8(destination / "vite-smoke.tsx", 'import { Card } from "./server";\nimport { Dialog } from "./client";\nexport const ViteSmoke = () => <Card heading="Smoke"><Dialog triggerLabel="Open" title="Title" description="Description">Body</Dialog></Card>;\n')


def stage_conformance(sources: list[Path], generated: Path = GENERATED, public: Path = PUBLIC) -> list[dict[str, Any]]:
    """Stage verified generated conformance data without reauthoring brand values."""
    public_target = public / "conformance-fixtures"
    for target, boundary in ((public_target, public),):
        resolved = target.resolve()
        try:
            resolved.relative_to(boundary.resolve())
        except ValueError as error:
            raise ValueError(f"refusing to replace conformance path outside boundary: {resolved}") from error
        if target.exists():
            shutil.rmtree(target)
    records = []
    for source in sources:
        problems = verify_conformance(source)
        if problems:
            raise ValueError(f"{source.name}: invalid conformance output: {problems[0]}")
        manifest = json.loads((source / "conformance" / "manifest.json").read_text(encoding="utf-8"))
        if manifest.get("brand") != source.name:
            raise ValueError(f"{source.name}: conformance brand must match its source directory")
        destination = public_target / source.name
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / "conformance" / "browser" / "specimen.html", destination / "specimen.html")
        shutil.copy2(source / "conformance" / "manifest.json", destination / "manifest.json")
        records.append({
            "slug": source.name,
            "title": manifest["brand_title"],
            "brandVersion": manifest["brand_version"],
            "sourceRevision": manifest["source_revision"],
            "contractVersion": manifest["conformance_contract_version"],
            "versions": manifest["versions"],
            "recipes": manifest["recipes"],
            "profiles": manifest["profiles"],
            "hostTracks": manifest["host_tracks"],
            "diagnosticClasses": manifest["diagnostic_classes"],
            "evidenceBoundaries": manifest["evidence_boundaries"],
            "specimenPath": f"/conformance-fixtures/{source.name}/specimen.html",
            "manifestPath": f"/conformance-fixtures/{source.name}/manifest.json",
        })
    generated.mkdir(parents=True, exist_ok=True)
    write_utf8(generated / "conformance.json", json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    return records


def main() -> int:
    if not DIST.is_dir():
        raise SystemExit("dist/ is missing; run python scripts/build_all.py first")
    PUBLIC.mkdir(parents=True, exist_ok=True)
    GENERATED.mkdir(parents=True, exist_ok=True)
    brands = []
    portals = []
    seen: set[str] = set()
    sources = source_dirs()
    stage_web_adapters(sources)
    loaded = []
    for source in sources:
        brand = load_brand(source)
        validate_source_identity(source, brand, seen)
        loaded.append((source, brand))
    public_sources = [(source, brand) for source, brand in loaded if public_showcase(brand, source)]
    for source, brand in public_sources:
        validate_registry(source, brand)
    stage_conformance([source for source, _ in public_sources])
    remove_stale_public_brands(PUBLIC, {source.name for source, _ in public_sources})
    for source, brand in public_sources:
        brands.append(copy_kit(source, brand))
        payload = json.loads((source / "guidelines" / "portal.json").read_text(encoding="utf-8"))
        portals.append(project_portal(source, payload))
    parent = DIST / "shruggietech"
    parent_css = "\n".join((parent / "tokens" / name).read_text(encoding="utf-8") for name in ("colors.css", "spacing.css", "typography.css", "base.css"))
    write_utf8(GENERATED / "parent.css", parent_css)
    write_utf8(GENERATED / "registry-theme.css", install_registry_theme(parent))
    generated_fonts = GENERATED / "fonts"
    if generated_fonts.exists():
        shutil.rmtree(generated_fonts)
    shutil.copytree(ROOT / "assets" / "fonts" / "woff2", generated_fonts)
    write_utf8(GENERATED / "brands.json", json.dumps(brands, indent=2) + "\n")
    publication = publication_record([source for source, _ in public_sources], set(PRODUCTION))
    write_utf8(GENERATED / "publication.json", json.dumps(publication, indent=2) + "\n")
    write_utf8(GENERATED / "guidelines.json", json.dumps(portals, ensure_ascii=False, indent=2) + "\n")
    docs = write_docs(REFERENCES, GENERATED / "docs", publication=publication)
    docs_publication = documentation_publication_record(REFERENCES, GENERATED / "docs", publication)
    docs_publication_bytes = json.dumps(docs_publication, indent=2) + "\n"
    write_utf8(GENERATED / "documentation-publication.json", docs_publication_bytes)
    (PUBLIC / "docs").mkdir(parents=True, exist_ok=True)
    write_utf8(PUBLIC / "docs" / "publication.json", docs_publication_bytes)
    routes = build_routes(brands, docs, portals)
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
