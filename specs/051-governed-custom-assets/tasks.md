# Tasks: Governed Custom Assets and Expressions

**Input**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/custom-assets.md`

**Tests**: The central contract cases were fail-first. Projection and integration regressions cover each subsequent implementation group.

## Phase 1: Foundation

- [X] T001 Confirm source bytes, existing authority, generator, portal, and site inventory paths.
- [X] T002 Add fail-first valid/empty/negative custom asset contract tests in `skill/templates/test_brand_contract.py`.
- [X] T003 Define schema and central validator/eligible selector in `skill/references/canon.schema.json` and `skill/templates/brand_contract.py`.

## Phase 2: Generated guides

- [X] T004 Add portable/PDF/portal expression tests, including exclusion and exact inventory.
- [X] T005 Replace `guide.expressions` with eligible projection in `gen_guidelines.py` and `gen_guide_pdf.py`; preserve source bytes and metadata.
- [X] T006 Migrate two I Heart PR Tours sand records to `custom_assets`; remove legacy independent authority.

## Phase 3: Hosted and downloads

- [X] T007 Add site projection, route, nav and download inventory tests for eligible and empty brands.
- [X] T008 Add optional hosted topic, verified custom delivery projection, asset library/download entries and preview behavior in generator, `prepare_site.py`, and site components.
- [X] T009 Verify every eligible ID appears once in each public output and no ineligible or empty section appears.

## Phase 4: Documentation and gates

- [X] T010 Document declaration, publication, source fidelity, preview, attribution and license rules in source-facing docs.
- [X] T011 Run complete documented Python/kit/glyph/site validation, browser/accessibility checks, source hash and mojibake/LF checks.
- [X] T012 Sync spec/plan/tasks/evidence, review source-only diff, commit, push and open official PR.
- [ ] T013 Address every received bot review comment, at most one additional Codex review round, and wait for CI green before owner handoff.

## Dependencies

T001 precedes T002-T003. T003 precedes all projections. T004 precedes T005-T006. T007 precedes T008-T009. T010 can proceed alongside implementation. T011-T013 follow implementation.
