# Feature Specification: Asset Delivery Fidelity

**Feature Branch**: `codex/021-asset-delivery-fidelity`

**Created**: 2026-09-08

**Status**: Implementation and local validation complete

**Input**: User description: "Combine GitHub issues #166 and #165 into S021, restoring Glitchpad's complete black and white full lockups and vertically centering and containing every asset-card preview without altering approved source artwork."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Download complete monochrome Glitchpad lockups (Priority: P1)

A user browsing or downloading Glitchpad's black and white full lockups receives the complete approved paper-and-G mark beside the complete wordmark, with monochrome treatment as the only permitted visual difference from the approved full lockup.

**Why this priority**: The current public delivery is corrupted and is a release-blocking identity failure across every advertised size and format.

**Independent Test**: Inspect and compare each black and white full-lockup delivery against the approved full-lockup structure. Every required mark component and the complete wordmark must remain present, proportionate, unclipped, and consistent across formats and sizes.

**Acceptance Scenarios**:

1. **Given** the approved Glitchpad full lockup, **When** a black or white full-lockup asset is generated, **Then** the complete paper-and-G mark and complete wordmark are present with unchanged structure, composition, proportions, alignment, and clear space.
2. **Given** any advertised black or white full-lockup download, **When** the user opens the vector or raster file, **Then** it visibly matches the corresponding preview and contains the complete lockup.
3. **Given** an output in which the paper, G, square, or other required mark component disappears, clips, collapses, or is substituted, **When** the kit is verified, **Then** verification fails before publication.

---

### User Story 2 - Trust every asset preview (Priority: P2)

A visitor can browse every brand's asset library and logo examples without artwork sitting against an edge, crossing the metadata divider, being cropped, or appearing distorted.

**Why this priority**: Inconsistent preview wells make valid assets appear broken and prevent users from confidently selecting the correct delivery.

**Independent Test**: Exercise every preview category with wide, tall, square, transparent, and opaque assets at desktop, tablet, and mobile widths in both themes. Each asset remains centered, contained, and separated from metadata.

**Acceptance Scenarios**:

1. **Given** any asset-card preview, **When** it is rendered at a supported viewport, **Then** the preview artwork and its presentation surface remain wholly inside a consistently sized media region above the metadata divider.
2. **Given** an asset with a wide, tall, square, transparent, or opaque canvas, **When** it is previewed, **Then** its aspect ratio and approved clear space remain unchanged and its opposing vertical margins are equal within normal raster-rounding tolerance.
3. **Given** the same asset library in light and dark themes, **When** the theme changes, **Then** containment, alignment, and card geometry remain equivalent.

---

### User Story 3 - Prevent delivery and preview regressions (Priority: P3)

A maintainer receives a failing quality gate when a monochrome full lockup loses required structure or when any preview paints outside its media region.

**Why this priority**: The defects escaped existing verification, so durable detection is required to keep future generator and site changes safe.

**Independent Test**: Introduce isolated synthetic failures matching the observed fold-fragment-only output and preview overflow. The quality gates must reject each failure while accepting complete assets of varied shapes.

**Acceptance Scenarios**:

1. **Given** a synthetic black or white full lockup with only a fold or detail fragment, **When** verification runs, **Then** it fails for missing required mark structure.
2. **Given** a preview whose artwork or background crosses its media boundary, **When** layout verification runs, **Then** it fails with the affected asset and boundary identified.
3. **Given** canonical source artwork and generated deliveries before and after the presentation correction, **When** source and delivery integrity are compared, **Then** no unrelated canonical geometry or delivery bytes changed.

### Edge Cases

