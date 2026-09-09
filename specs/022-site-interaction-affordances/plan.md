# Implementation Plan: Site Interaction Affordances

**Branch**: `codex/022-site-interaction-affordances` | **Date**: 2026-09-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/022-site-interaction-affordances/spec.md`

## Summary

Resolve #163 and #164 as one shared interaction-contract slice. Replace the footer's repeated link markup with a single local destination record set that explicitly marks exactly Download the skill, Source, and License for safe separate-context navigation. Keep Company same-tab despite its hostname because the issue's named behavior set is authoritative. Add narrow shared CSS overrides for the dependency-rendered documentation pagination cue row and theme buttons, then extend static and Playwright verification to enforce footer metadata, keyboard and focus behavior, rendered chevron centering, non-collapsing icon geometry, enabled and disabled cursor treatment, both themes, and responsive widths.

## Technical Context

**Language/Version**: Node.js 20 minimum; TypeScript, React 19, CSS, JavaScript, JSON, and Markdown

**Primary Dependencies**: Next.js 16 App Router with static export, Fumadocs UI 16.14.3, next-themes, Playwright 1.62.1, and axe-core

**Storage**: Site source under `site/`, generated site inputs and static output under ignored paths, and Spec Kit artifacts under `specs/022-site-interaction-affordances/`

**Testing**: Source-level Node assertions, TypeScript type-check, Next.js static export, Playwright rendered-layout and interaction checks, axe-core WCAG 2.1 AA audit, and hosted GitHub Actions

**Target Platform**: Statically exported public site across desktop and mobile widths, light and dark themes, pointer and keyboard input

**Project Type**: Statically exported documentation and brand-registry web application

**Performance Goals**: Preserve the existing 76-page static export and browser-verification envelope; add only bounded checks on representative shared-footer and documentation routes

**Constraints**: WCAG 2.1 AA without waiver; no dependency fork; no information-architecture or theme-behavior changes; 44 by 44 CSS pixel targets; explicit opener isolation; generated output stays ignored; UTF-8 without BOM and LF

**Scale/Scope**: Two GitHub issues, six footer destinations, one shared footer component, one pagination selector family, one theme-switch selector family, three representative documentation route shapes, two themes, and desktop/mobile widths

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

| Principle | Plan evidence | Result |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit only site source, tests, changelog, and Spec Kit artifacts. Keep static exports and generated kits ignored. | PASS |
| P2. Identity geometry is preserved | No brand source, logo, glyph, font, or generated identity asset changes are in scope. | PASS |
| P3. Accessibility has no exemption | Retain semantic links and buttons, visible focus, 44-pixel targets, keyboard behavior, both-theme checks, and the complete WCAG 2.1 AA sweep. | PASS |
| P4. Verification precedes publication | Add source and rendered regressions before implementation, then run the full CI-parity site and repository gates. | PASS |
| P5. The site consumes generated kits | Footer and documentation chrome remain site-owned; no generated brand value is restated or changed. | PASS |
| P6. Specifications and releases move together | S022 specification, design, tasks, implementation, evidence, PR traceability, and issue closure move together. No release is cut. | PASS |

### Post-Design Re-check

The design changes only site-owned chrome and verification. It preserves dependency component semantics, generated-kit consumption, identity assets, and the full accessibility floor. No constitution exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/022-site-interaction-affordances/
├── checklists/
│   ├── interaction-quality.md
│   └── requirements.md
├── contracts/
│   └── site-interaction-contract.md
├── data-model.md
├── evidence.md
├── plan.md
├── quickstart.md
├── research.md
├── spec.md
└── tasks.md
```

### Source Code (repository root)

```text
site/
├── app/globals.css               # shared pagination and theme-control affordances
├── components/footer.tsx         # explicit footer destination records
├── scripts/verify-site.mjs       # rendered interaction and geometry measurements
└── tests/site.test.mjs           # source and negative contract assertions

CHANGELOG.md                       # unreleased site correction and decision record
```

**Structure Decision**: Keep all behavior in the existing site-owned footer, stylesheet, and verification surfaces. Do not fork Fumadocs, add a client wrapper, or create route-specific exceptions. Footer policy is explicit data because hostname inference conflicts with the approved Company behavior; pagination and theme corrections are CSS because the dependency already emits correct semantic structure.

## Delivery Sequence

1. Capture the six-footer-link baseline, dependency-rendered pagination structure, theme-switch structure, and current failing rendered measurements.
2. Add source assertions and negative policy fixtures for exact footer target and relationship behavior, pagination selector coverage, and enabled/disabled theme cursor rules.
3. Add browser assertions for footer keyboard focus and metadata, pagination label/icon center delta and icon stability, and theme-control cursor, semantics, focus, activation, and state.
4. Implement the shared footer record map and safe attributes for exactly the approved three destinations.
5. Add narrow pagination and theme-control CSS overrides without replacing dependency components or changing layout.
6. Run focused static and browser checks, then the full site type-check, export, route matrix, WCAG audit, repository test suites, and all-kit verification.
7. Record evidence, commit, push, open a PR closing #163 and #164, reconcile CI and no more than two Codex review rounds, then return for owner merge review.

## Complexity Tracking

No constitution violation requires justification. Combining both issues is proportional because they share the same site-owned interaction, accessibility, responsive, test, and publication gates.
