# Feature Specification: CTA Role Consistency

**Feature Branch**: `codex/032-cta-role-consistency`

**Created**: 2026-09-13

**Status**: Draft

**Input**: User description: "Resolve GitHub issues #201 and #203 together by using #C5342C for every I Heart PR Tours primary CTA specimen, documenting that CTA role throughout the PDF brand guide, distinguishing it from other semantic colors, and standardizing generated guide prose on American English."

## User Scenarios & Testing

### User Story 1 - Apply the approved CTA color (Priority: P1)

An implementer consulting the I Heart PR Tours portable guidelines sees the approved CTA red on every primary button example, the live-site red-outline treatment on every secondary button example, and can distinguish those action roles from identity blue, links, focus treatments, chart colors, and destructive states.

**Why this priority**: The current examples teach an incorrect primary-action treatment and can directly cause off-brand, inaccessible interfaces.

**Independent Test**: Review every primary and secondary CTA specimen in the portable guidelines and verify that each primary default fill and each secondary default outline is exactly `#C5342C`, that all interactive states remain readable and visibly focusable, and that unrelated semantic roles retain their intended colors.

**Acceptance Scenarios**:

1. **Given** the dark and light theme-reference examples, **When** a reader compares their primary controls, **Then** both controls use `#C5342C` as the default fill.
2. **Given** the Type and components section, **When** a reader examines the primary component specimen, **Then** it uses `#C5342C` as the default fill.
3. **Given** any primary CTA example in the portable guidelines, **When** its default, hover, active, and keyboard-focus states are reviewed, **Then** text and focus treatments remain distinguishable and meet WCAG 2.1 AA on the actual surface.
4. **Given** links, focus tokens, chart series, destructive states, and identity-blue examples, **When** the CTA correction is applied, **Then** those non-CTA roles are not globally recolored red.
5. **Given** the dark and light theme-reference examples and Type and components, **When** a reader examines each secondary control, **Then** it uses a transparent default fill with a `#C5342C` outline and a surface-appropriate AA text color, then uses the governed CTA fill and foreground on hover.

---

### User Story 2 - Understand CTA semantics in the PDF guide (Priority: P1)

A designer or implementer reading the I Heart PR Tours PDF guide can find the approved CTA red by value and role, understand how to use it accessibly, and avoid confusing it with identity blue or destructive red.

**Why this priority**: The PDF currently states that red carries action while omitting the actual action color, leaving readers without enough information to implement the intended system.

**Independent Test**: Read and visually inspect the complete PDF, confirming that `#C5342C` appears in the palette and semantic guidance, that accessible CTA states are demonstrated, and that adjacent color roles are explicitly distinguished.

**Acceptance Scenarios**:

1. **Given** the PDF palette, **When** a reader looks for primary-action guidance, **Then** a visible `#C5342C` swatch is labeled as the primary CTA button role.
2. **Given** the semantic-use guidance, **When** a reader compares action, identity, link, focus, chart, and destructive roles, **Then** the guide explains that CTA red fills primary actions, outlines secondary actions, and remains distinct from each non-action role.
3. **Given** CTA usage guidance, **When** a reader implements a primary action, **Then** the guide provides an accessible text foreground and governed default, hover, active, and focus-visible behavior.
4. **Given** the portable guidelines and PDF, **When** their CTA guidance is compared, **Then** both artifacts identify the same value and semantic role.

---

### User Story 3 - Read consistent American English (Priority: P2)

A reader encounters consistent American English throughout generated brand-guide prose instead of a visible mixture of American and British spellings.

**Why this priority**: Mixed dialects reduce polish and make the shared generator appear internally inconsistent, but they do not block correct CTA implementation.

**Independent Test**: Extract and review all reader-facing text from the regenerated I Heart PR Tours PDF and confirm that the identified British spellings are absent and their American equivalents are present where applicable.

**Acceptance Scenarios**:

1. **Given** the complete generated PDF, **When** its reader-facing prose is extracted, **Then** it uses `color`, `color vision`, `colorway`, `recolor`, `rasterize`, and `synthesize` where those concepts appear.
2. **Given** another brand guide produced from shared prose, **When** that prose contains the same concepts, **Then** it also uses the standardized American spellings.
3. **Given** a generated guide, **When** its text is checked for the known British variants, **Then** none of those variants appears as a standalone reader-facing word.

### Edge Cases

- CTA red appears on both light and dark specimen surfaces, so the foreground and focus treatment must be valid on each actual surface rather than assumed from one example.
- CTA red cannot be used as small secondary-button text on the dark surface because its measured contrast is only 3.48:1 there; the dark specimen must use the legal surface foreground while retaining the red outline.
- Destructive red remains a separate state color even though it is visually related to CTA red.
- Chart palettes must not gain CTA red merely because the guide now displays it in the broader brand palette.
- American-English checks must detect whole words and common inflections without producing false positives inside unrelated names, URLs, file paths, or source metadata.
- The palette and semantic-use layout must accommodate the added CTA role without clipping, overlap, unreadable text, or pagination regressions.
- Regeneration must preserve authoritative logo artwork, geometry, proportions, transparency, and unrelated brand colors.

## Requirements

### Functional Requirements

