# Implementation Plan: v1.2.0 Publication and Production Certification

**Branch**: `codex/011-v1-2-publication-certification` | **Date**: 2026-09-05 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/011-v1-2-publication-certification/spec.md`

## Summary

Complete the post-merge portion intentionally deferred by S010: revalidate the exact owner-merged main revision, publish v1.2.0 through the tag-triggered GitHub Actions workflow, independently verify its seven public assets, qualify the production Pages deployment, and preserve sanitized evidence in one reviewed S011 pull request. Extend the existing site verifier with a fail-closed production-origin mode so the same route, metadata, resource, responsive, theme, and accessibility contract can run locally or against `https://brand.shruggie.tech`.

## Technical Context

**Language/Version**: Python 3.8 minimum, JavaScript on Node.js 20 minimum, Markdown, Git, and GitHub Actions

**Primary Dependencies**: Existing release contract and packaging scripts, Next.js static export, Playwright, axe-core, and GitHub CLI

**Storage**: Version-controlled source and specifications; ignored `release/`, `dist/`, `site/out/`, generated site content, and test screenshots; GitHub Releases and Pages

**Testing**: Full release candidate gate, public asset verifier, site lint/build/browser verification, production-origin browser verification, Markdown policy, encoding, sensitive-data, and generated-artifact hygiene

**Target Platform**: Windows development host, Ubuntu GitHub Actions, GitHub Releases, and GitHub Pages

**Project Type**: Source-driven brand generator, portable skill, release pipeline, and static documentation and portfolio site

**Performance Goals**: Reuse one browser verification process for the full production matrix and one shared release verifier for all seven assets

**Constraints**: UTF-8 without BOM, LF, no generated artifacts committed, no identity geometry changes, WCAG 2.1 AA, CI-built official assets only, exact allowed production origin, one owner merge gate, no more than two Codex review rounds

**Scale/Scope**: One annotated release tag, seven assets, five production brands, the complete generated route inventory, four closure-linked issues, and one milestone

## Constitution Check

| Principle | Design response | Gate |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit only the verifier source and Spec Kit evidence. Keep downloads, builds, notes, and screenshots ignored. | PASS |
| P2. Identity geometry is preserved | S011 changes no logo geometry, identity color, font, or shipped mark bytes. | PASS |
| P3. Accessibility has no exemption | Production mode retains the complete zero-violation WCAG 2.1 AA browser gate. | PASS |
| P4. Verification precedes publication | Revalidate merged main before tagging, then independently verify the published assets and production deployment. | PASS |
| P5. The site consumes generated kits | Production verification consumes the same generated route and asset contract as local verification. | PASS |
| P6. Specifications and releases move together | S011 records tag, release, production, issue, review, and closure evidence in one reviewed slice. | PASS |

Post-design re-check: PASS. Production-origin support changes only where content is served, not what is verified, and rejects an unsafe or unexpected remote origin.

## Technical Approach

1. Establish issue #129 and complete the S011 specification, plan, checklist, contracts, and task graph before publication.
2. Add regression coverage for production-origin selection, HTTPS enforcement, hostname restriction, and local-server fallback.
3. Refactor `site/scripts/verify-site.mjs` to select either the existing local static server or the explicitly approved production origin while preserving every existing check and always cleaning up only resources it created.
4. Revalidate the exact merged main revision using the S010 quickstart, hosted Build result, release packaging, and seven-asset candidate contract.
5. Prove v1.2.0 does not conflict, create one annotated tag at the verified main revision, push it, and wait for the tag-triggered Release workflow.
6. Inspect the release target and state, compare public notes, download all assets into a fresh ignored directory, and run the same seven-asset verifier.
7. Tie the successful Pages workflow to the merged main revision, run the site verifier against production, and inspect the generated theme and viewport screenshots.
8. Record sanitized immutable evidence, run repository gates, commit, push, and open the official S011 pull request with accurate closure keywords.
9. Process the automatic Codex round, optionally request exactly one second round, disposition every comment and finding, and stop with the green pull request open for owner merge.

## Project Structure

```text
site/scripts/verify-site.mjs
site/tests/production-origin.test.mjs
specs/011-v1-2-publication-certification/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── production-contract.md
│   ├── publication-contract.md
│   └── review-ledger.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

**Structure Decision**: Add no new deployment or release subsystem. Extend the existing browser verifier through a small testable origin-selection module and reuse the established release contract.

## Complexity Tracking

No constitutional violation or unjustified complexity is introduced.
