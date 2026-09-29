# Implementation Plan: Brand Essentials and Docs Navigation

**Branch**: `codex/068-brand-essentials-docs-navigation` | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

## Summary

Use the S067 source-bound messaging contract and existing kit assets to rebuild the first guide topic as Brand essentials across hosted, portable, and PDF output. Classify every legacy top-of-guide sentence for all eleven brands. Make the docs sidebar footer express the exact published manual version or collapse to a compact theme control for an unpublished candidate.

## Technical Context

**Language/Version**: Python 3.8-compatible generator, TypeScript/React 19 and Next.js 16 site, Node 20 minimum.

**Primary Dependencies**: Existing brand contract, guideline/PDF generators, Fumadocs 16.15.11, generated publication and portal records.

**Storage**: Canonical `brands/*/brand.json`; source-only Spec Kit artifacts under `specs/068-brand-essentials-docs-navigation/`; generated output under ignored `dist/` and `site/out/`.

**Testing**: Focused Python projection tests, portal/HTML/PDF text extraction, site Node and browser checks, full documented aggregate and publication gates.

**Target Platform**: Offline kit guides and public static site.

**Project Type**: Brand compiler and static documentation site.

**Performance Goals**: Reuse the existing parallel CI kit jobs without adding a duplicate serial build.

**Constraints**: Exact approved copy, unchanged logo geometry, WCAG 2.1 AA, no generated artifacts in Git, UTF-8 LF.

**Scale/Scope**: Eleven current production brands and two open Phase 19 issues.

## Constitution Check

- P1: Commit source and Spec Kit evidence only; rebuild generated kits in validation.
- P2: Preserve all logo masters and approved geometry; no new identity decision.
- P3: Retain AA contrast and keyboard/screen-reader access across guides and sidebar.
- P4: Rebuild and verify every production kit, with zero verifier and glyph failures.
- P5: Site reads the generated portal and publication records rather than restating identity values.
- P6: Specification, plan, tasks, analysis, implementation, and verification evidence remain synchronized.

## Design Decisions

1. Normalize essentials from existing canonical fields and delivered assets in a shared Python helper. The portal carries the result; React does not independently author brand-specific text. This avoids a new source schema or invented approval gate.
2. Separate identity words from optional strategy roles using the S067 `visual-guide` approval rule. Historic foundation, promise, scope, and product-boundary fields are inventory evidence, not page content. Three explicitly reviewed `sharp_edge` sources contain visual usage boundaries and remain exact Usage limits text.
3. Render concrete name, relationship, signatures, destinations, and logo usage limits for each brand. Keep detailed rules on the existing Logo, Color, Typography, and Assets pages; navigation describes only sections that render.
4. Use the supported Fumadocs theme-switch slot and the generated publication record for the sidebar. Release status shows the official version link; candidate status gets a compact control. No historical picker is implied.
5. Keep BrandBuilder 3.0.0 as the current unpublished candidate. This slice does not cut a release or alter brand identity bytes; Unreleased records the changed guide presentation.
6. Make `/{brand}/guidelines/brand-essentials/` the canonical first topic in the documentation contract and export compatibility bridges from the former guideline root and Overview URL.

## Project Structure

```text
specs/068-brand-essentials-docs-navigation/  # Spec, disposition inventory, verification
skill/templates/brand_essentials.py            # Shared source-bound projection
skill/templates/gen_guidelines.py              # Portal and portable guide
skill/templates/gen_guide_pdf.py               # PDF guide
site/components/guidelines/                   # Hosted first-page rendering
site/components/documentation-sidebar-theme.tsx
site/lib/documentation-sidebar-publication.mjs
site/app/docs/layout.tsx
site/lib/guidelines.ts
skill/references/documentation-contract.json
site/tests/ and site/scripts/                   # Export and browser assertions
```

## Verification and Handoff

Write failing focused tests before implementation. Rebuild all production kits and run documented source, glyph, PDF, site, accessibility, registry, and publication checks. Record exact evidence in `verification.md`, commit source-only changes, push the branch, open a linked PR, resolve first and at most one requested second Codex review round plus security review, then wait for green required CI before owner merge handoff.
