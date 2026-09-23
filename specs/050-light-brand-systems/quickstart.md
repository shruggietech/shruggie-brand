# Quickstart Validation: S050

## Prerequisites

Use the Python environment, `coloraide`, Node 20+, pnpm, Playwright Chromium, and PDF raster tools listed in `CONTRIBUTING.md`. No network is required during routine generation.

## Validate the source contract

Run `python skill/templates/test_brand_contract.py` and `python skill/templates/test_pipeline.py`. Invalid mode and missing light palette fixtures must fail; a missing mode must resolve to dark.

## Build both presentation modes

Run `python scripts/build_all.py`. Inspect I Heart PR Tours as the light representative and ShruggieTech as a dark-default representative. Their kit `VERIFY.md` files report zero problems, `validate_glyph.py` reports zero failures, and PDF ground QC measures every page against the declared mode. Open generated contact sheets where the full tier produces them.

## Validate hosted and portable views

Run `pnpm --dir site build`, which executes site contract and browser validation. Check the I Heart PR Tours portfolio card, guideline overview/color/logo routes, and downloads at 360px, 390px, desktop width, 200 percent zoom, no-script, reduced-motion, and print. Compare a dark-first brand in the same conditions. The light guide stays light when the host theme changes, while home and documentation still follow host theme.

## Full gate and evidence

Run the complete command list in `CONTRIBUTING.md`, then record exact command outcomes, measured contrast/ground evidence, any capability skips, and artifact inspection in `evidence.md`. Keep all generated kits, PDFs, screenshots, and site exports out of the commit.
