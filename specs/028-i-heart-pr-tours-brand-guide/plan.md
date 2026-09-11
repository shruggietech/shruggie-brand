# Implementation Plan: Identity-Locked I Heart PR Tours Brand Guide

**Branch**: `codex/028-i-heart-pr-tours-brand-guide` | **Date**: 2026-09-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/028-i-heart-pr-tours-brand-guide/spec.md`

## Summary

Deliver issue #188 as a two-gate authoritative-source ingestion. Privately inventory the supplied guide and exact logo-package files, resolve role authority, font identity, palette use, transformations, affiliation, and publication at Gate 1, then promote approved bytes through S027 continuity without reconstruction. Gate 2 candidate `iheartpr-g2-r1` was rejected on 2026-09-11, so the plan returns to Gate 1 with exact revised copy, a live-site and brochure-grounded palette, a light-first white-paper guide, a governed single-ink transform, supplied sandy expressions, and live-verified colored-heart favicon and app-icon authority. Generate a revised private kit, guide, comparisons, and validation only after `iheartpr-g1-r4` approval. Candidate `iheartpr-g2-r2` then received a focused typography revision, and candidate `iheartpr-g2-r3` exposed remaining footer, cover metadata, shorthand, and preview-surface corrections. Candidate `iheartpr-g2-r4` reserves Courier Prime for literal code blocks, uses the supplied body family for every other small-text role, records `IHPRT` shorthand, and binds source assets to correct preview surfaces. Only after approval of candidate `iheartpr-g2-r4` may the already-authorized branch and pull-request workflow proceed.

## Technical Context

**Language/Version**: Python 3.8 minimum and 3.12 CI; Node.js 20 minimum and 24 CI; JSON Schema Draft 2020-12; Markdown; CSS/TypeScript where generated and site contracts apply

**Primary Dependencies**: Existing Pillow, ColorAide, fontTools, PyMuPDF/Poppler inspection capability, svgelements, CairoSVG/native SVG renderer chain, pikepdf, Next.js static site, and S027 identity-continuity promotion and proof machinery

**Storage**: Governed source files under `brands/i-heart-pr-tours/` after Gate 1; approved redistributable shared fonts under `assets/fonts/`; committed Spec Kit records under this feature directory; private intake inventories and generated gate packets under ignored `dist/i-heart-pr-tours/`

**Testing**: Repository Python unittest suites, brand-contract and identity-continuity regressions, aggregate production builds, PDF/image QC, Markdown policy, static-site type/build/browser tests, and WCAG 2.1 AA checks

**Target Platform**: Cross-platform source contract and generated static brand kit, with GitHub Actions Linux parity and local Windows-safe tooling

**Project Type**: Source-governed brand generator, verification CLI, generated documentation kit, and optional static-site consumer

**Performance Goals**: Add the eighth production kit without increasing aggregate CI beyond the current all-brand baseline plus 120 seconds; complete continuity preflight before any derivative write

**Constraints**: Exact source-byte preservation; no tracing or live-type logo reconstruction; approved deterministic single-ink derivation only; light-first white-paper guide; WCAG 2.1 AA without waivers; two owner halts; no private intake paths in committed files; no generated outputs committed; Python 3.8 compatibility; UTF-8 without BOM and LF; no public publication without Gate 2

**Scale/Scope**: One independent third-party customer identity, at least three documented logo roles, eight declared colors, two guide typography roles plus one ambiguous generation label, one private generated kit, and one bounded pull-request review cycle

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **P1 Sources and artifacts**: PASS. Only approved source bytes, metadata, tests, and specifications may be committed. Intake reviews, contact sheets, PDFs, PNG exports, archives, and site exports remain ignored.
- **P2 Geometry preservation**: PASS. The plan forbids extraction, tracing, retyping, normalization, cropping, or reframing as silent production authority. Revised Gate 1 must bind the exact supplied sources and the narrow single-ink alpha-mask and recolor transform before regeneration.
- **P3 Accessibility**: PASS. All semantic roles require measured AA. Fixed failing brand colors remain unchanged and are constrained to suitable uses.
- **P4 Verification**: PASS. Both source preflight and final kit require fail-closed continuity, zero verifier problems, zero applicable glyph failures, and full CI parity.
- **P5 Site consumption**: PASS. The brand is not discoverable until Gate 2 explicitly approves hosted publication; any approved site surface consumes verified generated output.
- **P6 Spec Kit and releases**: PASS. S028 follows specify, clarify, checklist, plan, tasks, analyze, implement, verify, commit, authorized push, bounded review, and owner merge. No release, tag, or deployment is authorized.

**Post-design recheck**: PASS. The contracts separate private intake from committed source, distinguish PDF reference art from permitted authoritative inputs, model both owner gates as exact state transitions, and keep unavailable variants blocked instead of inventing them.

## Project Structure

### Documentation (this feature)

```text
specs/028-i-heart-pr-tours-brand-guide/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
brands/i-heart-pr-tours/             # Created only after Gate 1
├── brand.json
├── identity-continuity.json
├── README.md
├── assets/                          # Exact approved supplied sources only
└── fixtures/                        # Representative product UI content, not identity masters

