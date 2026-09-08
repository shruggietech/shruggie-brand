# Implementation Plan: Asset Delivery Fidelity

**Branch**: `codex/021-asset-delivery-fidelity` | **Date**: 2026-09-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/021-asset-delivery-fidelity/spec.md`

## Summary

Resolve #166 and #165 as one fidelity boundary. Correct the shared square-knockout mask so its coordinate region is explicit and remains complete when the mark is nested inside horizontal or stacked lockups. Extend logo verification and regressions to reject a clipped or component-deficient monochrome mark in both SVG and rendered PNG output. Replace the loose asset-preview sizing rules with one bounded media viewport used by asset-library cards and guideline logo examples, then measure centering and containment in the production browser sweep without changing canonical source assets or presentation-only delivery bytes.

## Technical Context

**Language/Version**: Python 3.8 minimum for generation and verification; Node.js 20 minimum for site source; TypeScript, CSS, SVG, JSON, and Markdown contracts

**Primary Dependencies**: Existing Pillow, CairoSVG or native SVG raster capability, svgelements, Next.js App Router, Fumadocs, Playwright, and axe-core verification

**Storage**: Source brand contracts under `brands/`, generator and verifier templates under `skill/templates/`, site source under `site/`, Spec Kit artifacts under `specs/021-asset-delivery-fidelity/`, and ignored generated output under `dist/` and site export directories

**Testing**: Python `unittest` suites, generated SVG structure assertions, rendered raster measurements, full multi-kit build, Markdown and hygiene checks, site type-check/static build, Playwright layout and WCAG audit, hosted GitHub Actions

**Target Platform**: Generated portable brand kits and the statically exported public brand-guideline site across desktop, tablet, mobile, light theme, and dark theme

**Project Type**: Source-driven Python generator plus statically exported Next.js documentation and registry site

**Performance Goals**: Keep all six production kits and the 76-page static site within the existing CI build envelope; add only bounded per-asset layout measurements on asset routes

**Constraints**: Preserve Glitchpad source path bytes; do not redraw or normalize geometry; no CSS filters or per-brand offsets; WCAG 2.1 AA without waiver; Python 3.8 compatibility; generated files remain ignored; UTF-8 without BOM and LF

**Scale/Scope**: Two GitHub issues, one shared SVG mask defect, black and white full horizontal and stacked lockups plus their raster deliveries, all production asset-library cards and logo examples, six brands, two themes, three responsive viewport classes

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

| Principle | Plan evidence | Result |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit only generator, verifier, site, test, and Spec Kit source. Rebuild kits, rasters, PDFs, and static exports under ignored paths. | PASS |
| P2. Identity geometry is preserved | Freeze and hash-check Glitchpad's existing full and reduced paths. Repair mask bounds and output composition without editing canonical geometry. | PASS |
| P3. Accessibility has no exemption | Retain the complete WCAG 2.1 AA route sweep in both themes and responsive widths. | PASS |
| P4. Verification precedes publication | Add failing structural, rendered-asset, and browser-layout regressions before production changes, then run every documented gate. | PASS |
| P5. The site consumes generated kits | Continue using generated portal preview URLs and exact deliveries. Change only shared presentation components and styles. | PASS |
| P6. Specifications and releases move together | S021 specification, design, tasks, implementation, evidence, PR traceability, and issue closure move together. No release is cut. | PASS |

### Post-Design Re-check

The design repairs a coordinate-boundary defect in the existing generator, adds measured validation rather than byte comparisons, and keeps site content derived from verified kit manifests. No source geometry, palette, brand rule, or publication architecture changes. No constitution exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/021-asset-delivery-fidelity/
├── checklists/
│   ├── asset-fidelity.md
│   └── requirements.md
├── contracts/
│   ├── asset-preview-layout.md
│   └── monochrome-lockup-integrity.md
├── data-model.md
├── evidence.md
├── plan.md
├── quickstart.md
├── research.md
├── spec.md
└── tasks.md
```

### Source Code (repository root)

```text
brands/glitchpad/
└── brand.json                         # frozen identity source contract

skill/templates/
├── gen_logo.py                       # explicit square-knockout coordinate region
├── verify.py                         # structural and rendered lockup integrity gate
└── test_pipeline.py                  # isolated generator regressions

site/
├── app/globals.css                   # shared bounded preview viewport
├── components/guidelines/
│   ├── asset-library-client.tsx      # exact-delivery media wrapper
│   └── topic-content.tsx             # shared logo-example media wrapper
├── scripts/verify-site.mjs           # measured centering and containment
└── tests/site.test.mjs               # static contract coverage
```

**Structure Decision**: Reuse the existing generator, provenance verifier, manifest-derived portal, and site verification architecture. The generator owns SVG coordinate correctness, the verifier owns delivery integrity, and the site owns only bounded presentation. Do not introduce brand-specific rendering paths or duplicate asset metadata in site source.

## Delivery Sequence

1. Freeze the current Glitchpad source geometry hashes and capture the failing black and white lockup measurements.
2. Add generator regressions proving that implicit mask regions clip nested monochrome marks and that explicit local mask bounds preserve their full height.
3. Add verifier regressions for missing mask coverage, component loss, and SVG-to-PNG disagreement.
4. Correct the shared square-knockout mask region without changing path data, lockup proportions, or monochrome role policy.
5. Add static and browser regressions for one shared asset-preview media boundary across both guideline surfaces.
6. Implement the shared bounded viewport and exact-delivery wrappers, retaining existing themes and asset metadata.
7. Rebuild all production kits, run the full CI-parity matrix, inspect the affected Glitchpad lockups and representative asset pages, and record evidence.
8. Commit, push, open a PR closing #166 and #165, reconcile CI and no more than two Codex review rounds, then return for owner merge review.

## Complexity Tracking

No constitution violation requires justification. The slice deliberately spans generator and site presentation because the two issues share the same asset-fidelity acceptance boundary and validation run.
