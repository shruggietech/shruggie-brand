# Research: Guidelines Reference Experience

## Decision 1: Generated manifests are the only inventory authority

Use `logos/provenance.json` and `icons/manifest.json`. Their records already carry role, variant, appearance, dimensions, format, destination, and source lineage. Filename-only inference or a second hand-authored catalog would drift.

## Decision 2: Group by semantic design key, then retain delivery records

Logo groups use kind, variant, and colourway; icon groups use platform, role, appearance, and source variant. Dimensions do not create a new group. Compatibility aliases attach to their target group. The largest raster or vector master becomes the representative.

## Decision 3: Embed previews but link to delivery files

The portable guide stays self-contained for viewing, so representative images are embedded. Download links are relative kit paths and carry `data-kit-asset`. The site publisher alone rewrites them to the copied `downloads/files` tree.

## Decision 4: Use ColorAide for governed conversions

The repository already depends on ColorAide. Convert canonical sRGB HEX into integer RGB, CSS HSL, OKLCH, and Lab D50 with fixed precision. CMYK remains unavailable without a governed output profile.

## Decision 5: Progressive enhancement stays inline and local

Contents anchors and a footer top link work without script. JavaScript upgrades copy buttons and a fixed back-to-top control, keeps hidden controls unfocusable, updates an aria-live region only after clipboard resolution, and honors reduced-motion preference.

## Decision 6: Scoped theme wells use complete token maps

Each well receives the entire generated dark or light custom-property set. This prevents a light specimen nested under the dark document from inheriting invalid foreground, border, chart, or focus values.

## Rejected Alternatives

- A client-rendered catalog would weaken offline behavior and semantic fallback.
- A new catalog schema would duplicate complete existing manifests.
- Arithmetic CMYK would misrepresent process-dependent print color.
- A site shell around each guide would violate brand neutrality and portable parity.
