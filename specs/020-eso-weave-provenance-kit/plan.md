# Implementation Plan: ESO Weave Provenance and Current-Spec Kit

**Branch**: `codex/020-eso-weave-provenance-kit` | **Date**: 2026-09-07 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/020-eso-weave-provenance-kit/spec.md`

## Summary

Deliver issue #153 as one approval-gated migration. Snapshot the synchronized ESO Weave default branch, acquire exact identity, font, reproduction, historical, rendered-reference, product-voice, and legal evidence, then model ESO Weave as a public independent third-party brand. Preserve the two supplied SVGs byte for byte. Before constructing any missing lockup or outlined wordmark, generate an ignored proof packet and stop for hash-bound owner approval. After approval, add the source kit, any narrowly required generator validation, a representative UI specimen, and complete generated output. Stop again with the finished guide and exact public surface set, then publish only after approval.

## Technical Context

**Language/Version**: Python 3.8 minimum for generators and validation; Node.js 20 minimum for site source; JSON, Markdown, SVG, CSS, and HTML source contracts

**Primary Dependencies**: Existing `fontTools`, Pillow, svgelements, coloraide, WeasyPrint, CairoSVG or native SVG renderer capability, Next.js App Router, and repository-owned brandbuilder templates

**Storage**: Source files under `brands/eso-weave/`, approved brand-local fonts under the existing asset contract, Spec Kit evidence under `specs/020-eso-weave-provenance-kit/`, and ignored generated output under `dist/` and site export directories

**Testing**: Python `unittest` suites, generator contract and pipeline tests, glyph and image validation, full multi-kit build, Markdown/hygiene checks, site lint/build/tests, hosted GitHub Actions

**Target Platform**: Offline-generated portable brand kit, static hosted brand portal, web/framework bindings, and web, Android, iOS, macOS, Windows, and compatibility icon consumers

**Project Type**: Source-driven Python generator plus statically exported Next.js documentation and registry site

**Performance Goals**: No new network dependency in routine generation; all six production kits complete within the existing hosted build envelope; generated portal navigation and downloads remain static

**Constraints**: Preserve authoritative SVG bytes and path data; WCAG 2.1 AA without waivers; fail closed on stale or missing approvals; no generated files committed; exact neutral credit only; current vendor disclaimer retained; two mandatory operator halts; Python 3.8 compatibility; UTF-8 without BOM and LF

**Scale/Scope**: One new production brand, 25 functional requirements, two supplied SVG masters, three fixed Inter faces plus OFL, 10 rendered references, historical S012 evidence, complete current kit layers, one site/registry integration

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

| Principle | Plan evidence | Result |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit only source inputs, brand definition, UI specimen source, tests, and Spec Kit evidence. Proof rasters, PDFs, kits, registries, and site exports stay ignored. | PASS |
| P2. Identity geometry is preserved | Copy both SVGs byte for byte, record hashes, prohibit normalization, and block derivative construction on the first owner approval. | PASS |
| P3. Accessibility has no exemption | Explicit independent semantic colors must pass measured AA. Any failing value changes before palette approval or publication. | PASS |
| P4. Verification precedes publication | Approval-aware preflight, glyph validation, `verify.py`, full build, site tests, CI, and affiliation/disclaimer scans precede publication. | PASS |
| P5. The site consumes generated kits | ESO Weave public pages will be created only by the existing verified `dist/` projection after the second approval. | PASS |
| P6. Specifications and releases move together | S020 specification, research, contracts, tasks, approval evidence, implementation, PR, and issue closure move together. No release is cut. | PASS |

### Post-Design Re-check

The design keeps both approvals as fail-closed source data, separates source acquisition from derivative construction, and separates verified private generation from public site eligibility. No constitution exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/020-eso-weave-provenance-kit/
├── checklists/
│   ├── provenance-identity.md
│   └── requirements.md
├── contracts/
│   ├── affiliation-and-disclaimer.md
│   ├── approvals-and-publication.md
│   └── source-provenance.md
├── data-model.md
├── evidence.md
├── plan.md
├── quickstart.md
├── research.md
├── source-inventory.json
├── spec.md
└── tasks.md
```

### Source Code (repository root)

```text
brands/eso-weave/
├── assets/
│   ├── fonts/
│   ├── reference/
│   └── source/
├── ui_kits/eso-weave-desktop/
├── brand.json
├── NOTES.md
├── README.md
└── SKILL.md

skill/templates/
├── brand_contract.py
├── test_brand_contract.py
├── test_pipeline.py
└── existing generation and verification templates

scripts/
├── build_all.py
├── prepare_site.py
├── test_prepare_site.py
└── existing repository validation

site/
├── app/
├── components/
├── generated/
└── public/
```

**Structure Decision**: Reuse the current source-to-`dist/` architecture. Keep ESO Weave evidence inside its source brand directory when needed by generation, keep approval and audit evidence in S020 artifacts, and make site publication a derived projection of a verified public-showcase contract. Do not introduce a second publishing path or modify the upstream ESO Weave repository.

## Delivery Sequence

1. Synchronize both repositories and freeze the upstream snapshot.
2. Acquire exact source inputs, classify them, verify current hashes and font metadata, and create the source inventory.
3. Add negative tests for third-party affiliation, vendor-boundary enforcement, source drift, approval staleness, and publication gating before implementation.
4. Produce the ignored first-gate proof packet from authoritative sources without adding production derivative masters.
5. **Owner Gate 1**: approve, reject, or amend the hash-bound derivative set, palette, and any additional typography proposal.
6. After approval, construct only the approved derivatives through source-driven generation, complete the brand definition and UI specimen, then run the full local gate.
7. Produce the ignored second-gate packet containing the final guide, specimen, derivative sheet, manifests, verification results, and exact public surfaces.
8. **Owner Gate 2**: approve, reject, or amend publication.
9. After approval, enable generated site/registry publication, re-run full validation, commit, push, open the official PR, reconcile CI and no more than two Codex review rounds, then return for owner merge review.

## Complexity Tracking

No constitution violation requires justification. The two-stage approval model is required by identity preservation and publication safety, not additional architecture.

## Execution Adjustment

On 2026-09-07, T005 through T009 were deferred until after Gate 1. The source inventory and non-production proof packet do not require production approval-schema changes, and implementing those changes before the owner accepts the proposed derivative, palette, and mono-font contract would create speculative code. This explicitly changes task execution order without changing scope: acquisition and Gate 1 evidence complete first, then the approved data shape drives the fail-closed implementation.
