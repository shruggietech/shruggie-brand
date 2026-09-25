# Implementation Plan: Evergreen, Release-Bound Documentation

**Branch**: `codex/054-evergreen-release-bound-docs` | **Date**: 2026-09-25 | **Spec**: [spec.md](spec.md)

## Summary

Deliver #264, #265, and #276 through the existing documentation and release pipeline. Correct main-manual sources and README, derive documentation identity from the existing publication record, and bind exact source and prepared bytes to tagged assets.

## Technical Context

- **Language/Version**: Python 3.8+ and TypeScript/Next.js static export
- **Dependencies**: Documentation catalog, site preparation, release contract, skill archives
- **Storage**: Committed Markdown/JSON source; ignored generated MDX, JSON, HTML, kits, archives
- **Testing**: Isolated mutation tests, full kit/glyph/site/release-candidate gates
- **Target**: GitHub README, public manual, portable skill, tagged release
- **Constraints**: WCAG AA, LF/UTF-8, exact revision, candidate status in previews
- **Scope**: 15 source pages plus overview, route/search copy, README, issues #264, #265, and #276

## Constitution Check

- P1 PASS: Commit sources, tests, and Spec Kit records only.
- P2 PASS: No logo geometry changes.
- P3 PASS: Preserve accessible links/images and AA gates.
- P4 PASS: Full kit, glyph, site, and release checks remain required.
- P5 PASS: Site manual derives from packaged skill references.
- P6 PASS: One existing version authority controls documentation identity.

## Project Structure

```text
specs/054-evergreen-release-bound-docs/{spec,plan,research,data-model,quickstart,tasks,analysis,evidence}.md
specs/054-evergreen-release-bound-docs/{contracts,checklists}/
README.md
skill/references/*.md
scripts/{prepare_site,documentation_render,documentation_publication,audit_public_documentation,check_readme_links,release_contract}.py
scripts/test_{documentation_publication,public_documentation,check_readme_links}.py
site/tests/site.test.mjs
.github/workflows/build.yml
```

**Structure Decision**: Generate a documentation record from existing publication facts, catalog, source SHA-256 hashes, and prepared MDX SHA-256 hashes. Copy it to static export and release candidate. Verify it against exact packaged skill references. No page owns an editable version.

## Design Sequence

1. Write fail-first mutation tests for source guidance, README, documentation record, and release preflight.
2. Audit all catalog pages, overview, route descriptions, and search text. Correct stale guidance and compare operative claims with code and canon.
3. Rewrite README as a stable front door and retire the per-brand link requirement while retaining link, path, destination, and accessibility checks.
4. Generate the documentation record and visible candidate/release identity on every manual route.
5. Extend candidate and tagged preflight to compare record, source references, prepared pages, release assets, and static export.
6. Run full local validation, commit, push, open PR, resolve CI and at most two review rounds, then hand off for merge. Live production evidence follows the formal release.

## Decision Log

2026-09-25: S053's v2.2.0 remains unpublished. S054 retains its source version as a candidate; a later authorized tag publishes these exact docs. This avoids inventing a manual version or claiming an unreleased tag is live.

2026-09-25: Bundle the three issues for shared publication validation while keeping README and manual content scopes separate, as #276 requires.

2026-09-25: Reuse existing bundle status and release metadata; derive all content hashes. A matching version label alone cannot prove content parity.

2026-09-25: Because v2.2.0 is still an unpublished candidate, add S054 documentation corrections to that version's root and skill changelog sections. Creating a second version before the first formal release would orphan the approved S053 candidate; the tagged release must include the combined history.

## Post-Design Constitution Check

P1-P6 remain PASS. Generated records and exports stay out of Git; formal publication requires matching version, revision, content inventory, and release status.
