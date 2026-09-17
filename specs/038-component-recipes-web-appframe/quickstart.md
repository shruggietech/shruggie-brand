# Quickstart: Verify Component Recipes and Web AppFrame

## 1. Run focused contract tests

```powershell
.venv\Scripts\python skill/templates/test_component_contract.py
.venv\Scripts\python skill/templates/test_interface_contract.py
.venv\Scripts\python skill/templates/test_pipeline.py
```

Expected result: the closed recipe vocabulary, semantic roles, state requirements, override boundaries, AppFrame ownership, deterministic generation, React entry boundaries, and consumer version fields pass. Negative fixtures fail with the named component or rule.

## 2. Build every production kit

```powershell
.venv\Scripts\python scripts/build_all.py
```

Expected result: every production brand generates the authoritative Web/React adapter and updated enforcement output, reports zero verification problems, and retains identity and affiliation data.

## 3. Exercise generated adapters

Inspect `dist/shruggietech/web/adapter.json`, recipe and ownership files, semantic tokens, and server/client sources. Confirm all 15 recipes, governed CSS variables, a server-safe entry, the exact accessible dependency, and one owner per shell responsibility.

```powershell
pnpm --dir site lint
pnpm --dir site test
```

Expected result: generated adapter smoke imports type-check, and Playwright Chromium interaction plus axe checks pass for browser and simulated Windows 11 and Android Chrome configurations with explicit limitations.

## 4. Run release and repository gates

```powershell
.venv\Scripts\python scripts/test_package_release.py
.venv\Scripts\python scripts/test_release_contract.py
.venv\Scripts\python scripts/package_release.py
.venv\Scripts\python scripts/check_markdown.py
```

Expected result: release certification requires and verifies recipe, adapter, support, schema version 2, exact version fields, and recovery provenance.

## 5. Run full CI parity

Run every command in `CONTRIBUTING.md` and `.github/workflows/build.yml`, including Python 3.8 checks, all template and script suites, all-brand generation, synchronized instructions, site lint/build/test, publication audit, `git diff --check`, and a check that generated paths are untracked. Commit no `dist/` content.
