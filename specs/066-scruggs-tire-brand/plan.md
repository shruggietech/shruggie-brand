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

The [Gate 1 review](gate1-review.md) binds the already-transparent Full PNG to a clear square master, a true white square with black wording, and a true black square with white wording. The black-to-white wording transform uses the original pixel alpha through a passive SVG filter, preserving the supplied red tire pixels and all letter contours. The tire-only Reduced source and its 16 proof hashes remain unchanged. Existing `full_colourway_input_ids` supply the two contextual Full variants without changing schemas or generator code. Revision r2 was the reviewed visual direction.

## 2026-09-29 Gate 1 approval and source promotion, r3

Revision r3 binds native-canvas horizontal sources and licensed guide typography to the same visual artwork. The four reviewed source hashes and all 32 production proof hashes match r2. The owner selected "Approve complete record" for packet digest `d8fa645bc4b68e79185f30307ea360e403ad1e4720f414d10dce6d0bcbff832f`. The canonical record validates, and `promote_identity.py` installed the exact seven approved SVG sources and brand files in `brands/scruggs-tire-alignment/`. Gate 2 remains pending.

## 2026-09-29 dark palette correction and approval, r4

A private full-kit preview found AA failures with bright red and immutable fault red against the r3 `#222222` dark base, and deep red dark emphasis was unreadable there. The corrected r4 packet keeps all seven SVG logo source hashes unchanged, switches the dark base to true black, and uses existing tire red for dark emphasis. The owner selected "Approve corrected palette" for exact packet digest `3f9a932c157e3b69b8df453d59f0447f1320d5437e911712fd1e6a56efa55206`. The revised canonical source was promoted after validation. The private kit rebuild with generator repairs completed with zero verification, affiliation, image, and PDF problems; Gate 2 remains pending.

## Downstream verification

`quickstart.md` names the existing build flow and approval stops. The approved Gate 1 source produced a clean private kit preview, with exact commands and observations in [verification.md](verification.md). Final aggregate and site publication checks depend on Gate 2 approval; the private preview is not a hosted result.

## 2026-09-29 owner supplied social copy and CI renderer routing

The owner supplied `Expert alignments, tire repair, and honest automotive service.` and explicitly omitted the description. The generator accepts optional exact `slogan_lines` and fits the two lines inside the logo's visible width without altering the 32-image identity proof stage. A proof-relevant semantic fingerprint excludes only this social-copy branch while still invalidating any proof-stage edit. The private Gate 2 packet is validated and the one assembled image is awaiting the owner's visual decision.

The approved Scruggs proof renderer is Node 26.5.0, while existing CI kits are pinned to Node 24.11.0. Local Node 24 replay reproduced all 32 approved Scruggs proof hashes, but the exact approved renderer contract still requires Node 26.5.0. CI now exports Scruggs proofs and builds its kit with Node 26.5.0, and retains Node 24.11.0 for existing kit builds. This preserves both exact approval contracts without changing the owner's approved record.

The first assembled image used the display bold face at 60 px. The owner asked to reduce its text size and weight. The revised candidate uses the licensed Source Sans 3 semibold face at 54 px and caps the visible two-line width at 82% of the logo width. Its measured tagline width is 464 px beneath a 552 px logo. The revised packet supersedes the first Gate 2 candidate and is awaiting the owner's decision.

## 2026-09-29 Gate 2 approval and production validation

The owner selected "Approve revised image" for packet `4ff5f087267495989ca5984a0a5660549666d8cbc8819e3c683e02073e9943cb`. The source ledger binds social SVG `84ffb71053750c7eef792e804e9a06d63bc0274ab57dae30f8f1ee792a400969`, PNG `8f0d4f81e6fe76b43dc11d0535101e8221acb667962fc7c4a010748c82aa1dfb`, and the complete derivative manifest. The Gate 1 source binding remains unchanged. The Scruggs kit builds clean, and the separate Node 24 aggregate build reports eight clean existing kits. Site preparation now includes all nine.

The first complete site run exposed fixed eight-brand test counts and a fixed-height card that clipped the longer client title. The page now lets cards grow from a 20rem minimum and tests count the generated brand inventory. A second verifier run also changed the checksum-bound `VERIFY.md` report; the verifier now writes only when `--out` is explicit, as the builder already does. The full site browser rerun remains underway.

The rebuilt static site and full browser rerun passed, checking 103 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. The local registry consumer test passed for all nine brands. The source-only release packaging produced nine verified current-release assets; this step did not publish them. The final native WordPress fixtures and release-inclusive audit remain in progress.

## 2026-09-29 PR consolidation against current main

PR #304 now includes the S065 DanceWithMe865 source commit and current main, including the published S064 Local Companion brand. The resulting production inventory is eleven kits. CI exports I Heart PR Tours and Local Companion proofs under Node 24.11.0, exports Scruggs and DanceWithMe865 under Node 26.5.0, builds the nine existing kits under Node 24.11.0, then builds the two clients under Node 26.5.0. The verified-kit artifact enumerates all eleven. First-round Codex findings are resolved on both original PRs, and the second review completed without new findings. Final CI remains before the owner's merge ritual.

## 2026-09-29 CI browser verification throughput

The first green consolidated run took 49m46s in `verified-build`. Its site export and test step took about 21m37s, with about 20m43s in `verify-site.mjs` after the Next build. The full site gate checks every generated HTML route at 360 and 1280 pixels and runs axe with WCAG 2.1 AA tags on each case. Run those independent route and viewport cases on three browser pages in one context, while retaining their metadata, interaction, overflow, and axe checks. The visual route and viewport matrix also runs both themes, axe, and screenshots; dispatch those independent cases across three isolated browser contexts so concurrent theme settings cannot interfere. Keep conformance profiles, interaction sequences, and publication gates as they are. Record both matrix timings in the CI log and compare the next complete run against the 49m46s baseline before the merge handoff.
