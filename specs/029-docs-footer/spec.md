# Feature Specification: Documentation Footer Removal

**Feature Branch**: `codex/029-docs-footer`

**Created**: 2026-09-10

**Status**: Draft

**Input**: GitHub issue #191 requests removal of the shared marketing footer from documentation pages because it clutters the interface and separates critical documentation navigation from the page content.

## User Scenarios & Testing

### User Story 1 - Continue through documentation without obstruction (Priority: P1)

A documentation reader reaches the end of any documentation page and can immediately use the documentation previous or next navigation without encountering the unrelated global marketing footer first.

**Why this priority**: Previous and next links are critical navigation within a sequential documentation experience. The marketing footer currently interrupts that flow and makes the relevant controls harder to discover.

**Independent Test**: Export the site, open the documentation index and a representative article at desktop and narrow viewport widths, and confirm that each page contains no global site footer while its expected documentation pagination remains present and reachable.

**Acceptance Scenarios**:

1. **Given** the documentation index, **When** a reader reaches the end of the page, **Then** the next-page navigation follows the content without a global marketing footer between them.
2. **Given** a documentation article with previous or next destinations, **When** a reader reaches the end of the page, **Then** the available documentation navigation remains visible, reachable, and adjacent to the content.
3. **Given** a narrow viewport or keyboard-only navigation, **When** a reader traverses the end of a documentation page, **Then** no global footer interrupts the documentation navigation order.

---

### User Story 2 - Retain the marketing footer where intended (Priority: P2)

A visitor to the main marketing site continues to receive the established ShruggieTech footer and its approved destinations.

**Why this priority**: The correction must remain scoped to documentation pages and must not regress the existing marketing-site footer contract.

**Independent Test**: Open the homepage and confirm that exactly one global site footer remains with the approved ordered links and browsing-context behavior.

**Acceptance Scenarios**:

1. **Given** the homepage, **When** a visitor reaches the end of the page, **Then** the established global site footer remains present exactly once.
2. **Given** the retained global footer, **When** its destinations are inspected, **Then** their labels, order, targets, and opener-isolation policy remain unchanged.

### Edge Cases

- The documentation index has only a forward pagination destination, while middle articles can have both previous and next destinations and the final article can have only a previous destination.
- Documentation pages must retain their sidebar, mobile menu, table of contents, no-script hierarchy, metadata, and structured data after the footer is removed.
- Per-brand guideline portals already exclude the global marketing footer and must remain unchanged.
- Empty space formerly associated with the embedded footer must not leave a misleading visual gap before documentation pagination.

## Requirements

### Functional Requirements

- **FR-001**: Every route under `/docs/` MUST omit the global ShruggieTech marketing footer.
- **FR-002**: Every documentation page MUST retain its applicable previous and next navigation destinations after the marketing footer is removed.
- **FR-003**: Documentation pagination MUST follow the documentation content without an intervening global footer region or footer-sized empty gap.
- **FR-004**: Documentation navigation order MUST remain logical and complete for keyboard, pointer, touch, narrow viewport, and no-script use.
- **FR-005**: The main marketing site MUST retain exactly one global footer with the existing approved destination labels, order, link targets, and browsing-context policy.
- **FR-006**: The documentation sidebar, mobile navigation, table of contents, page titles, body content, metadata, structured data, canonical routes, and pagination sequence MUST remain unchanged.
- **FR-007**: Per-brand guideline portals MUST continue to omit the global marketing footer and retain their dedicated guide footer behavior.
- **FR-008**: Automated coverage MUST distinguish marketing-site footer presence from documentation and guideline footer absence and MUST verify documentation pagination at desktop and narrow viewport widths.

## Success Criteria

### Measurable Outcomes

- **SC-001**: One hundred percent of exported `/docs/` pages contain zero global site footer regions.
- **SC-002**: One hundred percent of documentation pages retain every applicable previous and next destination in the established pagination sequence.
- **SC-003**: The homepage retains exactly one global footer with zero label, order, target, or opener-isolation discrepancies.
- **SC-004**: Desktop and narrow viewport verification reports zero hidden, obstructed, or unreachable documentation pagination destinations.
- **SC-005**: The documented repository gate reports zero accessibility violations, zero broken internal links, zero static-export failures, and zero repository-hygiene violations.

## Assumptions

- `/docs/` is the complete route boundary for project documentation pages affected by issue #191.
- The shared footer component and its approved records remain authoritative for marketing-site routes; this slice changes only where that component is rendered.
- The existing Fumadocs pagination component remains the authoritative previous and next navigation surface.
- No brand identity geometry, palette, typography, documentation copy, or route structure changes are in scope.

## Traceability

- GitHub #191: FR-001 through FR-008 and SC-001 through SC-005.
