# Feature Specification: Portfolio Card Consistency

**Feature Branch**: `codex/033-portfolio-card-consistency`

**Created**: 2026-09-13

**Status**: Complete

**Input**: User description: "Resolve GitHub issues #199 and #200 together by normalizing homepage portfolio cards, repairing their accessible actions and bottom spacing, presenting I Heart PR Tours like the other dark cards, and replacing the accumulating disclaimer list with one short generic third-party notice."

## User Scenarios & Testing

### User Story 1 - Scan a coherent portfolio (Priority: P1)

A visitor scanning the homepage portfolio sees one visually coherent dark card system with consistently white titles, descriptions, and action labels, including the I Heart PR Tours entry.

**Why this priority**: Mixed text colors and a single white card disrupt the portfolio hierarchy and make some content appear disabled or unrelated.

**Independent Test**: View all portfolio cards at desktop and mobile widths and verify that every visible title, description, and action label is white on a dark card surface while each approved logo remains unchanged.

**Acceptance Scenarios**:

1. **Given** the desktop portfolio grid, **When** all eight cards are compared in their default states, **Then** every title and description is white and every card uses the shared dark presentation language.
2. **Given** the I Heart PR Tours card, **When** it is compared with adjacent cards, **Then** its surface follows the same dark showcase treatment while its approved logo and brand accent remain intact.
3. **Given** the mobile portfolio accordions, **When** entries are opened and closed, **Then** titles, descriptions, and action labels remain white and visually consistent.

---

### User Story 2 - Operate accessible card actions (Priority: P1)

A keyboard, pointer, touch, reduced-motion, or zoom user can reveal and activate Guidelines and Download Kit without hidden focus targets, unreadable states, clipped content, or layout movement.

**Why this priority**: Portfolio actions are primary navigation and download controls, so contrast and operability failures block users from reaching the showcased work.

**Independent Test**: Exercise every action reveal and dismissal path by pointer and keyboard, including Escape, focus traversal, reduced motion, narrow widths, and 200 percent zoom, while measuring contrast, target size, focus visibility, and card geometry.

**Acceptance Scenarios**:

1. **Given** a desktop card in its default state, **When** it is not hovered or focused, **Then** hidden actions are neither visible nor focusable and the description remains readable.
2. **Given** a desktop card, **When** a pointer hovers it or keyboard focus enters it, **Then** both actions become visible and operable without changing the card's size or position in the grid.
3. **Given** revealed actions, **When** the visitor hovers, activates, or keyboard-focuses either action, **Then** its label remains white, its focus indicator is unmistakable, and the rendered combination meets WCAG 2.1 AA.
4. **Given** a focused card action, **When** the visitor presses Escape, **Then** actions are dismissed, focus returns to the card, and no hidden action remains focusable.
5. **Given** reduced-motion preferences or 200 percent zoom, **When** card actions are used, **Then** all information and controls remain available without clipped content or motion-dependent meaning.

---

### User Story 3 - Read one concise third-party notice (Priority: P2)

A visitor sees one short shared notice explaining the meaning of asterisks on third-party portfolio entries, regardless of how many third-party brands are present.

**Why this priority**: The current list grows with brand-specific legal language and obscures the simple disclosure needed on the portfolio summary.

**Independent Test**: Render the portfolio with zero, one, and multiple third-party entries and verify notice count, exact copy, marker association, and preservation of detailed wording outside the homepage.

**Acceptance Scenarios**:

1. **Given** one or more third-party portfolio entries, **When** the homepage renders, **Then** exactly one notice reads “* Third-party projects are independently owned and operated.”
2. **Given** another third-party entry is added, **When** the homepage renders again, **Then** the notice remains one paragraph with exactly the same wording.
3. **Given** an asterisked brand name, **When** assistive technology encounters its marker, **Then** the marker has an accessible text equivalent and is programmatically associated with the shared notice.
4. **Given** no third-party portfolio entries, **When** the homepage renders, **Then** the shared notice is omitted.
5. **Given** an applicable brand's guideline route or metadata, **When** its detailed vendor boundary is inspected, **Then** the existing brand-specific wording remains unchanged.

### Edge Cases

- A long description must preserve visible space below its final line without clipping or touching the card border.
- Revealed actions must fit inside the fixed card geometry at representative narrow desktop widths and 200 percent zoom.
- White action labels must remain readable in default, hover, active, focus-visible, dismissed, and reduced-motion states.
- A governed light-first brand may retain that presentation in its own guidelines while using the shared dark treatment only in the homepage portfolio.
- The portfolio may contain zero, one, or several third-party brands without producing an empty notice, duplicated notice, or changing the generic copy.
- A third-party marker must not rely solely on its visible asterisk to communicate meaning.
- No full-card link or hidden action may create duplicate or unreachable keyboard navigation.
- Existing logo files, geometry, colors, proportions, and transparency must remain unchanged.

## Requirements

### Functional Requirements

