# Implementation Plan: Verified Publication Pipeline

**Branch**: `codex/030-verified-publication-pipeline` | **Date**: 2026-09-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/030-verified-publication-pipeline/spec.md`

**Note**: This template is filled in by the `$speckit-plan` command; its definition describes the execution workflow.

## Summary

Replace three independently restated hosted build paths with one same-run verified publication pipeline in the existing Build workflow. Pull requests produce all verified kit, release-candidate, and Pages artifacts without external publication; successful main pushes deploy the exact Pages artifact; authorized `v*` tag pushes publish the exact certified release candidate. Preserve the Windows-approved identity proof bundle, exact Node 24.11.0 and resvg 2.6.2 contract, the required `build` status context, and all existing verification gates. Remove the obsolete Pages and Release workflows, isolate write and OIDC permissions to checkout-free publisher jobs, SHA-pin external actions, and add fail-closed workflow and artifact-boundary regressions.

## Technical Context

**Language/Version**: GitHub Actions YAML; Python 3.8 compatibility and Python 3.12 hosted builds; Node.js 24.11.0; pnpm 10.28.2

**Primary Dependencies**: GitHub-hosted Ubuntu and Windows runners, GitHub Actions artifacts, GitHub Pages, GitHub Releases, `@resvg/resvg-js` 2.6.2, existing repository build and verification scripts

**Storage**: Same-run immutable GitHub Actions artifacts for approved proofs, verified kits, the Pages tarball, and the release candidate; no persistent application storage

**Testing**: Python `unittest` workflow-contract and publication-artifact regressions; existing Python compatibility, generator, release, continuity, site preparation, TypeScript, static export, browser, payload, origin, WCAG, and repository-hygiene gates; pinned `actionlint` syntax validation

**Target Platform**: GitHub Actions, GitHub Pages at `brand.shruggie.tech`, and GitHub Releases

**Project Type**: CI/CD orchestration for a Python generator and statically exported Next.js site

**Performance Goals**: One expensive verified build per pull-request revision, main revision, or version tag; no second Pages or Release rebuild; hosted completion remains within the current approximately 30-minute verification envelope

**Constraints**: Preserve required check name `build`; preserve exact canonical proof hashes and renderer settings; generated outputs stay uncommitted; pull requests receive no publisher credentials; Pages deploys only main; releases publish only verified `v*` tags whose commit is on main; no test release tag

**Scale/Scope**: Three existing workflows converge into one; eight production brands and the current nine-file v1.2.1 release candidate; one production Pages environment and one release publisher

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **P1, sources and artifacts**: PASS. Only workflow, test, specification, and changelog sources are committed. Proof, kit, site, and release outputs remain ephemeral or ignored.
- **P2, identity geometry**: PASS. No brand source, renderer tolerance, proof hash, approval record, or geometry changes are permitted.
- **P3, accessibility**: PASS. The existing browser and WCAG 2.1 AA site gate remains part of the authoritative build before Pages eligibility.
- **P4, verification before publication**: PASS. Both publisher jobs depend on the same complete verified build and consume its artifacts without rebuilding.
- **P5, generated site consumption**: PASS. The Pages artifact is produced only after verified kits feed site preparation, static export, payload tests, and browser verification.
- **P6, Spec Kit and releases**: PASS. S030 carries synchronized Spec Kit artifacts, release certification remains mandatory, and no tag or release is created by the slice.
- **Permissions and process**: PASS. Verification uses read-only permissions; write and OIDC capabilities exist only in event-guarded publisher jobs that do not checkout or execute repository code.

Post-design re-check: PASS. The artifact and event contracts preserve every gate and introduce no constitutional exception.

## Project Structure

### Documentation (this feature)

```text
specs/030-verified-publication-pipeline/
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
.github/workflows/
└── build.yml                         # Authoritative validation, artifact production, and guarded publishers

scripts/
├── test_publication_workflow.py      # Workflow, trigger, permission, and artifact-lineage contract
└── audit_publication_artifacts.py    # Symlink and hidden-file allowlist before artifact upload

specs/030-verified-publication-pipeline/
└── [artifacts listed above]

CHANGELOG.md                          # Unreleased fix and dated CI architecture decision
```

**Structure Decision**: Retain `build.yml` as the single top-level workflow so the active ruleset's exact `build` context remains stable and every event uses one same-run artifact boundary. Delete `pages.yml` and `release.yml` after their event-specific publication behavior moves into guarded downstream jobs. Add only focused root-level Python contract and artifact-audit scripts because workflow YAML has no native reusable assertion layer and the existing release tests already inspect workflow source.

## Complexity Tracking

No constitution violations require justification.
