# Feature Specification: Canonical Brand Guideline Routes

**Feature Branch**: `codex/059-guideline-canonical-routes`

**Created**: 2026-09-26

**Status**: Implemented and locally verified, PR review in progress

**Input**: S059 addresses issue #285. Give every dedicated brand guideline menu item a predictable page URL whose final segment matches the visible menu label, migrate site references, and keep existing public page links usable.

## User Scenarios & Testing

### User Story 1 - Predictable guideline destinations (Priority: P1)

A visitor reading any brand's guideline menu can infer a page URL from the plain-English label and share that page with confidence.

**Why this priority**: Current Overview, Logo, and Assets destinations break the label-to-path pattern and make navigation harder to predict.

**Independent Test**: Inspect every menu item across all eight production brands and an optional-topic brand. Each item opens the page whose final path segment is the documented lowercase slug of its label.

**Acceptance Scenarios**:

1. **Given** the Overview, Logo, and Assets entries, **when** a visitor opens each entry, **then** the destinations end in `/overview/`, `/logo/`, and `/assets/` respectively.
2. **Given** any other dedicated topic entry, **when** its label is compared with its destination, **then** the final path segment follows the same documented slug rule.
3. **Given** a brand with an optional topic or a future brand using the same topic contract, **when** its menu is built, **then** it follows the same rule without a brand-specific exception.

---

### User Story 2 - Existing page links still work (Priority: P1)

A visitor arriving from an existing bookmark or external link reaches the corresponding canonical guideline page.

**Why this priority**: Public links to the old overview, logo, and asset page paths already exist.

**Independent Test**: Open every pre-S059 page URL whose destination changed, with and without its trailing slash; each settles on exactly one canonical page and is excluded from the indexable page inventory.

**Acceptance Scenarios**:

1. **Given** a legacy brand guidelines root, **when** a visitor opens it, **then** it leads to that brand's Overview page.
2. **Given** legacy Logo or Assets page links, **when** a visitor opens them, **then** they lead to the same brand's canonical Logo or Assets page.
3. **Given** a direct file download URL, **when** a visitor opens it, **then** the same file remains available; page-route migration does not reinterpret file URLs.

---

### User Story 3 - One consistent published identity for each page (Priority: P2)

A visitor, search engine, or link preview sees the canonical page URL wherever the site describes or links to a guideline page.

**Why this priority**: Stale links and metadata can create duplicate pages or inconsistent previews after the route change.

**Independent Test**: Audit menus, breadcrumbs, pagination, search, page metadata, structured data, sitemap, and published page inventory for all brands. All discoverable references target canonical pages, while the general `/docs/` manual remains a separate navigation tree.

**Acceptance Scenarios**:

1. **Given** a canonical topic page, **when** its navigation, metadata, and structured data are inspected, **then** they refer to that page's single canonical URL.
2. **Given** a legacy page URL, **when** its published representation is inspected, **then** it has one redirect destination and cannot be indexed as a duplicate content page.
3. **Given** the main `/docs/` manual, **when** its routes are inspected, **then** they retain their established path contract.

### Edge Cases

- A menu label may contain spaces or punctuation in future. Its lowercase URL slug must be deterministic, documented, and unique within one brand.
- A topic may be optional for one brand. No orphan navigation entry, redirect, or canonical page should be generated for an absent topic.
- A legacy page path may be requested without a trailing slash or with query and fragment information. Navigation should settle on the same canonical destination while retaining useful fragment and query context where possible.
- Page URLs and URLs under a brand's direct download file tree have different purposes and must never collide.
- A legacy redirect must not form a chain, loop, or additional indexable copy of the destination.

## Requirements

### Functional Requirements

- **FR-001**: The site MUST define one documented lowercase slug grammar for every dedicated brand guideline menu label and MUST use that slug as the final canonical page path segment.
- **FR-002**: The canonical topic page pattern MUST be `/<brand>/guidelines/<label-slug>/` for every dedicated menu item, including Overview, Logo, Assets, and optional topics.
- **FR-003**: The same topic contract MUST drive generated brand guideline menus, page inventory, and site navigation for all eight production brands and future compatible brands, without brand-specific route exceptions.
- **FR-004**: Existing public page paths that change in S059 MUST lead directly to their one canonical replacement, including the guidelines root and existing Logo and Assets page paths. Legacy entries MUST not be included in the canonical sitemap or indexable page inventory.
- **FR-005**: Direct downloadable file URLs MUST remain distinct from navigation page URLs and continue to resolve to their existing files.
- **FR-006**: Internal links, breadcrumbs, pagination, search entries, route descriptions, canonical and social metadata, structured data, robots and sitemap references, and publication checks MUST use canonical page URLs.
- **FR-007**: The general `/docs/` manual MUST retain its existing route structure and navigation scope.
- **FR-008**: Route validation MUST reject duplicate slugs, missing destinations, stale canonical references, redirect chains or loops, and legacy pages exposed as indexable content.
- **FR-009**: The navigable pages and redirects MUST preserve keyboard access, readable fallback navigation, and WCAG 2.1 AA behavior.

### Key Entities

- **Guideline topic**: A visible label, stable key, documented label slug, brand scope, and canonical page path.
- **Canonical page**: The single indexable destination for one brand topic, with navigation and metadata references.
- **Legacy page route**: A prior public page URL mapped directly to one canonical page and excluded from indexable content.
- **Download file URL**: A direct asset location independent of guideline page navigation.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every dedicated guideline menu item in all eight production brands, including the optional Expressions topic where present, opens a page whose final segment exactly matches its documented label slug.
- **SC-002**: Every changed pre-S059 page path reaches its intended canonical page without an application-level redirect chain or loop, with no legacy page listed in the sitemap or canonical route inventory. The static host may first normalize a missing trailing slash.
- **SC-003**: All internal page references and published page metadata for migrated topics use the new canonical URL; direct download file paths remain retrievable.
- **SC-004**: All eight production kits report zero verification problems and zero glyph validation failures; the site passes its documented accessibility and publication checks.
- **SC-005**: A visitor can find, open, and share Overview, Logo, and Assets from any brand's menu without encountering a dead link or duplicate page.

## Assumptions

- The established visible labels are retained. S059 changes route destinations, not brand vocabulary or approved visual identity.
- The site remains statically published; a redirect may use a static compatibility page if the publishing host does not support server-side status redirects. The compatibility page must immediately navigate to, identify, and canonically reference its destination while preventing duplicate indexing.
- Existing direct file URLs under each brand's downloads tree remain stable. The old Assets *page* URL is distinct from the file subtree.
- Issue #270's wider documentation architecture is outside S059. This slice resolves issue #285 and only updates adjacent links needed for the route migration.
- S059 prepares a PR and validation evidence. Formal public release and merge remain separate owner decisions.
