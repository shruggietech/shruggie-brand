# Data Model: Integration Preview Visibility

## Delivery

Fields: `path`, `family`, `platform`, `kind`, `variant`, `colourway`, `role`, `appearance`, `source_variant`, `format`, `width`, `height`, optional `embedded_sizes`, and `destination`.

Validation: The path must exist inside the generated kit inventory. PNG and SVG dimensions must match the file. Container sizes must be derived from the exact payload. Manifest text is escaped before HTML emission. Delivery bytes remain read-only.

## Delivery Group

Fields: stable group `id`, normalized grouping `key`, ordered `deliveries`, and a preferred representative.

Relationships: A group contains one or more deliveries with matching family, platform, kind, variant, colorway, normalized role, appearance, and source variant. A group can be visual-only, nonvisual-only, or mixed.

Validation: Every input delivery appears in exactly one group and every delivery link appears exactly once in portable output. Mixed groups retain a visual representative when one exists.

## Preview Presentation

Fields: `kind` (`visual` or `nonvisual`), `preview` delivery when visual, `surface` (`light`, `dark`, or `nonvisual`), `basis` (`measured`, `declared`, or `nonvisual`), optional measured contrast score, surface label, resource label, and detail label.

State transitions: If measurable pixels exist, significant-pixel coverage selects the stronger surface and median contrast breaks ties, regardless of generic or target-oriented appearance metadata. Declared appearance is used only without measurable output. A group with no visual delivery transitions directly to a nonvisual presentation. Fully transparent visual input transitions to a generation error. An approved asset intrinsically below 3:1 on both supported wells retains the stronger well and its measured score without asset mutation; affected-guide acceptance rejects such an outcome.

Validation: Visual presentation requires an image payload, exact source-byte embedding, and a finite contrast score when measured. The affected guide additionally requires a score of at least 3. Nonvisual presentation forbids an image payload and requires format-aware visible copy.

## Visible Output Sample

Fields: sampled dimensions, maximum alpha, meaningful-alpha threshold, per-well significant-pixel coverage, per-well median contrast, and selected well.

Validation: Sampling preserves aspect ratio and is bounded by the 180 CSS pixel preview size. Fully transparent samples are invalid. Identical bytes produce identical values.

## Browser Observation

Fields: viewport width, zoom, preview kind, computed background and foreground, image load and bounds, declared contrast, text contrast, overflow, axe violations, source route, and direct-file mode.

Validation: Required observations cover 1280 pixels, 360 pixels, 200 percent zoom, both visual wells, nonvisual wells, hosted copy, and the direct portable file.
