# Implementation Plan: Local Media Gallery Brand and Official Showcase

**Branch**: `codex/071-localmedia-gallery-brand` | **Date**: 2026-10-21 | **Spec**: [spec.md](spec.md)

## Summary

Develop the owner-selected D Contact sheet into a source-bound Full/Reduced identity and official ShruggieTech brand package. Preserve Full's four equal rounded media tiles with photo and video cutouts; simplify only the Reduced photo. Use the current BrandBuilder compiler, existing approval/promotion machinery and generated official-site projection. Add a small shared glyphkit compound-path primitive because the selected transparent cutouts cannot currently pass the direct-primitive provenance check.

## Technical Context

**Language/Version**: Python 3.8 minimum, local Python 3.12.9; current site TypeScript/Next.js.

**Primary Dependencies**: Existing glyphkit, identity_continuity, Coloraide, fontTools, Pillow, resvg and Playwright. Canonical candidate uses the already installed Windows Node 24.11.0 renderer group, matching supported approved-proof CI.

**Storage**: Private candidate and review material under ignored `dist/private/localmedia-gallery/`; approved source only under `brands/localmedia-gallery/`; generated kit under `dist/localmedia-gallery/`.

**Testing**: Glyphkit topology/composition regressions, construction-provenance tests, complete 32-proof repeated-render matrix, palette qualification, exact source promotion, Gate 2 binding, full documented kit and aggregate checks.

**Target Platform**: Portable brand package and official static ShruggieTech brand site.

**Project Type**: One brand addition plus a backward-compatible shared geometry primitive.

**Performance Goals**: Deterministic verified assets and recognizable small icons; no product speed or offline claims.

**Constraints**: Exactly two creative approvals, WCAG AA, unchanged existing logo geometry, true transparent cutouts, hidden Windows subprocesses, source-only Git, UTF-8 without BOM and LF.

**Scale/Scope**: One new owned brand. Product implementation and localmedia.gallery hosting are separate work.

## Constitution Check

| Principle | Design response | Status |
| --- | --- | --- |
| P1 Sources/artifacts | Commit spec, approved brand and toolkit source; all provisional/generated output remains ignored. | Pass in design |
| P2 Geometry | Preserve selected Full paths; add compound composition without reserialization; do not change existing identities. | Pass in design |
| P3 Accessibility | Measure formal inks and separately review semantic cues; failing values change. | Pass in design |
| P4 Verification | Require zero glyph/kit failures and aggregate validation before final publication. | Pending execution |
| P5 Generated site | Reuse discovery and verified kit projections rather than hand-authoring public brand assets. | Pass in design |
| P6 Spec/release | Complete spec, plan, tasks and analysis before implementation; integrate reviewed release/source evidence. | Active |

Post-design review finds no constitutional exception or parallel brand compiler. Final checks remain pending creative approvals and implementation.

## Phase 0: Research

The installed speckit-plan workflow explicitly requests research delegation. A read-only research agent inspected current Insonic review scripts and identity-continuity APIs. [research.md](research.md) records the current method, source-provenance gap, exact proof light ground and renderer limits. All technical unknowns are resolved; creative decisions remain proposals until the owner reviews the actual packet.

## Phase 1: Design and Contracts

Use existing schemas. [data-model.md](data-model.md) names the private brief, candidate, approval and kit state transitions. [contracts/delivery.md](contracts/delivery.md) binds delivered behavior and authority. [quickstart.md](quickstart.md) defines verification entry points. Full keeps the exact selected concept; Reduced keeps four tiles and both content cues, removes the sun and uses one broad mountain.

## Project Structure

```text
specs/071-localmedia-gallery-brand/
  spec.md
  plan.md
  research.md
  data-model.md
  contracts/delivery.md
  quickstart.md
  tasks.md
  verification.md
brands/localmedia-gallery/             # only after exact Gate 1 promotion
  brand.json
  build/mk_paths.py
  identity-continuity.json
skill/templates/glyphkit.py            # compound primitive
skill/templates/identity_continuity.py # approved primitive vocabulary
skill/templates/test_glyphkit.py
skill/templates/test_identity_continuity.py
dist/private/localmedia-gallery/       # ignored brief and review packets
dist/localmedia-gallery/               # final generated kit
```

**Structure Decision**: Extend the existing primitive vocabulary and reuse source/proof/promotion contracts. No special transparent-background imitation or per-brand generator fork.

## Integration and Verification

The compound primitive accepts closed absolute M/L/C/Z subpaths, preserves their bytes and leaves fill-rule choice explicit. Test cutouts under evenodd at 256, 32 and 16 pixels, multiple contours, invalid/open input and provenance acceptance/rejection. Existing geometry helpers and approved snapshots must remain unchanged.

