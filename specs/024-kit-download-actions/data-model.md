# Data Model: Complete Kit Downloads and Explicit Brand Actions

## ProductionBrandArchive

| Field | Type | Rules |
|---|---|---|
| slug | string | Matches the source directory and `brand.json` |
| version | semantic version string | Matches `brand.json`, `manifest.json`, and the filename |
| filename | string | `<slug>-brand-<version>.zip` |
| publicPath | site path | `/<slug>/downloads/<filename>` |
| sourceRoot | directory | Final verified `dist/<slug>/` only |
| entries | ordered files | Every source file plus required root licenses |
| manifestCoverage | path, bytes, SHA-256 | Every non-license payload except `manifest.json` is recorded exactly once |
| archiveMetadata | timestamp, mode, compression | Stable for identical inputs |

### Validation

- The source must contain `brand.json`, `manifest.json`, `VERIFY.md`, and a PDF-signature `brand-guide.pdf`.
- Paths are relative POSIX paths with no absolute root, drive prefix, backslash, parent traversal, or normalized duplicate.
- Recorded byte counts and SHA-256 hashes match archive payloads.
- Added licenses match repository source bytes.
- Any unrecorded non-exempt payload fails publication.
- Verification completes before the staged file replaces the public destination.

## PortfolioBrandRecord

| Field | Type | Rules |
|---|---|---|
| slug | string | Unique public brand identifier |
| title | string | Public brand name |
| descriptor | string | Generated public description |
| icon | site path | Generated square mark asset |
| accent | color | Generated accessible presentation token |
| guidelinesPath | site path | `/<slug>/guidelines/` |
| kitArchive | site path | ProductionBrandArchive public path |
| kitArchiveFilename | string | Exact download filename |
| vendorBoundary | string or null | Full generated legal notice |
| showcaseSurface | color or absent | Explicitly approved card surface only |
| showcaseForeground | color or absent | Measured foreground for governed surface |

## DesktopBrandCard

| State | Description | Allowed interaction |
|---|---|---|
| Resting | Mark, name, and descriptor visible | Only hidden-but-focusable action anchors can receive sequential focus |
| Revealed | Mark and name remain; actions replace descriptor | Guidelines and Download Kit anchors only |
| Reduced motion | Same semantic states without animated displacement | Same two anchors |

The outer card height and grid position are invariant across states.

## MobileBrandDisclosure

| State | Summary | Panel | Focus contract |
|---|---|---|---|
| Collapsed | Mark and name | Hidden | Descendant actions excluded from sequential focus |
| Expanded | Mark and name | Descriptor, Guidelines, Download Kit | Header and both anchors available in document order |

Native disclosure state supplies the expanded relationship without client state.

## PortfolioVendorNotice

| Field | Type | Rules |
|---|---|---|
| id | string | Stable target for marker association |
| applicableBrands | ordered slugs | Records whose vendor boundary is present |
| notices | unique ordered strings | Full generated notices, never rewritten |
| marker | `*` plus accessible text | Present only for applicable brands |

## State Transitions

- Verified kit output transitions to a staged archive, then to a published archive only after contract verification passes.
- Desktop cards transition between Resting and Revealed from hover or focus-within; leaving both returns to Resting.
- Mobile disclosures transition between Collapsed and Expanded through native summary activation.
- CSS breakpoint selection exposes the desktop or mobile representation while both derive from the same PortfolioBrandRecord.
