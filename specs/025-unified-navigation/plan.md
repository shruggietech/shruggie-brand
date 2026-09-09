# Implementation Plan: Unified Site Navigation and Route Consolidation

**Branch**: `codex/025-unified-navigation` | **Date**: 2026-09-09 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/025-unified-navigation/spec.md`

## Summary

Deliver issues #175, #180, and #179 as one route-contract migration. Remove generated brand-root pages, make the stable downloads route the single Assets destination, emit authoritative navigation metadata alongside generated portal and documentation records, and render nested brand and documentation trees from those records. Preserve all content, documentation URLs, kit archives, direct downloads, and schema-valid shadcn endpoints while extending static, no-script, input-mode, zoom, link, and accessibility verification.

## Technical Context

**Language/Version**: Python 3.8 minimum for generation and route contracts; TypeScript 5.9 and JavaScript ES modules on Node.js 20 minimum for the site

**Primary Dependencies**: Next.js 16.3 static export, React 19.2, Fumadocs 16.14, Playwright 1.62.1, axe-core, Python standard library

**Storage**: Source-controlled Python, TSX, CSS, JSON-contract definitions, and Spec Kit records; generated `dist/`, `site/generated/`, `site/public/generated/`, static exports, and browser evidence remain uncommitted

**Testing**: Python `unittest`, Node source-contract tests, TypeScript, Next.js static export, Playwright rendered-site checks, axe WCAG audits, aggregate production-kit verification

**Target Platform**: GitHub Pages static export in evergreen desktop and mobile browsers, including keyboard, touch-only, no-script, and 200% zoom use

**Project Type**: Deterministic build pipeline plus static brand and project documentation website

**Performance Goals**: Navigation trees derive in one linear pass over each small generated inventory; no network or client-side fetch is required; core links remain server-rendered

**Constraints**: WCAG 2.1 AA floor; byte-preserved logo geometry; site values and content sourced from verified kits; static hosting has no route middleware or per-brand redirect facility; documentation canonical URLs stay stable

**Scale/Scope**: Six public brands, eight brand destinations per portal including three Identity children, ten documentation destinations, three GitHub issues, and one shared route contract

## Constitution Check

### Pre-design gate

- **P1 PASS**: Only generator, site source, tests, and Spec Kit records are committed. Generated portals and exports remain ignored.
- **P2 PASS**: No mark, lockup, icon, or path geometry changes.
- **P3 PASS**: Semantic hierarchy, current state, expanded state, keyboard, touch, no-script, focus, zoom, and WCAG checks remain blocking.
- **P4 PASS**: All production kits and generated portals are rebuilt before publication, with fail-closed route and registry validation.
- **P5 PASS**: Brand content and inventories remain generated-kit outputs; the site adds navigation metadata and rendering without restating brand values.
- **P6 PASS**: S025 uses the complete Spec Kit flow and retains issue, CI, review, changelog, and verification evidence.

### Post-design gate

- **PASS**: The design removes duplicate routes and navigation models rather than creating compatibility pages.
- **PASS**: One generated navigation contract feeds desktop, mobile, and no-script presentation.
- **PASS**: Assets consolidation preserves the stable downloads path and verified generated files while eliminating the duplicate guidelines Assets route.

## Project Structure

### Documentation (this feature)

```text
specs/025-unified-navigation/
├── checklists/
│   ├── navigation-contract.md
│   └── requirements.md
├── contracts/
│   └── navigation-route-contract.md
├── data-model.md
├── evidence.md
├── plan.md
├── quickstart.md
├── research.md
├── spec.md
└── tasks.md
```

### Source Code (repository root)

```text
skill/templates/
├── gen_guidelines.py
└── test_pipeline.py

scripts/
├── prepare_site.py
└── test_prepare_site.py

site/
├── app/
│   ├── (guidelines)/[slug]/layout.tsx
│   ├── (guidelines)/[slug]/downloads/page.tsx
│   ├── (guidelines)/[slug]/guidelines/[[...topic]]/page.tsx
│   ├── docs/layout.tsx
│   └── globals.css
├── components/guidelines/
│   ├── downloads-content.tsx
│   └── topic-content.tsx
├── lib/
│   ├── documentation.ts
│   ├── guidelines.ts
│   └── routes.ts
├── scripts/verify-site.mjs
└── tests/site.test.mjs
```

**Structure Decision**: Lift the guideline layout to the brand route-group boundary so both `/guidelines/` and the stable `/downloads/` Assets page share one navigation tree. Generate navigation assignments with portal and documentation records, then construct Fumadocs trees from those records rather than maintaining component-local lists.

## Implementation Strategy

### Phase 0: Lock route and hierarchy contracts

Add failing generator, route, source, and rendered tests for removed brand roots, stable Assets routes, exact nested navigation, one-to-one content mapping, stable documentation URLs, registry resolution, and semantic accessibility states.

### Phase 1: Migrate the brand route contract

Remove `brand` route records and structured-data brand entities, point brand breadcrumbs at guidelines, exclude root pages and obsolete `/guidelines/assets/` routes, and keep downloads, archives, registries, and nested delivery endpoints stable. Move the downloads page under the guideline route group and combine its direct resource list with the generated asset library.

### Phase 2: Publish and render authoritative hierarchies

Extend generated portal topics with concise labels, ordered section membership, and canonical paths. Extend generated documentation records with the approved section and label mapping. Build both navigation trees from those records, preserving document titles and URLs while exposing semantic nested groups and active ancestors.

### Phase 3: Validate every access mode

Exercise exact tree shape, active child and parent presentation, keyboard, pointer, touch-only, no-script, narrow viewport, 200% zoom, content uniqueness, link integrity, route absence, schema-valid registries, static export, and WCAG AA across all brands and documentation pages.

### Phase 4: Validate and publish

Run focused Python and site tests, full production kit builds, release archive certification, static export, browser accessibility checks, repository hygiene, encoding, and mojibake scans. Commit and push under the operator's explicit authorization, open a PR closing #175, #179, and #180, process every initial review finding, request at most one second `@Codex` review, resolve all threads, and wait for green CI.

## Complexity Tracking

No constitution violation is required. The route-group layout relocation is the smallest design that lets the stable downloads URL become the sole Assets destination inside the same semantic brand-navigation shell. Retaining a second `/guidelines/assets/` page was rejected because it would contradict #180's one-destination requirement; removing `/downloads/` was rejected because it would contradict #175's stable-route contract.
