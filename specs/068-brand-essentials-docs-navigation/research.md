# S068 research and decisions

## Current source and publication state

The production inventory is eleven brands. S067 put approved messaging decisions in `brand.json.messaging` and retained historical visual instructions in `brand.json.guidance`. Only ShruggieTech currently has a slogan approved for visual-guide use. Six short descriptions are approved for site metadata only; no other brand-specific words may be promoted from legacy guide fields. The current generated publication record is a 3.0.0 review candidate, while the inspected hosted /docs/ site still shows the 2.8.0 official release. The sidebar footer is emitted by Fumadocs `DocsLayout` when its theme switch is present: a full-width bordered flex row contains only a right-aligned switch.

## Guide boundary

The source-facing section order is Name and relationship, Approved words when present, Visual signatures, Where each asset belongs, Usage limits, and optional Brand strategy. Product scope and generic promises remain in the S067 migration evidence and are classified again in the S068 disposition inventory; they are not brand identity rules. Existing `logo.prohibitions`, `guidance.logo`, `guidance.palette`, typography, affiliation, and verified asset families can supply concrete essentials without rewriting identity geometry or inventing copy. Optional strategy uses only explicit approved message decisions whose `uses` include `visual-guide`.

The PDF already has a second sheet for name and historical personality/promises. Replace that sheet's product/brand-strategy content with Brand essentials and keep detailed logo, color, and typography sheets. The portable guide currently has a message-only header and detailed implementation and asset sections. Add an essentials section and derive its contents navigation from actual rendered sections. The hosted guide consumes the generated portal's source-bound essentials data; its TOC must be derived from the same section presence instead of a fixed list.

## Sidebar decision

Fumadocs exposes a supported `slots.themeSwitch` override. The first option was a dedicated version label with a release link whenever the publication status is `release`; the second was a compact switch only. Use both according to the source publication state. A candidate's future tag URL is not an existing release, so candidate builds show a compact switch without a link. Release builds show the exact `publication.version` with `publication.releaseUrl`. No version selector is offered because the docs tree is unversioned.

## Validation decision

The source and output changes require focused Python tests, all eleven kit rebuilds, HTML/PDF content checks, site lint/build and browser checks, and the documented publication audit. Tests inspect text and layout rather than PDF or PNG byte identity. Source changes are confined to the compiler, site, documentation, and Spec Kit evidence; no logo paths, brand source approvals, or generated `dist/` files are committed. The active 3.0.0 candidate version remains unchanged until a release decision; the S068 change is recorded in Unreleased.
