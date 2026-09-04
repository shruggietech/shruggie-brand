# Feature Specification: v1.1.2 Release and Publication Certification

**Feature Branch**: `codex/004-release-publication-certification`

**Created**: 2026-09-04

**Status**: In progress

**Input**: Prepare and certify the v1.1.2 release, preserve complete version history and migration metadata, publish exactly seven licensed assets after owner merge, process at most two Codex review rounds, and close linked GitHub work only after publication evidence exists.

## User Scenarios & Testing

### User Story 1 - Trustworthy release candidate (Priority: P1)

As a release owner, I can review a release-readiness pull request whose changelog, skill metadata, canon metadata, release notes, archive manifest, and migration statement agree before I decide whether to merge it.

**Why this priority**: The tag publishes immutable artifacts. Contradictory metadata or an under-specified archive set must be found before the owner merge gate.

**Independent Test**: Generate the v1.1.2 release notes and build all release archives locally, then run one repository-owned verifier that reports the expected seven filenames, validates every archive, and rejects version or history drift.

**Acceptance Scenarios**:

1. **Given** the current release candidate, **When** the release preflight runs for version 1.1.2, **Then** the root and bundled histories preserve 1.1.0, 1.1.1, and 1.1.2 and the generated notes state skill version 1.1.2, canon version 1.1.2, and the required migration impact.
2. **Given** freshly rebuilt distribution output, **When** the packaging and archive verification run, **Then** exactly two skill bundles and five production-kit archives are present and every archive passes its type-specific content contract.
3. **Given** an archive, filename, version, license, PDF, or notes mismatch, **When** preflight runs, **Then** it exits nonzero with the failing artifact and rule identified.

---

### User Story 2 - Bounded reviewed publication (Priority: P1)

As the repository owner, I receive an open pull request that has passed continuous integration and exactly the authorized Codex review lifecycle, with every actionable finding tracked, answered, corrected when warranted, and resolved before I perform the merge ritual.

**Why this priority**: Publication readiness depends on both technical gates and complete review handling, while merge authority remains with the owner.

**Independent Test**: Inspect the pull request review ledger, review threads, issue links, comment history, head SHA, and required checks. There is one automatic round, no more than one explicit `@Codex` request, no unresolved actionable thread, and no merge or tag.

**Acceptance Scenarios**:

1. **Given** the official S004 pull request, **When** automatic Codex feedback arrives, **Then** every negative finding is filed as a linked GitHub issue before its review thread is substantively answered and resolved.
2. **Given** round 1 is complete, **When** round 2 is requested, **Then** exactly one explicit `@Codex` comment is posted and its immutable URL is recorded.
3. **Given** all permitted review feedback has been processed, **When** required checks are green, **Then** the pull request remains open and the owner is asked to perform the final review and merge ritual.

---

### User Story 3 - Evidence-backed public release (Priority: P2)

As a release consumer and project stakeholder, I can inspect v1.1.2 and see seven CI-built assets with complete licensing, matched source and archive versions, required PDFs, explicit migration guidance, and GitHub issue states backed by public evidence.

**Why this priority**: This outcome completes work-order issues #63, #72, and #73, but it can occur only after the owner merges the reviewed source change.

**Independent Test**: From the merged main SHA, publish tag v1.1.2 once, download the GitHub release into a clean temporary directory, verify its notes and all seven assets, and attach sanitized evidence to the three child issues before closing eligible parents and milestones.

**Acceptance Scenarios**:

1. **Given** the owner has merged the S004 pull request, **When** the post-merge continuation starts, **Then** current `origin/main` and the release-readiness commit are reconciled before tag v1.1.2 is created.
2. **Given** the v1.1.2 tag workflow succeeds, **When** the published release is inspected, **Then** its target is the verified main revision and exactly the seven expected assets and release notes pass the same contract used locally.
3. **Given** published evidence satisfies every criterion in issues #63, #72, and #73, **When** GitHub housekeeping runs, **Then** those children close first, parents #10 and #13 close only after all their children are closed, and milestones 15 and 18 close only when their open issue counts reach zero.

### Edge Cases

- If v1.1.2 already exists locally or remotely, publication halts unless its tag target, release target, notes, and assets exactly match the verified intended release.
- If the owner merges with a non-identical commit due to squash or another concurrent main change, the post-merge continuation re-runs validation against the actual merged main revision before tagging.
- If the release workflow fails or produces partial assets, no child release issue or parent phase is closed; the failure is corrected through a new reviewed change if source changes are required.
- If Codex supplies only a thumbs-up reaction or an explicit no-findings signal, that signal completes the round only after pending threads and review records are checked.
- Late feedback from either authorized round is processed, but it never triggers a third review request.
- Release verification uses a newly created temporary download directory so stale local archives cannot satisfy or contaminate the published-asset contract.

## Requirements

### Functional Requirements

