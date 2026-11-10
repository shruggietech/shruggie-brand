# Implementation Plan: Brand Messaging and Delivery Polish

**Branch**: `codex/075-brand-delivery-polish` | **Date**: 2026-11-09 | **Spec**: [spec.md](spec.md)

## Summary

Resolve #328 and #353 through shared message projection and one coordinated patch candidate. #352 is blocked by authenticated DNS/rule management permissions, independent of repository work.

## Technical Context

- **Language/Version**: Python 3.8+ compiler, Node.js 20+ static Next.js site, pinned pnpm 10.28.2.
- **Dependencies**: Existing messaging/essentials, Chromium, PyMuPDF, coloraide and publication pipeline.
- **Storage**: Canonical source and Spec Kit evidence in Git; generated proofs/builds in ignored dist or isolated temporary directories.
- **Testing**: Focused projection/layout regressions, full contributor and CI-parity checks, thirteen kit builds, site/accessibility/publication contracts.
- **Target**: A4 PDF/print HTML, portable/hosted guidelines, desktop/mobile portfolio, Cloudflare edge alias.
- **Performance**: Preserve static delivery without additional client network requests.
- **Constraints**: Exact copy, unchanged logo geometry, WCAG AA, hidden noninteractive Windows subprocesses, UTF-8 without BOM/LF, source-only commits.
- **Scale**: Thirteen production kits, three issues, one patch candidate.

## Constitution Check

P1: Generated output stays ignored and fixtures temporary. P2: No identity redesign. P3: Measure text contrast and layout. P4: Rebuild all production kits and run full documented checks. P5: Site consumes generated approved messages. P6: Installed Spec Kit and version/migration metadata stay synchronized. No exceptions; post-design review reaches the same result.

## Research and Decisions

- Prefer label-free cover per owner direction; supersede S067 only for opening presentation, retaining reference labels and semantic roles.
- Slogan uses 23pt declared display face/weight. Supporting copy uses 13.5pt body, 1.5 leading and foreground on declared page ground with measured AA contrast.
- Explicit data-message-value content is compared exactly within data-message-role wrappers. Optional reference labels stay separate; legacy labeled reference output remains accepted. Duplicate/nested roles and unauthorized text remain errors.
- Measure cover layout before PDF export. Overflow uses identified continuation sheets at unchanged readable sizes. Whole roles move first; unusually long individual roles split at word boundaries with explicit ordered fragments whose reconstructed text must match exactly. This stays confined to opening messages, not a general layout engine.
- DanceWithMe865 short-description uses include visual-guide, strategy-reference, site-metadata and consumer-data, following the requested existing surfaces. Social-image copy/composition remains unchanged.
- Cloudflare research agent confirmed zone discovery succeeds, but DNS, redirect entrypoint and ruleset reads return 403. No mutation is attempted. Record required DNS Edit and Single Redirect Edit access and remaining work in cloudflare.md.
- Prepare v3.1.2 compiler/site and affected kit patch metadata under existing version policy, retaining Brand Canon/adapter versions. Honor the usual pre-push halt; live completion requires subsequent authorized tagged publication.
- Custom checklist markers remain reviewer-owned. The explicit autopilot kickoff authorizes proceeding after analysis without an additional inter-step permission request.

## Implementation Order

1. Complete specify, clarify, checklist, plan and tasks, then blocking analyze.
2. Preserve Local Media Gallery before proof; add exact-message and rendered layout tests before implementation.
3. Update canonical copy/continuity hashes, shared generator/verifier, tests and superseded prose/contracts.
4. Document exact Cloudflare blocker and reconciliation/rollback procedure.
5. Coordinate metadata, rebuild all kits, run documented validation, inspect renders and audit source/encoding hygiene.
6. Commit locally and present pre-push review. PR/release/Pages and issue closure remain pending authorization and live evidence.

## Project Structure

Source: brands/dancewithme865/brand.json and continuity record; skill/templates/gen_guide_pdf.py, verify.py and focused cover-layout helper/tests; S067 projection contract/prose; existing release metadata/history sources. Evidence: specs/075-brand-delivery-polish/. New behavior remains in shared templates.

## Complexity Tracking

No constitution exceptions. No unrelated dependency upgrades.

## Validation Follow-up Decision

The required WordPress fixture audit discovered current transitive findings. T016/T017 add a bounded validation-only repair with exact patched versions and a real glob/rimraf filesystem compatibility check; the existing audit threshold remains unchanged. This is necessary to complete the documented gate, rather than an expansion into the unrelated dependency PR backlog. Supplemental cross-artifact analysis confirms coverage under FR-009/FR-010 and no new constitution conflict.
