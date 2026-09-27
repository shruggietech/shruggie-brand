# Feature Specification: WordPress Brand Delivery

**Feature Branch**: `codex/062-wordpress-brand-delivery`
**Created**: 2026-09-27
**Status**: Ready for review
**Input**: S062 completes #273 and #274 as one end-to-end native WordPress delivery. Generate a source-bound adapter first, then an installable block-theme starter and an upgradeable client handoff.

## Clarifications

The owner approved native WordPress core blocks and Site Editor as the baseline. No page builder, commerce, forms, multilingual, or client-specific information architecture is presumed. The latest stable core version observed in the official release news on 2026-09-27 is 7.1.2. Support claims will name exact WordPress and PHP versions exercised by integration fixtures, not infer compatibility from schema checks.

## User Scenarios & Testing

### User Story 1 - Apply approved brand values in WordPress (Priority: P1)

A developer generates a brand kit and receives native WordPress presets, block styles, local fonts, asset references, support records, and versioned instructions without reconstructing a second palette.

**Independent Test**: Generate a kit for a production brand and a temporary independent-palette fixture. Inspect native editor and published page values from a clean pinned WordPress instance, compare them with the resolved brand and interface contracts, and confirm unrelated admin UI is unchanged.

**Acceptance Scenarios**:

1. Given a valid brand source, when the kit is built, then `wordpress/adapter.json`, `wordpress/theme/stbb-<slug>/theme.json`, scoped styles, support records, and referenced local assets are present and checksummed.
2. Given formal identity colors and interface cues, when WordPress loads the adapter, then they retain distinct names, purposes, and readable combinations in the editor and front end.
3. Given saved Global Styles overrides, when a new generated theme is installed, then client changes remain and the handoff identifies differences from file defaults.

### User Story 2 - Start a usable client site (Priority: P1)

An operator installs a generated ZIP, activates a brand-specific block theme, builds a representative page from native patterns, edits it, and publishes it with matching front-end appearance.

**Independent Test**: Install and activate the ZIP on a temporary supported WordPress instance; insert, save, reopen, and render a page with the starter patterns; exercise navigation, buttons, media, search, archive, and empty states.

**Acceptance Scenarios**:

1. Given an untouched WordPress installation, when the ZIP is uploaded and activated, then theme metadata, fallback and specific templates, header/footer parts, fonts, assets, and core-block patterns work without another plugin.
2. Given nested and repeated patterns, when a user edits and saves them, then they reopen without invalid-block recovery or duplicate IDs.
3. Given a non-root site URL, narrow viewport, keyboard navigation, or reduced-motion preference, when the site renders, then assets resolve and content remains usable at WCAG 2.1 AA.

### User Story 3 - Upgrade without losing client work (Priority: P1)

A developer can identify generated files, client-owned content, and database overrides, export customizations, install a pinned update, inspect conflicts, and roll back.

**Independent Test**: In a temporary site, create a page and saved style/template override, replace the theme package with a regenerated version, verify content and overrides persist, produce a drift report, and restore the previous package.

**Acceptance Scenarios**:

1. Given an installed theme and client edits, when the generated package changes, then the edits remain in WordPress and the update guide explains which file defaults are masked by database state.
2. Given a kit archive, when a consumer checks its manifest, then WordPress package bytes, adapter version, brand version, and compiler version trace to the same source revision.

### Edge Cases

- Brand slugs that share their first two letters, contain punctuation, or have long names must produce collision-resistant `stbb-` identifiers and valid WordPress slugs.
- Missing or unlicensed assets, unsupported font weights, unsupported schema properties, unsafe archive paths, and unsupported core/PHP combinations must fail or be reported explicitly.
- Supplemental CSS must not restyle admin chrome, unrelated plugin UI, or other themes; editor iframe and non-iframe configurations need honest support records.
- Saved Global Styles, template overrides, and plugin filters can outrank theme files; a regenerated file alone cannot be called the effective site state.
- An optional style variation is an editor selection, not a visitor-facing light/dark toggle.

## Requirements

### Functional Requirements

- **FR-001**: Generate a first-class WordPress adapter from the resolved brand, interface, color-role, and component-recipe contracts using native `theme.json` format 3 and a scoped CSS supplement only where needed.
- **FR-002**: Preserve identity versus interface-cue semantics; map typography, local font faces, spacing, widths, borders, links, buttons, group/columns, media/captions, navigation, and core-block states to stable `stbb-` names and source-derived values. Provide an editor-selected dark style variation from approved dark roles without claiming visitor switching.
- **FR-003**: Emit adapter support classification for each relevant recipe and block as native, adapted, unsupported, or unverified, with a concrete reason and tested-version evidence. A shared recipe name alone cannot imply implementation.
- **FR-004**: Package a valid brand-specific block theme with required metadata, `theme.json`, template fallback, useful page/post/archive/search/404 templates, header/footer parts, and editable native patterns for hero, text/media, features, and contact/action sections.
- **FR-005**: Bundle licensed local fonts and approved image assets with portable references; preserve logo path geometry, aspect ratio, and attribution. Do not require remote fonts, React, Next.js, or unrestricted SVG uploads.
- **FR-006**: Provide a safe, deterministic ZIP and exact inventory/checksums, plus adapter, brand, compiler, and WordPress/PHP compatibility metadata in kit and consumer contracts. Generated themes and test fixtures remain outside Git.
- **FR-007**: Document install, composition, saved-override precedence, client-owned changes, export, pinned update, conflict reconciliation, rollback, and supported/untested ecosystem boundaries. Extend official skill and generated instructions.
- **FR-008**: Test in pinned clean WordPress fixtures: install/activate, editor versus front-end values, pattern round trip, navigation and content flows, non-root asset URLs, and update/rollback behavior. Schema-only and CSS-string checks are insufficient.
- **FR-009**: Verify focus, keyboard, reflow, long text, non-color cues, reduced motion, and contrast against WCAG 2.1 AA without waivers. Preserve existing adapters and all eight production kit gates.
- **FR-010**: Select a specific minimum WordPress/PHP pair and current stable pair in the plan; state only combinations actually exercised as supported. The optional Gutenberg plugin is not a dependency.

### Key Entities

- **WordPress adapter**: Native theme settings/styles, scoped supplement, local asset map, support matrix, and exact version authority.
- **Brand starter theme**: Installable archive containing templates, parts, patterns, assets, metadata, and guidance.
- **Customization state**: Client content, saved Global Styles, saved template/part overrides, and generated file defaults with explicit precedence.
- **Compatibility record**: Exact core, PHP, adapter, brand, compiler, and schema versions plus test evidence.

## Success Criteria

- **SC-001**: #273 and #274 each have complete acceptance-to-test disposition in S062 verification evidence.
- **SC-002**: The generated ZIP installs and activates on each declared supported fixture; a representative pattern page survives edit/save/reopen and renders with matching tokens.
- **SC-003**: All eight kits report zero `verify.py` problems and zero `validate_glyph.py` failures; existing adapter tests and site/publication audit remain green.
- **SC-004**: Archive inventory matches actual package entries, checksums match bytes, and no generated output enters Git.
- **SC-005**: WCAG 2.1 AA checks pass for the starter's declared text and fill roles, keyboard/focus and responsive behavior; any untested ecosystem integration is labeled unverified.

## Assumptions and Boundaries

- Client-specific site content, forms, commerce, multilingual plugins, page builders, and hosting choices are discovered per engagement; S062 supplies a reusable native foundation.
- The current brand identities and logo path data remain unchanged.
- A formal public release is separate from this PR. PR CI builds candidate artifacts from source.
