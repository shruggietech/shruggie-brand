# Feature Specification: Phase 13 Brand Site Polish

**Feature Branch**: `codex/012-brand-site-polish`

**Created**: 2026-09-05

**Status**: Ready for Review

**Input**: User description: "Complete Phase 13 as one tightly packed Spec Kit slice covering issues #120 through #126, then publish a reviewed pull request under the two-round Codex limit."

## User Scenarios & Testing

### User Story 1 - Recognize the official ShruggieTech identity (Priority: P1)

A visitor sees the approved ShruggieTech favicon and colored horizontal lockup throughout the landing and documentation experiences, with consistent presentation in both themes and at desktop and mobile widths.

**Why this priority**: Incorrect white-background icons and monochrome lockups visibly contradict the finalized company identity on every entry point.

**Independent Test**: Inspect the root icon suite and the landing header, documentation header/sidebar, documentation footer card, and shared footer in both themes and viewport classes. Every surface uses the approved black-background favicon treatment and colored lockup while preserving canonical geometry.

**Acceptance Scenarios**:

1. **Given** any public landing or documentation route, **When** browser icon metadata and files are inspected, **Then** they resolve to the same approved opaque-black ShruggieTech icon suite.
2. **Given** a dark or light themed page at desktop or mobile width, **When** the header, documentation navigation, and footer branding are viewed, **Then** the green ShruggieTech identity mark remains visible within the approved horizontal lockup treatment.
3. **Given** an incorrect white, transparent, empty, off-token, or monochrome identity asset, **When** validation runs, **Then** publication fails before deployment.

---

### User Story 2 - Navigate with clear canonical language (Priority: P1)

A visitor reaches documentation through compact viewport-appropriate navigation and sees one canonical name for the documentation area and the Variance Contract everywhere those destinations appear.

**Why this priority**: Crowded navigation and inconsistent labels weaken orientation, while generated metadata can silently restore rejected terminology unless the source contract is corrected.

**Independent Test**: Inspect landing navigation at desktop and mobile widths plus every public navigation, heading, search, social, and structured-metadata surface for the documentation root and Variance Contract. The exact inventories and canonical labels are present, banned variants are absent, and route paths are unchanged.

**Acceptance Scenarios**:

1. **Given** a desktop landing header, **When** navigation is inspected, **Then** `Documentation` is the only text navigation link and targets `/docs/`.
2. **Given** a mobile landing header, **When** its menu is opened, **Then** it contains exactly `Documentation`, `Download the Skill`, and `View on GitHub`, with no `Portfolio` item.
3. **Given** any public navigation or metadata surface, **When** the documentation root is named, **Then** its exact label is `Documentation` and no rejected legacy phrase appears.
4. **Given** any public display or metadata surface for the first numbered document, **When** its title is read, **Then** its exact display name is `Variance Contract` while `/docs/00-variance-contract/` remains unchanged.

---

### User Story 3 - Understand actions and links before interaction (Priority: P1)

A visitor can distinguish primary actions, secondary actions, ordinary links, code semantics, and documentation navigation cards before hover, with equally clear keyboard and reduced-motion behavior.

**Why this priority**: The current green primary actions, neutral documentation content, and hover-dependent link card do not express the approved hierarchy or provide a sufficiently clear interaction affordance.

**Independent Test**: Inspect representative landing and documentation pages in both themes, at desktop and mobile widths, in normal and reduced-motion modes. Primary, secondary, inline-link, code, list-marker, and pagination-card roles remain distinct and pass accessibility checks.

**Acceptance Scenarios**:

1. **Given** a primary call to action, **When** viewed in either theme, **Then** it uses the approved CTA-safe orange treatment with compliant foreground contrast.
2. **Given** a secondary action, identity accent, list marker, or code string token, **When** viewed in either theme, **Then** it uses the approved green role appropriate to its surface without making color the sole signal.
3. **Given** an ordinary eligible text link, **When** hovered or keyboard-focused, **Then** an orange underline progresses from left to right within the approved motion duration, while reduced-motion mode retains a clear static state.
4. **Given** a documentation previous or next card at rest, **When** viewed without hover on desktop or touch width, **Then** its action and destination are unmistakable and keyboard focus remains obvious.

### Edge Cases

