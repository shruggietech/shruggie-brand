# Quickstart: Verify S003

## 1. Confirm feature context and baseline

```powershell
.\.specify\scripts\powershell\check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
git merge-base --is-ancestor origin/main HEAD
git status --short
```

## 2. Run focused regression suites

```powershell
python -m compileall -q scripts skill/templates
python scripts/build_all.py --list
python skill/templates/test_glyphkit.py
python skill/templates/test_pipeline.py
python scripts/check_markdown.py
```

Expected: every command exits zero. Pipeline output names the tests that cover `003-T001` through `003-T019`.

## 3. Probe, build, and verify all targets

```powershell
python skill/templates/probe.py
python scripts/build_all.py
python skill/templates/sync_agents_md.py skill
git diff --exit-code -- skill/AGENTS.md
```

Expected: six targets build, each reports zero verification problems and zero glyph failures, and generated agent instructions remain synchronized.

## 4. Build the generated-kit consumer

```powershell
pnpm --dir site install --frozen-lockfile
pnpm --dir site lint
pnpm --dir site build
```

Expected: the static site exports every required route from freshly generated kit output without fetching canonical fonts from the network.

## 5. Dry-run release packaging

```powershell
python scripts/package_release.py
```

Expected: exactly two skill archives and five production kit archives are generated locally. Each archive contains its required licensing files, and each production kit contains its guide PDF. No tag or release is created.

## 6. Validate public-content hygiene

```powershell
git diff --check
python scripts/check_markdown.py
```

Also inspect new public prose for absolute workstation paths, secrets, provider identifiers, BOMs, CRLF, and mojibake before publication.

## 7. Enforce the review ceiling

After opening the pull request:

1. Process the automatic Codex round and update review row 1.
2. Post exactly one `@Codex` request and record its comment URL in row 2.
3. Process round 2 and never post another review request.
4. Wait for every required check to pass.
5. Leave the pull request open and ask the owner for the final review and merge ritual.
