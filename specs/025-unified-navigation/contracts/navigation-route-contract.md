# Navigation and Route Contract

## Brand hierarchy

Every public brand exposes this exact ordered tree:

```text
Overview     -> /<slug>/guidelines/
Voice        -> /<slug>/guidelines/voice/
Identity
  Logo       -> /<slug>/guidelines/logos/
  Color      -> /<slug>/guidelines/color/
  Typography -> /<slug>/guidelines/typography/
Components   -> /<slug>/guidelines/components/
Assets       -> /<slug>/downloads/
Integration  -> /<slug>/guidelines/integration/
```

`/<slug>/` and `/<slug>/guidelines/assets/` are not content routes, navigation targets, canonical URLs, sitemap entries, social-preview contracts, breadcrumbs, search records, or structured-data entities.

## Documentation hierarchy

Existing page titles and URLs remain unchanged beneath this exact ordered tree:

```text
Overview       -> /docs/
Foundation
  Contract     -> /docs/00-variance-contract/
  Kit          -> /docs/02-kit-anatomy/
Discovery
  Interview    -> /docs/03-interview/
Identity
  Logo         -> /docs/06-logo-protocol/
  Glyphs       -> /docs/08-glyph-construction/
  Voice        -> /docs/07-voice/
Implementation
  Toolchain    -> /docs/04-toolchain/
  shadcn       -> /docs/05-shadcn-binding/
  Portability  -> /docs/09-portability/
```

## Semantic behavior

- Grouped entries are semantic tree folders/disclosures, not fabricated pages.
- The current page exposes current-page state.
- A current child keeps its parent group visibly identifiable and expanded.
- Desktop and mobile receive the same complete tree.
- Server-rendered anchors remain available without JavaScript.
- Focus indicators, target sizes, narrow layouts, wide touch-only layouts, and 200% zoom meet WCAG 2.1 AA requirements.

## Content preservation

- Overview retains foundations, promises, and boundaries.
- Voice retains principle, qualities, vocabulary, and personality guidance.
- Identity children retain all logo, palette, and typography content.
- Components retains all domain component examples.
- Assets combines the direct resource hub with every generated asset family and resource.
- Integration retains every platform instruction and source download.
- Documentation content, titles, descriptions, and slugs remain byte-equivalent after public-Markdown derivation.

## Registry preservation

- The registry catalog remains available and schema-valid.
- Every advertised item resolves to a sibling JSON endpoint and declares the expected item type.
- Theme CSS values remain only in the theme item, not duplicated into the catalog.

## Failure contract

Site preparation fails before publication for unsafe or duplicate routes, duplicate or missing navigation assignments, destinations without route records, content without a destination, or catalogs with missing, duplicated, malformed, or type-inconsistent items.
