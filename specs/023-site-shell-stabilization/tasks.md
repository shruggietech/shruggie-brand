# Tasks: Site Shell and Homepage Stabilization

**Input**: Design documents from `/specs/023-site-shell-stabilization/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/site-shell-contract.md`, `quickstart.md`

**Tests**: Source contracts and rendered-browser tests are mandatory because the specification requires exact semantics and measured layout behavior.

## Phase 1: Setup and baseline

**Purpose**: Confirm the approved boundary and record the current authoritative layout behavior.

- [x] T001 Confirm clean main ancestry, create `codex/023-site-shell-stabilization`, and retain `.specify/feature.json` as ignored machine-local state
- [x] T002 Validate `specs/023-site-shell-stabilization/spec.md` with `checklists/requirements.md` and record routine clarification decisions
- [x] T003 [P] Inspect homepage, shared layout, footer, Fumadocs TOC slot, and current verification sources in `site/app/(site)/page.tsx`, `site/lib/layout.shared.tsx`, `site/components/footer.tsx`, `site/app/globals.css`, `site/scripts/verify-site.mjs`, and `site/tests/site.test.mjs`
- [x] T004 [P] Record layout, policy, and verification decisions in `specs/023-site-shell-stabilization/research.md`, `data-model.md`, `contracts/site-shell-contract.md`, and `quickstart.md`

**Checkpoint**: S023 has an approved, issue-traceable design and measured-root-cause strategy.

---

## Phase 2: Foundational verification contracts

**Purpose**: Add regression checks before changing authoritative site behavior.

- [x] T005 Add failing source-policy assertions for exact homepage copy, removed callout, shared navigation records, and simplified footer records in `site/tests/site.test.mjs`
- [x] T006 Add failing rendered checks for homepage CTA order, destinations, arrow semantics, spacing, and removed content in `site/scripts/verify-site.mjs`
- [x] T007 Add failing rendered checks for shared header/footer route scope, canonical external behavior, and mobile navigation in `site/scripts/verify-site.mjs`
- [x] T008 Add geometry helpers and failing cross-route header, docs-column, scale, scrollbar, theme, and overflow checks in `site/scripts/verify-site.mjs`
- [x] T009 Run the focused source tests against the pre-change implementation and record the expected failures in `specs/023-site-shell-stabilization/evidence.md`

**Checkpoint**: New tests fail for the old homepage/chrome contract before implementation.

---

## Phase 3: User Story 1 - Primary homepage destinations (Priority: P1)

**Goal**: Deliver the exact Documentation, Download Skill, and Explore Our Portfolio hierarchy.

**Independent Test**: Render `/` at desktop and mobile widths and verify DOM order, targets, generated token treatments, cue semantics, spacing, interaction states, and reduced motion.

- [x] T010 [US1] Replace the hero action markup and exact labels in `site/app/(site)/page.tsx`
- [x] T011 [US1] Add deliberate supporting-action spacing and cue alignment using existing tokens in `site/app/globals.css`
- [x] T012 [US1] Run focused source and rendered homepage checks and resolve all failures

**Checkpoint**: The homepage exposes the approved action hierarchy and all three destinations.

---

## Phase 4: User Story 2 - Portfolio wording and callout removal (Priority: P1)

**Goal**: Present Our Portfolio with approved copy and remove the obsolete system panel completely.

**Independent Test**: Inspect source and rendered `/` for exact approved copy, unchanged portfolio anchor/cards, and absence of the obsolete wrapper, content, and styles.

- [x] T013 [US2] Change the portfolio heading and adjacent description in `site/app/(site)/page.tsx`
- [x] T014 [US2] Remove the system callout markup from `site/app/(site)/page.tsx` and its unused selectors from `site/app/globals.css`
- [x] T015 [US2] Run focused homepage copy, anchor, card, heading-order, and removed-content checks

**Checkpoint**: Homepage information architecture matches issues #171 and #172 without collateral card changes.

---

## Phase 5: User Story 3 - Shared navigation and footer (Priority: P1)

**Goal**: Add useful shared destinations and simplify the shared footer while preserving surface-specific target policies.

