# Quickstart: Validate ESO Weave Provenance and Kit

## Prerequisites

- Work from `codex/020-eso-weave-provenance-kit` with a clean source tree.
- Fetch `origin/main` in both Shruggie Brand and ESO Weave without disturbing unrelated working changes.
- Use the repository Python environment and site dependencies documented in `CONTRIBUTING.md`.
- Treat `dist/`, site exports, and proof rasters as disposable generated output.

## Stage 1: Source and Gate 1

1. Compare the recorded ESO Weave snapshot with the fetched default-branch head.
2. Recompute every `source-inventory.json` SHA-256 and fixed-font metadata record.
3. Byte-compare the contained mark and glyph against upstream.
4. Run the source-contract and approval-gate tests.
5. Generate the ignored Gate 1 proof packet.
6. Inspect four sizes on light and dark surfaces, then record the explicit owner decision before derivative construction.

Expected result: the source inventory is complete, authoritative bytes match, negative contract tests pass, and derivative generation remains blocked while Gate 1 is pending.

## Stage 2: Private Complete Kit

After Gate 1 approval:

```powershell
python scripts/build_all.py eso-weave
```

Inspect the generated manifest, logo and icon families, fixed fonts and licenses, framework bindings, enforcement rules, guideline portal, UI specimen, PDF, and migration notes. Run the ESO Weave `validate_glyph.py`, `verify.py`, affiliation scan, image QC, PDF QC, pagination, and mojibake checks.

Expected result: the private kit is complete with zero glyph failures, zero verifier problems, no prohibited affiliation claims, and the required vendor boundary. Site preparation still excludes ESO Weave while Gate 2 is pending.

## Stage 3: Gate 2 and Publication

Generate the ignored Gate 2 packet, inspect the final rendered guide and UI specimen, compare derivative hashes to Gate 1, review every verification result, and enumerate the exact public surfaces. Record owner approval before enabling public projection.

After Gate 2 approval, run full validation:

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
python skill/templates/probe.py
python scripts/build_all.py
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected result: six production kits build cleanly, ESO Weave appears only on the approved generated site and registry surfaces, existing brands do not drift, and repository hygiene remains clean.
