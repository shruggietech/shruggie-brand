# Feature Specification: Compact egui Desktop Density

**Feature Branch**: `codex/044-compact-egui-density`

**Created**: 2026-09-21

**Status**: In Progress

**Input**: User description: "Urgently correct the ESO Weave style regression that made buttons, toggles, radio-style controls, selectors, and Live Log rows excessively tall or inconsistently padded, while preserving the resource meters that already look appropriate. File the necessary GitHub issue, complete a minimal Spec Kit iteration, push a pull request, process one Codex review round, and report when CI is green."

**Issue**: [#239](https://github.com/shruggietech/shruggie-brand/issues/239)

## Clarifications

### Session 2026-09-21

- Q: Should the 44-unit interaction target continue to govern touch and coarse-pointer input? -> A: Yes; compact visible controls apply only to fine-pointer desktop input.
- Q: Should the health, Magicka, Stamina, and Ultimate meters change in this correction? -> A: No; preserve their current presentation.
- Q: Should this slice modify the downstream ESO Weave application repository? -> A: No; correct the generated egui adapter contract and provide migration guidance for consumers.

## User Scenarios & Testing

### User Story 1 - Use compact desktop controls (Priority: P1)

As an ESO Weave desktop user with a mouse or precise pointer, I can scan and operate controls without oversized buttons and switches overwhelming the application content.

**Why this priority**: The current generated style makes the main application visibly worse and reduces information density across every interactive section.

**Independent Test**: Generate the native adapter, apply its fine-pointer compact style at normal text scale, and measure buttons, selectors, switches, checkboxes, and radio-style controls against the declared body-line and spacing limits.

**Acceptance Scenarios**:

1. **Given** a fine-pointer desktop runtime at normal text scale, **When** the compact generated style is applied, **Then** ordinary interactive controls remain close to one body-text line plus restrained padding and no control is forced to the touch target height.
2. **Given** adjacent control types in one interface row, **When** the generated defaults are applied, **Then** their vertical padding and minimum height follow one coherent density rule.
3. **Given** the existing resource meters, **When** the correction is adopted, **Then** their size and presentation remain outside the change.

---

### User Story 2 - Read dense live logs (Priority: P1)

As an operator reading the Live Log, I can scan consecutive entries as a dense event stream without double-spaced vertical gaps.

**Why this priority**: The log is an operational diagnostic surface where unnecessary row gaps reduce context and force avoidable scrolling.

**Independent Test**: Render consecutive one-line labels under the generated fine-pointer compact defaults and measure the gap between their line boxes.

**Acceptance Scenarios**:

1. **Given** consecutive one-line log entries, **When** they use the generated compact style, **Then** the vertical gap is no more than 2 logical units at normal text scale.
2. **Given** a long sequence of log entries, **When** the operator scans the list, **Then** no global style forces each row to a button-sized height.

---

### User Story 3 - Retain touch accessibility (Priority: P2)

As a user on a touch or coarse-pointer runtime, I retain the governed minimum interaction target even though precise-pointer desktop controls become visually compact.

**Why this priority**: The density correction must not trade away the established non-mouse interaction contract.

**Independent Test**: Apply the generated style with coarse-pointer or touch capabilities and measure the resulting interaction target against the governed minimum.

**Acceptance Scenarios**:

1. **Given** touch is available or pointer precision is coarse or mixed, **When** runtime capabilities are applied, **Then** the minimum interaction target remains 44 logical units.
2. **Given** fine-pointer input without touch, **When** runtime capabilities are applied, **Then** the compact visual control height is used instead of the touch target height.

### Edge Cases

- Text scaling increases control height as needed so labels are not clipped, while ordinary normal-scale controls remain compact.
- A runtime reporting both fine pointer and touch uses the touch-safe target.
- A runtime with absent or ambiguous pointer precision uses the conservative touch-safe target.
- Density changes spacing and fine-pointer control height without reducing coarse or touch targets.
- Invalid non-finite or non-positive unit transforms continue to fail closed.

## Requirements

### Functional Requirements

- **FR-001**: The generated native style MUST distinguish fine-pointer visual control height from the governed coarse-pointer and touch interaction target.
- **FR-002**: Fine-pointer controls at normal text scale MUST use a visible height no greater than 28 logical units in comfortable density and no greater than 24 logical units in compact density.
- **FR-003**: Coarse-pointer, mixed-pointer, touch-capable, and pointer-unknown runtimes MUST retain a minimum interaction target of 44 logical units.
- **FR-004**: Buttons, selectors, switches, checkboxes, and radio-style controls MUST derive vertical sizing and padding from the same generated density model.
- **FR-005**: Fine-pointer compact row spacing MUST leave no more than 2 logical units between consecutive one-line log entries at normal text scale.
- **FR-006**: Text scaling MUST increase the minimum control height when the scaled body text and padding require more space.
- **FR-007**: The correction MUST preserve invalid-transform rejection, theme behavior, keyboard focus behavior, accessible naming, and deterministic generation.
- **FR-008**: Generated native evidence MUST cover fine-pointer comfortable and compact sizing, touch/coarse target retention, mixed-input fallback, text scaling, and dense row spacing.
- **FR-009**: Production kit verification MUST continue to report zero problems and glyph validation MUST continue to report zero failures.
- **FR-010**: The correction MUST NOT modify brand identity sources, logo geometry, resource-meter presentation, the Web/React adapter, or downstream application source.
- **FR-011**: Migration guidance MUST identify the prior visible-target conflation and tell native consumers to regenerate and adopt the corrected adapter.

### Key Entities

- **Native density profile**: The selected comfortable or compact spacing and visible-control scale for a generated native interface.
- **Runtime input profile**: Observed pointer precision and touch capability used to select a compact fine-pointer control or conservative interaction target.
- **Control metrics**: Generated minimum target, fine-pointer visual height, padding, and row spacing values used by the native style.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Fine-pointer comfortable controls measure at most 28 logical units high and compact controls measure at most 24 logical units high at normal text scale.
- **SC-002**: Touch, coarse, mixed, and unknown pointer profiles measure at least 44 logical units in both densities.
- **SC-003**: Consecutive one-line log-style rows have no more than 2 logical units of generated vertical gap at normal text scale.
- **SC-004**: One generated native test suite covers 100 percent of the required density, input-profile, text-scale, spacing, and invalid-input categories.
- **SC-005**: All production kits complete with zero verifier problems and zero glyph failures, with no approved identity-source byte changes.

## Assumptions

- ESO Weave is a desktop-first consumer whose ordinary mouse and trackpad interactions qualify as fine-pointer input.
- The existing 44-unit target remains the conservative contract for touch, coarse, mixed, and unknown pointer profiles.
- The generated adapter owns default control density, while product-specific resource meters remain consumer-owned domain components.
- A downstream consumer update is required to adopt newly generated adapter bytes, but that repository is outside this slice.
