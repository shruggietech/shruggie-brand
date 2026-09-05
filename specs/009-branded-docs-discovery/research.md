# Research: Branded Documentation and Discovery Completion

## Fenced code rendering

**Decision**: Restore the default Fumadocs MDX `pre` binding, which wraps highlighted code in the library's `CodeBlock` and `Pre` components, rather than maintaining the current raw `pre` override.

**Rationale**: The installed framework already provides the cohesive panel and copy-button behavior required by #108. The current local override removes that wrapper and directly causes the defect. The official [Fumadocs code-block documentation](https://www.fumadocs.dev/docs/ui/components/codeblock) confirms the wrapper and copy-control contract.

**Alternatives considered**: Build a new local code component, keep the raw `pre` and add JavaScript, or install a generated copy of the upstream component. All would duplicate maintained framework behavior without adding project-specific value.

## Syntax and inline code styling

**Decision**: Style inline code only when it is not inside a fenced-code wrapper and remove the blanket `pre code span` color override.

**Rationale**: The current global rule erases the Shiki token palette and makes fenced lines look like isolated inline strips. Fumadocs already supplies theme-aware token colors, boundaries, and scrolling.

**Alternatives considered**: Define a complete project-owned syntax palette or keep one syntax color. A local syntax system adds needless maintenance, while one color fails #108.

## Selective semantic notices

**Decision**: Author portable GitHub-style NOTE, WARNING, and CAUTION blockquotes in authoritative references and convert only those explicit markers into Fumadocs `info`, `warn`, and `error` callouts.

**Rationale**: Explicit markers are readable outside the site, deterministic, Python 3.8-compatible, and cannot accidentally promote every normative sentence. The default Fumadocs MDX component set includes semantic callouts, and the official [Fumadocs components documentation](https://www.fumadocs.dev/docs/ui/components) supports the required variants.

**Alternatives considered**: Heuristic promotion based on words such as "never" or "must", an exact-text mapping hidden in code, or site-only MDX files. Heuristics create false positives, hidden mapping obscures author intent, and duplicate MDX would violate the single-source requirement.

## Documentation theme source

**Decision**: Map Fumadocs semantic variables to the generated ShruggieTech token and registry variables, then add narrowly scoped documentation component rules through an owned `docs-page` hook.

**Rationale**: `brands/shruggietech/brand.json` and generated CSS are the identity sources. Mapping semantic roles avoids the current mix of framework defaults and hand-authored near-match colors while retaining framework state behavior. Built output confirms that the previously assumed `.fd-docs-page` selector does not exist.

**Alternatives considered**: Copy the Fragcap CSS or create a separate docs palette. Fragcap is a density reference, not an identity source, and a parallel palette would drift.

## Compact sidebar identity

**Decision**: Publish theme-appropriate generated ShruggieTech lockups and render a responsive compact identity treatment using shipped geometry.

**Rationale**: The current white-only wide lockup becomes visually indistinguishable from text at 1.35rem and fails in light mode. Existing generated light and dark lockups preserve approved geometry without a new identity design.

**Alternatives considered**: Enlarge the one white lockup, crop it, or create new compact geometry. Enlargement consumes navigation space, cropping alters the mark, and new geometry requires owner identity approval.

## Canonical route contract

**Decision**: Generate one page descriptor per public HTML route with a normalized trailing-slash path and absolute canonical URL, then consume those descriptors everywhere.

**Rationale**: The current sitemap, Next.js metadata, copied guidelines, and tests assemble URLs separately. Next.js documents that `trailingSlash: true` with static export emits directory `index.html` pages, so an exact trailing-slash contract matches the deployment. See [Next.js trailingSlash](https://nextjs.org/docs/app/api-reference/config/next-config-js/trailingSlash) and [sitemap metadata](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap).

**Alternatives considered**: Patch only Fumadocs URLs in the sitemap or normalize independently in each consumer. Both preserve multiple sources of truth and cannot prove cross-surface equality.

## Structured-data identity graph

**Decision**: Reference the authoritative company using a minimal external Organization node with `@id`, `url`, and name based on `https://shruggie.tech`, define the brand subdomain as its own WebSite, and attach page-appropriate CollectionPage, WebPage, TechArticle, Brand, and BreadcrumbList nodes.

**Rationale**: This models the public content without copying unsupported company facts. Third-party showcase brands remain neutral because their Brand nodes do not assert ownership. Safe server rendering follows the official [Next.js JSON-LD guidance](https://nextjs.org/docs/app/guides/json-ld), including escaping `<` in serialized data. Types and relationships follow [Schema.org CollectionPage](https://schema.org/CollectionPage), [TechArticle](https://schema.org/TechArticle), [Brand](https://schema.org/Brand), and [BreadcrumbList](https://schema.org/BreadcrumbList).

**Alternatives considered**: Duplicate the main site's complete Organization facts, invent an organization fragment identifier, or omit publisher relationships. The first two risk contradiction, while omission loses the intended company relationship.

## Route-aware social previews

**Decision**: Generate one physical 1280 by 640 PNG per route during site preparation using local licensed fonts and canonical generated marks. Store only descriptor and generator source in Git.

**Rationale**: Physical files work uniformly for App Router pages and copied guideline HTML, remain static-export and offline safe, and can be decoded in CI. Next.js metadata supports absolute image URLs, declared sizes, types, and alt text as documented in [generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata).

**Alternatives considered**: One generic image with route-specific alt text, dynamic Next.js image routes, or committed image files. A generic image is not page-aware, dynamic routes complicate static guideline pages, and committed generated raster output violates repository policy.

## Visual regression evidence

**Decision**: Generate screenshots in ignored `site/test-results/visual/`, manually inspect them during the slice, and enforce stable visual intent through computed-style and geometry assertions.

**Rationale**: Issues #108 and #109 require desktop and mobile visual evidence, while the constitution prohibits committed generated raster exports. Ignored screenshots provide current-run evidence without turning Git into an artifact store.

**Alternatives considered**: Commit golden screenshots or omit screenshots. Goldens violate source boundaries, while omission leaves the issue acceptance criteria unproven.

## Review and publication protocol

**Decision**: Treat PR publication as review round one, process every signal and thread, then request at most one explicit `@Codex review` round after any round-one corrections. Halt only when latest-head CI is green and all review threads are resolved.

**Rationale**: This is the explicit user authorization for S009 and prevents recursive review triggering.

**Alternatives considered**: Stop before push under the generic autopilot default or request reviews until no new findings arrive. The user explicitly overrides the first and prohibits the second.
