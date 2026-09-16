# Research: Embed Specimen Logo

## Exact-byte embedding format

**Decision**: Embed governed image components as base64 data URIs using a small explicit source-extension to media-type mapping.

**Rationale**: Base64 transports SVG and raster bytes without text decoding, namespace rewriting, escaping ambiguity, or platform newline conversion. It preserves the authoritative byte payload and matches established repository patterns for source-faithful logo wrappers.

**Alternatives considered**: Percent-encoded data URIs, inlining the source SVG element tree, and copying a neighboring asset into the specimen directory. Percent encoding adds encoding ambiguity, inlining reparses and rewrites authoritative SVG structure, and neighboring assets leave the specimen non-portable.

## Governed source resolution

**Decision**: Resolve each image path under the staged kit root, reject traversal or absolute-path escape, require a regular file, and fail closed on an unsupported extension.

**Rationale**: The brand contract normally validates governed paths earlier, but the specimen generator should not turn an unchecked string into filesystem access or a published URI. A contained resolver makes the embedding operation safe when invoked directly in tests or by operators.

**Alternatives considered**: Trust prior validation exclusively or accept any MIME value guessed by the host. Both make direct generator invocation less safe and can create platform-dependent output.

## SVG reference contract

**Decision**: Preserve both `href` and `xlink:href` for renderer compatibility and assign the identical embedded value to each. Verification accepts only `data:` or internal `#` references anywhere in a specimen.

**Rationale**: Existing output deliberately emits both forms. Keeping them avoids renderer regressions while the strict reference allowlist rules out every relative, filesystem, and network dependency.

**Alternatives considered**: Remove `xlink:href` or validate only image nodes. Removing the compatibility attribute can affect older SVG consumers, while scanning only image nodes could miss a future external dependency elsewhere in the specimen.

## Rendered mark evidence

**Decision**: Give the header mark group a stable internal identifier, rasterize the exact generated specimen at its native viewBox width, crop that declared group region, and require a meaningful count of pixels that differ from the specimen background.

**Rationale**: HTTP status, XML parsing, and a non-empty data URI do not prove visible artwork. Measuring the mark region avoids false positives from the specimen's outlined text elsewhere on the page.

**Alternatives considered**: Whole-page non-background pixels, screenshot snapshots, and SVG byte snapshots. Whole-page checks pass even when the mark is missing, screenshots are brittle, and byte snapshots conflict with measured-behavior verification.

## Browser and offline coverage

**Decision**: Use Playwright to navigate directly to the exact site-exported SVG over the local HTTP server and through a local `file:` URL, inspect the live SVG reference contract, and measure a screenshot of the mark group.

**Rationale**: These two paths reproduce the hosted and portable-local user journeys and exercise Chromium's SVG image resolution rather than only the repository rasterizer.

**Alternatives considered**: Fetch-only route checks or embedding the SVG in an HTML test page. Fetching repeats the status-only blind spot, while a wrapper page is not the published direct-navigation behavior.

## Publication equivalence

**Decision**: Rely on the existing deterministic brand-archive certification for source-to-ZIP equality, add an explicit source-to-hosted-copy byte assertion, and browser-test the hosted copy.

**Rationale**: The archive writer already verifies canonical kit entries. The missing link is a focused assertion that the site copy remains identical to the verified source specimen before browser rendering.

**Alternatives considered**: Duplicate ZIP parsing in the browser verifier or regenerate a specimen inside site code. Duplicate parsing adds unnecessary code, and regeneration would violate the site's generated-kit consumption boundary.

## Specimen lockup selection

**Decision**: Prefer the approved input named by `supplied_lockup_input_ids.horizontal.color` for the specimen header, validate that it is an approved lockup with unchanged-byte embedding permission, and otherwise fall back to `logo.paths.full` or `logo.paths.reduced`.

**Rationale**: The owner requested the wider stacked lockup after reviewing the first repair. I Heart PR Tours already governs `horizontal-dark-lockup` as an authoritative approved input, so the generator can honor that request without adding a duplicate brand setting or changing source bytes. Native source dimensions are centered within the existing logo grid and reduced only when necessary, preserving aspect ratio.

**Alternatives considered**: Change `logo.paths.full`, add a specimen-only field to `brand.json`, hard-code the brand slug, or edit the vertical artwork. Changing the canonical full path would affect unrelated outputs, a new field would duplicate an existing governed declaration and invalidate the source inventory, a slug branch would bypass the shared contract, and editing artwork would violate identity preservation.

## Security and tenancy applicability

**Decision**: Cover contained file resolution, fail-closed media types, reference allowlisting, and publication-path equivalence. Record authentication, private data, and multi-tenancy as not applicable.

**Rationale**: S034 processes local governed source and publishes static output. The relevant safety risks are path escape and external dependency injection, not user identity or tenant separation.

**Alternatives considered**: Synthetic authentication or tenancy tests. They would test nonexistent functionality and obscure the actual file and URI trust boundaries.
