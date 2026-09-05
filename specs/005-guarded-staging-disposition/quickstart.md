# Quickstart: Verify S005

Run these checks from a clean checkout of the S005 branch. Exact private roots and recovery commands are intentionally omitted from this public document.

Use Python 3.8 or newer in an environment containing the full dependencies from `skill/references/04-toolchain.md`. Full-tier regeneration also requires one governed SVG renderer, Pillow, and launchable Playwright Chromium; set `GP_RESVG_RENDERER` to the verified JavaScript helper when using the bundled Node fallback.

## 1. Spec Kit and documentation

```powershell
python scripts\check_markdown.py
python skill\templates\sync_agents_md.py skill
git diff --check origin/main...HEAD
```

Expected: Markdown policy passes, generated `skill/AGENTS.md` remains unchanged, and Git reports no whitespace error.

## 2. Focused regression suites

```powershell
python skill\templates\test_pipeline.py
python scripts\test_release_contract.py
python skill\templates\test_glyphkit.py
```

Expected: all pipeline, release, and glyph-construction regressions pass. These are executable test entry points rather than importable `scripts.*` packages.

## 3. Complete source rebuild

```powershell
python scripts\build_all.py
```

Expected: the entry point replaces each target under ignored `dist/`, all five production brands and the fixture build at full capability, each `verify.py` result reports zero problems, and each `validate_glyph.py` result reports zero failures.

## 4. Static site

```powershell
pnpm --dir site install --frozen-lockfile
pnpm --dir site lint
pnpm --dir site build
```

Expected: lint and static export succeed from freshly generated kits.

## 5. Disposition evidence

Inspect `docs/disposition.md` and `evidence.md`. Confirm every execution-time top-level item has one public row, all rows have verified final states, the source workspace terminal count is zero files, and exact private roots appear only in the operator-held recovery record.

## 6. Repository hygiene

Inspect changed text as UTF-8 without BOM and LF. Scan S005 public changes for mojibake, drive-qualified paths, user-profile paths, secrets, raw session output, backup names or locations, and provider resource identifiers. Generated `dist/`, release downloads, site export, dependency directories, and `.specify/feature.json` must remain untracked.

## 7. Hosted owner gate

Open the official S005 pull request, complete automatic Codex round 1, post exactly one `@Codex` comment, complete round 2, and wait for every required check. Keep the pull request open and close no implementation-dependent child, parent, milestone, slice, or program item until the owner merges.
