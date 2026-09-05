#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Explicitly ingest one licensed fixed font after hash and metadata checks."""

from __future__ import annotations

import argparse
import os
import shutil
import ssl
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

from brand_contract import ContractError, _font_metadata, contained_path, sha256_file


ROOT = Path(__file__).resolve().parents[2]
MAX_BYTES = 32 * 1024 * 1024


class HTTPSOnlyRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        if urllib.parse.urlparse(new_url).scheme.lower() != "https":
            raise ContractError("font ingestion refused a redirect outside HTTPS")
        return super().redirect_request(request, fp, code, message, headers, new_url)


def _copy_limited(source, destination, limit=MAX_BYTES):
    total = 0
    while True:
        chunk = source.read(1024 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > limit:
            raise ContractError("font source exceeds the %d-byte ingestion limit" % limit)
        destination.write(chunk)
    if total == 0:
        raise ContractError("font source is empty")


def _read_source(source, destination):
    local = Path(source).resolve()
    if local.is_file():
        with local.open("rb") as incoming, destination.open("wb") as outgoing:
            _copy_limited(incoming, outgoing)
        return
    parsed = urllib.parse.urlparse(source)
    if parsed.scheme:
        if parsed.scheme.lower() != "https":
            raise ContractError("remote font sources must use HTTPS")
        opener = urllib.request.build_opener(HTTPSOnlyRedirect, urllib.request.HTTPSHandler(context=ssl.create_default_context()))
        request = urllib.request.Request(source, headers={"User-Agent": "shruggie-brand-font-ingestion/1"})
        with opener.open(request, timeout=30) as response:
            if urllib.parse.urlparse(response.geturl()).scheme.lower() != "https":
                raise ContractError("font response left HTTPS")
            declared = response.headers.get("Content-Length")
            if declared is not None and int(declared) > MAX_BYTES:
                raise ContractError("font response exceeds the ingestion limit")
            with destination.open("wb") as handle:
                _copy_limited(response, handle)
        return
    raise ContractError("local font source is missing: %s" % source)


def ingest_font(source, destination, expected_sha256, family, weight, style, license_name, provenance, repo_root=ROOT):
    if not license_name or not license_name.strip():
        raise ContractError("font ingestion requires reviewed license evidence")
    if not provenance or not provenance.strip():
        raise ContractError("font ingestion requires public-safe provenance")
    if style not in {"normal", "italic", "oblique"}:
        raise ContractError("font ingestion style must be normal, italic, or oblique")
    if len(expected_sha256) != 64 or any(character not in "0123456789abcdef" for character in expected_sha256):
        raise ContractError("font ingestion requires a lowercase SHA-256")
    root = Path(repo_root).resolve()
    target = contained_path(root, destination, required=False, boundary="assets/fonts")
    if target.suffix.lower() not in {".ttf", ".otf", ".woff2"}:
        raise ContractError("font destination must end in .ttf, .otf, or .woff2")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix=".shruggie-font-", suffix=target.suffix, dir=str(target.parent), delete=False) as handle:
            temporary = Path(handle.name)
        _read_source(source, temporary)
        if sha256_file(temporary) != expected_sha256:
            raise ContractError("font source SHA-256 does not match the approved digest")
        measured = _font_metadata(temporary)
        expected_format = target.suffix.lower().lstrip(".")
        checks = {"family": family, "weight": int(weight), "style": style, "format": expected_format}
        for field, expected in checks.items():
            if measured[field] != expected:
                raise ContractError("font %s mismatch: expected %r, measured %r" % (field, expected, measured[field]))
        os.replace(str(temporary), str(target))
        temporary = None
        return target
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--destination", required=True, help="Repository-relative path under assets/fonts/")
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--weight", required=True, type=int)
    parser.add_argument("--style", required=True, choices=("normal", "italic", "oblique"))
    parser.add_argument("--license", required=True, dest="license_name")
    parser.add_argument("--provenance", required=True)
    args = parser.parse_args()
    try:
        target = ingest_font(args.source, args.destination, args.sha256, args.family, args.weight, args.style, args.license_name, args.provenance)
    except (ContractError, OSError, ValueError) as error:
        parser.error(str(error))
    print("ingested approved font at %s" % target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
