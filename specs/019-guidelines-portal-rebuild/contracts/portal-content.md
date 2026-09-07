# Portal Content Contract

`guidelines/portal.json` is generated beside the portable guide for each verified kit. It is presentation-independent and contains every fact required by hosted topic pages.

## Required top-level fields

- `schema_version`: fixed contract version.
- `brand`: slug, title, descriptor, affiliation copy, and theme token references copied from the verified brand record.
- `topics`: ordered topic descriptors with unique URL-safe keys.
- `palettes`: dark and light color reference entries derived from canonical tokens.
- `asset_families`: ordered task-oriented families containing representative designs and their complete deliveries.
- `resources`: nonvisual documents, manifests, containers, and instruction sources.
- `instructions`: Markdown content and source path keyed by platform or topic.
- `portable_guide`: relative path to the self-contained offline HTML file.

## Integrity rules

1. Every manifest and provenance delivery appears exactly once as a representative delivery or nonvisual resource.
2. Every referenced path exists below the kit and resolves without traversal, query, fragment, or backslash components.
3. Each representative preview points to an SVG or PNG delivery in its own delivery list.
4. Size-only variants and aliases do not create duplicate representative designs.
5. Nonvisual resources never declare a visual preview.
6. Color representations derive from one canonical value and preserve precision rules.
7. Markdown instructions preserve the authoritative source text and identify their raw download.
8. Unknown schema versions, duplicate identifiers, missing files, invalid aliases, or incomplete inventory fail publication.

## Hosted projection

`scripts/prepare_site.py` validates each payload, rewrites only validated kit-relative downloads, emits one generated registry with constrained instruction blocks, and records every topic in the canonical route registry. Site components may change presentation but may not alter brand facts or inventory.
