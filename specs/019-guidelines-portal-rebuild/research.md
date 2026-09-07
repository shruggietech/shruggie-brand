# Research: Hosted Guidelines Portal Rebuild

## Decision 1: Separate the hosted portal from the portable guide

**Decision**: Keep a concise self-contained HTML guide as a downloadable offline artifact, but make a structured generated payload the authoritative input for hosted topic pages.

**Rationale**: S017 optimized a single portable document and then reused it as the hosted experience. Once complete color and platform inventories were added, that coupling forced navigation, disclosure, and asset storage details into one page. A sibling structured payload retains one source of truth while allowing the site to own its information architecture as required by the constitution.

**Alternatives considered**: Continue styling the single HTML document, split the HTML using publication-time selectors, or hand-author brand pages. Styling cannot solve navigation scale, HTML slicing binds publication to presentation markup, and hand-authored brand facts violate P5.

## Decision 2: Reuse the existing documentation framework as a brand-neutral shell

**Decision**: Generate a guideline MDX topic tree and use the installed Fumadocs layout and page primitives with per-brand navigation options and no ShruggieTech marketing links.

**Rationale**: The installed framework already provides static page trees, persistent desktop navigation, mobile sidebar behavior, table-of-contents support, focus management, and direct URLs. A per-brand configuration can retain those capabilities while making the dedicated brand primary.

**Alternatives considered**: Add a second documentation dependency, build an unrelated custom navigation stack, or force the general ShruggieTech docs tree into brand portals. A second stack adds weight, a custom stack duplicates solved accessibility behavior, and the general docs tree violates the brand-neutral boundary.

## Decision 3: Generate one typed data registry and direct page trees

**Decision**: Publication writes one generated JSON registry for topic prose, structured colors, assets, instructions, and navigation metadata. The static route builds the Fumadocs page tree directly and source-controlled components render safe structured content by brand and topic key.

**Rationale**: Inspection of the installed Fumadocs API confirmed that page trees accept direct typed records, so generated MDX wrappers would duplicate routing metadata without improving navigation. Converting authoritative instruction Markdown to a constrained safe block model at publication retains headings, links, lists, and code while structured components implement interaction and measured layout.

**Alternatives considered**: Generate MDX wrappers, compile arbitrary HTML from the generator, parse Markdown at browser runtime, or emit structured data into attributes. Those choices add redundant build artifacts, weaken validation, require runtime parsing, or create unmaintainable generated pages.

## Decision 4: Use independent color rows with in-row details

**Decision**: Render colors as a semantic list of independent compact rows. Each row has a fixed resting header and its own full-width detail region inside the row, so expansion affects only that row and entries are never coupled by a shared CSS grid track.

**Rationale**: The regression comes from `details` elements inside equal-row grid cards. A semantic list matches the data, avoids layout-table misuse, works on mobile, and guarantees that opening one item cannot resize a neighbor.

**Alternatives considered**: A dense table, modal dialogs, popovers, or fixed-height cards. Tables become horizontally fragile with many formats, dialogs interrupt comparison, popovers are poor no-script containers, and fixed-height cards either clip or waste space.

## Decision 5: Treat assets as representative designs with delivery details

**Decision**: Derive one representative record for each distinct visual design, group records into task-oriented families, and attach every size, format, alias, destination, and hash as deliveries. Present nonvisual resources as document rows and integration Markdown as topic content.

**Rationale**: The manifest remains exhaustive while the visitor sees a bounded library organized by purpose. Grouping is deterministic and auditable because every delivery maps to exactly one representative or nonvisual resource.

**Alternatives considered**: One card per file, hide low-level deliveries, or manually curate featured assets. One card per file caused the regression, hiding files violates completeness, and manual curation drifts from manifests.

## Decision 6: Progressive enhancement preserves the complete collection

**Decision**: Server-render all asset-family sections and direct downloads. A small client component adds search, multi-select filters, URL query state, and live result announcements without fetching data or hiding content in the source document.

**Rationale**: This satisfies static export, runtime network independence, useful filtering, deep links, keyboard access, and a complete no-script experience.

**Alternatives considered**: Server search endpoints, an external search service, or a fully client-rendered library. All conflict with static runtime constraints or no-script completeness.

## Decision 7: Fix the heading contract at the component boundary

**Decision**: Give `.brand-hero h1` a smaller responsive scale, overflow-safe width behavior, balanced wrapping, and an earlier one-column breakpoint proven against the longest production name.

**Rationale**: The global marketing hero scale was designed for a wide single-column statement, not a constrained brand-name column. The fix belongs to the brand hero, not the brand name or logo.

**Alternatives considered**: Insert manual breaks, abbreviate names, shrink only ShruggieTech, or change identity geometry. Those choices encode content exceptions or alter identity rather than repairing layout.
