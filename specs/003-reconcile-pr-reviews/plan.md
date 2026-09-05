# Implementation Plan: Review Reconciliation and Foundation Certification

**Branch**: `codex/003-reconcile-pr-reviews` | **Date**: 2026-09-03 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/003-reconcile-pr-reviews/spec.md`

## Summary

Reconcile all 19 unresolved Codex findings inherited from merged pull requests #16 and #26, correct any behavior that still fails on the current `origin/main` baseline, and produce a public evidence ledger that supports issue-level certification. Use that same verified build to close the largest defensible group of completed work-order issues while preserving release, deployment, and staging work as open. Publish the result in an official pull request, process the automatic Codex review and exactly one explicit second round, wait for green required checks, and return the still-open pull request to the owner for merge.

## Technical Context

**Language/Version**: Python 3.8 minimum and Python 3.12 current verification; TypeScript/React under Node.js 20 minimum and Node.js 24 CI

**Primary Dependencies**: coloraide, fonttools, Pillow, svgelements, Playwright Chromium, Next.js, pnpm, ImageMagick, Poppler, librsvg

**Storage**: Committed JSON, Markdown, SVG, CSS, font, and source files; generated `dist/` and `site/out/` artifacts remain uncommitted

**Testing**: Python `unittest`, generator verification, glyph validation, Markdown policy checks, Next.js lint/type/static export, release packaging assertions, hosted GitHub Actions

**Target Platform**: Windows development, Ubuntu GitHub Actions, static GitHub Pages, offline-capable consumer projects

**Project Type**: Source-driven brand asset generator, portable skill, static documentation site, and GitHub release pipeline

**Performance Goals**: Complete six-kit and site verification in one CI run; no performance regression beyond the existing protected workflow budget

**Constraints**: UTF-8 without BOM, LF line endings, Python 3.8-compatible syntax and APIs, hidden non-interactive Windows subprocesses, source-only repository, non-exemptable WCAG AA, no private operational data, two Codex rounds maximum, no merge/tag/release/deployment in S003

**Scale/Scope**: 19 inherited findings, 37 candidate child issues, 6 candidate phase parents, 6 build targets, 5 production registries, and 1 official S003 pull request

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Gate | Plan evidence | Result |
|---|---|---|---|
| I. Sources are committed, artifacts are rebuilt | Corrections land in generators or source, and evidence comes from fresh builds | Clean rebuild and generated-output diff checks are required before publication | PASS |
| II. Geometry is identity | No mark is redrawn or simplified while addressing review findings | Existing geometry and glyph gates remain mandatory; the slice changes only reproduced behavior | PASS |
| III. Accessibility has no exemption | No contrast, form, or semantic check is weakened | Native required state, CTA semantics, WCAG verification, and current tests remain required | PASS |
| IV. Verify before publish | Local and hosted verification precede handoff | Focused regressions, six-kit build, site export, packaging, clean rebuild, and required PR checks are gates | PASS |
| V. The site consumes generated kits | Site evidence must derive from verified generated output | `scripts/prepare_site.py` and static export are exercised after rebuilding kits | PASS |
| VI. Specifications and releases move together | S003 decisions and evidence are recorded without creating a release | Complete Spec Kit artifacts and changelog note ship in the PR; release issues stay open | PASS |

Post-design re-check: PASS. The review and issue-evidence contracts strengthen principles I, IV, and VI without introducing a constitutional exception.

## Technical Approach

1. Capture an immutable baseline ledger for the 19 inherited source threads, their linked issues, the current `origin/main` commit, and the current open issue hierarchy.
2. Run focused review-finding tests before changing production code. Reproduce any remaining failure and add a failing regression before its smallest proportional fix.
3. Run the complete six-kit pipeline, site export, release packaging dry run, encoding and sensitive-data scans, plus an isolated clean-checkout rebuild.
4. Record each finding's test, implementation commit, current result, source-thread reply, and resolution in `evidence.md` and its GitHub issue.
5. Evaluate each work-order candidate independently. Close only candidates whose complete published acceptance criteria are demonstrated on current `main`; retain open issues with an explicit missing-proof statement.
6. Update eligible phase parents only after their entire child sets are evidence-backed and closed. Preserve program, release, deployment, and staging parents that remain incomplete.
7. Commit, push, and open the official S003 pull request with a two-entry review-round ledger.
8. Process automatic round 1 completely, post one and only one `@Codex` request for round 2, process round 2 completely, and wait for green required checks.
9. Halt with the pull request open for the owner's final review and merge ritual.

## Architecture Decisions

- GitHub Issues remain the public project-management source of truth. The committed S003 evidence ledger provides reproducible technical detail and links outward rather than replacing GitHub state.
- Review-thread status and issue status are related but separate. A thread can be resolved after branch verification, while an issue requiring current-main evidence remains open until its fix is merged.
- The verified base is the remote integration commit used to create the worktree. A divergent local `main` is neither rewritten nor treated as authoritative.
- Aggregate CI is necessary but insufficient for issue closure. Each candidate gets acceptance-criterion-specific evidence.
- Generated artifacts are evidence only when rebuilt from committed sources in the current run. Stale artifacts are deleted by the generator or rejected.
- Review requests form a bounded state machine: automatic round 1, one manual round 2, complete. There is no transition that triggers round 3.
- Existing S002 artifacts are historical records. S003 adds an explicit supersession note for stale operational completion claims instead of silently rewriting history.

## Project Structure

### Documentation (this feature)

```text
specs/003-reconcile-pr-reviews/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── issue-evidence.md
│   └── review-ledger.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Repository surfaces under verification

```text
.github/workflows/        # protected build, Pages, and release workflows
assets/fonts/             # canonical local fonts and OFL notices
brands/                   # five production source kits and UI provenance
fixtures/<retired>/       # synthetic sixth build target used at that time
scripts/                  # orchestration, Markdown, packaging, and site preparation
site/                     # generated-kit consumer and static export
skill/                    # portable brandbuilder source, templates, tests, and canon
specs/002-publication-completion/ # historical predecessor with supersession note
```

**Structure Decision**: Keep corrections in the existing generator, test, workflow, site, or documentation surfaces. Add only S003 planning and evidence documents; do not introduce a new runtime service or duplicate source of brand truth.

## Verification Strategy

- Run all existing focused review regressions in `skill/templates/test_pipeline.py` and add new tests before any still-needed correction.
- Run glyph tests and validation so behavioral corrections cannot alter identity geometry.
- Exercise core-tier skip and full-tier failure behavior explicitly, including stale-output cleanup.
- Rebuild all six sources and require zero verification problems and zero glyph failures.
- Prepare and export the site from freshly generated kits, then inspect required route and registry manifests.
- Dry-run release packaging and inspect the exact seven expected archives without tagging or publishing.
- Repeat documented build steps from a separate clean checkout with only repository-declared dependencies.
- Scan new public prose for forbidden private paths, provider identifiers, secrets, BOMs, CRLF, mojibake, and governed Markdown violations.
- Require all hosted pull-request checks to succeed after the final review correction commit.

## Complexity Tracking

No constitutional violations or added architectural layers require justification.
