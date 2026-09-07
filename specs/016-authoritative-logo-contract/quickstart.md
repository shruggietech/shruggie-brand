# Quickstart: Validate Authoritative Logo Source Enforcement

## Prerequisites

- Work from the repository root with Python dependencies installed in `.venv`.
- Keep generated kits, release files, site output, and temporary synthetic brands outside Git.
- Confirm `.specify/feature.json` selects `specs/016-authoritative-logo-contract`.

## 1. Focused contract tests

```powershell
.\.venv\Scripts\python skill/templates/test_brand_contract.py
```

Expected: explicit modes, variant bindings, hash and role checks, helper conflicts, imported-image exclusivity, constructed compatibility, and the issue #151 negative matrix all pass.

## 2. Focused generator and provenance tests

```powershell
.\.venv\Scripts\python skill/templates/test_pipeline.py
.\.venv\Scripts\python skill/templates/test_iconkit.py
.\.venv\Scripts\python skill/templates/test_glyphkit.py
```

Expected: authoritative SVG metadata, deterministic logo provenance, unchanged embedding, valid recolor and lockup lineage, silhouette-tamper rejection, verified platform master handoff, and existing constructed logo behavior all pass.

## 3. Production build and identity audit

```powershell
.\.venv\Scripts\python skill/templates/probe.py
.\.venv\Scripts\python scripts/build_all.py
```

Expected: all five brands build with explicit source modes, every `verify.py` report has zero problems, every `validate_glyph.py` report has zero failures, ShruggieTech contains complete authoritative provenance, and no source input or constructed path fingerprint changes.

## 4. Release and site parity

```powershell
.\.venv\Scripts\python scripts/test_package_release.py
.\.venv\Scripts\python scripts/test_release_contract.py
.\.venv\Scripts\python scripts/test_prepare_site.py
.\.venv\Scripts\python scripts/package_release.py --version 1.2.1
.\.venv\Scripts\python scripts/release_contract.py notes --version 1.2.1 --output release/release-notes.md
.\.venv\Scripts\python scripts/release_contract.py verify --version 1.2.1 --release-dir release --notes release/release-notes.md
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: packaging includes source-derived verified kits, the static site consumes generated logo assets, all browser and accessibility assertions pass, and no release is published.

## 5. Source hygiene

```powershell
.\.venv\Scripts\python scripts/check_markdown.py
.\.venv\Scripts\python skill/templates/sync_agents_md.py skill
git diff --check
git status --short
```

Expected: Markdown, UTF-8 without BOM, LF line endings, mojibake checks, generated agent synchronization, and repository hygiene pass. Only intentional S016 sources and documentation are tracked.
