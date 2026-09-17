# Implementation Plan: Cross-Host Conformance Fixtures

**Branch**: `codex/040-cross-host-conformance` | **Date**: 2026-09-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/040-cross-host-conformance/spec.md`

## Summary

Add a versioned conformance policy and compiler stage that emits the same profile, host, diagnostic, and evidence contract for every production brand. Reuse the generated Web/React specimen as the browser reference, add small executable Rust and Go host-boundary fixtures for Tauri Android and Wails Windows, and retain the existing real egui rendered-state crate as the native fixture. Stage verified generated conformance data into public site routes, exercise browser profiles with Playwright and axe, produce ephemeral screenshot candidates, validate human-only baseline decisions, and expose each failure category independently through kit verification and CI artifacts.

## Technical Context

**Language/Version**: Python 3.8-compatible compiler and validators; TypeScript/TSX on Node.js 20+; Rust 1.95+ for the existing egui adapter and a dependency-free Tauri host-envelope fixture; Go 1.22+ for a dependency-free Wails host-envelope fixture

**Primary Dependencies**: Python standard library; existing React 19, Next.js, Playwright Chromium, and axe-core site stack; Rust standard library plus the already pinned egui 0.36.1 and egui_kittest 0.36.1; Go standard library

**Storage**: Versioned JSON source policy, generated per-kit JSON and fixture source, static site staging data, ephemeral PNG candidates, and optional governed JSON baseline decisions; no database or network persistence

**Testing**: Python `unittest`, generated Rust `cargo test --locked`, generated Go `go test`, Playwright Chromium profile and interaction runs, axe WCAG 2.1 AA scans, deterministic-byte comparisons, all-brand builds, site static export, release suites, Markdown and repository-hygiene checks

**Target Platform**: Chrome browser reference; Android WebView ownership envelope used by Tauri 2; Windows 11 WebView2 window-chrome envelope used by Wails; native egui rendered states; public static Next.js site

**Project Type**: Static cross-runtime interface compiler, generated reference fixtures, and self-hosting documentation site

**Performance Goals**: One deterministic conformance generation pass per kit; zero generator-time network access; profile runs bounded to the declared matrix; fixture tests complete in ordinary CI without launching product applications

**Constraints**: WCAG 2.1 AA; no committed generated kits, PNG candidates, native targets, or site exports; no browser substitution for native-host evidence; no OS-name behavior routing; baseline acceptance remains human-only; no identity geometry changes; UTF-8 without BOM and LF

**Scale/Scope**: Eight production brands, fifteen bounded component recipes, seven required capability profiles, four host tracks, four diagnostic classes, one known-bad and one corrected Android ownership trace

## Constitution Check

*GATE: Must pass before Phase 0 research and after Phase 1 design.*

| Principle | Design response | Status |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit only policy, generator, validators, tests, site source, and Spec Kit records. Generate kits, screenshots, fixture build outputs, and site export under ignored paths. | PASS |
| P2. Identity geometry is preserved | Conformance consumes existing generated identity and interface data. No brand source, logo binding, path, mask, or artwork transformation changes are planned. | PASS |
| P3. Accessibility has no exemption | Browser reference profiles run axe and explicit keyboard, focus, target, scaling, motion, and contrast checks. Missing native accessibility evidence is explicit, never waived. | PASS |
| P4. Verification precedes publication | Every kit gains fail-closed conformance verification. All production kits rebuild, native fixtures execute, the site exports, and candidate screenshots remain review-only artifacts. | PASS |
| P5. The site consumes generated kits | Site routes consume staged per-kit conformance data and browser specimens. No brand token or specimen value is reauthored in site source. | PASS |
| P6. Specifications and releases move together | S040 includes spec, clarification record, checklist, plan, contracts, tasks, analysis, implementation evidence, and changelog. No release is cut. | PASS |

Post-design recheck: PASS. The design preserves the source/generated boundary, makes browser and host proof non-substitutable, adds no identity mutation, and keeps visual acceptance human-owned.

## Project Structure

### Documentation (this feature)

```text
specs/040-cross-host-conformance/
├── checklists/
│   ├── conformance-contract.md
│   └── requirements.md
├── contracts/
│   ├── baseline-review.md
│   ├── conformance-evidence.md
│   └── host-fixtures.md
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
skill/
├── references/
│   ├── conformance-baseline-decisions.json
│   └── conformance-contract.json
└── templates/
    ├── build_kit.py
    ├── conformance_contract.py
    ├── gen_conformance.py
    ├── test_conformance.py
    ├── test_pipeline.py
    └── verify.py

scripts/
├── prepare_site.py
└── test_prepare_site.py

site/
├── app/(site)/conformance/
│   ├── [slug]/page.tsx
│   └── page.tsx
├── components/conformance-reference.tsx
├── lib/conformance.ts
├── scripts/verify-site.mjs
└── tests/site.test.mjs

.github/workflows/build.yml
CHANGELOG.md
```

**Structure Decision**: Keep the canonical conformance policy under `skill/references/`, all generated host source under each ignored kit, and public presentation under `site/`. The Rust and Go fixtures are emitted from the generator so they remain pinned to the same brand and contract identities as the browser and egui outputs. Site source consumes staged kit data and does not become a second authority.

## Phase 0: Research and Decisions

1. Confirm existing browser specimen, AppFrame ownership profiles, egui rendered tests, site staging, and verification extension points.
2. Select fixture boundaries that execute host-specific ownership logic without importing product composition or requiring full product shells.
3. Define evidence classes and statuses that prevent browser, reference-host, and downstream-consumer proof from being conflated.
4. Define ephemeral candidate and human-only baseline decision rules compatible with the constitution's generated-artifact boundary.
5. Record exact local and CI toolchain floors plus fallback behavior when optional host tooling is unavailable.

## Phase 1: Design and Contracts

1. Model profiles, host tracks, envelopes, traces, fixture results, diagnostics, visual candidates, and baseline decisions in `data-model.md`.
2. Define conformance evidence substitution and status rules in `contracts/conformance-evidence.md`.
3. Define executable browser, Tauri, Wails, and egui fixture boundaries in `contracts/host-fixtures.md`.
4. Define candidate generation and human-only acceptance in `contracts/baseline-review.md`.
5. Provide complete validation commands and expected evidence in `quickstart.md`.

## Phase 2: Implementation Strategy

1. Add contract and generator tests first, including known-bad ownership, evidence substitution, invalid metadata, and baseline rejection cases.
2. Implement the canonical policy loader, schema-like validation, deterministic trace evaluator, diagnostic classification, and baseline decision validation.
3. Generate per-brand browser and native-host fixture inventories, executable Rust and Go ownership fixtures, and evidence manifests.
4. Integrate generation and verification into the build pipeline, release manifest boundary, deterministic tests, and all-brand checks.
5. Stage verified conformance records into the site, add the public index and per-brand routes, and exercise the profile matrix with Playwright and axe.
6. Upload ephemeral visual candidates and evidence manifests from CI without accepting or committing them.
7. Run focused suites, generated native fixture suites, full pipeline, all-brand build, site export, publication audit, Markdown, encoding, and repository-hygiene gates.

## Complexity Tracking

No constitution violations or justified exceptions are required.
