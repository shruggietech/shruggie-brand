# Feature Specification: Glitchpad Identity Color Approval

**Feature Branch**: `codex/015-glitchpad-color-system`

**Created**: 2026-09-07

**Status**: Approved implementation

**Input**: User description: "Kick off S015 and halt when the proposed Glitchpad coloring is ready for owner input and approval."

**Owner clarification, 2026-09-07**: The glyph is always a square-based enclosure containing the protected rectangular page construction. Optional plating is rejected. All Revision 1 candidates are rejected, `#867100` is permanently prohibited, and the comparison must be regenerated before approval.

**Owner adjustment, 2026-09-07**: Revision 3 combines Revision 2 Direction A in dark mode with Direction B in light mode. The focused proposal uses a sulfur square with charcoal page on dark surfaces and a charcoal square with sulfur page on light surfaces; both retain the slate fold and neutral wordmark.

**Owner approval, 2026-09-07**: Revision 3 is approved for production exactly as proposed. The permanent square, contextual dark/light inversion, slate fold, neutral wordmark, and prohibition on muddy or darkened yellow variants are authoritative for S015.

## User Scenarios & Testing

### User Story 1 - Compare credible identity directions (Priority: P1)

As the brand owner, I can compare three materially different Glitchpad color directions on identical protected geometry across realistic dark, light, small-size, lockup, desktop, and Android contexts.

**Why this priority**: Glitchpad's first desktop and Android release is blocked on an identity-defining choice. A visually honest, controlled comparison is required before source values change.

**Independent Test**: Review one labeled comparison set in which every direction uses identical source geometry, scale, and context positions, with exact color values and measured contrast supplied separately from aesthetic claims.

**Acceptance Scenarios**:

1. **Given** the current Glitchpad paper-and-G paths, **When** the three directions are compared, **Then** every sample places those byte-identical rectangular page paths safely inside the same permanent square enclosure and differs only in declared color roles.
2. **Given** dark and near-white contexts, **When** each direction is viewed as a mark, horizontal lockup, stacked lockup, reduced icon, and app tile, **Then** the owner can judge paper visibility, wordmark distinction, fold separation, small-size recognition, and overall character.
3. **Given** numerical contrast evidence, **When** a direction is assessed, **Then** measurements are identified as objective evidence and are not presented as a substitute for owner identity approval.

---

### User Story 2 - Approve one explicit color-role system (Priority: P1)

As the brand owner, I can select a direction, request a bounded adjustment, or reject all proposals before any exploratory palette becomes the shipped identity.

**Why this priority**: Changing the identity color allocation is materially irreversible and constitutionally requires an explicit owner decision with written rationale and comparison evidence.

**Independent Test**: Record one unambiguous owner disposition naming the approved direction or exact adjustment, including dark, light, square, square-edge, page, fold, reduced, monochrome, wordmark, and platform treatment.

**Acceptance Scenarios**:

1. **Given** the comparison evidence, **When** the owner approves a direction, **Then** the decision record contains exact role assignments and a concise rationale.
2. **Given** the comparison evidence, **When** the owner requests an adjustment, **Then** no shipped source changes until the adjusted proposal is compared and approved.
3. **Given** no direction is acceptable, **When** the owner rejects the set, **Then** the current identity remains authoritative and S015 records the next bounded exploration rather than silently choosing a fallback.

---

### User Story 3 - Ship the approved identity consistently (Priority: P2)

As a desktop, Android, web, or brand-guideline consumer, I receive the same approved Glitchpad color system in every applicable generated asset without geometry changes or contradictory guidance.

**Why this priority**: Approval has value only when the source contract, generator, documentation, and delivery surfaces agree.

**Independent Test**: After approval, rebuild all production kits and inspect Glitchpad mark-only, horizontal, stacked, full, reduced, monochrome, web, desktop, Android, Apple, Windows, guideline, specimen, and site outputs against the approved role matrix.

**Acceptance Scenarios**:

1. **Given** an approved color matrix, **When** production assets are generated, **Then** every applicable asset uses the approved role values and every non-applicable asset retains its governed platform behavior.
2. **Given** a wordmark role that differs by context, **When** lockups and standalone wordmarks are generated, **Then** their colors derive from brand source rather than a generator-owned Glitchpad literal.
3. **Given** the approved identity change, **When** guidance and tests are reviewed, **Then** no obsolete prohibition, assumption, rationale, or expected color remains.

### Edge Cases

- A candidate that passes background contrast but loses the fold against the paper must be shown as failing that local distinction rather than promoted.
- A bright yellow square on near-white must use a sufficiently distinct square edge rather than a muddy replacement yellow.
- Reduced icons may intentionally collapse to one color, but the mapping must be explicit and must not inherit a full-mark fold role accidentally.
- The square enclosure must appear in every glyph use and must never be added as a second app-only plate.
- The square must retain safe inset on every side and must not clip at any reference or actual-size sample.
- Monochrome black and white variants remain single-color delivery roles and must not be contaminated by full-color mappings.
- A requested owner adjustment that changes hue family, geometry, texture, or effects expands the decision surface and requires fresh comparison evidence.

## Requirements

### Functional Requirements