- **FR-001**: Every visible portfolio-card title, description, and action label MUST render white in every applicable interaction state.
- **FR-002**: Every homepage portfolio entry, including I Heart PR Tours, MUST use the shared dark card and accordion presentation in both site themes rather than a brand-specific or theme-inherited light surface.
- **FR-003**: The homepage-only dark treatment MUST preserve each brand's approved logo artwork and accent and MUST NOT change the brand's own guideline presentation or source identity.
- **FR-004**: Every card MUST retain at least 16 CSS pixels of visible bottom clearance beneath its description or revealed actions, with no clipping or border collision.
- **FR-005**: The desktop action reveal MUST preserve card and grid geometry without layout shift.
- **FR-006**: Hidden desktop actions MUST NOT be keyboard-focusable, and visible actions MUST be keyboard-operable.
- **FR-007**: Pointer hover, keyboard focus, active, Escape dismissal, pointer exit, and reduced-motion behavior MUST remain operable for every desktop card.
- **FR-008**: Mobile accordions MUST remain native, keyboard-operable disclosures with readable descriptions and actions.
- **FR-009**: Guidelines and Download Kit actions MUST meet WCAG 2.1 AA text contrast in every applicable state, and their focus indicator MUST maintain at least 3:1 contrast against adjacent colors.
- **FR-010**: Portfolio action targets MUST remain at least 44 by 44 CSS pixels at representative desktop and mobile widths.
- **FR-011**: When one or more portfolio entries are third-party, the homepage MUST render exactly one shared notice with the exact text “* Third-party projects are independently owned and operated.”
- **FR-012**: Adding further third-party entries MUST NOT add notice paragraphs or lengthen the generic homepage notice.
- **FR-013**: Third-party asterisks MUST appear only on applicable brand names, include an accessible text equivalent, and remain programmatically associated with the shared notice.
- **FR-014**: The shared notice MUST be omitted when no portfolio entry is third-party.
- **FR-015**: Detailed per-brand vendor-boundary wording MUST remain intact on applicable guideline pages, structured data, and metadata.
- **FR-016**: Automated coverage MUST reject mixed card text colors, governed light-card leakage, insufficient bottom spacing, inaccessible or focusable-hidden actions, layout shift, repeated disclaimer paragraphs, incorrect generic copy, and broken marker associations.
- **FR-017**: The portfolio MUST remain coherent at desktop and mobile widths, representative narrow widths, 200 percent zoom, keyboard-only operation, and reduced-motion preferences.
- **FR-018**: Existing site, publication, identity, accessibility, and release verification gates MUST continue to pass.

### Key Entities

- **Portfolio entry**: A public brand record shown on the homepage with title, descriptor, icon, accent, ownership metadata, and two actions.
- **Portfolio presentation**: The shared dark desktop-card and mobile-accordion treatment applied independently of a brand's own guide surface.
- **Action reveal state**: The default, revealed, focused, active, and dismissed presentation of the two card actions.
- **Third-party marker**: An asterisk and accessible equivalent attached only to applicable portfolio names.
- **Shared third-party notice**: The single generic homepage explanation associated with every applicable marker.
- **Detailed vendor boundary**: Brand-specific affiliation and provenance language retained on brand routes and in metadata but excluded from the homepage summary.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100 percent of visible portfolio titles, descriptions, and action labels compute to white across tested states and viewports.
- **SC-002**: All eight production portfolio entries use the same shared dark showcase treatment in both homepage themes, with zero changes to approved logo source bytes or brand-specific guideline surfaces.
- **SC-003**: Every card preserves at least 16 CSS pixels below its visible content at desktop, narrow, mobile, and 200 percent zoom layouts.
- **SC-004**: 100 percent of portfolio actions meet 4.5:1 text contrast, 3:1 focus-indicator contrast, keyboard-operability, hidden-focus, and 44-by-44 target requirements.
- **SC-005**: Revealing or dismissing actions changes no measured card dimension or grid position by more than 0.5 CSS pixels.
- **SC-006**: The homepage renders exactly one generic notice for any positive number of third-party entries and zero notices for no third-party entries.
- **SC-007**: 100 percent of applicable markers have accessible equivalents and programmatic association with the shared notice; zero non-third-party entries receive a marker.
- **SC-008**: Detailed vendor-boundary wording has zero unintended changes on guideline routes, structured data, or metadata.
- **SC-009**: The complete documented site and repository verification pipeline passes with zero accessibility violations.

## Scope

### In Scope

- Homepage portfolio desktop cards and mobile accordions.
- Shared card typography, dark showcase surfaces, spacing, and action states.
- Homepage third-party markers and one generic shared notice.
- Automated source, browser, accessibility, responsive, and reduced-motion coverage for the changed behavior.

### Out of Scope

- First-class light-theme systems across brand-specific routes, tracked by #193.
- Integration-instruction icon previews, tracked by #202.
- Type-specimen image embedding, tracked by #204.
- Changes to authoritative logo geometry or asset bytes.
- Changes to detailed vendor-boundary copy on brand-specific routes or in metadata.
- Generated artifacts under `dist/`, static site exports, release archives, or release publication.

## Assumptions

- White means the rendered color `#FFFFFF` for all visible portfolio card copy and action labels.
- The existing eight-card portfolio remains the production baseline for regression coverage while tests also exercise zero and multiple third-party records.
- Existing two-action behavior and native mobile disclosure structures remain the intended interaction model.
- The generic notice copy provided in #200 is final and needs no additional legal qualification on the homepage.
- The static public portfolio has no authentication, private data, tenant boundary, or user-generated input; security verification therefore focuses on preserving safe, explicit destinations and preventing hidden interactive controls.

## Dependencies

- GitHub issues #199 and #200 define the source acceptance criteria and close together with this slice.
- The existing generated brand registry supplies portfolio content and ownership metadata.
- The existing homepage browser verifier and source-level site tests provide the primary regression harness.
