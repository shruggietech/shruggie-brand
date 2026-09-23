# Feature Specification: Post-Merge Dependabot Refresh

**Feature Branch**: `codex/046-dependabot-refresh`

**Created**: 2026-09-22

**Status**: In Progress

**Input**: The owner merged S045, then reported that Dependabot PRs remained open. Complete the pending dependency-release work before the official 2.0.1 tag.

**Issue**: [#250](https://github.com/shruggietech/shruggie-brand/issues/250)

**Intake**: [#242](https://github.com/shruggietech/shruggie-brand/pull/242) through [#249](https://github.com/shruggietech/shruggie-brand/pull/249), all eight Dependabot PRs opened after the S045 merge. The two S045 intake PRs, #225 and #226, are already closed.

## User Scenarios & Testing

### User Story 1 - Receive coordinated maintenance updates (Priority: P1)

As a maintainer, I can review one candidate containing all compatible post-merge dependency updates, without eight independently failing bot PRs.

**Why this priority**: The bot PRs are open and workflow-action PRs fail the immutable-source policy when submitted alone.

**Independent Test**: Compare all eight requested versions to the combined candidate, then run the existing pinned-source and compatibility gates.

**Acceptance Scenarios**:

1. **Given** the eight open bot PRs, **When** the candidate is assembled, **Then** every requested dependency has an included update or a documented incompatibility disposition.
2. **Given** a workflow-action update, **When** the source contract runs, **Then** the pinned revision and version label agree with the reviewed upstream release.

---

### User Story 2 - Preserve shippable kits and site (Priority: P1)

As a release operator, I can build the eight production kits and public site with the combined updates while retaining accessibility, immutable identity, archive, and checksum gates.

**Why this priority**: A green single-dependency PR cannot prove the combined release candidate is safe.

**Independent Test**: Run the full documented validation and the official candidate PR checks.

**Acceptance Scenarios**:

1. **Given** the combined dependency candidate, **When** the full validation runs, **Then** all required kit, glyph, site, accessibility, archive, and publication checks pass.
2. **Given** a failing update, **When** it is isolated, **Then** the candidate is corrected or that update is explicitly deferred rather than weakening a gate.

---

### User Story 3 - Finish the pending release (Priority: P2)

As the owner, I receive one green, review-complete follow-up PR for final review and merge; afterward the official 2.0.1 tag is cut from its exact merged main commit.

**Why this priority**: The existing publisher accepts only a tagged main-ancestor revision with verified assets.

**Independent Test**: Confirm the PR checks and reviews before merge, then the tag, release, assets, and Pages deployment after merge.

**Acceptance Scenarios**:

1. **Given** the candidate PR, **When** reviews arrive, **Then** each actionable comment is answered and closed; no more than one additional Codex round is requested.
2. **Given** the owner's merge, **When** the 2.0.1 tag is pushed, **Then** it identifies the exact merged main commit and the official release succeeds.

### Edge Cases

- New Dependabot PRs may appear after this intake. Record the cutoff and assess any new PR before tagging, without silently expanding the tested candidate.
- Upstream action tags may be annotated; compare the peeled commit, not the tag object, with the workflow pin.
- Python 3.8-only versions remain pinned separately where newer packages do not support that runtime.
- An unmerged candidate or failed gate must not receive the release tag.

## Requirements

### Functional Requirements

- **FR-001**: The slice MUST inventory and disposition all eight Dependabot PRs open at this intake (#242-#249).
- **FR-002**: The candidate MUST include every compatible requested direct dependency update and retain Python 3.8-compatible pins.
- **FR-003**: Workflow action revisions MUST be immutable, verified against the intended upstream release, and paired with accurate version comments and regression expectations.
- **FR-004**: All existing security, provenance, kit, glyph, site, WCAG 2.1 AA, archive, checksum, and publication gates MUST remain enforced.
- **FR-005**: The follow-up PR MUST document issue traceability, verification, accessibility, identity, release impact, and every bot-PR disposition.
- **FR-006**: All actionable review comments MUST be answered and resolved; at most one extra Codex review round may be requested.
- **FR-007**: The owner MUST retain the final PR review and merge step. Only its exact merged main commit may be tagged `v2.0.1`.
- **FR-008**: Release notes MUST retain skill and canon versions, migration impact, and a complete account of S045/S046 dependency changes.
- **FR-009**: No logo path, brand source, generated kit, or `dist/` content may be changed or committed.

### Key Entities

- **Dependency intake**: Bot PR number, proposed version, reviewed source revision, and disposition.
- **Candidate**: A single commit set that combines source pins, runtime dependencies, tests, and release evidence.
- **Release**: Exact merged commit, tag, CI-generated assets, checksum manifest, and deployment state.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All eight intake PRs have a recorded disposition; zero redundant bot PRs remain open after the follow-up merges.
- **SC-002**: Every required candidate check passes with zero gate waivers and zero failing production kits.
- **SC-003**: Every actionable review comment is resolved with no more than one extra Codex review request.
- **SC-004**: One official `v2.0.1` release and its verified assets originate from the exact merged main revision.

## Assumptions

- The S045 `v2.0.1` notes and version metadata remain valid and the tag has not yet been published.
- The user wants the newly opened bot PRs handled before release, not merely acknowledged.
- The owner, not this agent, performs the final candidate PR merge ritual.
