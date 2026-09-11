# Quickstart: S028 Validation

## 1. Confirm feature and baseline

```powershell
git status --short --branch
git rev-parse HEAD
.\.specify\scripts\powershell\check-prerequisites.ps1 -Json -PathsOnly
```

Expected before Gate 1: the feature selector resolves `specs/028-i-heart-pr-tours-brand-guide`, the baseline traces merged S027 revision `435019dbc37e754fd1f0b16228a576c985e9468a`, and no production `brands/i-heart-pr-tours/` directory exists.

## 2. Inspect private Gate 1 evidence

Open the revised ignored Gate 1 packet under `dist/i-heart-pr-tours/gate-1-r4/`. Confirm it retains the approved source hierarchy and fonts, binds exact revised copy, uses a live-site and brochure-grounded palette, requires a light-first white-paper guide, demonstrates the knockout-aware single-ink transform, includes the sandy expressions, binds the live-verified colored-heart favicon family and app-icon framing, and keeps every public surface disabled.

Expected: candidate `iheartpr-g1-r4` is complete enough for an explicit approve, revise, or reject decision and remains blocked until the owner names and approves its exact manifest.

## 3. Run focused source and contract tests after Gate 1

```powershell
python skill\templates\test_brand_contract.py
python skill\templates\test_identity_continuity.py
python skill\templates\test_pipeline.py
python scripts\test_prepare_site.py
python scripts\check_markdown.py
```

Expected: valid approved authoritative inputs pass; missing sources, stale hashes, reconstruction, unauthorized transformations, unsafe paths, public discovery, false affiliation, and private-path leakage fail.

## 4. Build the private brand kit after Gate 1

```powershell
python scripts\build_all.py i-heart-pr-tours
python skill\templates\verify.py dist\i-heart-pr-tours
python skill\templates\validate_glyph.py dist\i-heart-pr-tours\brand.json dist\i-heart-pr-tours\qc\glyph-report.json
```

Expected: zero verifier problems and zero applicable glyph failures. Every derivative has approved lineage, imported bytes match Gate 1, and public discovery remains disabled.

## 5. Review Gate 2

Open the rendered guide, asset catalog, typography specimens, accessible color examples, implementation artifacts, representative 256/64/32/16 pixel comparisons, continuity report, glyph report, and verifier output under ignored `dist/i-heart-pr-tours/gate-2-r4/`.

Expected: the owner can approve, revise, or reject the complete private delivery. Any affected source or transformation revision returns to Gate 1.

## 6. Run full CI parity after Gate 2

```powershell
python skill\templates\test_glyphkit.py
python scripts\test_package_release.py
python scripts\test_release_contract.py
python scripts\test_prepare_site.py
python scripts\test_identity_continuity_audit.py
python skill\templates\test_brand_contract.py
python skill\templates\test_identity_continuity.py
python skill\templates\test_iconkit.py
python skill\templates\test_pipeline.py
python scripts\check_markdown.py
python scripts\build_all.py
npm --prefix site run lint
npm --prefix site run build
npm --prefix site test
```

Expected: every production kit, source contract, release contract, site route, and accessibility check passes. Generated output remains ignored.

## 7. Repository hygiene

Confirm tracked text is UTF-8 without BOM with LF endings, contains no mojibake or private workstation paths, and contains no generated kit, PDF, raster, registry, site export, archive, or local selector. `git diff --check` must pass before commit.
