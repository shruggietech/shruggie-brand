# Research: Asset Delivery Fidelity

## Decision 1: Make square-knockout mask coordinates explicit

**Decision**: Every generated square-knockout mask will declare an explicit local coordinate region matching the square mark canvas.

**Rationale**: The current mask declares `maskUnits="userSpaceOnUse"` but relies on percentage defaults for its region. When the mark is nested in a short lockup viewport, those defaults resolve against the lockup viewport and clip most of the 1000-unit square mask. This exactly explains the fold-fragment-only output. Explicit local bounds preserve the existing knockout geometry in standalone, horizontal, and stacked contexts.

**Alternatives considered**: Redrawing a monochrome mark was rejected because it would change protected identity geometry. Replacing knockout behavior with a flat filled mark was rejected because the paper-and-G interior would disappear. Expanding the outer lockup canvas was rejected because it would change approved composition and would not repair the underlying coordinate contract.

## Decision 2: Verify structure and rendered behavior

**Decision**: Validate explicit mask coverage in each generated SVG and add rendered alpha-bound and SVG-to-PNG checks for black and white full lockups.

**Rationale**: Structural validation catches the coordinate defect even when raster capability is unavailable. Rendered measurement catches semantically valid SVG that still collapses or clips in a real renderer. Existing provenance hashes prove byte integrity but cannot prove that the approved composition remains visible.

**Alternatives considered**: Golden PNG byte comparison was rejected by the constitution and because encoders vary by platform. Screenshot-only review was rejected because it is not a fail-closed production gate. A Glitchpad-only verifier was rejected because the mask contract is shared generator behavior.

## Decision 3: Keep canonical identity data frozen

**Decision**: Change no Glitchpad path, canvas, square-enclosure, palette, lockup, or typography value.

**Rationale**: The defect is caused by mask-region inheritance, not the approved source. Preserving the brand contract isolates the fix to generation and proves that S021 is corrective rather than an identity redesign.

**Alternatives considered**: Adding replacement paths, per-color variants, or brand-local offsets was rejected as prohibited reconstruction and unnecessary architecture.

## Decision 4: Use one bounded preview media viewport

**Decision**: Both asset-library cards and guideline logo examples will use a shared media wrapper with fixed block containment, centered layout, clipped paint, and a child image constrained in both axes.

**Rationale**: The existing rules constrain only maximum image size and do not provide a separately measurable inner media boundary on every surface. A common wrapper makes card artwork, baked backgrounds, and metadata separation explicit and testable across asset shapes.

**Alternatives considered**: Per-family dimensions and per-brand offsets were rejected because they hide bad layout assumptions. Changing generated asset canvases was rejected because #165 is presentation-only. Applying the rule only to asset cards was rejected because the issue also covers guideline logo examples.

## Decision 5: Measure browser geometry rather than visual intent

**Decision**: The production route audit will measure each preview boundary, image boundary, and metadata divider at mobile, tablet, desktop, and 200 percent zoom in both themes.

**Rationale**: Bounding-box assertions directly prove containment and center alignment within one device pixel. Existing route traversal already covers all generated brands and can add these checks without a second site harness.

**Alternatives considered**: Static class-name assertions alone were rejected because they cannot prove computed layout. Pixel screenshots alone were rejected because they make failures harder to localize and encourage fragile golden images.

## Decision 6: Treat transparency as a declared surface concern

**Decision**: Continue selecting preview wells from generated appearance metadata and require the full image canvas, including any baked background, to remain inside the media viewport.

**Rationale**: Transparent black and white assets need an opposing surface to remain visible, while opaque icons carry their own plate. The existing generated portal already declares the correct light or dark surface and remains the single source of truth.

**Alternatives considered**: CSS inversion and filename-only substitutions were rejected because they can misrepresent shipped bytes. Automatic visible-ink cropping was rejected because it would discard approved clear space.
