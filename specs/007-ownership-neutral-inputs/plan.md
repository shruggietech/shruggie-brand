# Implementation Plan: Ownership-Neutral Authoritative Inputs

**Branch**: `codex/007-ownership-neutral-inputs` | **Date**: 2026-09-05 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/007-ownership-neutral-inputs/spec.md`

## Summary

Deliver issues #104 and #105 as one contract migration. Add required affiliation, showcase, inheritance, typography-mode, and authoritative-input fields to the brand schema; validate them before generation; remove hard-coded ShruggieTech ownership, semantic-color inheritance, and house-font assumptions from generated surfaces; preserve and audit supplied artwork; derive deterministic palette evidence that requires current human approval before canonical use; add controlled, atomic fixed-font ingestion; and migrate all five production brands without changing their identities. Native platform icon suites remain in #106 for S008.

## Technical Context

**Language/Version**: Python 3.8 minimum; JSON Schema Draft 2020-12; TypeScript 5.9; Node.js 20 minimum

**Primary Dependencies**: Python standard library, Brotli 1.1.0, fontTools 4.55.8, Pillow 10.4.0, svgelements 1.9.6, coloraide 3.3, existing Next.js 16.3.4 site toolchain

**Storage**: Committed brand definitions and authoritative inputs under `brands/`; shared approved font binaries under `assets/fonts/`; ignored evidence and generated kits under `dist/`; no confidential contracts or generated release artifacts committed

**Testing**: Python contract, generator, site-preparation, release-contract, and pipeline tests; five production builds; glyph and kit verification; Next.js type check, export, and browser verification; hosted CI and two bounded external review rounds

**Target Platform**: Offline-generated brand kits and static site output on Windows and Ubuntu GitHub Actions, with Python 3.8-compatible source and hidden child processes

**Project Type**: Python generator and validator suite with a statically exported Next.js portfolio and documentation site

**Performance Goals**: Contract validation fails before expensive rendering; palette analysis is deterministic for unchanged bytes; controlled ingestion uses bounded downloads; routine generation performs zero network requests

**Constraints**: Preserve source bytes and shipped logo path data; require human palette approval; WCAG 2.1 AA; no implicit affiliation or typography default; UTF-8 without BOM and LF; generated artifacts remain ignored; no third Codex review request; owner-only merge

**Scale/Scope**: Five production brands, two GitHub issues, one schema, four shared contract operations, eight generator surfaces, the public publication filter, focused synthetic temporary regressions, and one official pull request

## Constitution Check

| Principle | Design response | Gate |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit schema, source declarations, templates, tests, and operator documentation only. Palette evidence and kits remain generated. Fixed fonts enter only through the existing `assets/fonts/` source boundary. | PASS |
| P2. Identity geometry is preserved | Hash every authoritative input, preserve original bytes and declared vector path data, reject undeclared transformation, and keep palette extraction evidence-only until approval. | PASS |
| P3. Accessibility has no exemption | Palette approval does not bypass existing contrast and WCAG 2.1 AA checks. | PASS |
| P4. Verification precedes publication | Validate the contract before generation, scan third-party outputs, rebuild all production kits and the site, and wait for hosted CI and bounded review completion. | PASS |
| P5. The site consumes generated kits | Site publication reads validated affiliation and showcase state from verified generated brand records and publishes only explicit public entries. | PASS |
| P6. Specifications and releases move together | S007 carries specification, plan, tasks, analysis, evidence, issue traceability, changelog records, review handling, and owner merge handoff. | PASS |

Post-design re-check: PASS. No constitution amendment is needed because the existing source, identity-integrity, accessibility, publication, site-consumption, and Spec Kit principles already govern this change.

## Project Structure

### Documentation for this feature

```text
specs/007-ownership-neutral-inputs/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── affiliation-and-publication.md
│   ├── authoritative-inputs.md
│   └── font-ingestion.md
├── checklists/
│   ├── requirements.md
│   └── integrity.md
└── tasks.md
```

### Source code

```text
assets/fonts/
brands/*/brand.json
scripts/
├── build_all.py
├── prepare_site.py
└── test_prepare_site.py
skill/
├── SKILL.md
├── references/
│   ├── canon.schema.json
│   └── *.md
└── templates/
    ├── brand_contract.py
    ├── validate_brand.py
    ├── analyze_inputs.py
    ├── ingest_font.py
    ├── build_kit.py
    ├── gen_*.py
    ├── build_specimen.py
    └── test_*.py
site/
└── generated and public output consumers
```

**Structure Decision**: Keep the current source-to-staged-kit architecture. Put one Python 3.8-compatible contract module beside the generators so validation, document output, framework bindings, site preparation, and tests consume the same normalized affiliation and typography decisions. Keep the machine-readable schema in the path already referenced by brand definitions.

## Technical Approach

1. Add `skill/references/canon.schema.json` using JSON Schema Draft 2020-12 for structural authoring support, then add `brand_contract.py` for cross-field, path, binary, and output rules that JSON Schema cannot express safely by itself.
2. Add `validate_brand.py` as the first build preflight. It rejects missing or contradictory affiliation, showcase, typography, authoritative-input, approval, path, hash, SVG safety, license, and font metadata before rendering.
3. Define explicit `affiliation` state for ownership, showcase, parent, inheritance, endorsement, and service credit. House inheritance retains ShruggieTech semantic orange; independent inheritance requires brand-specific emphasis and action colors. Derive all generated wording and semantic tokens through shared helpers, with no compatibility fallback.
4. Define `typography.mode` as `house` or `fixed`. House mode resolves the existing local family files explicitly. Fixed mode resolves declared local faces, validates fontTools metadata and hashes, and feeds the same role mapping into styles, bindings, documents, specimens, logo wordmarks, and enforcement.
5. Add an operator-only `ingest_font.py` command. Read a controlled local path or HTTPS source into bounded temporary storage, verify hash, license declaration, font metadata, and destination containment, then atomically place the approved file under `assets/fonts/`. Routine builds never invoke it.
6. Define authoritative supplied inputs by stable identifier and role. Validate byte hashes, unique roles, path containment, media facts, usage status, allowed transformations, and passive SVG restrictions. Preserve the original file and existing logo geometry verbatim.
7. Add deterministic palette analysis for raster pixels and passive SVG paint values. Emit ranked candidate evidence linked to the exact source hash, ignore transparent raster pixels, record limitations, and reject canonical palette linkage without a current explicit human approval.
8. Migrate all five production brands to explicit owned/public affiliation and house typography. Add authoritative raster source records and current palette approval evidence to ShruggieTech because it already uses supplied master artwork.
9. Update manifest, registry, guidelines, PDF, README, enforcement, specimen, site, and release paths to consume shared normalized values. Site preparation filters private brands instead of treating their presence in `dist/` as a publication error.
10. Add temporary third-party, supplied-image, and fixed-font tests, including prohibited-text scans, hash and path drift, stale palette approval, SVG active content, bad font metadata, destination escape, interrupted ingestion, and offline generation.
11. Update the skill interview and references so operators choose ownership, showcase, authoritative-input, palette-approval, and typography modes deliberately and without recording sensitive agreements.
12. Run analysis and the full documented validation, push the branch, open an official PR closing #104 and #105 only, process the automatic review round, request at most one explicit second Codex round, resolve every negative comment, and halt for the owner merge ritual.

## Issue Traceability

| Issue | Primary delivery area | Independent done signal |
| --- | --- | --- |
| #104 | Explicit affiliation and showcase contract, conditional output, public filter | A complete third-party kit has zero false ownership claims and private work is absent from public output |
| #105 | Supplied-input preservation, palette evidence and approval, fixed-font ingestion and use | Source hashes remain stable, unapproved colors fail, and a fixed-font kit completes offline with measured faces |
| #106 | Native platform icon suites | Explicitly excluded and remains open for S008 |

## Complexity Tracking

No constitution violations require justification.