assets/fonts/
├── ttf/                             # Approved OFL binaries only
├── woff2/
└── licenses/

skill/templates/
├── brand_contract.py                # Narrow contract changes only if required
├── identity_continuity.py           # Existing S027 gate
├── gen_logo.py
├── verify.py
├── test_brand_contract.py
├── test_identity_continuity.py
└── test_pipeline.py

scripts/
├── build_all.py
├── export_approved_identity_proofs.py
├── prepare_site.py
└── test_prepare_site.py

dist/i-heart-pr-tours/               # Ignored private intake and gate packets
├── gate-1/
└── gate-2/
```

**Structure Decision**: Reuse the existing source-first brand directory and authoritative-input contract. Do not create production files before Gate 1. Prefer current S027/S016 capabilities; change shared generator code only if exact approved lockup assets expose a fidelity gap that cannot be represented without reconstruction.

**Hosted proof decision**: The approved Windows host remains the canonical exact-render authority. Hosted Windows CI must regenerate the 32-proof matrix and Gate 2 derivative manifest with the bound Node 24.11.0 and resvg 2.6.2 stack, reject any hash drift, and publish that ephemeral evidence only as a workflow artifact. Linux CI must hash-bind the proofs and manifest to their approved records before applying the existing cross-renderer topology, edge-band, bounds, centroid, and color comparisons. Color uses the non-edge interior when present and the shared silhouette when a tiny proof has no interior core. Renderer-specific PNG encoding inside otherwise identical SVG wrappers is normalized only by decoded RGBA dimensions and pixels, while all surrounding SVG bytes and derivative paths remain exact. Thresholds remain unchanged. No generated proof raster or derivative is committed.

## Delivery Sequence and Halt Gates

1. Complete the private intake inventory and inspect only explicitly in-scope sources.
2. Generate review-only contact sheets and measurement evidence under ignored `dist/` without promoting or reconstructing artwork.
3. **Owner Gate 1**: approve exact source hashes, role authority, font contract, copy, palette, light surface mode, transformations, sandy-expression scope, affiliation, privacy, service credit, publication classification, and intentional wordmark-only omission. Approval is never inferred.
4. After approval, add negative tests, promote exact source bytes, create the approved brand contract and canonical continuity record, and generate the private kit.
5. Run source equality, derivative traceability, accessibility, kit, site-boundary, and repository-wide validation.
6. **Owner Gate 2**: approve the complete guide, artifacts, evidence, and exact public surfaces. Any affected source or transformation change returns to Gate 1.
7. After approval, commit, push under the existing authorization, open the official pull request, process every comment, optionally request one second Codex round, and halt at owner merge.

The first execution reached step 6 with `iheartpr-g2-r1`. The owner rejected that candidate and changed copy, palette, surface mode, monochrome transformation scope, and guide sections. Live favicon verification then added exact per-size colored-heart source authority. Execution therefore returns to step 3 with `iheartpr-g1-r4`. Issues #193 and #194 preserve the reusable generator and cross-brand findings for later slices.

## Complexity Tracking

No constitutional violation or new subsystem is planned.
