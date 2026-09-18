#!/usr/bin/env python3
"""Validate cross-host conformance policy, evidence, traces, and visual review."""

import hashlib
import json
import math
import re
from pathlib import Path


class ConformanceError(ValueError):
    """Raised when conformance source or evidence is invalid."""


HERE = Path(__file__).resolve().parent
DEFAULT_POLICY = HERE.parent / "references" / "conformance-contract.json"
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:[-+][0-9A-Za-z.-]+)?$")
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
REQUIRED_PROFILES = {
    "phone-portrait-touch", "phone-landscape-touch", "narrow-desktop",
    "normal-desktop", "reduced-motion", "forced-colors", "text-scale-200",
}
REQUIRED_TRACKS = {"browser-react", "tauri-android", "wails-windows", "egui-native"}
DIAGNOSTIC_CLASSES = ["visual", "accessibility", "interaction", "host-boundary"]
TRACK_EVIDENCE = {
    "browser-react": "browser-reference",
    "tauri-android": "tauri-reference-host",
    "wails-windows": "wails-reference-host",
    "egui-native": "egui-reference-renderer",
}


def _canonical(payload):
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _finite(value, label, positive=False, nonnegative=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ConformanceError("%s must be a finite %snumber" % (label, "positive " if positive else ""))
    if positive and value <= 0:
        raise ConformanceError("%s must be a finite positive number" % label)
    if nonnegative and value < 0:
        raise ConformanceError("%s must be a finite non-negative number" % label)
    return float(value)


def _unique(items, label):
    if len(items) != len(set(items)):
        raise ConformanceError("%s contains duplicate identifiers" % label)


def _validate_profile(profile):
    profile_id = profile.get("id")
    if not isinstance(profile_id, str) or not SAFE_ID.fullmatch(profile_id):
        raise ConformanceError("profile id is missing or unsafe")
    viewport = profile.get("viewport") or {}
    _finite(viewport.get("width"), "%s viewport width" % profile_id, positive=True)
    _finite(viewport.get("height"), "%s viewport height" % profile_id, positive=True)
    if viewport.get("orientation") not in {"portrait", "landscape"}:
        raise ConformanceError("%s viewport orientation is invalid" % profile_id)
    if profile.get("motion") not in {"standard", "reduced"}:
        raise ConformanceError("%s motion profile is invalid" % profile_id)
    if profile.get("contrast") not in {"normal", "forced-colors", "high-contrast", "unsupported"}:
        raise ConformanceError("%s contrast profile is invalid" % profile_id)
    _finite(profile.get("text_scale"), "%s text scale" % profile_id, positive=True)
    for edge in ("top", "right", "bottom", "left"):
        _finite((profile.get("safe_area") or {}).get(edge), "%s safe area %s" % (profile_id, edge), nonnegative=True)
    _finite(profile.get("ime_block_end"), "%s IME obstruction" % profile_id, nonnegative=True)
    if not isinstance(profile.get("input"), dict) or profile.get("window_class") not in {"compact", "narrow", "normal", "expanded"}:
        raise ConformanceError("%s capability record is incomplete" % profile_id)


def _validate_policy(policy):
    if policy.get("schema_version") != 1 or not SEMVER.fullmatch(str(policy.get("contract_version", ""))):
        raise ConformanceError("conformance schema or contract version is invalid")
    if policy.get("diagnostic_classes") != DIAGNOSTIC_CLASSES:
        raise ConformanceError("diagnostic classes must remain distinct and ordered")
    profiles = policy.get("profiles")
    if not isinstance(profiles, list):
        raise ConformanceError("conformance profiles are missing")
    profile_ids = [profile.get("id") for profile in profiles if isinstance(profile, dict)]
    _unique(profile_ids, "profiles")
    if set(profile_ids) != REQUIRED_PROFILES:
        raise ConformanceError("conformance profiles do not cover the required matrix")
    for profile in profiles:
        _validate_profile(profile)
    tracks = policy.get("host_tracks")
    if not isinstance(tracks, list):
        raise ConformanceError("host tracks are missing")
    track_ids = [track.get("id") for track in tracks if isinstance(track, dict)]
    _unique(track_ids, "host tracks")
    if set(track_ids) != REQUIRED_TRACKS:
        raise ConformanceError("host tracks do not cover the required renderers")
    for track in tracks:
        track_id = track.get("id")
        if track.get("evidence_class") != TRACK_EVIDENCE.get(track_id):
            raise ConformanceError("%s evidence class is invalid" % track_id)
        if track.get("status") not in policy.get("statuses", []):
            raise ConformanceError("%s status is invalid" % track_id)
        for version_field in ("host_version", "renderer_version", "target_version", "tool_version"):
            if not isinstance(track.get(version_field), str) or not track[version_field].strip():
                raise ConformanceError("%s %s is missing" % (track_id, version_field))
        if not isinstance(track.get("entry_point"), str) or ".." in track["entry_point"] or track["entry_point"].startswith(("/", "\\")):
            raise ConformanceError("%s entry point is unsafe" % track_id)
        if not set(track.get("profiles") or []).issubset(REQUIRED_PROFILES) or not track.get("profiles"):
            raise ConformanceError("%s profile coverage is invalid" % track_id)
    traces = policy.get("traces") or {}
    for required in ("glitchpad-safe-area-known-bad", "glitchpad-safe-area-corrected", "wails-window-chrome"):
        if required not in traces:
            raise ConformanceError("required trace is missing: %s" % required)
    baseline = policy.get("baseline_policy") or {}
    if baseline.get("candidate_review_state") != "pending-human-review":
        raise ConformanceError("candidate generation must remain pending human review")
    if set(baseline.get("decisions") or []) != {"accepted", "rejected"}:
        raise ConformanceError("baseline decision vocabulary is invalid")
    return policy


def load_policy(path=None):
    policy_path = Path(path) if path else DEFAULT_POLICY
    try:
        payload = json.loads(policy_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ConformanceError("cannot load conformance policy: %s" % error)
    if not isinstance(payload, dict):
        raise ConformanceError("conformance policy root must be an object")
    return _validate_policy(payload)


def _rect(record, label):
    values = {}
    for key in ("x", "y", "width", "height"):
        values[key] = _finite(record.get(key), "%s %s" % (label, key), positive=key in {"width", "height"})
    return values


def _overlaps(left, right):
    return not (
        left["x"] + left["width"] <= right["x"] or
        right["x"] + right["width"] <= left["x"] or
        left["y"] + left["height"] <= right["y"] or
        right["y"] + right["height"] <= left["y"]
    )


def _diagnostic(code, profile, host, subject, message):
    return {
        "class": "host-boundary", "code": code, "brand": "fixture",
        "profile": profile, "host": host, "subject": subject, "message": message,
    }


def evaluate_trace(trace):
    if not isinstance(trace, dict) or not isinstance(trace.get("events"), list) or not trace["events"]:
        raise ConformanceError("trace events are missing")
    host = trace.get("host_track")
    if host not in REQUIRED_TRACKS:
        raise ConformanceError("trace host track is invalid")
    diagnostics = []
    expected_sequence = 0
    for event in trace["events"]:
        if event.get("sequence") != expected_sequence:
            raise ConformanceError("trace sequence must be contiguous")
        expected_sequence += 1
        profile = event.get("profile")
        if profile not in REQUIRED_PROFILES:
            raise ConformanceError("trace profile is invalid")
        viewport = event.get("viewport") or {}
        width = _finite(viewport.get("width"), "viewport width", positive=True)
        height = _finite(viewport.get("height"), "viewport height", positive=True)
        safe = event.get("safe_area") or {}
        insets = {}
        for edge in ("top", "right", "bottom", "left"):
            insets[edge] = _finite(safe.get(edge), "safe area %s" % edge, nonnegative=True)
        ime = _finite(event.get("ime_block_end"), "IME obstruction", nonnegative=True)
        ownership = event.get("ownership") or {}
        owner_counts = {}
        for boundary in ("safe_area", "ime_obstruction", "titlebar_regions"):
            owner = ownership.get(boundary)
            owners = owner if isinstance(owner, list) else [owner]
            owners = [item for item in owners if item in {"host", "app-frame"}]
            if not owners:
                diagnostics.append(_diagnostic("host.missing-owner", profile, host, boundary, "%s has no declared owner" % boundary))
            if len(owners) != len(set(owners)) or len(set(owners)) > 1:
                diagnostics.append(_diagnostic("host.duplicate-owner", profile, host, boundary, "%s has more than one owner" % boundary))
            owner_counts[boundary] = max(1, len(owners))
        left = insets["left"] * owner_counts["safe_area"]
        right = width - insets["right"] * owner_counts["safe_area"]
        top = insets["top"] * owner_counts["safe_area"]
        bottom = height - insets["bottom"] * owner_counts["safe_area"] - ime * owner_counts["ime_obstruction"]
        if right <= left or bottom <= top:
            diagnostics.append(_diagnostic("host.no-usable-content", profile, host, "viewport", "host envelope leaves no positive usable content"))
        reserved = [_rect(region, "titlebar region") for region in event.get("titlebar_regions") or []]
        for control_record in event.get("required_controls") or []:
            control = _rect(control_record, "required control")
            control_id = str(control_record.get("id") or "required-control")
            contained = (
                control["x"] >= left and control["y"] >= top and
                control["x"] + control["width"] <= right and
                control["y"] + control["height"] <= bottom
            )
            if not contained:
                diagnostics.append(_diagnostic("host.control-obstructed", profile, host, control_id, "required control is outside usable content"))
            if any(_overlaps(control, region) for region in reserved):
                diagnostics.append(_diagnostic("host.titlebar-overlap", profile, host, control_id, "required control overlaps a native titlebar region"))
    return diagnostics


def validate_diagnostic(policy, diagnostic):
    problems = []
    if not isinstance(diagnostic, dict):
        return ["diagnostic must be an object"]
    if diagnostic.get("class") not in policy.get("diagnostic_classes", []):
        problems.append("diagnostic class is unknown")
    if not isinstance(diagnostic.get("code"), str) or not SAFE_ID.fullmatch(diagnostic.get("code", "")):
        problems.append("diagnostic code is missing or unsafe")
    for key in ("brand", "profile", "host", "subject", "message"):
        if not isinstance(diagnostic.get(key), str) or not diagnostic[key].strip():
            problems.append("diagnostic %s is missing" % key)
    return problems


def validate_evidence(policy, result):
    problems = []
    if not isinstance(result, dict):
        return ["evidence result must be an object"]
    tracks = {track["id"]: track for track in policy["host_tracks"]}
    track = tracks.get(result.get("host_track"))
    if not track:
        problems.append("host track is unknown")
        return problems
    if result.get("evidence_class") != track["evidence_class"]:
        problems.append("evidence class cannot substitute for %s" % track["id"])
    if result.get("status") not in policy.get("statuses", []):
        problems.append("evidence status is unknown")
    tool = result.get("tool") or {}
    if not isinstance(tool.get("name"), str) or not tool.get("name") or not isinstance(tool.get("version"), str) or not tool.get("version"):
        problems.append("evidence tool name and exact version are required")
    declared_profiles = set(result.get("profiles") or [])
    if not declared_profiles or not declared_profiles.issubset(set(track["profiles"])):
        problems.append("evidence profiles do not match the host track")
    for diagnostic in result.get("diagnostics") or []:
        problems.extend(validate_diagnostic(policy, diagnostic))
    return problems


def candidate_manifest(image_bytes, metadata):
    if not isinstance(image_bytes, bytes) or not image_bytes:
        raise ConformanceError("visual candidate image bytes are required")
    required = {"brand", "brand_version", "versions", "source_revision", "host", "profile", "viewport", "fonts", "rendering"}
    missing = sorted(required - set(metadata))
    if missing:
        raise ConformanceError("visual candidate metadata is missing: %s" % ", ".join(missing))
    image_sha = hashlib.sha256(image_bytes).hexdigest()
    payload = dict(metadata)
    payload["image_sha256"] = image_sha
    payload["review_state"] = "pending-human-review"
    payload["candidate_id"] = hashlib.sha256(image_sha.encode("ascii") + b"\n" + _canonical(payload)).hexdigest()
    return payload


def validate_decision(candidate, decision, policy=None):
    policy = policy or load_policy()
    baseline = policy["baseline_policy"]
    problems = []
    if not isinstance(decision, dict):
        return ["baseline decision must be an object"]
    for field in baseline["required_decision_fields"]:
        if field not in decision or decision[field] in (None, "", [], {}):
            problems.append("baseline decision %s is required" % field)
    if decision.get("candidate_id") != candidate.get("candidate_id"):
        problems.append("baseline decision candidate identity is stale or mismatched")
    if decision.get("decision") not in baseline["decisions"]:
        problems.append("baseline decision value is invalid")
    reviewer = str(decision.get("reviewer", "")).lower()
    if any(pattern in reviewer for pattern in baseline["automation_reviewer_patterns"]):
        problems.append("baseline reviewer must be a human identity")
    if not TIMESTAMP.fullmatch(str(decision.get("reviewed_at", ""))):
        problems.append("baseline reviewed_at must be a UTC timestamp")
    if decision.get("source_revision") != candidate.get("source_revision"):
        problems.append("baseline source revision does not match the candidate")
    expected_environment = {key: candidate.get(key) for key in ("host", "profile", "viewport", "fonts", "rendering")}
    if decision.get("environment") != expected_environment:
        problems.append("baseline environment does not match the candidate")
    return problems


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()
