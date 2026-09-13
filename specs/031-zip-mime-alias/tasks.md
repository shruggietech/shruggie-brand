# Tasks: Hosted ZIP MIME Compatibility

**Input**: Design documents from `/specs/031-zip-mime-alias/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Regression tests are required by FR-009 and must be written and observed failing before implementation.

**Organization**: Tasks are grouped by user story so the compatibility correction, fail-closed boundary, and non-ZIP regression protection remain independently reviewable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it changes a different file and has no incomplete dependency
- **[Story]**: Maps the task to a user story from `spec.md`
- Every task names its target file or command source

## Phase 1: Setup and Evidence Baseline

**Purpose**: Record the observed production condition and establish the focused test baseline.

- [X] T001 Record issue #198, branch, production ZIP response type, body-check baseline, and initial focused-test result in `specs/031-zip-mime-alias/evidence.md`
- [X] T002 Review and complete the requirements-quality criteria in `specs/031-zip-mime-alias/checklists/payload-contract.md`

---

## Phase 2: Foundational Contract Matrix

**Purpose**: Encode the exact metadata and structure boundary before changing the shared validator.

**Critical**: Implementation must not begin until the new alias regression is observed failing.

- [X] T003 Add table-driven valid ZIP cases for `application/zip` and `application/x-zip-compressed`, including existing normalization behavior, in `site/tests/payload-contract.test.mjs`
- [X] T004 Add fail-closed cases for malformed ZIP bodies under both accepted types and valid ZIP bytes under unsupported types in `site/tests/payload-contract.test.mjs`
- [X] T005 Run `node --test site/tests/payload-contract.test.mjs` and record the expected pre-implementation alias failure in `specs/031-zip-mime-alias/evidence.md`

**Checkpoint**: The focused regression matrix is complete, established cases remain green, and the alias case fails for the intended reason.

---

## Phase 3: User Story 1 - Verify Valid Hosted ZIP Downloads (Priority: P1) MVP

**Goal**: Accept valid ZIP bodies labeled with either supported ZIP media type through the shared payload contract.

**Independent Test**: Run the focused payload test and observe both valid media-type cases pass with no diagnostic.

- [X] T006 [US1] Add `application/x-zip-compressed` to the exact ZIP media-type allowlist in `site/scripts/payload-contract.mjs`
- [X] T007 [US1] Run `node --test site/tests/payload-contract.test.mjs` and record both positive aliases passing in `specs/031-zip-mime-alias/evidence.md`

**Checkpoint**: A valid production-style ZIP response is accepted without an origin-specific branch.

---

## Phase 4: User Story 2 - Reject Mislabeled or Malformed Downloads (Priority: P2)

**Goal**: Prove that neither an accepted header nor valid archive bytes can independently satisfy the full contract.

**Independent Test**: Run the focused matrix and observe every malformed-body and unsupported-type case fail with the expected distinct diagnostic.

- [X] T008 [US2] Verify the negative ZIP matrix reports structure failures for malformed bodies and media-type failures for unsupported declarations in `site/tests/payload-contract.test.mjs`
- [X] T009 [US2] Reconcile diagnostic wording and exact allowlist output with `specs/031-zip-mime-alias/contracts/zip-payload-contract.md` without weakening `site/scripts/payload-contract.mjs`

**Checkpoint**: Both metadata and archive evidence remain independently mandatory and diagnostics remain distinct.

---

## Phase 5: User Story 3 - Preserve All Other Payload Contracts (Priority: P3)

**Goal**: Demonstrate that the narrow ZIP correction leaves other extension contracts and the complete site verifier unchanged.

**Independent Test**: Run the full site test command and observe all production-origin policy, payload, and generated-site checks pass.

- [X] T010 [US3] Run `pnpm --dir site test` and record the complete local verifier result in `specs/031-zip-mime-alias/evidence.md`
- [X] T011 [US3] Run the production-origin verifier against `https://brand.shruggie.tech` and record the hosted ZIP results in `specs/031-zip-mime-alias/evidence.md`

**Checkpoint**: Local and hosted verification apply the same contract, and non-ZIP coverage stays green.

---

## Phase 6: Polish and Cross-Cutting Validation

**Purpose**: Synchronize project records and prove CI parity before the local commit.

- [X] T012 [P] Add the S031 correction and dated payload-contract decision to `CHANGELOG.md`
- [X] T013 Run every applicable command from `.github/workflows/build.yml` and record full CI-parity results in `specs/031-zip-mime-alias/evidence.md`
- [X] T014 Re-run Spec Kit consistency analysis and reconcile `specs/031-zip-mime-alias/spec.md`, `plan.md`, `tasks.md`, checklists, and `evidence.md`
- [X] T015 Run `git diff --check` and inspect `git status --short` to ensure only intended source and S031 artifacts are included

---

## Dependencies and Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Starts immediately and establishes evidence ownership.
- **Foundational (Phase 2)**: Depends on setup and blocks implementation until the alias regression fails as expected.
- **User Story 1 (Phase 3)**: Depends on the complete regression matrix and supplies the MVP correction.
- **User Story 2 (Phase 4)**: Depends on User Story 1 so negative results are evaluated against the final allowlist.
- **User Story 3 (Phase 5)**: Depends on User Stories 1 and 2 and validates the shared integration boundary.
- **Polish (Phase 6)**: Depends on all stories.

### User Story Dependencies

- **User Story 1 (P1)**: Depends only on the foundational test matrix.
- **User Story 2 (P2)**: Uses the final User Story 1 allowlist but remains independently testable through negative fixtures.
- **User Story 3 (P3)**: Exercises the integrated contract after the positive and negative boundaries are complete.

### Parallel Opportunities

- T012 can be drafted while the full verification commands for T010, T011, and T013 are running, but must be reconciled with final evidence before commit.
- No implementation test tasks are marked parallel because they modify one focused test module and must preserve the required red-to-green sequence.

## Parallel Example: Cross-Cutting Documentation

```text
Task: "Add the S031 correction and decision to CHANGELOG.md"
Task: "Run complete CI parity and record results in evidence.md"
```

## Implementation Strategy

### MVP First

1. Record the production baseline.
2. Add the focused positive and negative regression matrix.
3. Observe the production alias case fail.
4. Extend the exact allowlist.
5. Observe the focused suite pass.

### Incremental Delivery

1. Deliver User Story 1 as the minimal compatibility correction.
2. Prove User Story 2's fail-closed metadata and structure boundary.
3. Prove User Story 3 through complete local and production-origin verification.
4. Synchronize the changelog, evidence, Spec Kit artifacts, and CI-parity record.

## Notes

- Tests precede implementation and the expected alias failure must be captured.
- Generated `dist/`, `site/out/`, release files, and `.specify/feature.json` stay uncommitted.
- No task changes hosting configuration, non-ZIP rules, identity sources, or artifact contents.
- Halt after the local conventional commit and before `git push`.
