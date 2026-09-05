# Quickstart: S007 Verification

Run each command from the repository root in chronological order. Generated files remain ignored.

## 1. Contract and focused regressions

```powershell
.\.venv\Scripts\python.exe skill/templates/test_brand_contract.py
.\.venv\Scripts\python.exe skill/templates/test_pipeline.py
.\.venv\Scripts\python.exe scripts/test_prepare_site.py
.\.venv\Scripts\python.exe scripts/test_release_contract.py
.\.venv\Scripts\python.exe scripts/check_markdown.py
```

Expected: explicit missing-state, third-party text scan, supplied-input integrity, palette approval, fixed-font metadata, ingestion boundary, private-publication, and existing pipeline tests all pass.

## 2. Syntax and production discovery

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts skill/templates
.\.venv\Scripts\python.exe scripts/build_all.py --list
```

Expected: Python compilation succeeds and exactly the five production brand slugs are listed.

## 3. Full offline production build

```powershell
.\.venv\Scripts\python.exe scripts/build_all.py
```

Expected: all five explicitly migrated brands report zero contract, verification, and glyph failures. Generated manifests contain correct explicit affiliation and typography facts.

## 4. Generated contract and release checks

```powershell
.\.venv\Scripts\python.exe skill/templates/sync_agents_md.py skill
.\.venv\Scripts\python.exe scripts/package_release.py --version 1.1.2
.\.venv\Scripts\python.exe scripts/release_contract.py notes --version 1.1.2 --output release/release-notes.md
.\.venv\Scripts\python.exe scripts/release_contract.py verify --version 1.1.2 --release-dir release --notes release/release-notes.md
```

Expected: instruction synchronization reports `unchanged` and the release archive contract passes without publishing a release.

## 5. Static site preparation and verification

```powershell
.\.venv\Scripts\python.exe scripts/prepare_site.py
pnpm --dir site exec tsc --noEmit
pnpm --dir site run build
pnpm --dir site test
```

Expected: only explicit public brands appear in generated data and copied assets; static export, metadata, responsive layout, and accessibility checks pass.

## 6. Repository hygiene

```powershell
git status --short
git check-attr -a -- specs/007-ownership-neutral-inputs/spec.md skill/references/canon.schema.json skill/templates/brand_contract.py
```

Expected: only intentional source changes are tracked, no `dist/` or generated site output is staged, text is UTF-8 without BOM with LF, and no mojibake is present.
