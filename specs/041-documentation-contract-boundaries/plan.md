# Implementation Plan: Documentation Contract Boundaries

**Branch**: `codex/041-documentation-contract-boundaries` | **Date**: 2026-09-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/041-documentation-contract-boundaries/spec.md`

## Summary

Add one versioned documentation contract beside the existing canons that assigns manual pages, shared implementation facts, surface ownership, navigation, and migration dispositions. Generate one exact per-kit documentation fact record from the already validated consumer contract, use it to render the offline `IMPLEMENTATION.md`, carry the same record into the hosted child-brand portal, and reject drift. Expand the main manual with architecture, interface implementation, verification/versioning, and agent/extension pages. Replace hard-coded site documentation metadata with the governed contract, preserve every current route, and add three server-rendered semantic overview graphics with adjacent text equivalents.

## Technical Context

**Language/Version**: Python 3.8-compatible compiler, validators, and site staging; TypeScript/TSX on Node.js 20+ for the static documentation site

**Primary Dependencies**: Python standard library and existing JSON-schema validator; existing Next.js 16, React 19, Fumadocs, Playwright Chromium, and axe-core site stack; no new runtime dependency

**Storage**: Versioned JSON documentation contract and schema, Markdown manual sources, generated per-kit JSON documentation facts and Markdown implementation guidance, staged site JSON, static HTML; no database or network persistence

**Testing**: Python `unittest`, deterministic-byte comparisons, JSON-schema validation, generated-kit verification, route/disposition checks, TypeScript lint, static export, Node contract tests, Playwright desktop/narrow/no-script/zoom/forced-colors/reduced-motion checks, axe WCAG 2.1 AA, all-brand builds, publication audit, Markdown and encoding checks

**Target Platform**: Offline generated brand kits and the public statically exported Next.js documentation and hosted brand-guide routes

**Project Type**: Static brand and interface compiler with generated offline contracts and a self-hosting documentation site

**Performance Goals**: One deterministic documentation projection per kit; zero generator-time or verification-time network access; no meaningful increase in route interaction latency; documentation validation bounded by the small source and route inventories

**Constraints**: WCAG 2.1 AA; Python 3.8 minimum; Node.js 20 minimum; no committed `dist/`, site export, PDF, raster, archive, registry, or synthetic fixture output; preserve approved identity and all existing public routes; UTF-8 without BOM and LF; keep #193, #194, and #202 separate

**Scale/Scope**: Eight production brands, fifteen governed manual source pages after expansion plus the generated index, eight hosted portals, one bundled implementation contract per kit, five documentation-related public route kinds, three semantic overview graphics

## Constitution Check

*GATE: Must pass before Phase 0 research and after Phase 1 design.*

| Principle | Design response | Status |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit the documentation contract, schemas, Markdown sources, compiler/staging code, site components, tests, and Spec Kit records. Generate kit guidance and site exports only under ignored output roots. | PASS |
| P2. Identity geometry is preserved | Documentation projections read current brand and contract metadata. No brand source, logo binding, path, mask, palette, or artwork transformation changes are planned. | PASS |
| P3. Accessibility has no exemption | The manual, hosted summaries, navigation, and semantic overview graphics receive keyboard, no-script, zoom, forced-colors, reduced-motion, and axe coverage. | PASS |
| P4. Verification precedes publication | Shared facts, dispositions, routes, links, schema, kit verification, all-brand builds, and site accessibility fail closed before publication. | PASS |
| P5. The site consumes generated kits | Hosted contract summaries come from per-kit generated documentation facts staged with the existing portal. The site does not restate brand versions or bindings. | PASS |
| P6. Specifications and releases move together | S041 includes specification, clarifications, checklists, plan, contracts, tasks, analysis, evidence, and changelog. No release is cut. | PASS |

Post-design recheck: PASS. The design uses one governed source contract and one generated per-kit fact record, retains current routes and identity boundaries, and keeps every generated artifact outside source control.

## Project Structure

### Documentation (this feature)

```text
specs/041-documentation-contract-boundaries/
├── checklists/
│   ├── documentation-boundaries.md
│   └── requirements.md
├── contracts/
│   ├── documentation-authority.md
│   ├── migration-disposition.md
│   └── shared-facts.md
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
skill/
├── references/
│   ├── documentation-contract.json
│   ├── documentation-contract.schema.json
│   ├── 10-system-architecture.md
│   ├── 11-interface-implementation.md
│   ├── 12-verification-versioning.md
│   └── 13-agent-integration.md
└── templates/
    ├── documentation_contract.py
    ├── gen_enforcement.py
    ├── gen_guidelines.py
    ├── interface_contract.py
    ├── test_documentation_contract.py
    ├── test_interface_contract.py
    ├── test_pipeline.py
    └── verify.py

scripts/
├── prepare_site.py
└── test_prepare_site.py

site/
├── app/docs/[[...slug]]/page.tsx
├── app/globals.css
├── components/documentation-overviews.tsx
├── components/guidelines/topic-content.tsx
├── lib/guidelines.ts
├── scripts/verify-site.mjs
└── tests/site.test.mjs

.github/workflows/build.yml
CHANGELOG.md
```

**Structure Decision**: Keep documentation policy and manual prose under `skill/references/`, where the skill and site can share them. Compile exact kit facts under `enforcement/` before guideline generation. Site preparation validates the same contract and stages per-kit facts, while TSX renders accessible presentation without becoming a second authority.

## Phase 0: Research and Decisions

1. Inventory existing manual sources, generated implementation guidance, hosted portal data, route generation, navigation, and no-script behavior.
2. Define one documentation contract that can replace site-only description and navigation tables while recording content and route dispositions.
3. Select the minimal shared per-kit fact record that both hosted and bundled projections can consume without copying prose authorities.
4. Define current-hosted versus pinned-offline version authority and reject an unnecessary public historical archive.
5. Select semantic server-rendered HTML for the three graphics so accessibility and no-script behavior do not depend on image export or client JavaScript.

## Phase 1: Design and Contracts

1. Model documentation contracts, pages, topics, surfaces, shared facts, dispositions, and overview graphics in `data-model.md`.
2. Define authority, ownership, and projection boundaries in `contracts/documentation-authority.md`.
3. Define exact shared-fact fields and drift comparison in `contracts/shared-facts.md`.
4. Define source and route inventory expansion plus disposition rules in `contracts/migration-disposition.md`.
5. Provide focused and full validation commands in `quickstart.md`.

## Phase 2: Implementation Strategy

1. Add documentation contract, schema, and negative-first tests for ownership, topics, navigation, dispositions, unsafe paths, and duplicate positions.
2. Implement the Python 3.8 contract loader, shared-fact generator, offline Markdown renderer, portal projection, and drift verifier.
3. Extend consumer contract authority and provenance to include documentation sources and exact generated facts, with schema and tamper tests.
4. Replace site staging hard-coded documentation metadata with contract-derived navigation, descriptions, topic coverage, and route disposition validation.
5. Author the missing manual pages and add the semantic ownership, modes, and improvement-loop component with adjacent text equivalents.
6. Add hosted exact-version summaries and manual cross-links from staged generated facts.
7. Integrate documentation tests into CI parity, run focused suites, build all production kits, build and verify the site, audit publication, and check Markdown, encoding, mojibake, and repository hygiene.

## Complexity Tracking

No constitution violations or justified exceptions are required.
