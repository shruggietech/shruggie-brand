# Implementation Plan: Site text hierarchy and containment

**Branch**: codex/073-site-text-hierarchy | **Date**: 2026-10-27 | **Spec**: [spec.md](spec.md)

**Input**: Three open site issues, #310, #311, and #335, plus the owner clarification on DanceWithMe865 title sizing.

## Summary

Deliver one text-presentation slice for the public brand site. Group the portfolio description beneath its heading, fit complete portfolio titles and affiliation markers with measured clearance, and render the 68 bibliography entries as compact, separately labeled fields. Preserve approved text, reference anchors, link targets, and unrelated site layouts.

## Technical Context

**Language/Version**: TypeScript and React in Next.js 16; Python 3 for documentation preparation; Markdown reference source.

**Primary Dependencies**: Existing Fumadocs MDX documentation renderer, Playwright site verifier, and repository production-kit pipeline.

**Storage**: Committed site and Markdown sources only; generated docs and exports stay outside Git.

**Testing**: Site source assertions, rendered Playwright checks, documentation-reference validation, site lint/build, aggregate production-kit and accessibility gates.

**Target Platform**: Responsive public brand website in Chromium, with desktop and mobile widths and enlarged text.

**Project Type**: Static-exported web application backed by generated documentation pages.

**Performance Goals**: Title fitting is bounded and runs only on initial layout, font availability, and size changes; it must not run per frame or interfere with input.

**Constraints**: WCAG 2.1 AA, no new brand wording, no shortened names, no geometry edits, UTF-8 without BOM and LF, and no committed generated artifacts.

**Scale/Scope**: One home-page section, the portfolio cards, and 68 references on the standalone References page.

## Constitution Check

- P1 passes: only source and Spec Kit artifacts are committed; documentation and site exports are regenerated.
- P2 passes: logo path data and approved name text remain unchanged.
- P3 is a verification gate: rendered text contrast, heading order, focus, reflow, and enlarged text must pass AA without waiver.
- P4 is a verification gate: site checks and the full documented production-kit pipeline must pass before publication.
- Repository workflow passes: S073 has a numbered spec, plan, tasks, analysis, implementation evidence, and issue traceability. The dirty S072 checkout remains untouched.
- Re-check after design: the chosen Markdown list and scoped site styles do not require a constitution exception.

## Project Structure

### Documentation for this slice

- specs/073-site-text-hierarchy/spec.md, plan.md, research.md, data-model.md, quickstart.md, tasks.md, verification.md
- specs/073-site-text-hierarchy/contracts/site-text.md
- specs/073-site-text-hierarchy/checklists/requirements.md

### Source boundaries

- site/app/(site)/page.tsx: portfolio heading group
- site/components/brand-portfolio.tsx: title fitting and marker association
- site/app/docs/[[...slug]]/page.tsx: route-specific References class
- site/app/globals.css: home and References presentation
- skill/references/references.md: the four fields of each stable reference
- site/tests/site.test.mjs and site/scripts/verify-site.mjs: source and rendered assertions
- scripts/check_documentation_references.py: existing reference contract, changed only if the new format exposes a genuine gap

**Structure Decision**: Keep the existing Next.js and Markdown architecture. No new package, service, shared component library, or canonical brand field is needed.

## Phase 0: Research decisions

1. The current home page places the description as a sibling of the heading group; a shared flex rule moves it right on desktop. Nest it within the existing heading group and scope presentation to the portfolio section. Preserve the Conformance page's shared section-heading behavior.
2. The owner screenshot shows DanceWithMe865 crowded near its card edge; a rendered baseline measured 19px of inner-edge clearance at a 1168px viewport with no size reduction. The 1170px five-column transition produces the narrowest card, about 210px wide. Fit the rendered title against its content width with a 24px reserve and a readable lower font bound. Trigger a fit calculation after fonts load and when card width changes. Use wrapping only if the lower bound cannot fit. A static name-length guess or global title reduction would not meet the measured-clearance requirement.
3. Each reference currently has a heading and one paragraph containing all four bold field labels. Convert each entry to four ordinary Markdown list items. This preserves links and IDs in the shipped source, gives semantic separation without MDX-only syntax, and passes the existing reference validator. Add a References-only page class and compact CSS for the heading/list pair. Avoid broad documentation styling.
4. Reuse existing Playwright site verification for measured geometry, heading/reading order, anchors, and responsive reflow. Synthetic long-title input belongs only in temporary test state, never production brand discovery.

## Phase 1: Design and contracts

- [data-model.md](data-model.md) defines the presentation records and invariants.
- [contracts/site-text.md](contracts/site-text.md) maps each issue to observable DOM, geometry, and accessibility behavior.
- [quickstart.md](quickstart.md) records repeatable local and CI-parity checks.
- No public API or brand schema change is planned.

## Implementation sequence

1. Add failing focused assertions for the description's parent/order, title/marker geometry, and References field grouping and anchors.
2. Change the home heading markup and scoped style for #335.
3. Add bounded title fitting and a contained wrap fallback for #310, preserving marker association.
4. Reformat the 68 reference entries without changing their text or links, then add route-scoped compact styling for #311.
5. Re-run source checks, rendered site checks at desktop/390px/320px and 200% enlargement, docs reference checks, site lint/build, and the full documented repository validation. The full gate exposed newly vulnerable WordPress fixture transitives, so pin their verified patched releases in the fixture manifest and lockfile and rerun its tests and audit.
6. Inspect before/after renders and exact-copy/link diffs. Record verification, update the changelog, commit the source and Spec Kit artifacts, then push and open a PR under the owner's explicit authorization.

## Complexity Tracking

No constitution exception or new dependency is required. The measured title fit is the only behavior added to the client component; its lower bound and resize triggers are explicit so it cannot grow into a general typography system.
