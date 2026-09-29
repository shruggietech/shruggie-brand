# Implementation Plan: Scruggs Tire & Alignment Client Brand

**Branch**: `codex/066-scruggs-tire-brand` | **Date**: 2026-09-28 | **Spec**: [spec.md](spec.md)

## Summary

Create a source-bound independent client brand using the existing brand contract and complete generator output. Prepare exact Full and Reduced mark candidates and obtain Gate 1 approval, then assemble accessible provisional fundamentals and obtain Gate 2 approval. Only then compile and verify the complete production kit and project it to the official site through the existing generated-kit path. The supplied archive is evidence, not the output model.

## Technical Context

**Language/Version**: Python 3.8 minimum brand generator; Node.js 20 minimum static site.
**Primary Dependencies**: Existing `skill/references/canon.schema.json`, brand authoring/continuity tools, `scripts/build_all.py`, and the Next.js site projection.
**Storage**: Committed source under `brands/scruggs-tire-alignment/`, existing licensed fonts in `assets/fonts/` or controlled licensed ingestion; provisional and generated output under ignored `dist/`.
**Testing**: Source/schema and approval-ledger checks, 32 Gate 1 proofs, Gate 2 packet/contrast review, `verify.py`, `validate_glyph.py`, full documented `scripts/build_all.py`, site build/publication audit, and repository hygiene.
**Target Platform**: Standard generated brand kit and official static brand website.
**Project Type**: New production brand source plus generated site projection. No new schema or client-site implementation.
**Performance Goals**: Existing build and site budgets; no new runtime remote font dependency.
**Constraints**: Byte-preserved approved geometry, WCAG 2.1 AA, exact creative approvals, third-party ownership, UTF-8/LF source, and no committed generated output.
**Scale/Scope**: One client brand; full current kit inventory and eight governed public site surface categories.

## Constitution Check

| Principle | Planned response |
| --- | --- |
| P1 sources and artifacts | Commit only brand source and Spec Kit evidence; build all delivery artifacts in ignored output. |
| P2 identity geometry | Gate 1 fixes exact source bytes or construction helper; later changes require comparison and renewed approval. |
| P3 accessibility | Qualify every declared role at rendered size, including bright red and gray pairings; no waiver. |
| P4 verification | Run zero-problem kit and glyph gates and the documented aggregate before merge readiness. |
| P5 generated site authority | Site takes guideline, registry, logo, favicon, specimen, and download values from verified `dist/`. |
| P6 Spec Kit and release | Keep spec, plan, tasks, analysis, approval evidence, and implementation aligned; release/deploy is separate. |

No constitutional exception is proposed. Rechecked after research and design.

## Delivery order and creative stops

1. Record the exact source inventory, inspect format/topology and current-site presentation, and prepare a working brief with explicit facts, proposals, and unresolved choices.
2. Build actual Full and Reduced production candidates and the 32-proof Gate 1 matrix. Stop for explicit source-bound owner decision. Do not set an approval ledger to approved from archive prose or this plan.
3. After Gate 1, promote exact approved sources into `brands/scruggs-tire-alignment/` and assemble provisional typography, palettes, lockups, icons, copy, and applications. Keep all review derivatives private and ignored.
4. Build the Gate 2 packet, including a separate social share image with exact approved copy, measured contrast, derivative manifest, and source lineage. Stop for explicit owner decision.
5. After Gate 2, complete `brand.json`, continuity and asset records, then build and verify the entire current kit. Resolve any generator defect in `skill/templates/` rather than patching output.
6. Audit all eight website surfaces from generated output, run the full documented aggregate and repository hygiene checks, record evidence, commit the implementation, and prepare the isolated PR. Push and release remain explicit later actions.

## Project Structure

```text
specs/066-scruggs-tire-brand/             # Spec, research, contract, tasks, and verification evidence
brands/scruggs-tire-alignment/             # Approved brand.json, continuity, source artwork, and human guidance
assets/fonts/                              # Existing or controlled licensed fixed-face sources, only if needed
skill/templates/                           # Generator changes only if a demonstrated contract gap exists
site/                                      # Existing projection path; edit only if a demonstrated gap exists
dist/                                      # Ignored provisional packets and generated kits
```

**Structure Decision**: Reuse the repository's current source and generator schema. ZIP paths and old-site contents never become a parallel kit format.

## 2026-09-29 source candidate decision, r1 superseded

The first source proposal used authoritative passive SVG sources that embed the current Full image and Reduced favicon without changing their supplied pixels. It added a white plate to the Full source so black wording would appear on dark surfaces. The Reduced mark was selected below 128 pixels because the Full wordmark is unreadable in the 64-pixel and smaller proofs. A newly constructed vector identity was considered and declined because it would reinterpret the supplied geometry. The owner requested a surgical revision to the Full variants before approving a production binding.

## 2026-09-29 source candidate revision, r2

The [current Gate 1 review](gate1-review.md) binds the already-transparent Full PNG to a clear square master, a true white square with black wording, and a true black square with white wording. The black-to-white wording transform uses the original pixel alpha through a passive SVG filter, preserving the supplied red tire pixels and all letter contours. The tire-only Reduced source and its 16 proof hashes remain unchanged. Existing `full_colourway_input_ids` supply the two contextual Full variants without changing schemas or generator code. This revision is still a candidate pending the exact Gate 1 owner decision.

## Downstream verification

`quickstart.md` names the existing build flow and approval stops. A planning-only commit can be checked for specification quality, formatting, and repository hygiene. It cannot claim production kit, glyph, or hosted publication results before approved source and implementation exist.
