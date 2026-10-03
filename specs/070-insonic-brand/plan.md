# Implementation Plan: insonic Brand and Official Showcase

**Branch**: `codex/070-insonic-brand` | **Date**: 2026-10-03 | **Spec**: [spec.md](spec.md)

## Summary

Start from the verified latest BrandBuilder 3.0.0 and ship the approved insonic identity through compiler/site 3.0.1. The adaptive brief, exploratory directions, source-bound Gate 1 and assembled Gate 2 are approved. Complete final verification and official-site release with the independent Glacial blue palette and shared local typography/layout.

## Technical Context

**Language/Version**: Python 3.8 minimum, local Python 3.12.9; Node.js 20 minimum. Current exploratory host has Node 26.5.0. Select and record the canonical renderer before Gate 1, preferably the existing Node 24.11.0 Windows proof group.

**Primary Dependencies**: Existing glyphkit, identity_continuity, gen_logo, authoring_brief, promote_identity, build_all, prepare_site, Coloraide, fontTools, Pillow, pikepdf, Playwright, Node resvg, Next.js.

**Storage**: Source-only approved brand under `brands/insonic/`; specs under this directory; exploratory output and review packets under ignored `dist/private/insonic/`; final generated kit under `dist/insonic/`.

**Testing**: Private brief validation, glyph and palette qualification, exact source/proof continuity, Gate 2 packet validation, full kit validation, documented aggregate contract/site/publication checks, and live route/checksum verification.

**Target Platform**: Portable brand kit and official static brand site. Host applications consume the supported bindings independently.

**Project Type**: Brand source and catalog addition using an existing compiler and site.

**Performance Goals**: Reproducible identity and verified delivery; no invented product latency or recognition-accuracy targets.

**Constraints**: Two exact creative approvals, WCAG AA, no inferred messaging, source-only Git, unchanged existing geometry, hidden non-interactive Windows tooling, UTF-8 without BOM and LF.

**Scale/Scope**: One new brand, twelve hosted identities and nine release-authorized owned archives after integration; preserve three existing client hosted-only identities.

## Constitution Check

| Principle | Response | Status |
| --- | --- | --- |
| P1 Source/artifact boundary | Commit specs and approved source; keep previews, proofs, binaries, kits, and exports in ignored output. | Design passes |
| P2 Geometry preservation | Construct with glyphkit, bind exact source at Gate 1, promote approved bytes and preserve siblings. | Approved source and proofs pass |
| P3 Accessibility | Measure dark/light text, controls, state and palette roles; correct failures. | insonic palette and kit pass; aggregate site checks in progress |
| P4 Verification | Final compilation follows approvals and requires zero kit/glyph problems plus aggregate validation. | insonic passes; aggregate verification in progress |
| P5 Site projection | Reuse automatic brand discovery and verified generated projection. | Design passes |
| P6 Spec/release | Maintain this slice through reviewed change, tagged CI release, and live checks. | In progress |

No exception or parallel brand compiler is proposed. Post-design review finds no conflict; pending entries are execution gates rather than waived requirements.

## Phase 0: Research

Research uses the product docs and current generator/site source. The plan research subagent was explicitly requested by the installed speckit-plan workflow. Findings identify S064 Local Companion as the nearest new constructed identity workflow, the required release/site inventories, and the canonical Windows renderer concern. See [research.md](research.md).

## Phase 1: Design and Contracts

Use existing brand, identity continuity, messaging, and publication schemas without adding a new schema. [data-model.md](data-model.md) names authority and state transitions; [delivery.md](contracts/delivery.md) binds the public contract; [quickstart.md](quickstart.md) gives validation entry points. Creative discovery stays interactive, while the workflow and integration path are fully specified.

## Project Structure

```text
specs/070-insonic-brand/
  spec.md
  plan.md
  research.md
  data-model.md
  contracts/delivery.md
  quickstart.md
  tasks.md
  verification.md
  checklists/requirements.md
brands/insonic/
  brand.json
  build/mk_paths.py
  identity-continuity.json
dist/private/insonic/
  brief.json
  directions/
  gate-1/
  gate-2/
dist/insonic/
```

**Structure Decision**: Reuse canonical sources and generated delivery conventions. No application repo, domain deployment, or processing runtime is created by this slice.

## Integration and Verification

After both approvals, register insonic in release authorization, publication and identity audits, site expectations, and Windows proof/kit artifact inventories. Preserve hosted-only client release policy. Site discovery and pages are generated automatically, so do not author a duplicate brand page.

Use the current CI workflow and contributor guide as the exact aggregate-check authority. The new kit must pass current-source validation, all production proofs, glyph checks, source-bound Gate 2 validation, final build, render/pagination checks, encoding scan, site/registry/publication audits, and release checksum inspection. Existing kits require their current renderer groupings; do not rebuild siblings with a substituted approved renderer.

