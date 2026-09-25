# Feature Specification: Color Roles and Independent Palettes

**Feature Branch**: `codex/053-color-roles-independent-palettes`

**Created**: 2026-09-25

**Status**: Approved for implementation

**Input**: S053 implements [#267](https://github.com/shruggietech/shruggie-brand/issues/267) and [#268](https://github.com/shruggietech/shruggie-brand/issues/268). The owner approved independent palettes for every brand, including owned sub-brands. Existing approved palettes and logo path data remain unchanged.

## User Scenarios & Testing

### User Story 1 - Choose an owned brand's palette freely (Priority: P0)

As a brand author, I can create an owned child brand with its own identity and interface colors, even if one matches a sibling hue, without inheriting ShruggieTech orange merely because ShruggieTech owns it.

**Independent Test**: Generate and verify a temporary owned-child fixture with independent colors and a sibling-matching accent; contrast and semantic pairing failures must still fail.

**Acceptance Scenarios**:

1. **Given** an owned child with explicit independent color choices, **when** it is validated, **then** ownership and endorsement remain truthful while no house color is injected.
2. **Given** a valid chosen accent close to another brand's hue, **when** qualification runs, **then** hue proximity is advisory only and does not reject the brand.
3. **Given** a poor foreground/fill pair, **when** verification runs, **then** the WCAG AA gate fails for measured contrast, regardless of palette freedom.

### User Story 2 - Understand formal colors and interface cues (Priority: P0)

As a kit reader, I can see which approved colors belong to identity artwork and which communicate interface actions or states, with use, theme, measured pairing, and non-color cues explained consistently in JSON, web, portable, and PDF guides.

**Independent Test**: Build every production kit and inspect a representative multi-color mark and independent brand across machine-readable roles, theme tokens, web guideline data, portable guide, and PDF text.

**Acceptance Scenarios**:

1. **Given** a multi-color logo, **when** its guide is produced, **then** every declared formal color identifies an authoritative source and permitted use, and an approved combination points to its artwork without being mislabeled as a UI state.
2. **Given** a warning, error, success, information, action, focus, selection, or disabled cue, **when** its role is presented, **then** purpose, dark/light values, measured foreground or surface pairing, and a non-color state cue are available.
3. **Given** a color reused in identity and UI, **when** its roles are rendered, **then** the two uses remain separately named and the reuse is explicit.

### User Story 3 - Preserve approved output through migration (Priority: P1)

As an existing kit consumer, I receive the same approved logo geometry and color values after migration, while the new role metadata and compatibility aliases explain the changed policy.

**Independent Test**: Compare existing source logo path bytes and effective generated color values before and after the migration, and run every production kit and glyph verifier.

**Acceptance Scenarios**:

1. **Given** a legacy `shruggietech-house` brand, **when** S053 processes it, **then** its explicit existing choice retains its current orange values and typography independently.
2. **Given** a third-party brand that explicitly chooses a shared color, **when** it is validated, **then** the choice does not imply ownership or endorsement.
3. **Given** a missing or invalid role reference, **when** generation starts, **then** it fails before any kit or public site publication.

### Edge Cases

- A color can serve more than one role, but role names, intended uses, and non-color state cues must remain distinct.
- A visually similar sibling accent is allowed; an inaccessible foreground or indistinguishable state communicated only by color is not.
- House typography must never turn on house colors. A fixed font choice must never imply a palette.
- An owned independent brand retains parentage and endorsement facts. A third-party brand may explicitly reuse a color without acquiring those facts.
- Existing generated tokens remain compatible where practical; obsolete claims about mandatory parent colors and cross-brand hue exclusion must be removed.
- No existing logo path data, approved color value, or live brand identity is changed solely to demonstrate the new policy.

## Requirements

### Functional Requirements

- **FR-001**: Brand source and schema MUST represent multiple named formal identity colors with authoritative value references, intended uses, approved combinations, and artwork references, separately from interface cue roles.
- **FR-002**: A shared resolver MUST produce action, warning, error, success, information, focus, selection, and disabled cues for dark and light themes, including meaning, source, measured pairing, and a non-color cue. Invalid references or inaccessible text/fill pairs MUST fail before publication.
- **FR-003**: Affiliation ownership, parentage, endorsement, palette sharing, and typography mode MUST be independent decisions. An owned child MUST support independent color selection; an unrelated brand MAY explicitly share a color without claiming ownership.
- **FR-004**: The generator, canon, schema, qualification, enrichment, and verifier MUST NOT impose mandatory house orange or cross-brand hue distance on independently chosen palettes. WCAG 2.1 AA and within-interface semantic checks MUST remain effective.
- **FR-005**: Existing approved brands MUST preserve their current source color values and logo path bytes. Legacy inheritance records MUST receive an explicit compatibility meaning and no silent recoloring.
- **FR-006**: Generated tokens, adapters, registries, JSON references, hosted guidelines, portable HTML, PDF guides, and authoring/approval guidance MUST agree on the role distinction and values, with a correct-use and misuse example in each guide.
- **FR-007**: Tests MUST cover owned independent palettes, third-party shared-color choice, overlapping sibling hues, invalid references, poor contrast, non-color state cues, and existing-production migration parity.
- **FR-008**: S053 MUST use Spec Kit, run full documented production-kit/glyph/site checks, keep generated artifacts out of Git, and preserve UTF-8 without BOM, LF, and mojibake integrity.
- **FR-009**: S053 MUST NOT recolor an approved brand, alter logo geometry, complete the separate adaptive-interview redesign in #266, or claim closure of broader guideline usability #270.

### Key Entities

- **Formal identity color**: A named approved source color used in marks and brand applications, with an exact source reference and usage statement.
- **Interface cue**: A semantic role and per-theme resolved value with source reference, usage, non-color cue, and measured pairing.
- **Palette choice**: An explicit selection of shared house colors or independent values, separate from ownership and typography.
- **Compatibility record**: The documented interpretation of existing inheritance declarations and aliases after migration.

## Success Criteria

### Measurable Outcomes

- **SC-001**: An isolated owned-child fixture with no house color and a sibling-matching accent passes all relevant checks; a contrast-defective fixture fails the AA gate.
- **SC-002**: Every production kit exposes the same role values in its source-derived JSON and rendered guides; all cue pairings meet the declared measured floor.
- **SC-003**: All eight existing source brands retain their approved color and logo path values; no generated artifact is committed.
- **SC-004**: The full documented validation and required CI checks pass before owner handoff, with both issues traceable to tests and evidence.

## Assumptions

- The existing `shruggietech-house` inheritance value remains an explicit opt-in to the historical shared orange pair for compatible sources; ownership no longer selects or requires it.
- Existing `semantic_colors` remains the compatibility source for emphasis and action until a separate versioned token migration is justified. New role metadata references values rather than duplicating them.
- Status roles require words or icons in UI examples; contrast gates are measured on the actual theme pairing, not inferred from hue distance.
