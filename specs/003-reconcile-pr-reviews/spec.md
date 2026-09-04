# Feature Specification: Review Reconciliation and Foundation Certification

**Feature Branch**: `codex/003-reconcile-pr-reviews`

**Created**: 2026-09-03

**Status**: Draft

**Input**: Reconcile every unresolved review finding inherited from merged pull requests #16 and #26, certify the largest defensible set of work-order issues against current `main`, publish the work as an official pull request, process one automatic Codex review round and no more than one explicitly requested second round, then halt for the owner's final review and merge ritual.

## User Scenarios & Testing

### User Story 1 - Reconcile Every Inherited Review Finding (Priority: P1)

As the repository owner, I need every negative Codex review finding from pull requests #16 and #26 traced to a GitHub issue, verified against current `main`, corrected where still reproducible, answered substantively at its source, and resolved only after evidence exists.

**Why this priority**: Unanswered review findings obscure product risk and make the repository's visible status unreliable.

**Independent Test**: Inspect the 19 source review threads and issues #17 through #25 and #27 through #36. Each issue has current evidence, each thread has a substantive reply that identifies the disposition, every required correction is covered by a regression test, and every resolved thread meets its linked issue acceptance criteria.

**Acceptance Scenarios**:

1. **Given** a finding still reproduces on current `main`, **When** S003 handles it, **Then** a failing regression is captured before the correction, the smallest proportional correction is implemented, local verification passes, and the source thread receives a reply linking the correction and verification.
2. **Given** a finding no longer reproduces on current `main`, **When** S003 handles it, **Then** the source thread receives a reply with current-main evidence and the linked issue records why no new code change was required.
3. **Given** a source thread is marked outdated, **When** its disposition is evaluated, **Then** outdated status alone is not treated as resolution and the same evidence gate applies.

---

### User Story 2 - Certify Completed Work-Order Scope (Priority: P1)

As the repository owner, I need GitHub Issues to represent actual remaining work, with already-completed work-order requirements closed only after issue-level acceptance evidence is recorded and related parent phases updated coherently.

**Why this priority**: The issue ledger is the public project-management source of truth and must distinguish completed work from remaining release, deployment, and cleanup work.

**Independent Test**: Audit candidate child issues #39 through #62, #64 through #72, and #74 against their individual acceptance criteria on the current `main` commit. Record evidence on each issue, close only fully satisfied issues, and close phase parents #6 through #9, #11, and #12 only when every child in the phase is complete.

**Acceptance Scenarios**:

1. **Given** a candidate issue's full acceptance criteria are demonstrated by current-main files, tests, artifacts, or hosted behavior, **When** certification runs, **Then** the issue receives concise reproducible evidence and may be closed.
2. **Given** any acceptance criterion is unproven, branch-only, release-dependent, deployment-dependent, or requires private workstation state, **When** certification runs, **Then** the issue remains open with the missing evidence or follow-up dependency stated explicitly.
3. **Given** all child issues of a phase are closed with evidence, **When** the parent phase is evaluated, **Then** the parent receives a child-status summary and may be closed; otherwise it remains open.

---

### User Story 3 - Publish a Bounded, Review-Complete Pull Request (Priority: P2)

As the repository owner, I need S003 pushed as an official pull request, with continuous integration green and every comment from the permitted Codex review rounds answered and resolved before the work returns to me for merge.

**Why this priority**: The owner must receive a review-ready pull request without being asked to supervise routine CI or bot feedback, while avoiding another recursive review loop.

**Independent Test**: The pull request is open and unmerged, all required checks are successful, the automatic review round is fully handled, exactly one `@Codex` second-round request is posted, the second round is fully handled, and no third review request exists.

**Acceptance Scenarios**:

1. **Given** the S003 branch passes local verification, **When** it is pushed, **Then** an official pull request is opened with issue links, scope exclusions, verification evidence, and the review-round ledger.
2. **Given** the automatic first review round produces comments, **When** they arrive, **Then** every comment receives a substantive response, warranted changes are implemented and verified, and every addressed thread is resolved.
3. **Given** the automatic first round is represented only by an approving reaction or no actionable finding, **When** that signal is confirmed, **Then** it is recorded as a completed first round without inventing feedback.
4. **Given** the first round is complete, **When** the one authorized `@Codex` second-round request is posted, **Then** its comments are handled by the same evidence gate and no further review request is posted.
5. **Given** both permitted review rounds are satisfied and required checks are green, **When** S003 concludes, **Then** the pull request remains open and the owner is asked to perform the final review and merge ritual.

### Edge Cases

- A review finding maps to behavior already fixed by a merged correction but its source thread remains unresolved.
- A finding is outdated in GitHub while its underlying behavior still reproduces.
- A candidate issue has several acceptance criteria and only the aggregate build, rather than each criterion, is green.
- A generated artifact from a prior full-capability run survives a lower-capability rebuild and creates false evidence.
- A review round produces no review object but a Codex-authored thumbs-up reaction on the pull request body.
- CI is green before reviews arrive, or reviews are satisfied before CI completes.
- A late comment appears after the second-round request without requiring or authorizing a third request.
- Public evidence accidentally contains a local absolute path, credential, account identifier, zone identifier, or other private operational detail.

## Requirements

### Functional Requirements

