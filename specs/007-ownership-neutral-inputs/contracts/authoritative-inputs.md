# Contract: Authoritative Supplied Inputs

## Declaration

An authoritative input record identifies one unchanged source file, its role, byte hash, media facts, usage basis, and allowed operations. A supplied mark and supplied wordmark are independent roles. A constructed counterpart may coexist with either one.

## Integrity rules

1. Resolve the declared path inside the staged kit and reject traversal or link escape.
2. Measure the file format and SHA-256 from bytes, then compare both with the declaration.
3. Keep `mark`, `reduced-mark`, and `wordmark` roles unique. Permit multiple reference-art inputs only under unique identifiers.
4. Reject active SVG, live text, event attributes, external URL references, and externally loaded content.
5. Require every operation performed by a generator to appear in `approved_transformations`.
6. Never rewrite the authoritative file or normalize its vector path data.
7. Emit generated audit evidence without copying confidential agreements.

## Palette analysis

Raster analysis counts exact visible RGB values after RGBA conversion and ignores alpha-zero pixels. Passive SVG analysis counts literal solid fill and stroke colors. Candidate ordering is descending occurrence count followed by uppercase hex. The result records limitations and the exact source hash.

Palette evidence is advisory. A canonical color may cite it only through a human approval record that still matches the input identifier, current hash, and selected candidate. Existing WCAG 2.1 AA verification remains mandatory after approval.

## Failure

Missing input, hash drift, format mismatch, escaping path, unsafe SVG, duplicate protected role, undeclared transformation, no visible color, stale approval, or an approved candidate absent from current evidence blocks publication.
