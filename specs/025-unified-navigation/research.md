# Research: Unified Site Navigation and Route Consolidation

## Decision 1: Use `/downloads/` as the sole Assets page

**Decision**: Keep `/<brand-slug>/downloads/` and place both direct downloads and the generated asset library there. Remove `/guidelines/assets/` from generated routes and navigation.

**Rationale**: Issue #175 explicitly preserves the downloads route, while #180 requires Downloads and Asset Library to become one destination. This is the only option that satisfies both without an alias or duplicate page.

**Alternatives considered**: Keep both pages with cross-links (rejected as a duplicate); move everything to `/guidelines/assets/` (rejected because `/downloads/` must remain functional); generate a redirect (rejected because static GitHub Pages export has no dependable per-brand redirect mechanism).

## Decision 2: Return normal not-found responses for removed brand roots

**Decision**: Delete the root dynamic page and omit brand-root records from every generated contract.

**Rationale**: The repository uses static export and the issue explicitly permits documented intentional not-found behavior where redirects are unsupported.

**Alternatives considered**: Empty shell pages and client redirects (rejected as retained pages with poor semantics); host-specific redirect files (rejected as a new deployment contract not currently supported).

## Decision 3: Generate navigation assignments with content records

**Decision**: Add concise label, section, order, and path metadata to the generated brand-topic and documentation inventories, then construct presentation trees from those records.

**Rationale**: The generator already owns portal and documentation inventories. Extending those records creates one authoritative source for desktop, mobile, no-script, active-state, and test consumers without duplicating content or brand values.

**Alternatives considered**: Hard-code separate TSX lists (rejected because presentations can drift); reorganize source document directories (rejected because documentation URLs need no route change); infer groups from display titles (rejected as brittle).

## Decision 4: Lift the guideline shell above guidelines and downloads

**Decision**: Place the shared brand `DocsLayout` at `(guidelines)/[slug]/layout.tsx`, with guideline topics and downloads as sibling routes beneath it.

**Rationale**: Assets must remain at `/downloads/` while participating in the same nested navigation and active-parent behavior as the rest of the brand portal.

**Alternatives considered**: Duplicate the layout in the downloads page (rejected as two navigation renderers); keep downloads in the generic site shell (rejected because Assets would leave the portal hierarchy).

## Decision 5: Preserve documentation routes and titles

**Decision**: Keep all current documentation slugs, page frontmatter, metadata, and content while replacing only the generated navigation tree.

**Rationale**: Grouping does not require route changes, and issue #179 explicitly calls for shortened labels without renaming actual pages.

**Alternatives considered**: Move pages into physical group directories (rejected due to URL churn and redirects); rename frontmatter titles to labels (rejected because it changes page identity).
