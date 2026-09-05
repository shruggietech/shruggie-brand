# Implementation Plan: Brand Platform Refresh

**Branch**: `codex/006-brand-platform-refresh` | **Date**: 2026-09-05 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/006-brand-platform-refresh/spec.md`

## Summary

Deliver issues #100 through #103 as one public-platform reset. Remove the committed synthetic brand and fixed expected-count logic, retain regression coverage through temporary test data, enrich the generated brand record with canonical square marks, rebuild the public homepage and shared company chrome, migrate authoritative skill references into a statically exported Fumadocs experience, and add complete route metadata and discovery files. The slice updates the constitution because the previous version required the fixture that the owner has explicitly ordered removed.

## Technical Context

**Language/Version**: Python 3.8 minimum; TypeScript 5.9; Next.js 16.3.4; React 19.2.8; Node.js 20 minimum

**Primary Dependencies**: Fumadocs Core 16.14.3, Fumadocs UI 16.14.3, Fumadocs MDX 15.2.3, zbsearch 3.3.4, Tailwind CSS 4.2.4, Playwright 1.62.1, axe-core Playwright integration, existing brandbuilder dependencies

**Storage**: Committed brand and documentation sources; ignored generated kit output under `dist/`; ignored generated site data, copied assets, and derived MDX under `site/generated/` and `site/public/`

**Testing**: Python unit tests for production discovery and documentation derivation; existing generator and release tests; TypeScript type checking; static Next.js export; in-process static server with headless Playwright and axe checks; emitted metadata, sitemap, robots, semantic table, overflow, keyboard, and fixture-absence assertions

**Target Platform**: Static GitHub Pages deployment at `https://brand.shruggie.tech/`, modern mobile and desktop browsers, Ubuntu GitHub Actions, and Windows local development without visible child consoles

**Project Type**: Python-driven brand asset generator plus a statically exported Next.js documentation and portfolio site

**Performance Goals**: First-load public pages use only local assets; the generated search index remains client-side and static; portfolio layout remains stable with at least twice the current production-card count; site verification completes within the existing CI job budget

**Constraints**: Preserve all logo path and pixel data; WCAG 2.1 AA; no committed generated artifacts; no runtime network dependency; UTF-8 without BOM and LF; no public fixed brand count; no public marketing use of "canon"; no third Codex review request; owner-only merge

**Scale/Scope**: Five current production brands, ten authoritative reference documents, homepage plus brand and download routes, one documentation tree, complete static metadata and discovery output, four GitHub issues, and one official pull request

## Constitution Check

| Principle | Design response | Gate |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit only source, tests, and Spec Kit records. Generate MDX, copied kit assets, search data, and static export during the build. Replace the committed fixture with temporary test data. | PASS after the owner-authorized v2.0.0 amendment |
| P2. Identity geometry is preserved | Copy existing generated logo, mark, favicon, and social-preview files without editing or normalizing their geometry. | PASS |
| P3. Accessibility has no exemption | Use verified semantic foreground roles, 44-pixel targets, focus states, reduced motion, semantic tables, and automated axe and overflow gates. | PASS |
| P4. Verification precedes publication | Run focused tests, all five production builds, glyph validation, site export, browser checks, and hosted CI before owner handoff. | PASS after the owner-authorized v2.0.0 amendment |
| P5. The site consumes generated kits | Portfolio values, logos, icons, guidelines, registries, specimens, and downloads continue to come from verified `dist/` output. | PASS |
| P6. Specifications and releases move together | S006 includes specification, clarification, plan, tasks, analysis, evidence, issue traceability, changelog decisions, and review processing. | PASS |

Post-design re-check: PASS. Constitution 2.0.0 preserves the verification floor while replacing a publicly visible committed fixture with isolated test-time input.

## Project Structure

### Documentation for this feature

```text
specs/006-brand-platform-refresh/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── generated-content.md
│   └── public-site.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source code

```text
.specify/memory/constitution.md
scripts/
├── build_all.py
├── prepare_site.py
└── test_prepare_site.py
skill/templates/
└── test_pipeline.py
site/
├── app/
│   ├── (site)/
│   ├── docs/
│   ├── static.json/
│   ├── layout.tsx
│   ├── robots.ts
│   └── sitemap.ts
├── components/
├── generated/
├── lib/
├── scripts/
├── tests/
├── mdx-components.tsx
└── source.config.ts
```

**Structure Decision**: Keep the existing Python-to-static-site boundary. Use an App Router route group for the custom portfolio shell, a Fumadocs docs layout for documentation routes, and one root provider and metadata definition. Generate derived MDX under the already ignored `site/generated/` boundary so `skill/references/*.md` remains authoritative.

## Technical Approach

1. Amend constitution 1.0.0 to 2.0.0 because deleting the committed fixture is a backward-incompatible governance change explicitly authorized by the owner.
2. Restrict normal build discovery to source-only production brands under `brands/`. Replace tests that copy the deleted fixture with temporary copies derived from a production source in an isolated test directory.
3. Refactor site preparation into testable functions. Reject non-production records, duplicate slugs, missing verified assets, and stale generated public brand directories. Add canonical square mark paths to generated brand records.
4. Convert each authoritative skill reference to generated MDX with frontmatter, stable ordering, and public terminology rewriting outside code spans and fenced code. Generate the documentation index and navigation metadata in the same pass.
5. Add the Fumadocs MDX build, static search index, docs layout, page metadata, and ShruggieTech theme using the sibling Fragcap project as the structural reference.
6. Move custom public routes under a shared site route group. Add the approved homepage copy, generated portfolio cards, compact company mark, layered dark surfaces, immediate skill download, clearer documentation action, and a useful company footer.
7. Copy canonical ShruggieTech favicon, touch-icon, manifest icon, and 1280 by 640 social-preview assets from verified generated output to stable root paths. Generate route metadata, robots policy, and sitemap from shared brand and documentation records.
8. Add Python and browser regression tests before completing each corresponding implementation. Update CI to run the site browser verification after static export.
9. Run the complete five-brand pipeline, release-contract dry run, site type check and export, browser and accessibility verification, encoding and mojibake checks, and generated-artifact hygiene audit.
10. Push the branch, open one official pull request, process the automatic Codex round, optionally request exactly one second round, resolve every actionable comment, and halt with the pull request open for the owner.

## Issue Traceability

| Issue | Primary delivery area | Independent done signal |
| --- | --- | --- |
| #100 | Homepage, shared chrome, generated portfolio | Approved copy, five generated cards, responsive company-aligned presentation, useful footer |
| #101 | Metadata, icons, social previews, robots, sitemap | Complete absolute emitted metadata and exact public route inventory |
| #102 | Fumadocs documentation | Searchable responsive docs and semantic tables for every known affected page |
| #103 | Fixture retirement | No active synthetic brand source or public artifact, temporary regression coverage remains |

## Complexity Tracking

| Deviation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| Constitution major amendment | Constitution 1.0.0 mandates the exact committed fixture the owner ordered removed | Silently ignoring P1 and P4 would invalidate the mandatory Spec Kit gate |
| Generated MDX layer | Fumadocs needs source files at build time while skill references must remain authoritative | Committing a duplicate docs tree would violate the single-source requirement and create drift |
