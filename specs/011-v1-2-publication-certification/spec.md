# Feature Specification: v1.2.0 Publication and Production Certification

**Feature Branch**: `codex/011-v1-2-publication-certification`

**Created**: 2026-09-05

**Status**: Ready for Review

**Input**: Publish v1.2.0 from the owner-merged S010 revision, independently verify every public release asset and the production brand site, publish durable evidence in an official pull request, process no more than two Codex review rounds, and stop for the owner merge ritual.

## User Scenarios & Testing

### User Story 1 - Verified public release (Priority: P1)

As a release consumer, I can download v1.2.0 from a public GitHub release whose tag targets verified merged main and whose seven CI-built assets pass the repository release contract.

**Why this priority**: The release is immutable after publication, so provenance and asset integrity must be established before production certification.

**Independent Test**: Resolve the annotated tag, release workflow, release target, release state, notes, and exact asset inventory, then download all assets into a fresh ignored directory and run the shared verifier with zero failures.

**Acceptance Scenarios**:

1. **Given** merged main at `39b65b5daf9ea74c317132d26347566a9e4959d5`, **When** publication begins, **Then** the complete candidate gate passes against that exact revision before tagging.
2. **Given** no conflicting v1.2.0 tag or release, **When** the annotated tag is pushed, **Then** GitHub Actions builds and publishes a public, non-draft, non-prerelease release from the tag.
3. **Given** an empty public-download directory, **When** all release assets are downloaded, **Then** exactly two skill distributions and five production-kit archives pass the v1.2.0 release contract.

---

### User Story 2 - Qualified production deployment (Priority: P1)

As a site visitor or internal brand operator, I can use `brand.shruggie.tech` and obtain working routes, downloads, registries, metadata, discovery files, icons, and accessible responsive pages in both themes.

**Why this priority**: A green source build and a successful deployment job do not independently prove that the public domain serves the intended behavior.

**Independent Test**: Run the repository site verifier against the HTTPS production origin, compare it with the generated route contract, inspect representative downloads and registries, and review desktop and mobile screenshots in light and dark themes.

**Acceptance Scenarios**:

1. **Given** the merged-main Pages workflow, **When** its result is inspected, **Then** it succeeded for the exact S010 merge revision.
2. **Given** the production origin, **When** the complete route and resource contract runs, **Then** every required route and resource succeeds with expected metadata, content type, and a non-empty valid payload.
3. **Given** representative portfolio and documentation pages, **When** checked at 360 and 1280 CSS pixels in light and dark themes, **Then** they have zero WCAG 2.1 AA violations, no horizontal overflow, and no material visual regression.

---

### User Story 3 - Reviewable closure evidence (Priority: P2)

As the repository owner, I receive one open S011 pull request containing sanitized, reproducible evidence and accurate automatic closure links for the Phase 12 issue hierarchy.

**Why this priority**: Durable evidence should be reviewed before #116, #118, #119, #129, and milestone 22 are considered complete.

**Independent Test**: Inspect the committed specification, task ledger, evidence, pull-request checks, review ledger, and GitHub issue states. Generated artifacts are absent, every review comment is dispositioned, no more than one explicit `@Codex review` request exists, and the pull request remains open.

**Acceptance Scenarios**:

1. **Given** successful release and production certification, **When** evidence is committed, **Then** it contains immutable public URLs, revision identifiers, summarized command results, and no local paths, secrets, archives, screenshots, or generated site output.
2. **Given** the official pull request, **When** Codex feedback arrives, **Then** every comment receives a substantive response and every warranted change is verified before its thread is resolved.
3. **Given** the authorized review limit, **When** round one completes, **Then** no more than one explicit second-round request is posted and no third round is triggered.
4. **Given** all checks and reviews are satisfied, **When** handoff occurs, **Then** the pull request remains open for the owner merge ritual and its closure keywords close only evidence-complete issues on merge.

### Edge Cases

- If v1.2.0 already exists, publication halts unless its annotated tag target, public release target, notes, workflow provenance, and exact assets all match the intended revision.
- A failed release or production check keeps the corresponding issue open and requires a reviewed correction when source changes are needed.
- A delayed deployment is recorded as pending rather than misclassified as failure.
- Public verification cannot reuse candidate archives; downloads must land in a newly created ignored directory.
- Existing Phase 13 issues remain valid follow-up work and do not invalidate this release unless they contradict an explicit v1.2.0 contract gate.
- Corrections after the second Codex round do not authorize a third review request. Late feedback from either authorized round is still answered and resolved.

