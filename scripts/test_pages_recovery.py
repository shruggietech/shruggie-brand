#!/usr/bin/env python3
"""Exercise qualified recovery provenance and hostile archive boundaries."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tarfile
import tempfile
import unittest
from unittest import mock
import zipfile

import recover_pages as recovery


SHA = "a" * 40
CONTROLLER = "b" * 40
REPO = "owner/project"
TAG = "v3.1.2"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fixture():
    run = {"id": 123, "repository": {"full_name": REPO},
           "head_repository": {"full_name": REPO}, "event": "push",
           "path": ".github/workflows/build.yml", "status": "completed",
           "head_branch": TAG, "head_sha": SHA}
    jobs = [{"name": name, "status": "completed", "conclusion": "success"}
            for name in recovery.REQUIRED_JOBS]
    jobs.append({"name": "deploy-pages", "status": "completed", "conclusion": "failure"})
    artifacts = [{"id": index, "name": prefix + SHA, "expired": False,
                  "digest": "sha256:" + "c" * 64, "size_in_bytes": 1,
                  "workflow_run": {"head_sha": SHA}}
                 for index, prefix in enumerate(("github-pages-", "verified-release-assets-"), 1)]
    release = {"id": 7, "tag_name": TAG, "draft": False, "body": "notes\n", "assets": []}
    return run, jobs, artifacts, release


def qualify(values=None):
    run, jobs, artifacts, release = values or fixture()
    return recovery.qualify_source(REPO, TAG, SHA, run, release, jobs, artifacts, CONTROLLER)


def candidate(root):
    files = root / "files"
    files.mkdir(parents=True)
    values = {"example.zip": b"qualified brand archive", "skill.skill": b"qualified compiler"}
    for name, value in values.items():
        (files / name).write_bytes(value)
    checksums = "".join(digest(value) + "  ./" + name + "\n" for name, value in values.items())
    (root / "SHA256SUMS").write_bytes(checksums.encode())
    (root / "SOURCE_COMMIT").write_text(SHA + "\n", encoding="utf-8")
    (files / "release-notes.md").write_text("notes\n", encoding="utf-8")
    identity = {"status": "release", "version": "3.1.2", "tag": TAG, "sourceRevision": SHA}
    publication = dict(identity, packages=[{"brand_slug": "example", "filename": "example.zip"}])
    (root / "PUBLICATION.json").write_text(json.dumps(publication), encoding="utf-8")
    (root / "SITE-DOCUMENTATION.json").write_text(json.dumps(identity), encoding="utf-8")
    receipt = qualify()
    receipt["release"]["assets"] = [{"name": name, "digest": "sha256:" + digest(value)}
                                       for name, value in values.items()]
    receipt["release"]["assets"].append({"name": "SHA256SUMS", "digest": "sha256:" + digest(checksums.encode())})
    return receipt, values


def pages_zip(path, files, extra=None):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as archive:
        for name, data in files.items():
            item = tarfile.TarInfo(name)
            item.size = len(data)
            archive.addfile(item, io.BytesIO(data))
        if extra is not None:
            archive.addfile(extra)
    data = buffer.getvalue()
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("artifact.tar", data)
    return data


class ProvenanceTests(unittest.TestCase):
    def test_failed_deployment_can_recover_only_qualified_content(self):
        receipt = qualify()
        self.assertEqual(receipt["source_sha"], SHA)
        self.assertEqual(receipt["controller_sha"], CONTROLLER)
        self.assertEqual(receipt["pages_artifact"]["name"], "github-pages-" + SHA)

    def test_rejects_wrong_repository_fork_event_workflow_status_tag_and_commit(self):
        mutations = [
            lambda run: run["repository"].update(full_name="other/project"),
            lambda run: run["head_repository"].update(full_name="fork/project"),
            lambda run: run.update(event="pull_request"),
            lambda run: run.update(path="untrusted.yml"),
            lambda run: run.update(status="in_progress"),
            lambda run: run.update(head_branch="main"),
            lambda run: run.update(head_sha=CONTROLLER),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                values = fixture()
                mutate(values[0])
                with self.assertRaises(ValueError):
                    qualify(values)

    def test_every_original_gate_is_required(self):
        for name in recovery.REQUIRED_JOBS:
            for replacement in (None, "failure", "skipped"):
                values = fixture()
                if replacement is None:
                    values[1][:] = [job for job in values[1] if job["name"] != name]
                else:
                    next(job for job in values[1] if job["name"] == name)["conclusion"] = replacement
                with self.subTest(gate=name, result=replacement), self.assertRaises(ValueError):
                    qualify(values)

    def test_rejects_expired_duplicate_wrong_source_or_unsigned_artifact(self):
        for change in ("expired", "duplicate", "source", "digest"):
            values = fixture()
            if change == "expired":
                values[2][0]["expired"] = True
            elif change == "duplicate":
                values[2].append(copy.deepcopy(values[2][0]))
            elif change == "source":
                values[2][0]["workflow_run"]["head_sha"] = CONTROLLER
            else:
                values[2][0]["digest"] = None
            with self.subTest(change=change), self.assertRaises(ValueError):
                qualify(values)

    def test_rejects_unpublished_or_mismatched_release(self):
        for change in ({"draft": True}, {"tag_name": "v3.1.1"}):
            values = fixture()
            values[3].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                qualify(values)

    def test_activity_counters_do_not_invalidate_content_qualification(self):
        values = fixture()
        values[3]["assets"] = [{"name": "distribution.zip", "digest": "sha256:" + "d" * 64,
                                "size": 12, "download_count": 0}]
        first = qualify(values)
        values[3]["assets"][0]["download_count"] = 200
        values[2][0]["updated_at"] = "later retention bookkeeping"
        self.assertEqual(qualify(values), first)


class ArchiveTests(unittest.TestCase):
    def test_extract_rejects_traversal_collisions_devices_streams_and_links(self):
        for names in (["../escape"], ["/absolute"], ["C:/escape"], ["folder\\escape"],
                      ["folder/name:stream"], ["CON"], ["same", "./same"], ["Same", "same"]):
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                archive = root / "input.zip"
                with zipfile.ZipFile(archive, "w") as zipped:
                    for name in names:
                        item = zipfile.ZipInfo("placeholder")
                        item.filename = name  # Preserve hostile separators on Windows too.
                        zipped.writestr(item, "untrusted")
                with self.subTest(names=names), self.assertRaises(ValueError):
                    recovery.extract_zip(archive, root / "output")
                self.assertFalse((root.parent / "escape").exists())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            item = zipfile.ZipInfo("linked")
            item.create_system = 3
            item.external_attr = (stat.S_IFLNK | 0o777) << 16
            with zipfile.ZipFile(root / "link.zip", "w") as archive:
                archive.writestr(item, "../outside")
            with self.assertRaises(ValueError):
                recovery.extract_zip(root / "link.zip", root / "output")

    def test_official_digests_notes_source_and_records_are_bound(self):
        for change in ("source", "official", "notes", "publication", "bytes", "checksums"):
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                receipt, _ = candidate(root)
                if change == "source":
                    (root / "SOURCE_COMMIT").write_text(CONTROLLER, encoding="utf-8")
                elif change == "official":
                    receipt["release"]["assets"][0]["digest"] = "sha256:" + "0" * 64
                elif change == "notes":
                    receipt["release"]["body"] = "replaced notes"
                elif change == "publication":
                    (root / "PUBLICATION.json").write_text("{}", encoding="utf-8")
                elif change == "bytes":
                    (root / "files/example.zip").write_bytes(b"replacement")
                else:
                    (root / "SHA256SUMS").write_text("not a checksum", encoding="utf-8")
                with self.subTest(change=change), self.assertRaises(ValueError):
                    recovery.candidate_receipt(root, receipt)

    def test_payload_is_preserved_and_release_bytes_are_checked(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipt, values = candidate(root / "candidate")
            binding = recovery.candidate_receipt(root / "candidate", receipt)
            payload = pages_zip(root / "pages.zip", {
                "./docs/publication.json": binding["documentation"],
                "./example/downloads/example.zip": values["example.zip"],
                "./index.html": b"qualified homepage",
            })
            result = recovery.extract_pages(root / "pages.zip", root / "output", receipt, binding)
            self.assertEqual((root / "output/artifact.tar").read_bytes(), payload)
            self.assertEqual(result["tar_sha256"], digest(payload))
            bad = dict(binding, packages={"example/downloads/example.zip": "0" * 64})
            with self.assertRaises(ValueError):
                recovery.extract_pages(root / "pages.zip", root / "bad", receipt, bad)

    def test_pages_rejects_links_duplicates_wrong_documents_and_platform_overflow(self):
        for kind in ("symlink", "hardlink", "device", "traversal", "duplicate", "docs", "size"):
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                receipt, values = candidate(root / "candidate")
                binding = recovery.candidate_receipt(root / "candidate", receipt)
                docs = b"{}" if kind == "docs" else binding["documentation"]
                files = {"docs/publication.json": docs, "example/downloads/example.zip": values["example.zip"]}
                extra = None
                if kind in ("symlink", "hardlink", "device"):
                    extra = tarfile.TarInfo("bad")
                    extra.type = {"symlink": tarfile.SYMTYPE, "hardlink": tarfile.LNKTYPE, "device": tarfile.CHRTYPE}[kind]
                    extra.linkname = "../outside"
                if kind == "traversal":
                    files["../outside"] = b"escape"
                if kind == "duplicate":
                    files["./docs/publication.json"] = docs
                pages_zip(root / "pages.zip", files, extra)
                with self.subTest(kind=kind), mock.patch.object(recovery, "MAX_SITE_BYTES", 1 if kind == "size" else 2**30):
                    with self.assertRaises(ValueError):
                        recovery.extract_pages(root / "pages.zip", root / "output", receipt, binding)

    def test_tampered_download_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "download.zip"
            path.write_bytes(b"tampered")
            with self.assertRaises(ValueError):
                recovery.verify_download(path, {"digest": "sha256:" + "0" * 64, "size_in_bytes": 8})

    def test_child_tools_are_hidden_noninteractive_and_fail_closed(self):
        result = subprocess.CompletedProcess(["gh"], 0, stdout=b"result", stderr=b"")
        with mock.patch.object(recovery.os, "name", "nt"), mock.patch.object(subprocess, "CREATE_NO_WINDOW", 0x08000000, create=True), mock.patch.object(subprocess, "run", return_value=result) as invoke:
            self.assertEqual(recovery.run(["gh", "version"]), b"result")
            kwargs = invoke.call_args.kwargs
            self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
            self.assertEqual(kwargs["creationflags"], 0x08000000)
            self.assertEqual(kwargs["env"]["GIT_TERMINAL_PROMPT"], "0")
            self.assertEqual(kwargs["env"]["GH_PROMPT_DISABLED"], "1")
            self.assertNotIn("GIT_PAGER", kwargs["env"])
            self.assertFalse(kwargs.get("shell", False))


class UstarTests(unittest.TestCase):
    LONG_NAME = "./docs/" + "nested/" * 16 + "guide.html"

    def write_archive(self, path, change=None):
        rows = [("./", None), ("./empty/", None), (self.LONG_NAME, b"qualified page"), ("./index.html", b"homepage")]
        if change == "missing-directory":
            rows.pop(1)
        elif change == "extra":
            rows.append(("./extra", b"unexpected"))
        elif change == "order":
            rows.reverse()
        elif change == "bytes":
            rows[-1] = ("./index.html", b"replaced")
        elif change == "name":
            rows[-1] = ("./renamed.html", b"homepage")
        elif change == "unrepresentable":
            rows.append(("x" * 101, b"cannot fit USTAR name"))
        with tarfile.open(str(path), "w", format=tarfile.GNU_FORMAT) as archive:
            for name, data in rows:
                item = tarfile.TarInfo(name)
                item.type = tarfile.DIRTYPE if data is None else tarfile.REGTYPE
                item.size = 0 if data is None else len(data)
                item.mode = 0o755 if data is None else 0o664
                item.uid, item.gid = 1001, 1001
                item.uname, item.gname = "runner", "runner"
                item.mtime = 1794270000
                if change == "metadata":
                    item.uid = 1002
                archive.addfile(item, None if data is None else io.BytesIO(data))

    def test_long_names_reencode_without_changing_members_or_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, target = root / "original.tar", root / "ustar.tar"
            self.write_archive(source)
            before = source.read_bytes()
            self.assertIn(b"././@LongLink", before)
            result = recovery.repack_ustar(source, target, root)
            self.assertEqual(source.read_bytes(), before)
            self.assertNotEqual(target.read_bytes(), before)
            self.assertEqual(target.read_bytes()[257:265], b"ustar\x0000")
            self.assertEqual(result["original_tar_sha256"], digest(before))
            self.assertEqual(result["tar_sha256"], digest(target.read_bytes()))
            self.assertEqual(json.loads((root / "original-members.json").read_text()),
                             json.loads((root / "ustar-members.json").read_text()))
            self.assertEqual(recovery.archive_manifest(source), recovery.archive_manifest(target, require_ustar=True))

    def test_complete_equivalence_rejects_changed_bytes_paths_directories_order_or_metadata(self):
        for change in ("bytes", "name", "missing-directory", "extra", "order", "metadata"):
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                source, altered, output = root / "source.tar", root / "altered.tar", root / "output.tar"
                self.write_archive(source)
                self.write_archive(altered, change)
                recovery.repack_ustar(altered, output)
                with self.subTest(change=change), self.assertRaises(ValueError):
                    recovery.validate_ustar_transport(source, output)

    def test_repack_rejects_unrepresentable_names_and_overwriting_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.tar"
            self.write_archive(source, "unrepresentable")
            before = source.read_bytes()
            with self.assertRaises(ValueError):
                recovery.repack_ustar(source, root / "output.tar")
            with self.assertRaises(ValueError):
                recovery.repack_ustar(source, source)
            self.assertEqual(source.read_bytes(), before)

    def test_repack_rejects_unsafe_members_and_non_ustar_validation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.tar"
            self.write_archive(source)
            with self.assertRaises(ValueError):
                recovery.validate_ustar_transport(source, source)
            for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.CHRTYPE):
                malicious = root / (kind.decode() + ".tar")
                with tarfile.open(str(malicious), "w") as archive:
                    item = tarfile.TarInfo("linked")
                    item.type, item.linkname = kind, "../outside"
                    archive.addfile(item)
                with self.assertRaises(ValueError):
                    recovery.repack_ustar(malicious, root / (kind.decode() + "-output.tar"))

    def test_archive_cli_is_read_only_without_controller_or_staging_arguments(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, target = root / "source.tar", root / "ustar.tar"
            self.write_archive(source)
            recovery.repack_ustar(source, target)
            with mock.patch.object(recovery, "controller_sha", side_effect=AssertionError("controller lookup forbidden")), \
                    mock.patch.object(recovery, "GitHub", side_effect=AssertionError("network access forbidden")), \
                    mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "pull_request"}):
                with mock.patch.object(recovery.sys, "argv", ["recover_pages.py", "verify-archive", "--archive", str(target)]), \
                        mock.patch.object(recovery.sys, "stdout", new_callable=io.StringIO) as output:
                    self.assertEqual(recovery.main(), 0)
                    report = json.loads(output.getvalue())
                    self.assertEqual(report["tar_sha256"], digest(target.read_bytes()))
                    self.assertEqual(report["files"], 2)
                    self.assertEqual(report["directories"], 2)
                with mock.patch.object(recovery.sys, "argv", ["recover_pages.py", "verify-archive", "--archive", str(source)]):
                    with self.assertRaises(ValueError):
                        recovery.main()


if __name__ == "__main__":
    unittest.main()
