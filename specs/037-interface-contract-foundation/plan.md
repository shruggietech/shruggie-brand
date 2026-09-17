# Implementation Plan: Interface Contract Foundation

**Branch**: `codex/037-interface-contract-foundation` | **Date**: 2026-09-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/037-interface-contract-foundation/spec.md`

## Summary

Add a versioned renderer-neutral Interface Canon beside the existing Brand Canon, validate its aliases, runtime capabilities, accessibility pairs, and brand override boundaries before generation, and deliver the exact resolved contract inside every generated kit. Replace prompt-shaped routing with deterministic Author, Implementation, and Audit policy plus behavioral fixtures synchronized across `SKILL.md` and `AGENTS.md`. Extend enforcement generation with a concise merge-safe governed block, deeper implementation guidance, a machine-readable consumer contract, checksummed provenance, a bundled exact BrandBuilder distribution for offline recovery, and a reusable capability-gap template. Extend production verification and release archive certification so malformed authority, integrity drift, unsafe recovery, and non-deterministic regeneration fail closed.

## Technical Context

**Language/Version**: Python 3.8-compatible generator, validation, routing, and verification code; JSON Schema draft 2020-12 documents; Markdown host instructions

**Primary Dependencies**: Python standard library, existing `coloraide` accessibility dependency, existing deterministic ZIP and SHA-256 helpers, current brand contract and verification pipeline

**Storage**: Versioned JSON source contracts, JSON Schemas, generated Markdown instructions, generated JSON manifests, and a deterministic nested `.skill` archive; no database

**Testing**: Python `unittest`, production `verify.py`, `validate_glyph.py`, release archive certification, skill-to-AGENTS synchronization, all-production-kit builds, and full site CI parity

**Target Platform**: Claude-compatible skill metadata, Codex and bare-checkout ambient instructions, Web and future native renderers, Windows and Linux build hosts, offline consumer handover

**Project Type**: Static brand-interface compiler and generated consumer-contract toolchain

**Performance Goals**: Validate canon and runtime profiles in linear time over their small contract graphs; generate one deterministic exact-version bundle per kit; add no network dependency to routine build or verification

**Constraints**: Python 3.8 minimum, UTF-8 without BOM and LF, offline routine generation, no operating-system-based capability inference, no committed `dist/` or release artifacts, preserve approved identity geometry and affiliation, WCAG 2.1 AA floor, hidden non-interactive child processes

**Scale/Scope**: Seven release-certified production brands plus the I Heart PR Tours production source, three operating modes, thirteen normalized runtime inputs, three renderer transforms, and one generated consumer contract per kit

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

| Principle | Plan alignment | Result |
| --- | --- | --- |
| P1. Commit sources and rebuild artifacts | Only canon, schema, templates, tests, instructions, changelog, workflow documentation, and S037 records are committed. Generated kits, nested distributions, archives, PDFs, and registries remain ignored. | PASS |
| P2. Preserve identity geometry and provenance | Interface resolution reads governed brand values and affiliation boundaries without modifying logo paths, source bytes, approvals, or inheritance. Unsupported cross-boundary overrides fail. | PASS |
| P3. Accessibility is not exemptable | Invariant focus, target, motion, and contrast requirements cannot be overridden. Declared state pairs are measured for every production brand. | PASS |
| P4. Verification precedes publication | Canon, consumer-contract, governed-block, checksum, recovery, and archive gates join `verify.py` and release certification. All kits still require zero verification and glyph failures. | PASS |
| P5. The site consumes generated kits | This slice changes generated kit contracts only. Existing site preparation continues to consume verified `dist/` bytes and receives full regression coverage through the current CI matrix. | PASS |
| P6. Specifications and releases move together | Spec, clarification, checklists, plan, research, model, contracts, tasks, analysis, evidence, implementation, and changelog are maintained together. S037 does not tag, publish, or claim release certification. | PASS |

Post-design re-check: PASS. The design adds a separate contract layer without duplicating Brand Canon authority, introduces no renderer implementation, preserves identity sources, and strengthens verification and offline handover.

## Project Structure

### Documentation (this feature)

```text
specs/037-interface-contract-foundation/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── consumer-contract.md
│   ├── interface-canon.md
│   └── routing-policy.md
├── checklists/
│   ├── authority-portability.md
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
skill/
├── SKILL.md
├── AGENTS.md
├── references/
│   ├── interface-canon.json
│   ├── interface-canon.schema.json
│   ├── consumer-contract.schema.json
│   ├── operating-modes.md
│   └── routing-fixtures.json
└── templates/
    ├── interface_contract.py
    ├── gen_enforcement.py
    ├── build_kit.py
    ├── verify.py
    ├── test_interface_contract.py
    └── test_pipeline.py

