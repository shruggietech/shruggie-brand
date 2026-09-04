# Changelog

## 1.1.2 - 2026-09-03

- Scoped identity hue-separation checks to production identities while preserving all fixture contrast checks.
- Added `logo.geometry_provenance` and a required imported-geometry reason.
- Preserved legacy path data while downgrading unsupported imported commands to warnings.
- Preserved native imported SVG rectangles, strokes, caps, and joins through export.
- Added lossless raster-mask masters for identities whose authoritative artwork has no vector source.
- Recorded imported geometry and its reason in verification output.
- Replaced generated font-network imports with deterministic `next/font/local` bindings for all bundled faces.
- Aligned the `fonts` registry item with its emitted `fonts.json` route.
- Made full-tier PDF and rendered-page failures fatal while preserving explicit lower-tier skips.
- Verified the bundled Node rasterizer fallback before advertising it as available.
- Restored Python 3.8 build discovery and suppressed project-owned Windows console processes.
- Forwarded native form `required` state and removed nested CTA controls from the ShruggieTech source UI kit.
- Resolved specimen fonts relative to the staged kit instead of the skill directory.
- Added the resvg and Inkscape CLI fallbacks advertised by the capability probe.
- Made pagination report a recorded skip when Playwright is installed without a matching Chromium binary.
- Made failed verification, image, PDF, and pagination gates print their diagnostic output in CI.
- Cleared generated PDFs, raster exports, and favicons before capability-tier downgrade skips.
- Separated favicon ICO verification from the SVG rasterizer capability gate.
- Made pipeline regression fixtures runnable on Python 3.8.
- Included Pillow compositing in the raster capability gate and cleared stale QC sheets before regeneration or skips.
- Made image-backed core SVG masters independent of Pillow and cleared stale PDF QC evidence before tier routing.
- Deferred image-QC Pillow imports until a measured raster or full path runs.

## 1.1.1 - 2026-09-03

- Added the non-exemptable WCAG 2.1 AA floor and accessible parent-green rules.

## 1.1.0 - 2026-09-02

- Added glyph construction, portability tiers, chart hue rotations, promoted generators, and Apache-2.0 licensing.
