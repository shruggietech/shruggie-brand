# Quickstart: v1.1.2 Release and Publication Certification

Run these commands from the repository root with repository dependencies installed.

## 1. Focused compatibility and contract tests

```powershell
python -m compileall -q scripts skill/templates
python scripts/test_release_contract.py
python skill/templates/test_glyphkit.py
python skill/templates/test_pipeline.py
python scripts/check_markdown.py
```

Expected: all commands exit zero. Release-contract tests cover metadata, notes, exact assets, archive shape, version agreement, and checksum failures.

## 2. Full source build

```powershell
python skill/templates/probe.py
python scripts/build_all.py
python skill/templates/sync_agents_md.py skill
git diff --exit-code -- skill/AGENTS.md
```

Expected: five production kits and one fixture build with zero reported problems, zero glyph failures, and no generated agent drift.

## 3. Local release preflight

```powershell
python scripts/package_release.py --version 1.1.2
python scripts/release_contract.py notes --version 1.1.2 --output release/release-notes.md
python scripts/release_contract.py verify --version 1.1.2 --release-dir release --notes release/release-notes.md
```

Expected: exactly seven expected archives pass. The generated release notes contain skill 1.1.2, canon 1.1.2, explicit rebuild migration guidance, and the exact root changelog section.

## 4. Static site

```powershell
pnpm --dir site lint
pnpm --dir site build
```

Expected: lint and static export succeed from freshly generated kits.

## 5. Repository hygiene

```powershell
git diff --check
git status --short
```

Inspect tracked changed text as UTF-8 without BOM and LF. Scan S004 public changes for mojibake, secrets, private workstation paths, and provider resource identifiers. Generated `dist/`, `release/`, site export, dependency, and local Spec Kit pointer content must remain untracked.

## 6. Hosted pre-merge gate

Open the official S004 pull request, complete automatic Codex round 1, post exactly one `@Codex` comment, complete round 2, and wait for every required check. Keep the pull request open and create no tag or release.

## 7. Post-merge publication continuation

After the owner merges, fetch current main and verify its tree contains the reviewed S004 result. Re-run steps 1 through 5 against actual main, create annotated tag v1.1.2, push the tag, wait for the Release workflow, save the published release body and assets into a new temporary directory, and run the same release verifier there. Attach sanitized evidence to #63, #72, and #73 before closing children, eligible parents, and zero-open-issue milestones.
