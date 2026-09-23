# Implementation Plan: Repository Front Door and v2.0.3 Release Readiness

**Branch**: `codex/049-repository-front-door` | **Date**: 2026-09-23 | **Spec**: [spec.md](spec.md)

## Summary

Repair the root README using approved ShruggieTech assets and canonical site routes, replace fixed-version download names with an official latest-release entry point, and add a deterministic README link audit against the generated site route contract. Certify the unchanged 2.0.3 source candidate for formal release after owner merge.

## Technical Context

**Language/Version**: Python 3.8 minimum for the audit; Markdown and GitHub-compatible HTML for the README; Node.js 20 for existing site validation

**Primary Dependencies**: Python standard library, existing `site/generated/routes.json`, existing GitHub Actions and site build; no new dependency

**Storage**: Committed README, approved source images, audit code/tests, Spec Kit artifacts; ignored generated site output and release archives

**Testing**: Isolated temporary README/route fixtures, complete repository build and release-candidate verification, site tests, Markdown and publication audits

**Target Platform**: GitHub README light/dark rendering, repository CI, static brand site, exact-version release pipeline

**Project Type**: Brand-kit compiler and release-backed static documentation site

**Performance Goals**: The README audit runs locally from generated route data without network calls and completes in seconds

**Constraints**: Approved logo bytes and path geometry unchanged; WCAG 2.1 AA; no generated files committed; no consumer repository writes; publication only from merged exact tag

**Scale/Scope**: One root README, eight brand destinations, three status badges, one focused audit and test module, existing release candidate 2.0.3

## Constitution Check

| Principle | S049 treatment | Result |
| --- | --- | --- |
| P1 committed sources, rebuilt artifacts | Commit only README, scripts/tests, CI, and Spec Kit evidence; leave generated routes and archives ignored. | PASS |
| P2 preserve identity geometry | Embed existing approved light/dark logo PNGs without editing bytes. | PASS |
| P3 AA floor | Theme-specific logos, descriptive image text, readable prose and badge labels; no color waiver. | PASS |
| P4 verify before publication | Full production and site gates plus release-candidate certification before PR handoff. | PASS |
| P5 site consumes generated kits | README audit consumes the generated route contract rather than duplicating route definitions. | PASS |
| P6 specifications and releases move together | S049 spec/plan/tasks/evidence accompany CI and documentation changes; formal tag only after owner merge. | PASS |

**Security/isolation**: Resolve local destinations inside the repository root, reject encoded traversal and backslashes, require the exact trusted site host, and compare site URLs with generated canonical routes. Synthetic fixtures live in temporary directories. The repository has no authenticated tenant layer; brand-route completeness is its relevant isolation boundary.

**Post-design recheck**: All six principles remain satisfied. The CI workflow edit is in scope and will be recorded as a dated changelog decision.

## Project Structure

```text
README.md
CHANGELOG.md
scripts/check_readme_links.py
scripts/test_check_readme_links.py
.github/workflows/build.yml
brands/shruggietech/assets/{logo-lightbg.png,logo-darkbg.png}  # read-only
site/generated/routes.json                               # generated, ignored
specs/049-repository-front-door/{spec.md,plan.md,research.md,data-model.md,quickstart.md,tasks.md,evidence.md,contracts/,checklists/}
```

**Structure Decision**: Keep README link checking in one small standard-library script. Run its tests in the Python compatibility and verified-build jobs; run the actual README audit after the site generates its route contract. Do not add a live HTTP crawler or duplicate a brand slug manifest.

## Delivery Sequence

1. Add failing isolated tests for canonical routes, missing/unsafe local targets, lookalike host, omitted brand, and valid images/badges.
2. Implement the audit and CI invocation, then rebuild the README using approved theme-specific assets and stable release guidance.
3. Run focused tests, complete production and site validation, release-candidate certification, and encoding/hygiene checks; record evidence.
4. Commit and push the S049 branch, open issue-linked PR, process bot comments within two Codex rounds, and wait for green CI before owner handoff.
5. After owner merge, validate exact main commit and formal release tag; the existing tag-triggered pipeline must publish and certify v2.0.3 assets and checksums. This post-merge step is not represented as complete before merge.
