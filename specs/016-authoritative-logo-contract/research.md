# Research: Authoritative Logo Source Contract

## Decision 1: Require an explicit brand-level source mode

**Decision**: Add required `logo.source_mode` with exactly `constructed` or `authoritative`; migrate every production brand in the same slice and reject omission.

**Rationale**: Inferring authority from image elements, provenance labels, or the presence of supplied inputs recreates the ambiguity that caused issue #151. An explicit choice is reviewable and fail-closed.

**Alternatives considered**: Defaulting omitted values to constructed preserves compatibility but lets old definitions bypass the protection. Inferring authoritative mode from `geometry_provenance` or `authoritative_inputs` conflates reference artwork with generated identity.

## Decision 2: Bind Full and Reduced separately

**Decision**: Authoritative mode requires `logo.authoritative_input_ids.full` and `.reduced`, resolving respectively to approved unique `mark` and `reduced-mark` records.

**Rationale**: ShruggieTech already has distinct wide and reduced raster masters. One shared ID would either discard the approved reduced design or invite automatic derivation.

**Alternatives considered**: A single ID plus automatic reduction violates the issue's explicit reduced-redraw prohibition. Per-path embedded IDs duplicate source authority across rendering nodes.

## Decision 3: Keep one imported-image placement node per authoritative variant

**Decision**: Retain the existing `logo.paths.full` and `.reduced` containers for rendering compatibility, but authoritative mode permits exactly one image element per variant, requires its source to equal the bound input path, and rejects `d`, rect, or other constructed geometry.

**Rationale**: Existing image nodes contain the approved mask method and layout rectangle needed by the generic generator. Binding the node to an immutable input closes the substitution gap without rewriting the renderer or source art.

**Alternatives considered**: Removing paths and moving layout into a new source record couples immutable evidence to output placement. Accepting mixed image and vector nodes would preserve the defect.

## Decision 4: Reject construction helpers rather than silently ignore them

**Decision**: Authoritative mode fails contract validation when `build/mk_paths.py` exists beneath the staged brand source.

**Rationale**: A helper beside an authoritative logo is contradictory and may later be executed by an operator or automation. Explicit failure makes the migration intent visible before output exists.

**Alternatives considered**: Ignoring the helper with a warning is easier but leaves an attractive substitute source in the normal workflow. Deleting it automatically is destructive and hides the conflict.

## Decision 5: Record lineage in generated JSON and SVG metadata

**Decision**: Emit `logos/provenance.json` with a deterministic record for every logo SVG and generated logo PNG. Authoritative SVGs also carry source-mode, variant, input-ID, and source-hash attributes. Wordmark-only outputs are explicitly recorded as constructed typography and do not claim mark lineage.

**Rationale**: A standalone index supports verification and downstream tooling, while embedded metadata prevents an SVG from being detached from its claimed source without detection.

**Alternatives considered**: Metadata only is awkward to inventory and cannot cover PNGs. JSON only is separable from SVGs and weakens individual-file auditability.

## Decision 6: Verify deterministic raster mask topology

**Decision**: For raster authoritative inputs, derive the expected binary mask using the declared alpha or luminance method, normalize proportional scaling with nearest-neighbor measurement, and require exact binary topology agreement for generated recolor masters before platform conversion. Preserve the source aspect ratio inside declared placement bounds.

**Rationale**: Recoloring changes RGB intentionally, so byte equality is inappropriate. Mask topology detects shape changes without perceptual guessing and is deterministic offline.

**Alternatives considered**: Image similarity thresholds can bless visibly different art and require arbitrary tuning. Raw alpha comparison fails for the approved luminance-mask source. PNG byte comparison is prohibited and unstable across encoders.

## Decision 7: Extend the transformation vocabulary narrowly

**Decision**: Retain `embed-unchanged`, `recolor-mask`, and `palette-analysis`; add `resize` and `place-in-lockup`. Generation records only operations actually applied, in canonical order.

**Rationale**: These operations match the existing pipeline and the issue's explicitly approved examples. A closed vocabulary prevents free-form approval strings from authorizing unknown identity changes.

**Alternatives considered**: A generic `derive` permission is too broad. Encoding every output size as a distinct transformation would create noisy policy with no added identity protection.

## Decision 8: Preserve platform generators behind verified masters

**Decision**: Platform icon generators continue receiving generated Full or Reduced masters. Their manifests identify that master, while S016 proves those masters have valid authoritative lineage before the platform step begins.

**Rationale**: Reimplementing every platform compositor would expand risk without improving source authority. The security boundary belongs at the verified master handoff.

**Alternatives considered**: Recording every platform raster in the logo provenance index duplicates platform manifests and creates a large cross-generator transaction. Trusting platform inputs without validating the master leaves the original gap.
