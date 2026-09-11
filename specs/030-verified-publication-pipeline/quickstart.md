# Quickstart: Verified Publication Pipeline

## Prerequisites

- Work from `codex/030-verified-publication-pipeline` with Python 3.12, Node 24.11.0, pnpm 10.28.2, the repository Python dependencies, and site dependencies installed.
- Keep `.specify/feature.json`, `dist/`, `release/`, and `site/out/` uncommitted.
- Do not create a test version tag or GitHub release.

## 1. Run focused workflow and artifact contracts

```powershell
python scripts\test_publication_workflow.py
python scripts\test_release_contract.py
python scripts\test_identity_continuity_audit.py
```

Expected: trigger, permission, SHA pin, artifact, renderer, proof-transfer, Pages, and Release assertions pass. Mutation cases for unsafe workflow constructs and artifact paths fail closed inside their tests.

## 2. Run generator and source regression gates

```powershell
python skill\templates\test_glyphkit.py
python scripts\test_package_release.py
python scripts\test_prepare_site.py
python skill\templates\test_brand_contract.py
python skill\templates\test_identity_continuity.py
python skill\templates\test_iconkit.py
python skill\templates\test_pipeline.py
python scripts\check_markdown.py
```

Expected: every suite passes with no identity approval, proof hash, renderer tolerance, or geometry change.

## 3. Build and audit all production output

Use the existing canonical approved-proof root for the host, then run:

```powershell
python scripts\build_all.py
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
python scripts\audit_publication_artifacts.py --kits dist --site site\out
```

Expected: all eight kits report zero verifier problems and zero glyph failures; site tests cover every documented route at desktop and mobile widths with zero WCAG 2.1 AA violations; only governed hidden icon manifests are present and no symlink exists.

## 4. Certify release output without publishing

```powershell
$version = python scripts\release_contract.py current
python scripts\package_release.py --version $version
python scripts\release_contract.py notes --version $version --output release\release-notes.md
python scripts\release_contract.py verify --version $version --release-dir release --notes release\release-notes.md
```

Expected: the current release candidate contains exactly the declared assets and valid notes. No tag or GitHub release is created.

## 5. Validate workflow syntax and repository hygiene

```powershell
go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.7
git diff --check
git status --short
```

Expected: workflow syntax and shell expressions pass; generated outputs and local Spec Kit state remain ignored; committed text is UTF-8 without BOM, LF-only, and free of mojibake.

## 6. Validate the official pull request

Require the exact pull-request head to show green Python 3.8 compatibility, canonical proof export, authoritative build, and required `build` status. Confirm the run exposes SHA-qualified proof, kit, Pages, and release-candidate artifacts, but creates no Pages deployment or GitHub release. Process every Codex and security review item, request no more than one second review round, and leave zero unresolved threads.

## 7. Post-merge owner verification

After the owner completes the merge ritual, confirm the main run deploys the exact verified SHA, the production Pages environment advances from the last known-good revision, and the live I Heart PR Tours routes, registry endpoints, assets, and downloads pass the documented site checks. This post-merge evidence is intentionally outside the pre-merge S030 implementation halt.
