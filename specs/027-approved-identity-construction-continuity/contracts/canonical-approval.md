# Canonical Approval Contract

## Direction selection

A direction-selection packet may contain sketches, generated images, custom study geometry, or textual rationale. It must say that the decision is nonbinding and cannot authorize permanent source, derivatives, publication, or consumer integration. Selecting a direction creates no canonical source hash.

## Canonical candidate entry

A direction becomes a canonical candidate only after every required conversion has occurred. The provisional source must already use the final source mode, construction system or authoritative binding, full and reduced masters, view box, framing, role map, palette, and production renderer configuration.

The candidate packet must contain:

- the exact provisional source inventory and SHA-256 values;
- the canonical identity snapshot and digest;
- construction provenance and allowed primitive vocabulary;
- full and reduced geometry, topology, and framing records;
- complete palette qualification whose role set equals the governed palette and whose exact sRGB/OKLCH correspondence is independently measured;
- renderer identity, version, and deterministic settings;
- production-path proofs at 256, 64, 32, and 16 pixels on dark, light, black, and white surfaces;
- per-coordinate hash-bound side-by-side, overlay, silhouette-XOR, and color-difference PNG evidence;
- the exact manifest hash offered for approval.

## Decision semantics

`approve` binds only the exact bundle, source snapshot, proof manifest, and scope shown. The record must carry a human approver, date, exact owner wording, source revision, and unique candidate identifier. Silence, direction selection, partial approval, or approval of a different representation does not satisfy canonical approval.

Gate 1 stores a normalized canonical-source digest. It excludes the `brand.json` source-file entry that contains the digest itself, while retaining the identity snapshot, every non-brand source digest, palette qualification, renderer settings, proof matrix, and approval decision. The exact `brand.json` bytes remain independently hash-bound by the continuity record, so the binding has no cryptographic cycle and source drift still fails.

Any missing field, stale hash, incomplete matrix, failed qualification, renderer ambiguity, source escape, or contradictory state keeps the candidate ineligible.

## Invalidation

Changing any construction engine, helper bytes, authoritative source binding, path array, topology, framing, role mapping, logo derivative setting, palette, renderer setting, production generator implementation, or governed proof invalidates canonical approval. The workflow returns to a new canonical candidate and cannot repair or reapprove automatically.

Gate 2 may change typography arrangements and derivative applications within its stated scope, but it may not reconstruct or first reveal production geometry.
