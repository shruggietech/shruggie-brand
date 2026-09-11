#!/usr/bin/env python3
"""Regression tests for the verified publication workflow and artifact boundary."""

from __future__ import annotations

import os
import re
import tempfile
import unittest
from pathlib import Path

import audit_publication_artifacts


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "build.yml"
PRODUCTION = (
    "covarity",
    "cueson",
    "eso-weave",
    "fragcap",
    "glitchpad",
    "go-schedule",
    "i-heart-pr-tours",
    "shruggietech",
)
EXPECTED_ACTIONS = {
    "actions/checkout": "d23441a48e516b6c34aea4fa41551a30e30af803",
    "actions/setup-python": "ece7cb06caefa5fff74198d8649806c4678c61a1",
    "actions/setup-node": "249970729cb0ef3589644e2896645e5dc5ba9c38",
    "actions/upload-artifact": "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
    "actions/download-artifact": "37930b1c2abaa49bbe596cd826c3c89aef350131",
    "actions/upload-pages-artifact": "fc324d3547104276b827a68afc52ff2a11cc49c9",
    "actions/deploy-pages": "368f82528645a54fb793d4d04e342629a3f51346",
    "pnpm/action-setup": "fc06bc1257f339d1d5d8b3a19a8cae5388b55320",
}


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def job_block(text: str, job_id: str) -> str:
    match = re.search(
        r"(?ms)^  " + re.escape(job_id) + r":\n(?P<body>.*?)(?=^  [a-zA-Z0-9_-]+:\n|\Z)",
        text,
    )
    if not match:
        raise AssertionError("workflow lacks job %s" % job_id)
    return match.group(0)


def create_publication_trees(root: Path) -> tuple[Path, Path]:
    kits = root / "dist"
    site = root / "site" / "out"
    for slug in PRODUCTION:
        kit_icons = kits / slug / "icons"
        site_icons = site / slug / "downloads" / "files" / "icons"
        kit_icons.mkdir(parents=True)
        site_icons.mkdir(parents=True)
        (kit_icons / ".iconkit-generated.json").write_text("{}\n", encoding="utf-8")
        (site_icons / ".iconkit-generated.json").write_text("{}\n", encoding="utf-8")
        (kits / slug / "brand.json").write_text("{}\n", encoding="utf-8")
        (site / slug / "index.html").write_text("ok\n", encoding="utf-8")
    return kits, site


class PublicationArtifactAuditTests(unittest.TestCase):
    def test_valid_publication_trees_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site = create_publication_trees(root)
            result = audit_publication_artifacts.audit(root, kits, site)
            self.assertEqual(8, result["kit_markers"])
            self.assertEqual(8, result["site_markers"])

    def test_symlink_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site = create_publication_trees(root)
            target = kits / PRODUCTION[0] / "brand.json"
            link = kits / PRODUCTION[0] / "brand-link.json"
            try:
                link.symlink_to(target.name)
            except OSError as error:
                self.skipTest("symlink creation unavailable: %s" % error)
            with self.assertRaisesRegex(ValueError, "symbolic link"):
                audit_publication_artifacts.audit(root, kits, site)

    def test_hard_link_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site = create_publication_trees(root)
            target = site / PRODUCTION[0] / "index.html"
            link = site / PRODUCTION[0] / "index-copy.html"
            try:
                os.link(str(target), str(link))
            except OSError as error:
                self.skipTest("hard-link creation unavailable: %s" % error)
            with self.assertRaisesRegex(ValueError, "hard link"):
                audit_publication_artifacts.audit(root, kits, site)

    def test_unexpected_hidden_path_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site = create_publication_trees(root)
            (site / ".secrets").write_text("no\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unexpected hidden path"):
                audit_publication_artifacts.audit(root, kits, site)

    def test_missing_governed_marker_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site = create_publication_trees(root)
            (site / PRODUCTION[0] / "downloads" / "files" / "icons" /
             ".iconkit-generated.json").unlink()
            with self.assertRaisesRegex(ValueError, "marker inventory"):
                audit_publication_artifacts.audit(root, kits, site)

    def test_extra_governed_marker_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site = create_publication_trees(root)
            extra = site / PRODUCTION[0] / "other" / ".iconkit-generated.json"
            extra.parent.mkdir()
            extra.write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unexpected hidden path"):
                audit_publication_artifacts.audit(root, kits, site)

    def test_paths_outside_repository_root_fail_closed(self):
        with tempfile.TemporaryDirectory() as root_tmp, tempfile.TemporaryDirectory() as other_tmp:
            root = Path(root_tmp)
            other = Path(other_tmp)
            kits, site = create_publication_trees(other)
            with self.assertRaisesRegex(ValueError, "outside repository root"):
                audit_publication_artifacts.audit(root, kits, site)


