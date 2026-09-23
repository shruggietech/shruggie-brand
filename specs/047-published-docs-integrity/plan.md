# Implementation Plan: Published Documentation and Guideline Integrity

**Branch**: `codex/047-published-docs-integrity` | **Date**: 2026-09-22 | **Spec**: [spec.md](spec.md)

## Summary

Correct public prose at its source, add a publication-bound source/output audit, make portable integration previews readable and appearance-aware, and correct bottom documentation navigation position and focus. Rebuild every production kit and the static site. Since generated kit bytes change, prepare BrandBuilder 2.0.2 as an unreleased patch candidate with a distinct immutable package identity; do not tag or publish a release in this slice.

## Technical Context

**Language/Version**: Python 3.8 minimum for generator and audits; Python 3.12 CI; TypeScript, Next.js 16.3.5, Node.js 20 minimum for the site

**Primary Dependencies**: Existing BrandBuilder templates, Fumadocs Core/UI 16.15.11, Next.js links, Playwright 1.63.0, local image/contrast tooling already used by the project

**Storage**: Governed Markdown, JSON, Python templates, and site source; generated `dist/` and `site/generated/` are disposable build output

**Testing**: Focused generator and publication tests, source/output prose audit, rendered Playwright checks, full production-kit build with zero verifier and glyph failures, release-candidate certification, site lint/build/test, publication audit

**Target Platform**: Published static documentation and portable guides across desktop and narrow viewports

**Project Type**: Brand-kit compiler plus static documentation site

**Performance Goals**: Audit remains deterministic and bounded to publication inventory; no new runtime network request or page bundle dependency for previews

**Constraints**: WCAG 2.1 AA with no waiver; exact logo and asset bytes; no generated commits; native links and history; explicit fragments retained; no release tag without separate authorization

**Scale/Scope**: Fifteen public manual pages, every production kit's reader-facing guidance, affected portable integration cards, one shared documentation pagination surface, issues #236/#237/#202

## Constitution Check

| Principle | Planned evidence | Result |
| --- | --- | --- |
| P1. Sources committed, artifacts rebuilt | Edit references, brand guidance, generator, site source, and tests; regenerate ignored outputs. | PASS |
| P2. Identity geometry preserved | Preview surfaces and fallback language may change; shipped artwork and path bytes do not. | PASS |
| P3. AA floor | Measure actual local text and meaningful icon contrast; fix failing values. | PASS |
| P4. Verification before publication | Full kit, glyph, site, browser, release-candidate, and audit gates remain required. | PASS |
| P5. Site consumes generated kits | Fix guide generator and source guidance, not copied site output. | PASS |
| P6. Specs and releases together | S047 records decisions, version impact, verification, and PR evidence; 2.0.2 remains an untagged candidate. | PASS |

**Post-design recheck**: The audit and preview contracts operate on existing publication paths. No exception to source, identity, accessibility, or verification rules is needed.

**Security and brand isolation**: The audit rejects traversal or symlink escape from publication roots, and fixtures ensure one brand's reader guidance cannot be silently substituted into another brand's kit. The repository has no authenticated tenant system; brand-scoped publication is the relevant isolation boundary.

## Project Structure

```text
specs/047-published-docs-integrity/{spec.md,plan.md,research.md,data-model.md,quickstart.md,tasks.md,evidence.md,checklists/,contracts/}
skill/references/*.md                  # authoritative public manual
brands/*/{README.md,NOTES.md,...}     # delivered reader guidance, only as needed
skill/templates/gen_guidelines.py      # portable integration previews
skill/templates/test_pipeline.py       # generator regressions
scripts/prepare_site.py               # manual transformation and site projection
scripts/audit_public_documentation.py  # bounded source/output prose audit
scripts/test_public_documentation.py   # audit negative and positive fixtures
scripts/export_approved_identity_proofs.py  # post-merge exact-hash proof retry
scripts/test_export_approved_identity_proofs.py  # retry and confinement regressions
site/app/docs/[[...slug]]/page.tsx     # documentation page focus target
site/app/layout.tsx                   # route scroll behavior opt-in
site/components/                     # docs pagination focus helper
site/scripts/verify-site.mjs          # rendered interaction and preview checks
.github/workflows/build.yml           # publication-bound audit gate
```

**Structure Decision**: Keep the site as owner of docs navigation, the generator as owner of portable guide HTML, and the documented source inventory as owner of prose audit. Do not patch copied output.

## Delivery Sequence

1. Record failing focused assertions for source/output prose leaks, dark-well text and nonvisual fallbacks, representative preview contrast, and scrolled pagination transitions.
2. Rewrite governed reader guidance and correct source-to-site transformation corruption while retaining active compatibility terms and safety rules.
3. Implement appearance-aware preview classification and explicit local-surface colors without changing asset bytes; verify the I Heart PR Tours portable file and representative fixtures.
4. Correct route scrolling and destination focus while retaining native links, fragments, history, direct loads, and reduced-motion behavior.
5. Add the bounded content audit to the full build, prepare 2.0.2 release-candidate metadata and patch versions for brands with changed delivered guidance, run the full local gate, inspect generated outputs, and record evidence.
6. Commit, push, open one issue-linked PR, address review findings, and wait for green CI and review satisfaction. The owner retains final merge authority.

## Decision Log

### 2026-09-22 - Audit publication-bound guidance, not internal history

The public manual inventory and production-kit discovery identify authoritative inputs and generated output. Blanket scanning of every repository document would incorrectly reject specifications, approval ledgers, and changelogs that legitimately retain history. S047 therefore checks reader-facing source and prepared output, with exact and documented exceptions for active compatibility language.

### 2026-09-22 - Preserve artwork and classify previews by visible appearance

An unchecked `appearance=default` to dark-well rule and inherited foreground color caused the reported failure. Explicit well colors and contrast-aware visual selection correct presentation while keeping approved file bytes. Nonvisual resources receive a distinct label, not a misleading empty icon preview. Broad light-theme architecture in #193 remains separate.

### 2026-09-22 - Use native navigation with a scoped focus correction

Fumadocs delegates its footer links to Next navigation. Add Next's smooth-scroll route opt-in and focus only after an activated fragment-free pagination transition. Global click interception or unconditional route scrolling would risk fragment destinations and browser history.

### 2026-09-22 - Advance compiler package identity before changing generated bytes

Corrected portable HTML and instructional output make new kit bytes. Reusing the published `bb2.0.1` identity would violate immutable publication. A 2.0.2 compiler patch candidate is the smallest compatible version change; this PR does not create or publish that release. A brand whose delivered source guidance changes receives its own patch version under the brand version policy, after reconciliation with active brand work.

### 2026-09-23 - Bound transient canonical-host proof regeneration

The merged S047 build failed once on the exact Gate 2 approval manifest while the same source tree, Windows image, and dependency versions passed on the PR and a clean retry. Keep the approved hash as the sole acceptance value. Retry only this mismatch once after clearing the generated proof destination, report expected and actual hashes, and upload failed generated evidence for later diagnosis. Do not retry renderer, source-continuity, or other generator failures. This is a reliability correction, not an identity-policy exception or a new release.

## Complexity Tracking

No constitutional exception or unnecessary subsystem is planned. A small audit script is justified because a one-time prose rewrite alone cannot stop the same leakage from returning through generated publication paths.
