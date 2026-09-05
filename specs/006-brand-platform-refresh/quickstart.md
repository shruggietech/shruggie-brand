# Quickstart: Brand Platform Refresh Verification

Run every command from the repository root in the listed order. Generated output remains ignored.

## 1. Focused source and preparation tests

```powershell
python scripts/test_prepare_site.py
python skill/templates/test_pipeline.py
python scripts/test_release_contract.py
python scripts/check_markdown.py
```

Expected: all focused tests pass, temporary test brands are removed automatically, and Markdown policy reports success.

## 2. Compile and discover production brands

```powershell
python -m compileall -q scripts skill/templates
python scripts/build_all.py --list
```

Expected: exactly the five production brand slugs are listed, with no fixture or manually maintained expected set.

## 3. Full production build

```powershell
python scripts/build_all.py
```

Expected: all five production kits report zero verification problems and zero glyph failures. Generated kits stay under ignored `dist/`.

## 4. Generated agent and release contracts

```powershell
python skill/templates/sync_agents_md.py skill
git diff --exit-code -- skill/AGENTS.md
python scripts/package_release.py --version 1.1.2
python scripts/release_contract.py notes --version 1.1.2 --output release/release-notes.md
python scripts/release_contract.py verify --version 1.1.2 --release-dir release --notes release/release-notes.md
```

Expected: generated agent instructions do not drift and the existing seven-archive release contract remains valid with five production kits.

## 5. Site type check, export, and browser verification

```powershell
pnpm --dir site install --frozen-lockfile
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: authoritative references generate into Fumadocs MDX, TypeScript passes, static export succeeds, browser checks find complete metadata and routes, all known tables are semantic, axe reports zero violations, and responsive pages have no horizontal overflow.

## 6. Repository hygiene

```powershell
git status --short
git diff --check
```

Expected: generated kits, site content, static export, search source, package archives, and release output remain ignored. Only intended source, test, specification, lockfile, workflow, constitution, documentation, and changelog changes are tracked.
