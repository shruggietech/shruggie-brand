# Quickstart: Hosted Guidelines Portal Rebuild

## Prerequisites

- Python dependencies installed from `requirements.txt`.
- Site dependencies installed from `site/pnpm-lock.yaml`.
- Chromium installed for the existing Playwright version.

## Focused validation

```powershell
.\.venv\Scripts\python scripts/test_prepare_site.py
.\.venv\Scripts\python skill/templates/test_pipeline.py
pnpm --dir site lint
```

Expected result: portal payload, publication, generated-topic, inventory, and TypeScript contracts pass.

## Build every production portal

```powershell
.\.venv\Scripts\python scripts/build_all.py
pnpm --dir site build
pnpm --dir site test
```

Expected result: five verified kits generate complete portal payloads; every applicable topic exports to its canonical route; browser checks cover navigation, colors, assets, instructions, footer utilities, and landing headings.

## Full repository gate

```powershell
.\.venv\Scripts\python skill/templates/test_glyphkit.py
.\.venv\Scripts\python scripts/test_package_release.py
.\.venv\Scripts\python scripts/test_release_contract.py
.\.venv\Scripts\python scripts/test_prepare_site.py
.\.venv\Scripts\python skill/templates/test_brand_contract.py
.\.venv\Scripts\python skill/templates/test_iconkit.py
.\.venv\Scripts\python skill/templates/test_pipeline.py
.\.venv\Scripts\python scripts/check_markdown.py
.\.venv\Scripts\python skill/templates/probe.py
.\.venv\Scripts\python scripts/build_all.py
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected result: every command exits zero, every production `verify.py` report contains zero problems, every glyph validation contains zero failures, and no generated output is staged.

## Manual evidence matrix

Review all five brands at 360, 768, 1024, and 1280 pixels plus 200 percent zoom. Complete these tasks for each brand: move between topics, copy a HEX value, reveal secondary color values, find and download a logo, locate platform instructions, filter for a platform asset, inspect complete delivery details, and use both footer utilities. Repeat core topic and download traversal with scripting disabled.
