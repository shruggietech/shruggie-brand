# Generated Specimen Portability Contract

## Artifact

Each brand kit exposes exactly one generated type specimen at `specimens/<slug>-type-specimen.svg`.

## Reference contract

- Every `href` and `xlink:href` value MUST begin with `data:` or `#`.
- An image-backed governed logo component MUST use one base64 data URI in both `href` forms.
- Relative paths, root-relative URLs, absolute filesystem paths, protocol-relative URLs, and external schemes are forbidden.
- An embedded source MUST declare the media type associated with its governed file format.

## Identity contract

- Decoding an authoritative embedded payload MUST reproduce the governed source bytes exactly.
- When `supplied_lockup_input_ids.horizontal.color` identifies an approved authoritative lockup with unchanged-byte embedding and resize permission, the specimen MUST prefer that source over the canonical full/reduced component list.
- A preferred lockup MUST retain its native aspect ratio, scale down only when required to fit the existing logo grid, and be centered within that grid.
- When no preferred lockup is declared, the component's `x`, `y`, `width`, `height`, `preserveAspectRatio`, and ancestor placement transform MUST retain the existing canonical specimen placement.
- Embedding MUST NOT parse, normalize, optimize, trace, recolor, or rewrite the authoritative artwork.

## Render contract

- The generated mark group MUST have a stable internal identifier.
- A renderer-capable verification tier MUST rasterize the exact generated SVG and find meaningful non-background pixels inside the mark group region.
- A missing renderer MUST produce a named skip at a lower capability tier, never a false pass.
- The authoritative CI tier MUST execute the rendered check.

## Publication contract

- The deterministic kit archive MUST contain the canonical specimen bytes.
- The hosted `downloads/files/specimens/` copy MUST match the same canonical bytes.
- Browser verification MUST navigate directly to the hosted SVG and to its offline local copy, with no supporting source-art directory available.

## Failure contract

Generation or verification fails when a source escapes the kit boundary, is missing, has an unsupported media type, produces inconsistent link attributes, decodes to noncanonical bytes, retains a non-self-contained reference, or yields no visible artwork in the declared mark region.
