# Implementation Plan: DanceWithMe865 Brand Restart

**Branch**: `codex/065-dancewithme865-restart` | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

## Summary

Rebuild S065 from the owner-provided Natalie image. Audit the supplied SVGs as candidate authoritative artwork, preserve selected source bytes, and use the repository's existing schema and generator to build a complete independent client brand. Recreate Gate 1 and Gate 2 approval evidence from this new source. Final kit generation and website registration follow both approvals and full validation.

## Technical Context

**Language/Version**: Python 3.8 minimum for the generator; Node.js 20 minimum for the site.
**Primary Dependencies**: Existing BrandBuilder Python templates, passive SVG input validation, Pillow and the production SVG rasterizer; existing Next.js App Router site.
**Storage**: Versioned source in `brands/`, approved shared fonts in `assets/fonts/`, ignored private review output and generated kits in `dist/`.
**Testing**: Brand contract and continuity validation, 32 production source proofs, `validate_glyph.py`, `verify.py`, aggregate `scripts/build_all.py`, site lint/build/test, repository hygiene.
**Target Platform**: Static company brand website and portable generated brand kits.
**Project Type**: Source-driven brand kit generator and static site.
**Performance Goals**: No new runtime path; build remains within existing CI timeouts.
**Constraints**: Byte-identical authoritative geometry, WCAG 2.1 AA, two explicit creative approvals, source-only Git, LF UTF-8 text.
**Scale/Scope**: One independent client brand, its required standard outputs, and the site registry entry. Add general supplied Reduced colorway and standalone wordmark bindings because the current generator cannot preserve those supplied sources across the required outputs. Preserve approved proof settings for unaffected brands through an exact, guarded legacy generator fingerprint and mandatory pixel-hash comparison.

## Constitution Check

| Principle | Design response | Status |
| --- | --- | --- |
| P1 sources only | Commit brand definitions and reviewed source assets; keep all proofs and generated exports in ignored `dist/`. | Pass |
| P2 geometry preserved | Bind selected SVG bytes and preserve path data; source changes require a new Gate 1 candidate. | Pass |
| P3 AA floor | Qualify formal palette and every declared text or fill pair before approval and publication. | Pass |
| P4 verification | Require zero production verifier and glyph failures before calling the kit shippable. | Pass |
| P5 generated site | Register generated kit data; do not hand-code a separate identity on the site. | Pass |
| P6 Spec Kit | Keep S065 spec, plan, tasks, analysis, evidence, and implementation synchronized. | Pass |

## Phase 0: Research Decisions

See [research.md](research.md). The supplied archive is a source candidate, not an output template. The pictured light stacked treatment is the visual target. Existing source validators and production renderer provide the approval proof path. Unverified copy and source rights claims from the ZIP do not become public assertions.

## Phase 1: Design and Contracts

See [data-model.md](data-model.md), [contracts/identity-and-delivery.md](contracts/identity-and-delivery.md), and [quickstart.md](quickstart.md). The new source uses `brands/dancewithme865/brand.json`, `brands/dancewithme865/identity-continuity.json`, and reviewed source assets under `brands/dancewithme865/assets/source/`. General input binding fixes stay in `skill/templates/` with regression checks. The generated kit remains in `dist/`; the site reads only verified generated inventory.

## Project Structure

```text
specs/065-dancewithme865-brand/
  spec.md
  plan.md
  research.md
  data-model.md
  quickstart.md
  tasks.md
  evidence.md
  contracts/identity-and-delivery.md
  checklists/
brands/dancewithme865/
  brand.json
  identity-continuity.json
  assets/source/
skill/templates/brand_contract.py
skill/templates/gen_logo.py
site/
scripts/build_all.py
dist/  (ignored review and generated output)
```

**Structure Decision**: Use the standard brand source and generated delivery paths. Do not import the ZIP directory tree or its `brand.json` as the repository contract.

## Approval and Delivery Sequence

1. Audit image, archive artwork, SVG safety, provenance, and palette; prepare exact Full and Reduced production candidates and the complete 32-proof comparison matrix.
2. Stop for a new Gate 1 decision on that exact source-bound packet. Prior approvals are void for this branch.
3. Promote approved source bytes; assemble standard derivatives, typography, separate social share composition, and website examples in a private Gate 2 packet.
4. Stop for a new Gate 2 decision. Return to Gate 1 if any master source changes.
5. Compile and verify the final kit, register the verified brand in the site, run the full validation, and commit sources. Follow the skill's pre-push halt unless the owner gives a later explicit push instruction.

## Post-Design Constitution Check

The proposed layout uses only governed source directories and the existing kit contract. No exception to P1-P6 is required. Approval and verification dependencies remain explicit rather than assumed complete.