- A favicon file that decodes correctly but uses white, transparency, or a near-black outside the canonical void token must fail validation.
- An identity asset that exists but is monochrome or does not come from the canonical generated ShruggieTech sources must fail validation.
- A narrow viewport must not expose desktop-only links, clip controls, reduce touch targets below 44px, or duplicate the documentation root inside the documentation application.
- Legacy wording that differs only by capitalization must still fail the source and emitted-site terminology contract.
- External download and repository links must retain their exact approved destinations and must not appear in desktop landing navigation.
- Disabled controls, buttons, cards, logo links, and heading anchors must not inherit the ordinary inline-link underline treatment.
- Reduced-motion mode must remove decorative transition movement without removing visible hover or focus affordances.
- Missing previous or next documentation destinations must not leave a misleading disabled link card.
- Asset load failure must retain meaningful alternative text while failing the build or verification contract rather than silently shipping broken identity chrome.

## Requirements

### Functional Requirements

- **FR-001**: Every public browser icon variant MUST present the canonical ShruggieTech reduced mark on the canonical opaque black void surface.
- **FR-002**: Browser icon coverage MUST include SVG, 16px and 32px PNG, all ICO frames, Apple touch, and manifest-declared application icons wherever the same company-favicon treatment applies.
- **FR-003**: Automated verification MUST reject white, transparent, empty, off-token, malformed, or dimensionally incorrect icon outputs.
- **FR-004**: All affected identity assets MUST remain traceable to canonical ShruggieTech source assets, and shipped mark and wordmark geometry MUST remain byte-for-byte unchanged.
- **FR-005**: The landing header, documentation header/sidebar, documentation footer card, and shared footer MUST use the approved colored horizontal ShruggieTech lockup treatment in both supported themes.
- **FR-006**: Identity verification MUST distinguish the approved colored lockup from monochrome alternatives and MUST retain correct aspect ratio, clear space, alternative text, and responsive sizing.
- **FR-007**: Desktop landing navigation MUST contain exactly one text navigation link, `Documentation`, targeting `/docs/`.
- **FR-008**: Mobile landing navigation MUST contain exactly `Documentation`, `Download the Skill`, and `View on GitHub`, with correct destinations and 44px minimum targets.
- **FR-009**: `Portfolio` MUST be absent from the landing header and mobile menu while portfolio content remains available in the page body.
- **FR-010**: Documentation navigation, search, theme, keyboard, focus, escape, and close behaviors MUST remain functional and MUST NOT gain a duplicate documentation-root entry.
- **FR-011**: `Documentation` MUST be the sole public-facing name of `/docs/` across navigation, headings, titles, breadcrumbs, structured data, social metadata, and generated route records.
- **FR-012**: Public source and emitted output MUST reject `How we build brands` and `How we build` case-insensitively when used as documentation labels.
- **FR-013**: `Variance Contract` MUST be the sole public display title for the first numbered document across source, page, navigation, search, cards, pagination, breadcrumbs, structured data, social metadata, and generated route records.
- **FR-014**: Public source and emitted output MUST reject `The ShruggieTech Variance Contract`, `ShruggieTech Variance Contract`, and `The Variance Contract` as display titles.
- **FR-015**: The `/docs/` and `/docs/00-variance-contract/` paths, source numbering, filenames, stable identifiers, canonical URLs, and inbound-link compatibility MUST remain unchanged.
- **FR-016**: Primary calls to action MUST use the canonical CTA-safe orange role with a compliant foreground in both themes, while secondary actions and identity accents MUST use the approved green role for their surface.
- **FR-017**: Documentation list markers and code string tokens MUST use deliberate approved green treatments while multi-token syntax meaning and text readability remain intact.
- **FR-018**: Eligible ordinary text and navigation links MUST provide a canonical orange underline that progresses left to right over 120ms to 300ms on hover and keyboard focus.
- **FR-019**: Buttons, cards, logos, heading anchors, disabled links, and components where an underline would misrepresent the interaction MUST be excluded from the ordinary animated-link treatment.
- **FR-020**: Reduced-motion mode MUST disable decorative underline movement while preserving a visible static hover and focus treatment.
- **FR-021**: Documentation previous and next cards MUST have an unmistakable resting-state link affordance, a visible action or destination treatment, distinct hover, focus, and active states, and a minimum 44px target in both themes and viewport classes.
- **FR-022**: Inline paragraph links within documentation MUST remain governed by the ordinary inline-link contract rather than the pagination-card contract.
- **FR-023**: All text, controls, focus indicators, and interaction states MUST meet WCAG 2.1 AA in both themes at desktop and mobile widths.
- **FR-024**: Validation MUST cover canonical source, generated content, static output, browser semantics, responsive inventories, visual states, reduced motion, and accessibility before the slice is considered complete.
- **FR-025**: Generated kits, raster exports, PDFs, registries, static exports, and release archives MUST remain absent from the committed change set.
- **FR-026**: The work MUST close issues #120 through #126 only through the owner-approved merge of the official pull request.
- **FR-027**: Every negative review finding MUST be filed as a GitHub issue before correction or disposition, every review comment MUST receive a substantive response, and every addressed thread MUST be resolved.
- **FR-028**: Review activity MUST stop after the automatic first round and at most one explicit second-round request, and the pull request MUST remain open for the owner merge ritual.

