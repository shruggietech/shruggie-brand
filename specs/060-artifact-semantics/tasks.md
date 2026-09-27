# Tasks: Generated Artifact Semantics

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [coverage matrix](contracts/coverage-matrix.md)

## Phase 1: Audit and failing tests

- [x] T001 [US3] Inventory generated artifact families, producers, consumers, schemas, required/optional states, publication surfaces, and use tests in `contracts/coverage-matrix.md`.
- [x] T002 [US1] Add failing portable-manifest tests for empty required inventory, duplicate/unsafe path, missing reference, wrong hash/version, and valid optional absence in `skill/templates/test_pipeline.py`.
- [x] T003 [US2] Add failing publication tests for omitted or altered registry/download, mismatched facts/versions, and staged release checksum drift in `scripts/test_publication_workflow.py`.

## Phase 2: Kit semantics

- [x] T004 [US1] Strengthen `skill/templates/verify.py` manifest validation to require a populated, root-contained, unique, complete-enough inventory with identity and byte checks.
- [x] T005 [US1] Run existing specialized registry, icon, provenance, adapter, conformance, documentation, and archive validators on the candidate; do not duplicate their contract rules.

## Phase 3: Public and candidate semantics

- [x] T006 [US2] Extend `scripts/audit_publication_artifacts.py` with exact per-brand kit-to-public registry, download, conformance, and projected fact/version checks.
- [x] T007 [US2] Certify exact staged release files and SHA256SUMS after copying in `.github/workflows/build.yml`; reject incomplete or changed candidate assets.
- [x] T008 [US2] Keep optional custom assets/handoff and unsupported capability states conditional while requiring every advertised public entry to resolve.

## Phase 4: Verification and handoff

- [x] T009 [US3] Update Unreleased changelogs and record classified findings, validation layers, and limitations in `verification.md`.
- [x] T010 Run focused regressions, eight production kit and glyph checks, archive and site CI-parity tests, accessibility, source encoding, and candidate publication audit.
- [ ] T011 Run Spec Kit cross-artifact analysis again, resolve blocking findings, commit and push S060, open the official PR, and attach it to this task.
- [ ] T012 Resolve all first-round review comments and CI failures, trigger at most one second review round, resolve its findings, and hand off only when checks are green.

## Dependencies

T001 establishes the family contract. T002-T003 precede T004-T008 and must fail for the expected reasons before implementation. T006 composes specialized checks without weakening T005. T009-T010 precede publication; T011-T012 follow the user's explicit push and PR authorization.
