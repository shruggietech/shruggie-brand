# Quickstart: v1.2.0 Release and Production Certification

Run from the repository root with project dependencies installed.

## 1. Focused compatibility and contract tests

```powershell
python -m compileall -q scripts skill/templates
python scripts/test_release_contract.py
python scripts/test_prepare_site.py
python skill/templates/test_brand_contract.py
python skill/templates/test_iconkit.py
python skill/templates/test_glyphkit.py
python skill/templates/test_pipeline.py
python scripts/check_markdown.py
```

Expected: every command exits zero on the active Python and the test set remains discoverable on Python 3.8 in hosted CI.

## 2. Full source build

```powershell
python skill/templates/probe.py
python scripts/build_all.py
python skill/templates/sync_agents_md.py skill
git diff --exit-code -- skill/AGENTS.md
```

Expected: all five production kits report zero verification problems and zero glyph failures, generated agent instructions are synchronized, and generated output remains ignored.

## 3. Local release preflight

```powershell
python scripts/release_contract.py current
python scripts/package_release.py
python scripts/release_contract.py notes --version 1.2.0 --output release/release-notes.md
python scripts/release_contract.py verify --version 1.2.0 --release-dir release --notes release/release-notes.md
```

Expected: current prints 1.2.0 and exactly seven assets plus generated notes pass the complete contract.

## 4. Static site

```powershell
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: content preparation, type checking, static export, route tests, responsive checks, both themes, and WCAG audits succeed from freshly generated kits.

## 5. Repository hygiene

```powershell
git diff --check
git status --short
```

Inspect every changed text file for UTF-8 without BOM, LF, mojibake, private paths, secrets, and provider identifiers. Confirm `dist/`, `release/`, generated site content, dependency folders, caches, and `.specify/feature.json` remain untracked or ignored.

## 6. Hosted pre-merge gate

Publish the S010 pull request, process automatic Codex round one, request no more than one explicit round two, resolve every comment, and wait for every required check. Keep the pull request open and create no tag or release.

## 7. Post-merge continuation

After owner merge, synchronize actual main and repeat sections 1 through 5. Create and push annotated tag v1.2.0, verify the Release workflow, download the public release body and seven assets into a fresh empty directory, and pass the shared verifier. Then qualify the Pages deployment under the production contract and close #118, #119, #116, and milestone 22 only when their evidence gates pass.

