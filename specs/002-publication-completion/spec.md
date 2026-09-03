# Feature specification: Publication completion

## Goal

Resolve every actionable post-merge review finding before v1.1.2, expose the private work directive through sanitized GitHub tracking, and preserve the brandbuilder's capability-tier contract across Python, Windows, Linux, and offline Next.js consumers.

## Tracked findings

This slice implements issues #17 through #30:

1. Python 3.8 build discovery.
2. Local bundled Next.js font bindings.
3. Fatal full-tier PDF export failures.
4. Fatal full-tier rendered-page QC failures.
5. Consistent `fonts` registry naming and routes.
6. One interactive element per ShruggieTech CTA.
7. Native required state on generated controls.
8. Hidden, non-interactive Windows console subprocesses.
9. Explicit core-tier raster skips with retained vector output.
10. Removal of stale PDFs during lower-tier rebuilds.
11. Removal of stale rasters and favicons during core-tier rebuilds.
12. Independent SVG raster and ICO capability gates.
13. Single-physical-line Markdown prose in governed planning records.

## Additional requirements

- Issues #6 through #15 must contain the complete sanitized public translation of the private directive, including progress and acceptance evidence.
- Public repository files must not expose private workstation paths or Cloudflare account, zone, or record identifiers.
- Lower-tier capability gaps must be named skips. A failure after a capability probe succeeds must return nonzero.
- Releases must assert that every production kit includes its brand-guide PDF.

## Acceptance criteria

- Python 3.8 compiles the scripts and lists all six build sources.
- Unit tests cover capability parsing, offline fonts, core raster skips, tier-downgrade cleanup, fatal full-tier PDF/page failures, independent ICO capability, Windows flags, form semantics, and CTA semantics.
- A full-tier local run builds all five production kits and the fixture with zero problems.
- The site statically exports all 25 routes and contains `fonts.json` for every brand registry.
- Release packaging emits exactly two skill bundles and five production kits, each with required licenses and each production kit with a PDF.
- Hosted PR checks pass before merge and the tag is created only from the corrected `main` commit.
