# Implementation Plan: Cueson Brand Kit

**Branch**: `codex/026-cueson-brand-kit` | **Date**: 2026-09-09 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/026-cueson-brand-kit/spec.md`

## Summary

Deliver issue #184 as one identity-creation and publication slice with two non-negotiable owner gates. Freeze synchronized Shruggie Brand and Cueson evidence, translate Cueson's lossless timed-language interchange purpose into four proposal directions, and recommend the Cueframe direction with a dark ink and accessible iris color system. Generate all proposal evidence under ignored output. Halt for Gate 1 before committing production identity sources. After exact glyph and palette approval, construct the full source-driven identity and derivative spread, halt again for Gate 2, then complete the verified kit, public projection, and consumer handoff. The owner's kickoff authorizes branch push and official pull-request creation after both gates, but not merge, release, deployment, consumer import, or domain activation.

## Technical Context

**Language/Version**: Python 3.8 minimum for generators and validation; Node.js 20 minimum for site source; JSON, Markdown, SVG, CSS, and HTML source contracts

**Primary Dependencies**: Existing `fontTools`, Pillow, svgelements, coloraide, CairoSVG or native SVG renderer capability, repository-owned brandbuilder templates, Next.js App Router, and local house font assets

**Storage**: Source files under `brands/cueson/`, shared approved fonts under `assets/fonts/`, Spec Kit and approval evidence under `specs/026-cueson-brand-kit/`, and ignored concept, approval, kit, registry, raster, PDF, archive, and site output under `dist/` and generated site directories

**Testing**: Python `unittest` suites, identity-study tests, generator contract and pipeline tests, glyph and image validation, full multi-kit build, Markdown and repository-hygiene checks, site lint/build/tests, and hosted GitHub Actions

**Target Platform**: Offline-generated portable brand kit, static hosted brand portal, web and framework bindings, plus web, Android, iOS, macOS, Windows, social, repository, and compatibility icon consumers

**Project Type**: Source-driven Python brand generator plus statically exported Next.js documentation and registry site

**Performance Goals**: No new network dependency in routine generation; all seven production kits complete within the existing hosted build envelope; concept and approval packets reproduce deterministically from recorded inputs

**Constraints**: Two mandatory owner halts; no production identity source before Gate 1; no public surface before Gate 2; WCAG 2.1 AA without waivers; zero glyph failures and zero kit-verification problems; passive SVG and contained generated-output security checks; generated artifacts remain ignored; Cueson working tree and `cueson.io` remain unchanged; at most two Codex review rounds; Python 3.8 compatibility; UTF-8 without BOM and LF; no authentication, user data, tenant boundary, or runtime service is introduced, so tenancy testing is not applicable

**Scale/Scope**: One new ShruggieTech-owned production brand, 32 functional requirements, four initial glyph directions, one recommended palette, two iterative approval packets, complete current kit layers, one public site and registry integration, one consumer handoff manifest, and one official pull request

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

| Principle | Plan evidence | Result |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit only approved source contracts, constructed geometry, tests, study generator, and Spec Kit evidence. All renders, kits, registries, PDFs, archives, and site exports stay ignored. | PASS |
| P2. Identity geometry is preserved | S026 creates a new identity, then makes the approved Gate 1 master and approved Gate 2 derivatives immutable through exact hashes, configuration fingerprints, and comparison evidence. | PASS |
| P3. Accessibility has no exemption | Gate 1 includes measured AA and color-vision evidence; failing values change before approval. The final kit must pass every declared role without waiver. | PASS |
| P4. Verification precedes publication | Fail-closed approval validation, glyph validation, `verify.py`, full build, site tests, CI, and review reconciliation precede public eligibility and merge handoff. | PASS |
| P5. The site consumes generated kits | Cueson public pages and registries are derived from the verified `dist/` kit only after Gate 2; site source does not restate brand values. | PASS |
| P6. Specifications and releases move together | S026 specification, research, contracts, tasks, approval evidence, implementation, pull request, review ledger, and issue traceability move together. No release is cut. | PASS |

### Post-Design Re-check

The design uses the existing source-to-`dist/` architecture, adds only the narrow constructed-identity approval behavior that the new owner gates require, and leaves external consumer and domain mutations to later workflows. The two approvals fail closed on configuration or manifest drift. No constitution exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/026-cueson-brand-kit/
├── checklists/
│   ├── identity-approval.md
│   └── requirements.md
├── contracts/
│   ├── identity-approval.md
│   ├── publication-and-review.md
│   └── source-and-handoff.md
├── data-model.md
├── evidence.md
├── gate-1-proposal.json
├── gate-2-proposal.json
├── plan.md
├── quickstart.md
├── research.md
├── spec.md
└── tasks.md
```

### Source Code (repository root)

```text
brands/cueson/
├── ui_kits/cueson-data/
├── brand.json
├── NOTES.md
├── README.md
└── SKILL.md

scripts/
├── cueson_identity_study.py
├── test_cueson_identity_study.py
├── build_all.py
├── prepare_site.py
└── existing repository validation

skill/templates/
├── brand_contract.py
├── test_brand_contract.py
├── test_pipeline.py
└── existing generation and verification templates

site/
├── app/
├── components/
├── generated/
├── public/
└── tests/
```

**Structure Decision**: Reuse the current source-to-`dist/` brand architecture and existing static-site discovery. Keep proposal generation in one deterministic repository script, approval and traceability evidence in S026, approved production identity in `brands/cueson/`, and every rendered proposal or generated deliverable in ignored output. Do not add a second publishing path and do not modify the Cueson repository.

## Delivery Sequence

1. Synchronize Shruggie Brand and Cueson remotes, freeze both default-branch revisions, read product authority, and record the visual exclusion for the explainer images.
2. Add deterministic study tests and a proposal generator for four concept directions, the recommended color system, exact size and surface proofs, measurements, rationale, and manifest hashes.
3. Generate and inspect the ignored Gate 1 packet without creating `brands/cueson/brand.json` or production geometry.
4. **Owner Gate 1**: present the four glyph directions and recommended palette, accept critique, revise as required, and proceed only after explicit hash-bound approval.
5. Encode the approved master, palette, typography, and constructed-identity approval ledger; add failing tests before the narrow contract adjustment that permits approval-ledger binding for constructed marks with no imported authoritative image.
6. Generate the complete derivative spread and ignored Gate 2 packet with exact source relationships, hashes, measurements, platform masks, copy compositions, and public-surface preview.
7. **Owner Gate 2**: present the full spread, accept critique, revise as required, and proceed only after explicit hash-bound approval.
8. Record Gate 2 approval, complete the kit source, UI specimen, consumer handoff, and public eligibility, then run the full local gate and inspect representative output.
9. Commit with a Conventional Commit subject, push the feature branch without a pre-push halt under the owner's explicit exception, and open the official pull request closing #184.
10. Reconcile CI, security-bot results, all review comments, and no more than two Codex review rounds. Halt only when everything received is satisfied and required checks are green, leaving final review and merge to the owner.

## Complexity Tracking

No constitution violation requires justification. The study generator and two approval ledgers are the minimum auditable mechanism for creating a new identity without treating a transient chat image or unbound owner response as production authority.

## Protocol Deviation

The installed checklist preflight requires `plan.md`, while the generic autopilot protocol lists checklist before plan. S026 therefore creates the Phase 0 and Phase 1 planning artifacts first, then generates the reviewer-owned domain checklist before task generation and analysis. This changes only the command order needed to satisfy the repository's installed preflight; it does not weaken checklist review or any identity gate.
