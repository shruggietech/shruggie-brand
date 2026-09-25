#!/usr/bin/env python3
"""Audit README links against local files and the generated site route contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE_ORIGIN = "https://brand.shruggie.tech"
LATEST_RELEASE = "https://github.com/shruggietech/shruggie-brand/releases/latest"
MARKDOWN_TARGET = re.compile(r"\]\((?:<([^>]+)>|([^\s)]+))")
MARKDOWN_IMAGE = re.compile(r"!\[[^\]]*\]\((?:<[^>]+>|[^\s)]+)\)")
MARKDOWN_AUTOLINK = re.compile(r"<(https?://[^\s<>]+)>")
BARE_URL = re.compile(r"https?://[^\s<>()\[\]\"']+")
HTML_TAG = re.compile(r"<[^>\n]+>")
REFERENCE_TARGET = re.compile(r"(?m)^ {0,3}\[(?P<id>[^\]]+)\]:[ \t]*(?:<(?P<angle>[^>]+)>|(?P<plain>[^\s]+))")
REFERENCE_USE = re.compile(r"(?P<image>!)?\[[^\]]+\]\[(?P<id>[^\]]+)\]")
FENCE = re.compile(r"^ {0,3}(```|~~~)")
VERSIONED_BUILDER_ASSET = re.compile(r"shruggie-brandbuilder-\d+\.\d+\.\d+(?:-portable)?\.(?:skill|zip)")
PORTFOLIO_COUNT = re.compile(r"\b(?:\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten|several|many)\s+(?:(?:production|showcased|subordinate|released|current)\s+)?(?:sub-?brands|brand kits|brands|kits)\b", re.IGNORECASE)
PORTFOLIO_HEADING = re.compile(r"(?im)^#{1,6}\s+(?:brand kits|brands|portfolio)\s*$")
EMPTY_MARKDOWN_IMAGE = re.compile(r"!\[\s*\]\(")
EMPTY_REFERENCE_IMAGE = re.compile(r"!\[\s*\]\[[^\]]+\]")


class _HtmlTargets(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.targets: list[tuple[str, bool]] = []
        self.images_without_alt = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"a", "img", "source"}:
            return
        if tag == "img" and not any(name == "alt" and value and value.strip() for name, value in attrs):
            self.images_without_alt += 1
        for name, value in attrs:
            if not value:
                continue
            if name == "href" and tag == "a":
                self.targets.append((value, True))
            elif name == "src":
                self.targets.append((value, False))
            elif name == "srcset":
                self.targets.extend((candidate.strip().split()[0], False) for candidate in value.split(",") if candidate.strip())


def destinations(markdown: str) -> list[tuple[str, bool]]:
    """Collect destinations and whether each is a navigable link."""
    visible: list[str] = []
    fence: str | None = None
    for line in markdown.splitlines():
        marker = FENCE.match(line)
        if marker:
            kind = marker.group(1)[0]
            if fence is None:
                fence = kind
            elif fence == kind:
                fence = None
            continue
        if fence is None:
            visible.append(line)
    content = "\n".join(visible)
    inline = list(MARKDOWN_TARGET.finditer(content))
    images = list(MARKDOWN_IMAGE.finditer(content))
    references = list(REFERENCE_TARGET.finditer(content))
    navigation_refs = {match.group("id").casefold() for match in REFERENCE_USE.finditer(content)
                       if not match.group("image")}
    links = [(match.group(1) or match.group(2),
              not any(image.start() <= match.start() < image.end() for image in images))
             for match in inline]
    links.extend((match.group("angle") or match.group("plain"), match.group("id").casefold() in navigation_refs)
                 for match in references)
    claimed = [*inline, *references]
    links.extend((match.group(1), True) for match in MARKDOWN_AUTOLINK.finditer(content)
                 if not any(item.start() <= match.start() < item.end() for item in claimed))
    bare_claimed = [*claimed, *HTML_TAG.finditer(content)]
    links.extend((match.group().rstrip(".,;:!"), True) for match in BARE_URL.finditer(content)
                 if not any(item.start() <= match.start() < item.end() for item in bare_claimed))
    html = _HtmlTargets()
    html.feed(content)
    return [*links, *html.targets]


def _site_routes(contract: dict) -> tuple[set[str], set[str]]:
    if contract.get("siteUrl") != SITE_ORIGIN or not isinstance(contract.get("routes"), list):
        raise ValueError("invalid generated site route contract")
    canonical: set[str] = set()
    brands: set[str] = set()
    for route in contract["routes"]:
        if not isinstance(route, dict):
            raise ValueError("invalid generated route record")
        path, url = route.get("pathname"), route.get("canonical")
        if not isinstance(path, str) or not path.startswith("/") or not path.endswith("/") or url != SITE_ORIGIN + path:
            raise ValueError("invalid generated canonical route")
        if url in canonical:
            raise ValueError("duplicate generated canonical route: " + url)
        canonical.add(url)
        if route.get("kind") == "guidelines":
            slug = route.get("brandSlug")
            if not isinstance(slug, str) or path != "/" + slug + "/guidelines/":
                raise ValueError("invalid generated brand overview route")
            brands.add(url)
    if not brands or SITE_ORIGIN + "/" not in canonical:
        raise ValueError("generated site contract has no brand overview routes")
    return canonical, brands


def _local_problem(root: Path, target: str, path: str) -> str | None:
    decoded = unquote(path)
    if (not decoded or decoded.startswith("/") or "\\" in decoded or "\x00" in decoded
            or any(part == ".." for part in decoded.split("/")) or "%" in decoded):
        return "unsafe local target: " + target
    resolved = (root / decoded).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return "unsafe local target: " + target
    if not resolved.exists():
        return "missing local target: " + target
    return None


def audit(root: Path, markdown: str, contract: dict) -> list[str]:
    canonical, brands = _site_routes(contract)
    problems: list[str] = []
    targets = destinations(markdown)
    for target, navigable in targets:
        parsed = urlsplit(target)
        if "%" in parsed.netloc:
            problems.append("unsupported URL scheme or authority: " + target)
            continue
        host = (parsed.hostname or "").lower()
        if host == "brand.shruggie.tech" or "brand.shruggie.tech" in (parsed.netloc or "").lower():
            if parsed.scheme != "https" or parsed.netloc.lower() != "brand.shruggie.tech":
                problems.append("untrusted site host: " + target)
                continue
            url = SITE_ORIGIN + parsed.path
            if parsed.query or url not in canonical:
                problems.append("undeclared site route: " + target)
        elif parsed.scheme:
            if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
                problems.append("unsupported URL scheme or authority: " + target)
        elif parsed.netloc:
            problems.append("unsupported URL scheme or authority: " + target)
        elif not parsed.path and parsed.fragment and not parsed.query:
            continue
        else:
            problem = "unsafe local target: " + target if parsed.query else _local_problem(root, target, parsed.path)
            if problem:
                problems.append(problem)
    if not any(target == LATEST_RELEASE and navigable for target, navigable in targets):
        problems.append("missing latest official release: " + LATEST_RELEASE)
    if not any(target == SITE_ORIGIN + "/" and navigable for target, navigable in targets):
        problems.append("missing brand site: " + SITE_ORIGIN + "/")
    if VERSIONED_BUILDER_ASSET.search(markdown):
        problems.append("versioned BrandBuilder asset name in README")
    if PORTFOLIO_COUNT.search(markdown) or PORTFOLIO_HEADING.search(markdown):
        problems.append("portfolio snapshot in README")
    if any(url in markdown for url in brands):
        problems.append("portfolio snapshot in README: brand route")
    if EMPTY_MARKDOWN_IMAGE.search(markdown) or EMPTY_REFERENCE_IMAGE.search(markdown):
        problems.append("missing image alt in README")
    html = _HtmlTargets()
    html.feed(markdown)
    if html.images_without_alt:
        problems.append("missing image alt in README")
    for url in brands:
        slug = url[len(SITE_ORIGIN) + 1:].split("/", 1)[0]
        if slug == "shruggietech":
            continue
        names = {slug, slug.replace("-", " ")}
        if any(re.search(r"\b" + re.escape(name) + r"\b", markdown, re.IGNORECASE) for name in names):
            problems.append("portfolio snapshot in README: brand slug " + slug)
    return problems


def _contained_file(root: Path, path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("input outside repository root: " + str(path)) from error
    if not resolved.is_file():
        raise ValueError("missing audit input: " + str(path))
    return resolved


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--readme", type=Path)
    parser.add_argument("--routes", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    readme = args.readme or root / "README.md"
    routes = args.routes or root / "site" / "generated" / "routes.json"
    try:
        markdown = _contained_file(root, readme).read_text(encoding="utf-8")
        contract = json.loads(_contained_file(root, routes).read_text(encoding="utf-8"))
        problems = audit(root, markdown, contract)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        print("README link audit: " + str(error), file=sys.stderr)
        return 1
    for problem in problems:
        print(problem, file=sys.stderr)
    print("README link audit: %d problem(s)" % len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
