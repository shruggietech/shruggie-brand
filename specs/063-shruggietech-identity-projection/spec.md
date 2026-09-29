# Feature Specification: ShruggieTech Identity Projection

**Feature Branch**: `codex/063-shruggietech-identity-projection`

**Created**: 2026-09-28

**Status**: Draft

**Input**: S063 resolves #294, #293, and #295 as one source-bound ShruggieTech identity correction across kit, site, and guidance.

## User Scenarios & Testing

### User Story 1 - Choose the correct square mark (Priority: P1)

A person selecting a ShruggieTech icon, avatar, app icon, or square logo receives the face-only artwork at every size. The full arms mark remains available only in approved paired and header or footer compositions.

**Independent Test**: Build the ShruggieTech kit and inspect every square asset and its manifest role, plus the paired lockups and documented usage rules. Compare the source identities without changing the paid artwork bytes.

**Acceptance Scenarios**:

1. **Given** a standalone square delivery at any supported size or platform, **when** the kit is built, **then** it uses the reduced face and never the arms-only mark.
2. **Given** an approved paired wordmark, slogan composition, website header or footer, or document footer, **when** it is rendered, **then** the full mark remains available with the correct role label.
3. **Given** the green-on-black face, **when** it is rendered at 16, 32, 48, and representative larger sizes, **then** interior pixels read as the approved bright green within raster tolerance and the face remains legible without clipping.

### User Story 2 - Recognize the parent brand in the portfolio (Priority: P1)

A visitor scanning the brand portfolio sees a square ShruggieTech face with perceived scale comparable to the other brand cards.

**Independent Test**: Render the portfolio beside all published peer cards at desktop and narrow mobile widths and inspect the source asset, generated site record, and accessible card content.

**Acceptance Scenarios**:

1. **Given** the portfolio card, **when** it is rendered, **then** its icon uses a square face-only source with no unused wide canvas reducing the visible mark.
2. **Given** desktop and narrow mobile layouts, **when** all cards are compared, **then** the parent face is comparably legible without cropping, overflow, or a regression in peer cards.

### User Story 3 - Read the exact approved slogan (Priority: P1)

A viewer of ShruggieTech social artwork, kit guidance, and published projections sees the exact slogan “We’ll figure it out.” Introductory uses of “We advance your vision.” retain their own role and are not silently replaced.

**Independent Test**: Trace each slogan and headline consumer from the canonical source through the generated social image, guide, metadata, kit manifest, and site; assert exact wording and role, including punctuation.

**Acceptance Scenarios**:

1. **Given** a field or asset labeled as the ShruggieTech slogan, **when** it is delivered, **then** it shows exactly “We’ll figure it out.”
2. **Given** introductory or headline copy using “We advance your vision.”, **when** the change is applied, **then** those uses are inventoried and retained in their distinct role unless a source-bound owner decision changes them.
3. **Given** a changed assembled social image, **when** it is proposed for final compilation, **then** the existing Gate 2 review contains the actual rendered candidate and its source and manifest identities.

### Edge Cases

- A square delivery may use a transparent, opaque, light, dark, maskable, monochrome, or platform-specific presentation. Each retains the face-only source role while satisfying its destination's safe area.
- A small favicon may require a different amount of inset than a large store icon. Optical maximization does not permit cropping or platform-safe-area violations.
- The paid raster masters may have transparent or low-luminance pixels. Any changed mask or derivation needs the approval and provenance required by the existing source contract before final publication.
- An unchanged introductory phrase may also appear in a guide field. Its distinct role must be documented rather than misreported as the slogan.
- Missing rendering capabilities must be reported as skips; a rendered candidate cannot be called approved until the applicable creative gate is recorded.
- Shared generator edits must retain every existing approved i-heart-pr-tours proof and comparison evidence exactly on the canonical host or continue to fail its continuity gate. A portable host may use the existing measured comparison only when a current canonical-host attestation binds the same renderer settings and all 32 exact approvals. Renderer-family changes cannot inherit the earlier approval.

