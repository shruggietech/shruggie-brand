# Data Model: Asset Delivery Fidelity

## Square Knockout Mask

Represents the monochrome square enclosure that retains the approved interior mark through negative space.

| Field | Meaning | Validation |
| --- | --- | --- |
| `id` | Unique mask identifier within one SVG | Non-empty and referenced exactly once by its enclosure |
| `coordinate_mode` | Coordinate interpretation for the mask region and content | Local user-space coordinates |
| `x`, `y` | Mask-region origin | Equal to the square mark canvas origin |
| `width`, `height` | Mask-region extent | Equal to the complete square mark canvas |
| `frame_bounds` | Rounded-square target bounds | Fully contained inside the mask region |
| `knockout_geometry` | Existing approved path set used as negative space | Byte-identical path strings from the brand contract |
| `colourway` | Black or white output treatment | Governed monochrome values only |

## Monochrome Lockup Delivery

Represents one full lockup and its derived files.

| Field | Meaning | Validation |
| --- | --- | --- |
| `kind` | Horizontal or stacked full lockup | Never reduced or wordmark-only |
| `colourway` | Black or white | Exactly one governed monochrome treatment |
| `svg_master` | Generated vector delivery | Complete explicit mask region, full mark, and complete wordmark |
| `raster_deliveries` | PNG sizes derived from the master | Pixel-equivalent to the verified SVG at each declared dimension |
| `mark_region` | Lockup region occupied by the square mark | Unclipped and proportionate to the declared lockup geometry |
| `wordmark_region` | Lockup region occupied by the wordmark | Complete, separate from the mark, and inside the canvas |
| `provenance` | Source variant and transformation lineage | Full source variant plus governed resize and lockup placement |

## Asset Preview Record

Represents the exact generated asset selected for a public preview.

| Field | Meaning | Validation |
| --- | --- | --- |
| `asset_id` | Stable generated catalog identity | Unique within the brand portal |
| `preview_url` | Exact shipped visual delivery | Present among the asset's delivery records |
| `surface` | Light or dark presentation well | Derived from generated appearance metadata |
| `shape` | Wide, tall, square, transparent, or opaque canvas behavior | Preserved without crop or stretch |
| `deliveries` | Every downloadable file represented by the preview | Complete and unique |

## Preview Media Region

Represents the shared bounded presentation area above card metadata.

| Field | Meaning | Validation |
| --- | --- | --- |
| `outer_bounds` | Fixed preview area including its presentation surface | Does not overlap the metadata region |
| `inner_bounds` | Centering and containment region for media | Positive width and height at every supported viewport |
| `image_bounds` | Rendered canvas of the exact preview asset | Fully contained within inner bounds |
| `horizontal_margin` | Space left and right of the image | Difference no greater than one device pixel |
| `vertical_margin` | Space above and below the image | Difference no greater than one device pixel |
| `paint_containment` | Clipping boundary for backgrounds and shadows | No paint crosses the divider |

## Relationships

- One square knockout mask appears in one generated monochrome mark and may be nested into multiple lockup deliveries.
- One SVG lockup master produces one or more raster deliveries.
- One asset preview record selects exactly one of its shipped visual deliveries.
- One asset card owns one preview media region followed by one metadata region.

## State Transitions

1. Canonical full paths remain frozen.
2. Generator composes the explicit square-knockout mask.
3. Structural verification accepts or rejects the SVG.
4. Raster generation derives declared sizes from the accepted SVG.
5. Rendered verification accepts or rejects SVG and PNG behavior.
6. Portal generation selects an exact verified delivery and declared surface.
7. Browser verification accepts or rejects preview containment before publication.
