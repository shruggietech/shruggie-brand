# Implementation Plan: Generated Artifact Semantics

**Branch**: `codex/060-artifact-semantics` | **Date**: 2026-09-27 | **Spec**: [spec.md](spec.md)

## Summary

Resolve #269 by inventorying every generated data family, tightening a demonstrated empty-manifest defect, and binding kit records to copied public and staged release bytes. Reuse existing deep family validators, then test their composition at the publication boundary. Record guideline fact integrity overlap with #270 without claiming its content audit complete.

## Technical Context

**Language/Version**: Python 3.8 minimum for portable kit verification; repository scripts use Python 3.11+, Node 20 minimum for the site.
**Primary Dependencies**: Existing kit verifier, registry and conformance contracts, release contract, Next static export.
**Storage**: Source files in `skill/`, `brands/`, `scripts/`, and `site/`; generated `dist/`, `release/`, `site/generated/`, and `site/out/` stay ignored.
**Testing**: Focused negative tests, all eight kit and glyph checks, archive certification, site lint/build/browser tests, and staged candidate audit.
**Target Platform**: Portable brand kits, hosted static site, and GitHub Actions release candidate.
**Constraints**: Exact byte copying, root-contained references, no logo geometry changes, WCAG 2.1 AA, no generated artifacts committed.
**Scale/Scope**: Eight brands; one shared artifact-family matrix; kit, hosted, skill, and staged release surfaces.

## Constitution Check

- **P1**: Only source, tests, and Spec Kit evidence are committed. Synthetic tampered fixtures live in temporary directories.
- **P2**: Audit and validation do not modify approved logo paths or derivative geometry.
- **P3**: Site behavior and accessibility remain at the AA floor. Site validation remains mandatory.
- **P4**: Every production kit retains zero problems in `verify.py` and `validate_glyph.py`; the candidate audit runs after generation.
- **P5**: The site continues to consume generated kits. Semantic checks compare projected and copied output to kit authority.
- **P6**: Spec, plan, tasks, tests, changelog, and evidence move together. Formal release remains a separate action.

## Decisions

1. **Check at both producer and publication boundaries**: Strengthen the portable verifier's manifest semantics so a consumer cannot mistake an empty list for a valid kit. Independently audit the exact exported site and staged candidate because a correct producer does not prove the copied output remained intact.
2. **Reuse deep validators**: Registry, icon, provenance, conformance, consumer, and release contracts already have specialized checks. Compose these at candidate certification and add missing cross-surface assertions rather than introducing a second divergent schema engine.
3. **Truthful optional states**: Preserve `capability-gap`, conditional custom assets, and human-only conformance baselines as explicit optional or unsupported states. Missing required records fail.
4. **Keep candidate version**: S059's 2.6.0 source is unpublished. The S060 audit changes certification, not approved identity or public kit shape, so the candidate remains 2.6.0 and the change is recorded under Unreleased.
5. **Issue boundary**: Documentation fact values are validated as artifacts here. The full reader-facing guideline redesign belongs to #270 and is not marked complete by #269.

## Project Structure

```text
skill/templates/verify.py               # portable manifest semantics
skill/templates/test_pipeline.py        # malformed-manifest regressions
scripts/audit_publication_artifacts.py  # exact kit/site/candidate cross-checks
scripts/test_publication_workflow.py    # publication failure regressions
.github/workflows/build.yml             # exact staged candidate gate
specs/060-artifact-semantics/           # matrix, contract, tasks, evidence
```

## Delivery Sequence

Write failing negative tests, implement portable and publication checks, build all eight kits, certify archives and site, stage/check the exact candidate, record evidence, commit, push, publish the authorized PR, resolve up to two review rounds and CI, then hand off for owner merge.