- **FR-001**: S004 MUST preserve the complete 1.1.0 glyph, portability, chart rotation, promoted-generator, and Apache-2.0 relicensing history; the 1.1.1 accessibility-floor history; and the 1.1.2 provenance, migration, accessibility, and review-remediation history.
- **FR-002**: The release notes MUST be generated from the exact 1.1.2 changelog section and MUST explicitly state skill version 1.1.2, canon version 1.1.2, and that existing kits require migration by rebuilding.
- **FR-003**: Release preflight MUST validate agreement among the requested tag version, root changelog, skill changelog, `skill/SKILL.md` metadata, canon metadata, archive filenames, and embedded kit versions.
- **FR-004**: Packaging MUST produce exactly seven expected files: two skill distributions and one archive for each of the five production brands.
- **FR-005**: Both skill distributions and all five production-kit archives MUST contain `LICENSE`, `NOTICE`, and `LICENSE-BRAND.md` at archive root.
- **FR-006**: Every production-kit archive MUST contain `brand.json`, `brand-guide.pdf`, and a complete manifest whose recorded checksums validate after excluding only the three release-added root licensing files.
- **FR-007**: The portable skill archive MUST omit `SKILL.md`, contain `AGENTS.md`, and contain its portable `README.md`; the Claude skill distribution MUST contain `SKILL.md` and `AGENTS.md`.
- **FR-008**: The release workflow MUST run the repository-owned preflight after packaging and MUST publish the generated notes file instead of independently hardcoding release metadata.
- **FR-009**: The build workflow MUST run release-contract regression tests on Python 3.8 and MUST run release metadata preflight on the full build job.
- **FR-010**: S004 MUST include repository-local Spec Kit artifacts, a sanitized evidence ledger, and a bounded review ledger linked to GitHub issues #63, #72, and #73 and parents #10, #13, and #37.
- **FR-011**: Every negative Codex review finding on the S004 pull request MUST be filed as a GitHub issue with appropriate labels, milestone, source-comment link, reproduction or rationale, and acceptance criteria before the source thread is resolved.
- **FR-012**: Every Codex review comment MUST receive a substantive response; warranted corrections MUST be verified and pushed before the corresponding thread is resolved.
- **FR-013**: S004 MUST allow only two review rounds: the automatic publication-triggered round and exactly one explicit `@Codex` request after round 1 completes. No transition or task may trigger a third round.
- **FR-014**: S004 MUST NOT merge its own pull request. Once both review rounds are satisfied and all required checks are green, it MUST halt at the owner merge gate.
- **FR-015**: The v1.1.2 tag MUST NOT be created before the owner merges the S004 pull request and the post-merge continuation verifies the actual current main revision.
- **FR-016**: Published-release verification MUST download the release into an empty temporary directory, validate the same notes and archive contract as local preflight, and record the tag target, workflow result, release URL, asset count, and verification result without exposing sensitive local or provider identifiers.
- **FR-017**: Issues #63, #72, and #73 MUST remain open until their published or current-main acceptance criteria are met; parents #10 and #13 and milestones 15 and 18 MUST close only after set-complete child verification.
- **FR-018**: All committed text MUST use UTF-8 without BOM and LF line endings, contain no mojibake, and exclude private workstation paths, secrets, and provider resource identifiers.

### Key Entities

- **Release Metadata**: The requested tag, skill version, canon version, migration statement, release title, and generated notes derived from version-controlled history.
- **Release Asset Contract**: The exact seven expected filenames and the type-specific required contents, licenses, versions, PDFs, and manifest integrity rules.
- **Review Round**: One authorized Codex arrival signal, its actionable findings, linked GitHub issues, responses, resolution state, and immutable trigger or signal URL.
- **Publication Evidence**: The actual merged commit, tag target, workflow run, release URL, downloaded assets, verifier output, and linked issue updates.
- **Issue Closure Set**: A child-first relationship whose parent issue and milestone become eligible only after all required children have evidence-backed closed states.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Local preflight generates one release-notes document for 1.1.2 and reports exactly seven valid archives with zero contract failures.
- **SC-002**: Automated release regression tests pass on Python 3.8 and the full release preflight passes in the hosted build job.
- **SC-003**: The official S004 pull request has zero unresolved actionable Codex comments after exactly two or fewer review rounds, exactly one explicit `@Codex` request, and all required checks successful.
- **SC-004**: Before owner merge, v1.1.2 does not exist as a new tag or GitHub release created by S004 and the pull request remains open.
- **SC-005**: After owner merge, the v1.1.2 release targets the verified current main revision and contains exactly seven assets, with seven of seven passing license and content validation.
- **SC-006**: After publication evidence is attached, issues #63, #72, and #73, eligible parents #10 and #13, and milestones 15 and 18 have states consistent with their published acceptance policies.
- **SC-007**: Sanitized scans report zero BOMs, CRLF text files, mojibake markers, private paths, secrets, or provider resource identifiers in the S004 change set.

## Assumptions

- The owner will merge the reviewed S004 pull request before the already-requested post-merge continuation can publish; that merge is the only intentional human gate in the slice.
- GitHub Actions remains the sole publisher of release assets. Local artifacts are preflight evidence and never release inputs.
- Production-kit versions remain the versions declared in each built `brand.json`; skill and canon release versions are 1.1.2.
- Review correction issues use the milestone matching the affected work-order phase. Cross-cutting release findings default to milestone 15 and link S004 plus all affected parents.
- Existing generated output directories remain ignored and disposable.
