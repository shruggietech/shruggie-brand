# Implementation Plan: Phase 13 Brand Site Polish

**Branch**: `codex/012-brand-site-polish` | **Date**: 2026-09-05 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/012-brand-site-polish/spec.md`

## Summary

Complete issues #120 through #126 as one source-driven site slice. Correct the canonical ShruggieTech application-icon background, select existing colored lockup variants, establish viewport-specific landing navigation, normalize documentation labels and the Variance Contract title at their generating sources, apply canonical CTA and link roles, and strengthen source plus browser verification so regeneration cannot restore the rejected presentation.

## Technical Context

**Language/Version**: Python 3.8 minimum for generators and tests, Python 3.12 in the primary hosted build, TypeScript 5.9, Node.js 20 minimum with Node.js 24 in hosted CI

**Primary Dependencies**: Next.js 16 App Router static export, React 19, Fumadocs UI 16, Fumadocs MDX 15, Playwright 1.62, axe-core, Pillow, existing ShruggieTech generator templates

**Storage**: Versioned JSON and Markdown source, generated ignored `dist/` kits, generated ignored site content, and static `site/out/` export

**Testing**: Python unittest scripts, Node test runner, TypeScript checking, Playwright browser assertions, axe WCAG 2.1 AA audits, source and artifact hygiene scans

**Target Platform**: Public static GitHub Pages site at `https://brand.shruggie.tech`, desktop and mobile browsers, dark and light themes

**Project Type**: Source-driven static website backed by a Python brand-kit generator

**Performance Goals**: Preserve the 26-route static export with no new runtime network dependency, client data fetch, or route expansion

**Constraints**: Preserve imported identity geometry byte for byte, consume generated kit assets, keep generated artifacts out of Git, retain public paths, use UTF-8 without BOM and LF, pass WCAG 2.1 AA, and stop after at most two Codex review rounds

**Scale/Scope**: Seven linked Phase 13 issues spanning one brand source, one documentation source, the site materializer, shared layout, landing content, documentation pagination, global styles, and complete verifier

## Constitution Check

*GATE: Passed before research and passed again after design.*

- **P1 Sources and rebuilt artifacts**: PASS. Changes remain in `brands/`, `skill/references/`, generator tests, and `site/`; `dist/`, generated content, screenshots, and exports remain ignored.
- **P2 Identity geometry**: PASS. The slice changes only the application-icon background token and selection of existing generated variants. No mark pixels, path data, source hashes, or wordmark geometry change.
- **P3 Accessibility**: PASS. CTA roles, interaction states, focus, touch targets, both themes, and reduced motion are mandatory browser gates with no waiver.
- **P4 Verification before publication**: PASS. Regression-first source tests, complete kit checks, static export, browser verification, and hosted CI precede owner merge.
- **P5 Site consumes generated kits**: PASS. Favicons and lockups continue to be copied from the verified ShruggieTech kit; the site does not author duplicate identity files.
- **P6 Specifications and releases move together**: PASS. S012 includes the complete Spec Kit ledger, issue traceability, changelog entry, and official reviewed pull request. No release is in scope.
- **Post-design re-check**: PASS. The contracts preserve every constitutional boundary and introduce no exception.

## Project Structure

### Documentation (this feature)

```text
specs/012-brand-site-polish/
├── checklists/
│   └── requirements.md
├── contracts/
│   ├── identity-contract.md
│   ├── presentation-contract.md
│   └── review-ledger.md
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
brands/shruggietech/brand.json
skill/references/00-variance-contract.md
scripts/
├── prepare_site.py
└── test_prepare_site.py
site/
├── app/
│   ├── (site)/page.tsx
│   ├── docs/[[...slug]]/page.tsx
│   └── globals.css
├── components/footer.tsx
├── lib/layout.shared.tsx
├── scripts/verify-site.mjs
└── tests/site.test.mjs
CHANGELOG.md
```

**Structure Decision**: Retain the existing source-to-kit-to-site pipeline. Canonical brand and documentation inputs change at their sources, the materializer selects generated assets and emits metadata, shared site files render the responsive contract, and the existing complete verifier gains fail-closed semantic and visual assertions.

## Implementation Phases

### Phase 0: Regression-first contract

Add source and materialization assertions for the black icon background, colored lockup mapping, canonical terminology, and responsive inventory before changing implementation. Extend the browser gate with representative semantic, computed-style, reduced-motion, favicon color, and pagination resting-state checks that fail against the current site.

### Phase 1: Canonical identity and terminology

Change only the application-icon background field to the canonical void token, map dark and light site surfaces to existing generated colored lockup variants, rename the documentation root at its generator, and shorten the authoritative Variance Contract source title without changing slugs or routes.

### Phase 2: Responsive layout and interaction hierarchy

Use Fumadocs' supported `on: nav` and `on: menu` link filtering for the exact desktop/mobile landing inventories. Bind primary actions to the generated CTA-safe orange token, retain green secondary emphasis, add scoped orange underline motion for eligible text links, color documentation list and code-string roles, and give Fumadocs pagination an explicit class with persistent branded states.

### Phase 3: Complete verification and review

Rebuild generated source, run Python and site CI parity, inspect the 12-image route-theme-width matrix, verify encoding and artifact boundaries, publish the PR with all seven closure links plus #133, process the automatic review, optionally request exactly one second round, and halt for the owner merge ritual.

## Complexity Tracking

No constitutional violations or complexity exceptions are required.