### Scope Boundaries

- This slice changes the public brand site's identity asset selection, navigation inventory, terminology, color hierarchy, link behavior, documentation card affordance, generation rules, and verification coverage.
- This slice does not alter canonical logo path geometry, rename public routes or source numbering, redesign the documentation information architecture, add new brand records, publish a new release, or merge its own pull request.

### Key Entities

- **Identity Asset Contract**: The canonical source, output role, theme treatment, dimensions, background token, color treatment, geometry provenance, and verification rules for each favicon or lockup.
- **Responsive Navigation Contract**: The viewport class, visible items, labels, destinations, interaction behavior, and exclusions for landing and documentation navigation.
- **Canonical Terminology Contract**: The accepted display name, rejected variants, stable route, and public surfaces for the documentation root and Variance Contract.
- **Interaction Role Contract**: The semantic role, canonical color, foreground, resting state, hover state, focus state, active state, reduced-motion behavior, and component exclusions for actions and links.
- **Visual Evidence Matrix**: Representative route, viewport, theme, motion preference, and inspected surfaces used to prove the public experience.
- **Review Round**: One of at most two Codex review passes, including its trigger, findings, issue links, responses, corrections, resolved threads, and CI result.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All seven Phase 13 child issues satisfy every acceptance criterion with traceable automated and visual evidence.
- **SC-002**: One hundred percent of public favicon entry points use the approved opaque-black treatment, and every tested white, transparent, empty, or off-token mutation is rejected.
- **SC-003**: One hundred percent of affected header, navigation, and footer identity surfaces use the approved colored lockup treatment in both themes and at both viewport classes.
- **SC-004**: Desktop landing navigation exposes exactly one requested text link, mobile landing navigation exposes exactly three requested text links, and both inventories contain zero `Portfolio` entries.
- **SC-005**: Public source and emitted-site scans contain zero rejected documentation labels and zero rejected Variance Contract title variants.
- **SC-006**: The landing, documentation index, and Variance Contract routes retain their existing canonical paths and pass representative browser checks at 360px and 1280px in both themes.
- **SC-007**: The complete visual evidence matrix contains at least 12 inspected screenshots spanning three representative routes, two viewport widths, and two themes, with no clipping, overlap, broken branding, unclear resting link state, or material regression.
- **SC-008**: Automated accessibility inspection reports zero WCAG 2.1 AA violations across the complete documented route matrix.
- **SC-009**: All generated site and production-kit verification gates report zero failures, and the committed diff contains zero generated publication artifacts.
- **SC-010**: The official pull request reaches green required checks with zero unresolved review threads after no more than two Codex review rounds and remains open for owner approval.

## Assumptions

- The canonical ShruggieTech void token is the approved opaque black application-icon surface described by issue #120.
- Existing canonical colored lockup assets are authoritative; this slice selects and verifies them without altering their geometry or inventing new artwork.
- The existing site breakpoints define desktop and mobile behavior; the contract is based on rendered visibility rather than duplicating breakpoint values in public requirements.
- The current external skill-download and GitHub destinations remain authoritative.
- The site is public and static, handles no private user data, and introduces no authentication or tenancy boundary.
- The existing complete site verifier remains the primary route, payload, metadata, responsive, theme, and accessibility gate and may be strengthened but not weakened.
