# Quickstart: Validate S014

## Prerequisites

- Python 3.8 or newer with repository requirements installed.
- Node.js 20 or newer and the pinned site dependencies.
- Full raster, PDF, and browser capabilities for the production gate.

## Focused checks

```powershell
.venv/Scripts/python skill/templates/test_brand_contract.py
.venv/Scripts/python skill/templates/test_iconkit.py
.venv/Scripts/python scripts/test_prepare_site.py
.venv/Scripts/python skill/templates/test_pipeline.py
pnpm --dir site lint
```

Expected result: the optional showcase-role contract, synthetic visible-bound cases, generated binding, and static types all pass.

## Complete source and production gate

```powershell
.venv/Scripts/python skill/templates/test_glyphkit.py
.venv/Scripts/python scripts/test_package_release.py
.venv/Scripts/python scripts/test_release_contract.py
.venv/Scripts/python scripts/test_prepare_site.py
.venv/Scripts/python skill/templates/test_brand_contract.py
.venv/Scripts/python skill/templates/test_iconkit.py
.venv/Scripts/python skill/templates/test_pipeline.py
.venv/Scripts/python scripts/check_markdown.py
.venv/Scripts/python skill/templates/probe.py
.venv/Scripts/python scripts/build_all.py
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected result: all five production kits report zero verification problems and zero glyph failures, the site exports successfully, and browser verification reports zero contract or accessibility failures.

## Visual and identity review

- Inspect the five landing cards at 360px, 1280px, and 200 percent zoom.
- Inspect the Glitchpad portfolio hero in dark and light themes and representative focus states.
- Confirm the landing image content box is square and visible opposite margins differ by no more than one raster pixel.
- Confirm Glitchpad large showcase surfaces use the governed card surface without yellow wash or glow.
- Compare canonical Glitchpad path strings with the pre-slice revision.
- Record every declared Glitchpad square asset as corrected, verified unchanged, or explicitly skipped in `evidence.md`.