**Independent Test**: Render main-site and docs desktop/mobile chrome and compare exact records, destinations, target attributes, focus order, and guidelines isolation.

- [x] T016 [US3] Add Company and Download Skill canonical external records to `site/lib/layout.shared.tsx`
- [x] T017 [US3] Remove Brands and rename Download Skill in `site/components/footer.tsx` while preserving the S022 Company same-tab exception
- [x] T018 [US3] Run source and rendered shared-chrome tests across `/`, a download route, `/docs/`, a docs article, mobile navigation, and a neutral guidelines route

**Checkpoint**: Shared site/docs chrome is consistent and neutral guideline portals are unchanged.

---

## Phase 6: User Story 4 - Stable cross-route layout (Priority: P1)

**Goal**: Eliminate route-dependent header and documentation reading-column movement.

**Independent Test**: Browser geometry comparisons pass within one CSS pixel across required routes, themes, widths, scale factors, TOC states, and content heights.

- [x] T019 [US4] Reserve a stable scrollbar gutter at the shared document root in `site/app/globals.css`
- [x] T020 [US4] Verify the Fumadocs TOC placeholder reserves the same desktop rail as populated TOCs and add a shared layout-variable rule in `site/app/globals.css` only if measurement proves it necessary
- [x] T021 [US4] Ensure homepage and brand downloads share the declared shell width/gutter primitive without route-specific compensation in `site/app/globals.css`
- [x] T022 [US4] Run desktop, narrow, light, dark, scale-factor, short/tall, TOC/no-TOC, and horizontal-overflow browser measurements

**Checkpoint**: Persistent header and documentation reading content remain stationary within tolerance.

---

## Phase 7: Full validation and publication

**Purpose**: Prove the slice, publish one reviewable branch, and close every automated review loop.

- [x] T023 Run `pnpm --dir site lint`
- [x] T024 Run the static site build, using the documented webpack fallback only if the Windows Turbopack launcher is unavailable
- [x] T025 Run `pnpm --dir site test` with zero source, route, visual, interaction, geometry, or WCAG failures
- [x] T026 Run `python scripts/build_all.py` with zero production-kit verification or glyph failures
- [x] T027 Run `git diff --check`, UTF-8/BOM/LF, mojibake, prohibited-artifact, and machine-local-state checks
- [x] T028 Update `specs/023-site-shell-stabilization/evidence.md` with commands, results, accessibility impact, identity impact, documentation impact, and changelog decision
- [x] T029 Mark implemented work complete in `specs/023-site-shell-stabilization/tasks.md` without modifying reviewer-owned checklist markers
- [ ] T030 Commit S023 with a Conventional Commit subject, push the branch, and open an official PR that closes #170, #171, #172, #176, #177, and #178
- [ ] T031 Wait for initial CI and third-party Codex review, address every comment, reply with evidence, and resolve every completed thread
- [ ] T032 Request exactly one second review with `@Codex review`, then address and resolve every resulting comment without requesting a third round
- [ ] T033 Confirm final required CI is green, unresolved review thread count is zero, the PR is mergeable, and the branch is synchronized with `origin/main`

## Dependencies & Execution Order

- Phase 1 precedes all implementation.
- Phase 2 tests precede Phases 3 through 6 production changes.
- Phases 3 through 6 share files and therefore run sequentially even though their user outcomes are independently testable.
- Phase 7 begins only after all four user stories pass focused checks.
- T031 begins only after T030 publishes the PR. T032 runs once after initial review is satisfied. T033 follows the second review and any resulting patch.

## Parallel Opportunities

- T003 and T004 inspect or document different files and may proceed together.
- Validation commands that do not write shared generated state may be batched, but site builds and aggregate builds remain sequential to avoid output races.

## Notes

- Reviewer-owned `checklists/ux-accessibility.md` remains unchecked until human review. The user's explicit autopilot authorization permits implementation to proceed without altering it.
- Do not commit `.specify/feature.json`, `dist/`, `site/out/`, `site/test-results/`, generated archives, PDFs, PNGs, or registries.
- Do not request more than one explicit `@Codex review` round.
