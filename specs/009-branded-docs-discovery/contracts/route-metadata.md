# Route Metadata Contract

## Route descriptor

Every indexable HTML page has exactly one record in generated `site/generated/routes.json`. The record follows `data-model.md` and owns all discovery values. Generation fails on an unsafe, external, duplicate, or non-trailing-slash route.

## Metadata

- Browser title, description, canonical, Open Graph, and Twitter values are taken from the route record.
- Open Graph and Twitter each declare the route title, description, exact canonical URL, route-specific PNG URL, 1280 by 640 dimensions where supported, `image/png`, and route-relevant alternative text.
- The root manifest, icons, metadata base, and robots policy remain unchanged unless required for exact contract compatibility.

## Structured data

- JSON-LD is serialized as valid JSON and escapes `<` before insertion into HTML.
- All routes include the minimal authoritative Organization and brand-subdomain WebSite nodes.
- Home uses CollectionPage and an ItemList of public brand URLs.
- Documentation index uses CollectionPage; nested documentation uses TechArticle without invented authors or dates.
- Brand detail uses WebPage and a neutral Brand node without ownership claims.
- Downloads uses CollectionPage; copied guidelines use WebPage.
- Every non-root route includes an ordered BreadcrumbList whose item URLs equal route-record canonicals.

## Sitemap and direct resolution

- The sitemap contains exactly the canonical set of all route records, without duplicates.
- Every location ends with `/`, maps to an exported `index.html`, returns HTTP 200 with redirects disabled, and equals the page canonical and Open Graph URL.

## Social assets

- Preparation safely replaces only the validated `site/public/social/` generated directory.
- Every record points to one unique deterministic PNG that decodes as 1280 by 640, uses local fonts and canonical marks, contains route-relevant visible text, and agrees with metadata.
- Stale preview files are removed before current generation.

## Copied guidelines

- Python guideline metadata injection accepts a complete route record rather than assembling its own canonical or preview values.
- Injected titles, descriptions, metadata, and JSON-LD escape HTML and JSON control characters safely.
- Existing guideline content and identity geometry remain unchanged.
