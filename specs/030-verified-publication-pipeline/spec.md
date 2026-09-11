# Feature Specification: Verified Publication Pipeline

**Feature Branch**: `codex/030-verified-publication-pipeline`

**Created**: 2026-09-11

**Status**: Ready for Owner Review

**Issue**: [#196](https://github.com/shruggietech/shruggie-brand/issues/196)

**Input**: User description: "Repair the failed Pages deployment by establishing one authoritative verified-build path for pull requests, main-branch publication, and tagged releases. Preserve the approved identity continuity gate, validate publication before merge, publish the exact verified static output, and prevent the release workflow from retaining the same renderer drift defect."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Publish a verified main revision (Priority: P1)

As the repository owner, I can merge an approved revision to the default branch and have the exact site output that passed the repository's mandatory verification gates published to the production Pages environment.

**Why this priority**: The public site is currently one revision behind because the publication path rebuilt with a different proof environment and correctly failed closed.

**Independent Test**: Merge a revision whose verified build succeeds, then confirm that the production deployment reports the same revision, contains all eight production brands, and exposes the I Heart PR Tours site surfaces and downloads.

**Acceptance Scenarios**:

1. **Given** a default-branch revision whose production kits and site pass every mandatory gate, **When** publication runs, **Then** the verified static output from that revision is deployed without a second divergent rebuild.
2. **Given** a revision with renderer, proof, source, verification, accessibility, or site-contract drift, **When** the publication pipeline runs, **Then** no new production deployment is created and the last known-good site remains available.
3. **Given** multiple default-branch revisions arrive close together, **When** publication runs overlap, **Then** only the newest eligible revision can become the production deployment.

---

### User Story 2 - Detect publication defects before merge (Priority: P2)

As a contributor or reviewer, I can see whether a pull request can produce a publishable static site through the same verification boundary used by production before I approve or merge it.

**Why this priority**: The S028 pull request passed its regular checks because the distinct Pages-only build path was exercised only after merge.

**Independent Test**: Open a pull request that changes a publication dependency and confirm that the required checks exercise the complete verified site-output path while creating no public deployment.

**Acceptance Scenarios**:

1. **Given** a pull request, **When** required checks run, **Then** they produce and validate the same publication artifact that a successful default-branch run would deploy.
2. **Given** a pull request with a publication-only incompatibility, **When** required checks run, **Then** the pull request fails before merge with the responsible gate identified.
3. **Given** any pull-request event, **When** its checks succeed, **Then** no Pages deployment or release is published.

---

### User Story 3 - Build releases through the same boundary (Priority: P3)

As a release operator, I can tag an approved revision and know that its release assets are rebuilt under the same deterministic identity-proof and verification contract used by continuous integration and site publication.

**Why this priority**: The release path retains the obsolete renderer setup that caused the Pages failure and would reject the next tag.

**Independent Test**: Run release certification for a candidate revision through the shared verified path, confirm that all expected release assets are produced, and confirm that publication remains gated on an authorized version tag.

**Acceptance Scenarios**:

1. **Given** an authorized version tag on a verified revision, **When** release publication runs, **Then** the release assets are derived from that same revision and mandatory verification boundary.
2. **Given** a release candidate with identity-proof or packaging drift, **When** release verification runs, **Then** no release is published.
3. **Given** an ordinary branch or default-branch push, **When** verification succeeds, **Then** no GitHub release is created.

### Edge Cases

- A canonical identity approval was created on a different operating system from the publication worker.
- The current worker offers another renderer earlier in its executable search order.
- A floating runtime version changes after approval while repository sources remain unchanged.
- Approved proof evidence is missing, incomplete, stale, unsafe, or associated with another revision.
- Verification succeeds but publication-artifact upload or deployment fails.
- The newest default-branch run cancels an older in-progress publication.
- A tag points to a revision that has not completed the shared verification boundary.
- A pull request originates from an untrusted fork and must not receive publication permissions.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The repository MUST define one authoritative verification boundary for production kits, static-site output, Pages publication inputs, and release inputs.
- **FR-002**: Pull requests, default-branch publication, and tagged releases MUST use that authoritative boundary rather than independently restating its build environment.
- **FR-003**: The authoritative boundary MUST preserve the approved identity renderer, runtime version, proof evidence, and fail-closed comparison behavior.
- **FR-004**: The pipeline MUST reject missing, stale, altered, cross-revision, or unsafe approved proof evidence before generating publishable output.
- **FR-005**: A Pages deployment MUST consume the exact static-site artifact produced by the successful authoritative verification run for the same revision.
- **FR-006**: Pages deployment MUST NOT rebuild production kits or the static site in a separate environment after verification.
- **FR-007**: Pull-request checks MUST exercise creation and validation of the complete Pages-ready artifact without publishing it.
- **FR-008**: Pages publication MUST occur only for a successful eligible default-branch revision.
- **FR-009**: Release publication MUST occur only for an authorized version tag whose release assets passed the authoritative verification boundary.
- **FR-010**: A failed verification, artifact transfer, packaging, or publication step MUST prevent the affected deployment or release while preserving the last known-good publication.
- **FR-011**: Publication permissions MUST be limited to the jobs that perform the corresponding external publication action.
- **FR-012**: Concurrent Pages runs MUST prevent an older eligible revision from replacing a newer eligible revision.
- **FR-013**: The pipeline MUST retain all constitutionally required kit, glyph, accessibility, site-origin, payload, release, and repository-hygiene checks.
- **FR-014**: The repair MUST NOT change identity artwork, approved proof hashes, approval records, renderer tolerances, or logo geometry.
- **FR-015**: Maintainer-facing evidence MUST identify the verified revision, artifact lineage, gate results, and final publication outcome.
- **FR-016**: Repository regression coverage MUST fail when a publication or release entry point bypasses the authoritative verification boundary or reintroduces a conflicting renderer/runtime definition.

### Key Entities

- **Verified revision**: The immutable source revision that completed the authoritative verification boundary.
- **Approved proof bundle**: Ephemeral, hash-validated canonical identity evidence associated with the verified revision.
- **Verified publication artifact**: The complete static-site output produced and validated for one verified revision.
- **Verified release artifact set**: The release archives, metadata, and notes produced and certified for one verified revision.
- **Publication outcome**: The recorded success or failure connecting a verified revision and artifact to Pages or a tagged release.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every pull request exercises 100 percent of the verification and artifact-generation gates required before a production Pages deployment, while producing zero deployments.
- **SC-002**: A successful default-branch run creates exactly one Pages deployment whose recorded revision equals the verified source revision.
- **SC-003**: All eight production kits report zero verifier problems and zero glyph failures before any Pages or release publication is eligible.
- **SC-004**: The published site exposes all eight production brands, all governed I Heart PR Tours routes and downloads, and zero accessibility violations across the documented browser verification set.
- **SC-005**: Injecting any renderer, runtime, proof hash, artifact lineage, or publication-contract mismatch causes the responsible pre-publication check to fail in 100 percent of covered regression cases.
- **SC-006**: No Pages or release entry point contains an independent conflicting definition of the approved identity proof environment.
- **SC-007**: The next authorized version-tag build completes release certification without renderer or proof-environment drift.
- **SC-008**: The repair changes zero approved identity source bytes, proof hashes, approval records, or logo geometry values.

## Assumptions

- GitHub Actions and GitHub Pages remain the repository's hosted verification and publication services.
- The existing Windows-approved proof bundle and cross-platform comparison model remain authoritative.
- The currently pinned approved renderer and runtime versions remain unchanged by this repair.
- The current production site remains the last known-good fallback until a repaired default-branch run succeeds.
- Creating a new release tag is outside this slice; release packaging and orchestration are verified without publishing an unrequested release.
- Third-party review processing and the final owner merge ritual follow the operator's explicit S030 instructions.
- The active default-branch ruleset continues to require the exact hosted check context `build`.

## Scope

### In scope

- Shared verification and artifact lineage across pull requests, Pages publication, and release preparation.
- Pre-merge coverage of the Pages-ready artifact.
- Repair of the latent release renderer/proof mismatch.
- Hosted CI, Pages, and review evidence for the official S030 pull request.

### Out of scope

- Identity reapproval, proof regeneration as committed source, renderer-tolerance changes, or logo modifications.
- A new brandbuilder release, version change, release tag, or production release publication.
- Unrelated site presentation, content, navigation, or brand-system changes.

## Done When

- The official S030 pull request has green required checks and no unresolved review threads after no more than two review rounds.
- Pull requests validate the Pages-ready artifact without deploying it.
- Default-branch publication and tagged-release preparation cannot bypass the authoritative verification boundary.
- The owner receives a final-review handoff before merge.
