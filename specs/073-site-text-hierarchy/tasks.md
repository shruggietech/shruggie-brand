# Tasks: Site text hierarchy and containment

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/site-text.md](contracts/site-text.md), and [quickstart.md](quickstart.md).

**Tests**: Required by FR-009 and the repository accessibility and production-kit gates.

## Phase 1: Setup

- [x] T001 Create the isolated S073 branch and specification under specs/073-site-text-hierarchy/ without disturbing the S072 checkout.
- [x] T002 Run the Spec Kit specification, clarification, built-in quality checklist, and plan steps; record decisions and constitution gates.

## Phase 2: Foundation

- [x] T003 Read the current site, reference source, documentation validator, and verification selectors; record the 68-entry baseline and issue links in specs/073-site-text-hierarchy/research.md.
- [x] T004 Run the read-only Spec Kit analyze gate over spec.md, plan.md, and tasks.md; resolve any findings before implementation.
- [x] T005 Add #311 to shruggie-brand Delivery and assign S073 to #310, #311, and #335, using the project lifecycle fields without inventing a milestone.

## Phase 3: US1 - Complete portfolio titles (#310, P1)

**Goal**: Fit exact names and markers before reaching the card edge. **Independent test**: rendered clearance and synthetic long-name behavior.

- [x] T006 [US1] Add a failing rendered regression in site/scripts/verify-site.mjs for DanceWithMe865 clearance, current title consistency, a temporary long-name case, and marker accessibility.
- [x] T007 [US1] Implement bounded measured title fitting and contained wrap fallback in site/components/brand-portfolio.tsx and site/app/globals.css.
- [x] T008 [US1] Run the focused site verification and record measured title results in specs/073-site-text-hierarchy/verification.md.

## Phase 4: US2 - Compact References entries (#311, P1)

**Goal**: Make each ID and its four fields one scannable unit. **Independent test**: representative and full-entry structure, links, and reflow.

- [x] T009 [US2] Add failing source and rendered assertions for ordered, distinct fields, existing anchors, representative long entries, and narrow-width containment in site/tests/site.test.mjs and site/scripts/verify-site.mjs.
- [x] T010 [US2] Reformat all 68 entries in skill/references/references.md as separate labeled fields while preserving exact wording, IDs, and link targets.
- [x] T011 [US2] Scope compact reference-unit styling to the References route in site/app/docs/[[...slug]]/page.tsx and site/app/globals.css.
- [x] T012 [US2] Run documentation-reference, Markdown, and focused site checks; record entry/link equivalence and rendered results in verification.md.

## Phase 5: US3 - Portfolio introduction (#335, P2)

**Goal**: Put the approved description beneath its heading. **Independent test**: DOM order, visual grouping, exact copy, and unchanged Conformance heading layout.

- [x] T013 [US3] Add a failing site assertion for the portfolio introduction's shared parent and order, plus an unaffected Conformance check.
- [x] T014 [US3] Update site/app/(site)/page.tsx and scoped site/app/globals.css so the description sits beneath Our Portfolio.
- [x] T015 [US3] Run the focused site checks at desktop and mobile widths; record exact copy and anchor behavior in verification.md.

## Phase 6: Cross-surface validation and delivery

- [x] T016 Inspect rendered home and References pages at narrow desktop, 390px, 320px, and enlarged text, including dark/light themes, keyboard focus, overflow, and measured contrast; record evidence in verification.md.
- [x] T017 Run the full documented source, site, production-kit, glyph, PDF, WordPress, accessibility, and publication validation; record exact pass/fail/skip results in verification.md.
- [x] T018 Update CHANGELOG.md proportionally, check UTF-8 without BOM, LF, mojibake, generated-artifact exclusion, and git diff --check; reconcile spec, plan, tasks, and verification.md.
- [x] T019 Commit the verified S073 source and artifacts, push the branch, open an official PR closing #310, #311, and #335, and attach it to this task.
- [ ] T020 Monitor CI and external reviews, address every finding, run at most one explicit @Codex second review round, and hand off only after all checks and applicable reviews are satisfied.

## Dependencies

T001-T005 precede implementation. Each user story has independent tests and implementation; T006-T008, T009-T012, and T013-T015 may be completed in that order to avoid shared site verifier conflicts. T016-T020 depend on all three stories.

## Implementation strategy

Complete the three stories in priority order, proving each with a failing check before its implementation. Treat S073 as one reviewable source change; preserve all approved wording and IDs and use the full validation gate before publication.
