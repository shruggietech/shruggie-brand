# Tasks: Component Recipes and Web AppFrame

**Input**: Design documents from `specs/038-component-recipes-web-appframe/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and reviewer-owned checklist

**Tests**: Required by the specification. Test tasks precede implementation and must demonstrate the intended red state.

## Phase 1: Setup and dependency evidence

- [x] T001 Record the exact accessible headless package version, license, React range, and primary-source evidence in `specs/038-component-recipes-web-appframe/research.md` and `site/package.json`
- [x] T002 Update the frozen dependency lock in `site/pnpm-lock.yaml` without relying on a transitive package
- [x] T003 Confirm `.specify/feature.json`, branch naming, source/output boundaries, and the S038 baseline in `specs/038-component-recipes-web-appframe/plan.md`

---

## Phase 2: Foundational failing contracts

- [x] T004 [P] Add failing catalog, role, state, target, override, grammar, coverage, and ownership tests in `skill/templates/test_component_contract.py`
- [x] T005 [P] Add failing consumer schema v2, version, authority, provenance, and tamper tests in `skill/templates/test_interface_contract.py`
- [x] T006 [P] Add failing deterministic generator, export completeness, server safety, and adapter verification tests in `skill/templates/test_pipeline.py`
- [x] T007 [P] Add failing release archive and release-contract requirements in `scripts/test_package_release.py` and `scripts/test_release_contract.py`
- [x] T008 [P] Add failing generated TypeScript staging and cleanup tests in `scripts/test_prepare_site.py`

**Checkpoint**: New tests fail for missing recipe and adapter contracts, not for test harness errors.

---

## Phase 3: User Story 1 - Author bounded component recipes (Priority: P1)

**Goal**: Deliver the closed 15-recipe contract and fail-closed semantic validator.

**Independent Test**: Run `test_component_contract.py`; all valid catalog and negative mutation cases pass without generating a kit.

- [x] T009 [US1] Author the closed catalog and complete coverage rows in `skill/references/component-recipes.json`
- [x] T010 [US1] Author structural constraints in `skill/references/component-recipes.schema.json`
- [x] T011 [US1] Implement Python 3.8-compatible semantic validation, Interface Canon role resolution, override checks, and coverage checks in `skill/templates/component_contract.py`
- [x] T012 [US1] Implement AppFrame responsibility validation and browser, Tauri-style, and Wails-style single-owner host profiles in `skill/templates/component_contract.py`
- [x] T013 [US1] Run the focused contract suite and record completion in `specs/038-component-recipes-web-appframe/tasks.md`

**Checkpoint**: The recipe grammar cannot express arbitrary screens or weaken accessibility invariants.

---

## Phase 4: User Story 2 - Consume a shared web adapter (Priority: P2)

**Goal**: Generate framework-neutral semantic tokens and typed React server/client adapters for all recipes.

**Independent Test**: Generate one temporary production-brand kit twice, compare adapter bytes, type-check smoke imports, and verify complete recipe-to-export traceability.

- [x] T014 [US2] Implement `skill/templates/gen_web_react.py` to emit `tokens/interface.css`, adapter metadata, recipe copy, host profiles, support matrix, component CSS, and integration guidance
- [x] T015 [US2] Generate native semantic server components for AppFrame structure, Button, IconButton, Field, FormControls, ListRow, SplitPane structure, StatusBadge, Card, and EmptyState
- [x] T016 [US2] Generate the bounded Radix-backed client layer for Toolbar, Tabs, Menu, Dialog, Toast, SplitPane behavior, and the AppFrame environment bridge
- [x] T017 [US2] Add the generator to `skill/templates/build_kit.py` before enforcement generation and label legacy `components/` output as compatibility-only
- [x] T018 [US2] Stage generated TSX and Next/Vite smoke imports through `scripts/prepare_site.py` and include them in existing TypeScript validation
- [x] T019 [US2] Add the focused test to both Python CI jobs and keep it independent of Node in `.github/workflows/build.yml`

**Checkpoint**: Tokens work without React, server entry points are browser-global safe, and interactive imports are explicitly client-bound.

---

## Phase 5: User Story 3 - Establish one AppFrame owner (Priority: P3)

**Goal**: Prove shell ownership and accessible behavior in a generated browser specimen.

**Independent Test**: Run Playwright and axe against the generated specimen under browser and simulated desktop/mobile webview capability profiles.

- [x] T020 [US3] Generate `web/specimen.html` with all states, declared keyboard paths, focus return, announcements, targets, safe areas, titlebar regions, IME obstruction, forced colors, reduced motion, and scaled text
- [x] T021 [US3] Extend `site/scripts/verify-site.mjs` to exercise the generated specimen with axe and interaction measurements
- [x] T022 [US3] Emit conservative support records containing exact engine/configuration results and explicit native-host limitations
- [x] T023 [US3] Verify Radix portals target the AppFrame overlay root and that duplicate or missing inset ownership fails closed

**Checkpoint**: Actual browser checks, not prose alone, support the accessibility and ownership claims.

---

## Phase 6: Consumer, release, and documentation integration

- [x] T024 Upgrade `skill/references/consumer-contract.schema.json` and `skill/templates/interface_contract.py` to schema v2 with recipe and adapter versions, authority paths, and provenance
- [x] T025 Copy recipe authority through `skill/templates/gen_enforcement.py`, verify it in `skill/templates/verify.py`, and require it in deterministic recovery
- [x] T026 Update package and release certification in `scripts/package_release.py`, `scripts/test_package_release.py`, and `scripts/test_release_contract.py`
- [x] T027 Update `skill/SKILL.md`, synchronized `skill/AGENTS.md`, and relevant reference documentation with recipe and adapter entry points
- [x] T028 Synchronize Spec Kit artifacts and mark completed tasks in `specs/038-component-recipes-web-appframe/`

---

## Phase 7: Full verification and pull request

- [x] T029 Run Python compile, focused suites, interface/pipeline/release/site-preparation tests, and Markdown validation under local Python
- [x] T030 Run the full all-brand build and confirm zero `verify.py` and glyph failures without committing `dist/`
- [x] T031 Run site lint, static build, browser/axe tests, publication audit, instruction synchronization, mojibake scan, LF/BOM scan, `git diff --check`, and tracked-generated-artifact checks
- [x] T032 Review the complete diff for identity isolation, security, accessibility, test quality, and scope alignment; resolve all findings
- [ ] T033 Commit with a Conventional Commit subject including S038, push `codex/038-component-recipes-web-appframe`, and open an official PR closing #214 and #215
- [ ] T034 Wait for CI and every external review, address each comment, and trigger at most one authorized `@Codex` second review round
- [ ] T035 Confirm all checks and both review rounds are satisfied, then request the user's final review and merge ritual without merging

## Dependencies and execution order

- Phase 2 depends on dependency evidence but can precede final lock refresh.
- User Story 1 is foundational for User Stories 2 and 3.
- User Story 2 must generate the adapter before User Story 3 browser verification.
- Consumer and release integration follows stable generated paths.
- Full verification follows all implementation and documentation work.
- Test-first tasks T004 through T008 must demonstrate failures before T009 onward makes them pass.

## Notes

- The custom checklist is reviewer-owned and remains unchecked until a reviewer evaluates requirements quality. Autopilot proceeds because the built-in requirements checklist passed and no item records a known defect.
- Real Tauri, Wails, Android WebView, and cross-runtime golden evidence remain in #217. S038 records simulated profiles honestly and does not close #217 or #218.
- Generated `dist/`, release archives, site exports, and `site/generated/` are verification artifacts and must remain untracked.
