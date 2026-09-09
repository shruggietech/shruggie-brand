# Feature Specification: Unified Site Navigation and Route Consolidation

**Feature Branch**: `codex/025-unified-navigation`

**Created**: 2026-09-09

**Status**: Draft

**Input**: Work slice S025 covering GitHub issues #175, #179, and #180.

## User Scenarios & Testing

### User Story 1 - Reach useful brand guidance directly (Priority: P1)

A portfolio visitor can move directly from the homepage into a brand's useful guidance or assets without passing through a redundant brand landing page.

**Why this priority**: Removing the obsolete intermediate destination completes the explicit-action model delivered by S024 and prevents dead or misleading navigation.

**Independent Test**: Export the site, enumerate every public brand route and internal link, and confirm that no human-facing brand root is emitted or referenced while each guidelines, assets, archive, registry, and nested delivery endpoint remains available.

**Acceptance Scenarios**:

1. **Given** a published brand, **When** a visitor uses a portfolio action, **Then** the visitor reaches Guidelines or downloads directly and never a redundant brand-root page.
2. **Given** a legacy `/<brand-slug>/` address, **When** the static site is exported, **Then** no content page or route record exists and the host returns its normal not-found response.
3. **Given** a published shadcn catalog, **When** every advertised item is resolved, **Then** each item endpoint exists and validates against its assigned catalog or item schema.

---

### User Story 2 - Scan one consistent brand-guidelines hierarchy (Priority: P1)

A visitor can browse every brand portal through the same concise hierarchy: Overview, Voice, Identity with Logo, Color, and Typography, Components, Assets, and Integration.

**Why this priority**: The current flat, verbose list duplicates overview and download destinations and makes common guidance difficult to scan.

**Independent Test**: Open every brand portal at desktop, narrow, touch-only, no-script, and 200% zoom conditions and verify exact labels, order, nesting, active states, complete content placement, and valid destinations.

**Acceptance Scenarios**:

1. **Given** any public brand portal, **When** its navigation is read, **Then** it presents Overview, Voice, Identity, Components, Assets, and Integration in that order, with Logo, Color, and Typography nested under Identity in that order.
2. **Given** an Identity child page, **When** it is active, **Then** both the current child and its Identity grouping remain understandable.
3. **Given** existing foundations, download, asset-library, messaging, component, or integration content, **When** the new hierarchy is published, **Then** the content appears once in its mapped destination and no obsolete duplicate remains.
4. **Given** a visitor without JavaScript or using keyboard, pointer, or touch input, **When** they traverse the portal, **Then** every destination remains reachable with accurate current and expanded state.

---

### User Story 3 - Scan grouped project documentation (Priority: P2)

A documentation reader can browse the existing documentation through the concise Overview, Foundation, Discovery, Identity, and Implementation hierarchy without changing page titles, content, or URLs.

**Why this priority**: This applies the same navigation discipline to the project documentation after the higher-priority public brand portals are corrected.

**Independent Test**: Compare the generated documentation inventory with the final navigation tree and verify exact one-to-one mapping, labels, groups, URL stability, active states, and complete keyboard/mobile access.

**Acceptance Scenarios**:

1. **Given** the documentation sidebar, **When** it is read top to bottom, **Then** it contains Overview, Foundation, Discovery, Identity, and Implementation in that order with the exact approved children.
2. **Given** a shortened sidebar label such as Contract or Logo, **When** its page opens, **Then** the existing page title and canonical URL remain unchanged.
3. **Given** the complete documentation inventory, **When** it is mapped into the hierarchy, **Then** every page appears exactly once and no page is duplicated or omitted.

### Edge Cases

- A brand with no platform-specific instructions still receives the shared Integration destination and an explicit empty-state explanation instead of a missing or structurally different navigation item.
- The Assets destination must combine the asset library and direct download hub at the stable `/<brand-slug>/downloads/` route, while the obsolete `/guidelines/assets/` page is not emitted.
- Invalid multi-segment guideline topics and removed brand-root paths must not acquire generated route records, sitemap entries, social previews, breadcrumbs, or structured data.
- Navigation must remain complete without JavaScript and at wide touch-only viewports where hover assumptions are invalid.
- Generated navigation labels must not overwrite source document titles or authored brand content.

## Requirements

### Functional Requirements

