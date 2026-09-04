# Research: v1.1.2 Release and Publication Certification

## Decision 1: Treat publication as a two-stage slice

**Decision**: S004 contains a pre-merge readiness stage and a post-merge publication stage separated by the owner's merge ritual.

**Rationale**: The user authorized push, pull-request publication, and tag/release automation, while explicitly requiring a final owner review before merge. A tag created from the branch would violate both that gate and the work order's tagged-main requirement.

**Alternatives considered**: Tagging the branch was rejected because it would publish unmerged source. Ending S004 permanently at the pull request was rejected because issues #63 and #73 require actual published-asset evidence.

## Decision 2: Derive release notes from the root changelog

**Decision**: Generate the release body from the exact requested version section in `CHANGELOG.md`, preceded by validated skill version, canon version, and migration metadata.

**Rationale**: The current workflow hardcodes a short body and only points readers to the changelog. That can drift from tagged source and does not carry the complete history required by the work order.

**Alternatives considered**: A manually maintained release-notes file was rejected as a second source of truth. GitHub-generated notes were rejected because they do not guarantee the required skill, canon, and migration fields or the curated historical narrative.

## Decision 3: Keep per-brand archive versions

**Decision**: Production archive filenames continue to use the version from each built kit's `brand.json`, while the two skill distributions use the brandbuilder version 1.1.2.

**Rationale**: The five migrated identities have independent kit versions. Rebranding them all as 1.1.2 would falsely change kit metadata. The release contract will verify each filename against its embedded brand version and manifest version.

**Alternatives considered**: Using the release tag for every archive was rejected because it would obscure independent kit version history. Omitting versions from filenames was rejected because it weakens traceability.

## Decision 4: Validate archives with one reusable standard-library contract

**Decision**: One Python module handles metadata parsing, notes generation, exact asset enumeration, archive structure, license presence, embedded versions, required PDFs, and recorded manifest checksums.

**Rationale**: The same logic can run in Python 3.8 CI, tag publication, local preflight, and post-publication verification. It prevents shell assertions and manual inspection from drifting apart.

**Alternatives considered**: Keeping the workflow's inline ZIP license check was rejected because it covers only one acceptance dimension. Separate local and hosted verifiers were rejected because they would create inconsistent release gates.

## Decision 5: Correct manifest version provenance

**Decision**: Generated `manifest.json` uses the kit's declared `brand.json` version instead of a constant 1.0.0.

**Rationale**: Fragcap is version 1.1.0, so its current generated manifest disagrees with both the package filename and embedded brand metadata. Issue #63 explicitly requires version verification.

**Alternatives considered**: Teaching the release verifier to ignore manifest version was rejected because it would preserve a false provenance record.

## Decision 6: Reconcile the unreleased remediation history into 1.1.2

**Decision**: Move completed S003 fixed entries from the root Unreleased section into 1.1.2, align the root and bundled skill 1.1.2 dates to the actual release date, and retain an empty Unreleased heading.

**Rationale**: Leaving merged remediations under Unreleased while tagging 1.1.2 would omit them from that release's generated notes and conflict with the bundled skill history.

**Alternatives considered**: Creating 1.1.3 was rejected because the work order and open release issues explicitly designate this unpublished correction set as v1.1.2.

## Decision 7: Keep GitHub closure evidence-driven

**Decision**: Issues #63, #72, and #73 remain open through the pre-merge stage. They close only after the actual release and published archives satisfy their criteria. Parent issues and milestones close last.

**Rationale**: Branch-only proof cannot establish release existence, published notes, asset count, or archive download integrity.

**Alternatives considered**: Closing #72 on the readiness branch was rejected because its acceptance explicitly includes release-note agreement, which is not final until the tagged release is published.

## Decision 8: Keep review requests bounded

**Decision**: Record the automatic round and one explicit second-round request in a fixed two-row ledger. Never issue another `@Codex` request.

**Rationale**: The user explicitly authorized only one second round and previously required the recursive review loop to stop.

**Alternatives considered**: Requesting review after every correction push was rejected because it recreates the prohibited loop. Skipping the explicit second round was rejected because the user authorized and requested that lifecycle for this slice.