Gate 1 prepares actual production mark SVGs and renders all 32 coordinates twice. Store side-by-side, overlay, silhouette-XOR and color-difference artifacts per coordinate, qualify exact colors, bind renderer settings and source hashes, and keep approval pending. After owner approval, promote approved bytes; do not reconstruct.

Gate 2 presents source-derived lockups, typography, palettes, usage, representative gallery and separate social composition with the supplied exact slogan/description. Only after that approval compile the final package, integrate release/site inventories, run CONTRIBUTING.md and CI-parity checks, and verify official live routes/download checksums. Apply version-policy.json when preparing the reviewed release; no version or release claim is made during creative discovery.

## Decisions, Chronological

- 2026-10-21: Record supplied official ownership/publication relationship, exact slogan/description and domain; prepare four private directions in one provisional blue.
- 2026-10-21: Owner selects D: "Let's go with D. Continue down that direction." Retain its four rounded media tiles and transparent image/video cues.
- 2026-10-21: Preserve Full geometry exactly; propose Reduced without the sun and with one broad photo peak. Initial geometry checks pass with zero warnings/failures.
- 2026-10-21: Add a shared compound primitive and provenance allowlist entry because direct string composition is rejected by the existing canonical helper check. This preserves source geometry and genuine transparency rather than introducing opaque background patches.
- 2026-10-21: Propose the existing periwinkle study colors for the production candidate and provide two accessible alternatives for review. No color selection or creative approval is inferred from the direction choice.

- 2026-10-21: Owner selects Jade and requests a pairing wordmark. Bind #69D4BB/#08745F, propose the literal lowercase domain in the house bold face with an accented .gallery segment, and align the horizontal pair by measured visible ink. Preserve Full/Reduced paths and retain the Periwinkle packet privately as superseded evidence. The owner request authorizes private wordmark previews before Gate 1; both mandatory approvals remain pending.

- 2026-10-21: Owner approves the shown Jade logo, wordmark and pairings and requests the remaining fundamentals for review. Record the exact wording, promote source without reconstruction and confirm all 32 approved proof hashes. Assemble private palette, typography, functional cues, icon review, usage, gallery specimens and the exact-copy social proposal.

- 2026-10-21: Gate 2 inspection finds that the shared type-specimen header clips the long domain and drops compound path fill rules. Fit the header by measured glyph bounds, honor configured wordmark segment roles and retain exact mark fill rules. This is a specimen renderer correction; the approved master, helper, palette, logo renderer and all 32 proof hashes stay bound to Gate 1.

- 2026-10-21: Ten brand-essential tests and six specimen pipeline regressions pass after the specimen correction. Independent private review validation checks 19 asset roles, 40 logo derivatives, 98 icon PNGs, twelve approved pairing matches and 34 contrast pairs. Present one assembled Gate 2 review covering the exact social copy layout; finalize approved-copy metadata only after the owner decision, then require production reproduction of the shown image hashes.

- 2026-10-21: Owner corrects the typed name to Local Media Gallery and permits Local Media above Gallery if necessary. The primary one-line name fits. Prepare a separate source-bound name revision with neutral Local Media and Jade Gallery, preserve the prior approved packet, and regenerate all 32 square proofs to demonstrate unchanged geometry/palette. Revise wordmark and application previews privately; the changed source is pending review and cannot inherit the old wordmark approval.

- 2026-10-21: Owner requests a larger horizontal icon and smaller lettering, considering Local Media above larger Gallery. Compare one-line 72-unit type with a two-line 48/84-unit hierarchy beside the unchanged 160-unit icon. Render both at the same 112-pixel icon height for review. Preserve canonical sources and approved square proof bytes while exploring the requested layout. Option B needs governed per-lockup line support in the shared generator before canonical promotion; do not patch a generated kit or invent source approval.

- 2026-10-21: Owner chooses B and requests the refreshed fundamentals. Add opt-in logo.lockups.horizontal.wordmark_lines with text/role/font_size_units, padding_units and line_gap_units. Implement measured visible-ink layout in a shared lockup_typography module; keep the existing single-line branch unchanged for all other layouts. Bind the helper bytes for opt-in renderer identity while retaining old proof bindings only when the new guarded branch is absent at runtime. Validate malformed config and clipping, compare the selected B artwork against actual output, refresh canonical source/proofs with the owner wording and assemble the current Gate 2 review. No final kit or public publication is authorized by this review request.

- 2026-10-21: Production output matches all four selected B colorways exactly, and all 32 square proofs retain their approved hashes. Promote the source amendment using the owner's explicit B wording and shown-study digest, retaining the original square authority. Bind gen_logo, lockup_typography and the horizontal contract function for opt-in layouts; preserve existing default fingerprints by excluding only the guarded branch that cannot execute for unconfigured brands. The dependency tests cover both helper and contract drift. Refresh the private Gate 2 packet from the promoted source and increase the illustrative gallery-header logo box to satisfy its 200-pixel minimum width.

