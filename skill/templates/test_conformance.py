#!/usr/bin/env python3
"""Contract and generated-fixture tests for cross-host conformance."""

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from conformance_contract import (  # noqa: E402
    ConformanceError,
    candidate_manifest,
    evaluate_trace,
    load_policy,
    validate_decision,
    validate_diagnostic,
    validate_evidence,
)
from gen_conformance import generate_conformance, verify_conformance  # noqa: E402
from process_utils import hidden_process_kwargs  # noqa: E402


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, indent=2) + "\n")


def minimal_kit(root):
    kit = root / "example"
    write_json(kit / "brand.json", {
        "slug": "example", "title": "Example", "version": "2.0.0", "canon": "1.2.1",
    })
    versions = {
        "canon_version": "1.2.1", "interface_canon_version": "1.0.0",
        "component_recipe_version": "1.1.0", "web_react_adapter_version": "1.1.0",
        "egui_adapter_version": "1.0.0", "compiler_version": "1.2.1",
        "brand_version": "2.0.0",
    }
    write_json(kit / "enforcement" / "consumer-contract.json", {
        "schema_version": 3, "brand": {"slug": "example", "brand_version": "2.0.0"},
        "versions": versions, "source_revision": "abc123",
    })
    recipes = [
        "AppFrame", "Button", "IconButton", "Toolbar", "Tabs", "Menu", "Dialog",
        "Field", "FormControls", "ListRow", "SplitPane", "Toast", "StatusBadge", "Card",
        "EmptyState",
    ]
    write_json(kit / "web" / "adapter.json", {
        "adapter_version": "1.1.0", "component_recipe_version": "1.1.0",
        "interface_canon_version": "1.0.0", "brand": "example", "recipes": recipes,
    })
    write_json(kit / "native" / "egui" / "adapter.json", {
        "adapter": "egui", "adapter_version": "1.0.0", "brand": "example",
        "brand_version": "2.0.0", "brand_canon_version": "1.2.1",
        "interface_canon_version": "1.0.0", "component_recipe_version": "1.1.0",
        "compiler_version": "1.2.1", "recipes": recipes,
        "crate": {"dependencies": {"egui": "=0.36.1"}},
    })
    specimen = "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>Example specimen</title></head><body><main><h1>Example</h1></main></body></html>\n"
    with (kit / "web" / "specimen.html").open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(specimen)
    return kit


class ConformancePolicyTests(unittest.TestCase):
    def test_policy_covers_required_profiles_hosts_and_diagnostics(self):
        policy = load_policy()
        self.assertEqual(
            {"phone-portrait-touch", "phone-landscape-touch", "narrow-desktop", "normal-desktop", "reduced-motion", "forced-colors", "text-scale-200"},
            {profile["id"] for profile in policy["profiles"]},
        )
        self.assertEqual(
            {"browser-react", "tauri-android", "wails-windows", "egui-native"},
            {track["id"] for track in policy["host_tracks"]},
        )
        for track in policy["host_tracks"]:
            self.assertEqual("supported", track["status"])
            for field in ("host_version", "renderer_version", "target_version", "tool_version"):
                self.assertTrue(track[field])
        self.assertEqual(
            ["visual", "accessibility", "interaction", "host-boundary"],
            policy["diagnostic_classes"],
        )

    def test_known_bad_fails_and_corrected_trace_passes(self):
        policy = load_policy()
        bad = evaluate_trace(policy["traces"]["glitchpad-safe-area-known-bad"])
        self.assertIn("host.duplicate-owner", {item["code"] for item in bad})
        self.assertIn("host.control-obstructed", {item["code"] for item in bad})
        self.assertEqual([], evaluate_trace(policy["traces"]["glitchpad-safe-area-corrected"]))

    def test_invalid_geometry_fails_closed(self):
        policy = load_policy()
        trace = copy.deepcopy(policy["traces"]["glitchpad-safe-area-corrected"])
        trace["events"][0]["viewport"]["width"] = float("nan")
        with self.assertRaisesRegex(ConformanceError, "finite positive"):
            evaluate_trace(trace)

    def test_evidence_cannot_substitute_browser_for_native_host(self):
        policy = load_policy()
        result = {
            "brand": "example", "host_track": "tauri-android",
            "evidence_class": "browser-reference", "status": "supported",
            "tool": {"name": "chromium", "version": "1"},
            "profiles": ["phone-portrait-touch"], "diagnostics": [],
        }
        self.assertIn("evidence class", " ".join(validate_evidence(policy, result)).lower())

    def test_diagnostics_require_one_known_primary_class(self):
        policy = load_policy()
        diagnostic = {
            "class": "generic", "code": "unknown", "brand": "example",
            "profile": "normal-desktop", "host": "browser-react",
            "subject": "button", "message": "failed",
        }
        self.assertIn("diagnostic class", " ".join(validate_diagnostic(policy, diagnostic)).lower())


