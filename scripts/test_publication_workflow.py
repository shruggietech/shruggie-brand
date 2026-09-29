#!/usr/bin/env python3
"""Regression tests for the verified publication workflow and artifact boundary."""

from __future__ import annotations

import os
import hashlib
import json
import re
import shutil
import tempfile
import unittest
from unittest import mock
from pathlib import Path

import audit_publication_artifacts


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "build.yml"
PRODUCTION = (
    "covarity",
    "cueson",
    "dancewithme865",
    "eso-weave",
    "fragcap",
    "glitchpad",
    "go-schedule",
    "i-heart-pr-tours",
    "local-companion",
    "scruggs-tire-alignment",
    "shruggietech",
)
EXPECTED_ACTIONS = {
    "actions/checkout": "3d3c42e5aac5ba805825da76410c181273ba90b1",
    "actions/setup-python": "5fda3b95a4ea91299a34e894583c3862153e4b97",
    "actions/setup-node": "820762786026740c76f36085b0efc47a31fe5020",
    "actions/upload-artifact": "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
    "actions/download-artifact": "3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c",
    "actions/upload-pages-artifact": "fc324d3547104276b827a68afc52ff2a11cc49c9",
    "actions/deploy-pages": "368f82528645a54fb793d4d04e342629a3f51346",
    "pnpm/action-setup": "ea17c68df8912ef543352723c149a84f56e3d413",
}
EXPECTED_ACTION_VERSIONS = {
    "actions/checkout": "v7.0.1",
    "actions/setup-python": "v7.0.0",
    "actions/setup-node": "v7.0.0",
    "actions/upload-artifact": "v7.0.0",
    "actions/download-artifact": "v8.0.1",
    "actions/upload-pages-artifact": "v5.0.0",
    "actions/deploy-pages": "v5.0.0",
    "pnpm/action-setup": "v6.1.0",
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


def create_semantic_candidate(root: Path) -> tuple[Path, Path, Path, Path]:
    slug = "covarity"
    kits = root / "dist"
    site = root / "site" / "out"
    generated = root / "site" / "generated"
    release = root / "release"
    kit = kits / slug
    public = site / slug
    version = "2.6.0"
    package = {"id": "covarity-brand-1.0.0-bb2.6.0", "filename": "covarity-brand-1.0.0-bb2.6.0.zip",
               "brand_slug": slug, "brand_version": "1.0.0", "brandbuilder_version": version}
    brand = {"slug": slug, "version": "1.0.0", "canon": "1.6.0"}
    versions = {"brand_version": "1.0.0", "compiler_version": version}
    bundle = {"package": package, "versions": versions}
    consumer = {"brand": {"slug": slug}, "bundle": bundle, "versions": versions}
    facts = {"brand": consumer["brand"], "bundle": bundle, "versions": versions}
    portal = {"brand": {"slug": slug}, "implementation": facts, "topics": []}
    conformance = {"versions": versions, "source_revision": "a" * 40}

    def write_json(path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) + "\n", encoding="utf-8")

    def write_file(path: Path, value: bytes = b"file") -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value)

    write_json(kit / "brand.json", brand)
    write_json(kit / "manifest.json", {"version": "1.0.0", "canon": "1.6.0", "files": [{"path": "brand.json"}]})
    write_json(kit / "enforcement" / "bundle.json", bundle)
    write_json(kit / "enforcement" / "consumer-contract.json", consumer)
    write_json(kit / "enforcement" / "documentation-facts.json", facts)
    (public / "facts").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(kit / "enforcement" / "documentation-facts.json",
                    public / "facts" / "documentation.json")
    write_json(kit / "guidelines" / "portal.json", portal)
    write_json(kit / "conformance" / "manifest.json", conformance)
    write_file(kit / "conformance" / "browser" / "specimen.html", b"<html>specimen</html>")
    write_json(kit / "nextjs" / "registry" / "registry.json", {"items": [{"name": "theme"}]})
    write_json(kit / "nextjs" / "registry" / "theme.json", {"name": "theme"})
    for name in ("brand-guide.pdf", "guidelines/index.html", "wordpress/covarity-stbb-theme.zip", "logos/mark.svg",
                 "favicons/favicon.svg", "icons/.iconkit-generated.json", "specimens/specimen.svg"):
        write_file(kit / name, name.encode("utf-8"))
    shutil.copytree(kit / "nextjs" / "registry", public / "brand" / "r")
    downloads = public / "downloads" / "files"
    for name, source in audit_publication_artifacts._download_sources(kit, brand).items():
        destination = downloads / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    fixtures = site / "conformance-fixtures" / slug
    fixtures.mkdir(parents=True)
    shutil.copyfile(kit / "conformance" / "manifest.json", fixtures / "manifest.json")
    shutil.copyfile(kit / "conformance" / "browser" / "specimen.html", fixtures / "specimen.html")
    write_file(public / "downloads" / package["filename"], b"PK\x03\x04archive")
    write_json(generated / "brands.json", [{"slug": slug, "version": "1.0.0", "packageId": package["id"],
                                            "kitArchiveFilename": package["filename"], "brandbuilderVersion": version,
                                            "kitArchive": "/covarity/downloads/" + package["filename"]}])
    write_json(generated / "guidelines.json", [portal])
    write_json(generated / "conformance.json", [{"slug": slug, "brandVersion": "1.0.0", "versions": versions,
                                                 "sourceRevision": "a" * 40}])
    write_json(generated / "publication.json", {"version": version, "packages": [package],
                                                "sourceRevision": "a" * 40})
    write_json(generated / "documentation-publication.json", {"version": version,
                                                              "sourceRevision": "a" * 40})
    write_json(site / "docs" / "publication.json", {"version": version,
                                                   "sourceRevision": "a" * 40})
    write_file(release / package["filename"], b"PK\x03\x04archive")
    write_file(release / "shruggie-brandbuilder-2.6.0.skill", b"skill")
    write_file(release / "release-notes.md", b"notes")
    write_file(generated / "docs" / "index.mdx", b"# Documentation\n")
    staged = root / "staged"
    shutil.copytree(release, staged / "files")
    for name, source in (("PUBLICATION.json", generated / "publication.json"),
                         ("DOCUMENTATION.json", generated / "documentation-publication.json"),
                         ("SITE-DOCUMENTATION.json", site / "docs" / "publication.json")):
        shutil.copyfile(source, staged / name)
    shutil.copytree(generated / "docs", staged / "docs")
    sums = sorted((hashlib.sha256(path.read_bytes()).hexdigest(), path.name)
                  for path in (staged / "files").iterdir() if path.suffix in {".skill", ".zip"})
    (staged / "SHA256SUMS").write_text("".join("%s  ./%s\n" % pair for pair in sums), encoding="utf-8")
    (staged / "SOURCE_COMMIT").write_text("a" * 40 + "\n", encoding="utf-8")
    return kits, site, release, staged


