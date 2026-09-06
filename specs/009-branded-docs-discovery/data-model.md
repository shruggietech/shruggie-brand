# Data Model: Branded Documentation and Discovery Completion

## CanonicalRoute

Represents one indexable public HTML route.

| Field | Type | Rules |
|-------|------|-------|
| `key` | string | Unique stable identifier using safe lowercase segments |
| `kind` | enum | `home`, `brand`, `downloads`, `guidelines`, `docs-index`, or `docs-page` |
| `pathname` | string | Root-relative, begins and ends with `/`, contains no query, fragment, traversal, or duplicate slash |
| `canonical` | URL string | Exactly `https://brand.shruggie.tech` plus `pathname` |
| `title` | string | Source-derived page title without the global title-template suffix |
| `documentTitle` | string | Exact emitted browser title ending in `| ShruggieTech` |
| `description` | string | Non-empty, route-relevant source-derived summary |
| `social` | SocialPreview | Unique deterministic preview record |
| `breadcrumbs` | Breadcrumb[] | Ordered from home to current page; empty only for home |
| `brandSlug` | string or null | Required for brand, downloads, and guidelines kinds |
| `docsSlug` | string or null | Required for nested documentation pages |

### Validation

- Keys, pathnames, canonicals, and social paths are unique.
- Paths remain on the brand-subdomain origin and use the configured trailing-slash policy.
- Every route maps directly to one exported `index.html` path.
- Brand-backed values come from verified public brand records.
- Documentation-backed values come from generated documentation records.

## SocialPreview

| Field | Type | Rules |
|-------|------|-------|
| `path` | string | Root-relative PNG path below `/social/` |
| `url` | URL string | Absolute brand-subdomain URL derived from `path` |
| `width` | integer | Exactly 1280 |
| `height` | integer | Exactly 640 |
| `type` | string | Exactly `image/png` |
| `alt` | string | Route-relevant and non-generic |
| `eyebrow` | string | Short page-kind context used in the image |

## Breadcrumb

| Field | Type | Rules |
|-------|------|-------|
| `name` | string | Human-readable source-derived label |
| `url` | URL string | Exact canonical URL of an existing ancestor or current route |

Breadcrumb positions are assigned from one in emitted JSON-LD. Root has no breadcrumb graph. Documentation pages contain Home, Documentation, and current page. Brand child routes contain Home, brand, and current page.

## StructuredDataGraph

Each route emits an `@graph` containing:

- One minimal external Organization reference with `@id` and `url` equal to `https://shruggie.tech` and name `ShruggieTech`.
- One brand-subdomain WebSite node with stable `@id`, canonical root URL, name, and publisher reference.
- One page node whose type matches `CanonicalRoute.kind` and whose `@id` is `canonical + "#webpage"`.
- One BreadcrumbList for every non-root route.
- A homepage ItemList of public brand page URLs.
- A neutral Brand node on a brand page using public name, description, canonical URL, and logo without ownership claims.

## DocumentationNotice

| Field | Type | Rules |
|-------|------|-------|
| `marker` | enum | `[!NOTE]`, `[!WARNING]`, or `[!CAUTION]` at the start of a blockquote |
| `type` | enum | `info`, `warn`, or `error` |
| `body` | string | One or more quoted lines copied from the authoritative source |

Markers inside fenced code are literal. Ordinary blockquotes remain ordinary blockquotes. The transformation preserves body text and fails closed on an unsupported alert marker.

## DocumentationThemeContract

Maps canonical palette and typography roles to documentation semantic roles.

| Role group | Required source |
|------------|-----------------|
| Background, card, popover, secondary, hover | Generated ShruggieTech surface tokens |
| Text and muted text | Generated foreground and muted roles with measured AA contrast |
| Active, link, progress, and focus | Bright green on dark surfaces and accessible green on light surfaces |
| Rare warning emphasis | Canonical permitted orange or framework warning and error semantic roles with measured contrast |
| Display, body, and mono | Bundled Space Grotesk, Geist, and Geist Mono faces |

## VerificationFinding

| Field | Type | Rules |
|-------|------|-------|
| `route` | string | Route or source file that failed |
| `contract` | string | Code, notice, navigation, theme, metadata, graph, sitemap, preview, accessibility, or hygiene |
| `expected` | string | Exact rule or value |
| `actual` | string | Observed value with safe truncation |

A non-empty finding collection blocks S009 publication.
