# Tasks: Approved Messaging and Guide Parity

**Input**: spec.md, plan.md, research.md, data-model.md, contracts/messaging-projection.md

**Tests**: Required by spec and autopilot test discipline. Write focused failing tests before each implementation phase.

## Phase 1: Setup

- [x] T001 Confirm eleven-brand source and guide inventory in specs/067-approved-messaging-guide-parity/migration-inventory.md
- [x] T002 Record the complete PDF, portable, hosted, social, and consumer field-to-source map in specs/067-approved-messaging-guide-parity/field-map.md

## Phase 2: Foundational contract

- [x] T003 Add failing approved, absent, unresolved, conflicting, and cross-surface role tests in skill/templates/test_messaging.py
- [x] T004 Define the independent message roles and states in skill/references/canon.schema.json and skill/templates/brand_contract.py

## Phase 3: User Story 1 - Approved messages

**Goal**: Explicit owner decisions for each role; social composition approval remains independent.
**Independent Test**: Synthetic brief and brand validation reports the correct states and rejects inferred text.

- [x] T005 [US1] Extend private brief and Gate 2 review packet with separate role decisions in skill/templates/authoring_brief.py
- [x] T006 [US1] Update adaptive interview and source documentation in skill/references/03-interview.md and skill/references/02-kit-anatomy.md
- [x] T007 [US1] Migrate eleven brand records in brands/*/brand.json with only evidenced approvals and explicit absent or unresolved roles

## Phase 4: User Story 2 - Literal guide projection

**Goal**: Every public guide role is exact source copy or omitted.
**Independent Test**: Extracted PDF, portable, and hosted content agree with approved role values and source asset identities.

- [x] T008 [US2] Add failing guide role and asset parity tests for Fragcap, Go Schedule, Glitchpad, and ShruggieTech in skill/templates/test_messaging.py
- [x] T009 [US2] Remove generated brand prose and guide override fallbacks in skill/templates/_guidekit.py and skill/templates/gen_guide_pdf.py
- [x] T010 [US2] Project exact role decisions into portable HTML and portal JSON in skill/templates/gen_guidelines.py
- [x] T011 [US2] Render only approved roles in site/components/guidelines/overview-content.tsx and update site/lib/guidelines.ts
- [x] T012 [US2] Add exact-copy and role checks to skill/templates/verify.py and relevant consumer/site tests
- [x] T013 [US2] Move shared explanatory text to a shipped source and remove unapproved guide-only brand claims from brands/*/brand.json

## Phase 5: User Story 3 - Reviewable migration

**Goal**: No legacy message is silently lost or promoted.
**Independent Test**: Every source brand and old guide override has a classified exact-text inventory item.

- [x] T014 [US3] Complete per-brand source/evidence/disposition records in specs/067-approved-messaging-guide-parity/migration-inventory.md
- [x] T015 [US3] Complete all guide and asset role mappings in specs/067-approved-messaging-guide-parity/field-map.md

## Phase 6: Polish and gates

- [ ] T016 Run focused tests and full documented kit, glyph, PDF, site, accessibility, and publication gates; record results in specs/067-approved-messaging-guide-parity/verification.md
- [ ] T017 Update CHANGELOG.md with S067 behavior and architecture decision, check UTF-8 LF and mojibake, and commit source-only changes
- [ ] T018 Push codex/067-approved-messaging-guide-parity and open an official PR linked to #296 and #297
- [ ] T019 Resolve all first-round Codex and security bot comments, run and resolve at most one requested second Codex round, and wait for green required CI before owner merge handoff

## Dependencies

T001 and T002 establish the source inventory. T003 precedes T004 through T007. T008 precedes T009 through T013. T014 and T015 consolidate the completed mappings. T016 follows all code and source changes; T017 through T019 follow verification. No subagent parallelism is planned.
