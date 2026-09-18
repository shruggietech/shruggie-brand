# Data Model: Documentation Contract Boundaries

## Documentation Contract

| Field | Meaning | Validation |
| --- | --- | --- |
| `schema_version` | Structural version | Exact supported integer |
| `contract_version` | Independent documentation-policy version | Valid semantic version |
| `required_topics` | System-manual coverage vocabulary | Required topic identifiers exactly once |
| `surfaces` | Main, hosted, and bundled ownership boundaries | Exactly three declared surfaces with distinct audiences and authority |
| `manual_pages` | Governed Markdown pages and navigation | Every source page exactly once, safe path, unique slug and position |
| `source_dispositions` | Migration decision for each current source | Complete inventory with owner, action, destination, and rationale |
| `route_dispositions` | Policy for documentation-related route kinds | Every generated documentation route resolves to one policy |
| `shared_fact_fields` | Facts that must agree across projections | Required exact field paths exactly once |
| `graphics` | Required semantic overview graphics | Ownership, modes, and improvement loop exactly once |

## Manual Page

| Field | Meaning | Validation |
| --- | --- | --- |
| `slug` | Stable public page identifier | URL-safe, unique, matches source stem |
| `source` | Markdown authority under references | Safe contained relative path and existing file |
| `title` / `description` | Navigation and metadata copy | Non-empty direct prose |
| `section` / `label` | Hierarchy placement | Non-empty, unique section-order/page-order pair |
| `section_order` / `order` | Stable navigation ordering | Non-negative integers |
| `pagination_order` | Previous/next sequence | Unique contiguous positive integer |
| `topics` | Required topic groups covered by the page | Known topic identifiers, complete across catalog |

## Documentation Fact Record

| Field | Meaning | Validation |
| --- | --- | --- |
| `schema_version` | Generated fact shape | Exact supported integer |
| `documentation_contract_version` | Policy used to project facts | Matches copied contract |
| `brand` | Slug, title, brand version, affiliation | Matches brand and consumer contract |
| `versions` | Brand Canon, Interface Canon, recipes, Web/React, egui, compiler, brand | Exact consumer contract equality |
| `bindings` | Supported renderer and host artifacts | Safe relative paths that exist in kit |
| `authority` | Ordered local source and instruction paths | Matches consumer contract authority |
| `verification` | Exact entry points and success rule | Matches consumer contract verification |
| `recovery` | Exact offline distribution, checksum, and extract path | Matches consumer contract recovery |
| `capability_gap` | Local record path and authorization boundary | Matches consumer contract gap policy |
| `hosted` | Manual path and current-kit scope statement | Safe public path and explicit current scope |
| `bundled` | Offline authority statement | Explicit pinned-byte authority and no-latest rule |

## Documentation Surface

| Surface | Audience | Owns | Must not own |
| --- | --- | --- | --- |
| Main manual | Maintainers and extenders | Architecture, modes, canons, generators, adapters, verification, versions, releases, installation, agents, extensions | Individual brand identity and exact delivered-byte authority |
| Hosted child reference | Designers, stakeholders, current implementers | Approved brand expression, assets, specimens, bindings, overrides, current generated versions | Compiler architecture and historical pinned-byte authority |
| Bundled implementation contract | Consumer agents and engineers | Exact delivered paths, versions, constraints, checks, recovery, and escalation | Public showcase prose and unspecified latest behavior |

## Content Disposition

| Field | Meaning | Validation |
| --- | --- | --- |
| `source` | Existing source file or route kind | Safe source path or known generated route kind |
| `owner` | Main, hosted, bundled, provenance, or brand source | Closed vocabulary |
| `action` | Preserve, consolidate, generate, redirect, or retire | Closed vocabulary |
| `destination` | Resulting source or route | Required except approved retirement |
| `rationale` | Why the disposition preserves or removes value | Non-empty |

## Overview Graphic

| Field | Meaning | Validation |
| --- | --- | --- |
| `id` | Ownership, modes, or improvement loop | Required and unique |
| `title` | Reader-facing heading | Non-empty |
| `nodes` | Semantic ordered or definition-list items | At least three labeled items |
| `relationships` | Directed or ownership relationship labels | Every endpoint exists |
| `text_equivalent` | Adjacent prose expressing the same relationships | Non-empty and visible |

## Projection Flow

`documentation-contract.json -> manual navigation and content coverage`

`brand + consumer contract + generated adapters -> documentation-facts.json -> IMPLEMENTATION.md`

`documentation-facts.json -> guidelines/portal.json -> hosted child-brand summary`

Any source, version, adapter, verification, recovery, or gap-policy change produces a new fact record. A structural mismatch, missing path, or projection difference fails verification before site staging.