Release metadata changes occur after creative work is complete and must synchronize compiler, site, changelogs, release impact and tests without altering canon/adapter versions unless their contracts change. Live deployment follows successful tagged release publication. A merged main commit alone does not satisfy the official-site outcome.

## Decisions, Chronological

- 2026-10-03: Use repository BrandBuilder 3.0.0, verified against the published latest release, instead of cached plugin 1.0.0.
- 2026-10-03: Adopt the accepted independent-palette/shared-typography direction and public owned-project relationship; keep exact creative decisions pending.
- 2026-10-03: Use S064's prospective identity continuity workflow and existing generated site discovery. Do not copy historical custom concept-rendering assumptions into production.
- 2026-10-03: Select canonical renderer before Gate 1 and bind its version and settings; exploratory previews are nonbinding.
- 2026-10-03: Owner selects direction A and rejects the messy crossing bar. Compare removing the bar against moving the connection to a common terminal baseline, retaining the provisional palette to isolate the geometry decision.
- 2026-10-03: Owner selects A1 Clean rhythm and requests color comparisons on that geometry before choosing production colors. Preserve the selected three forms across comparison panels.
- 2026-10-03: Owner selects Glacial blue and retains all three forms in Reduced with stronger tiny-size stems. Construct Full with the exact selected path array and Reduced with 160-unit stems on the same centers and heights. Bind the canonical Windows Node 24.11.0 renderer group before source approval.
- 2026-10-03: Owner approves the exact Gate 1 packet. Record exact wording and source-bound evidence, promote canonical source atomically, and verify all current production proof and comparison hashes before provisional derivative generation.
- 2026-10-03: Owner selects developers and the slogan direction `Voice, with memory.`. Prepare source-derived lockups and type, distinct functional cues, a synthetic developer-workspace example and an exact social-copy proposal. Use the existing classic social layout because the centered-single-line preset crowds this lockup. Confirm independent message roles/uses and social line breaks before validating the formal Gate 2 packet.
- 2026-10-03: Owner accepts the shown fundamentals/copy and instructs continuation. Record exact message-role and social-copy decisions in the source and private brief, preserving the governed Gate 1 snapshot. Generate the canonical social SVG/PNG and outlined specimen, validate the formal source-bound Gate 2 packet, then request the final assembled creative approval.
- 2026-10-03: Owner identifies a confusing mark/name misalignment in the generated typography specimen. Correct the upstream specimen header using measured mark and font ink centers, regenerate its source/raster, and refresh the pending Gate 2 packet. Preserve approved logo geometry, existing logo derivatives and social composition.
- 2026-10-03: Owner approves the revised complete packet with "approved. CONTINUE". Record Gate 2 and exact social-image digests without changing the canonical Gate 1 binding. Integrate insonic 1.0.0 in BrandBuilder/site 3.0.1, a compiler patch for the specimen corrections; canon and adapter versions remain unchanged. Track publication through issue #319 and the reviewed tagged release.
- 2026-10-03: Connect the exact approved naming, personality, logo and palette narrative to the existing `guidance` fields consumed by the official guide. This corrects an omitted projection without introducing new copy or changing the approved identity snapshot. Extend the source-bound S068 disposition inventory and current production-count assertions to twelve brands.
- 2026-10-03: Concurrent aggregate builds expose shared global temporary screenshot filenames in `qc_images.py`. Give each QC run its own temporary directory and cover actual simultaneous red/blue kit captures in the pipeline regression suite. Rebuild affected distributions with the synchronized release-impact record.
- 2026-10-03: The required WordPress fixture dependency audit fails on newly reviewed GHSA-ch52-4w7c-c8xp through `@wordpress/env` 11.16.0, `got`, `cacheable-request` and `http-cache-semantics` 4.2.0. Both installed packages match the latest published versions and the advisory lists no patched release. Preserve the required audit gate and seek owner direction before expanding this brand slice into dependency remediation. Official publication remains pending.
- 2026-10-03: Owner states "Yes, remediate the test dependency". The pinned runner uses only JSON retrieval and streaming ZIP downloads from got, with no cache configuration. Replace that fixture dependency with a local built-in-fetch compatibility transport, eliminating the affected cache chain rather than suppressing the advisory. Cover the two consumed APIs, cookie/cache isolation, redirects, exact download bytes, HTTP/truncation errors, cancellation and actual installed runner resolution. Enforce these tests before the unchanged npm audit and pinned runtime checks in CI. The transport remains outside generated consumer kits.

## Complexity Tracking

Artifact checks identified platform-default CRLF serialization in the outlined typography generator. Correct that upstream in `skill/templates/build_specimen.py`, document it in the kit build notes, and verify LF output on Windows without changing rendered geometry.

No constitution violations or architectural expansion identified.
