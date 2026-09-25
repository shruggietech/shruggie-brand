# Feature Specification: Evergreen, Release-Bound Documentation

- **Feature Branch**: `codex/054-evergreen-release-bound-docs`
- **Created**: 2026-09-25
- **Status**: Approved for implementation
- **Input**: S054 delivers issues #264, #265, and #276 as one documentation-publication slice. The main manual and repository README retain distinct audiences and acceptance checks.

## User Scenarios & Testing

### User Story 1 - Read current system guidance (Priority: P1)

As a reader of the official main manual, I find task-relevant instructions on every page without obsolete portfolio counts, development anecdotes, work-slice identifiers, or unsupported claims.

**Independent Test**: Review the complete catalog, landing page, navigation, source references, prepared pages, exported pages, and search-visible descriptions against a page disposition; inject representative stale claims into isolated fixtures and confirm the publication audit rejects them.

**Acceptance Scenarios**:

1. **Given** any main-manual route, **when** a reader opens it, **then** its content describes current behavior and contains no claim of the number of brands or kits.
2. **Given** a digit or word portfolio count, a work-slice identifier, or known stale prose in publication-bound guidance, **when** the audit runs, **then** the build fails without rejecting legitimate technical quantities.
3. **Given** a contract rule cited in prose, **when** it is compared with current code or canon, **then** a discrepancy is corrected or recorded as a separate issue.

### User Story 2 - Identify the exact manual release (Priority: P1)

As a consumer of the main manual, I can see which formal BrandBuilder release its content describes, follow exact skill and release links, and inspect a machine-readable publication record that binds the manual to packaged references and the source revision.

**Independent Test**: Build a candidate and a tagged release fixture. Compare all page sources and prepared pages against the publication record and packaged skill references. Mutate version, revision, page content, inventory, and download destination independently; each mismatch fails preflight.

**Acceptance Scenarios**:

1. **Given** a tagged release, **when** its manual is exported, **then** every manual page and overview visibly names the exact BrandBuilder version and links to that tag and skill asset.
2. **Given** a main-branch preview, **when** its manual is viewed, **then** it is explicitly marked as a candidate until formal publication.
3. **Given** a manual or skill-reference mismatch, **when** release preflight runs, **then** publication stops before Pages deployment.
4. **Given** an independently versioned brand guide or technical contract, **when** the main manual version changes, **then** its independent version stays unchanged.

### User Story 3 - Enter through an evergreen README (Priority: P2)

As a newcomer, I can understand the project, get the current release, browse live brand documentation, and find contribution, security, conduct, and issue-reporting paths without relying on a hand-maintained portfolio inventory.

**Independent Test**: Run the README audit against the revised front door and isolated mutations for counts, catalog links, brand-specific commands, unsafe links, missing local targets, and inaccessible images.

**Acceptance Scenarios**:

1. **Given** the README, **when** a newcomer reads it, **then** it contains no fixed portfolio count, named subordinate-brand catalog, brand-specific command, or literal current version outside the dynamic badge.
2. **Given** a new brand is added to the site, **when** README link checks run, **then** no new README brand link is required.
3. **Given** a bad local path, untrusted site URL, unsafe scheme, or image with missing alternative text, **when** the audit runs, **then** it still fails.

### Edge Cases

- Technical counts such as operating modes, scale steps, and contrast ratios remain valid when they describe a contract rather than portfolio size.
- A timeless brand example remains valid in the manual only when clearly presented as an example; the README uses semantic placeholders.
- A release candidate must not describe its tag or asset as already published.
- The publication record must reject path traversal, duplicate/missing pages, stale prepared bytes, and a source revision that differs from the release revision.
- The main manual's version must not overwrite brand, canon, schema, adapter, or recipe versions.

## Requirements

### Functional Requirements

- **FR-001**: S054 MUST audit and disposition every cataloged main-manual page, its landing page, navigation and search-visible descriptions, and authoritative source. Individual brand guideline pages are outside this content audit.
- **FR-002**: The main manual MUST contain no portfolio-size statements, historical development narration presented as current guidance, unsupported promotional claims, or internal work-slice identifiers. Exceptions for technical quantities and necessary Spec Kit instructions MUST be narrow and reviewed.
- **FR-003**: Automated publication checks MUST inspect source, prepared MDX, exported HTML, and search-visible text, with isolated mutation tests for digit/word counts, slice identifiers, and stale phrases.
- **FR-004**: Every manual page and overview MUST show one release-authoritative BrandBuilder documentation version, exact release and skill links, and candidate status when the build is not a formal release.
- **FR-005**: A machine-readable documentation publication record MUST bind the complete catalog, authoritative reference hashes, prepared page hashes, version, status, exact tag and asset URLs, and source revision. Release preflight MUST compare it with packaged skill references and the tagged build before deployment.
- **FR-006**: Preflight MUST fail mismatched version, revision, inventory, page bytes, missing record, unqualified latest download, and production status for an unpublished candidate. Documentation-only changes MUST use the formal release/version path.
- **FR-007**: The README MUST link live site and latest-release inventory, retain its dynamic release badge and useful project orientation, and link existing contribution, security, conduct, license, and issue-reporting destinations without duplicating portfolio state.
- **FR-008**: The README audit MUST stop requiring one link per brand and MUST reject reintroduced portfolio counts or hand-maintained brand catalogs while preserving local-link, traversal, trusted-host, release-link, and accessible-image checks.
- **FR-009**: S054 MUST preserve independent brand and technical-contract versions, logo geometry, accessibility gates, UTF-8 without BOM, LF, and the source/artifact boundary. It MUST run full documented validation and record which production checks remain pending until the subsequent formal release.

### Key Entities

- **Manual catalog**: The authoritative set of source references and public routes.
- **Documentation publication record**: The exact version, status, revision, destination, and content inventory for one manual build.
- **README front door**: Stable project orientation and links, separate from the manual and live portfolio inventory.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All 15 cataloged main-manual routes and the overview receive page-by-page dispositions; zero portfolio-size claims remain in their source and exported text.
- **SC-002**: Every exported manual page displays the same exact version and candidate/release state; the publication record accounts for every cataloged reference and generated page.
- **SC-003**: At least one independent mutation for each version, revision, source byte, prepared byte, inventory, link, count, and slice-code mismatch fails before publication.
- **SC-004**: The README contains zero subordinate-brand inventory entries and retains working project, release, policy, and help links.
- **SC-005**: Full documented local gates and required PR CI pass; post-release live-route evidence is recorded only after a formally published release.

## Assumptions

- S053's `2.2.0` remains an unpublished candidate at kickoff. S054 can complete PR validation at that candidate version; formal production evidence follows an authorized tagged release after merge.
- Existing bundle publication facts and the version in `release-impact.json` remain the version authority; the documentation record adds content binding rather than a new editable version.
- The README and main manual share publication gates but have separate content ownership and tests.

## Clarifications

- **2026-09-25**: Candidate builds display a candidate label and exact prospective tag/asset destinations. Only the tagged build may display formal release status. This follows the existing publication record states and avoids claiming an unpublished release.
- **2026-09-25**: The manual and README remain separate reader surfaces. Sharing one slice does not move manual text into the README or impose the README's no-brand-example rule on instructional manual examples.
