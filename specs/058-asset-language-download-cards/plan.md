# Implementation Plan: Shared Asset Language and Distinct Download Cards

**Branch**: `codex/058-asset-language-download-cards` | **Date**: 2026-09-26 | **Spec**: [spec.md](spec.md)

## Summary

Implement #283's glossary and semantic asset grammar as a shared source-level publication contract, then use it for #284's one-design-per-card hosted and portable libraries. Keep every approved logo derivative and its Gate 2 manifest unchanged. Add separately verified descriptive aliases and an old-to-new map for direct consumers. Publish clear labels, first-use explanations, and accessible cards without changing guideline page routes.

## Technical Context

**Language/Version**: Python 3.8 minimum; TypeScript/Next.js on Node 20 minimum.
**Primary Dependencies**: Python standard library, Pillow, existing JSON Schema, Next.js, React, existing site design system.
**Storage**: Source under `skill/references/` and `skill/templates/`; ignored generated kits and site exports.
**Testing**: Python pipeline/contract tests, all eight kits, glyph checks, site lint/build/verify, publication audit and reader-task inspection.
**Target Platform**: Portable brand kits and static hosted brand portal.
**Project Type**: Brand-kit compiler and static site.
**Performance Goals**: Preserve bounded representative previews and avoid duplicate cards for aliases; no new runtime service.
**Constraints**: Existing Gate 2 derivative paths and bytes remain fixed; WCAG 2.1 AA; existing direct paths survive; no generated artifacts committed.
**Scale/Scope**: Eight brands, source-level glossary, descriptive delivery aliases, hosted/portable/PDF/manual terms, and per-design downloads grouping.

## Constitution Check

- **P1**: Only source, contracts, docs, and tests are committed; kit/site outputs remain ignored.
- **P2**: Gate 2 derivative inventory and approved social image digests remain untouched. Alias bytes are copies of approved derivatives and verified separately.
- **P3**: Expanded cards retain AA contrast, visible focus, keyboard and screen-reader semantics at rendered size.
- **P4**: Full kit/glyph and site gates run; alias validity and grouping are semantic checks, not shape-only assertions.
- **P5**: Hosted portal consumes generated asset catalog and kit files. Site does not author independent asset meanings.
- **P6**: Spec, plan, tasks, evidence, source, versions, and changelog stay synchronized. No release is cut in this slice.

All principles pass at design time and must be rechecked after implementation.

## Design Decisions

1. **Approval boundary**: Preserve `logos/approval.json` and its derivative set. Add descriptive publication aliases in a separate governed alias index after derivative approval; verify byte identity and provenance. Renaming existing derivatives would invalidate owner approval for all brands.
2. **Asset grammar**: Model purpose, form, layout, color treatment, actual background, recommended surface, foreground ink, size, and format independently. Icon alpha maps to clear or opaque file background; light/dark appearance maps to intended viewing surface. Use `wide` in reader-facing labels for the legacy `horizontal` layout; keep legacy source values mapped explicitly. Concatenating `kind+variant+role+appearance` repeats terms and conflates surface with ink.
3. **Card identity**: Group by semantic design axes, with size, format, and aliases inside a card. The web icon generator reuses artwork for favicon, touch, and installable files, so these delivery roles share a card only when their full, reduced, or source-preserved variant matches. Maskable artwork stays separate. Prefer an SVG face or the smallest raster at least 320 pixels on its shorter side, with the largest supplied raster as fallback. Reuse one Python grouping helper for hosted portal JSON and portable HTML. Site renders catalog values rather than recomputing classification.
4. **Names and compatibility**: Prefer descriptive new filenames in download labels and links, while preserving old files. Publish a machine-readable old-to-new path map and true alias provenance. Existing social-preview aliases stay in approved inventory. Site redirects alone cannot satisfy offline ZIP consumers.
5. **Manual placement**: Publish the glossary immediately after Kit Anatomy in the main manual and make no-script navigation count derive from the generated document inventory. This inserts one new pagination step between Kit Anatomy and Interview while keeping every existing page URL stable.
5. **Glossary**: Add a governed main-manual page and compact embedded/linked first-use reference in brand guides, PDF, and hosted Assets/Logo topics. Avoid independent definitions in renderers.
6. **Version**: Bump BrandBuilder and site to 2.5.0 for backward-compatible generator/verifier and delivery additions. Preserve Brand Canon 1.6.0 and brand identity versions because governed identity meaning and pixels do not change. Do not publish a release in S058.
7. **Scope boundary**: Leave guideline page URLs intact for #285. The changed asset file names require aliases; page-route migration is a separate navigation and SEO operation.

## Project Structure

```text
skill/references/asset-glossary.md           # authoritative meanings
skill/references/documentation-contract.json # governed manual route
skill/templates/asset_language.py            # semantic axes, names, aliases
skill/templates/gen_guidelines.py             # catalog and portable guide
skill/templates/gen_guide_pdf.py              # printed guide definitions
skill/templates/verify.py                     # alias and inventory validation
site/components/guidelines/                  # catalog presentation
site/lib/guidelines.ts                        # generated portal types
site/scripts/verify-site.mjs                  # published catalog checks
skill/templates/test_pipeline.py              # grouping and alias regressions
specs/058-asset-language-download-cards/      # spec and evidence
```

## Delivery Sequence

Write failing grammar/grouping/alias tests, implement semantic classification, add checked publication aliases and map, render glossary and truthful labels across kit/site/manual/PDF, update versions and changelog, run required validation, inspect reader tasks, commit, push, open PR, resolve CI and review comments within two rounds, then hand off for merge.

## Complexity Tracking

No constitution exception is needed. A separate publication alias index is necessary because the approved derivative manifest binds its original filenames.
