# Implementation Plan: Hosted ZIP MIME Compatibility

**Branch**: `codex/031-zip-mime-alias` | **Date**: 2026-09-12 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/031-zip-mime-alias/spec.md`

**Note**: This template is filled in by the `$speckit-plan` command; its definition describes the execution workflow.

## Summary

Extend the existing extension-specific payload contract so ZIP downloads accept both `application/zip` and GitHub Pages' observed `application/x-zip-compressed` alias. Keep the media-type allowlist exact, preserve existing case and parameter normalization, and retain the independent ZIP opening-signature and end-record checks. Add focused regression cases for both valid aliases, malformed bodies under both aliases, and a valid archive under an unsupported type, then prove the shared contract through local and production-origin verification.

## Technical Context

**Language/Version**: JavaScript ES modules on Node.js 24.11.0; repository validation retains Python 3.8 compatibility where applicable

**Primary Dependencies**: Node.js built-in `path`, `url`, `buffer`, `assert`, and `node:test`; existing static-site verifier and GitHub Pages production origin

**Storage**: Static files and in-memory response bodies; no persistent application storage

**Testing**: Focused Node test suite for payload contracts; complete site test command; existing repository CI parity and production-origin verification

**Target Platform**: Local static verifier, GitHub Actions Linux build, and GitHub Pages at `brand.shruggie.tech`

**Project Type**: Static-site verification contract

**Performance Goals**: Preserve one linear payload inspection per fetched file with no additional network request or archive extraction

**Constraints**: Accept exactly two ZIP media types; keep ZIP signature and end-record validation fail-closed; preserve non-ZIP behavior; do not modify generated artifacts or identity sources

**Scale/Scope**: One media-type allowlist entry, one focused test module, eight production brand ZIP downloads through the existing shared verifier

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **P1, sources and artifacts**: PASS. Only verifier source, tests, specification artifacts, and changelog prose may be committed. Generated kits and site output remain ignored.
- **P2, identity geometry**: PASS. The slice changes no brand source, logo path, proof, renderer, or approval record.
- **P3, accessibility**: PASS. No rendered interface changes; the full site accessibility gate remains required.
- **P4, verification before publication**: PASS. The correction removes a false metadata rejection while retaining independent ZIP body evidence and all publication gates.
- **P5, generated site consumption**: PASS. The verifier continues to inspect the generated site tree through the existing preparation and build workflow.
- **P6, Spec Kit and releases**: PASS. S031 maintains synchronized specification, plan, tasks, evidence, tests, and changelog artifacts and creates no release.
- **Security and process**: PASS. The allowlist remains exact, malformed bodies fail closed, and the production-origin restriction is unchanged.

Post-design re-check: PASS. The payload contract defines an exact two-value allowlist plus mandatory structural evidence and introduces no constitutional exception.

## Project Structure

### Documentation (this feature)

```text
specs/031-zip-mime-alias/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
├── checklists/
├── evidence.md
└── tasks.md
```

### Source Code (repository root)

```text
site/
├── scripts/
│   └── payload-contract.mjs          # Extension-specific media-type and body validation
└── tests/
    └── payload-contract.test.mjs     # Positive and fail-closed ZIP regression cases

CHANGELOG.md                           # Unreleased correction and contract decision
```

**Structure Decision**: Keep the correction inside the existing shared payload validator used by both local and production-origin verification. Extend its declarative ZIP allowlist and its focused tests instead of adding hosting-specific branches, response rewriting, or a second verifier.

## Complexity Tracking

No constitution violations require justification.
