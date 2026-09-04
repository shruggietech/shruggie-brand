# Research: S003 Review Reconciliation

## Decision 1: Use `origin/main` as the verification baseline

**Decision**: Base S003 on remote commit `cbd96487dec1a19d93695910ec4337729acb1325`, the current `origin/main` head at slice creation.

**Rationale**: The existing local `main` is divergent. The remote integration head contains the merged publication corrections and is the only appropriate baseline for review disposition and future pull-request comparison.

**Alternatives considered**:

- Reset or reuse local `main`: rejected because it would destroy or conflate unrelated local state.
- Continue the previous feature branch: rejected because its upstream is gone and it is not an isolated current-main baseline.

## Decision 2: Treat S002 completion claims as unverified historical claims

**Decision**: Preserve S002, but add a dated supersession note explaining that its checked implementation tasks do not establish source-thread resolution or issue closure.

**Rationale**: GitHub currently shows all 19 source threads unresolved and all related issues open. Rewriting the old checklist would obscure what happened. A correction note keeps history honest.

**Alternatives considered**:

- Leave S002 unchanged without explanation: rejected because it conflicts with current GitHub state.
- Uncheck or delete historical items: rejected because it silently rewrites the record.

## Decision 3: Separate technical disposition from issue closure

**Decision**: A review thread may be answered and resolved after a correction is verified on the S003 branch, but an issue whose acceptance demands current-main behavior remains open until merge supplies that evidence.

**Rationale**: This avoids both permanent review-thread clutter and premature claims about unmerged code.

**Alternatives considered**:

- Close an issue as soon as its branch is green: rejected because the published issue policy requires current-main evidence.
- Keep every review thread unresolved until after merge: rejected because the user explicitly requires the PR to arrive review-complete, and verified branch changes can substantively resolve review discussions.

## Decision 4: Use issue-level certification, not aggregate CI

**Decision**: Evaluate each candidate's full scope and acceptance checklist, cite exact checks and artifacts, and leave the issue open if any criterion is unproven.

**Rationale**: A green build can coexist with missing governance, hosted configuration, deployment, release, or documentation evidence.

**Alternatives considered**:

- Bulk-close all issues covered by a successful build: rejected as the failure mode this slice is intended to correct.
- Avoid closing any issue: rejected because it would preserve a misleading backlog despite demonstrably completed work.

## Decision 5: Bound Codex review with an explicit state machine

**Decision**: Record automatic round 1, then post exactly one `@Codex` request for round 2 after round 1 is complete. Handle late feedback without another trigger.

**Rationale**: The owner authorized a second round and prohibited more. A simple ordinal ledger makes compliance observable and prevents recursive triggers.

**Alternatives considered**:

- Trigger on every correction push: rejected because it creates the prohibited review loop.
- Skip round 2: rejected because the owner explicitly authorized and requested the second review cycle as part of the workflow.

## Decision 6: Keep release, deployment, and staging outside S003

**Decision**: Exclude v1.1.2 publication (#63 and #73), production redeployment evidence (#75 unless already independently satisfied), Phase 10 (#76 through #86), merge, tag, and release.

**Rationale**: These actions require post-merge state, separate destructive or external scope, or explicit owner ritual. They cannot be honestly completed by an open pull request.

**Alternatives considered**:

- Include them to maximize closure count: rejected because count is subordinate to truthful acceptance evidence and authorization boundaries.

## Findings on the Ground

- Pull request #16 contains 9 unresolved review threads.
- Pull request #26 contains 10 unresolved review threads, including 3 marked outdated but not resolved.
- Issues #17 through #25 and #27 through #36 map one-to-one to those 19 threads.
- Current main contains focused regression coverage for local fonts, registry naming, capability behavior, stale artifact cleanup, form and CTA semantics, Python 3.8 compatibility, and hidden Windows subprocess flags.
- The latest observed Build and Pages workflows on current main are successful, but that does not settle issue-specific hosted, release, deployment, or private-source criteria.
- No v1.1.2 GitHub release exists, so release-dependent issues cannot close in this slice.
