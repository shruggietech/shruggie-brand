# Quickstart: Integration Preview Visibility

## Prerequisites

- Python 3.8 or newer with `requirements.txt` installed.
- Node.js 20 or newer, the repository-pinned SVG renderer, site dependencies, and Playwright Chromium.
- An approved I Heart PR Tours proof root supplied through `GP_APPROVED_PROOF_ROOT` for production identity validation.

## Focused red-green validation

```powershell
python skill/templates/test_pipeline.py -k preview
```

Before implementation, the test must expose wrong-well selection, generic container copy, missing nonvisual semantics, or inherited dark-well text. After implementation, all temporary transparent, black, white, full-color, metadata, container, fully transparent, and mixed-group cases must satisfy [the presentation contract](contracts/integration-preview-contract.md).

## Focused generated kit

```powershell
python scripts/build_all.py i-heart-pr-tours
```

Expected: `validate_glyph.py` reports zero failures, `verify.py` reports zero problems, generated preview cards include light, dark, and nonvisual wells, and source asset hashes remain unchanged.

## Generated portable browser acceptance

```powershell
pnpm --dir site build
node site/scripts/verify-site.mjs
```

Expected: the copied portable guide passes every preview audit at 1280 and 360 CSS pixels, at 200 percent zoom, and when opened directly as a local file. Every well label and fallback reaches 4.5:1, every measured visual reaches 3:1, both visual well types are exercised, all images remain contained, and no horizontal overflow or axe violation is reported.

## Full verification

Run the Python 3.8 compatibility command set and the full `.github/workflows/build.yml` sequence: compile, discovery, publication, packaging, release-contract, site-preparation, identity, brand, icon, glyph, pipeline, Markdown, probe, all-kit build, release certification, generated-agent diff, site lint/build/test, and publication audit.

Expected: every production kit reports zero verifier problems and zero glyph failures, all unit and browser suites pass, generated artifacts remain ignored, and the final staged diff contains only governed source, tests, changelog, and S035 artifacts.