class PublicationWorkflowContractTests(unittest.TestCase):
    def test_build_is_the_only_publication_workflow(self):
        self.assertTrue(WORKFLOW.is_file())
        self.assertFalse((WORKFLOW.parent / "pages.yml").exists())
        self.assertFalse((WORKFLOW.parent / "release.yml").exists())

    def test_events_cover_pr_main_tag_and_manual_without_unsafe_triggers(self):
        text = workflow_text()
        self.assertIn("pull_request:\n", text)
        self.assertIn("branches: [main]", text)
        self.assertIn('tags: ["v*"]', text)
        self.assertIn("workflow_dispatch:\n", text)
        self.assertNotIn("pull_request_target", text)
        self.assertNotIn("workflow_run", text)
        self.assertNotRegex(text, r"(?m)^  push:\s*$\n  pull_request:")

    def test_external_actions_are_immutable_and_expected(self):
        text = workflow_text()
        found = re.findall(r"uses:\s+([^\s@]+)@([^\s#]+)(?:\s+#\s+([^\n]+))?", text)
        self.assertTrue(found)
        for action, revision, comment in found:
            if action.startswith("./"):
                continue
            self.assertIn(action, EXPECTED_ACTIONS)
            self.assertEqual(EXPECTED_ACTIONS[action], revision, action)
            self.assertRegex(revision, r"^[0-9a-f]{40}$")
            self.assertRegex(comment or "", r"^v\d")

    def test_checkouts_are_exact_and_do_not_persist_credentials(self):
        text = workflow_text()
        checkout_count = text.count("uses: actions/checkout@")
        self.assertGreaterEqual(checkout_count, 3)
        self.assertEqual(checkout_count, text.count("ref: ${{ github.sha }}"))
        self.assertEqual(checkout_count, text.count("persist-credentials: false"))
        self.assertEqual(checkout_count, text.count('test "$(git rev-parse HEAD)" = "$GITHUB_SHA"'))

    def test_renderer_and_runtime_contract_are_exact(self):
        text = workflow_text()
        self.assertGreaterEqual(text.count("node-version: 24.11.0"), 2)
        self.assertGreaterEqual(text.count("@resvg/resvg-js@2.6.2"), 2)
        self.assertNotIn("rsvg-convert", text)
        self.assertNotIn("librsvg", text)

    def test_artifacts_are_sha_qualified_and_hidden_files_follow_audit(self):
        text = workflow_text()
        for name in (
            "approved-identity-proofs-${{ github.sha }}",
            "verified-brand-kits-${{ github.sha }}",
            "github-pages-${{ github.sha }}",
            "verified-release-assets-${{ github.sha }}",
        ):
            self.assertIn(name, text)
        self.assertGreaterEqual(text.count("include-hidden-files: true"), 2)
        self.assertIn("python scripts/audit_publication_artifacts.py --kits dist --site site/out", text)

    def test_terminal_build_fails_unless_every_verifier_succeeds(self):
        block = job_block(workflow_text(), "build")
        self.assertIn("if: ${{ always() }}", block)
        for dependency in (
            "python-38-compatibility",
            "approved-identity-proofs",
            "verified-build",
        ):
            self.assertIn(dependency, block)
            self.assertIn("needs.%s.result" % dependency, block)
        self.assertIn("exit 1", block)

    def test_main_concurrency_and_pages_publisher_are_fail_closed(self):
        text = workflow_text()
        self.assertIn("github.ref == 'refs/heads/main'", text)
        self.assertIn("cancel-in-progress: ${{ github.ref == 'refs/heads/main' }}", text)
        block = job_block(text, "deploy-pages")
        self.assertIn("needs: [build, verified-build]", block)
        self.assertIn("github.event_name == 'push'", block)
        self.assertIn("github.event_name == 'workflow_dispatch'", block)
        self.assertIn("pages: write", block)
        self.assertIn("id-token: write", block)
        self.assertNotIn("actions/checkout", block)
        self.assertNotRegex(block, r"(?m)^\s+run:")
        self.assertIn("artifact_name: github-pages-${{ github.sha }}", block)

    def test_pull_requests_verify_but_cannot_publish(self):
        text = workflow_text()
        self.assertIn("permissions:\n  contents: read", text)
        for publisher in ("deploy-pages", "publish-release"):
            block = job_block(text, publisher)
            self.assertNotIn("pull_request", block)
        verified = job_block(text, "verified-build")
        self.assertIn("upload-pages-artifact", verified)
        self.assertIn("verified-release-assets-${{ github.sha }}", verified)

    def test_release_preflight_and_publisher_preserve_provenance(self):
        text = workflow_text()
        preflight = job_block(text, "release-preflight")
        publisher = job_block(text, "publish-release")
        for block in (preflight, publisher):
            self.assertIn("refs/tags/v", block)
            self.assertIn("SOURCE_COMMIT", block)
            self.assertIn("sha256sum --check", block)
        self.assertIn("git merge-base --is-ancestor", preflight)
        self.assertIn("python scripts/release_contract.py current", preflight)
        self.assertIn("contents: write", publisher)
        self.assertIn("needs: [build, release-preflight]", publisher)
        self.assertIn("gh release create", publisher)
        self.assertIn("--verify-tag", publisher)
        self.assertNotIn("actions/checkout", publisher)
        self.assertNotIn("python scripts/", publisher)


if __name__ == "__main__":
    unittest.main(verbosity=2)
