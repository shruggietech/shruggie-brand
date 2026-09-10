# Identity Continuity

Identity work has two distinct approvals. Direction selection chooses what to construct. Canonical approval accepts the exact production source that later generation must use. Never treat the first as the second.

## Lifecycle

`exploratory` may advance to `direction-selected`; `direction-selected` may advance only to `canonical-candidate`; `canonical-candidate` may advance to `canonical-approved`; and only that approved source may be promoted. Promotion precedes derivative review. Gate 2 approval authorizes the derived surface set and may lead to publication eligibility. Any governed drift invalidates the applicable approval and returns the work to a new canonical candidate.

A direction-selected image or sketch is nonbinding. It cannot authorize permanent source, derivative generation, publication, or consumer integration. Silence cannot supply canonical approval.

## Canonical approval packet

Construct or bind the real Full and Reduced production masters before asking for canonical approval. Use the same source mode, construction helper, path arrays, framing, palette role map, and renderer configuration that production will use. The packet must include:

- exact source inventory and SHA-256 values;
- canonical snapshot and source revision;
- construction provenance and allowed primitive vocabulary;
- geometry, topology, view box, crop, padding, and framing records;
- complete palette qualification with bound sRGB and OKLCH values;
- production renderer identity, version, and deterministic settings;
- Full and Reduced proofs at 256, 64, 32, and 16 pixels on dark, light, black, and white;
- side-by-side, alpha-overlay, silhouette-XOR, and color-difference evidence;
- exact owner wording, approver, date, scope, candidate identifier, and packet hash.

Palette qualification happens before canonical approval. Every declared role must pass contrast, sibling separation, color-vision, semantic-role, surface, single-ink, and rendered-color checks. A selected hue or extracted swatch is only a proposal until this evidence is complete.

## Construction continuity

New constructed identities use `glyphkit-constructed`. Their helper imports `glyphkit`, calls approved primitives, and contains no literal path payload or custom path serializer. Existing helpers or path data that predate this rule use `legacy-constructed` only as a historical baseline. Existing authoritative masters use `authoritative` and remain byte-identical.

Canonical promotion copies declared source bytes atomically. It never traces, redraws, normalizes, serializes a second time, or reconstructs approved geometry. The production build validates the committed continuity record before any derivative generation and writes a measured report that verification checks independently.

## Proof policy

When approval and production use the same renderer, proof files must be byte-identical. A documented cross-renderer comparison keeps source snapshot, topology, palette, and framing exact, then measures components, holes, bounds, centroid, hard-mask overlap, changed pixels outside a one-pixel antialias edge band, and interior Delta E. Raw IoU remains review evidence rather than the sole verdict.

Any new component or hole, changed framing, changed intended color, changed source method, changed helper bytes, changed path data, changed renderer setting, or stale proof hash fails closed. Visual similarity cannot override these source and structural invariants.

## Historical migration

A `historical-baseline` records the current production source and its limits. It cannot claim retrospective owner approval, satisfy a new canonical approval, or change public eligibility. Moving a historical identity into the prospective workflow requires a new canonical candidate and explicit owner approval.

## Gate 2 boundary

Gate 2 reviews derivatives made from the promoted canonical source. It may approve lockups, wordmarks, icons, and publication surfaces within the recorded scope. It must not introduce, reconstruct, simplify, or first reveal production master geometry. Any such change invalidates canonical approval and returns to the canonical candidate stage.
