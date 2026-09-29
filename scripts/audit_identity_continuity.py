#!/usr/bin/env python3
"""Generate or audit truthful continuity records for production brand sources."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "skill" / "templates"
sys.path.insert(0, str(TEMPLATES))

from identity_continuity import canonical_digest, identity_snapshot, record_digest, validate_brand_continuity
from process_utils import hidden_process_kwargs


BRAND_CLASSES = {
    "covarity": "legacy-constructed",
    "cueson": "glyphkit-constructed",
    "dancewithme865": "authoritative",
    "eso-weave": "authoritative",
    "fragcap": "legacy-constructed",
    "glitchpad": "legacy-constructed",
    "go-schedule": "legacy-constructed",
    "i-heart-pr-tours": "authoritative",
    "local-companion": "glyphkit-constructed",
    "scruggs-tire-alignment": "authoritative",
    "shruggietech": "authoritative",
}
MIGRATION_BASELINE_BRANDS = set(BRAND_CLASSES) - {"i-heart-pr-tours", "local-companion"}
MIGRATION_BASELINE_REVISION = "011f35303ef1d555dbbbcf6708447cc321df40db"
# S057 approved the current go-schedule mark after the historical migration.
# The source commit binds that owner-approved snapshot independently of the
# historical record, whose status must remain truthful.
OWNER_APPROVED_IDENTITY_REVISIONS = {
    "go-schedule": "d33cb8c658eac2f66b58e715274e0c791bad9ba3",
    # S063 approved the reduced square source and framing while keeping the
    # historical continuity record honest about its original migration basis.
    "shruggietech": "d485017abdacfa4fa930595042b282ad950617dd",
}
OWNER_APPROVED_SNAPSHOT_SHA256 = {
    "shruggietech": "bdaaab0f6dc78a127d82ed0cb804549d52c67558039c7612a03ac0fea649c6a5",
}
REFERENCE = {"record": "identity-continuity.json", "status": "historical-baseline"}
COVARITY_REASON = "The custom arc and path serializer predates glyphkit. Its shipped path bytes remain unchanged as historical identity source."


def _write_json(path, value):
    with open(str(path), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def discover_brands(root=ROOT):
    parent = Path(root) / "brands"
    return {path.name: path for path in sorted(parent.iterdir()) if (path / "brand.json").is_file()}


def _source_files(source, brand, source_class):
    candidates = []
    helper = source / "build" / "mk_paths.py"
    if source_class in {"glyphkit-constructed", "legacy-constructed"} and helper.is_file():
        candidates.append(("build/mk_paths.py", "identity construction source"))
    for item in brand.get("authoritative_inputs", []):
        if item.get("usage_status") == "approved":
            candidates.append((item["path"], "authoritative %s source" % item["role"]))
    records = []
    for relative, purpose in sorted(set(candidates)):
        path = source / relative
        records.append({
            "path": relative,
            "purpose": purpose,
            "bytes": path.stat().st_size,
            "sha256": canonical_digest(path.read_bytes()),
        })
    return records


def build_record(source, brand, source_class, revision, recorded_on):
    snapshot = identity_snapshot(brand, source_class)
    record = {
        "schema_version": 1,
        "brand": brand["slug"],
        "status": "historical-baseline",
        "source_class": source_class,
        "recorded_on": recorded_on,
        "source_revision": revision,
        "source_files": _source_files(Path(source), brand, source_class),
        "identity_snapshot": snapshot,
        "topology": snapshot["topology"],
        "framing": snapshot["framing"],
        "palette": snapshot["palette"],
        "renderer": None,
        "proofs": [],
        "approval": None,
        "historical_evidence": {
            "basis": "current-authoritative-source",
            "baseline_revision": revision,
            "approval_completeness": "partial" if brand.get("approval_ledger") else "unknown",
            "limitation": "This migration records current source facts and is not retrospective canonical approval.",
            "migration_issue": 185,
        },
        "record_sha256": "",
    }
    record["record_sha256"] = record_digest(record)
    return record


def _normalized_for_preservation(slug, brand):
    value = copy.deepcopy(brand)
    value.pop("identity_continuity", None)
    if slug == "covarity":
        logo = value.get("logo") or {}
        if logo.get("geometry_provenance") == "legacy-constructed":
            logo["geometry_provenance"] = "glyphkit"
            logo.pop("geometry_provenance_reason", None)
    return value


def compare_brand_state(slug, before, after):
    left = _normalized_for_preservation(slug, before)
    right = _normalized_for_preservation(slug, after)
    if left == right:
        return []
    problems = []
    for key in sorted(set(left) | set(right)):
        if left.get(key) != right.get(key):
            problems.append("%s changed" % key)
    return problems


def _git_brand(revision, slug):
    result = subprocess.run(
        ["git", "show", "%s:brands/%s/brand.json" % (revision, slug)],
        cwd=str(ROOT), capture_output=True, check=True, text=True,
        **hidden_process_kwargs(),
    )
    return json.loads(result.stdout)


def compare_historical_identity(slug, revision, brand):
    """Reject identity drift even if current brand and continuity record agree."""
    approved_revision = OWNER_APPROVED_IDENTITY_REVISIONS.get(slug)
    baseline = _git_brand(approved_revision or revision, slug)
    source_class = BRAND_CLASSES[slug]
    before = identity_snapshot(_normalized_for_preservation(slug, baseline), source_class)
    after = identity_snapshot(_normalized_for_preservation(slug, brand), source_class)
    if approved_revision:
        approval = baseline.get("current_mark_approval") or {}
        expected = OWNER_APPROVED_SNAPSHOT_SHA256.get(slug, approval.get("identity_snapshot_sha256"))
        if expected != before["sha256"]:
            return ["approved identity baseline lacks its exact owner-bound snapshot"]
    return ["%s changed" % key for key in before if key != "sha256" and before[key] != after[key]]


def audit(revision, write=False, recorded_on="2026-09-09", report_path=None):
    brands = discover_brands(ROOT)
    problems = []
    results = []
    if set(brands) != set(BRAND_CLASSES):
        problems.append("production brand inventory does not match the explicit migration map")
    if not write and revision != MIGRATION_BASELINE_REVISION:
        problems.append("historical migration baseline revision changed")
    for slug, source in brands.items():
        brand_path = source / "brand.json"
        brand = json.loads(brand_path.read_text(encoding="utf-8"))
        if slug not in MIGRATION_BASELINE_BRANDS:
            try:
                result = validate_brand_continuity(brand, source)
                results.append(dict(result, preservation="new-approved-source"))
            except Exception as error:
                problems.append("%s: %s" % (slug, error))
            continue
        if write:
            updated = copy.deepcopy(brand)
            updated["identity_continuity"] = dict(REFERENCE)
            if slug == "covarity":
                updated["logo"]["geometry_provenance"] = "legacy-constructed"
                updated["logo"]["geometry_provenance_reason"] = COVARITY_REASON
            if updated != brand:
                with open(str(brand_path), "w", encoding="utf-8", newline="\n") as handle:
                    handle.write(json.dumps(updated, indent=2, ensure_ascii=False) + "\n")
            brand = updated
            record = build_record(source, brand, BRAND_CLASSES[slug], revision, recorded_on)
            _write_json(source / "identity-continuity.json", record)
        try:
            brand = json.loads(brand_path.read_text(encoding="utf-8"))
            result = validate_brand_continuity(brand, source)
            if write:
                baseline = _git_brand(revision, slug)
                drift = compare_brand_state(slug, baseline, brand)
                if drift:
                    problems.extend("%s: %s" % (slug, item) for item in drift)
                results.append(dict(result, preservation="passed" if not drift else "failed"))
            else:
                # Nonidentity copy and schema updates can differ from the old
                # source; governed identity must match its pinned baseline.
                if result["status"] == "approved-canonical":
                    results.append(dict(result, preservation="new-approved-source"))
                else:
                    drift = compare_historical_identity(slug, MIGRATION_BASELINE_REVISION, brand)
                    if drift:
                        problems.extend("%s: %s" % (slug, item) for item in drift)
                    results.append(dict(result, preservation="baseline-preserved" if not drift else "failed"))
        except Exception as error:
            problems.append("%s: %s" % (slug, error))
    report = {"schema_version": 1, "baseline_revision": revision, "brands": results, "problems": problems}
    if report_path:
        path = Path(report_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        _write_json(path, report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-revision")
    parser.add_argument("--recorded-on", default="2026-09-09")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true", help="Validate committed records without rewriting source")
    parser.add_argument("--report", "--output", dest="report")
    args = parser.parse_args()
    if args.write and args.check:
        parser.error("--write and --check are mutually exclusive")
    revision = args.baseline_revision
    if revision is None:
        revisions = set()
        for slug, source in discover_brands(ROOT).items():
            if slug not in MIGRATION_BASELINE_BRANDS:
                continue
            path = source / "identity-continuity.json"
            if path.is_file():
                revisions.add(json.loads(path.read_text(encoding="utf-8")).get("source_revision"))
        if len(revisions) != 1:
            parser.error("--baseline-revision is required when committed records do not agree")
        revision = revisions.pop()
    report = audit(revision, args.write, args.recorded_on, args.report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if report["problems"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