## Requirements

### Functional Requirements

- **FR-001**: S011 MUST maintain complete Spec Kit artifacts under `specs/011-v1-2-publication-certification/` and public tracking in issue #129.
- **FR-002**: Publication MUST use the owner-merged `origin/main` revision `39b65b5daf9ea74c317132d26347566a9e4959d5`, after synchronizing and re-running the complete candidate gate.
- **FR-003**: The v1.2.0 tag MUST be annotated, target the verified main revision, and be pushed only when no conflicting local tag, remote tag, or GitHub release exists.
- **FR-004**: GitHub Actions MUST be the sole builder and publisher of official release assets.
- **FR-005**: The public release MUST be non-draft, non-prerelease, target v1.2.0, and expose generated release notes that match the repository contract.
- **FR-006**: Fresh public verification MUST find exactly seven expected assets and pass all metadata, licensing, version, archive-safety, PDF, manifest, byte-count, and checksum rules.
- **FR-007**: Production certification MUST tie the successful Pages workflow to the merged main revision and verify the public HTTPS origin.
- **FR-008**: The repository site verifier MUST support an explicitly supplied HTTPS production origin without starting a local server or weakening any existing route, resource, metadata, responsive, theme, or WCAG check.
- **FR-009**: Production verification MUST reject non-HTTPS remote origins and origins other than `brand.shruggie.tech`.
- **FR-010**: Production evidence MUST cover all generated public routes, the sitemap and robots policy, route-specific metadata, social assets, skill and brand downloads, representative registries, native icons, mobile and desktop layouts, both themes, and WCAG 2.1 AA.
- **FR-011**: Generated archives, kits, release notes, site exports, screenshots, local absolute paths, secrets, provider identifiers, and machine-local feature state MUST NOT be committed.
- **FR-012**: The S011 pull request MUST link `Closes #116`, `Closes #118`, `Closes #119`, and `Closes #129` only after their acceptance evidence exists.
- **FR-013**: Every Codex review comment MUST receive a substantive response and every warranted correction MUST be implemented, tested, pushed, and resolved.
- **FR-014**: Every negative Codex finding MUST be filed as a linked GitHub issue before its thread is resolved.
- **FR-015**: Review activity MUST be limited to the automatic round and at most one explicit `@Codex review` request.
- **FR-016**: S011 MUST NOT merge its own pull request or close milestone 22 before owner merge.

### Key Entities

- **Publication Record**: Verified main revision, annotated tag object, workflow run, release URL, release state, notes comparison, and exact public asset inventory.
- **Public Asset Set**: Seven freshly downloaded CI-built files and their shared contract result.
- **Production Record**: Pages run, source revision, production origin, route and resource summary, accessibility result, theme matrix, and visual inspection result.
- **Review Round**: One authorized Codex arrival signal, findings, issue links, responses, corrections, resolutions, and immutable trigger or signal URL.
- **Closure Set**: Issues #116, #118, #119, and #129 plus milestone 22, whose final state depends on reviewed evidence.

## Success Criteria

### Measurable Outcomes

- **SC-001**: v1.2.0 resolves to the exact verified main revision and its Release workflow completes successfully.
- **SC-002**: The public release is non-draft and non-prerelease, has exactly seven expected assets, and seven of seven pass the release verifier.
- **SC-003**: The production verifier reports every expected HTML route checked at 360 and 1280 pixels with zero WCAG 2.1 AA violations and zero contract failures.
- **SC-004**: Manual inspection of the eight production route, theme, and viewport screenshots finds zero material regressions.
- **SC-005**: CI, repository hygiene, encoding, generated-artifact, and sensitive-data checks pass on the S011 change.
- **SC-006**: The pull request has zero unresolved actionable review comments after no more than two review rounds and remains open for the owner merge ritual.

## Assumptions

- S010 pull request #127 was owner-merged and its merged tree is the approved v1.2.0 release candidate.
- Successful Build and Pages runs for merged main are available as corroborating evidence, but public release and production checks are repeated independently in S011.
- Phase 13 issues #120 through #126 describe future improvements and remain outside S011 unless a current certification gate fails.
