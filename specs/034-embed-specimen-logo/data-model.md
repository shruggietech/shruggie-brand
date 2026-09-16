# Data Model: Embed Specimen Logo

## Governed image component

| Field | Meaning | Validation |
| --- | --- | --- |
| `element` | Declares an image-backed logo component | Exact value `image` selects byte embedding |
| `source` | Brand-relative governed artwork path | Must remain within the staged kit, exist as a file, and use a supported format |
| `role` | Existing semantic color or identity role | Preserved; no recoloring is applied to embedded artwork |
| `x`, `y` | Component position in logo-grid units | Canonical components preserve their values; a preferred lockup is centered from its native dimensions |
| `width`, `height` | Component dimensions in logo-grid units | Canonical components preserve their values; a preferred lockup preserves native proportions and scales down only to fit |
| `preserveAspectRatio` | SVG presentation behavior | Remains `xMidYMid meet` |

## Embedded image payload

| Field | Meaning | Validation |
| --- | --- | --- |
| Media type | Declares the source encoding | Derived from an explicit supported extension map |
| Transfer encoding | Transports arbitrary bytes | Exact value `base64` |
| Encoded bytes | Self-contained authoritative source | Strict base64 that decodes byte-for-byte to the governed file |
| `href` | Modern SVG image reference | Equals the complete data URI |
| `xlink:href` | Compatibility SVG image reference | Equals `href` exactly |

## Specimen lockup selection

| Field | Meaning | Validation |
| --- | --- | --- |
| Preferred input ID | Existing `supplied_lockup_input_ids.horizontal.color` value | Optional; when present, resolves exactly one authoritative input |
| Input role and usage | Approval boundary for the preferred artwork | Must be an approved `lockup` input |
| Transform permissions | Permitted handling of authoritative bytes | Must include `embed-unchanged` and `resize` |
| Source dimensions | Native SVG viewBox or raster dimensions | Positive dimensions; preserve their aspect ratio |
| Grid placement | Centered rectangle within `logo.grid` | Scale down only when either native dimension exceeds the grid |
| Fallback | Existing canonical specimen component list | Use `logo.paths.full`, then `logo.paths.reduced`, when no preferred input is declared |

## Specimen mark region

| Field | Meaning | Validation |
| --- | --- | --- |
| Stable identifier | Locates the header mark without depending on document order | Unique internal identifier on the generated mark group |
| Translation | Places the mark in specimen coordinates | Existing header `x` and `y` values remain unchanged |
| Scale | Maps logo-grid units into header height | Existing `height / grid` relationship remains unchanged |
| Raster bounds | Pixel-space crop used by verifiers | Derived from the rendered group bounding box or declared header region |
| Visible pixels | Pixels that differ materially from the specimen background | Must exceed the minimum meaningful-ink threshold |

## Portable specimen

| Property | Contract |
| --- | --- |
| References | Every `href` and `xlink:href` begins with `data:` or `#` |
| Source identity | Every governed image payload decodes to its exact source bytes |
| Geometry | Image attributes and mark-group transform agree with governed placement |
| Rendering | The declared mark region contains measurable visible artwork |
| Typography | Existing outlined glyph paths remain unchanged in behavior |

## Publication copy pair

| Copy | Origin | Equivalence rule |
| --- | --- | --- |
| Kit specimen | Verified `dist/<slug>/specimens/<slug>-type-specimen.svg` | Canonical source for archive and site publication |
| Archive specimen | Deterministic kit ZIP entry | Certified byte-identical to the kit specimen by the existing archive verifier |
| Hosted specimen | Site download-file copy | Must be byte-identical to the kit specimen before site export |

## State Transitions

1. The brand contract selects an approved supplied horizontal color lockup when declared, otherwise the canonical full/reduced component list.
2. The selected governed image component is validated and resolved inside the staged kit.
3. Its bytes and media type become one embedded payload used by both SVG reference attributes.
4. The completed specimen is structurally verified for portable references and source equivalence.
5. A capable tier rasterizes the exact specimen and verifies visible pixels in the mark region.
6. Archive certification and site preparation preserve the specimen bytes.
7. Browser verification opens the hosted and offline copies and rechecks references and visible mark pixels.
