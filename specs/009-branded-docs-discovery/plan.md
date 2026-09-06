# Implementation Plan: Branded Documentation and Discovery Completion

**Branch**: `codex/009-docs-discovery-completion` | **Date**: 2026-09-05 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/009-branded-docs-discovery/spec.md`

## Summary

Complete Phase 11 in one cohesive site slice by restoring the documentation component contract, applying canonical ShruggieTech semantic styling, and introducing one generated route descriptor graph consumed by metadata, structured data, social previews, breadcrumbs, the sitemap, copied guideline pages, tests, and browser verification. Preserve authoritative documentation under `skill/references/`, shipped logo geometry, static export, local assets, and the existing production-kit gates.

## Technical Context

**Language/Version**: Python 3.8 minimum for preparation and source tests; TypeScript 5.9 and JavaScript ES2022 on Node.js 20 minimum for the static site and browser verification

**Primary Dependencies**: Next.js 16.3.4 App Router, React 19.2.8, Fumadocs UI 16.14.3, Fumadocs MDX 15.2.3, Pillow, Playwright 1.62.1, and axe-core

**Storage**: Committed Markdown, Python, TypeScript, TSX, CSS, and JSON source; generated MDX, route records, social PNGs, copied kit assets, and static export remain ignored build artifacts

**Testing**: Python `unittest` entry points, TypeScript compilation, Next.js static export, Playwright Chromium assertions, axe WCAG 2.1 AA auditing, full five-kit verification, glyph checks, release-contract certification, Markdown and repository hygiene checks

**Target Platform**: Static GitHub Pages deployment at `https://brand.shruggie.tech/`, desktop and mobile browsers from 360 through 1280 CSS pixels, light and dark documentation themes

**Project Type**: Hybrid Python build pipeline and statically exported Next.js documentation and portfolio application

**Performance Goals**: Generate all route records and social assets within the existing site preparation step; serve every sitemap URL directly as an exported file; avoid network dependencies and runtime metadata generation

**Constraints**: WCAG 2.1 AA without waiver; static export and trailing slashes; local fonts and identity assets; no shipped geometry edits; Python 3.8 compatibility; no committed generated images or site output; exactly two Codex review rounds maximum

**Scale/Scope**: Five public brands, three routes per brand, the homepage, the documentation index, nine nested reference pages, and their route-specific metadata and preview assets

## Constitution Check

*GATE: Passed before Phase 0 research and passed again after Phase 1 design.*

| Principle | Design response | Gate |
|-----------|-----------------|------|
| P1. Sources are committed and artifacts are rebuilt | Commit only generator, site, test, and Spec Kit source. Generate MDX, route JSON, social PNGs, screenshots, and static export under ignored paths. | PASS |
| P2. Identity geometry is preserved | Reuse generated and shipped ShruggieTech and brand assets without tracing, normalization, or path edits. | PASS |
| P3. Accessibility has no exemption | Test both themes, desktop and mobile widths, keyboard controls, non-color states, overflow, and WCAG 2.1 AA. | PASS |
| P4. Verification precedes publication | Retain full five-kit verification and glyph gates, then add source, static-export, browser, structured-data, and asset assertions before publication. | PASS |
| P5. The site consumes generated kits | Generate route and preview descriptors from verified production records and source-derived docs rather than restating brand values in pages. | PASS |
| P6. Specifications and releases move together | Maintain complete S009 artifacts and issue traceability. Do not create a release or merge from this task. | PASS |

## Architecture Decisions

### Generate one page descriptor graph

`scripts/prepare_site.py` will write ignored `site/generated/routes.json` after public brands and documentation are known. Each record owns its route kind, stable key, normalized trailing-slash path, absolute canonical URL, document title, description, social-preview record, and ordered breadcrumbs. A TypeScript loader will provide exact lookup for App Router pages, while copied guideline HTML receives the same record during preparation.

This replaces the current independent URL assembly in Next.js metadata, sitemap generation, tests, and Python guideline injection. It is the smallest design that makes every discovery identifier provably equal.

### Generate one deterministic social PNG per route

Preparation will rebuild a validated `site/public/social/` directory from local fonts and canonical generated marks. Each route receives a stable 1280 by 640 PNG with route-specific visible title and category context. Route metadata supplies matching alternative text, dimensions, and media type. Physical assets are preferred over dynamic image routes because they also serve copied guideline HTML, remain fully static, and can be decoded directly during CI.

### Restore framework-owned code blocks and add explicit notice authoring

The site will stop replacing the Fumadocs fenced-code component with a raw `pre`. The default component already supplies a cohesive panel and accessible copy control. CSS will distinguish inline code without overriding syntax tokens. Authoritative references will use portable GitHub-style NOTE, WARNING, and CAUTION blockquote markers that preparation converts deterministically into the framework's `info`, `warn`, and `error` component syntax. Ordinary blockquotes and fenced literals remain unchanged.

### Bind documentation roles to canonical tokens

