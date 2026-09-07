# Data Model: Hosted Guidelines Portal Rebuild

## Portal Record

One verified hosted-guide payload per production brand.

Fields: schema version, brand slug, title, descriptor, affiliation copy, theme tokens, ordered topics, color palettes, asset families, nonvisual resources, integration instructions, portable-guide path, and source manifest references.

Rules: slug matches the kit directory; all topic keys are unique and URL-safe; every referenced delivery exists below the verified kit; no site-authored brand value may override the payload.

## Guideline Topic

Fields: key, title, short description, order, content kind, optional section outline, and optional related topic keys.

Relationships: belongs to one Portal Record; may reference one structured renderer such as color or assets; may contain authoritative generated Markdown.

Rules: overview is always present; optional topics are emitted only when authoritative content exists; stable keys determine URLs and navigation order.

## Color Reference Entry

Fields: palette, human role, canonical token, canonical HEX, swatch value, RGB, HSL, OKLCH, Lab D50, print guidance, and ordered aliases.

Relationships: belongs to one palette and one Portal Record.

Rules: all representations derive from the canonical value; the canonical token and aliases are distinct; values remain selectable without clipboard support.

## Asset Family

Fields: key, human title, purpose summary, order, representative assets, and document resources.

Relationships: belongs to one Portal Record; contains zero or more Representative Assets and Nonvisual Resources.

Rules: family assignment is determined by semantic role and platform rather than path prefix alone; empty optional families are omitted.

## Representative Asset

Fields: stable id, title, role, platform, appearance, surface, preview delivery, usage summary, format summary, variant summary, searchable terms, and deliveries.

Relationships: belongs to exactly one Asset Family; owns one or more Asset Deliveries.

Rules: exactly one representative exists per genuinely distinct visual design; preview format is SVG or PNG; preview dimensions and aspect ratio are measured; delivery count does not affect summary height.

## Asset Delivery

Fields: path, format, role, platform, dimensions or embedded sizes, destination, appearance, source variant, alias target, and optional SHA-256.

Relationships: maps to exactly one Representative Asset or Nonvisual Resource.

Rules: paths are safe relative paths below the kit; paths are unique; aliases resolve to catalogued targets; every file exists; hosted download paths are derived rather than accepted as input.

## Nonvisual Resource

Fields: stable id, human title, resource kind, format, purpose summary, path, destination, and optional rendered-instruction key.

Rules: no image-preview field is emitted; Markdown instructions have both rendered content and an optional raw download.

## Filter State

Fields: search query, selected family, platform, appearance, role, and format.

Rules: values come from the generated facet inventory; URL query parameters are optional progressive enhancement; an empty result exposes a count of zero and reset action.
