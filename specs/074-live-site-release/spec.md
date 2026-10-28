# Feature Specification: BrandBuilder 3.1.1 Live Site Release

- **Feature Branch**: `codex/074-live-site-release`
- **Created**: 2026-10-28
- **Status**: In progress
- **Input**: Owner request to update the live website end to end without further input.

## User Scenarios & Testing

### User Story 1 - Read the current public site (Priority: P1)

A visitor sees the approved portfolio descriptions, the corrected portfolio heading and card-title layout, and the complete References page at `brand.shruggie.tech`.

**Independent Test**: Open the public homepage and References page after Pages deployment and compare their visible content and layout with the tagged candidate.

**Acceptance Scenarios**:

1. **Given** v3.1.0 is live, **when** v3.1.1 Pages deployment succeeds, **then** the home page presents the S072 approved copy and S073 layout from the verified tag.
2. **Given** a visitor opens a brand guide or download, **when** the new site is live, **then** it resolves to a generated v3.1.1 kit, with the official release link pointing at the same version.

### User Story 2 - Obtain the exact release (Priority: P1)

A consumer can obtain official, checksum-verified v3.1.1 packages with accurate version and migration guidance.

**Independent Test**: Compare the tag revision, release metadata, uploaded asset names and SHA256SUMS against the CI candidate.

**Acceptance Scenarios**:

1. **Given** reviewed and green release metadata on main, **when** the annotated tag is pushed, **then** tag preflight, release publishing and Pages deployment all succeed from that revision.
2. **Given** a mismatch in version, ancestry, asset identity or checksum, **when** preflight or publication runs, **then** promotion stops before mismatched bytes are served.

### Edge Cases

- A new main commit arrives before tagging: inspect it and tag only the reviewed release revision if it remains an ancestor of main and its checks remain valid.
- A release or deployment run is partial: compare existing tag, release, and asset inventory before resuming the same revision.
- External review findings arrive on the preparation PR: resolve actionable findings and require green checks on the final reviewed head.

## Requirements

### Functional Requirements

- **FR-001**: BrandBuilder, site, release-impact metadata, dated root and skill history, and the seven edited brand packages MUST use coordinated patch versions.
- **FR-002**: Release notes MUST state BrandBuilder 3.1.1, Brand Canon 2.1.0, and the migration effect of approved messaging, generator corrections, site layout and dependency updates.
- **FR-003**: All thirteen production kits MUST pass the documented verifier and glyph gates; site and accessibility validation MUST pass before publication.
- **FR-004**: The release preparation PR MUST pass CI and receive review resolution before merge.
- **FR-005**: The `v3.1.1` tag, official release assets and Pages artifact MUST derive from the same verified main revision.
- **FR-006**: The public home page and References page MUST expose the merged S072 and S073 changes; downloads and release link MUST resolve to v3.1.1.
- **FR-007**: Generated artifacts and machine-local Spec Kit state MUST remain outside Git.

### Key Entities

- **Candidate**: The exact reviewed source revision and its built kits, site and release assets.
- **Release**: The annotated `v3.1.1` tag and official GitHub asset inventory.
- **Deployment**: GitHub Pages artifact from the tag workflow served at `brand.shruggie.tech`.

## Success Criteria

- **SC-001**: The tag workflow's build, preflight, release and Pages jobs succeed on one source SHA.
- **SC-002**: Every production kit has zero verifier problems and zero glyph failures; the site passes its WCAG 2.1 AA gate.
- **SC-003**: The public site visibly contains the approved copy and corrected home and References presentation.
- **SC-004**: Official release assets match the expected inventory and checksum record; no generated files enter Git.

## Assumptions

- The owner's unattended deployment request authorizes the release PR, merge, annotated tag, release publication and Pages deployment.
- v3.1.1 is the next patch version. Brand Canon, identity geometry, palettes, fonts and adapter APIs remain at their current versions.
