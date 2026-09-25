# Feature Specification: Dark Portfolio Cards

- **Feature Branch**: `codex/055-dark-portfolio-cards`
- **Created**: 2026-09-25
- **Status**: Approved for implementation
- **Input**: Emergency homepage regression: no brand may initially appear on a white portfolio card; the IHPRT mark must remain legible. The owner also approved reduced marks on the lander.

## User Scenarios & Testing

### User Story 1 - Read every brand on a dark card (Priority: P1)

As a visitor, I see every portfolio brand on a dark card with readable text and mark at desktop and mobile sizes, regardless of its own brand-page presentation.

**Independent Test**: Inspect initial desktop cards and collapsed mobile disclosures in both site themes; assert every card has a dark background and WCAG AA text contrast.

**Acceptance Scenarios**:

1. **Given** the homepage loads, **when** a brand has a light brand-page treatment, **then** its portfolio card and mobile disclosure still start dark.
2. **Given** the IHPRT card, **when** the homepage loads, **then** its approved dark card color and legible heart are shown.
3. **Given** a future brand with a white card source, **when** site publication runs, **then** publication rejects that source rather than presenting a white portfolio card.

### User Story 2 - Recognize compact marks (Priority: P1)

As a visitor, I see each brand's approved reduced mark in the small homepage icon tile, including the IHPRT heart, without shrinking a full lockup into a thumbnail.

**Independent Test**: Verify all homepage desktop and mobile icon URLs load the published approved reduced-color SVG for their brand; compare IHPRT's presentation visually.

## Requirements

- **FR-001**: Every homepage desktop portfolio card and mobile disclosure MUST initially use a dark background, including brands whose own showcase is light.
- **FR-002**: Homepage titles, descriptions, action links, and focus indicators MUST remain readable to WCAG 2.1 AA.
- **FR-003**: Each homepage icon MUST use that brand's approved reduced-color mark from its verified kit.
- **FR-004**: The brand's own landing page and guide MUST retain their independently approved showcase surface and mark treatment.
- **FR-005**: Publication MUST reject a missing, malformed, white, or insufficiently dark portfolio surface before export.
- **FR-006**: The fix MUST preserve source logo geometry, source/artifact boundaries, and formal release validation.

## Success Criteria

- **SC-001**: Zero initially white portfolio cards or mobile disclosures among all published brands in both site themes.
- **SC-002**: Every portfolio icon loads its approved reduced mark, and all measured card copy meets 4.5:1 contrast.
- **SC-003**: Light brand-page presentation remains intact.

## Assumptions

- The governed dark `surfaces.card` value is the appropriate homepage surface for every published brand; a brand's `showcase_surface` continues to govern its own page.
