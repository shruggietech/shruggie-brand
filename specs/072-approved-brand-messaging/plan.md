# Implementation Plan: Owner-decided portfolio messaging

**Branch**: `codex/072-approved-brand-messaging` | **Date**: 2026-10-21 | **Spec**: [spec.md](spec.md)

## Summary

Apply issue #309's latest decisions to seven brand sources. Repair two legacy-description consumers and retain unreviewed optional suggestions as unresolved under the owner's 2026-10-27 no-questions direction. Compile and validate the approved subset and its faithful public projections.

## Technical Context

**Language/Version**: Python 3.8+ generator; Node.js 20+ site.

**Primary Dependencies**: Existing messaging contract, brand validation, identity continuity, WordPress block patterns, Next.js registry, Playwright, and PDF tooling. No new dependency.

**Storage**: Canonical brands/*/brand.json plus source-only Spec Kit evidence. Generated output stays ignored under dist/.

**Testing**: Focused unittest regressions before fixes, production source/schema checks, documented aggregate kit/site/runtime checks before completion.

**Target Platform**: Static web publication and portable generated kits, authored from Windows with hidden noninteractive subprocesses.

**Project Type**: Brand compiler and static portfolio.

**Performance Goals**: No new runtime work. Avoid rebuilding complete kits for every editorial question; full validation uses the final selected source set.

**Constraints**: Exact owner-approved copy, independent absent/unresolved states, allowed uses, WCAG AA, unchanged logo geometry, UTF-8 without BOM and LF.

**Scale/Scope**: Thirteen production brands; three recorded-decision brands initially change. Remaining selections may expand the changed-source inventory.

## Constitution Check

P1: Source-only changes and isolated temporary test data. P2: No logo/path/palette edits, retain identity snapshot and source assets. P3: Existing AA floor and full site audit remain mandatory. P4: Every production kit must pass verifier/glyph gates before completion. P5: Site consumes generated approved text, never duplicated brand copy. P6: S072 records spec, plan, tasks, analysis, choices, and evidence. Pre-research and post-design gates pass with no exception.

## Phase 0: Research

Issue #309 comments are authoritative, including the 2026-10-01 DanceWithMe865 slogan update. Audit current source rather than the issue's older eleven-brand inventory. Inspect product READMEs and established brand guidance for suggestions; no candidate becomes approved automatically. Technical contracts are already established, so no new architecture research or delegated agents are required.

## Phase 1: Design

Preserve messaging.py's strict six-field approved record and status-only absent/unresolved records. Use approved_messages(brand, 'site-metadata') for WordPress description and Next.js OG alternative text. Omit the hero description block when absent; use a title-only alt value when absent. Preserve separate social_copy values. Correct S067's false approval claim with an explicitly dated supersession note. Record selected wording and role uses in decisions.md and inventory.md.

## Implementation and Validation Order

1. Add negative generator tests for absent/unresolved legacy text and positive tests for allowed canonical description text, including escaping.
2. Apply recorded source decisions, remove the revoked active descriptor, and refresh source-file hashes without changing identity evidence.
3. Fix the two consumers and verify focused tests/source schema. Apply the four 2026-10-27 owner-approved short descriptions; defer all other unreviewed roles.
4. Preserve current version identities in this source-only PR and record patch impact for the next release slice. The repository's release contract requires compiler, site, impact metadata, and dated changelogs to move together with a release candidate. Refresh source-bound continuity after final source bytes.
5. Run the complete contributor and CI-parity checks, inspect changed message surfaces and accessible output, audit UTF-8/LF/mojibake and source-only diff, update evidence, then commit, push, and merge after required checks and review. Do not tag or publish a release.

## Project Structure

- brands/{covarity,cueson,dancewithme865,fragcap,glitchpad,go-schedule,shruggietech}/brand.json.
- brands/*/identity-continuity.json for required source digest refresh only.
- skill/templates/gen_nextjs.py, gen_wordpress.py, test_messaging.py.
- specs/067-approved-messaging-guide-parity/migration-inventory.md for explicit historical correction.
- specs/068-brand-essentials-docs-navigation/disposition-inventory.md for the source-bound approved-message inventory.
- specs/072-approved-brand-messaging/{spec,plan,research,data-model,quickstart,tasks,decisions,inventory,verification}.md and contracts/public-messaging.md.
- CHANGELOG.md for unreleased source changes; skill/SKILL.md remains at the current release version until the coordinated release slice.

**Structure Decision**: Reuse the existing canonical messaging contract; no new runtime state or approval machinery.

## Decisions

- 2026-10-21: The owner's requested interactive copy review overrides unattended editorial choice. No extra copy approval is needed for already recorded decisions.
- 2026-10-21: Partial copy completion is valid; unresolved fields remain tracked rather than blocking the correction.
- 2026-10-21: Reusable slogans receive visual-guide, strategy-reference, consumer-data uses; new descriptions also receive site-metadata. Existing approvals retain their prior uses. Social-image text remains separately governed.
- 2026-10-21: Brand/compile patch versioning was initially planned after the final selected set to avoid multiple source-digest and full-build cycles.
- 2026-10-27: The four newly approved short descriptions are exact owner decisions, including Glitchpad's `fast`; suggestions for all other roles remain unresolved under the owner's no-questions cleanup direction. Push and merge are authorized after verification, but release publication remains outside this slice.
- 2026-10-27: Defer numeric version changes to the release slice. `release_contract.load_metadata` requires a dated root and skill changelog entry, release-impact metadata, and matching site/skill versions; changing only S072's source files and numeric versions fails that contract. The source fixes remain in Unreleased until a coordinated release candidate is prepared.
