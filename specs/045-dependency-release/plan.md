# Implementation Plan: Dependency Integration and 2.0.1 Release

**Branch**: `codex/045-dependency-release` | **Date**: 2026-09-22 | **Spec**: [spec.md](spec.md)

## Summary

Integrate both open Dependabot site groups into one tested release slice, correct the CI browser provisioning mismatch exposed by the tooling update, and deliver a review-complete `v2.0.1` release candidate. The owner performs final review and merge; only the merged main commit can be tagged because release preflight enforces main ancestry.

## Technical Context

**Language/Version**: Python 3.8+ verifier, Python 3.12 and Node 24.11.0 hosted build, TypeScript site

**Primary Dependencies**: Next 16.3.5, React/React DOM 19.3.0, Playwright Node 1.63.0, Playwright Python 1.62.0, Tailwind 4.3.3, Fumadocs Core/UI 16.15.11 and MDX 15.4.1, TypeScript 7.0.2

**Storage**: Committed `site/package.json` and `site/pnpm-lock.yaml`; generated kits and site export remain ignored

**Testing**: Frozen install, Python workflow contract, full repository tests, site lint/build/test, all eight verified kits, release archive certification, GitHub CI and external reviews

**Target Platform**: GitHub Actions Ubuntu release builder and static public site

**Project Type**: Brand-kit compiler, documentation site, and release pipeline

**Performance Goals**: Keep the current build jobs and artifact flow; no added runtime request or page route

**Constraints**: Main-ancestry preflight, exact versioned release assets, WCAG 2.1 AA, immutable artwork, no committed generated files, no more than one additional Codex review round

**Scale/Scope**: Two Dependabot PRs, one combined site lockfile, one browser-install workflow step and regression test, one release candidate and final PR

## Constitution Check

*GATE: Passed before research and rechecked after design.*

| Principle | Plan evidence | Result |
| --- | --- | --- |
| P1. Sources committed, artifacts rebuilt | Commit manifest, lockfile, workflow, tests, docs only; rebuild `dist/` in CI. | PASS |
| P2. Identity geometry preserved | No brand sources or logo paths change. | PASS |
| P3. Accessibility non-exemptable | Retain full site accessibility and contrast gates. | PASS |
| P4. Verification precedes publication | TDD workflow contract, full candidate build, release preflight, green PR CI. | PASS |
| P5. Site consumes generated kits | Retain verified kit to site pipeline; no hand-patched export. | PASS |
| P6. Specs and releases move together | S045 records intake, tests, decisions, evidence and 2.0.1 release state; tag only after merge. | PASS |

### Post-design recheck

The browser-install correction preserves all existing fail-closed gates. No constitution exception is needed. Release preflight remains the authority for tag ancestry and certified assets.

## Project Structure

```text
specs/045-dependency-release/{spec.md,plan.md,research.md,data-model.md,quickstart.md,tasks.md,evidence.md,checklists/,contracts/}
site/{package.json,pnpm-lock.yaml}
.github/workflows/build.yml
.github/dependabot.yml
scripts/test_publication_workflow.py
CHANGELOG.md
```

**Structure Decision**: Keep direct dependency changes in the site manifest and generated lockfile. Modify only the existing verified workflow's browser installation step and its existing contract test. Avoid a separate release workflow or generated artifact edit.

**Maintenance note**: Dependabot's configured `site` and `skill` labels do not exist, while `area: site` and `area: generator` do. Align the configuration to the existing taxonomy so future dependency PRs receive useful area labels.

## Delivery Sequence

1. Capture the exact two PR heads and direct version changes; write a failing CI regression for the two browser clients.
2. Integrate both direct dependency groups and regenerate the frozen lockfile, then make the CI browser installation satisfy both Python and Node versions without browser garbage collection removing either.
3. Run focused and full validation, record evidence, and update dated release decisions and notes.
4. Commit and push S045, open one official PR, process initial reviews and optionally one additional Codex review round, then wait for green CI.
5. Ask the owner for final review and merge. After merge, verify the exact main commit, push `v2.0.1`, and watch official release publication and assets.

## Decision Log

### 2026-09-22 - Integrate both Dependabot PRs in one slice

The two updates touch the same manifest and lockfile. One combined candidate tests their interaction and gives the owner one release gate. The PR records exact source heads; after merge, the redundant bot PRs can be closed as superseded.

### 2026-09-22 - Provision both Playwright browser revisions

The site test client advances to 1.63.0 while the Python kit verifier remains at 1.62.0. Playwright requires a browser revision matching each client. Install both revisions and suppress install-time browser garbage collection for the shared job. This avoids an unrelated Python dependency bump and preserves full-tier PDF evidence.

### 2026-09-22 - Pair Fumadocs MDX with compatible Core and UI

The combined build exposed that MDX 15.4.1 calls the new `fumadocs-core/server` export, absent from Core 16.14.3. MDX declares Core `^16.15.3`. Advance Core and UI together to 16.15.11 and verify the generated documentation and all site routes. Keeping the old Core would reproduce a broken public site despite a resolved lockfile.

### 2026-09-22 - Tag only the merged main revision

The publisher's release preflight explicitly checks that the tag commit is an ancestor of `origin/main`. A pre-merge tag would fail and could publish an unreviewed revision if that gate were weakened. Prepare the PR and request the owner's merge first, then tag the exact merged commit and let the existing workflow publish it.

## Complexity Tracking

No constitution violation or new release subsystem is introduced.
