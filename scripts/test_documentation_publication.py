#!/usr/bin/env python3
"""Mutation tests for exact main-manual publication binding."""

import copy
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from documentation_publication import build_record, verify_record
from documentation_render import render_index, render_page


class DocumentationPublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.refs = self.root / "references"
        self.docs = self.root / "docs"
        self.assets = self.root / "assets"
        for path in (self.refs, self.docs, self.assets):
            path.mkdir()
        (self.refs / "documentation-contract.json").write_text(json.dumps({"manual_pages": [
            {"slug": "guide", "source": "guide.md", "title": "Guide", "description": "Current guidance"}
        ]}) + "\n", encoding="utf-8")
        (self.refs / "guide.md").write_text("# Guide\nCurrent instructions.\n", encoding="utf-8")
        self.publication = {
            "status": "candidate", "version": "2.2.0", "tag": "v2.2.0", "sourceRevision": "a" * 40,
            "releaseUrl": "https://github.com/ShruggieTech/shruggie-brand/releases/tag/v2.2.0",
            "skillUrl": "https://github.com/ShruggieTech/shruggie-brand/releases/download/v2.2.0/shruggie-brandbuilder-2.2.0.skill",
        }
        (self.docs / "guide.mdx").write_bytes(render_page((self.refs / "guide.md").read_text(encoding="utf-8"), "Current guidance", self.publication).encode("utf-8"))
        (self.docs / "index.mdx").write_bytes(render_index(self.publication).encode("utf-8"))
        self.record_path = self.root / "documentation.json"
        self.exported = self.root / "exported.json"
        self.write_record()
        self.write_archives()

    def write_record(self):
        self.record = build_record(self.refs, self.docs, self.publication)
        data = json.dumps(self.record).encode("utf-8")
        self.record_path.write_bytes(data)
        self.exported.write_bytes(data)

    def write_archives(self, replacement=None):
        version = self.publication["version"]
        for filename in ("shruggie-brandbuilder-%s.skill" % version, "shruggie-brandbuilder-%s-portable.zip" % version):
            with zipfile.ZipFile(self.assets / filename, "w") as archive:
                archive.writestr("SOURCE_REVISION", self.publication["sourceRevision"] + "\n")
                archive.writestr("references/documentation-contract.json", (self.refs / "documentation-contract.json").read_bytes())
                archive.writestr("references/guide.md", replacement if replacement is not None else (self.refs / "guide.md").read_bytes())

    def verify(self, **kwargs):
        return verify_record(self.record_path, self.refs, self.docs, self.publication,
                             exported_record=self.exported, release_dir=self.assets, **kwargs)

    def test_exact_candidate_and_release(self):
        self.assertEqual("candidate", self.verify()["status"])
        with self.assertRaisesRegex(ValueError, "requires exact release status"):
            self.verify(require_release=True)
        self.publication["status"] = "release"
        (self.docs / "guide.mdx").write_bytes(render_page((self.refs / "guide.md").read_text(encoding="utf-8"), "Current guidance", self.publication).encode("utf-8"))
        (self.docs / "index.mdx").write_bytes(render_index(self.publication).encode("utf-8"))
        self.write_record()
        self.assertEqual("release", self.verify(require_release=True)["status"])

    def test_documentation_only_patch_release_has_new_identity(self):
        self.publication.update({
            "status": "release", "version": "2.2.1", "tag": "v2.2.1",
            "releaseUrl": "https://github.com/ShruggieTech/shruggie-brand/releases/tag/v2.2.1",
            "skillUrl": "https://github.com/ShruggieTech/shruggie-brand/releases/download/v2.2.1/shruggie-brandbuilder-2.2.1.skill",
        })
        (self.refs / "guide.md").write_text("# Guide\nClarified instructions.\n", encoding="utf-8")
        (self.docs / "guide.mdx").write_bytes(render_page((self.refs / "guide.md").read_text(encoding="utf-8"), "Current guidance", self.publication).encode("utf-8"))
        (self.docs / "index.mdx").write_bytes(render_index(self.publication).encode("utf-8"))
        self.write_record()
        self.write_archives()
        self.assertEqual("2.2.1", self.verify(require_release=True)["version"])

    def test_record_identity_and_inventory_mutations_fail(self):
        for field, value in (("version", "2.1.0"), ("sourceRevision", "b" * 40),
                             ("skillUrl", "https://github.com/ShruggieTech/shruggie-brand/releases/latest"),
                             ("catalogSha256", "0" * 64)):
            with self.subTest(field=field):
                bad = copy.deepcopy(self.record)
                bad[field] = value
                self.record_path.write_text(json.dumps(bad), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "record disagrees"):
                    self.verify()
        self.write_record()
        bad = copy.deepcopy(self.record)
        bad["pages"].pop()
        self.record_path.write_text(json.dumps(bad), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "record disagrees"):
            self.verify()

    def test_source_page_export_and_archive_mutations_fail(self):
        (self.refs / "guide.md").write_text("Stale source\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "deterministic source transform"):
            self.verify()
        (self.refs / "guide.md").write_text("# Guide\nCurrent instructions.\n", encoding="utf-8")
        (self.docs / "guide.mdx").write_text("Stale page\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "deterministic source transform"):
            self.verify()
        (self.docs / "guide.mdx").write_bytes(render_page((self.refs / "guide.md").read_text(encoding="utf-8"), "Current guidance", self.publication).encode("utf-8"))
        self.exported.write_bytes(b"{}")
        with self.assertRaisesRegex(ValueError, "exported"):
            self.verify()
        self.exported.write_bytes(self.record_path.read_bytes())
        self.write_archives(b"stale packaged reference")
        with self.assertRaisesRegex(ValueError, "packaged documentation reference differs"):
            self.verify()

    def test_unsafe_and_duplicate_catalog_fail(self):
        catalog = self.refs / "documentation-contract.json"
        catalog.write_text(json.dumps({"manual_pages": [{"slug": "guide", "source": "../secret.md"}]}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unsafe documentation source"):
            build_record(self.refs, self.docs, self.publication)
        catalog.write_text(json.dumps({"manual_pages": [{"slug": "guide", "source": "guide.md"},
                                                          {"slug": "guide", "source": "guide.md"}]}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate documentation"):
            build_record(self.refs, self.docs, self.publication)


if __name__ == "__main__":
    unittest.main()