scripts/
├── release_contract.py
└── test_package_release.py

.github/workflows/build.yml
CONTRIBUTING.md
CHANGELOG.md
```

**Structure Decision**: Keep the Interface Canon and consumer schemas in the existing portable `skill/references/` authority surface, place shared validation, resolution, routing, deterministic bundling, and merge logic in one standard-library-first template module, call it from existing generator and verifier entry points, and certify the delivered files through the existing manifest and release archive paths. Do not create a second compiler, separate package, renderer adapter, or brand-specific override implementation.

## Complexity Tracking

No constitution violations or justified complexity exceptions are required.

## Implementation Strategy

1. Add failing contract tests for canon structure, alias resolution, cycles, required roles, runtime profiles, accessibility state pairs, override boundaries, operating-mode routing, host instruction equivalence, deterministic consumer generation, governed-block merging, and offline recovery.
2. Implement `interface_contract.py` with bounded JSON loading, reference resolution, validation, production-brand defaults, capability-profile validation, contextual routing, deterministic exact-version archive generation, checksums, and fail-closed block merging.
3. Add source canon, schemas, mode guidance, and fixtures. Integrate interface validation into the first brand validation gate before publishable output.
4. Extend enforcement output with the concise governed `AGENTS.md` block, `IMPLEMENTATION.md`, copied Interface Canon, consumer manifest, gap template, and exact bundled `.skill` distribution.
5. Extend production verification and archive certification to validate field semantics, provenance checksums, instruction markers, exact recovery bytes, safe paths, and declared version agreement.
6. Synchronize ambient `skill/AGENTS.md`, run all production builds and the complete CI matrix, reconcile analysis, document evidence, commit, push, open the S037 pull request, and complete no more than two external review rounds.

## Decision Record

- Keep Brand Canon and Interface Canon separate. Brand Canon owns identity, affiliation, colors, typography, provenance, and artwork. Interface Canon owns renderer-neutral semantic UI roles, logical measures, runtime capabilities, invariants, and permitted override mechanics.
- Define `canon_version` as the Brand Canon version, `interface_canon_version` as the Interface Canon version, `compiler_version` as the BrandBuilder skill version, and `brand_version` as the consumer brand contract version. The full compatibility matrix remains reserved for #218.
- Use explicit `$primitive`, `$alias`, `$brand`, `$brand_canon`, and `$resolved` references. Raw renderer properties and product composition do not enter the canon.
- Validate the complete alias graph before resolving any brand. Missing roles, unknown roles, invalid targets, cycles, inaccessible pairs, and unsupported or cross-affiliation overrides stop the first contract gate.
- Model environment facts as observed capabilities. The profile deliberately has no operating-system field, and mixed pointer, viewport, keyboard, and touch combinations remain valid.
- Generate a nested deterministic `.skill` archive inside each kit. This makes exact-version recovery and integrity verification possible using delivered bytes even when the host has no network or prior skill installation.
- Keep the generated repository entry concise. `enforcement/AGENTS.md` contains one marked governed block and points to `IMPLEMENTATION.md`; deterministic merge preserves unrelated human content and rejects duplicated or malformed markers without rewriting the file.
- Keep capability-gap creation local. The generated record carries complete traceability, while issue submission or upstream mutation remains outside the record and requires separate authorization.
- Use the existing final kit `manifest.json` for whole-kit integrity and a dedicated `enforcement/consumer-contract.json` for consumer authority, recovery, renderer and host semantics, contract provenance, and focused checksums.
