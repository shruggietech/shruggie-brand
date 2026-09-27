# S059 Route Data Model

## Guideline topic

Fields: stable semantic `key`, reader-visible `label`, section and order, content title/description, canonical `path`. The final `path` segment is the normalized label slug. One brand may omit an optional topic. Paths and slugs are unique within a brand.

## Canonical page route

Fields: route key, kind, canonical pathname/URL, brand/topic identifiers, title/description, social image references, breadcrumbs, and structured data. Each present topic has exactly one canonical route and one export page. Overview keeps the brand-level guideline route kind used by Brand structured data; Assets keeps its collection-page kind.

## Legacy page bridge

Fields: legacy pathname, canonical destination, navigation mechanism, canonical URL, and robots exclusion. A bridge has no route-record or sitemap entry, no independent social preview, and no duplicated guide content. The current mapping is guidelines root to Overview, guidelines/logos to Logo, and downloads root to Assets, for each brand.

## Download file URL

Fields: existing path, bytes, digest, and delivery metadata. It is outside the guideline page namespace and must not be rewritten by the page migration.

## Relationships and validation

Each canonical topic route belongs to one brand and one generated topic. A legacy bridge targets exactly one canonical route in the same brand. All bridges are direct, without chains. The publication inventory includes canonical page routes and excludes bridges. Direct file paths have no bridge relationship.
