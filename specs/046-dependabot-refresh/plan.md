# Implementation Plan: Post-Merge Dependabot Refresh

**Branch**: `codex/046-dependabot-refresh` | **Date**: 2026-09-22 | **Spec**: [spec.md](spec.md)

## Summary

Combine five workflow-action and three Python dependency updates opened immediately after the S045 merge, adjust the immutable-action regression contract and accurate release comments, then validate one candidate before the owner merges and the 2.0.1 tag is published.

## Technical Context

**Language/Version**: Python 3.8 minimum, Python 3.12 hosted build, Node 24.11.0 proof and site jobs

**Primary Dependencies**: Five SHA-pinned GitHub Actions, fontTools 4.65.0, Playwright Python 1.63.0, pikepdf 10.13.0.post1

**Storage**: Tracked `requirements.txt`, workflow YAML, regression test, changelog, and Spec Kit source files only

**Testing**: Immutable-action contract, Python 3.8 compatibility, all production kit/glyph verifiers, site lint/build/a11y, archive certification, GitHub Build checks

**Target Platform**: GitHub Actions Ubuntu/Windows and static release publisher

**Project Type**: Brand-kit compiler, documentation site, release pipeline

**Performance Goals**: No additional job or public site route

**Constraints**: Immutable source pins, no credential persistence, exact checkout revision, WCAG 2.1 AA, no identity geometry change, no generated artifacts in Git, owner merge before tag

**Scale/Scope**: Eight bot PRs, one coordinated follow-up PR, existing `v2.0.1` release

## Constitution Check

| Principle | Evidence | Result |
| --- | --- | --- |
| P1. Sources only | Edit tracked source and tests; rebuild outputs. | PASS |
| P2. Identity geometry | No brand or logo edits. | PASS |
| P3. AA floor | Preserve site and kit accessibility gates. | PASS |
| P4. Verify before publication | Existing full gate and fail-closed action contract remain required. | PASS |
| P5. Generated-kit consumption | No site source or artifact flow change. | PASS |
| P6. Specs and releases | S046 records the post-merge intake, evidence, decision, and final tag gate. | PASS |

**Post-design recheck**: No new subsystem, exception, or gate waiver is planned.

## Project Structure

```text
specs/046-dependabot-refresh/{spec.md,plan.md,research.md,data-model.md,quickstart.md,tasks.md,evidence.md,checklists/,contracts/}
.github/workflows/build.yml
requirements.txt
scripts/test_publication_workflow.py
CHANGELOG.md
```

**Structure Decision**: Preserve the current publication workflow and update its pinned-action allowlist in the existing contract test. Keep Python 3.8 pins unchanged through environment markers.

## Delivery Sequence

1. Capture eight bot heads and verify action pins against upstream release tags; record focused failing contract evidence.
2. Apply all compatible direct updates, accurate version comments, and reviewed SHA expectations; run focused tests.
3. Run the full documented local gate, record evidence and release notes, then push one traceable PR.
4. Address review comments, wait for green CI, and ask the owner to merge. After merge, close redundant bot PRs and publish the exact merged commit as `v2.0.1`.

## Decision Log

### 2026-09-22 - Defer the S045 tag until the new intake is complete

Eight new bot PRs arrived after #241 merged and before `v2.0.1` existed. Tagging immediately would contradict the user's explicit request to finish the open bot queue. A small S046 follow-up keeps the release on one tested main revision while preserving the owner's final merge ritual.

### 2026-09-22 - Update action policy and comments together

Standalone action PRs fail the intentionally pinned immutable-source contract. Keeping that gate and updating approved SHAs together with exact upstream version comments is safer than weakening the contract. The existing comments for three actions were stale, so the same slice corrects them as part of source-provenance integrity.

## Complexity Tracking

No constitutional exception or architecture expansion.
