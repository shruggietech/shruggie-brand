# Implementation Plan: v1.2.0 Release and Production Certification

**Branch**: `codex/010-v1-2-release-certification` | **Date**: 2026-09-05 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/010-v1-2-release-certification/spec.md`

## Summary

Promote the completed S006 through S009 work into a coherent v1.2.0 release candidate, generalize the current-version release preflight so workflows do not retain stale literals, rebuild and certify the five production kits plus two skill distributions, and publish one reviewed pull request. S010 stops at the owner merge gate. After merge, the slice resumes from actual main to tag, publish, independently download and verify the seven assets, qualify the production Pages deployment, and close the evidence-complete Phase 12 hierarchy.

## Technical Context

**Language/Version**: Python 3.8 minimum, TypeScript on Node.js 20 minimum, YAML, JSON, and Markdown

**Primary Dependencies**: Python standard library release tooling; existing Pillow, fontTools, CairoSVG, Playwright, Next.js, Fumadocs, and GitHub Actions build stack

**Storage**: Version-controlled source plus ignored `dist/`, `release/`, `site/out/`, and generated site content; GitHub release assets and Pages deployment

**Testing**: Python `unittest`, full production-kit build, glyph and verification gates, archive contract, generated-agent synchronization, TypeScript check, static export, browser tests, WCAG audit, Markdown policy, and sanitized repository hygiene

**Target Platform**: Windows development host and Ubuntu GitHub Actions; published output targets GitHub Releases and GitHub Pages

**Project Type**: Source-driven brand generator, portable agent skill, release pipeline, and static documentation and portfolio site

**Performance Goals**: Certify exactly seven release assets in one preflight; inspect the full public route inventory without adding a second build pipeline

**Constraints**: UTF-8 without BOM, LF, no generated outputs committed, no identity geometry change, WCAG 2.1 AA, CI-built release assets only, one owner merge gate, no more than two Codex rounds, no tag before merged-main revalidation

**Scale/Scope**: One minor release, five production brands, two skill distributions, seven release assets, the complete generated route inventory, four GitHub issues, and one milestone

## Constitution Check

| Principle | Design response | Gate |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit only source metadata, release logic, tests, workflow changes, changelogs, and Spec Kit records. Keep all generated output ignored. | PASS |
| P2. Identity geometry is preserved | Update version and canon references only. Do not edit logo geometry, paths, identity colors, or shipped mark bytes. | PASS |
| P3. Accessibility has no exemption | Retain complete browser and generated-kit accessibility gates with zero waivers. | PASS |
| P4. Verification precedes publication | Reuse one release contract before merge, in tag CI, and on freshly downloaded public assets. | PASS |
| P5. The site consumes generated kits | Production certification validates the generated site and resources without adding site-owned brand values. | PASS |
| P6. Specifications and releases move together | S010 carries the full Spec Kit record and separates candidate, publication, and production closure by evidence. | PASS |

Post-design re-check: PASS. The design strengthens P4 and P6, introduces no exception, and preserves every non-exemptable identity and accessibility gate.

## Technical Approach

1. Create milestone 22 and issues #116 through #119 before implementation, linking the release candidate to post-merge publication and production evidence without premature closure.
2. Record the clean main, current v1.1.2 tag and release, current metadata, current Unreleased history, and absence of v1.2.0 in the evidence ledger.
3. Add regression-first coverage for validated current-version discovery, v1.2.0 metadata agreement, release history, migration wording, exact assets, and production-brand version preservation.
4. Generalize release history date agreement to the requested version and expose a validated `current` command that reports the authoritative skill and canon version only when the release metadata agrees.
5. Make packaging default to the validated current release instead of a duplicated literal and make pull-request CI discover the same version before packaging, notes generation, and verification.
6. Move the current Unreleased records into dated 1.2.0 sections, advance skill, canon, site, and five source canon references to 1.2.0, and update migration wording for the capabilities actually introduced.
7. Run focused regressions, the full five-kit build, exact seven-asset preflight, generated-agent synchronization, site lint, static export, browser tests, Markdown checks, encoding checks, sensitive-data checks, and generated-artifact hygiene.
8. Commit, push, and publish the official pull request. Close #117 on merge while tracking #116, #118, and #119.
9. Process automatic Codex round one, then post no more than one explicit `@Codex review` request for round two. File every negative finding as a linked Phase 12 issue, correct warranted findings, respond to every comment, and resolve addressed threads.
10. Wait for every required pull-request check to succeed and stop with the pull request open for the owner merge ritual.
11. After owner merge, synchronize and revalidate actual main, create one annotated v1.2.0 tag, verify the release workflow and fresh public downloads, qualify the Pages deployment, then close #118, #119, #116, and milestone 22 in evidence order.

## Architecture Decisions

- Version authority remains `skill/SKILL.md` plus the canon file, which must agree. A release command may print the current version only after validating both and the requested changelog section.
- The root changelog remains the release-note source. The bundled changelog carries skill-facing history and must have the same release date.
- Production brand versions remain independent. Their `canon` fields advance to 1.2.0, but their own `version` fields do not change.
- The additive ownership, supplied-input, icon, site, documentation, and discovery work warrants a minor release. No incompatible source or archive contract is introduced.
- Release packaging with no `--version` argument uses validated current metadata. Explicit versions remain supported for verification and historical tooling.
- The pull-request workflow discovers the version from repository source rather than carrying an independent hardcoded current version.
- GitHub closure remains evidence-driven. PR merge can satisfy #117, while publication and deployed-site issues remain open until post-merge proof exists.
- Review requests form a finite state machine: automatic round one, at most one explicit round two, complete. Corrections do not reset or extend the state machine.

## Project Structure

### Documentation for S010

```text
specs/010-v1-2-release-certification/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── production-certification.md
│   ├── release-contract.md
│   └── review-ledger.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Repository surfaces changed or verified

```text
.github/workflows/build.yml
CHANGELOG.md
brands/*/brand.json
scripts/package_release.py
scripts/release_contract.py
scripts/test_package_release.py
scripts/test_release_contract.py
site/package.json
skill/CHANGELOG.md
skill/SKILL.md
skill/references/01-canon.json
specs/010-v1-2-release-certification/
```

**Structure Decision**: Keep version and archive policy in the existing release modules. Do not add a second version file, deployment tool, or committed build artifact.

## Complexity Tracking

No constitutional violation or unjustified complexity is introduced.
