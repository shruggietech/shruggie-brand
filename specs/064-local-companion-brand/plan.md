# Implementation Plan: Local Companion Brand Kit and Public Showcase

**Branch**: `codex/064-local-companion-brand` | **Date**: 2026-09-28 | **Spec**: [spec.md](spec.md)

## Summary

Construct a new abstract Local Companion identity from the owner-selected calm-orbit direction, promote it after source-bound Gate 1 approval, assemble the complete kit for Gate 2 approval, then build, verify, release, and publish the kit through the ShruggieTech brand site. Retain the graphite and indigo identity, derive accessible light-surface roles, and keep chats, character imagery, model data, and unapproved screenshots out of public output.

## Technical Context

**Language/Version**: Python 3.8 minimum for kit generation; Node.js 20 minimum for the site. The current authoring host uses Python 3.12.9, while approved identity proofs and CI use Node.js 24.11.0.

**Primary Dependencies**: Repository `glyphkit`, `gen_logo.py`, `identity_continuity.py`, `validate_glyph.py`, `verify.py`, `build_all.py`, `prepare_site.py`; Coloraide, Pillow, fontTools, pikepdf, Playwright, Node resvg, and Next.js as declared by the repository.

**Storage**: Source JSON and Python under `brands/local-companion/`; shared licensed fonts under `assets/fonts/`; ignored private review material and generated output under `dist/`.

**Testing**: Source-bound continuity validation, glyph gate, full kit verification, production aggregate build, site tests, publication audits, and live artifact checksum inspection.

**Target Platform**: Portable brand kit and static official site; current development on Windows.

**Project Type**: Brand-system generator with a Next.js static export.

**Performance Goals**: Deterministic source bindings and successful aggregate CI; no runtime service or latency target.

**Constraints**: Two explicit owner creative gates, WCAG 2.1 AA floor, zero kit and glyph problems, generated output excluded from Git, UTF-8 without BOM and LF, non-interactive hidden console processes on Windows.

**Scale/Scope**: One product identity and kit, eight publication surfaces, the existing production-kit matrix, and a versioned public release.

## Constitution Check

| Principle | Design response | Status |
| --- | --- | --- |
| P1 Source and artifact boundary | Commit source only under `brands/` and site/skill changes; keep candidate and generated output in ignored `dist/`. | Pass |
| P2 Identity geometry | The owner rejected the LC monogram and selected a new abstract direction. Bind the exact new geometry to Gate 1 before promotion; preserve it afterward. | Gate 1 and corrected production binding approved, 32 proof hashes unchanged |
| P3 Accessibility | Measure dark and light roles at AA; correct failing values, including light-surface indigo. | Gate 2 cue pairs measured; Local Companion build reports zero problems |
| P4 Verification | Require zero glyph failures and zero `verify.py` problems for every production kit before release. | Pass: nine clean kits and required tag CI |
| P5 Site source | Project catalog, registry, images, and downloads from verified kit output through `prepare_site.py`. | Pass: live routes and exact hosted assets verified |
| P6 Specification and release | Keep this numbered slice current and publish from a versioned CI-built tag. | Pass: v2.8.0 published from merged main commit |

No constitutional exception is requested. Existing application files are source evidence only; this slice does not change the application repository.

## Phase 0: Research

Document canonical-source promotion, licensed font options, accessible palette roles, complete kit build, and release-to-Pages behavior in [research.md](research.md). Resolve site inventory and artifact naming from current repository code before implementation.

## Phase 1: Design and Contracts

Use [data-model.md](data-model.md) for approval states, governed source, derivatives, kit, and publication record. Document the public kit and site contract in `contracts/`. Use [quickstart.md](quickstart.md) for validation and expected evidence. Recheck P1 through P6 after these artifacts are written.

## Phase 2: Implementation Sequence

1. Complete the private Gate 1 candidate with exact Full and Reduced masters, hashes, palette qualification, renderer fingerprint, and 32 proofs. Record the owner decision before promotion.
2. Promote approved bytes under `brands/local-companion/` and finish brand source, guidance, color roles, licensed typography, and derivative configuration. Keep the canonical snapshot and source binding current.
3. Produce the private Gate 2 packet with lockups, colors, typography, interface cues, representative synthetic application, and a distinct social image with exact copy. Record approval before final compilation.
4. Add Local Companion to source-controlled site, release, test, and audit inventories. Update release metadata and migration notes.
5. Build all production kits, run documented verification, produce release assets, review changes, and publish a versioned release so Pages serves the approved kit. Verify the live route and archive checksum.

## Project Structure

```text
brands/local-companion/
├── brand.json
├── build/mk_paths.py
└── identity-continuity.json
specs/064-local-companion-brand/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
skill/templates/                 # generator and validation code if a source issue is found
site/                            # site source and tests
scripts/                         # publication inventory and audits
dist/                            # ignored approval candidates and generated artifacts
```

**Structure Decision**: Follow the existing source-only brand directory and kit-to-site projection architecture. The private `dist/` review packet is the approval surface until both gates are recorded.

## Post-Design Constitution Check

The design keeps public output dependent on verified generated kits, does not publish private review files, and requires owner-bound geometry and both approval gates. The approved Gate 2 packet and clean Local Companion build supply P3 and P4 evidence; full catalog, site, and release validation remain before publication.

## Post-Publication Constitution Check

On 2026-09-29, PR #301 merged as `8e7d688743d36c1bf692c1a7d55a7403545f3baf`. Tag `v2.8.0` completed required CI, release preflight, publication, and Pages deployment. The published Local Companion archive, social assets, registry, and guide were verified live against the approved hashes. P1 through P6 pass without an exception.
