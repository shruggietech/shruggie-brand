# S059 Research and Decisions

## Existing route flow

`skill/templates/gen_guidelines.py` emits portal topics; `scripts/prepare_site.py` validates them and constructs route records; the Next.js site consumes generated portal and route JSON. Three topic paths currently depart from the visible labels: Overview is the guidelines root, Logo uses the semantic key `logos`, and Assets is under `/downloads/`. The remaining active topic labels match their final path segments. The optional Expressions topic appears for I Heart PR Tours only.

## Decision 1: one label-derived grammar

**Decision**: Use `/<brand>/guidelines/<slug(label)>/` for all dedicated menu entries, while keeping the semantic `topic.key` unchanged.
**Rationale**: A single explicit rule handles current and future topics without key aliases or per-brand special cases. Content selection can retain stable semantic keys.
**Alternatives considered**: Rename the `logos` semantic key throughout the generator, which would conflate content identifiers with navigation; keep Overview at the root, which fails issue #285's predictable segment requirement.

## Decision 2: static legacy bridges

**Decision**: Publish `noindex` canonical bridge pages for the three changed page paths per brand, with immediate navigation and an accessible fallback link. Omit bridges from the route inventory and sitemap.
**Rationale**: `site/next.config.mjs` uses static export and GitHub Pages publishes `site/out`. That setup does not run Next.js redirect handlers or provide repository-controlled HTTP redirect rules. The bridge is the available self-contained compatibility mechanism.
**Alternatives considered**: Next.js `redirects()` requires a server and is unsupported for static export. A real HTTP 301/308 would require a hosting change and is outside S059. Duplicating old content would create indexable competing pages.

## Decision 3: keep file downloads independent

**Decision**: Migrate the Assets page to `/guidelines/assets/` and retain the `/downloads/files/` subtree and archive links byte-for-byte.
**Rationale**: Navigation pages and direct file URLs are separate contracts. S058 explicitly deferred only the page-route migration to #285.
**Alternatives considered**: Moving the whole downloads tree would break public asset links without providing user value.

## Decision 4: consume generated routes throughout publication

**Decision**: Generate canonical topic routes once from portal topics, use them in navigation and metadata, and audit all publication outputs for stale page links.
**Rationale**: Current `site/lib/guidelines.ts` and `scripts/prepare_site.py` both contain hardcoded special cases, a source of divergence. Route records already feed canonical/Open Graph/structured data/sitemap.
**Alternatives considered**: Adding redirects only would leave menus and previews inconsistent.

## Evidence sources

- Issue #285 defines the path, migration, metadata, and acceptance boundary.
- `skill/templates/gen_guidelines.py` defines generated topic labels and current path exceptions.
- `scripts/prepare_site.py` validates topic paths and builds route records.
- `site/next.config.mjs` and `.github/workflows/build.yml` establish static export to GitHub Pages.
- `site/lib/guidelines.ts`, `site/app/sitemap.ts`, and `site/lib/metadata.ts` show navigation and publication consumers.
