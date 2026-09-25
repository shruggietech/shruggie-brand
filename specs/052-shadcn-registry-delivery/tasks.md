# Tasks: shadcn Registry Delivery

**Input**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, and `contracts/registry-delivery.md`

## Phase 1: Contract foundation

- [X] T001 Confirm generated registry, site copy, PDF, documentation, CI, and consumer paths; pin shadcn 4.21.0 and official schema snapshots.
- [X] T002 Add fail-first tests for catalog/direct parity, valid fileless theme, invalid font provider, missing/empty UI content, unsafe targets, broken dependencies, and missing endpoints.
- [X] T003 Implement one item collection and complete schema/semantic validation in `gen_nextjs.py`, a shared registry contract module, and `prepare_site.py`.

## Phase 2: Supported installation

- [X] T004 Add fail-first temporary consumer tests for pinned CLI theme/UI installation, compiled component and stylesheet behavior, and bundled local-font path resolution.
- [X] T005 Remove unsupported `registry:font` advertisement; make theme and UI payloads installable and document the local-font copy workflow.
- [X] T006 Add consumer tests to CI before candidate publication; retain explicit supported Next.js/Tailwind/shadcn versions and prove generated output behavior.

## Phase 3: Guidance and publication

- [X] T007 Update skill, generated README, PDF, hosted guidelines, and downloads to distinguish catalog discovery, item installation, and manual font setup.
- [X] T008 Validate every production registry and public projection inventory; reject stale or undeclared endpoints.
- [X] T009 Run full documented validation, UTF-8/LF/mojibake checks, and review source-only diff; record evidence.
- [ ] T010 Sync Spec Kit artifacts, commit and push S052, open the official PR, address every bot review comment with at most one additional Codex review round, and wait for required CI success before owner handoff.

## Dependencies

T001 precedes T002-T003. T002 fails before T003 implementation. T003 precedes T004-T008. T004 fails before T005-T006. T007-T008 precede full verification. T009-T010 follow implementation. Post-release public checks are recorded as pending until an authorized release deploys the change.
