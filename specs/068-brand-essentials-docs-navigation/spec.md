# Feature Specification: Brand Essentials and Docs Navigation

**Feature Branch**: `codex/068-brand-essentials-docs-navigation`

**Created**: 2026-09-29

**Status**: Implemented and locally verified; external PR gates pending

**Input**: S068 implements #298 and #299 after the source-bound messaging work in S067.

## User Scenarios & Testing

### User Story 1 - Find usable brand essentials (Priority: P1)

As a designer or writer, I can open a brand's first guideline page and quickly identify its approved name, relationship, words, visual signatures, delivered assets, and concrete usage limits.

**Why this priority**: The existing opening mixes product scope and generic promise copy with identity guidance.

**Independent Test**: For every production brand, compare the rendered first page against canonical source, delivered assets, and the eleven-brand disposition inventory.

**Acceptance Scenarios**:

1. **Given** an approved visual-guide message, **when** the page renders, **then** it appears with its exact role and text.
2. **Given** no approved visual-guide message, **when** the page renders, **then** it does not substitute a descriptor, promise, or invented filler.
3. **Given** delivered marks, colors, and type, **when** a reader follows the essentials page, **then** the reader reaches the exact asset and detailed rule pages.

### User Story 2 - Get consistent guidance in every guide (Priority: P1)

As a kit reader, I find the same approved field meanings and literal brand copy in the hosted, portable, and PDF guides, while each format links or points to its own detailed assets.

**Why this priority**: Different guide formats currently emphasize different historical fields and can imply unsupported product claims.

**Independent Test**: Check extracted HTML, portal JSON, and PDF text for all eleven brands, including optional-section and table-of-contents behavior.

**Acceptance Scenarios**:

1. **Given** product scope or operational claims in historical foundation fields, **when** guides render, **then** those claims do not appear as identity rules.
2. **Given** approved words or a concrete visual prohibition, **when** each guide renders, **then** the literal source wording stays unchanged and is labeled for its actual purpose.
3. **Given** an omitted optional section, **when** navigation renders, **then** its heading is absent from the contents list.

### User Story 3 - Understand the documentation sidebar footer (Priority: P2)

As a manual reader, I see either a plainly labeled current manual version with a valid release destination or a compact theme control, with no empty-looking footer row.

**Why this priority**: The current Fumadocs sidebar shows a bordered row with blank space beside its theme switcher.

**Independent Test**: Exercise the docs index and a nested manual page at desktop, narrow mobile, and zoomed widths in both publication-status states.

**Acceptance Scenarios**:

1. **Given** a published manual record, **when** the sidebar renders, **then** it shows the exact BrandBuilder version and an official release link.
2. **Given** an unpublished candidate, **when** the sidebar renders, **then** it presents only the theme control in a compact wrapper and does not imply a selectable release.
3. **Given** either state, **when** a keyboard or screen-reader user switches theme, **then** the control has a name, visible focus, and no horizontal overflow.

### Edge Cases

- Preserve punctuation, casing, and exact approved wording; exclude unresolved or surface-restricted messages.
- Treat a missing brand-specific visual rule as absent rather than inventing one.
- Keep the original asset paths and logo geometry; a guide can point to delivered variants but cannot fabricate a variant.
- If the publication record is a review candidate, a future release URL is not presented as an active release link.
- A documentation version label is not a version selector; historical docs require actual archived content.

## Requirements

### Functional Requirements

- **FR-001**: An eleven-brand inventory MUST classify each current overview, foundation, promise, boundary, relationship, and relevant guidance sentence by source, reader purpose, and disposition before migration.
- **FR-002**: The first guideline topic MUST be Brand essentials at `/{brand}/guidelines/brand-essentials/`, with concrete name and relationship, approved words when present, visual signatures, asset destinations, and usage limits. The old Overview URL MUST remain a compatibility bridge.
- **FR-003**: Public guides MUST show only approved `visual-guide` message roles and canonical visual instructions; product scope, unapproved strategy, and generic fallback prose MUST be omitted from identity guidance.
- **FR-004**: Hosted, portable, and PDF guide representations MUST use the same source meanings and exact approved copy; optional sections and contents entries MUST match rendered headings.
- **FR-005**: All mark, color, typography, and asset references MUST resolve to canonical source or delivered kit assets, with links or precise local paths to detailed rules.
- **FR-006**: Optional strategy material MUST be separately labeled and shown only when its source decision explicitly permits visual-guide use.
- **FR-007**: Docs sidebar presentation MUST remove the unexplained empty area. A displayed version MUST come from the publication record and link to an existing official release; candidate builds MUST avoid an inactive release link.
- **FR-008**: Theme switching MUST preserve keyboard access, screen-reader labeling, visible focus, light/dark behavior, and responsive fit.
- **FR-009**: Regression checks MUST cover rich and sparse brand records, all eleven production brands, rendered heading/contents parity, exact source projection, and release/candidate sidebar states.
- **FR-010**: The full documented kit, glyph, PDF, site, accessibility, registry, and publication validation MUST pass before PR handoff.

### Key Entities

- **Brand essentials**: The first guide topic's source-bound name, relationship, approved words, visual signatures, asset destinations, and usage limits.
- **Disposition item**: An existing brand sentence or field with its source path, category, evidence, and retained or moved surface.
- **Publication record**: Exact BrandBuilder version, status, and official release URL used by the manual.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All eleven production brands have every current top-of-guide field and sentence classified in the migration inventory.
- **SC-002**: No rendered Brand essentials page contains old product scope, an inferred promise, or an empty fallback sentence.
- **SC-003**: Approved wording and field roles match source in hosted, portable, and PDF output for all eleven brands; every contents link points to a rendered heading.
- **SC-004**: The docs index and nested manual page show no empty-looking bordered sidebar area at desktop, narrow mobile, and zoomed widths, in release and candidate states.
- **SC-005**: Every production kit has zero verifier and glyph failures, and the full documented site and publication validation passes with zero WCAG 2.1 AA violations.

## Clarifications

- 2026-09-29: The current production inventory has eleven brands, superseding the eight-brand issue intake count.
- 2026-09-29: S068 may classify historical strategy and product claims and remove them from visual-guide projection; it does not newly approve or rewrite brand-specific copy.
- 2026-09-29: The existing `sharp_edge` text for I Heart PR Tours, Local Companion, and Scruggs Tire & Alignment is visual usage guidance. It stays source-bound in Usage limits; product-oriented `sharp_edge` content stays out of identity guidance.
- 2026-09-29: A candidate publication is not a live release. Its sidebar uses a compact theme control; a release build may show a source-bound version and release link.

## Assumptions

- S067's canonical `messaging`, `guidance`, generated portal, and publication records are the current source contract.
- The two issues share the Phase 19 documentation experience and can pass one PR/CI/review cycle.
- Current shipped brand assets and approved geometry remain unchanged.
