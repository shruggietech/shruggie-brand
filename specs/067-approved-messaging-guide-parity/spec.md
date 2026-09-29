# Feature Specification: Approved Messaging and Guide Parity

**Feature Branch**: `codex/067-approved-messaging-guide-parity`

**Created**: 2026-09-29

**Status**: Draft

**Input**: S067 implements issues #296 and #297 against the current eleven-brand inventory.

## User Scenarios & Testing

### User Story 1 - Record approved messages (Priority: P1)

As a brand owner, I can supply exact wording for each message role, its intended use and source, and leave a role absent or unresolved without another sentence being substituted.

**Why this priority**: A guide cannot be faithful until a slogan, description, introduction, and social composition have independent meanings.

**Independent Test**: Sparse, rich, absent, and conflicting briefs preserve independent state and publish only approved wording in authorized uses.

**Acceptance Scenarios**:

1. **Given** an approved slogan and unresolved descriptions, **when** guides render, **then** the slogan is exact and no description is inferred.
2. **Given** a social-image line approved only for that image, **when** a visual guide renders, **then** reuse as a general slogan requires separate intended-use evidence.
3. **Given** an explicitly absent optional strategy statement, **when** a kit compiles, **then** that statement is omitted without an additional creative gate.

### User Story 2 - Read the same approved copy in every guide (Priority: P1)

As a kit reader, I see consistent roles and exact approved wording in the PDF, portable guide, hosted guide, social image where applicable, and consumer data; visual examples come from shipped assets.

**Why this priority**: Existing guide overrides and generated defaults produce contradictory brand claims.

**Independent Test**: Compare source values with extracted PDF text, portable and hosted content, social copy, and consumer data for all eleven brands.

**Acceptance Scenarios**:

1. **Given** different introductory copy and an approved slogan, **when** the cover renders, **then** the slogan label carries only the slogan and the introduction retains its own role or is omitted.
2. **Given** no approved description, **when** guides render, **then** no descriptor, brand idea, product summary, or generated sentence appears in a description role.
3. **Given** a guide override that conflicts with canonical copy, **when** validation runs, **then** the conflict is reported instead of publishing either value as approved.

### User Story 3 - Review the migration (Priority: P2)

As the owner, I can inspect old wording, original location, current classification, provenance, and unresolved choices for each production brand.

**Why this priority**: Legacy phrases must neither disappear nor be promoted through inference.

**Independent Test**: An inventory covers eleven records, including descriptors, ideas, social lines, overrides, and material company or product claims.

**Acceptance Scenarios**:

1. **Given** Fragcap and Go Schedule's differing idea and social lines, **when** the inventory is read, **then** each phrase retains its source role.
2. **Given** ShruggieTech's superseding owner correction, **when** the migration is read, **then** “We’ll figure it out.” is the exact slogan and “We advance your vision.” remains introductory copy.

### Edge Cases

- Preserve curly punctuation, casing, and exact wording; layout line breaks are presentation choices.
- An unresolved candidate may be retained for review but cannot publish as approved copy.
- An absent role has no value and cannot be filled from another field.
- Mission and vision are optional strategy roles, omitted from visual guides unless their approved intended use includes that surface.
- A time-sensitive product claim needs an owned source; old guide text alone is not approval.

## Requirements

### Functional Requirements

- **FR-001**: Every production brand MUST classify independent slogan, short-description, and long-description roles with exact text when approved, intended use, provenance, and `approved`, `absent`, or `unresolved` state.
- **FR-002**: The contract MUST support optional positioning, mission, vision, values, brand promise, and introductory statement with the same independent rules.
- **FR-003**: Approved messages MUST record owner decision and permitted uses; absent and unresolved values MUST not appear as approved public guidance.
- **FR-004**: The adaptive interview and Gate 2 packet MUST show applicable roles and representative uses separately while retaining exactly the existing two mandatory creative gates.
- **FR-005**: A migration inventory MUST preserve and classify legacy descriptors, ideas, social lines, guide overrides, and material claims for all eleven brands with unknowns explicit.
- **FR-006**: PDF, portable, hosted, social, and consumer projections MUST display exact approved text only for its authorized role and surface; missing roles are omitted without invented brand prose.
- **FR-007**: Brand-specific guide overrides MUST move to canonical reviewed source or be rejected by validation; common explanatory guidance MUST reside in shared shipped source.
- **FR-008**: Every guide field and visual example MUST trace to a kit field or shipped asset, documented in an eleven-brand field-to-source map.
- **FR-009**: Validation MUST detect substitution, exact-text drift, stale overrides, unsupported claims, and asset mismatches. PDF checks MUST measure content and layout instead of bytes.
- **FR-010**: Approved logo geometry and social-image compositions MUST remain unchanged unless approved through the existing gates.
- **FR-011**: Documentation MUST explain visual-guide versus strategy-reference placement and approval of live product claims.

### Key Entities

- **Message role**: A distinct purpose, such as slogan or short description.
- **Message decision**: A role's state, exact approved wording, intended uses, source, approver, and date.
- **Legacy inventory item**: Original location and exact text with classification, evidence, and unresolved decision.
- **Guide projection**: A labeled appearance of one approved message or shipped asset on a guide surface.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All eleven current brand records and their legacy messages appear in the inventory, with no unclassified override or material claim.
- **SC-002**: Approved messages on multiple surfaces retain exact wording and role labels; absent and unresolved values appear on zero public guide surfaces.
- **SC-003**: Fragcap, Go Schedule, Glitchpad, and ShruggieTech pass exact role and punctuation comparisons, including extracted PDF and rendered guide text.
- **SC-004**: Every production kit reports zero verifier problems and glyph failures, and full documented guide/site validation passes without accessibility regression.
- **SC-005**: The creative approval flow retains exactly two mandatory gates and adds no required strategy statement.

## Assumptions

- The current inventory is eleven brands, superseding the issue intake's eight-brand count.
- Existing social approval authorizes exact image copy for social use, not automatically a reusable visual-guide slogan or description.
- ShruggieTech's exact correction in #295 is owner-approved for slogan use; other cross-surface promotions need evidence.
- The broader Brand essentials redesign in #298 and documentation navigation in #299 remain separate.
- No approved logo or social-image bytes need alteration for guide projection.
