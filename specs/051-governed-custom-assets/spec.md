# Feature Specification: Governed Custom Assets and Expressions

**Feature Branch**: `codex/051-governed-custom-assets`

**Created**: 2026-09-23

**Status**: Approved for implementation

**Input**: S051 approval to implement [#194](https://github.com/shruggietech/shruggie-brand/issues/194), governing optional brand-owned custom assets and publishing eligible expressions across generated and hosted outputs.

## User Scenarios & Testing

### User Story 1 - Declare a non-core custom asset (Priority: P1)

As a brand maintainer, I can register a supplied stylized mark, campaign treatment, mood image, environmental asset, or background without granting it core-logo authority.

**Independent Test**: Declare the two supplied I Heart PR Tours sand SVGs and validate their sources, metadata, and role separately from core logo roles.

**Acceptance Scenarios**:

1. **Given** a valid optional `custom_assets` record, **when** the brand is validated, **then** its ID, role, source, hash, provenance, approval, transformations, usage, legibility, attribution, license, and publication eligibility are checked and retained.
2. **Given** an absent or empty collection, **when** a brand is built, **then** existing output is unchanged and no expressions section appears.
3. **Given** a custom expression, **when** logo rules are produced, **then** it does not become a canonical logo or override approved logo geometry.

---

### User Story 2 - Reject unsafe or ambiguous declarations (Priority: P1)

As a publisher, I can trust that invalid, changed, externally hosted, or unapproved assets do not leak into public deliverables.

**Independent Test**: Mutate one field at a time in a temporary brand fixture and run contract and generation gates.

**Acceptance Scenarios**:

1. **Given** path traversal, hotlink, missing file, unsupported format, duplicate ID, or stale SHA-256, **when** validation runs, **then** it fails with the affected asset ID and cause.
2. **Given** missing ownership, provenance, attribution, license, usage rules, or accessibility guidance, **when** validation runs, **then** it fails clearly.
3. **Given** an unapproved or non-public asset, **when** outputs are built, **then** it is excluded from PDF, portable guide, site, asset library, and downloads.
4. **Given** a source asset, **when** a kit is built, **then** its source bytes remain unchanged.

---

### User Story 3 - Browse expressions wherever brand guidance appears (Priority: P2)

As a reader, I can find approved expressions and atmosphere in PDF, portable and hosted guides, asset library, and download kit, with coherent metadata and safe previews.

**Independent Test**: Build I Heart PR Tours and a brand without custom assets, inspect each output and compare inventory IDs to the declared eligible set.

**Acceptance Scenarios**:

1. **Given** eligible assets, **when** guides and site are built, **then** each eligible ID appears in all applicable inventories with the same title, role, credit, license, use limits, and source link.
2. **Given** no eligible assets, **when** guides and site are built, **then** no empty Expressions and atmosphere topic, nav item, or download category appears.
3. **Given** a preview, **when** rendered, **then** its declared light/dark/grid/image well is respected without crop, distortion, recolor, or text-over-image contrast failure; alt text and motion guidance remain available.

### Edge Cases

- IDs and committed relative paths must be unique. Path checks must reject both separator styles, absolute paths, symlink escapes, query strings, fragments, and URL schemes.
- SVGs must not carry active content or external references; supplied path geometry is never rewritten.
- Source format and hash are declaration facts, not inferred approval. Approval and publication eligibility are distinct.
- Animated or WebGL-like media may be modeled with reduced-motion guidance but are not newly published in this slice unless the generator can safely support their preview format.
- Non-photographic or generated imagery must be disclosed when applicable, without inventing imagery in this slice.

## Requirements

### Functional Requirements

- **FR-001**: Brand manifests MUST support an optional `custom_assets` collection for non-core assets with stable IDs and role/category.
- **FR-002**: Each asset MUST declare committed relative source, source format and SHA-256, owner or generator provenance, approval state, publication eligibility, allowed transformations, positive and negative usage guidance, accessibility/legibility guidance, attribution, and license.
- **FR-003**: Validation MUST reject traversal or external paths, escapes outside the brand source tree, missing sources, stale hashes, duplicate IDs/paths, unsupported public formats, ambiguous ownership, and public use without approval.
- **FR-004**: Public outputs MUST derive from the same eligible manifest set. Ineligible assets MUST remain outside all public guide, site, library, and download surfaces.
- **FR-005**: Eligible assets MUST have an optional Expressions and atmosphere section in generated PDF and portable guidelines, hosted guideline topic/navigation, and asset library/download kit. No section or category may appear when the set is empty.
- **FR-006**: Preview metadata MUST support bounded light, dark, grid, or image wells, fit-without-crop, meaningful alt text, text-overlay guidance, and reduced-motion guidance when motion applies. Previews MUST preserve source geometry and legibility.
- **FR-007**: The two supplied I Heart PR Tours sand SVGs MUST be first governed fixtures. Their bytes and canonical logo authority MUST remain unchanged.
- **FR-008**: Contract and generation tests MUST cover valid, empty, and negative fixtures, source-byte preservation, cross-output inventory completeness, and accessibility behavior.
- **FR-009**: Documentation MUST explain the manifest contract, publication gates, preview guidance, and how to add an approved custom expression.
- **FR-010**: S051 MUST NOT create artwork, modify downstream repositories, publish a release tag, or merge its own PR.

### Key Entities

- **Custom asset**: A brand-owned, non-core visual source with identity, provenance, usage, accessibility, and publication metadata.
- **Eligible set**: Valid, approved assets explicitly marked for public publication.
- **Expression inventory**: The same eligible IDs projected into guide, portal, library, and download output.
- **Preview contract**: Declared surface and fitting rules that preserve geometry and readable surrounding content.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Both supplied sand SVGs pass governance and appear in every required eligible output with identical IDs, with zero source-byte changes.
- **SC-002**: A brand with no eligible custom assets produces zero empty expression sections, navigation entries, and download categories.
- **SC-003**: Every negative fixture in FR-003 fails its intended gate with a cause-specific diagnostic; an unapproved asset appears in zero public outputs.
- **SC-004**: Full documented production, glyph, markdown, and site validation passes, including measured WCAG 2.1 AA checks where presentation introduces foreground/background pairings.

## Assumptions

- Issue #194 is authoritative. Existing `guide.expressions` entries are transitional data, not a second independent authority; the governed collection replaces them while retaining visible content.
- Supplied sand SVGs and existing ownership records are the only production fixtures in this slice.
- The implementation may model future generated or moving artwork, but does not create or publish new artwork without the owner supplying and approving it.
