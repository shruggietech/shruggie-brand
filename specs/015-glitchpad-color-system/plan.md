# Implementation Plan: Glitchpad Identity Color Approval

**Branch**: `codex/015-glitchpad-color-system` | **Date**: 2026-09-07 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/015-glitchpad-color-system/spec.md`

## Summary

Resolve #146 through a two-stage identity workflow. Stage A generates a byte-identical-geometry comparison of three explicit color systems, measures every relevant surface relationship, and halts for owner approval. Stage B begins only after that approval, promotes the selected matrix into Glitchpad source and proportional shared generator contracts, rebuilds all five production kits, verifies every output family, and publishes through the standard reviewed pull-request workflow.

## Technical Context

**Language/Version**: Python 3.8 minimum for generator and comparison tooling; Node.js 20 minimum for the static site

**Primary Dependencies**: Existing brandbuilder templates, svgelements, Pillow, ColorAide, CairoSVG or installed SVG renderer fallback, Next.js App Router, Playwright

**Storage**: Committed JSON and Python source plus Spec Kit Markdown; generated comparison, kits, PDFs, raster exports, screenshots, registries, and site exports remain ignored

**Testing**: Python `unittest`, protected path hashes, contrast re-derivation, visible-alpha measurements, generated SVG inspection, five-kit build, `verify.py`, `validate_glyph.py`, TypeScript, static export, Playwright, WCAG 2.1 AA audit, Markdown and repository hygiene

**Target Platform**: Portable brand kits, desktop application assets, Android launcher/adaptive/store assets, web, Apple, Windows, static guidelines, and brand.shruggie.tech

**Project Type**: Source-driven brand asset generator and static documentation site

**Performance Goals**: Generate the complete comparison locally in one command; retain existing production build duration and artifact counts within normal variance

**Constraints**: Owner approval before promotion; canonical page paths unchanged and safely enclosed in a permanent square; rejected muddy deep gold prohibited; WCAG 2.1 AA non-exemptable; Python 3.8 compatibility; no generated artifacts in Git; project child processes hidden and non-interactive

**Scale/Scope**: One Glitchpad identity, three candidate systems, two presentation themes, five production kits, all declared Glitchpad output families, and no sibling redesign

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Result |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit only the study source, brand source, shared templates, tests, and Spec Kit evidence; generate candidate and production artifacts in ignored paths. | PASS |
| P2. Identity geometry is preserved | Hash protected page path strings, compare every direction using one identical safe square composition, and require explicit owner approval before production changes. | PASS |
| P3. Accessibility has no exemption | Measure each fill against intended surfaces and adjacent fills; reject any approved mapping that fails the applicable floor. | PASS |
| P4. Verification precedes publication | Rebuild and verify all production kits only after approval; pre-approval output is clearly exploratory and ineligible for publication. | PASS |
| P5. The site consumes generated kits | Any eventual site result continues to consume rebuilt Glitchpad output and generated metadata rather than restated identity values. | PASS |
| P6. Specifications and releases move together | S015 specification, plan, tasks, analysis, decision evidence, implementation, verification, and changelog remain synchronized. | PASS |

Post-design re-check: PASS. The explicit decision gate is required by P2 and does not waive any later production gate.

## Delivery Stages

### Stage A: Decision evidence

1. Preserve current source hashes and capture the current identity baseline.
2. Implement a non-publishing study generator that accepts only the three revised square-based candidate matrices, reuses protected page geometry, verifies protected hashes, rejects prohibited color values, and writes ignored HTML/SVG/JSON evidence.
3. Render identical dark, light, small-size, lockup, launcher, and store contexts for all directions.
4. Record contrast and visual dispositions, present the recommended system and tradeoffs, then halt for owner approval.

### Owner approval gate

The owner may approve a named direction, request a bounded value or role adjustment, or reject the set. No exploratory color enters `brands/glitchpad/brand.json`, shared production templates, generated public kits, or site source before this disposition is recorded.

### Stage B: Approved implementation

1. Encode the approved dark, light, permanent square, square-edge, page, fold, reduced, monochrome, and wordmark roles in Glitchpad source.
2. Add optional shared wordmark-role configuration only if the approved matrix cannot be represented by the existing contract; preserve the absent behavior for all sibling brands.
3. Replace obsolete Glitchpad prohibitions, guide prose, assumptions, measured values, tests, and changelog decisions.
4. Rebuild and classify every output family, run the complete gate, publish the pull request, process no more review rounds than the owner authorizes, and halt before merge.

## Architecture Decisions

- Treat color exploration as generated decision evidence, never as a temporary production source mutation. This prevents an unapproved identity from leaking into kits or public output.
- Use one complete matrix per direction rather than isolated swatches. Permanent square, square edge, paper, fold, wordmark, reduced mark, and monochrome roles must be judged as a system across dark and light contexts.
- Treat the square as part of every glyph composition, never an optional platform plate. Use a 1000 by 1000 study canvas with the square inset on all sides and the byte-identical rectangular page uniformly centered inside it.
- Compare sulfur placement directly: sulfur square, sulfur page inside charcoal square, and sulfur fold inside slate square.
- Promote the owner-approved contextual mix: Sulfur Square in dark mode and Charcoal Square in light mode. This preserves sulfur prominence while the charcoal square supplies the required light-surface boundary without a muddy yellow substitute.
- Preserve explicit dark and light edge roles where the square fill itself does not distinguish from the presentation surface.
- Make any required wordmark role a validated optional shared configuration. A Glitchpad-only generator condition or patched SVG would violate source authority and sibling stability.

## Project Structure

### Documentation

```text
specs/015-glitchpad-color-system/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── candidate-matrix.md
│   └── approval-gate.md
└── checklists/
    ├── requirements.md
    └── identity-decision.md
```

### Source and generated evidence

```text
brands/glitchpad/brand.json             # approved source change after gate
scripts/glitchpad_color_study.py         # deterministic non-publishing comparison
skill/references/canon.schema.json       # optional shared role schema if required
skill/templates/brand_contract.py        # validation if required
skill/templates/gen_logo.py              # shared generation behavior if required
skill/templates/test_brand_contract.py   # role validation regression
skill/templates/test_pipeline.py         # generated identity regression
dist/.s015-color-study/                   # ignored generated comparison evidence
```

**Structure Decision**: Keep authoritative identity values in Glitchpad brand source, shared behavior in templates, and the reproducible comparison tool in `scripts/`. Store generated decision boards and measurements under ignored `dist/` so they can be inspected without crossing the source/artifact boundary.
