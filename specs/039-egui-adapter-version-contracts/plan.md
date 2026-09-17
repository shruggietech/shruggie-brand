# Implementation Plan: Native egui Adapter and Versioned Contracts

**Branch**: `codex/039-egui-adapter-version-contracts` | **Date**: 2026-09-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/039-egui-adapter-version-contracts/spec.md`

## Summary

Compile the existing Brand Canon, Interface Canon, and bounded component recipes into a deterministic, self-contained Rust crate for egui. The crate exposes typed semantic tokens, logical-unit and density transforms, observed runtime capabilities, idiomatic immediate-mode helpers, and a machine-readable support matrix that distinguishes native support, deliberate adaptation, and unsupported behavior. Exercise the generated crate with `egui_kittest` against input, focus, selection, validation, density, and scaling behavior. Upgrade the consumer contract, manifests, offline recovery, release certification, and documentation to independently version Brand Canon, Interface Canon, component recipes, Web/React adapter, egui adapter, compiler, and each brand, with explicit compatibility, bump, provenance, pinning, and exact-recovery rules.

## Technical Context

**Language/Version**: Python 3.8-compatible compiler and validation code; JSON Schema draft 2020-12; generated Rust edition 2024 with MSRV 1.88

**Primary Dependencies**: Python standard library and existing `coloraide`; generated `egui` 0.36.1 runtime dependency; generated `egui_kittest` 0.36.1 development dependency

**Storage**: Versioned JSON reference contracts and generated static kit files; no database or network persistence

**Testing**: Python `unittest`, JSON Schema validation, deterministic-byte comparisons, generated Rust `cargo test`, `egui_kittest` accessibility-tree assertions, all-brand builds, existing site and release suites

**Target Platform**: Rust applications embedding egui on desktop or web hosts; behavior is selected from observed capabilities and host handoffs, never an operating-system name

**Project Type**: Static design-system compiler with generated web and native adapters

**Performance Goals**: Deterministic generation for every production brand; zero generator-time network fetches; one typed token resolution per theme/density selection; no hidden background process or renderer requirement during ordinary Python contract tests

**Constraints**: WCAG 2.1 AA; no generated `dist/` committed; no logo or identity-source changes; no React/CSS emulation or cross-renderer component DSL; unsupported behavior remains explicit; UTF-8 without BOM and LF; exact independent versions and checksums throughout the handoff

**Scale/Scope**: 15 bounded shared recipes, two themes, two densities, all production brands, one egui adapter version, seven independently identified contract domains

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

| Principle | Gate | Result |
| --- | --- | --- |
| I. Source-Only Repository | Rust crates, Cargo locks, rendered evidence, kits, and release archives remain under ignored `dist/` or temporary directories. Only generators, reference contracts, tests, and Spec Kit artifacts are committed. | PASS |
| II. Preserve Identity Geometry | No brand source, approved artwork, logo path, affiliation, or provenance changes are planned. The native adapter consumes resolved semantic roles only. | PASS |
| III. Measured Accessibility | Existing contrast gates remain authoritative. `egui_kittest` validates accessible names, focusable controls, selection state, error state, density, and pixel scaling using the generated adapter. | PASS |
| IV. Full-Kit Verification | `build_all.py`, `verify.py`, glyph validation, generated Rust tests, release certification, and deterministic rebuild checks cover every production brand. | PASS |
| V. Site Consumes Verified Kits | No parallel site design system is introduced. Native artifacts are generated kit output and site behavior remains sourced from verified kits. | PASS |
| VI. Spec-Driven Releases | S039 spec, plan, research, model, contracts, tasks, and verification evidence stay synchronized. Independent versions are recorded without publishing a release. | PASS |

Post-design re-check: the adapter remains a generated derivative, not a new brand authority. The Rust surface is deliberately idiomatic to egui and does not impose a renderer-neutral runtime abstraction. Version policy adds compatibility evidence without forcing synchronized releases. No constitutional exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/039-egui-adapter-version-contracts/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── egui-adapter.md
│   └── version-compatibility.md
├── checklists/
│   ├── requirements.md
│   └── native-version-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
skill/
├── SKILL.md
├── references/
│   ├── consumer-contract.schema.json
│   └── version-policy.json
└── templates/
    ├── gen_egui.py
    ├── build_kit.py
    ├── interface_contract.py
    ├── verify.py
    ├── test_egui_adapter.py
    ├── test_interface_contract.py
    └── test_pipeline.py
scripts/
├── release_contract.py
├── test_package_release.py
└── test_release_contract.py
.github/workflows/build.yml
```

Generated and never committed:

```text
dist/<brand>/native/egui/
├── Cargo.toml
├── Cargo.lock
├── README.md
├── adapter.json
├── support-matrix.json
├── version-policy.json
├── src/
│   ├── lib.rs
│   ├── tokens.rs
│   └── components.rs
└── tests/
    └── adapter.rs
```

**Structure Decision**: Keep independent version policy in one governed JSON reference, generation in one dedicated Python template, and all generated Rust under `native/egui/`. The crate exposes egui-native functions and types while JSON manifests provide language-neutral traceability. The existing recipe catalog remains shared authoring input, not a runtime cross-renderer DSL.

## Complexity Tracking

No constitution violations require justification.
