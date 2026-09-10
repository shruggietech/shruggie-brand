#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atomically promote exact approved identity source bytes into a brand root."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path

from identity_continuity import (
    DIGEST,
    canonical_source_binding,
    canonical_digest,
    load_json,
    record_digest,
    safe_path,
    validate_record,
)


class PromotionError(ValueError):
    """Raised when promotion cannot preserve the approved source contract."""


def _require(condition, message):
    if not condition:
        raise PromotionError(message)


def _contained_bundle(bundle_path, approval_root):
    root = Path(approval_root).resolve()
    path = Path(bundle_path)
    try:
        relative = path.resolve().relative_to(root).as_posix()
    except ValueError as error:
        raise PromotionError("approval bundle escapes the approved root") from error
    try:
        return safe_path(root, relative)
    except ValueError as error:
        raise PromotionError(str(error)) from error


def _validate_bundle(bundle, approval_root):
    required = {"schema_version", "source_root", "record_path", "record_file_sha256", "record_sha256"}
    _require(isinstance(bundle, dict) and set(bundle) == required,
             "promotion bundle has unsupported or missing fields")
    _require(bundle["schema_version"] == 1, "promotion bundle schema_version must be 1")
    _require(isinstance(bundle["record_sha256"], str) and DIGEST.fullmatch(bundle["record_sha256"] or "") and
             bundle["record_sha256"] == record_digest(bundle), "promotion bundle digest is invalid or stale")
    try:
        source_root = safe_path(approval_root, bundle["source_root"], required=False)
    except ValueError as error:
        raise PromotionError(str(error)) from error
    _require(source_root.is_dir(), "promotion source root is missing")
    try:
        record_path = safe_path(source_root, bundle["record_path"])
    except ValueError as error:
        raise PromotionError(str(error)) from error
    _require(bundle["record_path"] == "identity-continuity.json",
             "promotion continuity record must install as identity-continuity.json")
    _require(DIGEST.fullmatch(bundle["record_file_sha256"] or "") and
             canonical_digest(record_path.read_bytes()) == bundle["record_file_sha256"],
             "promotion continuity record hash drift")
    record = load_json(record_path)
    _require(record.get("status") == "approved-canonical", "promotion requires approved-canonical continuity")
    brand_record = next((item for item in record.get("source_files", []) if item.get("path") == "brand.json"), None)
    _require(brand_record is not None, "approved continuity record must govern brand.json")
    brand = load_json(safe_path(source_root, "brand.json"))
    validate_record(brand, source_root, record, verify_proof_files=True)
    gate_binding = (((brand.get("approval_ledger") or {}).get("gate_1") or {}).get("canonical_source_sha256"))
    _require(gate_binding == canonical_source_binding(record),
             "Gate 1 canonical source binding is absent or stale")
    _require(brand.get("identity_continuity") == {"record": "identity-continuity.json", "status": "approved-canonical"},
             "promoted brand.json must reference its approved continuity record")
    records = list(record["source_files"])
    seen = set()
    resolved = []
    for item in records:
        relative = item["path"]
        _require(relative not in seen, "duplicate promotion destination: %s" % relative)
        seen.add(relative)
        first = Path(relative).parts[0] if Path(relative).parts else ""
        _require(first not in {"proofs", "dist", "qc", "release", "site"},
                 "generated or external path cannot be promoted: %s" % relative)
        _require(Path(relative).suffix.lower() not in {".exe", ".dll", ".com", ".bat", ".cmd", ".ps1", ".msi"},
                 "executable source cannot be promoted: %s" % relative)
        try:
            source = safe_path(source_root, relative)
        except ValueError as error:
            raise PromotionError(str(error)) from error
        _require(isinstance(item["bytes"], int) and source.stat().st_size == item["bytes"],
                 "promotion source byte count drift: %s" % relative)
        _require(isinstance(item["sha256"], str) and DIGEST.fullmatch(item["sha256"] or "") and
                 canonical_digest(source.read_bytes()) == item["sha256"],
                 "promotion source hash drift: %s" % relative)
        resolved.append((relative, source, item["sha256"]))
    _require("brand.json" in seen, "promotion source must include brand.json")
    resolved.append(("identity-continuity.json", record_path, bundle["record_file_sha256"]))
    declared = seen | {"identity-continuity.json"}
    actual = set()
    for path in source_root.rglob("*"):
        relative = path.relative_to(source_root).as_posix()
        if relative == "proofs" or relative.startswith("proofs/"):
            continue
        _require(not path.is_symlink(), "symbolic-link source is not permitted: %s" % relative)
        if path.is_file():
            actual.add(relative)
    _require(actual == declared,
             "promotion source contains undeclared files: %s" % ", ".join(sorted(actual - declared)))
    return record["brand"], resolved


def promote(bundle_path, approval_root, brands_root, replace=False):
    """Copy declared approved files into brands/<slug> without transformation."""
    approval_root = Path(approval_root).resolve()
    brands_root = Path(brands_root).resolve()
    _require(approval_root.is_dir(), "approval root is missing")
    _require(brands_root.is_dir() and not brands_root.is_symlink(), "brands root is missing or unsafe")
    path = _contained_bundle(bundle_path, approval_root)
    try:
        bundle = load_json(path)
        brand_slug, records = _validate_bundle(bundle, approval_root)
    except ValueError as error:
        if isinstance(error, PromotionError):
            raise
        raise PromotionError(str(error)) from error

    destination = brands_root / brand_slug
    _require(destination.parent.resolve() == brands_root, "promotion destination escapes brands root")
    _require(not destination.exists() or replace, "promotion destination already exists")
    stage = Path(tempfile.mkdtemp(prefix=".identity-stage-", dir=str(brands_root)))
    backup = brands_root / (".identity-backup-" + brand_slug)
    installed = False
    backed_up = False
    try:
        for relative, source, digest in records:
            target = stage / Path(relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(source), str(target))
            _require(canonical_digest(target.read_bytes()) == digest, "staged source hash drift: %s" % relative)
        if destination.exists():
            _require(not destination.is_symlink(), "existing destination cannot be a symlink")
            _require(not backup.exists(), "promotion backup path already exists")
            os.replace(str(destination), str(backup))
            backed_up = True
        os.replace(str(stage), str(destination))
        installed = True
        for relative, _, digest in records:
            target = safe_path(destination, relative)
            _require(canonical_digest(target.read_bytes()) == digest, "installed source hash drift: %s" % relative)
        if backup.exists():
            shutil.rmtree(str(backup))
            backed_up = False
        return {
            "result": "promoted",
            "brand": brand_slug,
            "bundle_sha256": bundle["record_sha256"],
            "files": [{"path": relative, "sha256": digest} for relative, _, digest in records],
        }
    except Exception as error:
        if installed and destination.exists():
            shutil.rmtree(str(destination))
        if backed_up and backup.exists():
            os.replace(str(backup), str(destination))
        if stage.exists():
            shutil.rmtree(str(stage))
        if isinstance(error, PromotionError):
            raise
        raise PromotionError("promotion rolled back: %s" % error) from error
    finally:
        if stage.exists():
            shutil.rmtree(str(stage))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle")
    parser.add_argument("--approval-root", required=True)
    parser.add_argument("--brands-root", required=True)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    try:
        result = promote(args.bundle, args.approval_root, args.brands_root, args.replace)
    except PromotionError as error:
        print("promotion: FAIL, %s" % error)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
