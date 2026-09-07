# Implementation Plan: Hosted Guidelines Portal Rebuild

**Branch**: `codex/019-guidelines-portal-rebuild` | **Date**: 2026-09-07 | **Spec**: [spec.md](spec.md)

## Summary

Replace the S017 single-page hosted guideline document with statically generated, multi-page brand portals. Extend the verified kit output with a structured portal payload, project that payload into generated site content, render it through the existing Fumadocs navigation and page primitives, and add dedicated color and asset-library components. Preserve a concise portable guide as a download, keep manifests and brand records authoritative, repair landing typography and topic footers, and validate all five production brands end to end.

## Technical Context

**Language/Version**: Python 3.8 minimum; TypeScript 5.9; React 19.2; Next.js 16.3 App Router; Node.js 20 minimum

**Primary Dependencies**: Python standard library, ColorAide, Pillow, Fumadocs 16.14, existing Playwright and axe-core verification

**Storage**: Committed generator and site source; generated portal payloads and the typed site registry under ignored `dist/` and `site/generated/`; static downloads under ignored `site/public/`

**Testing**: Python unittest pipeline and publication contract tests, five-kit aggregate build, TypeScript lint, Next static export, Playwright browser verification, axe-core, Markdown and encoding checks

**Target Platform**: Static `brand.shruggie.tech` routes plus a network-independent portable HTML guide

**Project Type**: Source-first Python generator with a statically exported Next.js documentation site

**Performance Goals**: Server-render complete topic collections; bounded asset summaries independent of delivery count; client enhancement limited to library search, filters, color copying, and active-section feedback

**Constraints**: WCAG 2.1 AA, keyboard and touch access, 360px through desktop layouts, 200 percent zoom, reduced motion, no-script core access, Python 3.8 compatibility, no committed generated output, no identity or palette changes

**Scale/Scope**: Five production brands; eight topic families per brand where authoritative content exists; complete logo and platform inventories from existing manifests

## Constitution Check

| Principle | Treatment | Result |
| --- | --- | --- |
| P1 Sources only | Commit generator, publisher, site components, tests, and Spec Kit records. Keep kit output, generated MDX, static exports, and screenshots outside Git. | PASS |
| P2 Identity preserved | Consume existing logo and palette values without changing geometry, bytes, or canonical color values. | PASS |
| P3 Accessibility | Make navigation, disclosures, copy actions, search, filters, details, footer controls, responsive text, zoom, and no-script access part of the blocking browser matrix. | PASS |
| P4 Verification first | Rebuild and verify all production kits, run browser and publication contracts, and retain zero kit and glyph failures before push. | PASS |
| P5 Site consumes kits | Generate a structured portal contract beside the portable guide, then project verified output into site-generated content without hand-authored brand facts. | PASS |
| P6 Spec Kit | Keep specification, requirements review, design, tasks, analysis, implementation, and evidence synchronized under S019. | PASS |

Post-design recheck: PASS. No constitution exception is required.

## Project Structure

```text
specs/019-guidelines-portal-rebuild/
|-- spec.md
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- evidence.md
|-- checklists/
|   |-- requirements.md
|   `-- experience.md
|-- contracts/
|   |-- portal-content.md
|   `-- portal-navigation.md
`-- tasks.md

skill/templates/gen_guidelines.py
skill/templates/test_pipeline.py
scripts/prepare_site.py
scripts/test_prepare_site.py
site/lib/guidelines.ts
site/lib/routes.ts
site/components/guidelines/
site/app/(guidelines)/[slug]/guidelines/
site/app/globals.css
site/scripts/verify-site.mjs
site/tests/site.test.mjs
CHANGELOG.md
skill/CHANGELOG.md
```

**Structure Decision**: `gen_guidelines.py` continues to create the portable guide and additionally emits `guidelines/portal.json`. `prepare_site.py` validates and consumes that verified payload, copies the portable HTML into the brand download tree, and generates one typed site data registry. The hosted route constructs a Fumadocs page tree directly from that registry and uses the existing documentation framework for navigation and page structure, while purpose-built React components render topic, color, asset, and instruction data. No brand values or manifest inventory are duplicated in site source.

## Implementation Phases

1. Pin failing generator, publication, route, layout, and browser contracts for the complete five-brand matrix.
2. Refactor guideline extraction into a stable portal payload while simplifying the portable guide to a concise offline reference.
3. Project verified portal payloads into generated MDX topics and extend canonical route, metadata, sitemap, and social-preview records.
4. Build the brand-neutral guideline shell with persistent desktop navigation, mobile disclosure, in-page outline, safe fragment offsets, and separated footer utilities.
5. Build compact HEX-first color rows and the task-oriented asset library with representative summaries, detail inventories, document treatments, rendered instructions, search, filters, query state, announcements, and no-script collections.
6. Apply the landing-page heading contract and finish responsive, accessibility, task-flow, encoding, and full-repository validation.
7. Publish the PR, resolve all first-round review findings, optionally request one second Codex review round, and stop after CI and review convergence.

## Complexity Tracking

| Decision | Why Required | Simpler Alternative Rejected |
| --- | --- | --- |
| Add a structured portal payload alongside portable HTML | The hosted site needs page-level content and asset semantics without parsing presentation HTML or restating brand facts. | Rewriting or slicing the generated HTML at publication would preserve S017's presentation coupling and remain brittle. |
| Build Fumadocs page trees from the generated registry | Meaningful static topic URLs and existing documentation navigation require page records known at build time, but generated MDX wrappers would duplicate routing metadata. | A client-side pseudo-router would weaken direct URLs, no-script access, metadata, and static export. |
| Use dedicated color and asset components | These topics need stable disclosures, filtering, announcements, details, and measured layout contracts that prose-only MDX cannot express safely. | Hand-authored per-brand pages would violate the generated-kit authority boundary. |
