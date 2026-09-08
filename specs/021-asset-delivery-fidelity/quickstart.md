# Quickstart: Asset Delivery Fidelity

## Prerequisites

- Use the repository Python environment with dependencies from `requirements.txt`.
- Install site dependencies from `site/pnpm-lock.yaml`.
- Keep generated `dist/` kits and site exports ignored.

## Focused Generator Regression

```powershell
.venv\Scripts\python.exe skill/templates/test_pipeline.py
```

Expected: the square-enclosure test proves explicit mask coverage, complete black and white horizontal and stacked mark regions, preserved source paths, and SVG-to-PNG agreement. Synthetic clipped-mask and fold-fragment cases fail the verifier.

## Glitchpad Production Build

```powershell
.venv\Scripts\python.exe scripts/build_all.py glitchpad
```

Expected: `validate_glyph.py` reports zero failures, `verify.py` reports zero problems, and every black and white full-lockup SVG and PNG contains the complete square-based paper-and-G mark and wordmark.

Inspect these ignored outputs:

- `dist/glitchpad/logos/svg/glitchpad-horizontal-black.svg`
- `dist/glitchpad/logos/svg/glitchpad-horizontal-white.svg`
- `dist/glitchpad/logos/svg/glitchpad-stacked-black.svg`
- `dist/glitchpad/logos/svg/glitchpad-stacked-white.svg`
- corresponding PNG deliveries under `dist/glitchpad/logos/png/`
- `dist/glitchpad/qc/logo-sheet.png`

## Focused Site Contract

```powershell
.venv\Scripts\python.exe scripts/prepare_site.py
pnpm --dir site lint
pnpm --dir site exec next build --webpack
pnpm --dir site test
```

Expected: every generated asset route uses exact manifest deliveries, all media remains centered and contained above metadata, and the browser audit passes mobile and desktop routes with zero WCAG 2.1 AA violations.

## Full CI-Parity Gate

```powershell
.venv\Scripts\python.exe skill/templates/test_glyphkit.py
.venv\Scripts\python.exe scripts/test_package_release.py
.venv\Scripts\python.exe scripts/test_release_contract.py
.venv\Scripts\python.exe scripts/test_prepare_site.py
.venv\Scripts\python.exe skill/templates/test_brand_contract.py
.venv\Scripts\python.exe skill/templates/test_iconkit.py
.venv\Scripts\python.exe skill/templates/test_pipeline.py
.venv\Scripts\python.exe scripts/check_markdown.py
.venv\Scripts\python.exe scripts/build_all.py
pnpm --dir site lint
pnpm --dir site exec next build --webpack
pnpm --dir site test
```

Expected: all six kits build cleanly, release and generator contracts pass, the static site exports every route, and the responsive accessibility sweep reports zero violations.

## Hygiene

- Confirm Glitchpad source path hashes are unchanged.
- Confirm presentation-only site changes do not alter generated delivery hashes.
- Confirm `dist/`, site exports, and `.specify/feature.json` remain untracked.
- Confirm committed text is UTF-8 without BOM, uses LF, and contains no mojibake.
