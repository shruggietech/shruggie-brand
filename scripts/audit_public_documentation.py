#!/usr/bin/env python3
"""Reject internal planning and stale prose in publication-bound guidance."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, Iterator, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
SLICE_CODE = re.compile(r"\bS\d{2,4}\b|\b(?:work[ -]?)?slice\s+(?:S\s*)?\d{2,4}\b", re.IGNORECASE)
PORTFOLIO_COUNT = re.compile(r"\b(?:\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten|several|many)\s+(?:(?:production|existing|current|published|showcased|subordinate)\s+)?(?:sub-?brands|brand kits|brands|kits)\b|\b(?:brand|kit)\s+count\b", re.IGNORECASE)
PROCESS_REFERENCE = re.compile(r"\bSpec[ -]?Kit\b", re.IGNORECASE)
ALLOWED_PROCESS_INSTRUCTION = "Run the repository-installed Spec Kit workflow before changing governed source."
ALLOWED_PROCESS_PATHS = {
    "skill/references/operating-modes.md",
    "site/generated/docs/operating-modes.mdx",
    "site/out/docs/operating-modes/index.html",
}
ISSUE_REFERENCE = re.compile(r"\bIssue\s+#\d+\b|\bspecs/\d{3}[-/]", re.IGNORECASE)
VAGUE = re.compile(r"\b(?:usually|often|generally|might|where possible)\b", re.IGNORECASE)
HISTORICAL = re.compile(
    r"\b(?:Fragcap\s+1\.0\.0|once said|earlier Cue Iris approval|initial S020 snapshot|"
    r"later Cueson repository issue|No production derivative geometry or public registry entry exists while Gate 1 is pending)\b",
    re.IGNORECASE,
)
PROMOTIONAL = re.compile(r"genuinely good at|could say out loud without wincing|Sometimes it renders a PNG and looks", re.IGNORECASE)
SKIP_HTML_TAGS = {"script", "style", "svg"}


class _VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.parts = []  # type: list[str]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag in SKIP_HTML_TAGS:
            self.hidden += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_HTML_TAGS and self.hidden:
            self.hidden -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden:
            self.parts.append(data)


def visible_html_text(content: str) -> str:
    parser = _VisibleText()
    parser.feed(content)
    return " ".join(" ".join(parser.parts).split())


def require_contained(root: Path, path: Path) -> Path:
    base = root.resolve()
    resolved = path.resolve()
    try:
        resolved.relative_to(base)
    except ValueError as exc:
        raise ValueError("outside publication root: %s" % path) from exc
    return resolved


def _read(root: Path, path: Path) -> str:
    safe = require_contained(root, path)
    if not safe.is_file():
        raise ValueError("missing publication input: %s" % path)
    return safe.read_text(encoding="utf-8")


def _label(root: Path, path: Path) -> str:
    return require_contained(root, path).relative_to(root.resolve()).as_posix()


def _brands(root: Path) -> tuple[str, ...]:
    parent = root / "brands"
    return tuple(path.name for path in sorted(parent.iterdir()) if path.is_dir() and (path / "brand.json").is_file())


def source_documents(root: Path, brands: Optional[Iterable[str]] = None) -> Iterator[Tuple[str, str]]:
    catalog = json.loads(_read(root, root / "skill" / "references" / "documentation-contract.json"))
    for page in catalog["manual_pages"]:
        name = page["source"]
        if Path(name).name != name or not name.endswith(".md"):
            raise ValueError("unsafe documentation source: %s" % name)
        path = root / "skill" / "references" / name
        yield _label(root, path), _read(root, path)
        yield "manual-catalog/%s" % page["slug"], " ".join(str(page[key]) for key in ("title", "description", "label", "section"))
    for slug in tuple(brands) if brands is not None else _brands(root):
        if Path(slug).name != slug or slug in {".", ".."}:
            raise ValueError("unsafe brand slug: %s" % slug)
        base = root / "brands" / slug
        brand = json.loads(_read(root, base / "brand.json"))
        if brand.get("slug") != slug:
            raise ValueError("brand scope mismatch: %s" % slug)
        for path in sorted(base.rglob("*.md")):
            if "provenance" in path.relative_to(base).parts:
                continue
            yield _label(root, path), _read(root, path)


def prepared_documents(root: Path, brands: Optional[Iterable[str]] = None) -> Iterator[Tuple[str, str]]:
    selected = tuple(brands) if brands is not None else _brands(root)
    docs = root / "site" / "generated" / "docs"
    if not docs.is_dir():
        raise ValueError("missing prepared manual: %s" % docs)
    catalog = json.loads(_read(root, root / "skill" / "references" / "documentation-contract.json"))
    expected = {"index.mdx"} | {str(page["slug"]) + ".mdx" for page in catalog["manual_pages"]}
    actual = {path.name for path in docs.glob("*.mdx")}
    if actual != expected:
        raise ValueError("prepared manual inventory differs: %s" % sorted(actual ^ expected))
    for path in sorted(docs.glob("*.mdx")):
        yield _label(root, path), _read(root, path)
    for name in ("documentation.json", "routes.json"):
        path = root / "site" / "generated" / name
        data = json.loads(_read(root, path))
        records = data if name == "documentation.json" else data["routes"]
        for record in records:
            if name == "routes.json" and record.get("kind") not in {"docs-index", "docs-page"}:
                continue
            yield _label(root, path) + "/" + str(record.get("slug", record.get("id", "index"))), json.dumps(record, ensure_ascii=False)
    for slug in selected:
        kit = root / "dist" / slug
        brand = json.loads(_read(root, kit / "brand.json"))
        if brand.get("slug") != slug:
            raise ValueError("brand scope mismatch: %s" % slug)
        for path in sorted(kit.rglob("*.md")):
            if "provenance" in path.relative_to(kit).parts:
                continue
            yield _label(root, path), _read(root, path)
        for relative in ("guidelines/index.html", "build/brand-guide.print.html"):
            path = kit / relative
            yield _label(root, path), visible_html_text(_read(root, path))
    exported = root / "site" / "out"
    if not exported.is_dir():
        raise ValueError("missing exported site: %s" % exported)
    exported_docs = exported / "docs"
    expected_routes = {"index.html"} | {str(page["slug"]) + "/index.html" for page in catalog["manual_pages"]}
    actual_routes = {path.relative_to(exported_docs).as_posix() for path in exported_docs.rglob("*.html")}
    if actual_routes != expected_routes:
        raise ValueError("exported manual inventory differs: %s" % sorted(actual_routes ^ expected_routes))
    for path in sorted(exported_docs.rglob("*.html")):
        yield _label(root, path), visible_html_text(_read(root, path))
    for slug in selected:
        guide = exported / slug / "guidelines"
        for path in sorted(guide.rglob("*.html")):
            yield _label(root, path), visible_html_text(_read(root, path))


def scan_text(label: str, text: str) -> list[str]:
    problems = []  # type: list[str]
    process_text = text.replace(ALLOWED_PROCESS_INSTRUCTION, "") if label in ALLOWED_PROCESS_PATHS else text
    for kind, pattern in (
        ("work-slice code", SLICE_CODE),
        ("Spec Kit process reference", PROCESS_REFERENCE),
        ("issue or specification history", ISSUE_REFERENCE),
        ("historical narrative", HISTORICAL),
        ("vague wording", VAGUE),
        ("vague promotional wording", PROMOTIONAL),
    ):
        match = pattern.search(process_text if kind == "Spec Kit process reference" else text)
        if match:
            problems.append("%s: %s: %s" % (label, kind, match.group(0)))
    if (label.startswith(("skill/references/", "manual-catalog/", "site/generated/docs/", "site/generated/documentation.json", "site/generated/routes.json", "site/out/docs/"))
            or label == "manual.md"):
        match = PORTFOLIO_COUNT.search(text)
        if match:
            problems.append("%s: portfolio count: %s" % (label, match.group(0)))
    return problems


def audit(root: Path, sources: bool, prepared: bool) -> list[str]:
    brands = _brands(root)
    if not brands:
        raise ValueError("no production brands discovered")
    problems = []  # type: list[str]
    for label, content in source_documents(root, brands) if sources else ():
        problems.extend(scan_text(label, content))
    for label, content in prepared_documents(root, brands) if prepared else ():
        problems.extend(scan_text(label, content))
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", action="store_true", help="Audit publication-bound source guidance")
    parser.add_argument("--prepared", action="store_true", help="Audit generated kits and exported site")
    args = parser.parse_args()
    if not (args.sources or args.prepared):
        parser.error("select --sources or --prepared")
    try:
        problems = audit(ROOT, args.sources, args.prepared)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("public documentation audit: %s" % exc, file=sys.stderr)
        return 1
    for problem in problems:
        print(problem, file=sys.stderr)
    print("public documentation audit: %d problem(s)" % len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
