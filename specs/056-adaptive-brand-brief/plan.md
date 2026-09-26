# Implementation Plan: Adaptive Brand Brief and Two Approval Gates

**Branch**: `codex/056-adaptive-brand-brief` | **Date**: 2026-09-25 | **Spec**: [spec.md](spec.md)

## Summary

Replace the minimal-input interview with adaptive discovery and a reusable brief. Align the skill, generated ambient instructions, logo protocol, continuity guide, and hosted manual around exactly two source-bound creative approvals. Define a private Gate 2 review packet with explicit social copy and a distinct social-image preview before final kit compilation. The generator-wide social-image migration remains in #281.

## Technical Context

- **Language/Version**: Markdown guidance, Python 3.8 minimum for contract checks, Node 20 minimum for site validation.
- **Dependencies**: Existing approval ledger, continuity record, generated documentation catalog, and private kit review path.
- **Storage**: Source references in `skill/references/`; approval evidence remains in source records and ignored private review output.
- **Testing**: Python workflow-contract tests, full `scripts/build_all.py`, kit verification, site lint/build/test, Spec Kit analysis.
- **Constraints**: No retrospective approval, no shipped logo geometry change, no generated `dist/` commit, WCAG 2.1 AA, UTF-8 LF.
- **Scale**: Future brand authoring and the hosted/manual reference projections; current approved sources remain stable.

## Constitution Check

- **P1**: Commit source instructions and tests only. Private review output stays ignored.
- **P2**: No logo source bytes change; Gate 1 stays source-bound.
- **P3**: Existing accessibility gates remain mandatory.
- **P4**: Full build and kit gates precede any release claim.
- **P5**: The hosted manual consumes packaged reference files.
- **P6**: Numbered Spec Kit artifacts and release notes accompany the change.

## Project Structure

```text
specs/056-adaptive-brand-brief/     spec, plan, tasks, analysis, evidence
skill/SKILL.md                      authoring entry point
skill/AGENTS.md                     generated ambient entry point
skill/references/03-interview.md    adaptive discovery workflow
skill/references/06-logo-protocol.md and identity-continuity.md approval mapping
skill/references/03-interview.md reusable brief and packet record
skill/templates/authoring_brief.py   private brief and review-packet validator
skill/templates/test_pipeline.py    workflow regression checks
CHANGELOG.md and skill/CHANGELOG.md migration notes
```

## Delivery Decisions

1. Reuse `approval_ledger.gate_1` and `gate_2`. A third approval record would contradict the owner decision. Direction selection and discussion are ordinary discovery.
2. Keep the brief private working evidence. Do not put unresolved creative claims into published brand contracts.
3. Review provisional private derivatives at Gate 2. The source-specific approval manifest binds what was reviewed. Final compilation follows explicit Gate 2 approval and normal verification.
4. Require exact approved social copy in the brief and review packet. #281 owns the dedicated final image role and migration of eight published brands; this slice cannot claim their ambiguous `descriptor` or `brand_idea` is approved slogan copy.

## Verification

Run documentation and approval tests, then all required CI-parity checks. Check generated `skill/AGENTS.md` synchronization, packaged manual inclusion, LF/no-BOM, and mojibake. Record actual results in `evidence.md`.
