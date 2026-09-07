# Data Model: Guidelines Reference Experience

## Asset Delivery

| Field | Rule |
| --- | --- |
| path | Existing generated file, normalized relative to kit root |
| family | `logo` or `icon` |
| semantic key | Stable visual role, variant, colourway, appearance, and source combination, with destination-only roles normalized |
| format | Measured file format |
| dimensions | Measured width and height where applicable |
| destination | Existing integration destination or logo use class |
| status | Generated or explicitly skipped |

## Asset Group

| Field | Rule |
| --- | --- |
| id | Stable unique identifier derived from semantic key |
| title | Human-readable role and appearance |
| representative | Vector master when useful, otherwise largest delivered raster |
| deliveries | Every matching path, format, size, destination, and alias |
| guidance | Concise role, background, transparency, and minimum-use guidance |

## Color Reference

| Field | Rule |
| --- | --- |
| token | Canonical generated token name |
| role | Identity, semantic, surface, chart, or text role |
| hex | Unchanged canonical sRGB value |
| rgb | Integer sRGB channels |
| hsl | CSS degrees and percentages |
| oklch | Fixed precision CSS value |
| lab | CIELAB D50 with explicit white point |
| print | Profile-required statement unless governed profile metadata exists |

## Publication Context

Portable source contains internal anchors and relative `data-kit-asset` links. Hosted preparation maps each declared asset link beneath `/<slug>/downloads/files/` and injects exactly one neutral `All brands` link to `/`. No other guide content changes.
