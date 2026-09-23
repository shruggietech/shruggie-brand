# Implementation Plan: First-Class Light Brand Systems

**Branch**: `codex/050-light-brand-systems` | **Date**: 2026-09-23 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/050-light-brand-systems/spec.md`

## Summary

Complete the existing partial light-guide implementation as one governed brand presentation contract. Validate the optional declaration early, pass it through the generated portal and site records, scope hosted guideline and portfolio styles locally, correct PDF/portable copy and state colors, and add measured light/dark regression gates. The global portfolio and documentation theme remain independent.

## Technical Context

**Language/Version**: Python 3.8+ generator and validation, TypeScript/Next.js on Node 20+

**Primary Dependencies**: Existing BrandBuilder tokens and contrast helpers, Playwright Chromium, Fumadocs UI, Pillow and PDF raster tooling for full-tier checks

**Storage**: Source `brand.json` and generated, ignored kit/site JSON and assets

**Testing**: Python `unittest` modules and full kit verifier, Node site contract tests, Playwright browser and accessibility checks, PDF ground QC

**Target Platform**: Offline kit generation plus static public site in supported desktop/mobile browsers

**Project Type**: Source generator and static website

**Performance Goals**: No extra network fetch or client-only theme flash; existing build and page budgets retained

**Constraints**: WCAG 2.1 AA, source logo byte invariance, source-only commits, Python core tier works without Chromium, dark default compatibility

**Scale/Scope**: Eight production brands, one currently declared light-first; generated PDF, portable HTML, hosted routes, portfolio cards, and verification

## Constitution Check

- **Source-only artifacts**: PASS. Edit `skill/templates/`, `skill/references/`, `scripts/`, `site/`, and `specs/`; do not commit `dist/` or generated site exports.
- **Identity preservation**: PASS. No logo path data or supplied masters change. White wells select presentation only.
- **AA floor**: PASS by design. Evaluate local semantic pairings and fail invalid light configuration rather than waive contrast.
- **Measured and offline verification**: PASS. Use generated token data, PDF/page QC, and existing offline build pipeline.
- **Site consumes generated kits**: PASS. Project mode and semantic colors through generated portal/site records, not manually maintained brand CSS.
- **Spec Kit and release boundary**: PASS. S050 documentation and evidence accompany PR. No tag or release in this slice.

## Project Structure

### Documentation (this feature)

```text
specs/050-light-brand-systems/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/guide-presentation.md
├── quickstart.md
├── tasks.md
├── evidence.md
└── checklists/requirements.md
```

### Source Code (repository root)

```text
brands/i-heart-pr-tours/brand.json
skill/references/canon.schema.json
skill/references/02-kit-anatomy.md
skill/templates/brand_contract.py
skill/templates/gen_guide_pdf.py
skill/templates/gen_guidelines.py
skill/templates/build_kit.py
skill/templates/qc_render.py
skill/templates/test_brand_contract.py
skill/templates/test_pipeline.py
scripts/prepare_site.py
scripts/test_prepare_site.py
site/lib/guidelines.ts
site/components/brand-portfolio.tsx
site/app/(guidelines)/[slug]/layout.tsx
site/app/globals.css
site/tests/site.test.mjs
site/scripts/verify-site.mjs
```

**Structure Decision**: Extend the existing generator-to-site data path and tests. No second theme engine, runtime network service, or downstream consumer mutation.

## Design Sequence

1. Make `guide.surface_mode` a schema-backed, early-validated value with a dark default and explicit light-source preconditions. Validate the same complete light palette when `showcase_surface` selects `light.*`, even if the guide remains dark.
2. Keep a single mode resolver in generator code; use it in PDF, portable HTML, build QC, and emitted portal data.
3. Include the selected guide block and complete dark/light semantic token blocks in the generated portal, project only the relevant mode into each site record, then scope hosted guide and portfolio UI with brand-local CSS variables and data attributes.
4. Preserve explicit dark/light specimen wells while making the document outer ground deterministic. Select white wells from asset metadata and governed showcase surface, never by editing artwork.
5. Add fail-first contract and browser cases, run full production build and site verification, inspect generated contact sheets, and record evidence.

## Post-Design Constitution Check

All six gates above remain PASS. The only deliberate deviation from current implementation is removing the hardcoded dark-only portfolio-card rule and the matching tests, because issue #193 requires a complete light scope for declared light brands. The global shell and dark-brand defaults are preserved.
