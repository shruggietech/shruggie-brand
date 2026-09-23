# Feature Specification: Repository Front Door and v2.0.3 Release Readiness

**Feature Branch**: `codex/049-repository-front-door`

**Created**: 2026-09-23

**Status**: Implemented, pending PR review and CI

**Input**: S049 approval to repair and brand the root README, prevent dead links and stale download guidance, and prepare the merged 2.0.3 source for an exact-revision formal release. Issue [#259](https://github.com/shruggietech/shruggie-brand/issues/259).

## User Scenarios & Testing

### User Story 1 - Find the right brand and download (Priority: P1)

As a repository visitor, I can recognize the ShruggieTech source, open any of the eight brand guidelines, and find the current BrandBuilder distribution without following a dead or obsolete destination.

**Why this priority**: The current root README is the primary repository entry point and its eight brand paths do not match the published route contract.

**Independent Test**: Inspect the rendered README in light and dark GitHub themes and follow every brand, distribution, and documentation destination.

**Acceptance Scenarios**:

1. **Given** the repository front page, **when** a visitor opens any listed brand, **then** the destination is that brand's canonical guideline page.
2. **Given** a visitor choosing a Claude or portable distribution, **when** they use the README, **then** they reach the current official release and can identify the appropriate asset without a stale fixed-version filename.
3. **Given** light or dark GitHub presentation, **when** the README is displayed, **then** an existing approved ShruggieTech lockup is legible without changing identity geometry.

---

### User Story 2 - Trust front-page status and links (Priority: P2)

As a contributor, I can see the build, release, and license status and trust that repository-local and brand-route links are checked when the README changes.

**Why this priority**: Badges are absent and manual link maintenance has already missed invalid routes and stale asset names.

**Independent Test**: Inspect each badge and destination, then introduce broken local, unsafe, and brand-route links in isolated tests and observe a failing check.

**Acceptance Scenarios**:

1. **Given** the README, **when** a contributor reads its badges, **then** Build, latest official release, and code-license badges have descriptive text and meaningful destinations.
2. **Given** a local link or a brand-site route in the README that does not exist, **when** the repository check runs, **then** it fails with the offending target.
3. **Given** a URL that looks like a brand route but points outside the trusted site, **when** the check runs, **then** it is not accepted as a valid brand destination.

---

### User Story 3 - Publish a traceable v2.0.3 release (Priority: P3)

As the maintainer, I can review the release candidate against the README and release contract, merge a green PR, then publish v2.0.3 from exactly the merged revision with verified assets and checksums.

**Why this priority**: Source declares 2.0.3 while v2.0.1 is the latest formal release. A README-only fix must not imply candidate bytes are already published.

**Independent Test**: Run the complete documented validation and release-candidate certification, inspect release notes and asset manifest, and ensure publication is gated on the merged exact tag.

**Acceptance Scenarios**:

1. **Given** the open PR, **when** visitors read the README, **then** its download guidance does not claim an unpublished version is downloadable.
2. **Given** the merged and validated main revision, **when** v2.0.3 is tagged, **then** the release pipeline builds assets from that revision and verifies its declared files and checksums.
3. **Given** an incomplete or mismatched release candidate, **when** certification runs, **then** publication is blocked rather than presented as successful.

### Edge Cases

- The newest source version may be ahead of the latest published release. Public download guidance must not conflate them.
- A relative link may contain a fragment or percent encoding; only a safe, existing repository target may pass.
- Brand slugs and site routes can change. The README check must compare with the declared route contract rather than a duplicated hand-maintained slug list.
- A badge image can fail remotely without making the README unreadable; meaningful link text must remain available.
- External URLs are subject to network and provider availability; CI must not depend on live external HTTP requests.

## Requirements

### Functional Requirements

- **FR-001**: The root README MUST use existing approved ShruggieTech artwork in a presentation that remains legible in light and dark GitHub themes, with useful alternative text and unchanged source geometry.
- **FR-002**: The root README MUST provide Build, latest-release, and code-license badges with meaningful destinations and accessible labels.
- **FR-003**: The root README MUST direct users to all eight canonical brand guideline pages, the official current-release landing page, build/contribution guidance, and the correct code-versus-brand licensing boundaries.
- **FR-004**: The root README MUST explain Claude skill and portable Codex/repository distributions without hard-coded obsolete asset filenames or claims that an unpublished candidate is available.
- **FR-005**: A deterministic repository check MUST reject missing local README targets, unsafe local paths, noncanonical brand paths, and missing declared brand links without requiring live HTTP.
- **FR-006**: The check MUST derive valid brand routes from the site publication contract and MUST have positive and negative regression cases, including path traversal and lookalike hosts.
- **FR-007**: The slice MUST certify the 2.0.3 source candidate through the documented full build, release contract, site, accessibility, identity, security/isolation, and hygiene gates before PR handoff.
- **FR-008**: Formal v2.0.3 tagging and publication MUST occur only after owner merge from the exact validated main revision; the release pipeline MUST verify the expected assets and checksums.
- **FR-009**: Work MUST remain in this repository; consumer repinning, downstream runtime verification, light-theme generator changes (#193), and custom imagery changes (#194) are out of scope.

### Key Entities

- **README destination**: A repository-relative file, an official release destination, a badge destination, or a canonical brand-site route.
- **Brand route**: A slug-specific guideline destination declared by the site publication contract.
- **Release candidate**: Source-version metadata, declared assets, release notes, checksums, and exact source revision before formal tag publication.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All eight README brand links resolve to declared canonical guideline routes, with zero invalid local links.
- **SC-002**: The README has one legible approved lockup for each GitHub theme and three labeled status badges with valid destinations.
- **SC-003**: At least four isolated negative link fixtures fail for missing local files, traversal, invalid brand routes, and lookalike hosts, while valid links pass.
- **SC-004**: Before handoff, every documented production and release-candidate validation gate passes; after owner merge and tag, the release contains every contract-declared asset and a valid checksum manifest.

## Assumptions

- The current approved ShruggieTech light/dark logo assets can be reused without alteration.
- The official latest-release page is the stable public download entry point, while exact-version pinning is described in release assets.
- Existing repository metadata already provides a homepage and topics, so this slice does not expand into GitHub repository settings.
- The owner controls final PR merge. The formal release is a post-merge action and is not claimed complete at PR handoff.
