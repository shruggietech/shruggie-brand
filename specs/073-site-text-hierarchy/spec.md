# Feature Specification: Site text hierarchy and containment

**Feature Branch**: `codex/073-site-text-hierarchy`

**Created**: 2026-10-27

**Status**: Implemented, pending PR review

**Input**: S073 combines #310, #311, and #335 into one site presentation slice. Keep portfolio titles and affiliation markers inside cards, place the portfolio introduction beneath its heading, and make bibliography entries compact and scannable.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read complete portfolio titles (Priority: P1)

A visitor can read every brand name and any affiliation marker in its card, including DanceWithMe865, without characters crowding or crossing the card's usable edge. A title becomes smaller when needed for clearance while remaining comfortably readable.

**Why this priority**: The current DanceWithMe865 marker is clipped in the owner screenshot and its association with the third-party notice must remain clear.

**Independent Test**: Inspect cards at supported desktop and mobile widths, with enlarged text, and measure the complete title and marker against the card's content area.

**Acceptance Scenarios**:

1. **Given** the DanceWithMe865 card at the narrowest desktop grid width, **when** its name and marker are displayed, **then** both remain fully visible with at least 24 CSS pixels of clearance from the usable right edge.
2. **Given** other current brand cards, **when** the title treatment changes, **then** their names remain readable and visually consistent without unnecessary reduction.
3. **Given** a synthetic title longer than DanceWithMe865, **when** space is insufficient even after bounded size reduction, **then** the title wraps within the card without losing characters or separating an affiliation marker from its name.
4. **Given** a visitor who enlarges the browser's default font size, **when** a long desktop title no longer fits on one line, **then** it retains the enlarged rem-based font size and wraps inside the card with its marker visible.

---

### User Story 2 - Scan individual references (Priority: P1)

A reader can scan the References page as a sequence of compact entries, each with a clearly associated ID and separately legible Source, Class, Use, and Limit fields.

**Why this priority**: The current paragraphs blend four fixed fields into a wall of text and make the bibliography hard to use.

**Independent Test**: Review representative short and long entries at desktop and narrow widths, navigate by heading and link, and verify every entry has the same four readable fields.

**Acceptance Scenarios**:

1. **Given** a reference entry, **when** a reader scans it, **then** Source, Class, Use, and Limit appear as distinct rows or lines in that order within one compact visual group.
2. **Given** a long source link or Use/Limit field, **when** the page narrows or text is enlarged, **then** the content wraps without clipping or horizontal page scrolling.
3. **Given** an existing inbound reference link, **when** it is followed, **then** it reaches the same reference ID and all original source links and meanings remain available.

---

### User Story 3 - Associate the portfolio description with its heading (Priority: P2)

A visitor sees the approved identity-spectrum sentence directly beneath Our Portfolio and before the cards, so the introduction reads as part of that heading group.

**Why this priority**: The owner's screenshot shows the current description detached to the right of its heading.

**Independent Test**: Read the section visually and in document order at desktop and narrow widths, and confirm its exact heading, description, and anchor still work.

**Acceptance Scenarios**:

1. **Given** the home page, **when** the portfolio section appears, **then** Selected work, Our Portfolio, and the approved description form one left-aligned text group immediately before the cards.
2. **Given** a narrow viewport or enlarged text, **when** the sentence wraps, **then** it remains beneath the heading without clipping, overlap, or horizontal page scrolling.
3. **Given** the Explore Our Portfolio link, **when** it is followed, **then** it reaches the same section and the heading continues to name that section.

### Edge Cases

- Exceptionally long brand titles must remain complete; no approved name may be abbreviated, truncated, or hidden.
- Affiliation markers must remain attached to the correct name and retain the accessible third-party explanation.
- Long bibliography URLs and prose must wrap without changing the link target or reference text.
- Presentation changes must not alter unrelated section headings, documentation pages, brand copy, generated kits, or logo geometry.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The portfolio MUST display complete brand titles and affiliation markers within each card's content area at supported widths and enlarged text sizes.
- **FR-002**: At the standard browser default font size, the title treatment MUST reduce size only as needed for measured clearance, keep text readable, and permit contained wrapping when a bounded reduction is insufficient. At enlarged browser default font sizes, it MUST preserve the rem-based title size and wrap instead of cancelling the visitor's enlargement.
- **FR-003**: DanceWithMe865 and its asterisk MUST remain visible with at least 24 CSS pixels of right-side clearance at the narrowest desktop card width.
- **FR-004**: The portfolio description MUST appear immediately beneath Our Portfolio in the same visual group and before the cards, retaining the exact approved sentence, Selected work eyebrow, section heading, and anchor.
- **FR-005**: Each References entry MUST show Source, Class, Use, and Limit separately and in that order, visually grouped with its ID heading.
- **FR-006**: Existing reference IDs, inbound anchors, source links, citations, and wording MUST remain intact.
- **FR-007**: The changed presentation MUST preserve meaningful reading and heading order, keyboard access, text selection, and the accessible third-party notice.
- **FR-008**: The changed surfaces MUST meet the repository's WCAG 2.1 AA floor, including measured contrast, readable enlargement, and reflow at 320 CSS pixels without loss or two-dimensional scrolling.
- **FR-009**: Verification MUST cover current and unusually long names, representative short and long references, exact approved portfolio copy, and unrelated section-heading behavior.

### Key Entities

- **Portfolio heading group**: The eyebrow, heading, and approved description that introduce the card grid.
- **Portfolio title**: A brand's exact name with any affiliation marker and accessible explanation.
- **Reference entry**: A stable ID heading with Source, Class, Use, and Limit content and links.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every current portfolio title and marker is fully visible at the tested desktop, 390px, and 320px widths; DanceWithMe865 has at least 24 CSS pixels of clearance at the narrowest desktop card width.
- **SC-002**: Every References entry presents all four fields as distinct, ordered parts of one compact unit, with all existing anchors and links still resolving.
- **SC-003**: The portfolio introduction remains directly below its heading at all tested widths and preserves the exact approved wording and section link.
- **SC-004**: At 200% zoom, 125% and 200% browser default font sizes, and 320 CSS pixels, the changed content is readable without clipping, overlap, or two-dimensional page scrolling; long desktop titles retain their enlarged rem-based size.
- **SC-005**: The full documented site and production-kit validation passes, including zero kit or glyph failures and no new WCAG 2.1 AA findings.

## Assumptions

- The three linked issues define the approved scope and wording. This slice changes presentation, not canonical brand messages or identity assets.
- The 24-pixel clearance is a measurable implementation threshold selected after the initial rendered check showed that 8 pixels did not prompt a reduction for DanceWithMe865.
- References content is authoritative; only its field structure and presentation may change.
- The uncommitted S072 messaging work is independent and remains in its existing checkout. S073 starts from the synced mainline.