class BaselineDecisionTests(unittest.TestCase):
    def setUp(self):
        self.metadata = {
            "brand": "example", "brand_version": "2.0.0",
            "versions": {"conformance_contract_version": "1.0.0"},
            "source_revision": "abc123", "host": "browser-react",
            "profile": "normal-desktop", "viewport": {"width": 1280, "height": 900, "orientation": "landscape"},
            "fonts": [{"family": "Example Sans", "source": "fonts/example.woff2", "loaded": True}],
            "rendering": {"renderer": "chromium", "version": "1", "device_scale_factor": 1, "color_scheme": "light", "contrast": "normal", "motion": "standard"},
        }
        self.candidate = candidate_manifest(b"png bytes", self.metadata)

    def valid_decision(self):
        return {
            "candidate_id": self.candidate["candidate_id"], "decision": "accepted",
            "reviewer": "William Thompson", "reason": "Reviewed the complete candidate set.",
            "reviewed_at": "2026-09-17T23:00:00Z", "source_revision": "abc123",
            "environment": {key: self.candidate[key] for key in ("host", "profile", "viewport", "fonts", "rendering")},
        }

    def test_candidate_is_pending_and_deterministic(self):
        self.assertEqual("pending-human-review", self.candidate["review_state"])
        self.assertEqual(self.candidate, candidate_manifest(b"png bytes", self.metadata))

    def test_human_decision_accepts_exact_candidate(self):
        self.assertEqual([], validate_decision(self.candidate, self.valid_decision()))

    def test_automation_and_stale_decisions_fail_closed(self):
        automated = self.valid_decision()
        automated["reviewer"] = "github-actions[bot]"
        self.assertTrue(validate_decision(self.candidate, automated))
        stale = self.valid_decision()
        stale["candidate_id"] = "0" * 64
        self.assertTrue(validate_decision(self.candidate, stale))
        incomplete = self.valid_decision()
        incomplete["reason"] = ""
        self.assertTrue(validate_decision(self.candidate, incomplete))


class GeneratedFixtureTests(unittest.TestCase):
    def test_generation_is_deterministic_and_complete(self):
        with tempfile.TemporaryDirectory(prefix="conformance-") as temporary:
            root = Path(temporary)
            first = minimal_kit(root / "first")
            second = minimal_kit(root / "second")
            generate_conformance(first / "brand.json", first)
            generate_conformance(second / "brand.json", second)
            paths = [
                "conformance/manifest.json", "conformance/browser/specimen.html",
                "conformance/evidence/traces.json", "conformance/hosts/tauri-android/Cargo.toml",
                "conformance/hosts/tauri-android/Cargo.lock", "conformance/hosts/tauri-android/src/lib.rs",
                "conformance/hosts/tauri-android/tests/ownership.rs",
                "conformance/hosts/wails-windows/go.mod", "conformance/hosts/wails-windows/ownership.go",
                "conformance/hosts/wails-windows/ownership_test.go", "conformance/README.md",
            ]
            for relative in paths:
                self.assertEqual((first / relative).read_bytes(), (second / relative).read_bytes(), relative)
            self.assertEqual([], verify_conformance(first))
            manifest = json.loads((first / "conformance" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(15, len(manifest["recipes"]))
            self.assertEqual(7, len(manifest["profiles"]))
            self.assertEqual(4, len(manifest["host_tracks"]))
            self.assertTrue(all(track["status"] == "supported" for track in manifest["host_tracks"]))
            self.assertRegex(manifest["source_revision"], r"^[0-9a-f]{40,64}$")

    def test_tampering_and_missing_files_fail_verification(self):
        with tempfile.TemporaryDirectory(prefix="conformance-") as temporary:
            kit = minimal_kit(Path(temporary))
            generate_conformance(kit / "brand.json", kit)
            (kit / "conformance" / "hosts" / "wails-windows" / "ownership.go").unlink()
            self.assertIn("missing", " ".join(verify_conformance(kit)).lower())

    def test_generated_rust_and_go_fixtures_execute_when_tools_exist(self):
        with tempfile.TemporaryDirectory(prefix="conformance-") as temporary:
            kit = minimal_kit(Path(temporary))
            generate_conformance(kit / "brand.json", kit)
            cargo = shutil.which("cargo")
            go = shutil.which("go")
            if os.environ.get("CI"):
                self.assertIsNotNone(cargo, "CI must execute the generated Rust fixture")
                self.assertIsNotNone(go, "CI must execute the generated Go fixture")
            if cargo:
                command = ["cargo", "test", "--manifest-path", str(kit / "conformance" / "hosts" / "tauri-android" / "Cargo.toml"), "--locked"]
                completed = subprocess.run(command, cwd=str(ROOT), capture_output=True, text=True, **hidden_process_kwargs())
                self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
            if go:
                completed = subprocess.run(["go", "test", "./..."], cwd=str(kit / "conformance" / "hosts" / "wails-windows"), capture_output=True, text=True, **hidden_process_kwargs())
                self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