- 2026-10-21: Owner requests removal of the social image description and vertical re-centering of the remaining content. Keep the selected B logo and exact slogan sizes/spacing, add an opt-in centered-group composition measured from visible ink, and regenerate the review from the actual shared compiler output. Scope selected-B proof dependency binding to the same proof-stage semantic digest already used by other brands so social-only edits cannot invalidate unchanged identity proofs. Validate the copy contract, default composition stability, visible bounds and all current source proofs. The assembled Gate 2 review remains pending.

- 2026-10-21: Owner approves the shown final fundamentals and authorizes final package validation and publication preparation. Record exact Gate 2/social-image hashes and compile through the shared builder. Prepare BrandBuilder 3.1.0 and Brand Canon 2.1.0 because optional governed source fields and compiler capabilities are additive. Update compatible version rules, existing source canon metadata without changing identity snapshots, new-brand proof/release/audit inventories, and current-version release assertions. Run the documented aggregate, delivery, runtime, site and publication gates. Stop at a reviewable publication candidate; live release/tag/Pages deployment is outside this preparation step.

- 2026-10-21: The required WordPress npm audit fails on @simple-git/argv-parser below 2.0.1 and the sprintf-js chain inherited through js-yaml 3.x. Inspect primary advisory and installed API usage; pin simple-git 4.0.2 (with parser 2.0.1) and js-yaml 4.3.2 within the fixture only. wp-env uses the retained simple-git clone API and yaml.dump. Keep wp-env 11.16.0, existing transport replacement, audit threshold and consumer adapter unchanged; verify dependency behavior and both actual runtime pairs before completion.

- 2026-10-21: Visual inspection of the full final logo sheet finds that its fixed wordmark row overlaps the taller selected horizontal pairing despite passing the existing numeric gates. Space the QC rows by measured alpha bounds, retain at least 24 pixels between visible inks, and grow the panel when needed. Add an independent colored-pixel regression. This changes only the contact sheet composer, with no approved asset changes; regenerate affected kits after the shared compiler source settles.

- 2026-10-21: Final portable screenshots expose browser-default blue links on a dark guide surface and a standalone Web specimen that declares font tokens but never applies or embeds the local faces. Inherit readable link color in the guide and apply embedded local type only in the standalone specimen. Keep consumer component APIs and styles unchanged. Measure actual browser font loading and link contrast, then regenerate all packages from settled compiler source before publication assembly.

- 2026-10-21: Complete the settled-source 13-kit rebuild, 514-case contract campaign, actual WordPress pairs, clean registry consumer, 139-route desktop/mobile AA campaign and 96 theme visual checks. Certify the final staged kits/site/release bytes and archive encoding. Inspect all logo/PDF contact sheets and the Local Media Gallery portable/preview sheets. Prepare a source-only PR for BrandBuilder 3.1.0, Brand Canon 2.1.0 and Local Media Gallery 1.0.0; leave the reviewed tagged release and live verification task T018 open.

- 2026-10-21: The first hosted PR run fails before tests because ubuntu-latest now resolves to Ubuntu 26.04 and setup-python cannot install Python 3.8 there. The official actions/python-versions manifest lists Python 3.8.18 binaries for Ubuntu 24.04. Pin only the minimum-version job to ubuntu-24.04, retain Python 3.8 and all test gates, and assert the image in the existing workflow contract test. Rerun the hosted campaign on the corrected source.

- 2026-10-21: The supported hosted runner exposes Path.write_text(newline=...) in two horizontal-layout fixture writes. Use explicit UTF-8 bytes to retain LF on Python 3.8 and current Python. The six local cases pass; rerun hosted validation and use its final checksummed compiler/release candidate for handoff.

- 2026-10-21: The Python 3.8 campaign reaches the new core-vector social test and finds an unintended call into raster proof generation. Isolate only its temporary report-writing dependency, as existing vector cases do. Retain real SVG/glyph measurements and full canonical-host/aggregate proof gates. The focused Cueson/Local Media Gallery vector case passes; rerun hosted verification.

- 2026-10-21: Automatic PR review identifies invalid omitted canvas dimensions and a missing wordmark-ink fallback. Preserve the source-bound explicit renderer byte-for-byte. Add a small defaults adapter selected only when canvas height or dark/light wordmark mappings are absent. Bind that adapter for affected inputs; for fully explicit profiles, retain the existing fingerprint only after removing the exact isolated fallback import whose guard cannot execute. Measured bounds, color fallback, source non-mutation, production-routing and dependency-drift cases pass. All 13 current fingerprints and the Local Media Gallery canonical source binding remain unchanged. Run the expanded pipeline and final hosted aggregate before handoff.
