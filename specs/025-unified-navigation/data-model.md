# Data Model: Unified Site Navigation and Route Consolidation

## Navigation Section

- `label`: exact concise top-level presentation label.
- `order`: unique ordinal within one navigation tree.
- `destination`: optional direct destination for a leaf top-level entry.
- `children`: ordered navigation destinations for a grouped entry.

Validation requires unique keys and labels, contiguous order, a destination or children but not both, and exactly the hierarchy declared by the applicable portal contract.

## Navigation Destination

- `key`: stable topic or documentation slug.
- `label`: concise sidebar label.
- `path`: canonical internal pathname ending in `/`.
- `title`: retained content-page title, distinct from the sidebar label.
- `section`: owning section key.
- `order`: unique ordinal within the section.

Each destination appears exactly once. Every path must resolve to one route record, and every mapped content record must have one destination.

## Brand Portal

- Existing brand identity, content, palettes, asset families, resources, and instructions remain unchanged; the portal brand projection carries the existing version so migrated Overview copy stays complete.
- `topics[]` gains `label`, `section`, `order`, and `path` presentation metadata.
- The `assets` topic path is `/<slug>/downloads/`; all other topic paths remain under `/<slug>/guidelines/`.

All six public portals expose the same topic keys and ordered hierarchy. Missing optional Integration content produces an empty state without removing the topic.

## Documentation Record

- Existing `slug`, `title`, `description`, and `content` remain unchanged.
- `navigation` contains `section`, `sectionOrder`, `label`, `order`, and `path`.
- The synthetic documentation index maps to Overview; nine reference documents map exactly once to approved child groups.

## Route Record

- `kind` excludes the retired `brand` kind.
- Brand guideline and download breadcrumbs use the guidelines root as the brand destination.
- Home structured data lists public guideline URLs rather than removed brand roots.
- Route paths, canonical URLs, social paths, and keys remain unique and safe.

## Registry Catalog Relationship

- One catalog at `/<slug>/brand/r/registry.json` advertises item names and types.
- Each catalog item maps to one sibling `/<name>.json` endpoint.
- Catalog schema and registry-item schema remain distinct.
- Publication fails if an item is missing, malformed, duplicated, or incorrectly typed.

## State Transitions

1. Existing generated inventories contain flat topics and brand-root route records.
2. Preparation validates complete content and registry inventories.
3. Preparation emits authoritative hierarchical navigation and routes without brand roots or `/guidelines/assets/`.
4. Static export renders shared trees and the combined Assets destination.
5. Validation rejects stale links, duplicate mappings, invalid active states, or inaccessible navigation.
