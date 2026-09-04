# Changelog

All notable changes to the Shruggie brand system are documented in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

No unreleased changes.

## [1.1.2] - 2026-09-03

### Added

- Added `logo.geometry_provenance` with `glyphkit` and `imported` values so legacy geometry remains unchanged while its origin is visible in verification.
- Added repository-wide CI, deterministic release automation, and a generated documentation and registry site.
- Added five migrated production kits and a synthetic pipeline fixture.
- Added Spec Kit 1.0.4 with Codex skills integration and PowerShell scripts.

### Changed

- Imported path command violations are warnings for legacy geometry and remain failures for glyphkit-authored geometry.
- Preserved native SVG primitives and raster-only authoritative identity art through generated exports.
- Scoped sibling hue allocation to production identities while retaining contrast checks for fixtures.

### Fixed

- Replaced ShruggieTech's `#2BCC73` light-surface link color, measured at 1.98:1, with `#037B40`, measured at 5.05:1, to meet WCAG 2.1 AA.
- Corrected the shadcn binding documentation to use the published `/brand/r/{name}.json` route.
- Restored Python 3.8 kit discovery and added a minimum-version CI job.
- Replaced generated font-network imports with local bundled bindings and aligned the `fonts.json` registry route.
- Made unexpected full-tier PDF and page-QC failures block builds and releases.
- Made the core tier preserve vector output while explicitly recording raster and PDF skips.
- Verified renderer fallbacks before advertising them as available.
- Suppressed project-owned Windows console subprocesses and disabled their interactive input.
- Forwarded native required state from generated form controls and removed nested interactive CTA markup.
- Removed private workstation paths and Cloudflare resource identifiers from public planning records.
- Cleared generated PDFs, raster exports, and favicons before capability-tier downgrade skips so stale artifacts cannot enter a later manifest or release.
- Verified favicon ICO output against its independently measured writer capability.
- Enforced the repository's single-physical-line Markdown prose policy in public planning records and CI.
- Made the pipeline regression fixtures Python 3.8-compatible and run them in the minimum-version hosted job.
- Included Pillow compositing in the measured raster capability instead of allowing a late import failure.
- Cleared stale generated QC sheets before full-tier capture or lower-tier skips.
- Recolored image-backed SVG master masks through a standard-library PNG path so core-tier generation does not import Pillow.
- Cleared stale PDF contact sheets and extracted pages before lower-tier skips or replacement attempts.

## [1.1.1] - 2026-09-03

### Added

- Added the non-exemptable WCAG AA floor for all canon-declared text and fill roles.
- Added canon rules for accessible ShruggieTech green on light surfaces.

## [1.1.0] - 2026-09-02

### Added

- Added the glyph construction layer, portability tiers, per-brand chart hue rotations, promoted generators, and standard-library geometry tests.

### Changed

- Relicensed the brandbuilder code, templates, and reference documentation from proprietary terms to Apache-2.0 while reserving names and marks.

[Unreleased]: https://github.com/ShruggieTech/shruggie-brand/compare/v1.1.2...HEAD
[1.1.2]: https://github.com/ShruggieTech/shruggie-brand/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/ShruggieTech/shruggie-brand/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/ShruggieTech/shruggie-brand/releases/tag/v1.1.0
