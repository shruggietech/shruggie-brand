# Contract: Monochrome Lockup Integrity

## Purpose

Define the fail-closed contract for black and white full lockups built from a square-enclosed mark.

## Generation Contract

- The lockup uses the full source variant and the existing protected path strings.
- The square-knockout mask declares local user-space coordinates and explicit bounds equal to the complete square mark canvas.
- The mask region fully contains the rounded-square target and every approved knockout path after its declared composition transform.
- The only permitted difference between black and white output is the governed monochrome paint value.
- Horizontal and stacked placement retain the declared mark size, gap, wordmark scale, baseline, padding, and canvas.
- No reduced path, CSS filter, trace, crop, or replacement geometry may satisfy this contract.

## Verification Contract

- Each black and white full-lockup SVG contains one complete referenced square-knockout mask with explicit coordinates.
- Each mask target and its transformed content remain inside the explicit mask region.
- The rendered mark region reaches the expected declared height and does not collapse to a fold or border fragment.
- The full wordmark remains present and inside the lockup canvas.
- Each raster delivery agrees pixel-for-pixel in rendered behavior with its verified SVG master at the same dimensions, independent of encoder bytes.
- Any missing component, clipped mask, reduced substitution, malformed reference, or SVG-to-PNG disagreement fails verification.

## Identity Boundary

The following remain byte-identical source data: Glitchpad full and reduced path strings, fill rules, square-enclosure dimensions, role assignments, lockup measurements, and typography selection.
