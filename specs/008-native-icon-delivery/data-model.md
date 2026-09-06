# Data Model: Native Icon Delivery and Favicon Integrity

## IconProfile

The brand-level rules used to compose every icon derivative.

| Field | Type | Rules |
|---|---|---|
| `foreground_full` | canonical mark reference | Required; preserves approved full geometry |
| `foreground_reduced` | canonical mark reference | Optional; falls back to full geometry |
| `reduced_below_px` | positive integer | Existing browser and small-container source threshold |
| `background` | six-digit hex color | Optional brand override; defaults to canonical base surface |
| `safe_zone_ratio` | decimal | Generator-owned platform rule, not identity geometry |

## IconArtifact

One file declared by the authoritative icon manifest.

| Field | Type | Rules |
|---|---|---|
| `path` | normalized relative path | Required; forward slashes; no absolute paths, traversal, or duplicates |
| `platform` | enum | `web`, `android`, `apple-ios`, `apple-macos`, or `windows` |
| `role` | non-empty string | Stable role such as `favicon`, `adaptive-foreground`, `app-store`, or `target-size` |
| `format` | enum | `svg`, `png`, `ico`, `icns`, `json`, `xml`, or `markdown` |
| `width` | positive integer or null | Required for raster images and image container entries |
| `height` | positive integer or null | Required for raster images and image container entries |
| `appearance` | enum or null | `default`, `dark`, `tinted`, `light-unplated`, or `dark-unplated` where applicable |
| `alpha` | enum or null | `opaque`, `transparent`, or `either` for pixel-bearing images |
| `source_variant` | enum or null | `full`, `reduced`, or `metadata` |
| `destination` | non-empty string | Human-readable project placement guidance |

## PlatformSuite

A navigable platform delivery rooted below `icons/`.

| Field | Type | Rules |
|---|---|---|
| `id` | enum | One of the five platform identifiers |
| `root` | relative directory | Unique and present |
| `readme` | relative path | Required and inside the suite root |
| `manifest` | relative path | Required when the platform has no native single metadata file |
| `artifacts` | list of IconArtifact paths | Non-empty for raster-capable production output |
| `status` | enum | `generated` or explicit `skipped` |
| `reason` | string or null | Required only for `skipped` |

## IconManifest

The authoritative index at `icons/manifest.json`.

| Field | Type | Rules |
|---|---|---|
| `schema_version` | semantic version string | Starts at `1.0.0` |
| `brand` | slug | Must match `brand.json` |
| `profile` | IconProfile summary | Records effective background and reduced threshold |
| `suites` | list of PlatformSuite | Exactly five unique platform entries |
| `artifacts` | list of IconArtifact | Exact agreement with generated files excluding platform README files if explicitly declared as documentation |
| `aliases` | map of relative paths | Maps compatibility `favicons/` paths to authoritative `icons/web/` paths |

An artifact may use the non-suite platform value `domain` when it is a byte-preserved source-owned product interface symbol relocated under `icons/domain/`. These records participate in exact inventory validation but do not change the required five application platform suites.
| `capability` | object | Records tier and required skips |

## Native Metadata

### Android

- Adaptive icon XML references one background, foreground, and monochrome resource.
- Color XML declares the configured background.
- Density directories map mdpi, hdpi, xhdpi, xxhdpi, and xxxhdpi to 48, 72, 96, 144, and 192 pixels.

### Apple mobile

- `Contents.json` identifies a universal iOS 1024-pixel default image and dark and tinted luminosity appearances.
- All filenames resolve inside the application-icon set.

### macOS

- `Contents.json` maps 16, 32, 128, 256, and 512 point roles to 1x and 2x representations.
- `.iconset` and `.icns` contain the same required pixel representations.

### Windows

- The manifest fragment references base square-logo and store-logo names.
- Scale and target-size qualifiers map to exact pixel dimensions and appearances.

## SiteIconContract

| Field | Type | Rules |
|---|---|---|
| `svg` | root URL | Self-contained and visible |
| `png16` | root URL | 16 by 16, reduced mark |
| `png32` | root URL | 32 by 32, reduced mark |
| `ico` | root URL | Contains the declared classic entries |
| `apple_touch` | root URL | 180 by 180 and opaque |
| `manifest` | root URL | JSON whose icon URLs resolve and match size, type, and alpha rules |

## State Transitions

1. `source` to `profile-resolved`: validate brand configuration and select full/reduced sources.
2. `profile-resolved` to `generated`: clear only approved output roots, compose suites, write native metadata, write manifests, then create compatibility aliases.
3. `generated` to `verified`: decode every declaration and reject missing, extra, malformed, unsafe, stale, or inconsistent output.
4. `verified` to `published`: copy generated kit outputs into the site and release archive.
5. Any generation failure leaves the target suite absent or incomplete and cannot transition to `verified`.
