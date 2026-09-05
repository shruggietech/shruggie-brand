# Research: v1.2.0 Release and Production Certification

## Decision 1: Use version 1.2.0

**Decision**: Advance the brandbuilder and canon from 1.1.2 to 1.2.0.

**Rationale**: S006 through S009 add multiple backward-compatible capabilities: ownership-neutral third-party work, supplied marks and fixed fonts, native application icon suites, a generated portfolio, Fumadocs documentation, and route-level discovery. A patch would understate that new public capability; a major release is unnecessary because the existing source and archive contracts remain valid.

**Alternatives considered**: 1.1.3 was rejected as too small for additive public behavior. 2.0.0 was rejected because no incompatible contract is intentionally introduced.

## Decision 2: Separate candidate, publication, and deployment evidence

**Decision**: The PR closes only #117. Issues #118 and #119 remain open until the tagged release and deployed site can be independently inspected, and parent #116 closes last.

**Rationale**: Branch and pull-request evidence cannot establish a public GitHub release or a production Pages result.

**Alternatives considered**: Closing all four issues from the PR was rejected as false completion. Keeping candidate work untracked until publication was rejected because it would hide current progress.

## Decision 3: Keep production brand versions independent

**Decision**: Advance the `canon` reference in all five production sources without changing their brand `version` values.

**Rationale**: S010 changes the shared system and release, not the approved identity revision of each brand. Existing archive names continue to express the version embedded in each kit.

**Alternatives considered**: Bumping every brand to 1.2.0 was rejected because it would manufacture identity-version history. Leaving brand canon references at 1.1.2 was rejected because generated output would contradict authoritative canon.

## Decision 4: Discover the current release through validated metadata

**Decision**: Add a `current` release-contract command, make packaging default to validated current metadata, and make pull-request CI consume that command.

**Rationale**: The current workflow and packaging default both repeat 1.1.2. Repeating 1.2.0 would recreate the same drift risk immediately after this release.

**Alternatives considered**: Editing both literals to 1.2.0 was rejected as avoidable duplication. Adding a new VERSION file was rejected because it would create a third source of truth beside skill and canon metadata.

## Decision 5: Validate release dates for the requested version

**Decision**: Generalize the root and bundled changelog date comparison to the requested version while retaining explicit required-history phrase checks for historical releases.

**Rationale**: The existing validator treats 1.1.2 as permanently current. The requested release already identifies which new section must exist and agree.

**Alternatives considered**: Adding another fixed 1.2.0 date comparison was rejected because every release would require another special case.

## Decision 6: State migration as rebuild-required

**Decision**: Release notes say existing kits require migration by rebuilding with v1.2.0.

**Rationale**: Existing outputs do not contain the new ownership contract, supplied-input handling, native icon suites, current canon reference, updated site resources, or full discovery behavior.

**Alternatives considered**: Claiming no migration was rejected because old generated kits cannot acquire new assets or metadata without rebuilding. Describing an in-place manual migration was rejected because generated output must come from source automation.

## Decision 7: Keep publication in GitHub Actions

**Decision**: Local builds prove readiness, but the official seven assets are rebuilt and published only by the tag workflow.

**Rationale**: This preserves reproducibility and prevents workstation output from becoming a release input.

**Alternatives considered**: Uploading locally generated archives was rejected by the constitution and existing release contract.

## Decision 8: Preserve the two-round review ceiling

**Decision**: Process the automatic round, optionally request exactly one second round after round one completes, and never request a third review.

**Rationale**: This satisfies the explicit operator instruction and prevents the prior recursive review-loop failure mode.

**Alternatives considered**: Requesting review after every correction was rejected. Skipping all review handling was rejected because every comment must be answered and resolved.