Documentation theme variables and scoped component rules will use values already emitted by the generated ShruggieTech token and registry layers. Marketing headings will be scoped to marketing surfaces, and documentation will receive a compact type scale through an owned `docs-page` hook because the installed Fumadocs output does not contain the assumed `.fd-docs-page` selector. Active and focus states will use official green plus border, underline, weight, or shape cues. No parallel near-match palette will be introduced.

### Verify rendered geometry without committed screenshots

Browser checks will capture review screenshots under an ignored repository-local test-results path and record visual inspection in `evidence.md`. Durable regressions will use DOM, computed-style, geometry, accessibility, and asset-semantic assertions. This honors issue requirements without violating the prohibition on committed generated raster exports.

### Serialize structured data defensively

Next.js routes will emit shared structured-data graphs with `<` escaped as `\u003c`. Python-injected guideline graphs will use equivalent safe JSON serialization. Route normalization will reject external origins, unsafe paths, duplicate keys, duplicate canonicals, and duplicate social asset paths.

## Project Structure

### Documentation (this feature)

```text
specs/009-branded-docs-discovery/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── documentation-rendering.md
│   ├── documentation-theme.md
│   └── route-metadata.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
scripts/
├── prepare_site.py
└── test_prepare_site.py

skill/references/
└── 04-toolchain.md

site/
├── app/
│   ├── (site)/
│   ├── docs/
│   ├── globals.css
│   ├── layout.tsx
│   └── sitemap.ts
├── components/
│   └── structured-data.tsx
├── generated/
│   └── routes.json                 # ignored, generated
├── lib/
│   ├── layout.shared.tsx
│   ├── metadata.ts
│   └── routes.ts
├── public/
│   └── social/                     # ignored, generated
├── scripts/
│   └── verify-site.mjs
├── tests/
│   └── site.test.mjs
└── mdx-components.tsx

CHANGELOG.md
docs/decisions.md
```

**Structure Decision**: Extend the existing preparation and static-site seams. Route facts originate in Python because that step already combines verified brands, documentation sources, and copied guideline pages. TypeScript consumes the generated contract without recreating the inventory.

## Phased Approach

### Phase 0: Research and contracts

1. Confirm current Fumadocs fenced-code and callout contracts, Next.js metadata behavior, static-export trailing-slash behavior, and safe JSON-LD rendering.
2. Define the canonical route, documentation rendering, and theme contracts.
3. Map every #108, #109, and #111 acceptance criterion to a measurable requirement and test seam.

### Phase 1: Failing tests and shared route foundation

1. Add source tests for selective notices, fenced content, route normalization, duplicate rejection, breadcrumbs, preview descriptors, and safe guideline metadata.
2. Add emitted-site expectations for exact metadata, structured data, preview assets, sitemap equality, code panels, copy controls, navigation uniqueness, theme values, viewport density, and screenshots.
3. Implement the generated descriptor graph, preview composition, and TypeScript loader.

### Phase 2: Documentation rendering and identity

1. Restore the framework code-block contract and bind semantic notice components.
2. Remove duplicate documentation navigation.
3. Scope marketing and documentation type systems, bind canonical semantic roles, and install a compact existing ShruggieTech identity treatment.
4. Validate both themes and responsive states before discovery integration.

### Phase 3: Metadata and discovery integration

1. Convert all App Router pages and copied guidelines to descriptor-driven metadata.
2. Emit page-appropriate structured-data graphs and breadcrumbs without unsafe or unsupported company claims.
3. Generate the sitemap from the descriptor graph and make browser verification enforce direct, exact URL resolution.

### Phase 4: Aggregate verification and publication

1. Run focused source and site tests, full production builds, release certification, agent-contract sync, static export, browser and accessibility verification, and repository hygiene.
2. Record evidence, changelog entries, identity and accessibility impact, and current task completion.
3. Commit, push, publish the S009 pull request, process the automatic review, request at most one second review, resolve every thread, verify latest-head CI, and halt for owner merge.

## Issue Traceability

| Issue | Primary requirements | Closure gate |
|-------|----------------------|--------------|
| #108 | FR-001 through FR-006, FR-013, FR-014, FR-025 through FR-030 | All code, notice, navigation, keyboard, overflow, screenshot, export, and aggregate gates pass on merged main |
| #109 | FR-007 through FR-014, FR-027 through FR-030 | Canonical token, density, identity, responsive, screenshot, and AA gates pass on merged main |
| #111 | FR-015 through FR-028, FR-030 | Every emitted route, graph, image, and URL relationship passes on merged main |

## Scope Control

- Do not edit brand JSON identity values or shipped path geometry.
- Do not introduce a second documentation source tree.
- Do not commit generated MDX, routes, preview PNGs, screenshots, kits, archives, or static output.
- Do not alter unrelated generator, release, or dependency behavior.
- Do not request more than the automatic review and one explicit `@Codex` review.
- Do not merge the pull request.

## Post-Design Constitution Re-check

The design preserves source-only Git history, generated-site consumption, identity geometry, WCAG 2.1 AA, production verification, and Spec Kit traceability. The new route graph reduces duplicated truth rather than adding another authored source. No constitution exception or amendment is required.

## Complexity Tracking

No constitution violations require justification.