## Requirements

### Functional Requirements

- **FR-001**: Every ShruggieTech standalone square asset, including logo exports and previews, favicons, avatars, web installable icons, Android, Apple, macOS, Windows, store, and manifest references, MUST use the approved face-only source at all sizes. The inventory MUST distinguish standalone square roles from allowed paired and header or footer uses of the full arms mark.
- **FR-002**: The face MUST be deliberately framed within each destination's actual safe area, optically comparable to peer square marks where shown together, and never cropped or distorted. Required dark, light, transparent, monochrome, and platform variants MUST preserve source identity and correct labels.
- **FR-003**: The green-on-black face MUST use the approved bright-green token in its interior rendered pixels within documented raster tolerance. Antialiasing MUST be assessed at 16, 32, 48, and representative larger sizes.
- **FR-004**: Authoritative paid source artwork and path or image data MUST remain byte-for-byte unchanged. A changed mask or derivation MUST receive the existing source-bound approval and provenance before final kit compilation. A changed assembled social image MUST receive the existing Gate 2 approval; no new creative gate is added.
- **FR-005**: The portfolio card MUST consume a square-proportioned face-only source and present a comparable perceived scale at desktop and narrow mobile widths, without breaking the shared card presentation or accessibility.
- **FR-006**: The canonical ShruggieTech slogan MUST be exactly “We’ll figure it out.” Provenance MUST mark the older S057 slogan classification as superseded while retaining legitimate “We advance your vision.” introduction or headline uses in their own roles.
- **FR-007**: Generated social artwork, kit guidance, site metadata, portable and hosted projections, PDF text, manifests, labels, and download names MUST agree with the canonical slogan and mark roles where those roles are displayed. No blind global replacement or guide-only patch may substitute for a source correction.
- **FR-008**: Automated regression coverage MUST reject an arms-only square output, muted interior green, incorrect square framing, incorrect slogan punctuation or role, stale approval binding, or source identity drift. Documented kit and site validation MUST pass without weakening accessibility or source controls.

### Key Entities

- **Authoritative mark**: Paid full and reduced raster masters, their exact digests, approved mask methods, and permitted transformations.
- **Delivery role**: Intended use, square or paired geometry, platform safe area, color presentation, source variant, filename, and manifest binding.
- **Approved message**: Exact slogan text, distinct headline or introduction text, intended use, superseded classification, and approval provenance.
- **Review packet**: Exact source identity, candidate derivatives, rendered proofs, measured results, and applicable Gate 1 or Gate 2 decision.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every generated standalone square ShruggieTech asset and its delivery manifest uses the face-only source; zero arms-only square assets remain.
- **SC-002**: Rendered proofs at 16, 32, 48, and representative large sizes demonstrate legible bright-green face interiors, safe-area fit, and no clipping. The portfolio comparison covers desktop and narrow mobile widths and all published peer cards.
- **SC-003**: Every output claiming the slogan matches “We’ll figure it out.” character-for-character, including the apostrophe and period. The prior phrase is documented only in its retained introduction or headline roles.
- **SC-004**: The source artwork digests remain unchanged, applicable Gate 1 and Gate 2 decisions bind the exact approved candidates, and all eight production kits report zero verifier problems and zero glyph failures.
- **SC-005**: Full documented repository validation, including site rendering and accessibility checks, passes; each issue #293, #294, and #295 has acceptance-to-evidence disposition.

## Assumptions and Boundaries

- The owner's exact slogan correction and square-use direction are requirements. Approval of a specific new derivation or assembled image is recorded through the existing creative gates when applicable.
- The broader eight-brand messaging schema and Brand essentials redesign belong to #296 through #298; S063 uses the current approved social-copy contract.
- Generated kits, site exports, raster proofs, and review packets remain outside Git. Only governed sources, generator code, documentation, tests, and Spec Kit evidence are committed.
- A formal release, site deployment, and merge are separate from this pull request.