- **FR-001**: S015 MUST address GitHub issue #146 as a standalone identity-decision slice.
- **FR-002**: The revised pre-approval comparison MUST include Sulfur Square, Charcoal Square, and Slate Square directions that vary where saturated sulfur appears within one permanent square construction.
- **FR-003**: Every candidate MUST use byte-identical canonical Glitchpad page path data inside an identical safe square enclosure, with identical page scale, placement, and layout within each comparison context.
- **FR-004**: Comparison evidence MUST include charcoal and near-white surfaces, mark-only and reduced marks, horizontal and stacked lockups, 16, 24, 32, and 48 pixel contexts, and representative desktop, Android launcher, and store-artwork contexts.
- **FR-005**: Each candidate MUST declare exact dark, light, square, square-edge, page, fold, reduced, monochrome, wordmark, and platform roles, including where a role is intentionally unchanged or not applicable.
- **FR-006**: Each proposed fill MUST include measured contrast against its intended background and, where visually adjacent, against the neighboring fill.
- **FR-007**: Objective measurements MUST be separated from subjective judgments about distinction, punch, calmness, and brand character.
- **FR-008**: The comparison MUST identify any candidate-context pairing that does not meet the required accessibility or non-text distinction floor.
- **FR-009**: No candidate value, prohibition change, generator behavior, generated kit, or public site treatment MAY become authoritative before explicit owner approval.
- **FR-010**: The workflow MUST halt after presenting the proposed coloring and MUST accept approval, bounded adjustment, or rejection as valid owner dispositions.
- **FR-011**: The approved decision MUST preserve the imported paper-and-G shape, G channel, fold geometry, and path strings byte-for-byte. The enclosing square MUST not stretch, clip, or rederive those protected paths.
- **FR-012**: Post-approval implementation MUST express identity roles in `brands/glitchpad/brand.json` and shared generator contracts, never by patching generated SVG, PNG, PDF, registry, or site output.
- **FR-013**: If wordmark color becomes configurable, the capability MUST be a validated optional shared contract whose absent state preserves every existing brand.
- **FR-014**: Post-approval implementation MUST update every contradictory Glitchpad prohibition, assumption, guide statement, measured record, test expectation, and changelog decision.
- **FR-015**: All full-color, light, reduced, black, white, desktop, Android, web, Apple, Windows, guideline, specimen, and site dispositions MUST be recorded as changed, verified unchanged, or inapplicable.
- **FR-016**: Every production kit MUST finish with zero `verify.py` problems and zero `validate_glyph.py` failures, and the site MUST finish with zero WCAG 2.1 AA violations.
- **FR-017**: Generated comparisons, kits, raster exports, PDFs, screenshots, and archives MUST remain outside Git.
- **FR-018**: S015 MUST record the owner approval and final identity rationale before publication or pull-request completion.

### Key Entities

- **Color direction**: A complete exploratory mapping of permanent square, square edge, paper, fold, reduced mark, wordmark, and monochrome roles across dark and light contexts.
- **Comparison context**: One controlled surface, size, layout, or platform presentation used identically across directions.
- **Contrast observation**: A measured relationship between a fill and its intended surface or neighboring fill, with threshold and disposition.
- **Owner disposition**: Approval, bounded adjustment, or rejection attached to a named direction and exact values.
- **Approved identity matrix**: The authoritative post-decision mapping that production source, generator behavior, tests, and guidance must implement.

## Success Criteria

### Measurable Outcomes

- **SC-001**: One comparison set presents all three required directions in 100 percent of the contexts listed in FR-004 with zero path-data differences.
- **SC-002**: Every proposed color role has an exact hexadecimal value and 100 percent of applicable surface and adjacent-fill relationships have recorded contrast measurements.
- **SC-003**: The owner can approve, adjust, or reject the proposal from one decision summary without needing hidden implementation context.
- **SC-004**: Before approval, zero exploratory identity values appear in committed brand source or generated public artifacts.
- **SC-005**: After approval, 100 percent of applicable Glitchpad output families match the approved identity matrix and every obsolete color instruction is removed.
- **SC-006**: Protected `logo.paths` hashes and source lockup proportions remain identical before and after S015; the new enclosing square introduces no path distortion or clipping.
- **SC-007**: The complete production gate reports five successful kit builds, zero verification problems, zero glyph failures, and zero site WCAG 2.1 AA violations.

## Scope

### In scope

- Issue #146, controlled comparison evidence, owner approval, approved role-source changes, proportional shared wordmark-role support if required, generator and documentation synchronization, generated-output verification, and release handoff evidence.

### Out of scope

- Any protected page path, G-channel, fold shape, typography, naming, texture, bevel, glow, animation, unrelated sibling palette, global site theme, guideline catalog, or link-navigation redesign.

## Assumptions

- The owner's clarification supersedes the earlier assumption that square containment was merely contextual. The square is permanent glyph geometry around the protected rectangular page.
- The owner wants a genuine identity choice rather than an automatic accessibility-only correction, so the explicit approval gate is mandatory.
- The approved contextual system uses Sulfur Square in dark mode and Charcoal Square in light mode, preserving a strong silhouette in both contexts without a muddy substitute.
- Current black and white monochrome variants remain valid unless the approved direction explicitly requires a different delivery disposition.
