# Implementation Plan: Authoritative Logo Source Contract

**Branch**: `codex/016-authoritative-logo-contract` | **Date**: 2026-09-07 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/016-authoritative-logo-contract/spec.md`

## Summary

Close issue #151 by making logo authority explicit and fail-closed. Extend the existing supplied-input contract with required `constructed` and `authoritative` source modes, bind authoritative Full and Reduced variants to approved immutable inputs, reject any contradictory construction helper or vector geometry, emit deterministic provenance for every generated logo derivative, verify source metadata and raster-mask topology, migrate all five production brands without changing identity data, and document the protected workflow.

## Technical Context

**Language/Version**: Python 3.8 minimum; JSON Schema Draft 2020-12; Markdown; generated SVG/PNG/JSON

**Primary Dependencies**: Python standard library, Pillow 10.4 minimum for raster measurement, FontTools, svgelements, existing native SVG rasterizers and ImageMagick capability routing

**Storage**: Committed brand definitions and authoritative input files under `brands/`; generator source under `skill/templates/`; generated provenance and kits under ignored `dist/`

**Testing**: `unittest` suites in `skill/templates/` and `scripts/`; five-kit aggregate build; release certification; site lint/build/tests; Markdown, encoding, mojibake, and Git hygiene checks

**Target Platform**: Offline-capable cross-platform brand-kit generator, Python 3.8 through current; generated web, desktop, Android, Apple, and Windows assets

**Project Type**: Source-first generator, static site consumer, and packaged skill

**Performance Goals**: Contract failures occur before generation; provenance verification adds no network access and completes within the existing aggregate build budget

**Constraints**: Never rewrite source artwork or existing path strings; no generated artifacts committed; WCAG 2.1 AA remains mandatory; authoritative validation cannot depend on Python assertions; Windows child processes remain hidden

**Scale/Scope**: Five production brands, one authoritative raster brand with distinct Full and Reduced masters, four constructed brands, all generated logo SVG/PNG variants and their downstream icon inputs

## Constitution Check

*GATE: Passed before research and rechecked after design.*

| Principle | S016 treatment | Result |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit contracts, brand definitions, tests, and docs only; write derivative provenance under ignored kit output. | PASS |
| P2. Identity geometry is preserved | Hash supplied bytes, fingerprint existing constructed paths, prohibit reconstruction, and compare derived raster masks to their declared sources. | PASS |
| P3. Accessibility has no exemption | Retain all existing color and rendered-size gates; S016 introduces no accessibility waiver or identity color change. | PASS |
| P4. Verification precedes publication | Add contract and derivative verification before successful kit completion, then run the complete production gate. | PASS |
| P5. The site consumes generated kits | Guidelines and site continue consuming generated logo outputs; no separately authored logo is introduced. | PASS |
| P6. Specifications and releases move together | S016 includes specification, plan, tasks, analysis, implementation evidence, and changelog entries; no release is cut. | PASS |

Post-design recheck: PASS. The data model and contracts keep immutable authority in committed brand source, generated evidence under `dist/`, and all identity comparisons measured without altering the approved masters.

## Project Structure

### Documentation (this feature)

```text
specs/016-authoritative-logo-contract/
|-- spec.md
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- evidence.md
|-- checklists/
|   |-- requirements.md
|   `-- authority.md
|-- contracts/
|   |-- source-authority.md
|   `-- derivative-provenance.md
`-- tasks.md
```

### Source Code (repository root)

```text
brands/*/brand.json                     # required source-mode migration
brands/shruggietech/assets/*            # immutable authoritative inputs
skill/references/canon.schema.json      # authoring schema
skill/references/03-interview.md         # operator decision workflow
skill/references/08-glyph-construction.md
skill/references/09-portability.md
skill/SKILL.md
skill/templates/brand_contract.py       # source-mode and binding validation
skill/templates/gen_logo.py             # derivative metadata and index
skill/templates/verify.py               # fail-closed generated lineage checks
skill/templates/build_kit.py            # construction-helper preflight messaging
skill/templates/test_brand_contract.py
skill/templates/test_pipeline.py
scripts/build_all.py
CHANGELOG.md
skill/CHANGELOG.md
```

**Structure Decision**: Extend the established brand contract and logo generator rather than introduce a second asset pipeline. Authoritative variants remain represented by the existing single imported-image element because it carries measured placement and mask semantics, but the new binding makes that element subordinate to the approved input record and rejects every non-image substitute. The generator emits a source-derived provenance index beside logo assets, and verification independently reconstructs the expected lineage from `brand.json`.

## Implementation Phases

1. Capture pre-S016 path and source hashes, then write failing contract tests for mode omission, invalid binding, unrelated geometry, stale sources, helper collision, and constructed-mode conflicts.
2. Extend the schema and runtime contract with explicit source mode, Full/Reduced bindings, a closed transformation vocabulary, and early construction-helper rejection.
3. Write failing pipeline and verifier tests for provenance completeness, embedded SVG metadata, valid recolors and lockups, stale lineage, undeclared operations, and altered mask topology.
4. Emit deterministic logo derivative provenance and verify it against source bindings, output metadata, source hashes, aspect ratio, and normalized raster masks.
5. Migrate all production brand definitions, update operator documentation and changelogs, and prove identity inputs did not change.
6. Run Spec Kit analysis again, complete all focused and aggregate gates, inspect generated evidence, and record official PR review outcomes.

## Complexity Tracking

No constitution violations require justification.
