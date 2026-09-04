# Implementation Plan: v1.1.2 Release and Publication Certification

**Branch**: `codex/004-release-publication-certification` | **Date**: 2026-09-04 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/004-release-publication-certification/spec.md`

## Summary

Turn the existing tag-triggered publication workflow into a single testable release contract. The implementation will derive v1.1.2 notes from the version-controlled changelog, validate skill and canon metadata, package the exact two skill distributions and five production kits, inspect type-specific archive contents and manifest checksums, and reuse that preflight in pull-request CI and tagged publication. S004 then publishes an official pull request, processes the automatic Codex review and exactly one manual second round, and stops at the owner merge gate. After owner merge, the same slice continues from actual main to tag, download, verify, document, and close the release work.

## Technical Context

**Language/Version**: Python 3.8 minimum; YAML for GitHub Actions; Markdown and JSON release metadata

**Primary Dependencies**: Python standard library for release validation; existing full-build dependencies for kit and PDF generation; GitHub CLI and GitHub Actions for publication

**Storage**: Version-controlled files plus ignored `dist/` and `release/` build output; GitHub release assets and issue metadata

**Testing**: Python `unittest`, repository build and glyph suites, archive preflight, Markdown policy, Next.js lint/static export, hosted GitHub Actions, and post-publication download verification

**Target Platform**: Windows development host plus Ubuntu GitHub Actions; release-contract tests remain Python 3.8 compatible

**Project Type**: Source-driven brand asset generator, portable skill, static documentation site, and GitHub release pipeline

**Performance Goals**: Release preflight inspects exactly seven archives in one run and adds negligible time beside the full kit build

**Constraints**: UTF-8 without BOM, LF line endings, no private operational data, CI-built assets only, non-exemptable identity/accessibility gates, two Codex rounds maximum, owner-only merge gate, tag only after merged-main revalidation

**Scale/Scope**: One 1.1.2 release, two skill bundles, five production-kit archives, three child issues, two phase parents, and two milestones

## Constitution Check

| Principle | Design response | Gate |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit only release logic, tests, workflows, changelog, and Spec Kit records. Keep `dist/`, notes output, downloads, and archives ignored. | PASS |
| P2. Identity geometry is preserved | No brand geometry or identity token is edited. Archive verification reads generated content only. | PASS |
| P3. Accessibility has no exemption | The complete build remains a prerequisite and S004 makes no accessibility exception. | PASS |
| P4. Verification precedes publication | The same repository-owned preflight runs in PR CI, tag CI, and post-publication inspection. | PASS |
| P5. The site consumes generated kits | No site-owned brand values are introduced; the existing generated-kit build remains part of the full gate. | PASS |
| P6. Specifications and releases move together | S004 contains specification, plan, tasks, contracts, and evidence, and publication is gated by those records. | PASS |

Post-design re-check: PASS. The release contract strengthens P1, P4, and P6 and introduces no constitutional exception.

## Technical Approach

1. Capture the current issue, tag, release, workflow, version, and history baseline in the S004 evidence ledger.
2. Add a Python 3.8-compatible release-contract module that parses authoritative metadata, derives notes from the requested changelog section, computes the exact expected asset set, and validates type-specific archive contents.
3. Add focused regression tests for history/version drift, release-note generation, skill bundle shape, portable bundle shape, production archive requirements, checksum failures, and unexpected assets.
4. Correct generated kit manifest versions to reflect each kit's declared `brand.json` version so the package filename, embedded brand metadata, and manifest agree.
5. Make packaging start from an empty known release-output directory and call shared expected-asset logic so stale local output cannot contaminate certification.
6. Fold the completed S003 remediation entries into the unreleased 1.1.2 history, align both changelogs to the release date, and keep a clean empty Unreleased heading for future work.
7. Update pull-request and tag workflows so Python 3.8 runs focused release-contract tests, the full build creates and verifies all archives, and the release publisher consumes the generated notes file.
8. Execute focused tests, full six-kit build, site export, exact seven-archive preflight, encoding and sensitive-data scans, and a clean-checkout run.
9. Create and link an S004 GitHub slice issue, then push and open the official pull request with a two-entry review ledger.
10. Process automatic round 1 completely, post one `@Codex` request for round 2, process round 2 completely, and wait for green required checks.
11. Stop with the pull request open. After the owner merges, reconcile actual main, tag v1.1.2, verify the workflow and downloaded release, update and close eligible child and parent issues, close zero-open-issue milestones, and record the final evidence.

## Architecture Decisions

- `scripts/release_contract.py` is the sole release metadata and archive contract. GitHub Actions invokes it instead of duplicating assertions in shell snippets.
- The root `CHANGELOG.md` is the release-note source. `skill/CHANGELOG.md` remains the bundled skill-facing history and is validated for the same release sequence and required historical subjects.
- Production archives retain each brand's own version in the filename. The skill and canon version identify the brandbuilder release. The verifier makes that distinction explicit.
- Generated release notes are ignored build output. The tagged workflow regenerates them from the tagged changelog and supplies them to `gh release create --notes-file`.
- Archive validation is type-specific. Licenses are universal; skill distributions have mutually exclusive entry-point rules; production kits require brand metadata, a guide PDF, and valid recorded manifest checksums.
- Review requests form a finite state machine: automatic round 1, one explicit round 2, complete. Correction pushes and late feedback never create another request.
- GitHub issue state follows evidence. Branch readiness cannot close publication-dependent work.

## Project Structure

### Documentation (this feature)

```text
specs/004-release-publication-certification/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── release-contract.md
│   └── review-ledger.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Repository surfaces changed or verified

```text
.github/workflows/build.yml
.github/workflows/release.yml
CHANGELOG.md
scripts/package_release.py
scripts/release_contract.py
scripts/test_release_contract.py
skill/CHANGELOG.md
skill/templates/build_kit.py
specs/004-release-publication-certification/
```

**Structure Decision**: Keep release policy in one standard-library Python module and reuse existing source/build surfaces. No service, database, generated artifact, or duplicate release metadata source is added.

## Verification Strategy

- Run release-contract unit tests under the active Python and the hosted Python 3.8 job.
- Run compile, kit discovery, glyph, pipeline, and Markdown tests.
- Build all five production kits and the fixture at full capability and require zero reported problems.
- Generate release notes, package the release, and require exactly seven expected assets with all archive contracts passing.
- Build the static site from the fresh distribution output.
- Repeat the release-contract and repository-only gates from an isolated clean checkout.
- Scan changed public text for BOM, CRLF, mojibake, private paths, secrets, and provider resource identifiers.
- Require hosted pull-request checks after the final correction push.
- After merge, download published assets into a new temporary directory and apply the same verifier to the release body and archives.

## Complexity Tracking

No constitutional violations or added architectural layers require justification.
