#!/usr/bin/env python3
"""Bind the generated main manual to exact packaged skill reference bytes."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any, Mapping, Optional

from documentation_render import render_index, render_page


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_record(references: Path, docs: Path, publication: Mapping[str, Any]) -> dict[str, Any]:
    catalog_path = references / "documentation-contract.json"
    catalog_bytes = catalog_path.read_bytes()
    catalog = json.loads(catalog_bytes)
    pages = catalog["manual_pages"]
    sources = [page["source"] for page in pages]
    slugs = [page["slug"] for page in pages]
    if len(sources) != len(set(sources)) or len(slugs) != len(set(slugs)):
        raise ValueError("duplicate documentation catalog entry")
    if any(re.fullmatch(r"[a-z0-9][a-z0-9-]*\.md", name) is None for name in sources):
        raise ValueError("unsafe documentation source")
    if any(re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug) is None or slug == "index" for slug in slugs):
        raise ValueError("unsafe documentation slug")
    expected_pages = {"index.mdx"} | {slug + ".mdx" for slug in slugs}
    if {path.name for path in docs.glob("*.mdx")} != expected_pages:
        raise ValueError("prepared documentation inventory differs")
    if {path.name for path in references.glob("*.md")} != set(sources):
        raise ValueError("source documentation inventory differs")
    if (docs / "index.mdx").read_bytes() != render_index(publication).encode("utf-8"):
        raise ValueError("prepared documentation overview differs from deterministic source transform")
    for page in pages:
        expected = render_page((references / page["source"]).read_text(encoding="utf-8"),
                               page["description"], publication).encode("utf-8")
        if (docs / (page["slug"] + ".mdx")).read_bytes() != expected:
            raise ValueError("prepared documentation page differs from deterministic source transform: %s" % page["slug"])
    return {
        "schemaVersion": 1,
        **{name: publication[name] for name in ("status", "version", "tag", "sourceRevision", "releaseUrl", "skillUrl")},
        "catalogSha256": _sha(catalog_bytes),
        "references": [{"source": name, "sha256": _sha((references / name).read_bytes())} for name in sources],
        "pages": [{"slug": slug, "path": "/docs/" if slug == "index" else "/docs/%s/" % slug,
                   "sha256": _sha((docs / (slug + ".mdx")).read_bytes())} for slug in ["index", *slugs]],
    }


def verify_record(record_path: Path, references: Path, docs: Path, publication: Mapping[str, Any],
                  *, exported_record: Optional[Path] = None, release_dir: Optional[Path] = None,
                  require_release: bool = False) -> dict[str, Any]:
    raw = record_path.read_bytes()
    record = json.loads(raw)
    if record != build_record(references, docs, publication):
        raise ValueError("documentation publication record disagrees with exact source, page, or release identity")
    if require_release and record["status"] != "release":
        raise ValueError("documentation publication requires exact release status")
    if exported_record is not None and exported_record.read_bytes() != raw:
        raise ValueError("exported documentation publication record disagrees")
    if release_dir is not None:
        version = record["version"]
        for filename in ("shruggie-brandbuilder-%s.skill" % version,
                         "shruggie-brandbuilder-%s-portable.zip" % version):
            with zipfile.ZipFile(str(release_dir / filename)) as archive:
                if archive.read("SOURCE_REVISION").decode("utf-8").strip() != record["sourceRevision"]:
                    raise ValueError("packaged documentation source revision disagrees")
                if archive.read("references/documentation-contract.json") != (references / "documentation-contract.json").read_bytes():
                    raise ValueError("packaged documentation catalog differs")
                for entry in record["references"]:
                    if archive.read("references/" + entry["source"]) != (references / entry["source"]).read_bytes():
                        raise ValueError("packaged documentation reference differs: %s" % entry["source"])
    return record
