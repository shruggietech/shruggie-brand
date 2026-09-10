# Implementation Plan: Approved Identity Construction Continuity

**Branch**: `codex/027-approved-identity-construction-continuity` | **Date**: 2026-09-09 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/027-approved-identity-construction-continuity/spec.md`

## Summary

Replace the ambiguous concept-to-production handoff with a source-bound identity lifecycle. A shared continuity module will validate committed identity records, produce and compare canonical approval proofs, enforce glyphkit provenance for newly approved constructed marks, and promote approved provisional sources without reconstruction. The build and verifier will fail before derivative generation when a governed source, geometry, framing, topology, palette, renderer, or proof binding drifts. All seven existing brands will receive historical-baseline records generated from their unchanged authoritative sources, with Cueson retained as the regression case for the previously observed construction-method and framing failure.

## Technical Context

**Language/Version**: Python 3.8 minimum for generator, validation, migration, and tests; JSON Schema 2020-12 and Markdown for source contracts and guidance

**Primary Dependencies**: Python standard library, Pillow 10.4+ for proof measurement and difference artifacts, existing coloraide 3.3+ for rendered color comparison, existing glyphkit and brand-contract modules, existing SVG rasterizer capability chain

**Storage**: Committed JSON and Python source under `brands/`, `skill/`, and `scripts/`; ignored approval packets, proof rasters, comparison images, audits, kits, site output, and archives under `dist/`

**Testing**: Existing unittest-style Python entry points, focused identity-continuity contract tests, synthetic temporary regression fixtures, full seven-kit build, release certification, site lint/build/browser accessibility suite, encoding and repository-hygiene checks

**Target Platform**: Offline-capable Windows and Linux workstations plus GitHub Actions; Python 3.8 compatibility and full Python 3.12 hosted validation

**Project Type**: Source-driven brand asset generator, governed approval workflow, verifier, static documentation site, and migration repository

**Performance Goals**: Validate one source identity in under 2 seconds without raster comparison; compare the complete 32-proof full/reduced matrix and emit evidence in under 30 seconds on the supported full tier; add less than 60 seconds to the aggregate seven-brand build

**Constraints**: Preserve all shipped geometry and palette bytes; fail closed before derivative generation; remain offline during ordinary generation; reject root and symlink escapes; preserve deterministic UTF-8/LF JSON; do not commit generated proof or kit output; do not infer historical approval; do not weaken WCAG 2.1 AA

**Scale/Scope**: Seven current production identities, two master variants where applicable, four sizes, four surfaces, same-renderer exact comparison, bounded cross-renderer comparison, one known-equivalent Cueson fixture, one known-divergent reconstruction fixture, and future brand creation

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

| Principle | Planned treatment | Result |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit schemas, continuity records, generator/verifier logic, tests, and guidance. Keep proof matrices, visual diffs, audits, kits, rasters, PDFs, registries, site exports, and archives ignored. | PASS |
| P2. Identity geometry is preserved | Snapshot every current master before migration, create records from unchanged source, use the merged Cueson source as regression evidence, and fail on any path or palette drift. No geometry normalization or identity redesign is permitted. | PASS |
| P3. Accessibility has no exemption | Require palette qualification before canonical approval and retain the existing AA floor without waivers. | PASS |
| P4. Verification precedes publication | Insert continuity validation before logo derivative generation, test all drift and security cases, rebuild every kit, and require full hosted validation. | PASS |
| P5. The site consumes generated kits | Do not author identity values in site source. Existing generated-kit projection remains the only public data path. | PASS |
| P6. Specifications and releases move together | Deliver complete S027 specification, research, data model, contracts, tasks, evidence, implementation, changelog decision, PR, and bounded review ledger. No tag or release is in scope. | PASS |

Post-design re-check: PASS. The design adds a source contract and fail-closed validation inside the existing generator boundary, retains imported identities without reconstruction, confines visual output to ignored paths, and makes no constitutional exception.

## Architecture and Delivery Decisions

1. Add `identity_continuity` as a required brand-source reference and define its record shape in the canon schema. Keep the record separate from `brand.json` so it can bind the relevant identity configuration without a self-referential file hash.
2. Store one committed `identity-continuity.json` beside each production `brand.json`. An `approved-canonical` record carries current owner approval evidence; a `historical-baseline` record states only current authoritative facts and evidence limits.
3. Compute one deterministic identity snapshot from logo source mode, exact full and reduced path arrays or authoritative-input bindings, palette and semantic roles, framing, construction provenance, and approved renderer/proof configuration. Hash structured values canonically rather than transcribing digests.
4. Validate continuity during the first source-contract phase of every build and again from generated output. A mismatch stops before logo derivatives. The generated kit receives a copy of the validated source record plus a measured continuity report.
5. For `glyphkit-constructed` sources, inspect the construction helper as Python syntax and require a glyphkit import plus approved primitive calls for path-producing values. Reject literal path data, custom path serializers, and executable indirection. Existing Covarity is classified `legacy-constructed` because its helper predates this law; correct only its inaccurate provenance label while preserving helper and path bytes exactly.
6. Provide a bounded promotion command that accepts only a complete `approved-canonical` bundle beneath an ignored approval root, validates every source hash and safe relative destination, copies into a new or explicitly replaceable brand root, revalidates byte equality, and rolls back partial writes.
7. Treat same-renderer proof hashes as exact. For documented cross-renderer comparisons, keep source and structural invariants exact, measure hard-mask topology and interior color exactly, ignore changed pixels only inside a one-pixel antialias edge band, require no changed pixels outside that band above 0.5 percent, and calibrate visible-bound and centroid tolerances from the unchanged Cueson source. Raw IoU remains evidence, not the decisive gate.
8. Generate side-by-side, alpha-overlay, silhouette-XOR, and color-difference images for review, but commit only their deterministic manifest contract and tests. Proofs remain ignored.
9. Update the brandbuilder interview and logo guidance so direction selection is not called final approval, every required conversion precedes canonical approval, and Gate 2 cannot introduce production geometry.
10. Push and open the S027 PR automatically after local verification under the owner’s explicit authorization. Process all received findings and no more than two Codex rounds, then halt before merge.

## Project Structure

### Documentation (this feature)

```text
specs/027-approved-identity-construction-continuity/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── canonical-approval.md
│   ├── promotion.md
│   └── verification-and-migration.md
├── checklists/
│   ├── requirements.md
│   └── continuity.md
├── spec.md
└── tasks.md
```

### Source Code (repository root)

```text
brands/
└── <slug>/
    ├── brand.json
    └── identity-continuity.json

scripts/
├── audit_identity_continuity.py
└── test_identity_continuity_audit.py

skill/
├── SKILL.md
├── CHANGELOG.md
├── references/
│   ├── 03-interview.md
│   ├── 06-logo-protocol.md
│   ├── 08-glyph-construction.md
│   ├── canon.schema.json
│   └── identity-continuity.md
└── templates/
    ├── identity_continuity.py
    ├── promote_identity.py
    ├── test_identity_continuity.py
    ├── brand_contract.py
    ├── build_kit.py
    ├── gen_logo.py
    ├── verify.py
    ├── test_brand_contract.py
    └── test_pipeline.py
```

**Structure Decision**: Extend the existing source-to-`dist/` generator boundary. The shared continuity module owns hashes, record validation, construction-source inspection, proof comparison, and evidence generation. Brand contract and build orchestration call that module rather than reimplementing identity rules. Per-brand records describe authoritative source; generated proof packets remain disposable. Promotion is a separate explicit command because ordinary builds must never mutate source.

## Complexity Tracking

No constitution violation or architectural exception is required.
