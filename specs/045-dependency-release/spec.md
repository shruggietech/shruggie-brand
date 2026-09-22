# Feature Specification: Dependency Integration and 2.0.1 Release

**Feature Branch**: `codex/045-dependency-release`

**Created**: 2026-09-22

**Status**: In Progress

**Input**: User description: "Handle every open Dependabot pull request, complete the next work slice under autopilot, push an official pull request, satisfy CI and up to two Codex review rounds, then request final review and merge before publishing a fresh tagged release."

**Dependabot intake**: [#225](https://github.com/shruggietech/shruggie-brand/pull/225) (site runtime) and [#226](https://github.com/shruggietech/shruggie-brand/pull/226) (site tooling), the complete open Dependabot inventory at kickoff.

## User Scenarios & Testing

### User Story 1 - Receive current site dependencies (Priority: P1)

As a site visitor, I can use the public brand site after its pending runtime and tooling updates without a broken page, inaccessible control, or invalid download.

**Why this priority**: Both pending update groups must be accounted for before release.

**Independent Test**: Build and verify the site with the combined dependency set, including page, accessibility, and download gates.

**Acceptance Scenarios**:

1. **Given** the two open dependency groups, **When** they are combined, **Then** every requested direct dependency update is represented and the lockfile resolves consistently.
2. **Given** the combined dependencies, **When** the full site gates run, **Then** static export and accessibility checks pass without changing public routes or brand identity.

---

### User Story 2 - Preserve the verified release build (Priority: P1)

As a release operator, I can build and certify all production kits with the updated site tooling without losing required PDF guides or verified archives.

**Why this priority**: The tooling PR currently fails the release archive gate because two browser clients require different browser revisions.

**Independent Test**: Run the complete release-candidate build and archive checks after installing the browser required by each client.

**Acceptance Scenarios**:

1. **Given** the updated site browser client and the current kit browser client, **When** CI prepares the build, **Then** both can launch their required browser revisions.
2. **Given** all production kits, **When** release packaging runs, **Then** every required guide, archive, checksum, and metadata gate passes.

---

### User Story 3 - Publish a reviewed 2.0.1 release (Priority: P2)

As the owner, I receive one reviewable slice PR with green checks and addressed bot feedback, then can complete the final merge ritual and obtain the official 2.0.1 tagged release from the exact merged commit.

**Why this priority**: The publication workflow requires main ancestry and must not publish unmerged branch bytes.

**Independent Test**: Confirm the PR is review-complete and green; after owner merge, confirm the tag matches the merged main commit and the official release workflow publishes certified assets.

**Acceptance Scenarios**:

1. **Given** a passing combined slice PR, **When** review comments arrive, **Then** each actionable comment is answered and resolved, with no more than one additional Codex review request.
2. **Given** the owner's final merge, **When** the 2.0.1 tag is pushed on the merged commit, **Then** release preflight verifies main ancestry and publishes the certified assets.

### Edge Cases

- A Dependabot PR may be retargeted or updated after kickoff; compare current heads before finalizing the combined PR and record the precise included revisions.
- If a dependency update is incompatible, document the failure and narrow or defer only that update with an explicit reason; never mark a failing release ready.
- If one browser revision is available while the other is missing, the build must fail before claiming a verified release.
- If review bots provide only a reaction or no comments, record that observation rather than fabricating review approval.
- A tag on an unmerged branch cannot satisfy the main-ancestry release gate; publication follows the final merge.

## Requirements

### Functional Requirements

- **FR-001**: The slice MUST inventory and disposition every Dependabot PR open at kickoff, including #225 and #226.
- **FR-002**: The combined site dependency manifest and lockfile MUST contain all compatible direct updates proposed by those PRs.
- **FR-002a**: Dependencies required for compatibility with a proposed update MUST advance together when the existing pinned version cannot satisfy the new package's declared contract or build successfully.
- **FR-003**: The verified build MUST provision the distinct browser revisions required by its site and kit clients, and MUST fail when either is unavailable.
- **FR-004**: All existing production kit, glyph, site, accessibility, archive, checksum, and publication gates MUST remain enforced and pass.
- **FR-005**: The release notes MUST state the skill version, Brand/Interface Canon version, migration impact, and the dependency/CI correction.
- **FR-006**: The slice PR MUST be pushed, opened, and processed through all review comments and green CI before the owner is asked to merge.
- **FR-007**: The agent MUST request no more than one additional Codex review round beyond the automatic initial round.
- **FR-008**: The official tag MUST identify the exact merged `main` commit and MUST be published only after the owner's final review and merge.
- **FR-009**: No approved logo path, source artwork, or generated `dist/` contents may be changed or committed.
- **FR-010**: Dependency automation labels MUST reference existing repository labels so pending and future updates can be triaged consistently.

### Key Entities

- **Dependency intake**: The numbered PR, source head revision, requested direct packages, and disposition.
- **Release candidate**: The exact source revision, versioned notes, certified archives, and checksums that publication consumes.
- **Review state**: CI checks, comment threads, bot reactions, and the count of requested Codex review rounds.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All 2 Dependabot PRs open at kickoff have an explicit integration or justified disposition in one release slice, including any required companion updates.
- **SC-002**: 100 percent of required kit, site, accessibility, release-contract, and archive gates pass on the combined PR.
- **SC-003**: Every actionable review comment receives a response and resolution, with at most one extra Codex review request.
- **SC-004**: The final PR is green and review-complete before the owner is pinged for merge.
- **SC-005**: After merge, one `v2.0.1` tag points to the merged main commit and one official release has the verified asset set.

## Assumptions

- The current untagged 2.0.1 version is the next release; `v2.0.0` is the latest published v2 tag.
- The final review and merge ritual belongs to the owner; this run prepares the PR, then publication resumes after that merge.
- The two kickoff Dependabot PRs are integrated into this slice rather than merged separately to keep one combined release gate; they can be closed as superseded after the slice merges.
- No application source or approved brand identity change is necessary for the dependency update.
