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
REFERENCE_TARGET = re.compile(r"(?m)^ {0,3}\[[^\]]+\]:[ \t]*(?:<([^>]+)>|([^\s]+))")
FENCE = re.compile(r"^ {0,3}(```|~~~)")
VERSIONED_BUILDER_ASSET = re.compile(r"shruggie-brandbuilder-\d+\.\d+\.\d+(?:-portable)?\.(?:skill|zip)")


class _HtmlTargets(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"a", "img", "source"}:
            return
        for name, value in attrs:
            if not value:
                continue
            if name in {"href", "src"}:
                self.targets.append(value)
            elif name == "srcset":
                self.targets.extend(candidate.strip().split()[0] for candidate in value.split(",") if candidate.strip())


def destinations(markdown: str) -> list[str]:
    """Collect inline Markdown and HTML targets outside fenced examples."""
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
    links = [match.group(1) or match.group(2) for pattern in (MARKDOWN_TARGET, REFERENCE_TARGET)
             for match in pattern.finditer(content)]
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
    if not brands:
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
    seen_brands: set[str] = set()
    problems: list[str] = []
    targets = destinations(markdown)
    for target in targets:
        parsed = urlsplit(target)
        host = (parsed.hostname or "").lower()
        if host == "brand.shruggie.tech" or "brand.shruggie.tech" in (parsed.netloc or "").lower():
            if parsed.scheme != "https" or parsed.netloc.lower() != "brand.shruggie.tech":
                problems.append("untrusted site host: " + target)
                continue
            url = SITE_ORIGIN + parsed.path
            if parsed.query or url not in canonical:
                problems.append("undeclared site route: " + target)
            elif url in brands:
                seen_brands.add(url)
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
    if LATEST_RELEASE not in targets:
        problems.append("missing latest official release: " + LATEST_RELEASE)
    if VERSIONED_BUILDER_ASSET.search(markdown):
        problems.append("versioned BrandBuilder asset name in README")
    problems.extend("missing brand overview: " + url for url in sorted(brands - seen_brands))
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
