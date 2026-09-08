# Contract: Asset Preview Layout

## Purpose

Define one measurable presentation boundary for exact shipped assets on public guideline pages.

## Content Contract

- The preview URL is an exact delivery listed in the generated asset record.
- Asset-library cards and guideline logo examples share the same media-region structure.
- The presentation surface comes from generated light or dark appearance metadata.
- Metadata, delivery links, and summaries remain outside the media region.

## Layout Contract

- The outer media region has a stable block size and clips all descendant paint.
- The inner media region has positive dimensions after padding and centers its image in both axes.
- The image fills the inner region only as far as its intrinsic aspect ratio permits.
- The image canvas, baked background, and shadow remain inside the inner media region.
- The outer media region ends before the metadata divider, with no overlap.
- Wrapped titles, long metadata, asset shape, theme, and viewport width do not change these boundaries.

## Measurement Contract

- Image bounds remain within inner media bounds with a tolerance of one device pixel.
- Opposing horizontal and vertical margins differ by no more than one device pixel.
- The media region and metadata region do not intersect.
- Measurements cover all production brands at mobile, tablet, and desktop widths, both themes, and 200 percent zoom.
- Transparent, opaque, wide, tall, and square asset classes are represented.

## Prohibitions

- Do not change canonical or generated asset bytes to compensate for site layout.
- Do not apply per-brand or per-asset offsets.
- Do not crop visible or transparent clear space.
- Do not use CSS filters to synthesize a different delivery.
