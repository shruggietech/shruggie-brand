# Feature Specification: Complete Kit Downloads and Explicit Brand Actions

**Feature Branch**: `codex/024-kit-download-actions`

**Created**: 2026-09-09

**Status**: Implemented and verified

**Input**: Work slice S024 covering GitHub issues #173 and #174.

## User Scenarios & Testing

### User Story 1 - Download a complete, trustworthy brand kit (Priority: P1)

A visitor can download one complete archive for any homepage brand and trust that the archive contains every distributable asset declared by that brand's verified kit.

**Why this priority**: The download is the primary deliverable behind the new homepage action and must be complete before the interface can advertise it.

**Independent Test**: Build every production brand, download each published archive, compare its normalized contents and checksums with the authoritative distributable inventory, and confirm its filename, response behavior, safety, and provenance documentation.

**Acceptance Scenarios**:

1. **Given** a published homepage brand, **When** a visitor activates `Download Kit`, **Then** the correct stable, version-aware archive downloads for that brand.
2. **Given** a generated archive, **When** it is inspected, **Then** every distributable file declared by the verified kit appears exactly once with the expected size and checksum.
3. **Given** a missing, stale, empty, unsafe, duplicated, corrupted, or undistributable expected entry, **When** publication is prepared, **Then** publication fails with an actionable explanation rather than emitting an incomplete archive.
4. **Given** a legitimate redistribution exception, **When** the archive inventory is read, **Then** the omitted delivery and its reason are stated explicitly.

---

### User Story 2 - Choose an explicit brand action on desktop (Priority: P1)

A desktop visitor can inspect a brand card and deliberately choose either its guidelines or complete kit download without the entire card acting as an unlabeled third destination.

**Why this priority**: Explicit actions remove ambiguous navigation and connect the portfolio directly to its two useful outcomes.

**Independent Test**: Render every card at supported desktop widths and operate it with pointer and keyboard, confirming stable geometry, exact actions, correct destinations, visible focus, and reduced-motion behavior.

**Acceptance Scenarios**:

1. **Given** a desktop brand card in its resting state, **When** it receives hover or focus within, **Then** its description yields to `Guidelines` and `Download Kit` actions without resizing the card or shifting the grid.
2. **Given** either revealed action, **When** a visitor moves the pointer to it or tabs into it, **Then** the actions remain available and the selected action works.
3. **Given** unused card space, the brand name, or the brand mark, **When** it is activated, **Then** no implicit navigation occurs.
4. **Given** reduced-motion preferences, **When** action state changes, **Then** content swaps without rotational motion, mirrored text, or a prolonged blank state.

---

### User Story 3 - Browse compact brand actions on mobile (Priority: P1)

A mobile visitor can expand one compact brand row to read its description and use the same two explicit actions with accurate, accessible disclosure behavior.

**Why this priority**: Mobile has no hover and needs a space-efficient interaction that preserves the complete portfolio and action set.

**Independent Test**: Render the portfolio at supported narrow widths, use pointer, touch-equivalent, and keyboard input to expand and collapse every row, and inspect state, focus order, clipping, and action destinations.

**Acceptance Scenarios**:

1. **Given** the mobile portfolio, **When** it first renders, **Then** every brand is a collapsed row showing only its mark and name.
2. **Given** a collapsed row, **When** its semantic header control is activated, **Then** its description, `Guidelines`, and `Download Kit` actions become visible in predictable reading and focus order.
3. **Given** an expanded row, **When** its header is activated again, **Then** the panel collapses and none of its hidden controls remains clickable or keyboard-focusable.
4. **Given** a narrow viewport or 200% zoom, **When** any row is expanded, **Then** its complete content remains visible without horizontal clipping or inaccessible controls.

---

### User Story 4 - Understand third-party attribution once (Priority: P1)

A visitor sees concise markers on applicable brands and one legally meaningful shared third-party disclaimer after the portfolio instead of repeated disclaimer paragraphs inside multiple cards.

**Why this priority**: The disclaimer must remain legally clear while the cards become concise enough for both desktop transitions and mobile rows.

**Independent Test**: Compare the authoritative brand attribution data with rendered desktop and mobile portfolio output, confirming exact marker eligibility, one disclaimer instance, accessible associations, and preserved wording.

**Acceptance Scenarios**:

1. **Given** a brand to which the third-party disclaimer applies, **When** its name is rendered, **Then** it has an accessible marker associated with the shared explanation.
2. **Given** a brand to which the disclaimer does not apply, **When** its name is rendered, **Then** it has no marker.
3. **Given** the complete portfolio, **When** its content is inspected, **Then** the legally meaningful disclaimer appears exactly once after the card or accordion list and no repeated card-level copy remains.

### Edge Cases

- A production kit declares an optional capability that is intentionally unavailable.
- An archive path normalizes to a duplicate, escapes the intended root, or uses an unsafe absolute or parent-relative form.
- A distributable file is empty, missing, stale relative to its manifest, or changes while an archive is assembled.
- Two brands have similarly named artifacts or filenames that could otherwise target the wrong download.
- Pointer movement crosses from revealed card content onto an action near a card boundary.
- Keyboard focus enters or leaves a card without any preceding hover event.
- A viewport crosses the desktop/mobile breakpoint while a mobile row is expanded or a desktop action owns focus.
- JavaScript is unavailable, delayed, or fails after the static page is delivered.
- A long brand name or localized browser font metric increases the collapsed row height.
- Motion is reduced while the theme or breakpoint changes.

## Requirements

### Functional Requirements

