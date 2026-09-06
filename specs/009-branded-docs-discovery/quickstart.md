# Quickstart: Branded Documentation and Discovery Completion

Run from the repository root in this order. Generated artifacts remain ignored.

## 1. Focused source tests

```powershell
.venv\Scripts\python.exe scripts\test_prepare_site.py
.venv\Scripts\python.exe scripts\check_markdown.py
```

Expected: notice, route, preview, guideline, source-preservation, Markdown, UTF-8, LF, and mojibake tests report zero failures.

## 2. Generate and inspect the site

```powershell
.venv\Scripts\python.exe scripts\build_all.py
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: all five production kits verify, TypeScript and static export pass, every public route passes exact metadata and structured-data checks, social assets decode, sitemap URLs equal page canonicals, documentation code and navigation behave correctly, both themes pass WCAG 2.1 AA, and screenshots are written below ignored `site/test-results/visual/`.

Inspect the eight screenshots for `/docs/` and `/docs/04-toolchain/` at 360 and 1280 CSS pixels in light and dark themes. Confirm compact hierarchy, readable code panels, visible callouts, recognizable sidebar identity, branded navigation state, and no clipping.

## 3. Full CI-parity verification

```powershell
.venv\Scripts\python.exe -m compileall -q scripts skill\templates
.venv\Scripts\python.exe scripts\build_all.py --list
.venv\Scripts\python.exe skill\templates\test_glyphkit.py
.venv\Scripts\python.exe scripts\test_release_contract.py
.venv\Scripts\python.exe scripts\test_prepare_site.py
.venv\Scripts\python.exe skill\templates\test_brand_contract.py
.venv\Scripts\python.exe skill\templates\test_iconkit.py
.venv\Scripts\python.exe skill\templates\test_pipeline.py
.venv\Scripts\python.exe scripts\check_markdown.py
.venv\Scripts\python.exe skill\templates\probe.py
.venv\Scripts\python.exe scripts\build_all.py
.venv\Scripts\python.exe scripts\package_release.py --version 1.1.2
.venv\Scripts\python.exe scripts\release_contract.py notes --version 1.1.2 --output release\release-notes.md
.venv\Scripts\python.exe scripts\release_contract.py verify --version 1.1.2 --release-dir release --notes release\release-notes.md
.venv\Scripts\python.exe skill\templates\sync_agents_md.py skill
git diff --exit-code -- skill/AGENTS.md
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
git diff --check
```

Expected: zero test, verification, glyph, accessibility, metadata, archive, agent-contract, and hygiene failures.

## 4. Publication boundary

Commit only source and Spec Kit files. Push `codex/009-docs-discovery-completion`, open a pull request that closes #108, #109, and #111, process the automatic Codex review, request at most one explicit second review, and leave the green reviewed pull request open for the owner merge ritual.
