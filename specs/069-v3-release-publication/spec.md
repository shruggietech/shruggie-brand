# Feature Specification: BrandBuilder 3.0.0 Release Publication

**Feature Branch**: `codex/069-v3-release-publication`
**Created**: 2026-09-29
**Status**: In progress
**Input**: Owner request to complete the full up-to-date release process without intermediate handoffs.

## User Scenarios & Testing

### User Story 1 - Obtain the current official release (Priority: P1)

An integrator can download BrandBuilder 3.0.0 and each release-authorized brand archive from one official release, with matching checksums, source revision, and migration guidance.

**Why this priority**: The latest published release is 2.8.0 while the reviewed source and generated guide contract are at 3.0.0.

**Independent Test**: Inspect the exact tagged release, download its inventory and checksum record, and compare version and source identity with the tagged revision.

**Acceptance Scenarios**:

1. **Given** the reviewed 3.0.0 source on `main`, **when** the exact tag is published, **then** the official release contains the skill, portable distribution, eight authorized brand archives, and checksum record built from that tag.
2. **Given** a release archive, **when** its version, revision, contents, or checksum differs from the tagged candidate, **then** publication stops before serving it as official.

---

### User Story 2 - Read current guides and migration impact (Priority: P1)

A reader sees the 3.0.0 Brand essentials and exact approved messaging in the published site and guides, with a working release link and clear migration guidance.

**Why this priority**: S067 and S068 changed the current source and guide contract after the 2.8.0 release.

**Independent Test**: Compare the published guide, release notes, and downloadable guide content against the tagged source and all eleven built brand kits.

**Acceptance Scenarios**:

1. **Given** the 3.0.0 tag, **when** the site is published, **then** all eleven production brand guides derive from verified kits and the manual shows the exact 3.0.0 release link.
2. **Given** a consumer of an older kit, **when** they read the notes, **then** they can identify BrandBuilder 3.0.0, Brand Canon 2.0.0, and the required source and guide migration.

---

### User Story 3 - Recover from a failed publication (Priority: P2)

An operator can identify whether a failed tag run published no release, an incomplete release, or a complete release, and resume without substituting bytes from another revision.

**Why this priority**: Release assets and site deployment must remain pinned to the exact reviewed revision even across reruns.

**Independent Test**: Exercise the release contract's failure cases and confirm that a repeated run either reuses the same verified candidate or stops without replacing a published asset.

**Acceptance Scenarios**:

1. **Given** a failed verification or incomplete candidate, **when** publication is attempted, **then** no production site or official release is promoted.
2. **Given** an existing 3.0.0 release, **when** a retry is considered, **then** its tag, asset names, and checksums are compared before any update.

### Edge Cases

- A newer commit arrives on `main` after review: tag the reviewed release commit only if it remains an ancestor of `main` and its exact candidate gates pass.
- A new GitHub issue or PR arrives during the release: assess whether it is a release blocker; do not silently add unrelated work to the frozen candidate.
- A hosted brand has no formal release archive: retain its generated site download and candidate status without claiming a GitHub release archive.
- CI or external review is pending, failed, or unresolved: stop promotion until the exact reviewed revision is green and comments are resolved.

## Requirements

### Functional Requirements

- **FR-001**: The 3.0.0 release MUST identify the reviewed source revision, BrandBuilder 3.0.0, Brand Canon 2.0.0, and exact migration impact.
- **FR-002**: Release notes MUST incorporate the S067 and S068 changes, including source-bound message roles, Brand essentials, Usage limits, and documentation navigation.
- **FR-003**: The published asset inventory MUST match the current release authorization contract: one skill, one portable bundle, eight brand archives, and `SHA256SUMS`. The three other public brands MUST remain in the eleven-brand hosted kit inventory without being described as formal release archives.
- **FR-004**: Every published archive and site artifact MUST derive from the exact tagged, reviewed, CI-verified commit; the release MUST NOT mix candidate revisions or overwrite prior immutable packages.
- **FR-005**: All eleven production kits MUST pass the documented build, verifier, glyph, PDF, site, and accessibility gates before tag promotion.
- **FR-006**: The release preparation PR MUST have all required checks green and all received security and Codex findings resolved before merge. It MUST complete exactly two Codex review rounds and MUST NOT trigger a third.
- **FR-007**: Publication MUST occur only after the release preparation changes are merged to `main` and the exact tag's release preflight passes.
- **FR-008**: The published site MUST link to the exact 3.0.0 release and expose the eleven source-derived brand guides without claiming unpublished archive status for the three candidate brands.
- **FR-009**: Release failure or retry MUST preserve checksum and revision identity; any partial release state requires an inventory comparison before resuming.
- **FR-010**: Generated kits, exports, PDFs, release archives, and machine-local Spec Kit state MUST remain uncommitted.

### Key Entities

- **Release candidate**: Exact source revision, version tuple, tested brand-kit and site output, archive inventory, and checksums.
- **Official release**: Immutable `v3.0.0` tag and uploaded asset inventory derived from the candidate.
- **Hosted brand**: One of eleven verified site kits; eight are also formal release archives under the current contract.
- **Publication record**: Exact candidate or release status, version, tag, source revision, and download destinations.

## Success Criteria

### Measurable Outcomes

- **SC-001**: One official `v3.0.0` release contains exactly ten distribution files plus `SHA256SUMS`, all tied to one tagged source revision.
- **SC-002**: All eleven production kits report zero verifier problems and zero glyph failures, and the site reports zero WCAG 2.1 AA violations in its documented checks.
- **SC-003**: Release notes and published documentation agree on BrandBuilder 3.0.0, Brand Canon 2.0.0, and the guide migration.
- **SC-004**: The release and Pages deployment succeed from the exact tag, and published downloads pass the uploaded checksum record.
- **SC-005**: No generated or machine-local output appears in the release preparation commit.

## Assumptions

- The owner's authorization covers PR publication, merge, exact tag creation, and release publication for this slice.
- The existing eight-brand release allowlist remains the formal asset boundary. Public hosting of eleven verified kits continues under the established contract; expanding GitHub release assets for three client brands is separate scope.
- No approved identity geometry or brand source needs changing for this release.
