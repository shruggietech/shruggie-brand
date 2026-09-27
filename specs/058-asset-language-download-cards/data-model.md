# S058 Data Model

## Asset vocabulary entry

Fields: stable anchor, canonical term, short definition, examples, optional legacy aliases. Each alias maps to one canonical meaning; no contradictory term is reused for background and ink.

## Asset design identity

Fields: purpose, form, layout, color treatment, actual background, recommended surface, foreground ink, platform role when relevant, source variant when visually distinct. Not-applicable is explicit. For icons, actual alpha maps to clear or opaque background; light/dark appearance maps to intended surface. The tuple identifies one human-recognizable composition and use. When the generator reuses the same web artwork for favicon, touch, and installable roles, the semantic platform role is `web-icon`; individual delivery records retain their actual roles and destinations. Size and format are excluded.

## Asset delivery

Fields: source path, preferred public path, legacy aliases, SHA-256, format, dimensions, provenance, design identity. An alias must resolve to an existing approved or otherwise verified source file and have identical bytes. Old paths remain directly retrievable.

## Download card

Fields: stable design ID, title, summary/usage hint, search terms, surface choice, representative preview, ordered deliveries. Every delivery belongs to exactly one card; one card has exactly one design identity. The face uses a vector if supplied. Otherwise it uses the smallest raster with at least 320 pixels on its shorter side, falling back to the largest supplied raster. A preferred public path wins among visually equivalent candidates of the same size.

## Compatibility path map

Fields: schema version, brand, old path, preferred new path, digest, alias type. It covers every changed public path, with no collisions. Gate 2 approval data remains separate and unchanged.
