<!--
SYNC IMPACT REPORT
Version change: template -> 1.0.0
Added principles:
  - P1. Sources are committed and artifacts are rebuilt
  - P2. Identity geometry is preserved
  - P3. Accessibility has no exemption
  - P4. Verification precedes publication
  - P5. The site consumes generated kits
  - P6. Specifications and releases move together
Added sections:
  - Technical and documentation constraints
  - Development workflow
Removed sections: template placeholders
Follow-up TODOs: none
-->

# Shruggie Brand Constitution

This file is the durable law for the ShruggieTech brand-system repository. Product identity decisions live in source `brand.json` files and the canon. Change-specific decisions live in Spec Kit artifacts under `specs/`.

## Core Principles

### P1. Sources are committed and artifacts are rebuilt

Git MUST contain generator source, canon and reference documentation, source-only kit definitions, shared font sources, fixture source, CI, and site source. Generated kits, PDFs, raster images, registries, static exports, and release archives MUST be rebuilt by automation and MUST NOT be committed. Bundled font binaries are the sole binary-source exception.

### P2. Identity geometry is preserved

Shipped logo geometry MUST NOT be redrawn, normalized, optimized, or re-derived during a migration or generator change. Existing path data remains source of truth. An identity change requires an explicit owner decision, written rationale, and identity comparison evidence. Accessibility corrections are pre-authorized only for the value required to reach the AA floor.

### P3. Accessibility has no exemption

WCAG 2.1 AA at rendered size is the minimum for every text-bearing and declared fill role. `aa-floor`, `accent-rule`, `globals-slots`, and `contrast-rederived` are non-exemptable. A failing value MUST change before publication. Legacy status, deadlines, and operator preference cannot waive the requirement.

### P4. Verification precedes publication

Every production kit and fixture MUST report zero problems from `verify.py` and zero failures from `validate_glyph.py`. CI MUST rebuild all kits whenever generator, canon, kit, fixture, font, or build code changes. PDF and PNG byte identity is not a correctness gate. Missing optional capabilities MUST be recorded as explicit skips.

### P5. The site consumes generated kits

The static site owns navigation, documentation rendering, and shell chrome. It MUST copy per-brand guidelines, registries, logo masters, favicons, specimens, and downloads from verified `dist/` output without restating or independently authoring those values. The site build MUST consume its own registry so malformed binding output fails before deployment.

### P6. Specifications and releases move together

Features, architecture changes, generator changes, migrations, site behavior, CI, and releases MUST use the repository-installed Spec Kit workflow. Release tags use `vMAJOR.MINOR.PATCH`. Every release MUST state skill version, canon version, and whether existing kits require migration. Release assets MUST be built by CI from the tagged revision.

## Technical and Documentation Constraints

- Text files MUST use UTF-8 without BOM and LF line endings. Deliverables MUST be checked for mojibake.
- Authored prose SHOULD avoid em dashes.
- Site source uses Next.js App Router with static export and local bundled fonts.
- Python 3.8 is the minimum skill runtime and Node.js 20 is the minimum site runtime.
- Apache-2.0 covers code and documentation. Names, marks, wordmarks, endorsement lockups, and logo path geometry remain reserved. Font sources retain their SIL Open Font License 1.1 terms.
- Architecture diagrams use Mermaid only when they materially improve comprehension, with top-to-bottom layout.

## Development Workflow

Work starts with a numbered specification under `specs/`, proceeds through planning and tasks, and passes cross-artifact analysis before completion. Pull requests include issue traceability, build evidence, accessibility impact, identity impact, documentation impact, and a changelog decision. The aggregate gate rebuilds all production kits and the fixture, validates Spec Kit and generated agent entry points, builds the site, and audits repository hygiene.

## Governance

This constitution supersedes conflicting repository practices. Amendments use the Spec Kit constitution workflow and semantic versioning independent of the brandbuilder version. A major amendment removes or incompatibly redefines a principle, a minor amendment adds or materially expands governance, and a patch clarifies existing law. Temporary exceptions require explicit scope, owner, rationale, and expiry, and no exception may weaken P2, P3, or P4.

**Version**: 1.0.0 | **Ratified**: 2026-09-03 | **Last Amended**: 2026-09-03
