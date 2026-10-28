# Tasks: Owner-decided portfolio messaging

**Input**: spec.md, plan.md, research.md, data-model.md, contracts/public-messaging.md.

## Phase 1: Setup

- [x] T001 Create S072 specification and quality checklist in specs/072-approved-brand-messaging/.
- [x] T002 Read issue #309 comments and record supersession and use policy in specs/072-approved-brand-messaging/research.md.

## Phase 2: Foundation

- [x] T003 Inventory thirteen brands and source-bound evidence in specs/072-approved-brand-messaging/inventory.md (FR-005, FR-009).
- [x] T004 Analyze spec, plan, tasks, and constitution before implementation; record the result later in specs/072-approved-brand-messaging/verification.md.

## Phase 3: US1 - Recorded decisions (P1)

**Goal**: Apply exact recorded decisions without changing social copy. **Independent test**: source/schema checks and regenerated exact-message projections.

- [x] T005 [US1] Apply Covarity and Cueson decisions in brands/covarity/brand.json and brands/cueson/brand.json (FR-001, FR-002, FR-004).
- [x] T006 [US1] Apply DanceWithMe865's later slogan, explicit absence, and revoked descriptor removal in brands/dancewithme865/brand.json (FR-001, FR-003, FR-004).
- [x] T007 [US1] Record dated decisions in specs/072-approved-brand-messaging/decisions.md and correct specs/067-approved-messaging-guide-parity/migration-inventory.md (FR-002, FR-003).
- [x] T008 [US1] Refresh required brand source digests in brands/*/identity-continuity.json without changing identity snapshots or approvals (FR-009).

## Phase 4: US3 - Faithful consumers (P1)

**Goal**: Eliminate legacy fallback publication. **Independent test**: temporary approved/absent/unresolved consumer output including escaping and wrong-use records.

- [x] T009 [US3] Add and run failing consumer regressions in skill/templates/test_messaging.py (FR-007, FR-008).
- [x] T010 [US3] Replace legacy description fallbacks in skill/templates/gen_nextjs.py and skill/templates/gen_wordpress.py (FR-008).
- [x] T011 [US3] Run focused messaging, brand-contract, and continuity checks; record exact results in specs/072-approved-brand-messaging/verification.md (FR-010).

## Phase 5: US2 - Optional editorial completion (P2)

**Goal**: Let the owner choose researched copy without requiring all fields to be filled. **Independent test**: each new source value traces to a role-specific reply; deferred values stay unresolved.

- [x] T012 [US2] Research current brand/project material and document suggestions in specs/072-approved-brand-messaging/suggestions.md (FR-006, FR-007).
- [x] T013 [US2] Record the owner's four 2026-10-27 short-description approvals and defer other suggestions under the no-questions direction in specs/072-approved-brand-messaging/decisions.md (FR-002, FR-006).
- [x] T014 [US2] Apply only selected values in brands/*/brand.json and refresh specs/072-approved-brand-messaging/inventory.md; explicitly track unreviewed/unresolved roles (FR-001, FR-004, FR-005, FR-007).

## Phase 6: Final validation and handoff

- [x] T015 Record patch-version impact for the next coordinated release in CHANGELOG.md and refresh final continuity digests, retaining current numeric versions in this source-only slice (FR-009).
- [x] T016 Run all documented production kit, glyph, PDF, contract, WordPress runtime, site, accessibility, and publication checks; inspect changed copy surfaces and record evidence in specs/072-approved-brand-messaging/verification.md (FR-010).
- [x] T017 Check source-only diff, UTF-8/BOM/LF/mojibake, Markdown, and git diff --check; synchronize specs/072-approved-brand-messaging/ artifacts and commit locally (FR-010).

## Dependencies and execution order

T001-T004 precede source implementation. US1 and US3 share the foundation and can be validated independently; execute them before editorial review. T012 research may run alongside focused checks, but T014 depends on explicit owner selections. No arbitrary wait turns a pending suggestion into approval. T015-T017 follow the final selected or deferred set.

## Parallel opportunities

Independent Covarity/Cueson source edits and separate Next.js/WordPress fixes may be developed independently, but all canonical JSON and continuity edits are serialized per brand. Research for US2 can overlap validation of US1/US3. No agent delegation is required.

## Implementation strategy

Deliver recorded corrections and the four later approved short descriptions. The owner deferred further questions, so retain visible unresolved rows and finish validation of the selected subset. Push and merge are authorized by the 2026-10-27 cleanup request; do not tag, release, or deploy as part of this slice.
