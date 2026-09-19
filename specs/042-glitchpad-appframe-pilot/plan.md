# Implementation Plan: Glitchpad AppFrame Adoption Pilot

**Branch**: `codex/042-glitchpad-appframe-pilot` | **Date**: 2026-09-19 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/042-glitchpad-appframe-pilot/spec.md`

## Summary

Complete the first BrandBuilder consumer pilot by adding two backward-compatible AppFrame capabilities discovered through live Glitchpad integration, generating and verifying a pinned kit for the upstream candidate revision, importing that exact kit into Glitchpad under downstream issue #196, adopting the generated shell and environment bridge, and collecting separate reference, Android consumer-host, Windows consumer-host, fresh-session, handover, and pilot-observation evidence. The shared generator owns AppFrame layout and environment behavior. Glitchpad retains document composition and imports governed bytes without hand-patching them.

## Technical Context

**Language/Version**: Upstream Python 3.8 minimum and generated TypeScript/React; downstream TypeScript 6.0.2, React 19.3.0, Rust 1.96.0, Kotlin/Android SDK 36

**Primary Dependencies**: BrandBuilder generator and validators, React, Tauri 2.11, Android WebView instrumentation, Vitest, Testing Library, axe-core, existing Glitchpad brand-kit importer

**Storage**: Versioned JSON and Markdown contracts, generated kit files in ignored upstream `dist/`, exact vendored kit bytes and integration receipt downstream

**Testing**: Python `unittest`, generated-kit verification, Vitest/jsdom, TypeScript build, Android `ActivityScenario` plus real WebView JavaScript evaluation, Windows Tauri build and shell smoke, repository aggregate gates

**Target Platform**: BrandBuilder generator on CI-supported hosts; Glitchpad Tauri 2 on Android API 24 and API 36 plus Windows 11/WebView2

**Project Type**: Cross-repository compiler and desktop/mobile consumer integration

**Performance Goals**: Preserve the existing shell startup and interaction budgets; AppFrame environment updates perform constant-time CSS custom-property writes per viewport event

**Constraints**: WCAG 2.1 AA, one owner per inset, no identity change, no generated upstream artifacts committed, no browser or reference evidence substituted for actual consumer-host evidence, UTF-8 without BOM and LF, no product composition moved upstream

**Scale/Scope**: One additive AppFrame layout variant, one dependency-free environment entry, eight regenerated production kits, one Glitchpad application shell, two Android emulator levels, one Windows desktop host track, and one coordinated evidence record

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

- **P1, source and artifact boundary**: PASS. Generator changes stay in `skill/templates/` and governed references. Upstream `dist/`, screenshots, packages, site exports, and native targets remain ignored. The downstream repository may vendor a verified generated kit under its existing integration contract.
- **P2, identity geometry**: PASS. No logo path, framing, palette, affiliation, or identity-continuity source changes are planned. The downstream importer preserves exact governed bytes.
- **P3, accessibility**: PASS. AppFrame focus, target, safe-area, IME, forced-color, reduced-motion, contrast, and text-scale behavior remain gated with no waiver.
- **P4, verification before publication**: PASS. All eight production kits rebuild, `verify.py` and `validate_glyph.py` remain zero-failure gates, and actual consumer-host evidence remains distinct from reference evidence.
- **P5, generated consumption**: PASS. Glitchpad imports the exact generated kit and consumes generated adapter sources and styles. It does not restate shared values or patch generated output.
- **P6, specifications and releases**: PASS. Upstream S042 and the downstream repository's next sequential Spec Kit feature govern their respective changes. No release, tag, or deployment is authorized.
- **Cross-repository authorization**: PASS. User authorization explicitly covers the proposed S042 pilot approach, push, and pull-request publication. GitHub issue #196 separately tracks the consumer mutation.

## Project Structure

### Documentation (this feature)

```text
specs/042-glitchpad-appframe-pilot/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   └── glitchpad-adoption.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Upstream Source Code

```text
skill/
├── SKILL.md
├── references/
│   ├── component-recipes.json
│   └── version-policy.json
└── templates/
    ├── gen_web_react.py
    ├── interface_contract.py
    ├── test_component_contract.py
    ├── test_web_react_adapter.py
    ├── test_interface_contract.py
    └── test_pipeline.py

scripts/
├── test_package_release.py
├── test_prepare_site.py
└── test_release_contract.py
```

### Downstream Consumer Code

```text
A:/Code/glitchpad/
├── specs/041-brandbuilder-appframe-adoption/
├── brand/
│   ├── web/
│   ├── tokens/
│   ├── enforcement/
│   ├── conformance/
│   ├── INTEGRATION.json
│   └── INTEGRATION.md
├── apps/glitchpad/
│   ├── index.html
│   └── src/
│       ├── App.tsx
│       ├── App.test.tsx
│       ├── main.tsx
│       └── styles.css
├── crates/glitchpad-host/gen/android/app/src/androidTest/
├── scripts/
│   ├── check-brand.mjs
│   └── check-shell-layout.mjs
└── .github/workflows/ci.yml
```

**Structure Decision**: Keep shared AppFrame API, layout, IME handling, version semantics, generation, and reusable verification upstream. Import exact generated output into Glitchpad using its existing kit boundary, then limit downstream source changes to shell composition, product-level regression tests, actual-host instrumentation, and evidence. Do not create a third package or copy editable adapter source outside the governed kit.

## Delivery Sequence

1. Add failing upstream tests for a full-bleed AppFrame layout and a dependency-free environment entry.
2. Implement the additive recipe and Web/React adapter changes, apply the required minor version bumps, and rebuild all production kits.
3. Commit and push the upstream candidate, open its pull request, and wait for the successful verified-kit artifact.
4. Create Glitchpad's repository-local Spec Kit feature, import the exact upstream artifact with its immutable candidate revision and CI artifact receipt, and adopt the generated AppFrame.
5. Add downstream unit, shell-layout, Android WebView instrumentation, Windows host, fresh-session, and handover evidence under test-driven discipline.
6. Commit and push the downstream candidate, open its pull request, and wait for its required CI and bot reviews.
7. Update upstream S042 evidence with the downstream candidate revision, PR, actual-host results, measurements, limitations, and review state. Re-run upstream CI if evidence changes require a final commit.
8. Request at most one manual `@Codex` second review round per pull request after the automatic round, respond to every comment, and stop only when both PRs are green and review-complete.

## Version Decision

- Component recipes: `1.0.0` to `1.1.0` because `full-bleed` is a backward-compatible AppFrame variant.
- Web/React adapter: `1.0.0` to `1.1.0` because the adapter adds a prop and a dependency-free environment entry without removing current exports.
- BrandBuilder compiler: `1.2.1` to `1.3.0` because the exact offline recovery distribution must include the backward-compatible generator capability. S042 prepares coherent release-candidate metadata and migration guidance but does not tag or publish a release.
- Interface Canon, egui adapter, Brand Canon, and Glitchpad brand: unchanged because their meanings and approved identity do not change.

## Complexity Tracking

No constitution violation or unjustified architecture expansion is required. Two repositories and two pull requests are necessary because actual consumer adoption cannot be honestly represented by an upstream fixture or by committing Glitchpad product composition into BrandBuilder.
