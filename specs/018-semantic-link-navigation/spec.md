# Feature Specification: Semantic Link and Documentation Navigation

**Feature Branch**: `codex/018-semantic-link-navigation`

**Created**: 2026-09-07

**Status**: In Review

**Input**: Resolve GitHub issues #142 and #143 as one end-to-end site interaction slice.

## User Scenarios & Testing

### User Story 1 - Recognize every link by purpose (Priority: P1)

As a visitor, I can distinguish editorial links, standalone actions, navigation, cards, buttons, identity links, and utility links without conflicting decorations.

**Why this priority**: The current global hover rule creates duplicate underlines and leaks into unrelated components.

**Independent Test**: Inspect representative routes at 360 and 1280 pixels in dark and light themes and verify each anchor family has one explicit, accessible treatment.

**Acceptance Scenarios**:

1. **Given** a standalone text action, **When** it rests, receives focus, or is hovered, **Then** it uses accessible accent text and a directional cue without an underline.
2. **Given** an editorial inline link, **When** it rests or interacts, **Then** it retains a persistent non-color-only underline with stronger interaction feedback.
3. **Given** desktop navigation, **When** it receives focus or hover, **Then** it uses one green two-pixel accent line, with motion removed under reduced-motion preference.
4. **Given** a card, button-shaped anchor, logo, mobile utility, footer, sidebar, breadcrumb, or table-of-contents link, **When** it interacts, **Then** no global ordinary-link decoration leaks into it.

---

### User Story 2 - Move between documents with quiet hierarchy (Priority: P1)

As a documentation reader, I can identify previous and next destinations from restrained neutral cards with readable hierarchy and clear direction.

**Why this priority**: The current orange wash and selector bug give title and description the same loud treatment.

**Independent Test**: Verify first, middle, and last documentation pages in both themes and at both target widths, including keyboard focus, touch sizing, long wrapping, and 200 percent zoom.

**Acceptance Scenarios**:

1. **Given** a pagination destination, **When** it rests, hovers, focuses, or activates, **Then** its fill remains neutral and its persistent border supplies restrained green feedback without an underline or lift.
2. **Given** a pagination card, **When** its content is read, **Then** direction, destination, and description have distinct neutral hierarchy and the entire card remains one anchor.
3. **Given** a first, middle, or last document, **When** pagination is rendered, **Then** only valid neighbors appear and all labels wrap without clipping.

---

### User Story 3 - Preserve semantics and brand boundaries (Priority: P1)

As a keyboard, touch, or assistive-technology user, I retain native navigation and download behavior while dedicated brand guidelines remain isolated from ShruggieTech site styling.

**Why this priority**: Visual corrections cannot weaken semantics, accessibility, or generated-kit ownership boundaries.

**Independent Test**: Exercise keyboard focus, modifier-safe native anchors, downloads, reduced motion, and hosted guideline pages while confirming WCAG 2.1 AA and no inherited site taxonomy.

**Acceptance Scenarios**:

1. **Given** any anchor, **When** it is used by keyboard or touch, **Then** it remains at least 44 pixels high where it is a discrete control and retains visible focus.
2. **Given** an external link or download, **When** classified, **Then** destination attributes do not silently change its visual role or native behavior.
3. **Given** a hosted per-brand guideline, **When** it is displayed, **Then** it retains its generated brand treatment and receives no ShruggieTech link taxonomy.

### Edge Cases

- Multiline editorial links and wrapping standalone actions must not break decoration geometry.
- Links that wrap code, images, headings, or framework-generated markup must receive the intended role without nested interactive elements.
- Visited editorial links must remain recognizable and readable without leaking visited styling into navigation, cards, buttons, or identity links.
- Reduced motion must remove decorative animation while preserving a visible state change.
- Empty previous or next positions must not create dead or hidden anchors.

## Requirements

### Functional Requirements

- **FR-001**: The current site MUST inventory every rendered anchor family and assign one explicit semantic visual role.
- **FR-002**: The new authority MUST supersede the blanket orange-underline rule from S012 without rewriting completed historical evidence.
- **FR-003**: Generated consumer defaults MUST not apply native hover underlines globally.
- **FR-004**: Standalone text actions MUST use accessible accent text, a directional cue, and color-state feedback without an underline.
- **FR-005**: Editorial inline links MUST expose a persistent offset underline at rest and stronger hover and focus feedback.
- **FR-006**: Desktop header text navigation MUST use neutral text and a left-origin two-pixel green accent line on hover and focus.
- **FR-007**: Mobile navigation, footer, sidebar, table of contents, breadcrumbs, current-page links, search results, skip links, headings, identity links, cards, and button-shaped anchors MUST retain explicit component treatments without taxonomy leakage.
- **FR-008**: Link state requirements MUST cover rest, hover, focus-visible, active, current, visited where applicable, and reduced motion.
- **FR-009**: Native anchor, modifier-click, external destination, and download semantics MUST remain intact, with no nested interactive controls.
- **FR-010**: Documentation pagination MUST use neutral theme surfaces in every state and MUST remove CTA-colored wash, inset line, lift, and underline.
- **FR-011**: Pagination cards MUST distinguish direction, destination, and description through stable hooks and neutral size, weight, and color hierarchy.
- **FR-012**: Pagination cards MUST retain a persistent border, restrained green hover and focus border feedback, one-anchor structure, minimum 44-pixel height, and wrapping without clipping.
- **FR-013**: First, middle, and last documentation pages MUST expose only valid previous and next destinations.
- **FR-014**: Verification MUST measure text decoration, decorative backgrounds or pseudo-elements, descendant text, focus, state colors, dimensions, wrapping, URLs, and overflow at 360 and 1280 pixels in both themes.
- **FR-015**: All affected public routes MUST pass WCAG 2.1 AA, keyboard, touch, reduced-motion, and 200 percent zoom checks.
- **FR-016**: Dedicated per-brand guideline pages MUST remain outside the ShruggieTech site link taxonomy.
- **FR-017**: Identity geometry, canonical palettes, generated kits, and public content values MUST remain unchanged.

### Key Entities

- **Anchor Family**: A group of links with the same user purpose, component context, semantics, and allowed visual states.
- **Link State Contract**: The resting and interaction properties permitted for one anchor family.
- **Pagination Destination**: One valid previous or next document with direction, title, description, URL, and availability.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every rendered anchor on representative public routes maps to exactly one documented family, with zero duplicate underline mechanisms.
- **SC-002**: All first, middle, and last document pagination cases expose the correct neighbor count and valid URLs.
- **SC-003**: All discrete link controls meet a 44-pixel minimum target and all text remains unclipped at 360 pixels and 200 percent zoom.
- **SC-004**: Browser verification reports zero WCAG 2.1 AA violations across both themes and target widths.
- **SC-005**: All five production kits report zero verification problems and zero glyph failures.

## Assumptions

- The pinned official-company source evidence recorded in #142 remains the visual authority for role-specific treatments.
- Green is the navigation and restrained-border interaction accent; orange remains available only for roles that explicitly own it and never as a universal link decoration.
- Existing Fumadocs neighbor selection remains authoritative; this slice changes presentation and verifies its output rather than replacing routing.
- No identity, palette, font, content, information architecture, or release change is in scope.
