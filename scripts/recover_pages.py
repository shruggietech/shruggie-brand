#!/usr/bin/env python3
"""Transport a published tag's qualified Pages TAR into a fresh controller run."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
MAX_SITE_BYTES = 2**30
MAX_ARCHIVE_BYTES = 2 * MAX_SITE_BYTES
REQUIRED_JOBS = (
    "python-38-compatibility", "approved-identity-proofs", "contract-tests",
    "verified-build", "build", "release-preflight", "publish-release",
)
SHA = re.compile(r"[a-f0-9]{40}\Z")
DIGEST = re.compile(r"sha256:[a-f0-9]{64}\Z")
TAG = re.compile(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
RESERVED = {"CON", "PRN", "AUX", "NUL"} | {prefix + str(number) for prefix in ("COM", "LPT") for number in range(1, 10)}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def run(command, output=None, cwd=ROOT):
    environment = dict(os.environ, GIT_TERMINAL_PROMPT="0", GH_PROMPT_DISABLED="1")
    for name in ("GIT_PAGER", "PAGER"):
        environment.pop(name, None)
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    result = subprocess.run(command, cwd=str(cwd), env=environment, stdin=subprocess.DEVNULL,
                            stdout=output if output is not None else subprocess.PIPE,
                            stderr=subprocess.PIPE, creationflags=flags, timeout=300, check=False)
    if result.returncode:
        raise RuntimeError("%s failed: %s" % (command[0], result.stderr.decode("utf-8", "replace")[-2000:]))
    return result.stdout


class GitHub:
    def __init__(self, repository):
        require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) is not None, "invalid repository")
        self.repository = repository
        self.base = "repos/" + repository

    def get(self, path):
        return json.loads(run(["gh", "api", self.base + "/" + path]))

    def collection(self, path, key):
        pages = json.loads(run(["gh", "api", "--paginate", "--slurp", self.base + "/" + path]))
        return [item for page in pages for item in (page[key] if key else page)]

    def download(self, artifact, target):
        with target.open("wb") as output:
            run(["gh", "api", self.base + "/actions/artifacts/%d/zip" % artifact["id"]], output=output)
        verify_download(target, artifact)


def file_digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def positive_id(value):
    require(type(value) is int and value > 0, "invalid resource ID")
    return value


def qualify_source(repository, tag, commit, source_run, release, jobs, artifacts, controller_sha):
    require(TAG.fullmatch(tag) is not None, "invalid release tag")
    require(SHA.fullmatch(commit or "") is not None and SHA.fullmatch(controller_sha or "") is not None, "invalid source/controller SHA")
    for key in ("repository", "head_repository"):
        require((source_run.get(key) or {}).get("full_name", "").lower() == repository.lower(), "source repository/fork mismatch")
    require(source_run.get("event") == "push" and source_run.get("head_branch") == tag, "source is not the requested tag push")
    require(source_run.get("head_sha") == commit, "tag/source revision mismatch")
    require(source_run.get("path") == ".github/workflows/build.yml" and source_run.get("status") == "completed", "source Build run is not complete")
    for name in REQUIRED_JOBS:
        matching = [job for job in jobs if job.get("name") == name]
        require(len(matching) == 1 and matching[0].get("status") == "completed" and matching[0].get("conclusion") == "success", "source gate did not pass: " + name)
    require(release.get("tag_name") == tag and release.get("draft") is False, "matching published release is required")
    require(isinstance(release.get("body"), str), "published release notes are missing")
    selected = []
    for prefix in ("github-pages-", "verified-release-assets-"):
        matching = [item for item in artifacts if item.get("name") == prefix + commit]
        require(len(matching) == 1, "missing or ambiguous source artifact: " + prefix)
        artifact = matching[0]
        require(artifact.get("expired") is False, "source artifact expired")
        require(DIGEST.fullmatch(artifact.get("digest") or "") is not None, "artifact digest is missing")
        require((artifact.get("workflow_run") or {}).get("head_sha") == commit, "artifact source mismatch")
        positive_id(artifact.get("id"))
        selected.append({key: artifact[key] for key in ("id", "name", "expired", "digest", "size_in_bytes")})
    published = {key: release[key] for key in ("id", "tag_name", "draft", "body")}
    published["assets"] = [{key: asset.get(key) for key in ("name", "digest", "size")} for asset in release["assets"]]
    return {"repository": repository, "tag": tag, "version": tag[1:], "source_sha": commit,
            "controller_sha": controller_sha, "run_id": positive_id(source_run.get("id")),
            "release": published, "pages_artifact": selected[0], "candidate_artifact": selected[1]}


def resolve_source(client, tag, run_id, controller_sha):
    require(TAG.fullmatch(tag) is not None, "invalid release tag")
    positive_id(run_id)
    commit = client.get("commits/" + tag)["sha"]
    release = client.get("releases/tags/" + tag)
    release["assets"] = client.collection("releases/%d/assets?per_page=100" % positive_id(release["id"]), None)
    source_run = client.get("actions/runs/%d" % run_id)
    require(source_run.get("id") == run_id, "source run ID mismatch")
    return qualify_source(client.repository, tag, commit, source_run, release,
                          client.collection("actions/runs/%d/jobs?filter=latest&per_page=100" % run_id, "jobs"),
                          client.collection("actions/runs/%d/artifacts?per_page=100" % run_id, "artifacts"), controller_sha)


def verify_download(path, artifact):
    require(DIGEST.fullmatch(artifact.get("digest") or "") is not None, "missing download digest")
    require(path.stat().st_size == artifact.get("size_in_bytes"), "download size mismatch")
    require("sha256:" + file_digest(path) == artifact["digest"], "download digest mismatch")


def safe_name(name):
    require(bool(name) and not name.startswith(("/", "\\")) and "\\" not in name, "unsafe archive path")
    require(not any(ord(character) < 32 for character in name), "control character in archive path")
    parts = PurePosixPath(name).parts
    require(bool(parts), "empty archive path")
    require(".." not in parts, "unsafe parent archive path")
    for part in parts:
        require(":" not in part and not part.endswith((" ", ".")) and part.split(".")[0].upper() not in RESERVED, "nonportable archive path")
    return str(PurePosixPath(name))


def register(name, seen):
    normalized = safe_name(name)
    key = normalized.casefold()
    require(key not in seen, "duplicate or colliding archive path")
    seen.add(key)
    return normalized


def extract_zip(path, output):
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        seen = set()
        total = 0
        for item in entries:
            register(item.orig_filename, seen)
            mode = stat.S_IFMT(item.external_attr >> 16)
            require(mode in (0, stat.S_IFDIR if item.is_dir() else stat.S_IFREG), "ZIP links/special types are forbidden")
            require(not item.flag_bits & 1, "encrypted ZIP is not supported")
            total += item.file_size
        require(total <= MAX_ARCHIVE_BYTES, "archive exceeds recovery staging limit")
        output.mkdir(parents=True, exist_ok=False)
        for item in entries:
            target = output / safe_name(item.orig_filename)
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(item) as source, target.open("wb") as destination:
                    shutil.copyfileobj(source, destination)


def checked_members(archive, limit):
    seen = set()
    total = 0
    for item in archive:
        if item.isdir() and item.name in (".", "./"):
            continue
        name = register(item.name, seen)
        require(item.type in (tarfile.REGTYPE, tarfile.AREGTYPE, tarfile.DIRTYPE), "TAR links/special types are forbidden")
        if item.isfile():
            require(item.size >= 0, "negative TAR member size")
            total += item.size
            require(total <= limit, "TAR exceeds content limit")
        yield item, name


def export_source(receipt, directory):
    try:
        run(["git", "merge-base", "--is-ancestor", receipt["source_sha"], receipt["controller_sha"]])
    except RuntimeError as error:
        raise ValueError("released source is not an ancestor of the controller") from error
    archive_path = directory / "source.tar"
    with archive_path.open("wb") as output:
        run(["git", "archive", receipt["source_sha"]], output=output)
    target = directory / "source"
    target.mkdir()
    with tarfile.open(str(archive_path), "r|") as archive:
        for item, name in checked_members(archive, MAX_ARCHIVE_BYTES):
            path = target / name
            if item.isdir():
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(item) as source, path.open("wb") as output:
                    shutil.copyfileobj(source, output)


def identity(value, receipt):
    require(all(value.get(key) == expected for key, expected in (
        ("status", "release"), ("tag", receipt["tag"]), ("version", receipt["version"]),
        ("sourceRevision", receipt["source_sha"]))), "publication identity mismatch")


def normalized_notes(value):
    return "\n".join(value.splitlines()).rstrip() + "\n"


def candidate_receipt(candidate, receipt):
    require((candidate / "SOURCE_COMMIT").read_text(encoding="utf-8").strip() == receipt["source_sha"], "candidate source mismatch")
    publication = json.loads((candidate / "PUBLICATION.json").read_text(encoding="utf-8"))
    identity(publication, receipt)
    documentation = (candidate / "SITE-DOCUMENTATION.json").read_bytes()
    identity(json.loads(documentation), receipt)
    assets = {}
    for asset in receipt["release"]["assets"]:
        require(asset["name"] not in assets, "duplicate official asset name")
        assets[asset["name"]] = asset
    checksums = candidate / "SHA256SUMS"
    require(assets.get("SHA256SUMS", {}).get("digest") == "sha256:" + file_digest(checksums), "official checksum asset mismatch")
    hashes = {}
    for line in checksums.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([a-f0-9]{64})\s+\*?(?:\./)?([^/\\]+)", line)
        require(match is not None, "invalid distribution checksum")
        checksum, name = match.groups()
        require(safe_name(name) == name and name not in hashes, "unsafe/duplicate checksum name")
        require(file_digest(candidate / "files" / name) == checksum, "candidate bytes differ")
        require(assets.get(name, {}).get("digest") == "sha256:" + checksum, "official distribution digest differs")
        hashes[name] = checksum
    require(bool(hashes), "distribution checksum inventory is empty")
    notes = (candidate / "files" / "release-notes.md").read_text(encoding="utf-8")
    require(normalized_notes(notes) == normalized_notes(receipt["release"]["body"]), "official release notes differ")
    packages = {}
    for package in publication.get("packages", []):
        slug, filename = package["brand_slug"], package["filename"]
        require(re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug) is not None and filename in hashes, "invalid release package binding")
        path = slug + "/downloads/" + filename
        require(path not in packages, "duplicate release package")
        packages[path] = hashes[filename]
    require(bool(packages), "release package inventory is empty")
    return {"documentation": documentation, "packages": packages}


def validate_tag_contracts(source, candidate, receipt):
    tool = [sys.executable, str(source / "scripts" / "release_contract.py")]
    common = ["--version", receipt["version"], "--revision", receipt["source_sha"], "--require-release"]
    run(tool + ["verify", *common, "--release-dir", str(candidate / "files"), "--notes", str(candidate / "files/release-notes.md")], cwd=source)
    run(tool + ["publication", *common, "--record", str(candidate / "PUBLICATION.json")], cwd=source)
    run(tool + ["documentation", *common, "--record", str(candidate / "DOCUMENTATION.json"),
                "--publication", str(candidate / "PUBLICATION.json"), "--docs", str(candidate / "docs"),
                "--exported", str(candidate / "SITE-DOCUMENTATION.json"), "--release-dir", str(candidate / "files")], cwd=source)


def extract_pages(path, output, receipt, binding):
    output.mkdir(parents=True, exist_ok=False)
    target = output / "artifact.tar"
    with zipfile.ZipFile(path) as archive:
        require(len(archive.infolist()) == 1 and archive.infolist()[0].orig_filename == "artifact.tar", "Pages envelope must contain only artifact.tar")
        item = archive.getinfo("artifact.tar")
        require(stat.S_IFMT(item.external_attr >> 16) in (0, stat.S_IFREG), "invalid Pages envelope type")
        require(item.file_size <= MAX_ARCHIVE_BYTES, "Pages envelope exceeds staging limit")
        with archive.open(item) as source, target.open("wb") as destination:
            shutil.copyfileobj(source, destination)
    before = file_digest(target)
    found = set()
    documentation_found = False
    files = 0
    content_bytes = 0
    with tarfile.open(str(target), "r|*") as archive:
        for item, name in checked_members(archive, MAX_SITE_BYTES):
            if not item.isfile():
                continue
            files += 1
            content_bytes += item.size
            if name == "docs/publication.json":
                require(archive.extractfile(item).read() == binding["documentation"], "Pages documentation differs from qualified candidate")
                documentation_found = True
            elif name in binding["packages"]:
                value = hashlib.sha256()
                with archive.extractfile(item) as data:
                    for chunk in iter(lambda: data.read(1024 * 1024), b""):
                        value.update(chunk)
                require(value.hexdigest() == binding["packages"][name], "hosted ZIP differs from official release")
                found.add(name)
    require(documentation_found and found == set(binding["packages"]), "Pages release inventory is incomplete")
    require(file_digest(target) == before, "Pages TAR changed during preparation")
    return {"tar_sha256": before, "files": files, "content_bytes": content_bytes}


def write_json(path, value):
    with path.open("w", encoding="utf-8", newline="\n") as output:
        json.dump(value, output, indent=2)
        output.write("\n")


def controller_sha():
    actual = run(["git", "rev-parse", "HEAD"]).decode().strip()
    if os.environ.get("GITHUB_ACTIONS") == "true":
        require(os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch" and os.environ.get("GITHUB_REF") == "refs/heads/main", "recovery controller must be dispatched on main")
        require(os.environ.get("GITHUB_SHA") == actual, "controller checkout mismatch")
    return actual


def prepare(directory):
    saved = json.loads((directory / "receipt.json").read_text(encoding="utf-8"))
    if os.environ.get("GITHUB_ACTIONS") == "true":
        require(saved["repository"].lower() == os.environ.get("GITHUB_REPOSITORY", "").lower(), "controller repository mismatch")
    client = GitHub(saved["repository"])
    receipt = resolve_source(client, saved["tag"], saved["run_id"], controller_sha())
    for key in ("repository", "tag", "version", "source_sha", "controller_sha", "run_id", "pages_artifact", "candidate_artifact"):
        require(receipt[key] == saved[key], "source qualification changed between recovery phases: " + key)
    candidate_zip, pages_zip = directory / "candidate.zip", directory / "pages.zip"
    print("Downloading qualified source artifacts", flush=True)
    client.download(receipt["candidate_artifact"], candidate_zip)
    client.download(receipt["pages_artifact"], pages_zip)
    candidate = directory / "candidate"
    extract_zip(candidate_zip, candidate)
    binding = candidate_receipt(candidate, receipt)
    validate_tag_contracts(directory / "source", candidate, receipt)
    result = extract_pages(pages_zip, directory / "pages", receipt, binding)
    controller_run = os.environ.get("GITHUB_RUN_ID", "local")
    require(controller_run == "local" or re.fullmatch(r"[1-9][0-9]*", controller_run) is not None, "invalid controller run ID")
    result.update(source_sha=receipt["source_sha"], controller_sha=receipt["controller_sha"],
                  tag=receipt["tag"], run_id=receipt["run_id"],
                  artifact_name="github-pages-recovery-" + receipt["source_sha"] + "-" + controller_run)
    write_json(directory / "transport.json", result)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8", newline="\n") as output:
            for name in ("artifact_name", "source_sha", "controller_sha", "tar_sha256"):
                output.write(name + "=" + result[name] + "\n")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8", newline="\n") as output:
            output.write("Qualified Pages artifact ready for deployment.\n\nContent: %s at %s, original run %d.\n\nController: %s.\n\nUnchanged TAR SHA-256: %s.\n" %
                         (receipt["tag"], receipt["source_sha"], receipt["run_id"], receipt["controller_sha"], result["tar_sha256"]))
    print(json.dumps(result), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    resolve = commands.add_parser("resolve")
    resolve.add_argument("--repository", required=True)
    resolve.add_argument("--tag", required=True)
    resolve.add_argument("--run-id", required=True, type=int)
    resolve.add_argument("--directory", required=True, type=Path)
    stage = commands.add_parser("prepare")
    stage.add_argument("--directory", required=True, type=Path)
    args = parser.parse_args()
    directory = args.directory.resolve()
    if args.command == "resolve":
        if os.environ.get("GITHUB_ACTIONS") == "true":
            require(args.repository.lower() == os.environ.get("GITHUB_REPOSITORY", "").lower(), "controller repository mismatch")
        receipt = resolve_source(GitHub(args.repository), args.tag, args.run_id, controller_sha())
        directory.mkdir(parents=True, exist_ok=False)
        export_source(receipt, directory)
        write_json(directory / "receipt.json", receipt)
        print("Qualified %s at %s from run %d" % (receipt["tag"], receipt["source_sha"], receipt["run_id"]), flush=True)
    else:
        prepare(directory)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, OSError, tarfile.TarError, zipfile.BadZipFile) as error:
        print("Pages recovery failed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
