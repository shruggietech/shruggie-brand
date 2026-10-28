# Implementation Plan: BrandBuilder 3.1.1 Live Site Release

**Branch**: `codex/074-live-site-release` | **Date**: 2026-10-28 | **Spec**: [spec.md](spec.md)

## Summary

Package the S072 approved messaging and generator correction, S073 site layout, and merged dependency patches as one versioned release. Use the existing tag-triggered release pipeline to publish CI-built assets and deploy GitHub Pages. Verify the public result directly.

## Technical Context

- **Language/Version**: Python 3.8+ generator; Node.js 20+ static Next.js site.
- **Primary Dependencies**: Existing release contract, Spec Kit, CI build workflow, GitHub Release and Pages.
- **Storage**: Canonical source, version metadata and Spec Kit evidence in Git; generated output under ignored `dist/`.
- **Testing**: Focused contract tests, full documented build and site checks, CI on PR and tag, live HTTP/browser inspection.
- **Target Platform**: GitHub Pages at `brand.shruggie.tech`; release archives on GitHub.
- **Project Type**: Static site and brand kit compiler.
- **Constraints**: Exact source SHA, immutable package IDs/checksums, WCAG 2.1 AA, source-only commits, UTF-8 without BOM and LF.

## Constitution Check

P1: Generated outputs remain ignored. P2: No approved geometry changes. P3: Rendered accessibility gate required. P4: Rebuild and verify thirteen kits. P5: Site copies verified kit output. P6: S074 includes specification, plan, tasks, analysis and verification; tag builds assets in CI. No exception required.

## Research and Decisions

- `main` at `31b34611` has a successful Build run, while the latest official release is v3.1.0. The deployment job runs only for `refs/tags/v*`; a workflow dispatch or main push cannot update Pages.
- S072 explicitly deferred version assignment to the next release. Seven brand sources changed, so each receives a patch version. BrandBuilder and site move together to 3.1.1. Brand Canon and adapters retain their existing contracts.
- The owner requested unattended live deployment. This authorization covers the review and release stages, including merging the preparation PR after all gates pass.
- The three client brands remain hosted candidates; the existing ten owned archives, skill, portable bundle and checksum record remain the release inventory.

## Implementation Order

1. Establish S074 metadata and update patch versions, dated histories, impact and migration guidance.
2. Update current-version tests and source hash records, then run focused and full validation.
3. Commit source and evidence, open the release PR, resolve reviews and require green exact-head CI.
4. Merge the reviewed PR, verify main, create an annotated v3.1.1 tag and push it.
5. Require tag preflight, release publication and Pages success, then inspect uploaded assets and the live site.

## Project Structure

Versioned sources: `brands/*/brand.json`, `skill/SKILL.md`, `skill/references/release-impact.json`, `site/package.json`, `CHANGELOG.md`, `skill/CHANGELOG.md`, `scripts/release_contract.py`. Current-version assertions live in `scripts/test_release_contract.py` and `skill/templates/test_interface_contract.py`. S074 evidence lives under `specs/074-live-site-release/`.
