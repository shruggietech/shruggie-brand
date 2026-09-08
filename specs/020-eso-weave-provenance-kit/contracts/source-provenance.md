# Contract: Source Provenance and Fidelity

## Snapshot

S020 reads the fetched ESO Weave default branch and records its exact commit before copying files. The snapshot is refreshed immediately before both owner gates. The issue intake commit is retained as a comparison baseline.

## Inventory

Every required file has a Source Evidence Record matching the data model. Missing files, unsafe paths, duplicate ids, hash mismatch, unknown usage basis, or unclassified authority fail before brand generation.

Moved intake paths must record `intake_path` and `upstream_path`. S020 currently recognizes:

| Intake path | Current canonical evidence |
| --- | --- |
| `docs/brand/ESO-Weave-Brand-v1.md` | `docs/src/development/brand-standard.md` |
| `docs/ESO-Weave-Specification.md` | Current `docs/src/` manual plus `docs/project/` governance and migration records |

## Authoritative SVG Rule

`eso-weave-mark.svg` and `eso-weave-glyph.svg` are copied byte for byte. Their SHA-256 values must remain:

- Mark: `696d256c4ec0eae9aed315a1b489bbf5115ec33827e966a6e993708bf3f3109f`
- Glyph: `552f3203f0001b15e3adea9b720cb2f78be1427a12410f3e304170d973fef5ea`

The source diff may add these files but must not rewrite their XML, strokes, path commands, coordinates, colors, or metadata.

## Provenance Classes

- Public repository evidence may prove paths, bytes, commits, authored statements, and historical introduction.
- Operator-supplied assertions may record facts supplied in issue #153 but must say that the public history does not independently establish them.
- Reference-only rasters may establish intended rendering and platform coverage but never become authoritative geometry.

## Drift

If a synchronized source hash differs from an approved record, every dependent palette, derivative, and publication approval becomes stale. No tolerance, visual-similarity exception, or filename-based fallback is permitted.
