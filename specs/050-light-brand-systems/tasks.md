# Tasks: First-Class Light Brand Systems

**Input**: Design documents from `specs/050-light-brand-systems/`

**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/guide-presentation.md`

**Tests**: Required by FR-008 and FR-009. Write failing regression cases before each implementation group.

## Phase 1: Setup

- [X] T001 Inspect current generator, site, and test boundaries in `skill/templates/`, `scripts/prepare_site.py`, and `site/` against `specs/050-light-brand-systems/plan.md`.

## Phase 2: Foundational

- [X] T002 Add fail-first missing/default/light/invalid guide-mode contract tests in `skill/templates/test_brand_contract.py` and `skill/templates/test_pipeline.py`.
- [X] T003 Define and validate optional `guide.surface_mode` and required light palette in `skill/references/canon.schema.json` and `skill/templates/brand_contract.py`; resolve default dark centrally.

## Phase 3: User Story 1 - Read a light-first brand guide (Priority: P1)

**Goal**: Generated PDF and portable output use the declared mode coherently.

**Independent Test**: Build light and default-dark representatives; inspect both generated HTML documents and measure all PDF page grounds.

- [X] T004 [P] [US1] Add failing PDF/portable guide mode, palette-copy, and focus-state tests in `skill/templates/test_pipeline.py`.
- [X] T005 [US1] Use the validated mode and correct light/dark comparison copy in `skill/templates/gen_guide_pdf.py`, `skill/templates/gen_guidelines.py`, and `skill/templates/build_kit.py`.
- [X] T006 [US1] Emit resolved mode and selected semantic colors in `skill/templates/gen_guidelines.py` portal payload.

## Phase 4: User Story 2 - Browse a light brand inside the portfolio (Priority: P2)

**Goal**: Hosted brand routes and portfolio cards are a complete light scope, independent of host theme.

**Independent Test**: Inspect light card, overview, logo, color, and downloads with root light/dark themes and no-script; compare unchanged dark brand.

- [X] T007 [P] [US2] Add failing portal/site-record contract cases in `scripts/test_prepare_site.py` and `site/tests/site.test.mjs`.
- [X] T008 [US2] Project governed card/guide mode and semantic tokens in `scripts/prepare_site.py` and `site/lib/guidelines.ts`.
- [X] T009 [US2] Apply route-local presentation and Fumadocs aliases in `site/app/(guidelines)/[slug]/layout.tsx` and `site/app/globals.css`.
- [X] T010 [US2] Replace dark-only portfolio filtering with governed light card, white well, action, hover, and focus styling in `site/components/brand-portfolio.tsx` and `site/app/globals.css`.

## Phase 5: User Story 3 - Trust the quality gates (Priority: P3)

**Goal**: Measured document and browser checks reject mode and contrast regressions.

**Independent Test**: Fail wrong-ground and inherited-dark fixtures, then run complete light/dark validation.

- [X] T011 [P] [US3] Add negative mode/ground tests in `skill/templates/test_pipeline.py` and `skill/templates/qc_render.py` test coverage.
- [X] T012 [US3] Extend hosted browser checks for mode invariance, local token colors, contrast, 360/390px, 200 percent zoom, no-script, reduced motion, and print in `site/scripts/verify-site.mjs`.
- [X] T013 [US3] Run both representative production builds and zero-problem `verify.py`, `validate_glyph.py`, and `qc_render.py` gates via `scripts/build_all.py`.

## Phase 6: Polish and Handoff

- [X] T014 [P] Document the authoritative presentation declaration and dark default in `skill/references/02-kit-anatomy.md`, `skill/SKILL.md`, and source-facing guidance.
- [X] T015 Run the complete validation from `CONTRIBUTING.md`, inspect produced contact sheets, and record results in `specs/050-light-brand-systems/evidence.md`.
- [X] T016 Review diff, source-only boundary, UTF-8/LF, and mojibake; sync all S050 docs and task markers in `specs/050-light-brand-systems/`.

## Phase 7: PR Review Resolution

- [X] T017 Validate a `light.*` showcase palette independently of guide mode, derive accessible light border tokens unconditionally, and add dark-guide/light-showcase regression tests in `skill/templates/`.
- [X] T018 Rerun the affected contract and full pipeline suites, audit source and Spec Kit files, and record the review correction in verification evidence. PR-thread response and CI monitoring follow the pushed commit.

## Dependencies and Execution Order

T001 precedes T002-T003. T003 is foundational. T004 precedes T005-T006. T007 precedes T008-T010. T011 precedes T012-T013. T014 may run alongside a story in separate files; T015-T016 follow all story work. User Story 1 is the MVP and can be verified independently; Stories 2 and 3 add hosted publication and quality gates.

## Parallel Opportunities

T004 and T007 touch separate test files and may be prepared in parallel after T003. T011 may be prepared alongside hosted styling. T014 touches documentation only and may run alongside implementation. Shared generator and CSS files remain sequential to avoid conflicts.

## Implementation Strategy

Complete validated source-mode resolution first, then generator parity, then hosted parity, then measured regression gates. Keep dark-first behavior as the compatibility baseline and leave release publication and downstream consumer adoption outside S050.
