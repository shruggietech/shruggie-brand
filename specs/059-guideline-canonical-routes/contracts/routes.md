# S059 Public Guideline Route Contract

## Canonical grammar

For brand slug `b` and visible topic label `L`, the canonical page URL path is `/{b}/guidelines/{slug(L)}/`. `slug(L)` lowercases ASCII words, joins them with one hyphen, and rejects empty or duplicate results. A label's semantic topic key does not change its URL. Current examples: `Overview` -> `/overview/`, `Logo` -> `/logo/`, `Assets` -> `/assets/`, `Expressions` -> `/expressions/`.

All canonical page links include a trailing slash. The static host and browser may normalize a request without it. Any query or fragment on a legacy link should survive navigation where the browser allows it.

## Compatibility map

| Former page path | Canonical destination |
| --- | --- |
| `/{b}/guidelines/` | `/{b}/guidelines/overview/` |
| `/{b}/guidelines/logos/` | `/{b}/guidelines/logo/` |
| `/{b}/downloads/` | `/{b}/guidelines/assets/` |

Each former path exports a static compatibility page with immediate browser navigation, a visible link, `noindex`, and a canonical reference to its destination. On GitHub Pages the response status is 200, since the host has no HTTP redirect rule. These pages are excluded from the canonical route JSON and sitemap.

## Unchanged paths

`/{b}/downloads/files/**`, public kit archives, the main `/docs/**` manual, and existing topic pages whose label slug already matches remain at their current paths. A topic absent from one brand has no canonical page or bridge.

## Publication invariants

Menus, breadcrumbs, pagination, homepage brand links, route descriptions, canonical/Open Graph/Twitter metadata, structured data, sitemap, robots references, and search inventory resolve to canonical pages. Validation rejects duplicate slug/path, redirect chain/loop, stale old page URL in canonical references, legacy page in sitemap, and missing export page or direct download file.