class PublicationArtifactAuditTests(unittest.TestCase):
    def test_semantic_candidate_accepts_real_optional_absence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site, release, staged = create_semantic_candidate(root)
            result = audit_publication_artifacts.audit_semantics(
                root, kits, site, release, staged, ("covarity",), ("covarity",), "a" * 40)
            self.assertEqual(1, result["brands"])
            self.assertGreater(result["public_files"], 0)

    def test_semantic_candidate_rejects_missing_registry_dependency_and_download(self):
        for relative in ("covarity/brand/r/theme.json", "covarity/downloads/files/logos/mark.svg"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                kits, site, _, _ = create_semantic_candidate(root)
                (site / relative).unlink()
                with self.assertRaisesRegex(ValueError, "inventory or bytes differ"):
                    audit_publication_artifacts.audit_semantics(
                        root, kits, site, production=("covarity",), release_authorized=("covarity",))

    def test_semantic_candidate_rejects_changed_download_and_version(self):
        for relative in ("logos/mark.svg", "wordpress/covarity-stbb-theme.zip"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                kits, site, _, _ = create_semantic_candidate(root)
                (site / "covarity" / "downloads" / "files" / relative).write_bytes(b"changed")
                with self.assertRaisesRegex(ValueError, "download inventory or bytes differ"):
                    audit_publication_artifacts.audit_semantics(
                        root, kits, site, production=("covarity",), release_authorized=("covarity",))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site, _, _ = create_semantic_candidate(root)
            record = root / "site" / "generated" / "publication.json"
            payload = json.loads(record.read_text(encoding="utf-8"))
            payload["version"] = "9.0.0"
            record.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "publication package inventory or version"):
                audit_publication_artifacts.audit_semantics(
                    root, kits, site, production=("covarity",), release_authorized=("covarity",))

    def test_semantic_candidate_rejects_facts_drift_and_staged_checksum(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site, _, _ = create_semantic_candidate(root)
            public_facts = site / "covarity" / "facts" / "documentation.json"
            public_facts.write_text('{"schema_version": 9}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "public documentation facts differ"):
                audit_publication_artifacts.audit_semantics(
                    root, kits, site, production=("covarity",), release_authorized=("covarity",))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site, _, _ = create_semantic_candidate(root)
            path = kits / "covarity" / "enforcement" / "documentation-facts.json"
            facts = json.loads(path.read_text(encoding="utf-8"))
            facts["versions"]["compiler_version"] = "9.0.0"
            path.write_text(json.dumps(facts), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "documentation facts differ"):
                audit_publication_artifacts.audit_semantics(
                    root, kits, site, production=("covarity",), release_authorized=("covarity",))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site, release, staged = create_semantic_candidate(root)
            (staged / "SHA256SUMS").write_text("0" * 64 + "  ./covarity-brand-1.0.0-bb2.6.0.zip\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "SHA256SUMS"):
                audit_publication_artifacts.audit_semantics(
                    root, kits, site, release, staged, ("covarity",), ("covarity",), "a" * 40)

    def test_semantic_candidate_rejects_wrong_source_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site, release, staged = create_semantic_candidate(root)
            (staged / "SOURCE_COMMIT").write_text("b" * 40 + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "staged source revision"):
                audit_publication_artifacts.audit_semantics(
                    root, kits, site, release, staged, ("covarity",), ("covarity",), "a" * 40)

    def test_semantic_candidate_checks_hosted_archive_without_release_asset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site, _, _ = create_semantic_candidate(root)
            publication = root / "site" / "generated" / "publication.json"
            payload = json.loads(publication.read_text(encoding="utf-8"))
            payload["packages"] = []
            publication.write_text(json.dumps(payload), encoding="utf-8")
            archive = site / "covarity" / "downloads" / "covarity-brand-1.0.0-bb2.6.0.zip"

            def synthetic_archive(_source, destination, *, root):
                destination.write_bytes(b"PK\x03\x04archive")

            with mock.patch.object(audit_publication_artifacts, "write_brand_archive", side_effect=synthetic_archive):
                audit_publication_artifacts.audit_semantics(
                    root, kits, site, production=("covarity",), release_authorized=())
                archive.write_bytes(b"PK\x03\x04corrupt")
                with self.assertRaisesRegex(ValueError, "hosted archive differs from certified kit"):
                    audit_publication_artifacts.audit_semantics(
                        root, kits, site, production=("covarity",), release_authorized=())

    def test_semantic_candidate_rejects_unsafe_optional_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site, _, _ = create_semantic_candidate(root)
            path = kits / "covarity" / "brand.json"
            brand = json.loads(path.read_text(encoding="utf-8"))
            brand["custom_assets"] = [{"approval": {"status": "approved", "publication_eligible": True},
                                       "source": {"path": "../escape.svg"}}]
            path.write_text(json.dumps(brand), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsafe artifact reference"):
                audit_publication_artifacts.audit_semantics(
                    root, kits, site, production=("covarity",), release_authorized=("covarity",))

    def test_valid_publication_trees_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kits, site = create_publication_trees(root)
            result = audit_publication_artifacts.audit(root, kits, site)
            self.assertEqual(len(PRODUCTION), result["kit_markers"])
            self.assertEqual(len(PRODUCTION), result["site_markers"])

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
            self.assertEqual(EXPECTED_ACTION_VERSIONS[action], comment, action)

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
        minimum_python = job_block(text, "python-38-compatibility")
        self.assertIn("python skill/templates/test_pipeline.py", minimum_python)
        self.assertNotIn("setup-node", minimum_python)
        self.assertNotIn("@resvg/resvg-js", minimum_python)
        self.assertNotIn("rsvg-convert", text)
        self.assertNotIn("librsvg", text)

    def test_verified_build_installs_both_playwright_browser_revisions(self):
        block = job_block(workflow_text(), "verified-build")
        self.assertIn("PLAYWRIGHT_SKIP_BROWSER_GC: \"1\"", block)
        self.assertIn("python -m playwright install chromium --with-deps", block)
        self.assertIn("pnpm --dir site exec playwright install chromium --with-deps", block)
        self.assertLess(block.index("python -m playwright install chromium --with-deps"),
                        block.index("pnpm --dir site exec playwright install chromium --with-deps"))

    def test_proof_bound_contracts_run_alongside_kit_builds(self):
        text = workflow_text()
        contracts = job_block(text, "contract-tests")
        verified = job_block(text, "verified-build")
        self.assertIn("needs: approved-identity-proofs", contracts)
        self.assertIn("approved-identity-proofs-${{ github.sha }}", contracts)
        self.assertIn("GP_APPROVED_PROOF_ROOT=\"$GITHUB_WORKSPACE/approved-identity-proofs\" python skill/templates/test_pipeline.py", contracts)
        self.assertIn("python scripts/test_publication_workflow.py", contracts)
        self.assertNotIn("Test geometry and publication contracts", verified)

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

    def test_verified_artifact_contains_every_production_kit(self):
        text = workflow_text()
        upload = text.split("name: verified-brand-kits-${{ github.sha }}", 1)[1].split(
            "if-no-files-found:", 1)[0]
        for slug in PRODUCTION:
            with self.subTest(slug=slug):
                self.assertIn("dist/%s/" % slug, upload)
        self.assertIn("--exclude scruggs-tire-alignment --exclude dancewithme865", text)
        self.assertIn("scripts/build_all.py scruggs-tire-alignment dancewithme865", text)

    def test_terminal_build_fails_unless_every_verifier_succeeds(self):
        block = job_block(workflow_text(), "build")
        self.assertIn("if: ${{ always() }}", block)
        for dependency in (
            "python-38-compatibility",
            "approved-identity-proofs",
            "contract-tests",
            "verified-build",
        ):
            self.assertIn(dependency, block)
            self.assertIn("needs.%s.result" % dependency, block)
        self.assertIn("exit 1", block)

    def test_main_concurrency_and_tag_only_pages_publisher_are_fail_closed(self):
        text = workflow_text()
        self.assertIn("github.ref == 'refs/heads/main'", text)
        self.assertIn("cancel-in-progress: ${{ github.ref == 'refs/heads/main' }}", text)
        block = job_block(text, "deploy-pages")
        self.assertIn("needs: [build, verified-build, publish-release]", block)
        self.assertIn("needs.publish-release.result == 'success'", block)
        self.assertIn("github.event_name == 'push'", block)
        self.assertIn("startsWith(github.ref, 'refs/tags/v')", block)
        self.assertNotIn("github.event_name == 'workflow_dispatch'", block)
        self.assertNotIn("github.ref == 'refs/heads/main'", block)
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
        self.assertIn("GH_REPO: ${{ github.repository }}", publisher)
        self.assertIn("gh release create", publisher)
        self.assertIn('"$CANDIDATE/SHA256SUMS"', publisher)
        self.assertIn("sha256sum -- ./*.skill ./*.zip", text)
        self.assertNotIn("sha256sum -- ./* |", text)
        self.assertIn("--verify-tag", publisher)
        self.assertNotIn("actions/checkout", publisher)
        self.assertNotIn("python scripts/", publisher)


if __name__ == "__main__":
    unittest.main(verbosity=2)
