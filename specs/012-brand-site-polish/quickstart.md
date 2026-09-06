# Quickstart: Validate S012 Brand Site Polish

## Prerequisites

- Python 3.8 or newer with repository requirements installed
- Node.js 20 or newer and pnpm 10.28.2
- Existing native renderers for the full production-kit gate
- Site dependencies and Chromium installed as documented by CI

## Source and generator checks

```powershell
python skill/templates/test_glyphkit.py
python scripts/test_package_release.py
python scripts/test_release_contract.py
python scripts/test_prepare_site.py
python skill/templates/test_brand_contract.py
python skill/templates/test_iconkit.py
python skill/templates/test_pipeline.py
python scripts/check_markdown.py
```

Expected: every test and policy check passes, including canonical black application-icon input, colored lockup selection, canonical documentation terminology, and preserved geometry.

## Complete build and site checks

```powershell
python scripts/build_all.py
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: five production kits report zero problems and zero glyph failures; the 26-route static export succeeds; browser verification reports zero failures and zero WCAG 2.1 AA violations.

## Visual inspection

Inspect all 12 screenshots under `site/test-results/visual/`: the landing page, documentation index, and Variance Contract route at 360px and 1280px in light and dark themes. Confirm the colored lockup, exact navigation inventory, orange primary hierarchy, green documentation accents, visible inline-link and pagination affordances, canonical wording, responsive reflow, and absence of clipping or overlap.

## Repository hygiene

```powershell
git diff --check
git status --short
```

Expected: no whitespace errors, no generated publication artifacts in the diff, UTF-8 without BOM and LF-only text, no mojibake or private paths, and only intended S012 source, test, changelog, and Spec Kit files.
