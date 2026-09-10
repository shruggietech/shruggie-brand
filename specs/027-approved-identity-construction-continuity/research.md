# Research: Approved Identity Construction Continuity

## Decision 1: Approve a production-ready source, not an exploratory representation

**Decision**: Keep exploratory direction selection as a nonbinding state. Canonical approval begins only after every stroke-to-fill, bitmap-to-vector, primitive-system, view-box, crop, and framing conversion is complete and the candidate is rendered by the production path.

**Rationale**: S026 failed because Gate 1 approved a custom stroke representation while production later used different filled geometry and framing. Calling the earlier decision final approval made divergence both likely and costly.

**Alternatives considered**: Continue approving sketches and rely on a later visual check. This leaves reconstruction authorized implicitly. Treat Gate 2 as the production-geometry check. This reveals identity drift only after derivative work and repeats the known failure.

## Decision 2: Use a separate continuity record with a canonical identity digest

**Decision**: Add a fixed `identity-continuity.json` source record referenced by `brand.json`. Hash a canonical structured snapshot of governed identity fields and separately hash every external authoritative or construction source file.

**Rationale**: Embedding the record and its own file hash inside `brand.json` creates a digest cycle. A separate record can bind the exact identity configuration, source files, topology, framing, palette, and approval evidence without self-reference.

**Alternatives considered**: Store only a hash in the approval ledger. This reproduces the S026 failure because different representations can have unrelated hashes. Hash all of `brand.json`. That binds unrelated copy and metadata changes and creates unnecessary approval invalidations.

## Decision 3: Preserve historical brands through explicit baseline records

**Decision**: Classify every current brand as `glyphkit-constructed`, `legacy-constructed`, or `authoritative`. Generate `historical-baseline` records from current authoritative source without claiming retrospective approval. New canonical promotion requires `approved-canonical` status.

**Rationale**: The constitution forbids redrawing shipped geometry, while several identities predate glyphkit or formal approval bundles. A factual baseline provides future drift detection without fabricating history or disabling currently approved public kits.

**Alternatives considered**: Reconstruct every legacy mark in glyphkit. This is an identity change prohibited by P2. Grandfather brands without records. This leaves the strongest existing identities outside the new drift detector. Mark historical baselines as owner-approved. This makes a false provenance claim.

## Decision 4: Make glyphkit enforcement prospective and evidence-based

**Decision**: `glyphkit-constructed` records require a syntax-valid helper that imports glyphkit and produces path values from an approved primitive vocabulary. Literal SVG path data, custom geometry serializers, dynamic execution, and unapproved helper imports fail. `legacy-constructed` records preserve existing exceptions and cannot serve as new canonical approvals.

**Rationale**: Cueson’s corrected helper already follows this pattern. Covarity’s current metadata says glyphkit but its helper is a legacy custom arc serializer; correcting that provenance label is a factual metadata repair, not an identity alteration, and is safer than rewriting the mark.

**Alternatives considered**: Require glyphkit for all historical helpers immediately. This violates P2. Search source text only. Text matching is easy to evade and cannot distinguish a primitive call from a path literal. Execute helpers during validation. Untrusted source execution expands the security boundary and is unnecessary for provenance inspection.

## Decision 5: Exact structural invariants precede perceptual metrics

**Decision**: Require exact identity snapshot, path-array, source-file, role-map, framing, topology signature, and intended-color equality. Same-renderer proofs require exact file hashes. Cross-renderer proofs use hard-mask component and hole equality, an edge-aware changed-pixel fraction, visible bounds, centroid, interior color difference, and reviewable visual diffs.

**Rationale**: A high-resolution file can still contain coarse replacement geometry. Conversely, equivalent renderers can differ at antialias edges. Exact source invariants catch method changes, while edge-aware pixel measurements detect visible drift without pretending different rasterizers are byte-identical.

**Alternatives considered**: Gate only on IoU. The corrected S026 pair measured 0.947 at 512 and 0.831 at 32 despite exact coordinate continuity, so the preliminary 0.995 threshold would reject valid cross-renderer output. Ignore pixels entirely. This misses renderer, crop, and compositing defects.

## Decision 6: Calibrate cross-renderer thresholds from fixtures

**Decision**: Retain the issue’s 0.5 percent maximum for changed hard-mask pixels outside a one-pixel antialias edge band, require zero component and hole changes, rendered interior Delta E 2000 no greater than 1.0, visible bounds within one pixel, and centroid movement within one pixel. Record raw IoU but do not gate on it. Tests must prove the unchanged Cueson construction passes and the rejected method/framing switch fails.

**Rationale**: The S026 measurements show that raw boundary overlap degrades sharply at tiny sizes even when the coordinate contract is exact. Removing only the documented one-pixel edge band focuses the gate on interior and structural differences. One-pixel bound and centroid tolerances match the measured equivalent renderer displacement without allowing the former occupancy change.

**Alternatives considered**: Use the preliminary 0.995 IoU, 0.25 pixel centroid, and 0.5 percent total changed-pixel thresholds literally. They reject the known-equivalent fixture. Use loose IoU alone. It can hide local holes and topology changes.

## Decision 7: Promotion is explicit, bounded, atomic, and separate from build

**Decision**: Provide a promotion command that reads an approved bundle under an ignored approval root, validates safe relative paths and source hashes, stages copies in the destination parent, rejects existing destinations unless explicitly replacing the same bound files, then atomically installs and verifies byte equality. Ordinary builds remain read-only with respect to source.

**Rationale**: Promotion is the lifecycle point most likely to reintroduce reconstruction. Making it a narrow copy operation with rollback and containment checks prevents both identity drift and filesystem escape.

**Alternatives considered**: Document manual copying. This is not enforceable. Let normal generation promote automatically. Builds would mutate version-controlled source and violate P1. Accept arbitrary destination paths. This introduces traversal and overwrite risk.

## Decision 8: Palette qualification becomes canonical-approval input

**Decision**: Bind measured contrast, sibling hue separation, color-vision simulations, semantic-role separation, light/dark behavior, single-ink behavior, exact sRGB values, and measured OKLCH values before canonical approval.

**Rationale**: S026’s first palette approval collided with an existing sibling brand and had to be superseded. Qualification after approval wastes operator time and makes the approval bundle incomplete.

**Alternatives considered**: Keep palette checks at final kit verification. This detects problems too late. Allow accessibility waivers. P3 prohibits them.

## Decision 9: Build-time validation and independent verification share data, not logic

**Decision**: The continuity module produces a deterministic measured report. The build contract validates source and writes the report before derivative generation; the final verifier reloads the source record and independently checks the generated report and proof inventory.

**Rationale**: One shared canonical model avoids contradictory hashes, while a separate final consumer prevents generation from marking its own output valid without inspection.

**Alternatives considered**: Validate only at final verification. Invalid derivatives would already exist. Duplicate all logic in `verify.py`. Independent implementations are likely to drift and create the same handoff problem at a different layer.

## Decision 10: Preserve the existing two-gate workflow with a corrected first phase

**Decision**: Gate 1 contains direction selection followed by canonical-master approval. Gate 2 remains derivative and publication-surface approval and cannot modify production geometry.

**Rationale**: The two-gate model is valuable. The defect was the meaning of Gate 1, not the need for a later derivative review.

**Alternatives considered**: Add a third top-level owner gate. This increases ceremony without resolving terminology. Collapse all work into one approval. This hides the distinction between core identity and derivatives.
