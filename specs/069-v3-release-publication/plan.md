# Implementation Plan: BrandBuilder 3.0.0 Release Publication

**Branch**: `codex/069-v3-release-publication` | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

## Summary

Finalize the existing BrandBuilder 3.0.0 candidate to include S068's merged documentation changes, validate its complete source and asset contract, then publish one exact tagged release and matching site through the current CI pipeline.

## Technical Context

**Language/Version**: Python 3.8 minimum; GitHub CI Python 3.12 and pinned Node 24/26 renderers
**Primary Dependencies**: Existing BrandBuilder release contract, generated kits, static site, GitHub Actions
**Storage**: Tracked changelog, release-impact and release-contract source, Spec Kit evidence only; generated output ignored
**Testing**: Release contract and publication tests, full eleven-kit and site validation, exact PR and tag CI
**Target Platform**: GitHub Release and GitHub Pages
**Project Type**: Brand compiler, generated kit catalog, static documentation
**Performance Goals**: No new CI job or unnecessary repeat of the long build
**Constraints**: Exact source revision and checksums, no identity geometry changes, WCAG 2.1 AA, no generated files in Git
**Scale/Scope**: Eleven verified hosted brands, eight official brand archives, one 3.0.0 release

## Constitution Check

| Principle | S069 treatment | Result |
| --- | --- | --- |
| P1 source and artifact boundary | Commit metadata and Spec Kit files only; CI rebuilds outputs. | PASS |
| P2 identity geometry | No brand logo source edits. | PASS |
| P3 accessibility | Full kit and site AA gates remain required. | PASS |
| P4 verification | Exact candidate and tag gates precede publication. | PASS |
| P5 generated kit site | Eleven site brands remain copied from verified kits. | PASS |
| P6 specification and release | S069 spec, plan, tasks, analysis, and evidence bind `v3.0.0`. | PASS |

**Post-design recheck**: The existing release workflow supplies every required build and provenance gate. No constitutional exception is needed.

## Project Structure

```text
specs/069-v3-release-publication/{spec.md,plan.md,research.md,data-model.md,quickstart.md,tasks.md,analysis.md,verification.md,contracts/,checklists/}
CHANGELOG.md
scripts/release_contract.py
skill/references/release-impact.json
specs/068-brand-essentials-docs-navigation/verification.md
```

**Structure Decision**: Update the current release metadata and evidence in place. The CI publisher already builds exact-tag release assets and Pages from the same source revision.

## Delivery Sequence

1. Align changelog, migration notes, release impact, and S068 verification evidence with the merged source.
2. Run focused release and documentation contract checks; verify the candidate asset inventory and source-only diff.
3. Push one S069 PR, finish the two-round Codex protocol and security review, and require all authoritative PR checks green.
4. Merge the exact reviewed head; verify `main` ancestry and green candidate; create and push `v3.0.0` on that commit.
5. Observe tag preflight, release upload, and Pages deploy; verify GitHub assets, checksums, release notes, site version link, and eleven-brand inventory.

## Decision Log

### 2026-09-29 - Keep the untagged 3.0.0 identity

BrandBuilder 3.0.0 already carries S067 and was not published. S068 is merged and can be included in the final 3.0.0 candidate without reusing an immutable public version. The release notes and impact record must identify both slices.

### 2026-09-29 - Preserve eight formal archives and eleven hosted kits

The release allowlist and publication tests distinguish GitHub release archives from client site downloads. S069 maintains that boundary and makes it explicit in notes and verification rather than expanding publication semantics while cutting the release.

## Complexity Tracking

No constitutional exception or new publication subsystem.
