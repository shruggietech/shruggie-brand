# Research: Documentation Contract Boundaries

## Decision 1: One governed documentation contract replaces site-only metadata

**Decision**: Add a versioned JSON documentation contract and schema under `skill/references/`. It owns manual page descriptions, topic coverage, navigation positions, source dispositions, route-kind dispositions, surface responsibilities, and shared-fact requirements.

**Rationale**: `scripts/prepare_site.py` currently hard-codes documentation descriptions and navigation while the Markdown sources live elsewhere. A single contract makes missing pages, duplicate positions, uncovered topics, and undocumented route changes fail before site generation.

**Alternatives considered**:

- Keep Python dictionaries as the authority. Rejected because they are site-specific and cannot travel in generated kits or be schema-validated independently.
- Put frontmatter in every reference Markdown file. Rejected because source and route dispositions, shared-fact requirements, and cross-surface ownership need one complete inventory.
- Create a new documentation repository. Rejected by the program architecture and unnecessary for compiler-owned documentation.

## Decision 2: One per-kit shared fact record drives hosted and bundled projections

**Decision**: Generate `enforcement/documentation-facts.json` from the validated brand, version policy, consumer contract, adapter manifests, verification contract, and documentation policy. Render `IMPLEMENTATION.md` from this record and embed the exact same record in `guidelines/portal.json` for hosted staging.

**Rationale**: Shared facts can be compared structurally without forcing hosted and offline prose to be identical. Brand-specific presentation stays in the portal, while exact implementation authority stays in the bundle.

**Alternatives considered**:

- Compare independently authored hosted and bundled prose. Rejected because wording differences are not a reliable drift signal.
- Make the hosted site read files directly from the repository. Rejected because constitution P5 requires site brand facts to come from verified generated kits.
- Put full system-manual prose in each kit. Rejected because it duplicates architecture authority and increases drift.

## Decision 3: Current hosted guidance and pinned bundled guidance have distinct version roles

**Decision**: Hosted child-brand guidance declares the exact current kit versions used by the site build. A delivered kit's `IMPLEMENTATION.md` and fact record remain authoritative for those pinned bytes after the site advances. S041 does not build public historical version routes.

**Rationale**: Consumers already receive deterministic recovery bytes and independently pinned version domains. A public historical archive would add release-retention and routing scope not required for offline correctness.

**Alternatives considered**:

- Redirect all consumers to `/docs/latest`. Rejected because it breaks exact-version authority.
- Publish a permanent public route for every past kit. Deferred because artifact retention and release publication policy belong to later release work.
- Omit versions from hosted guides. Rejected because readers could not tell which generated contract the guide describes.

## Decision 4: Preserve existing public routes and validate by route kind

**Decision**: Keep all current `/docs/`, `/{brand}/guidelines/`, topic, downloads, and integration routes. The documentation contract assigns a disposition to each relevant route kind, and site preparation expands that policy over every generated route to prove complete coverage.

**Rationale**: The existing routes are useful, indexed, and already validated. Route-kind expansion covers all eight brands without duplicating a fragile list of generated URLs.

**Alternatives considered**:

- Rename numbered documentation routes. Rejected because no user outcome justifies link churn.
- Create redirect-only cleaner slugs. Rejected because static-export redirect support and preservation work would add risk without fixing the authority problem.
- Record only source-file dispositions. Rejected because source coverage cannot prove published-route continuity.

## Decision 5: Graphics are server-rendered semantic HTML

**Decision**: Implement the documentation-ownership, operating-mode, and shared-improvement-loop graphics as server-rendered semantic sections using ordered lists, definition lists, links, headings, and CSS layout, each followed by a concise text equivalent.

**Rationale**: The graphics remain searchable, keyboard-readable, no-script compatible, responsive, zoom-safe, forced-colors friendly, and accessible without maintaining image exports or alternate SVG descriptions.

**Alternatives considered**:

- Mermaid diagrams. Rejected because these relationships are small enough for semantic HTML and would otherwise require a rendering dependency or client script.
- Static SVG files. Rejected because text equivalence, responsive reflow, and maintenance would be duplicated.
- Raster diagrams. Rejected because they are generated binary artifacts and scale poorly.

## Decision 6: Existing references remain useful and four pages fill the coverage gaps

**Decision**: Preserve all twelve existing manual source pages and add four focused pages for system architecture, interface implementation, verification/versioning, and agent integration/extensions. The contract maps the ten required topic groups across these pages.

**Rationale**: Existing material already covers variance, kit anatomy, discovery, identity, toolchain, shadcn, portability, continuity, and modes. Four pages close program gaps without rewriting or merging mature references.

**Alternatives considered**:

- Replace the manual with a new monolithic page. Rejected because it destroys useful deep links and creates an unreviewable prose change.
- Add ten new pages, one per work-order topic. Rejected because it duplicates current coverage and fragments navigation.
- Fold #193, #194, or #202 into documentation work. Rejected because their focused generator and presentation outcomes remain separately traceable.
