# Implementation Plan: Documentation Footer Removal

**Branch**: `codex/029-docs-footer` | **Date**: 2026-09-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/029-docs-footer/spec.md`

## Summary

Deliver issue #191 by removing the shared marketing `Footer` from the documentation page composition while preserving Fumadocs pagination, documentation shell behavior, and the homepage footer contract. Add source and rendered regressions that prove all documentation routes omit `.site-footer`, representative desktop and narrow pages retain reachable `.docs-pagination` destinations, and the homepage still exposes the approved footer once.

## Technical Context

**Language/Version**: TypeScript 5.9 and JavaScript ES modules on Node.js 20 minimum; Python 3.8 minimum remains part of the aggregate repository gate

**Primary Dependencies**: Next.js 16.3 static export, React 19.2, Fumadocs 16.14, Playwright 1.62.1, axe-core

**Storage**: Source-controlled TSX, JavaScript tests, and Spec Kit records; generated site content and static exports remain ignored

**Testing**: Node source-contract tests, TypeScript, Next.js static export, Playwright rendered-site checks, axe WCAG audits, aggregate production-kit verification

**Target Platform**: GitHub Pages static export in evergreen desktop and mobile browsers

**Project Type**: Static brand and project documentation website backed by a deterministic build pipeline

**Performance Goals**: Remove unused documentation-page markup without adding client work, network requests, or route-specific runtime branching

**Constraints**: WCAG 2.1 AA floor; existing documentation routes, hierarchy, content, metadata, and pagination remain stable; existing marketing-footer records remain unchanged; no generated output is committed

**Scale/Scope**: Eleven documentation routes, one shared documentation page composition, one homepage footer, one source-contract suite, and one rendered-site verification suite

## Constitution Check

### Pre-design gate

- **P1 PASS**: Only site source, tests, and Spec Kit records are committed. Generated site content and exports remain ignored.
- **P2 PASS**: No logo, lockup, icon, or path geometry changes.
- **P3 PASS**: Keyboard, narrow viewport, minimum target, focus, and WCAG checks remain blocking for retained documentation pagination.
- **P4 PASS**: The full documented repository gate rebuilds and verifies production kits before publication.
- **P5 PASS**: The site remains the owner of documentation rendering and shell chrome; no generated brand values are restated.
- **P6 PASS**: S029 uses the complete Spec Kit flow and retains issue, CI, review, changelog, and verification evidence.

### Post-design gate

- **PASS**: Removing `Footer` from the documentation page composition is the smallest change that prevents the marketing region from entering the rendered document or accessibility tree.
- **PASS**: The shared footer component and marketing-site layout remain unchanged, preserving the approved footer destination policy.
- **PASS**: Source and browser regressions verify both route-scope absence and retained contextual pagination.

## Project Structure

### Documentation (this feature)

```text
specs/029-docs-footer/
├── checklists/
│   └── requirements.md
├── contracts/
│   └── documentation-footer-contract.md
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
site/
├── app/
│   ├── docs/[[...slug]]/page.tsx
│   └── globals.css
├── components/
│   └── footer.tsx
├── scripts/
│   └── verify-site.mjs
└── tests/
    └── site.test.mjs

CHANGELOG.md
```

**Structure Decision**: Keep route-surface ownership explicit in the existing layouts and pages. The marketing route-group layout continues to compose the shared `Footer`; the documentation page stops composing it and retains its Fumadocs `footer` pagination property.

## Implementation Strategy

### Phase 0: Lock the route-surface contract

Add failing source assertions that documentation page source neither imports nor renders the shared `Footer`, while the marketing layout still renders it and the footer component records remain unchanged.

### Phase 1: Remove the documentation marketing footer

Delete the unused `Footer` import and `<Footer />` element from the documentation catch-all page and remove its now-obsolete documentation-specific footer spacing selector without changing `DocsPage` pagination, content, metadata, hierarchy, or structured-data composition.

### Phase 2: Verify rendered navigation and route boundaries

Replace the rendered documentation footer expectation with checks that every documentation route has zero `.site-footer` elements. Verify representative desktop and narrow documentation pages retain applicable pagination links with minimum target size, visible focus, valid destinations, and no obstruction. Preserve existing homepage and guideline footer checks.

### Phase 3: Validate and publish

Run focused source, type, build, browser, accessibility, full production-kit, release-contract, Markdown, encoding, mojibake, and repository-hygiene gates. Record evidence, commit, push under the operator's explicit authorization, open a pull request closing #191, process review findings, and wait for green required CI.

## Complexity Tracking

No constitution violation or additional abstraction is required. Conditional rendering inside the shared footer was rejected because route scope belongs to page composition and a conditional would couple a stable marketing component to pathname awareness. CSS-only hiding was rejected because it would preserve unnecessary markup and risk leaving an accessibility or spacing defect.