- **FR-001**: S003 MUST maintain a one-to-one trace from inherited finding tasks `003-T001` through `003-T019` to GitHub issues #17 through #25 and #27 through #36 and their source review threads.
- **FR-002**: Each inherited finding MUST be tested against the exact current `origin/main` base used to create the S003 branch.
- **FR-003**: A still-reproducible finding MUST receive a regression test that fails before its correction and passes afterward, except where an existing regression already demonstrates the failure and can be cited without duplication.
- **FR-004**: Each inherited source thread MUST receive a substantive disposition reply and MUST NOT be resolved until its linked acceptance criteria are supported by reproducible evidence.
- **FR-005**: Outdated thread status MUST NOT substitute for a disposition reply or verification evidence.
- **FR-006**: S003 MUST evaluate candidate work-order child issues #39 through #62, #64 through #72, and #74 individually against their published acceptance criteria.
- **FR-007**: Issue closure evidence MUST identify the verified commit, the relevant repository or hosted evidence, and the reproducible check used.
- **FR-008**: An issue MUST remain open when any acceptance criterion depends on an unmerged S003 correction, an unpublished release, an unverified deployment, private workstation state, or other missing proof.
- **FR-009**: Phase parents #6 through #9, #11, and #12 MUST be closed only after every linked child is closed with evidence; otherwise the parent MUST remain open with an accurate progress summary.
- **FR-010**: Issues #63 and #73, issue #75 unless its production acceptance is independently demonstrated, issues #76 through #86, and program parent #37 are outside the closure target for this slice.
- **FR-011**: S003 MUST NOT create a tag, publish a release, deploy a release, merge its pull request, or perform Phase 10 legacy staging disposition.
- **FR-012**: All public repository and GitHub evidence MUST omit secrets, credentials, private absolute workstation paths, and private provider account, zone, record, or infrastructure identifiers.
- **FR-013**: S003 MUST run the repository's focused tests, full local verification, generated-content checks, encoding checks, and a clean repository-only rebuild before publication.
- **FR-014**: The S003 branch MUST be pushed and an official pull request MUST be opened after local verification succeeds.
- **FR-015**: The pull request MUST document linked issues, verified scope, deliberately excluded scope, local checks, and a review-round ledger.
- **FR-016**: Review round 1 MUST be the review automatically triggered by pull-request publication and MUST be fully processed before requesting round 2.
- **FR-017**: Review round 2 MUST be requested by exactly one pull-request comment containing `@Codex` and MUST be fully processed.
- **FR-018**: S003 MUST NOT post a second explicit `@Codex` request or otherwise initiate a third Codex review round.
- **FR-019**: Every actionable comment in both permitted rounds MUST receive necessary code or documentation changes, verification, a substantive reply, and thread resolution.
- **FR-020**: Completion requires every required continuous-integration check to be successful and the pull request to remain open for owner-controlled merge.
- **FR-021**: Historical S002 artifacts MUST be retained, but any stale completion claim discovered during reconciliation MUST receive a clear dated correction or supersession note.

### Key Entities

- **Review Finding**: One inherited Codex observation with a stable task ID, GitHub issue, source pull request, source thread, affected behavior, acceptance criteria, current disposition, and evidence.
- **Issue Certification**: The decision for one work-order issue, including acceptance criteria checked, evidence collected, verified commit, closure eligibility, and any remaining blocker.
- **Evidence Record**: A public, reproducible reference to a file, test, generated artifact, workflow run, deployment, or review reply that contains no sensitive information.
- **Review Round**: One bounded Codex review event with ordinal 1 or 2, trigger type, arrival signal, comments, responses, changes, resolution state, and completion time.
- **Phase Closure**: A parent-issue decision derived from the evidence-backed state of every linked child.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All 19 inherited review findings have a current-main disposition, public evidence, a substantive source-thread reply, and a resolved source thread.
- **SC-002**: All still-reproducible inherited findings are protected by regression coverage and corrected without weakening an existing test or quality gate.
- **SC-003**: Every candidate work-order issue is evaluated individually, and 100 percent of closures include reproducible issue-level evidence rather than only aggregate CI status.
- **SC-004**: Every parent phase closure is supported by 100 percent closed child issues; no incomplete phase parent is closed.
- **SC-005**: Local verification and every required pull-request check complete successfully.
- **SC-006**: Every actionable comment from both permitted Codex review rounds is answered and resolved.
- **SC-007**: The review ledger records exactly one automatic round and exactly one explicit `@Codex` round, with zero third-round triggers.
- **SC-008**: The final pull request is open, unmerged, and ready for the owner's final review and merge ritual.
- **SC-009**: Automated and manual scans find zero secrets, private absolute paths, or private provider identifiers in new public content.

## Clarifications

### Session 2026-09-03

- The owner's push and pull-request authorization overrides the autopilot protocol's usual pre-push halt for S003 only; merge, tag, release, and deployment authority remain excluded.
- The maximum Codex review budget is two rounds: the automatic publication round followed by exactly one explicit `@Codex` request after round 1 is complete.
- Issue closure is based on current-main acceptance evidence. A correction that exists only on the open S003 branch cannot by itself justify closing the affected issue before merge.
- Release tasks #63 and #73, production deployment issue #75 unless independently already proven, Phase 10 issues #76 through #86, and the overall program parent #37 remain outside this slice's closure target.

## Assumptions

- GitHub issues and source review threads remain available through the authenticated GitHub CLI.
- `origin/main` is the authoritative integration baseline, even if another local checkout's `main` branch is divergent.
- Existing generated assets may be reused as evidence only when their provenance and reproducibility from committed sources are demonstrated.
- A bot-authored approving reaction with no actionable review comments is a valid no-findings signal for a review round only after the pull request's review state and threads are inspected.
- Late comments belonging to an already-triggered permitted round are handled, but they do not authorize another review request.