- **FR-001**: Every primary CTA specimen in the I Heart PR Tours portable guidelines MUST use exactly `#C5342C` as its default fill, including both theme-reference wells and Type and components.
- **FR-002**: Primary CTA text and default, hover, active, and focus-visible treatments MUST meet WCAG 2.1 AA on every surface where the CTA is demonstrated.
- **FR-003**: Keyboard focus on every CTA specimen MUST remain unmistakably visible without relying on color alone.
- **FR-004**: CTA red MUST be represented as a distinct governed semantic role rather than replacing or aliasing the general primary identity role.
- **FR-005**: Identity blue, links, focus tokens, chart-series colors, and destructive states MUST retain their existing semantic roles unless a measured accessibility correction is required.
- **FR-006**: The PDF palette MUST include a visible `#C5342C` swatch labeled with a semantic token name and the plain-language role `Primary CTA button`.
- **FR-007**: The PDF semantic-use guidance MUST state that `#C5342C` is the default primary CTA fill.
- **FR-008**: The PDF MUST explicitly distinguish CTA red from destructive `#E9505F`, identity blue, links, focus treatments, and chart-series colors.
- **FR-009**: Introductory PDF guidance that refers to a fixed red MUST name `#C5342C` and its primary CTA role.
- **FR-010**: The PDF MUST document and visually demonstrate an accessible text foreground plus governed hover, active, and focus-visible behavior for CTA red.
- **FR-011**: The portable guidelines and PDF MUST agree on the CTA token, value, purpose, and state guidance.
- **FR-012**: All shared reader-facing generated brand-guide prose MUST use American English consistently, including `color`, `color vision`, `colorway`, `recolor`, `rasterize`, and `synthesize` where applicable.
- **FR-013**: Automated regression coverage MUST reject missing or incorrect CTA values, destructive-role mislabeling, blue primary CTA fallback, inaccessible CTA pairings or focus treatments, and reintroduced known British spellings.
- **FR-014**: The complete generated PDF MUST contain no clipped, overlapping, unreadable, or corrupted reader-facing text after the palette and semantic-use additions.
- **FR-015**: All production brand kits and published-site outputs MUST continue to satisfy the repository's existing identity, accessibility, generator, publication, and release gates.
- **FR-016**: Every secondary CTA specimen in the portable guidelines MUST use a transparent default fill with a `#C5342C` border, an AA text color derived for its actual surface, and a governed filled-red hover state with accessible interaction cues.
- **FR-017**: The PDF CTA guidance MUST visibly identify the secondary action as the red-outline alternative to the filled primary action.

### Key Entities

- **CTA semantic role**: The governed primary-action role, including token name, default value `#C5342C`, accessible foreground, and interaction-state guidance.
- **Identity and state color roles**: Existing blue identity, link, focus, chart, and destructive roles that remain semantically separate from the CTA role.
- **Portable guidelines**: The standalone HTML reference that demonstrates theme and component behavior.
- **PDF brand guide**: The printable reference that defines the palette, semantic use, accessibility guidance, and brand prose.
- **Shared guide prose**: Reader-facing language reused across generated brand guides and standardized on American English.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100 percent of primary CTA specimens in the I Heart PR Tours portable guidelines use a computed default fill of exactly `#C5342C`.
- **SC-002**: 100 percent of measured CTA text, state, and focus combinations meet WCAG 2.1 AA on their demonstrated surfaces.
- **SC-003**: The PDF contains one clearly labeled CTA-red palette entry and one explicit semantic-use entry, both identifying `#C5342C` as the primary CTA button fill.
- **SC-004**: The portable guidelines and PDF have zero disagreements about the CTA token, value, purpose, foreground, or interaction-state guidance.
- **SC-005**: Text extraction from the complete PDF finds zero occurrences of the identified British spellings in reader-facing prose.
- **SC-006**: Visual inspection of every PDF page finds zero clipped, overlapping, unreadable, or corrupted text regions.
- **SC-007**: Every production kit reports zero verification problems and zero glyph-validation failures, and the complete publication pipeline passes.
- **SC-008**: 100 percent of secondary CTA specimens use a computed `#C5342C` default border, a transparent default fill, an AA surface-aware text color, and the governed red/white pair on hover.

## Scope

### In Scope

- I Heart PR Tours CTA semantics and accessible interaction guidance.
- CTA projection into the portable-guidelines theme and component specimens.
- CTA presentation in the PDF palette, semantic-use table, and related explanatory prose.
- American-English normalization in shared generated guide prose.
- Regression coverage for CTA semantics, accessibility, artifact agreement, PDF layout, and dialect consistency.

### Out of Scope

- Broad light-theme support tracked by #193.
- Recoloring identity-blue roles, links, focus tokens, chart palettes, or destructive states.
- Changing authoritative logo geometry or shipped artwork.
- Repairing integration-instruction asset previews tracked by #202.
- Repairing the type-specimen image dependency tracked by #204.
- Patching generated files under `dist/` or committing regenerated outputs.

## Assumptions

- `#C5342C` is the owner-approved default fill for the I Heart PR Tours primary CTA role.
- The existing governed brand source already exposes enough information to represent a distinct CTA role, or can be extended without changing unrelated identity roles.
- White is expected to be a viable CTA text foreground, subject to measured WCAG 2.1 AA verification on every documented state.
- Existing generator and publication checks remain authoritative and may be extended, but not weakened.
- The two GitHub issues close together because their shared semantic source and generated artifacts must ship atomically.

## Dependencies

- GitHub issues #201 and #203 define the source acceptance criteria and close with this slice.
- Existing I Heart PR Tours brand source, portable-guidelines generator, PDF generator, and publication pipeline provide the governed inputs and outputs.
- Existing color-contrast, PDF extraction/rendering, kit verification, glyph validation, and site verification capabilities provide the required evidence.
