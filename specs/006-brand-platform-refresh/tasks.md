# Tasks: Brand Platform Refresh

**Input**: Design documents from `specs/006-brand-platform-refresh/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: S006 uses test-driven implementation. Focused Python and browser assertions are written before their corresponding source changes.

**Organization**: Tasks are grouped by user story and ordered so the fixture retirement and generated-content boundary support the public site, documentation, and metadata stories.

## Phase 1: Setup and governance

**Purpose**: Establish the constitution and dependency baseline required by the slice.

- [x] T001 Amend fixture governance and record the 2.0.0 constitution decision in `.specify/memory/constitution.md`
- [x] T002 Add the Fumadocs, static search, Tailwind, Playwright, and accessibility dependencies and scripts in `site/package.json`, `site/pnpm-lock.yaml`, and `site/next.config.mjs`
- [x] T003 Extend ignored generated-site boundaries in `.gitignore` for Fumadocs and derived content without ignoring committed source

---

## Phase 2: Foundational generated-content boundary

**Purpose**: Make production discovery, documentation derivation, and copied identity assets deterministic and testable before page work begins.

**Critical**: No public page story begins until this phase passes.

- [x] T004 Write failing production-discovery, generated-brand-record, MDX-derivation, asset-copy, and stale-output tests in `scripts/test_prepare_site.py`
- [x] T005 Refactor production source discovery, deterministic record validation, canonical icon paths, derived MDX, public terminology handling, and stable root identity assets in `scripts/prepare_site.py`
- [x] T006 Add the Fumadocs source definition and generated MDX component contract in `site/source.config.ts` and `site/mdx-components.tsx`
- [x] T007 Add shared generated brand, documentation, metadata, and navigation helpers in `site/lib/brands.ts`, `site/lib/source.ts`, `site/lib/metadata.ts`, and `site/lib/layout.shared.tsx`

**Checkpoint**: One preparation command produces five validated brand records, authoritative generated MDX, stable root identity assets, and no hard-coded production set.

---

## Phase 3: User Story 4 - Remove synthetic public brand material (Priority: P1)

**Goal**: Remove the committed synthetic brand and retain isolated regression coverage.

**Independent Test**: Normal discovery lists five production brands, focused generator tests create temporary input, and no synthetic brand enters public or release output.

- [x] T008 [US4] Write failing temporary-input and production-only discovery regressions in `skill/templates/test_pipeline.py` and `scripts/test_prepare_site.py`
- [x] T009 [US4] Replace fixture-copy tests with temporary production-derived test input in `skill/templates/test_pipeline.py`
- [x] T010 [US4] Restrict normal source discovery to `brands/` and remove fixture assumptions in `scripts/build_all.py`, `.gitignore`, and active repository documentation
- [x] T011 [US4] Delete the retired synthetic fixture and remove its active homepage, preparation, test, workflow, and release references
- [x] T012 [US4] Add an active-source and generated-output absence regression to `scripts/test_prepare_site.py`

**Checkpoint**: The current implementation tree and clean generated output contain no active synthetic brand, while focused temporary regression input still exercises generator behavior.

---

## Phase 4: User Story 1 - Present the ShruggieTech brand portfolio (Priority: P1)

**Goal**: Deliver the approved message, company-aligned chrome, generated icon cards, responsive surfaces, and useful destinations.

**Independent Test**: A mobile or desktop visitor can identify the company, value, portfolio, process, and skill download, and all five generated cards are usable without a fixed count.

- [x] T013 [US1] Write failing homepage, navigation, footer, approved-copy, generated-card, and responsive-overflow assertions in `site/tests/site.test.mjs`
- [x] T014 [P] [US1] Implement accessible shared site header, footer, and skip link through the Fumadocs layout contract, `site/components/footer.tsx`, and `site/app/layout.tsx`
- [x] T015 [US1] Move custom routes into the shared route group and implement approved homepage messaging and generated portfolio cards in `site/app/(site)/layout.tsx`, `site/app/(site)/page.tsx`, `site/app/(site)/[slug]/page.tsx`, and `site/app/(site)/[slug]/downloads/page.tsx`
- [x] T016 [US1] Implement layered ShruggieTech surfaces, square app-icon cards, focus states, reduced motion, target sizing, and responsive layouts in `site/app/globals.css`

**Checkpoint**: The public site is visibly and verbally ShruggieTech, surfaces every generated production brand, and no longer exposes the rejected project, count, version, or CTA language.

---

## Phase 5: User Story 2 - Deliver searchable rendered documentation (Priority: P1)

**Goal**: Replace the flat Markdown renderer with the ShruggieTech-themed Fumadocs experience.

**Independent Test**: Every reference is searchable and navigable, the eight known table pages emit semantic tables, and public explanatory prose avoids the rejected term.

- [x] T017 [US2] Add failing documentation-route, search-index, semantic-table, source-preservation, and public-terminology assertions in `scripts/test_prepare_site.py` and `site/tests/site.test.mjs`
- [x] T018 [P] [US2] Implement the Fumadocs root provider, docs navigation shell, page renderer, generated parameters, and page metadata in `site/app/layout.tsx`, `site/app/docs/layout.tsx`, and `site/app/docs/[[...slug]]/page.tsx`
- [x] T019 [P] [US2] Implement the statically exported client search index in `site/app/static.json/route.ts`
- [x] T020 [US2] Complete ShruggieTech Fumadocs styling, semantic table overflow, code, heading, and navigation behavior in `site/app/globals.css`
- [x] T021 [US2] Remove the obsolete flat documentation routes and JSON renderer from `site/app/docs/page.tsx`, `site/app/docs/[slug]/page.tsx`, and generated preparation output

**Checkpoint**: `/docs/` is a searchable responsive documentation application generated from authoritative skill references, with all known tables rendered semantically.

---

## Phase 6: User Story 3 - Complete metadata and discovery (Priority: P1)

**Goal**: Emit complete route metadata, favicon and preview assets, manifest, robots policy, and an exact sitemap.

**Independent Test**: Static HTML and discovery files for every route contain absolute, route-appropriate metadata and exactly match the generated public inventory.

- [x] T022 [US3] Add failing emitted-title, canonical, description, Open Graph, Twitter, favicon, manifest, robots, sitemap, and route-inventory assertions in `site/tests/site.test.mjs`
- [x] T023 [US3] Implement root metadata, viewport, icon declarations, and stable site identity in `site/app/layout.tsx` and `site/lib/metadata.ts`
- [x] T024 [P] [US3] Implement generated robots and sitemap output in `site/app/robots.ts` and `site/app/sitemap.ts`
- [x] T025 [US3] Add route-specific metadata for homepage, brand, download, and documentation routes in `site/app/(site)/page.tsx`, `site/app/(site)/[slug]/page.tsx`, `site/app/(site)/[slug]/downloads/page.tsx`, and `site/app/docs/[[...slug]]/page.tsx`

**Checkpoint**: Every indexable route and discovery asset is complete, absolute, deterministic, and free of synthetic or duplicate entries.

---

## Phase 7: User Story 5 - Verify and publish the official pull request (Priority: P2)

**Goal**: Produce a complete, green, review-satisfied S006 pull request while retaining owner merge authority.

**Independent Test**: The pull request links all four issues, every required check is green, all authorized review comments are answered and resolved, and no third Codex review request exists.

- [x] T026 [US5] Implement the in-process static server, headless Playwright, axe, responsive, metadata, table, and route checks in `site/scripts/verify-site.mjs`, `site/tests/site.test.mjs`, and `site/package.json`
- [x] T027 [US5] Run site browser verification in `.github/workflows/build.yml` after static export without adding an interactive or visible child-process launcher
- [x] T028 [US5] Update current repository guidance, release descriptions, changelog additions, and architecture decisions in `README.md`, `CHANGELOG.md`, `docs/decisions.md`, and `skill/CHANGELOG.md` without rewriting accurate historical records
- [x] T029 [US5] Run every command in `specs/006-brand-platform-refresh/quickstart.md` and record exact local evidence in `specs/006-brand-platform-refresh/evidence.md`
- [x] T030 [US5] Validate UTF-8 without BOM, LF endings, mojibake absence, generated-artifact boundaries, and full task completion across the S006 change set
- [x] T031 [US5] Commit, push `codex/006-brand-platform-refresh`, and open the official pull request with `Closes #100`, `Closes #101`, `Closes #102`, and `Closes #103`
- [x] T032 [US5] Process the automatic Codex review and every CI result, push warranted corrections, respond substantively, and resolve threads only after evidence exists
- [x] T033 [US5] Request at most one explicit second Codex review when useful, process it completely, and record the bounded review outcome in `specs/006-brand-platform-refresh/evidence.md`
- [x] T034 [US5] Confirm all required checks and authorized reviews are satisfied, leave the pull request open, and ask the owner for the final review and merge ritual

## Dependencies and execution order

- Phase 1 establishes governance and dependencies.
- Phase 2 is the shared generated-content boundary and blocks all public stories.
- Phase 3 removes the synthetic source before public route generation.
- Phase 4 establishes shared public chrome used by homepage, brand, and download routes.
- Phase 5 adds the documentation shell without duplicating the custom public header.
- Phase 6 completes metadata after all route families exist.
- Phase 7 verifies the integrated result and owns all external pull-request state.

## Implementation strategy

Implement sequentially in the stated phase order because preparation, route structure, documentation compilation, and metadata share files and generated outputs. Tasks marked `[P]` are logically independent but remain within the same foreground session. Run each test task before its paired implementation and confirm the new assertion fails for the intended reason.

## Notes

- Historical specifications and changelog entries remain accurate records even when they mention the retired fixture. "Active reference" means current build, test, publication, operator guidance, or release behavior.
- Issue #104 is not implemented or closed by this slice. Publication eligibility remains production-source membership until the third-party ownership model is delivered.
- The explicit owner wording gate is complete. The remaining owner-only gate is merge after review completion.
