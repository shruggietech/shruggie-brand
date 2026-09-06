# Implementation Plan: v1.2.1 Release and Production Certification

**Branch**: `codex/013-v1-2-1-release` | **Date**: 2026-09-06 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/013-v1-2-1-release/spec.md`

## Summary

Promote the completed S012 brand-site and identity polish plus the merged Brotli security update into a coherent v1.2.1 patch candidate, certify all production kits and release archives, process the automatic pull-request review, merge the verified source, publish CI-built official assets, and qualify the deployed production site.

## Technical Context

**Language/Version**: Python 3.8 minimum, TypeScript on Node.js 20 minimum, YAML, JSON, and Markdown

**Primary Dependencies**: Python standard-library release tooling; existing Pillow, fontTools, CairoSVG, Playwright, Next.js, Fumadocs, and GitHub Actions stack

**Storage**: Version-controlled source plus ignored `dist/`, `release/`, `site/out/`, generated site content, public-download evidence, and screenshots

**Testing**: Python `unittest`, five-kit build, glyph and verifier gates, archive contract, generated-agent synchronization, TypeScript check, static export, browser tests, WCAG audit, Markdown policy, and repository hygiene

**Target Platform**: Windows development host and Ubuntu GitHub Actions; GitHub Releases and GitHub Pages

**Project Type**: Source-driven brand generator, portable agent skill, release pipeline, and static documentation and portfolio site

**Performance Goals**: Certify exactly seven release assets and all discovered production routes without adding a second publication path

**Constraints**: UTF-8 without BOM, LF, no generated output committed, unchanged logo geometry, WCAG 2.1 AA, CI-built official assets only, automatic Codex review only, tag only after reviewed-main revalidation

**Scale/Scope**: One patch release, five production brands, two skill distributions, seven release assets, one tracking issue, one milestone, and the complete production route inventory

## Constitution Check

| Principle | Design response | Gate |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit metadata, release logic, tests, changelogs, and Spec Kit records only; rebuild all output. | PASS |
| P2. Identity geometry is preserved | Advance release metadata and preserve every logo path and source mark byte. | PASS |
| P3. Accessibility has no exemption | Retain the full WCAG 2.1 AA browser gate with zero waivers. | PASS |
| P4. Verification precedes publication | Run the shared release contract before merge, in tag CI, and on fresh public downloads. | PASS |
| P5. The site consumes generated kits | Rebuild the site from verified kits and validate its generated route and resource inventory. | PASS |
| P6. Specifications and releases move together | S013 records candidate, review, publication, and production evidence before closing its GitHub hierarchy. | PASS |

Post-design re-check: PASS. The design preserves all non-exemptable gates and introduces no constitutional exception.

## Technical Approach

1. Establish Phase 14 milestone 24 and tracking issue #140, then record the synchronized v1.2.0 baseline and absent v1.2.1 state.
2. Add regression coverage for v1.2.1 metadata, history, conditional migration notes, exact assets, and independent production-brand versions.
3. Advance skill, canon, site, and production-brand canon references to v1.2.1 without changing production-brand versions.
4. Promote applicable Unreleased records into dated v1.2.1 sections and make migration notes version-specific.
5. Run the full source, build, packaging, site, accessibility, and repository-hygiene gates.
6. Publish the S013 pull request, process only its automatic Codex review, file any negative finding, correct warranted feedback, answer every comment, and resolve every addressed thread.
7. Merge only after review and required checks pass, synchronize actual main, and repeat the release candidate contract.
8. Create the annotated v1.2.1 tag, wait for CI publication, download all public assets into fresh ignored repository-local storage, and verify them.
9. Verify the Pages deployment and production-origin contract, record public evidence on #140, then close only #140 and milestone 24.

## Architecture Decisions

- Keep the established synchronized skill and canon release version because current release validation and production-source contracts treat them as one compatibility baseline.
- Keep production-brand versions unchanged; only their canon references advance.
- Use v1.2.1 because all shipped changes are backward-compatible corrections or dependency maintenance.
- Store version-specific migration text in release tooling so v1.2.0 and v1.2.1 notes cannot silently inherit the wrong consumer guidance.
- Keep GitHub Actions as the sole official asset builder and publisher.
- Do not manually request another Codex review round. Automatic feedback remains mandatory to inspect and resolve.
- Keep the S013 issue open through merge because release and production evidence can exist only afterward.

## Project Structure

### Documentation for S013

```text
specs/013-v1-2-1-release/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── production-contract.md
│   ├── release-contract.md
│   └── review-ledger.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Repository surfaces changed or verified

```text
CHANGELOG.md
brands/*/brand.json
scripts/release_contract.py
scripts/test_package_release.py
scripts/test_release_contract.py
site/package.json
skill/CHANGELOG.md
skill/SKILL.md
skill/references/01-canon.json
specs/013-v1-2-1-release/
```

**Structure Decision**: Reuse the existing release modules and verification surfaces. Do not add another version file, deployment mechanism, or committed artifact directory.

## Complexity Tracking

No constitutional violation or unjustified complexity is introduced.