- **FR-001**: Every production brand represented on the homepage MUST have exactly one complete downloadable kit archive derived from its final verified distributable inventory.
- **FR-002**: Each archive MUST include every distributable delivery declared by that inventory, including applicable logo, lockup, mark, wordmark, web-icon, application or platform icon, social, token, guideline, licensing, inventory, provenance, and checksum material.
- **FR-003**: Archive assembly MUST reject missing, stale, corrupted, unexpectedly empty, duplicate-normalized, unsafe, or out-of-root entries and MUST NOT publish a partial archive.
- **FR-004**: Any declared asset that cannot legally or technically be redistributed MUST be identified with its reason in the archive documentation rather than silently omitted.
- **FR-005**: Archive contents and paths MUST be stable and deterministic for unchanged verified inputs, and archive filenames MUST identify the brand and current kit version.
- **FR-006**: Each published archive MUST be downloadable from a stable brand-specific destination with correct archive media type and download disposition.
- **FR-007**: The site's published archive MUST correspond to the same verified brand-kit revision used for the rest of that brand's published content.
- **FR-008**: Desktop brand cards MUST preserve their current outer height and grid alignment while replacing the description with exactly two explicit actions, `Guidelines` followed by `Download Kit`, on hover or focus within.
- **FR-009**: Only the two explicit actions inside a desktop card MUST be interactive; the card container, mark, name, and unused space MUST NOT form an implicit navigation target.
- **FR-010**: Desktop action transitions MUST keep actions available while the pointer moves onto them, MUST NOT mirror readable content or expose an excessive blank interval, and MUST become non-rotational under reduced-motion preferences.
- **FR-011**: Mobile brand cards MUST render as a vertical accordion whose collapsed rows show only the brand mark and brand name.
- **FR-012**: Every mobile accordion header MUST be a semantic control with accurate expanded and controlled-region relationships, visible focus, an adequate touch target, and predictable reading order.
- **FR-013**: An expanded mobile row MUST reveal the brand description followed by `Guidelines` and `Download Kit`; a collapsed panel MUST not expose invisible interactive controls.
- **FR-014**: Desktop and mobile variants MUST expose the same brands, descriptions, action labels, and destinations from one authoritative portfolio data contract.
- **FR-015**: Each `Guidelines` action MUST open the correct brand guidelines destination, and each `Download Kit` action MUST download that brand's complete archive.
- **FR-016**: The repeated third-party disclaimer copy MUST be replaced with exactly one section-level disclaimer after the portfolio list while preserving its legally meaningful wording.
- **FR-017**: Applicable brand names MUST carry an accessible marker associated with the shared disclaimer; non-applicable brands MUST not carry a marker.
- **FR-018**: The portfolio MUST remain fully usable with keyboard, pointer, and touch-equivalent input at supported desktop and mobile widths, 200% zoom, light and dark themes, and reduced-motion settings.
- **FR-019**: Core guidelines and download destinations MUST remain available without JavaScript; enhancement state MUST not make a destination unreachable when scripting is unavailable.
- **FR-020**: Automated coverage MUST verify archive completeness and integrity, correct brand-to-archive mapping, desktop and mobile interaction behavior, focus and disclosure state, breakpoint transitions, browser history stability, disclaimer placement, static export, accessibility, and repository hygiene.

### Key Entities

- **Distributable inventory**: The authoritative set of files, metadata, versions, checksums, and declared redistribution exceptions that defines a complete brand kit.
- **Brand kit archive**: A deterministic brand-specific package containing exactly the safe, distributable inventory and its human-readable verification material.
- **Portfolio brand record**: The shared brand name, mark, description, guidelines destination, archive destination, and disclaimer applicability consumed by desktop and mobile presentation.
- **Desktop action state**: The resting or revealed card content state governed by pointer, focus, and motion preferences without changing outer card geometry.
- **Mobile disclosure state**: The expanded or collapsed relationship between a semantic brand header control and its action panel.
- **Shared disclaimer**: One section-level attribution statement with accessible references from only the applicable brand markers.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every homepage brand has exactly one downloadable archive whose normalized file set, sizes, and checksums match 100% of its authoritative distributable inventory.
- **SC-002**: Rebuilding an unchanged brand kit twice produces archives with identical normalized contents and bytes.
- **SC-003**: All desktop cards expose exactly two working actions through both pointer and keyboard interaction with zero measurable card-height or grid-position change.
- **SC-004**: All mobile rows begin collapsed, report accurate disclosure state, reveal every required content item when expanded, and leave zero hidden interactive controls focusable when collapsed.
- **SC-005**: Every guidelines and download action resolves to the correct brand-specific destination with zero cross-brand or missing-target errors.
- **SC-006**: The portfolio contains exactly one shared third-party disclaimer, and 100% of applicable brand markers have an accessible association while non-applicable brands have none.
- **SC-007**: The documented repository validation reports zero production-kit verification problems, zero glyph failures, zero archive-integrity failures, zero accessibility violations, and zero repository-hygiene violations.

## Assumptions

- The authoritative distributable inventory is the existing verified generated-kit inventory rather than a separate hand-maintained site list.
- Generated archives remain build and release artifacts and are never committed to Git.
- Existing legally meaningful third-party disclaimer wording remains authoritative; S024 changes placement and association, not substance.
- The existing desktop card dimensions and portfolio grid are the visual baseline for the no-layout-shift requirement.
- The existing responsive breakpoint system remains authoritative unless measured behavior requires a narrowly documented adjustment.
- A deterministic archive means byte-identical output for identical inputs, including stable entry ordering, timestamps, metadata, and compression settings.
- Issue #175's root-brand-page removal and issues #179 and #180's navigation restructuring remain outside S024.

## Traceability

- GitHub #173: FR-001 through FR-007, FR-014, FR-015, FR-020, SC-001, SC-002, SC-005, SC-007
- GitHub #174: FR-008 through FR-020, SC-003 through SC-007