- A transparent monochrome asset must be evaluated against an explicit preview surface rather than appearing empty or inheriting an accidental page color.
- An opaque icon or social image may include a baked background, but that background must remain inside the media region.
- A very wide lockup and a tall platform asset must both retain aspect ratio without using category-specific offsets.
- Wrapped asset titles and variable metadata lengths must not change the media-region boundary or allow preview paint to overlap details.
- Vector and raster deliveries of the same variant must preserve equivalent visible structure even though their file encodings differ.
- Reduced marks remain distinct from full marks and must never be substituted into full-lockup output.
- Monochrome transformation may change governed color treatment but must not redraw, simplify, invert with presentation filters, or reconstruct the approved geometry.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every Glitchpad full black and full white lockup MUST contain the complete approved full mark and complete wordmark.
- **FR-002**: Monochrome full lockups MUST preserve the approved full-lockup silhouette, component relationships, proportions, alignment, canvas, and clear space apart from the governed color transformation.
- **FR-003**: Every advertised vector and raster size for the affected variants MUST represent the same complete lockup.
- **FR-004**: Guidelines examples and asset-library previews MUST display the exact corresponding shipped delivery rather than a substitute or independently reconstructed image.
- **FR-005**: Downloaded files MUST agree with their preview and declared delivery metadata.
- **FR-006**: Verification MUST reject a full monochrome lockup that omits, clips, collapses, or substitutes any required mark component or the wordmark.
- **FR-007**: Regression coverage MUST include the observed fold-fragment-only failure for both black and white full lockups.
- **FR-008**: The correction MUST NOT redraw, normalize, approximate, simplify, crop, trace, or modify approved Glitchpad source geometry.
- **FR-009**: The correction MUST NOT use a presentation filter, per-page asset substitution, or brand-specific visual offset as a repair.
- **FR-010**: Every visual asset preview category MUST use one shared containment and alignment contract.
- **FR-011**: Every preview media region MUST have a stable boundary that remains separate from the metadata region.
- **FR-012**: Preview artwork, presentation surfaces, backgrounds, and shadows MUST remain entirely within the media region and MUST NOT cross the metadata divider.
- **FR-013**: Wide, tall, square, transparent, and opaque previews MUST preserve their aspect ratio and approved clear space without cropping or stretching.
- **FR-014**: Preview artwork MUST be vertically and horizontally centered within its media region within normal raster-rounding tolerance.
- **FR-015**: Preview containment and alignment MUST remain consistent across all production brands, asset categories, themes, and supported desktop, tablet, and mobile widths.
- **FR-016**: Automated layout coverage MUST measure the preview media boundary, rendered preview boundary, and metadata divider and MUST fail on overflow or misalignment.
- **FR-017**: Presentation-only corrections MUST leave canonical source artwork and generated delivery bytes unchanged.
- **FR-018**: The final production kits and public site MUST pass their complete existing identity, accessibility, responsive-layout, static-publication, and artifact-integrity gates.

### Key Entities

- **Approved full lockup**: The governed composition of the full Glitchpad mark and wordmark, including component identity, proportions, alignment, canvas, and clear space.
- **Monochrome delivery family**: The black and white vector masters and every raster size derived from each master.
- **Asset preview**: The exact shipped delivery selected for a guideline example or asset-library card, together with its declared presentation surface.
- **Preview media region**: The bounded card area reserved for artwork and any presentation background, separate from the asset metadata.
- **Delivery manifest record**: The declaration connecting an asset identity, variant, format, dimensions, preview, download, and integrity evidence.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100 percent of Glitchpad black and white full-lockup vector and raster deliveries contain every required full-mark component and the complete wordmark.
- **SC-002**: 100 percent of affected downloads visually agree with their previews and manifest records.
- **SC-003**: Across every production brand, preview category, theme, and tested viewport, zero preview pixels or presentation backgrounds cross the media-region boundary or metadata divider.
- **SC-004**: Every tested preview is centered within one device pixel vertically and horizontally when the source canvas permits symmetric placement.
- **SC-005**: Wide, tall, square, transparent, and opaque fixtures exhibit zero cropping, stretching, or aspect-ratio drift.
- **SC-006**: Both black and white fold-fragment-only regressions fail verification before publication.
- **SC-007**: Canonical Glitchpad source geometry remains byte-identical, and presentation-only changes alter zero generated delivery bytes.
- **SC-008**: All production kits report zero verification problems and zero glyph failures, and all public routes pass the documented accessibility and responsive-layout gate.

## Assumptions

- GitHub issues #166 and #165 are the complete scope of S021.
- The current approved Glitchpad full and reduced source paths remain authoritative and cannot be changed in this slice.
- Black and white are governed output treatments, not new identity variants requiring owner selection.
- Shared fixes apply to any production brand affected by the same generation or preview behavior.
- Existing asset categories, delivery naming, download routes, and metadata labels remain stable.
- No release or version bump is included; this slice prepares a merge-ready correction only.

## Scope Boundaries

### In Scope

- Correct the shared generation or selection path responsible for incomplete Glitchpad black and white full lockups.
- Strengthen structural and rendered verification for monochrome full lockups and their raster derivatives.
- Establish shared asset-preview containment and centering across guideline examples and asset-library cards.
- Add isolated regression inputs and browser layout measurements for both reported defects.
- Rebuild and visually inspect all production brands, themes, and representative viewport classes.

### Out of Scope

- Any Glitchpad identity redesign or source-geometry edit.
- Changes to full/reduced identity policy, lockup naming, delivery inventory, or platform safe-area ratios.
- General site interaction polish tracked by GitHub issues #163 and #164.
- Release tagging, publishing a versioned archive, or changing licensing terms.

## Traceability

- **GitHub Issue #166**: Restore the missing mark in Glitchpad black and white full lockups.
- **GitHub Issue #165**: Vertically center and contain every asset-card preview.
