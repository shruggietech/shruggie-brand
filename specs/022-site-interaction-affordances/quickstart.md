# Quickstart: Validate Site Interaction Affordances

## Prerequisites

- Python dependencies from `requirements.txt`
- Node.js 20 or newer
- pnpm 10.28.2
- Site dependencies and Playwright Chromium installed

## 1. Run Source-Level Contracts

```powershell
node --test site/tests/production-origin.test.mjs site/tests/payload-contract.test.mjs
```

Expected outcome: footer metadata, pagination selectors, theme cursor selectors, and isolated negative contract fixtures pass.

## 2. Type-check and Export the Site

```powershell
pnpm --dir site lint
pnpm --dir site build
```

Expected outcome: generated content preparation, TypeScript checking, and the complete static export finish without errors.

## 3. Run Rendered Interaction Verification

```powershell
pnpm --dir site test
```

Expected outcome: all routes, payloads, footer destination metadata, keyboard and focus behavior, pagination center measurements, theme-control cursor and semantic states, responsive layouts, both themes, and WCAG 2.1 AA checks pass.

## 4. Run Repository CI Parity

```powershell
python -m compileall -q scripts skill/templates
python skill/templates/test_glyphkit.py
python scripts/test_package_release.py
python scripts/test_release_contract.py
python scripts/test_prepare_site.py
python skill/templates/test_brand_contract.py
python skill/templates/test_iconkit.py
python skill/templates/test_pipeline.py
python scripts/check_markdown.py
python scripts/build_all.py
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected outcome: all source tests, six production-kit builds, site checks, and publication gates pass with zero problems.

## 5. Review Hygiene

Confirm that `dist/`, site exports, screenshots, caches, and `.specify/feature.json` remain ignored, and that tracked text is UTF-8 without BOM with LF line endings and no mojibake.
