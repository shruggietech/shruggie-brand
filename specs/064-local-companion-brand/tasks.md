# Tasks: Local Companion Brand Kit and Public Showcase

## Phase 1: Setup

- [x] T001 Create the S064 specification and requirements checklist in `specs/064-local-companion-brand/`.
- [x] T002 Create the implementation plan, research, data model, public contract, and validation quickstart in `specs/064-local-companion-brand/`.

## Phase 2: Foundation

- [x] T003 Confirm the source app palette, typography, logo, packaging placeholder, and public-content boundary from `B:/AI/local-companion/brand/local-companion.json` and related local assets.
- [x] T004 Run the BrandBuilder full-tier preflight and prepare ignored approval workspace under `dist/local-companion-approval/`.

## Phase 3: User Story 1, Approved Identity

**Goal:** Bind an exact new abstract Full and Reduced identity to owner approval.

**Independent test:** The approved `glyphkit` source, renderer, palette, framing, and 32 proofs match the committed continuity record and regenerate without drift.

- [x] T005 [US1] Construct Full and Reduced calm-orbit paths using `dist/local-companion-approval/source/build/mk_paths.py`.
- [x] T006 [US1] Generate 32 production size and surface proofs and palette evidence in `dist/local-companion-approval/gate1-candidate.json`.
- [x] T007 [US1] Record the owner's exact Gate 1 decision and promote source atomically to `brands/local-companion/`.
- [x] T008 [US1] Revalidate the promoted `brands/local-companion/identity-continuity.json` after nonidentity brand copy and the owner-approved Node v24.11.0 production binding revision. The 32 proof hashes and geometry are unchanged.

## Phase 4: User Story 4, Assembled Fundamentals

**Goal:** Obtain exact owner approval of generated lockups, colors, type, icon sizes, synthetic application, and social image copy.

**Independent test:** Every reviewed derivative hash in the private Gate 2 manifest matches the current generated file, and approved social SVG/PNG hashes match final output.

- [x] T009 [US4] Render private lockup, icon, social, and synthetic application previews under `dist/local-companion-gate2/` and `dist/local-companion-approval/`.
- [x] T010 [US4] Finalize measured independent interface cue colors in `brands/local-companion/brand.json` and `skill/templates/color_roles.py` with focused tests. The owner chose app parity, and all four cue pairs meet AA on their assigned surfaces.
- [x] T011 [US4] Complete Local Companion guidance and the owner-approved single-line social copy in the private Gate 2 source and checksummed review packet under `dist/local-companion-gate2/`.
- [x] T012 [US4] Record owner approval for corrected Gate 2 packet SHA-256 `4f668c3e328fb84593812374791f7659156cd851785b62e3c02cd6e8409bf71c`, exact derivatives, social copy, SVG/PNG hashes, and public surface scope in `brands/local-companion/brand.json`.

## Phase 5: User Story 2, Verified Kit

**Goal:** Build a complete portable Local Companion kit with zero required failures.

**Independent test:** `scripts/build_all.py local-companion` and the full production aggregate report zero `verify.py` problems and zero glyph failures; generated platform and social assets match the approved manifest.

- [x] T013 [US2] Finish the source-only `brands/local-companion/brand.json` guide, content, type, palette, and approval bindings.
- [x] T014 [US2] Validate schema, source continuity, logo geometry, AA roles, icon suites, social image, and generated kit in `dist/local-companion/`. The build reports zero verification problems, zero glyph failures, and exact social SVG/PNG and derivative manifest hashes.
- [ ] T015 [US2] Run the full documented production build and regression suite from `scripts/build_all.py`, `skill/templates/`, and `site/`.

## Phase 6: User Story 3, Public Site and Release

**Goal:** Publish the verified Local Companion kit through the official catalog and a versioned release.

**Independent test:** The CI-built release archive checksum matches SHA256SUMS, and the live site serves the approved Local Companion route, registry, guidance, social image, and download.

- [x] T016 [US3] Add Local Companion to `skill/templates/interface_contract.py`, `scripts/audit_publication_artifacts.py`, `.github/workflows/build.yml`, and site/release test inventories.
- [x] T017 [US3] Update builder version, `skill/references/release-impact.json`, migration note, and root/skill changelogs for the new public release.
- [ ] T018 [US3] Build the static site and audit public routes, metadata, registries, downloads, and private-content exclusion from `site/` and `dist/`.
- [ ] T019 [US3] Review and merge the source change, publish the exact tag-built release, and verify live `brand.shruggie.tech` output and archive SHA-256.

## Final Phase: Cross-Cutting Review

- [x] T020 Run cross-artifact Spec Kit analysis, reconcile `spec.md`, `plan.md`, `tasks.md`, and verification evidence in `specs/064-local-companion-brand/`. All ten functional requirements and five measurable outcomes map to tasks, with no constitution conflict found.
- [x] T021 Confirm all authored text is UTF-8 without BOM and LF, scan deliverables for mojibake, and ensure no generated `dist/` content is committed. The scan covered 37 authored text files, 182 kit files, and 183 archive entries with zero issues; Git status contains only source paths.

## Dependencies and Execution Order

US1 precedes US4 because derivatives must use approved canonical geometry. US4 precedes US2 because final kit compilation requires Gate 2 approval. US2 precedes US3 because public site and release assets consume verified kit output. T010 followed the owner's app-cue decision. T012 followed the complete review packet and the owner's exact approval. T019 depends on all required CI and publication audits.

Both owner creative gates are approved. Publication eligibility and release work cannot be marked complete until the full production gates and live output checks pass.