- **FR-001**: The export MUST emit no human-facing `/<brand-slug>/` page or route record for any public brand.
- **FR-002**: Homepage, footer, guidelines, downloads, documentation, metadata, search, sitemap, breadcrumbs, structured data, and tests MUST contain no internal destination targeting a removed brand root.
- **FR-003**: Removed brand roots MUST use the static host's intentional not-found behavior; S025 MUST NOT retain an empty page or introduce an unsupported redirect layer.
- **FR-004**: Every `/<brand-slug>/guidelines/`, `/<brand-slug>/downloads/`, complete kit archive, downloadable file, and declared registry endpoint MUST remain available.
- **FR-005**: Each registry catalog MUST retain at least the theme and fonts items, resolve every advertised item to a present JSON endpoint, and validate catalog and item shapes without duplicating theme variables into the catalog.
- **FR-006**: Every brand navigation tree MUST expose top-level destinations exactly as Overview, Voice, Identity, Components, Assets, and Integration in that order.
- **FR-007**: Identity MUST contain exactly Logo, Color, and Typography in that order.
- **FR-008**: Overview MUST contain all existing brand overview and foundations content exactly once at `/<brand-slug>/guidelines/`.
- **FR-009**: Assets MUST combine the existing direct-download hub and asset-library content exactly once at the stable `/<brand-slug>/downloads/` route; `/guidelines/assets/` MUST NOT be emitted.
- **FR-010**: Voice, Logo, Color, Typography, Components, and Integration MUST retain their existing authored guidance, examples, generated metadata, and resources under concise navigation labels.
- **FR-011**: All public brands MUST consume the same generated hierarchy; unavailable optional content MUST use an explicit empty state rather than removing a required navigation destination.
- **FR-012**: Brand navigation MUST use semantic nested structures with accurate current-page and expanded parent state on desktop and mobile.
- **FR-013**: Every brand destination MUST remain reachable by keyboard, pointer, touch, and without JavaScript, with visible focus and no clipped or hidden destinations at narrow widths or 200% zoom.
- **FR-014**: Documentation navigation MUST expose top-level sections exactly as Overview, Foundation, Discovery, Identity, and Implementation in that order.
- **FR-015**: Foundation MUST contain Contract and Kit; Discovery MUST contain Interview; Identity MUST contain Logo, Glyphs, and Voice; Implementation MUST contain Toolchain, shadcn, and Portability, each in the stated order.
- **FR-016**: Documentation sidebar labels MAY be shortened, but all existing page titles, content, canonical URLs, metadata, search records, breadcrumbs, and previous/next relationships MUST remain stable and complete.
- **FR-017**: Every documentation page MUST appear exactly once in the authoritative navigation model, with no duplicate or omitted page.
- **FR-018**: Desktop and mobile navigation MUST consume the same authoritative generated hierarchy for each portal so the presentations cannot drift.
- **FR-019**: Route preparation MUST fail closed on duplicate paths, unsafe paths, invalid navigation targets, missing mapped content, duplicate content placement, or a registry catalog that advertises a missing or malformed item.
- **FR-020**: Automated coverage MUST verify exact hierarchy, ordering, nesting, active and expanded states, one-time content placement, URL stability, removed-route absence, registry resolution, no-script behavior, keyboard/touch behavior, 200% zoom, static export, WCAG 2.1 AA, and repository hygiene.

### Key Entities

- **Route record**: The authoritative pathname, canonical URL, page kind, metadata, breadcrumbs, structured data, and brand or documentation association for one emitted page.
- **Navigation section**: An ordered top-level label with either one destination or an ordered set of child destinations.
- **Navigation destination**: A concise sidebar label mapped to one stable route and one retained content source.
- **Brand portal**: Generated brand identity, topic content, asset families, resources, instructions, and its shared navigation hierarchy.
- **Documentation record**: An existing source document's slug, title, description, content, stable URL, and assigned navigation section and label.
- **Registry catalog**: The catalog-schema entry point that advertises installable item names and types, distinct from each populated registry item.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All six public brands emit zero brand-root content pages and zero internal links, route records, sitemap entries, social previews, or structured-data entities targeting those roots.
- **SC-002**: All six brand portals expose the exact six-section hierarchy and exact three-child Identity group, with 100% of prior content mapped once.
- **SC-003**: All six stable downloads destinations combine direct resources and the asset library, while zero `/guidelines/assets/` pages or links remain.
- **SC-004**: All ten documentation destinations appear exactly once under the five approved top-level sections while retaining 100% of existing page titles, content, and canonical URLs.
- **SC-005**: Every generated navigation destination resolves successfully under desktop, mobile, touch-only, no-script, and 200% zoom verification with zero hidden, clipped, duplicate, or unreachable links.
- **SC-006**: Every published registry catalog resolves 100% of its advertised items to valid schema-appropriate JSON endpoints.
- **SC-007**: The documented repository gate reports zero production-kit verification problems, zero glyph failures, zero broken links, zero accessibility violations, and zero repository-hygiene violations.

## Assumptions

- The stable `/<brand-slug>/downloads/` route is the single canonical Assets destination because #175 requires that route to remain functional and #180 requires downloads and the asset library to become one destination.
- The static GitHub Pages export has no supported per-brand redirect facility, so removed `/<brand-slug>/` pages intentionally return the host's normal not-found response.
- Existing guideline topic keys remain stable except that `assets` maps to the stable downloads route and is no longer generated below `/guidelines/`.
- Existing documentation source slugs and page titles remain authoritative; grouping changes navigation presentation only.
- No logo geometry, palette, typography, or authored brand identity content changes are in scope.

## Traceability

- GitHub #175: FR-001 through FR-005, FR-019, FR-020, SC-001, SC-006, SC-007
- GitHub #180: FR-006 through FR-013, FR-018 through FR-020, SC-002, SC-003, SC-005, SC-007
- GitHub #179: FR-014 through FR-020, SC-004, SC-005, SC-007
