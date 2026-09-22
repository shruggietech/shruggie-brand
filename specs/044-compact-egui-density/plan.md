# Implementation Plan: Compact egui Desktop Density

**Branch**: `codex/044-compact-egui-density` | **Date**: 2026-09-21 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/044-compact-egui-density/spec.md`

## Summary

Correct the generated egui adapter's conflation of accessible touch targets with desktop visual control height. Preserve the canonical 44-unit target for touch, coarse, mixed, and unknown input profiles, but derive a compact fine-pointer height from the target minus the declared pointer hit-slop envelope. Tighten generated button padding and vertical item spacing, grow controls when text scaling requires it, add rendered-state regressions, publish the behavior as egui adapter patch 1.0.1 and BrandBuilder patch 2.0.1, and leave Web/React output, resource meters, brand sources, and identity geometry unchanged.

## Technical Context

**Language/Version**: Python 3.8+ generator and tests; generated Rust 1.95 using egui 0.36.1

**Primary Dependencies**: Repository Interface Canon resolver, component recipe catalog, generated egui crate, `egui_kittest` 0.36.1

**Storage**: Deterministic generated files in ignored temporary kit directories; no persistent application data

**Testing**: Python `unittest`, generated `cargo test --locked`, production `verify.py`, `validate_glyph.py`, full repository build and publication checks

**Target Platform**: Native desktop egui consumers with fine, coarse, mixed, unknown, and touch-capable input profiles

**Project Type**: Brand-system compiler and generated native adapter

**Performance Goals**: Constant-time style selection per application; no new allocation, network request, renderer, or background process

**Constraints**: Fine-pointer controls at most 28 points comfortable and 24 points compact at normal text scale; touch/coarse/mixed/unknown targets at least 44 points; compact row gap at most 2 points; all invalid transforms remain fail-closed; generated artifacts remain uncommitted; no identity or resource-meter change

**Scale/Scope**: One generator, one focused Python suite, one generated Rust suite, one version-policy compatibility update, eight production kits, and one downstream migration note

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

| Principle | Plan evidence | Result |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Change only generator source, tests, version policy, changelog, and Spec Kit artifacts. Keep generated crates, kits, site export, archives, and registries ignored. | PASS |
| P2. Identity geometry is preserved | Do not touch brand inputs, logo paths, approvals, or derived identity configuration. | PASS |
| P3. Accessibility has no exemption | Preserve the 44-unit target for touch and imprecise input, text-scale growth, focus behavior, accessible names, contrast, and invalid-input rejection. | PASS |
| P4. Verification precedes publication | Add failing generated-source and rendered-state regressions first, then run focused and full CI-parity gates including every production kit. | PASS |
| P5. The site consumes generated kits | Site bindings and Web/React output remain unchanged; rebuilt kits remain the source for any publication check. | PASS |
| P6. Specifications and releases move together | S044 records issue traceability, decisions, tasks, evidence, adapter version impact, implementation, and PR status. No release is cut. | PASS |

### Post-Design Re-check

The design preserves every non-exemptable accessibility and identity gate. The intentional deviation from S039 is bounded to native fine-pointer presentation: S039 treated the 44-unit touch target as an unconditional visible desktop size, while this slice uses observed input capabilities already present in the contract. Conservative profiles still receive 44 units, so no exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/044-compact-egui-density/
├── checklists/
│   └── requirements.md
├── contracts/
│   └── native-density.md
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
├── references/version-policy.json     # compiler-to-adapter compatibility
└── templates/
    ├── gen_egui.py                    # generated metrics and runtime style selection
    └── test_egui_adapter.py           # deterministic source/version regression

site/scripts/verify-site.mjs            # stable conformance-frame measurement gate

CHANGELOG.md                            # unreleased repository correction
skill/CHANGELOG.md                      # generated-skill correction
```

**Structure Decision**: Keep the correction entirely inside the existing native adapter generator and its focused regression suite. Reuse the canonical target, hit slop, density, pointer precision, touch, and text-scale inputs rather than adding brand-specific values or editing ESO Weave application source.

## Delivery Sequence

1. Record the current generator baseline and expected oversized-control failure.
2. Add Python source assertions and generated Rust rendered-state tests for compact fine-pointer controls, conservative targets, text-scale growth, padding, and dense row spacing.
3. Implement capability-aware style metrics in `gen_egui.py` without changing existing public function signatures.
4. Bump the egui adapter patch identity to 1.0.1, permit compiler major 2 to consume that exact adapter version, and assign changed generator output the immutable BrandBuilder 2.0.1 package identity.
5. Run focused Python and generated Cargo tests, then rebuild and verify every production kit and execute the complete documented CI-parity suite.
6. Record evidence, update changelogs, check UTF-8/LF/mojibake, commit, push, open the PR, process one Codex review round, and wait for all CI checks to pass.

## Decision Log

### 2026-09-21 - Separate visible desktop density from conservative targets

Use the canonical target minus two pointer-hit-slop margins as the fine-pointer comfortable control height, then apply the existing compact density multiplier. This produces 28 points comfortable and 22.96 points compact from the current 44/8 contract without inventing an ESO Weave-only size. Touch, coarse, mixed, and unknown input profiles retain 44 points.

### 2026-09-21 - Let scaled text grow controls

Compute the final minimum height as the larger of the profile target and the scaled body font plus twice the generated vertical button padding. This avoids clipped labels while keeping normal-scale desktop controls compact.

### 2026-09-21 - Tighten global row rhythm, preserve component-owned spacing

Derive horizontal item spacing and button padding from bounded fractions of `spacing.control.block`, and cap fine-pointer compact vertical item spacing at 2 points. Product sections and resource meters may add their own spacing, while repeated one-line logs no longer inherit a double-spaced default.

### 2026-09-21 - Publish as an adapter patch

Bump the egui adapter from 1.0.0 to 1.0.1 because public symbols and function signatures remain compatible and the version policy classifies corrected generated behavior without symbol changes as a patch. Advance BrandBuilder from 2.0.0 to 2.0.1 because the generated bytes and immutable kit package checksum change. The Brand, Interface Canon, component recipes, Web/React adapter, and approved identities do not change.

### 2026-09-21 - Synchronize conformance-frame measurement

Wait for the selected profile URL and completed same-origin iframe document before measuring browser conformance targets. Full verification exposed a deterministic detached-context race after the profile selector changed the iframe source. The synchronization keeps every existing geometry and WCAG assertion intact and changes no product presentation.

## Complexity Tracking

No constitution violation requires justification. The capability-aware branch uses runtime inputs already required by the Interface Canon and avoids a broader canon or recipe revision.
