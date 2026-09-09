# Quickstart: Validate Unified Navigation and Routes

## Prerequisites

- Run from the repository root.
- Install Python dependencies from `requirements.txt`.
- Install site dependencies with the lockfile and Playwright Chromium.

## Focused generator and route checks

```text
python skill/templates/test_pipeline.py
python scripts/test_prepare_site.py
node --test site/tests/production-origin.test.mjs site/tests/payload-contract.test.mjs site/tests/site.test.mjs
```

Expected: exact hierarchy, one-to-one mapping, root removal, Assets consolidation, registry resolution, and stable documentation-route assertions pass.

## Build and rendered checks

```text
python scripts/build_all.py
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: every production kit reports zero verification problems and glyph failures; the static export contains no brand-root or `/guidelines/assets/` page; every retained route passes desktop, mobile, touch-only, no-script, zoom, link, and axe checks.

## Release and repository gates

```text
python skill/templates/test_glyphkit.py
python scripts/test_package_release.py
python scripts/test_release_contract.py
python skill/templates/test_brand_contract.py
python skill/templates/test_iconkit.py
python skill/templates/probe.py
python scripts/check_markdown.py
python scripts/release_contract.py current
```

Use the reported version with `scripts/package_release.py` and `scripts/release_contract.py verify` exactly as CI does. Confirm generated outputs remain ignored, text is UTF-8 without BOM with LF endings, and no mojibake appears.

## Manual inspection

- Open representative brand Overview, Identity child, Assets, and Integration pages in light and dark themes.
- Open documentation pages from each group.
- Inspect desktop, narrow mobile, wide touch-only, no-script, and 200% zoom navigation.
- Confirm the active page and owning group remain clear, content is not duplicated, and no identity artwork changed.
