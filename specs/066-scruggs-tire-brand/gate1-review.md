# Gate 1 Review: Scruggs Tire & Alignment

**Prepared**: 2026-09-29 | **Current candidate**: `scruggs-g1-r2` | **Status**: Owner decision pending

Revision r2 responds to the owner's direction to retain the tire-only mark and change the Full lockup's backgrounds and wording color surgically. It supersedes r1's white-plate Full source. The complete private review packet is `dist/scruggs-gate1-r2/gate1-packet.json` (ignored by Git), with canonical content digest `cff80cc50c777cbe2335358f3c4d95e877c525a4414e05b7eb2710ff30c04ad0`. Its identity snapshot is `7681816322f1f38a5b9f15fb3542a3b78481a3f6992d3e7dbf2b78c8b08d95c3`. This is a candidate packet, not approval or a publishable kit.

## One image to judge

The single design review image is `dist/scruggs-gate1-r2/full-white-square.png`: the red tire with the existing black wording on a true white square. The transparent square contains the same logo pixels without a background. The dark square contains the same red tire and wording shapes, with the wording turned white so it reads on black. These are exports of one identity, not competing logos. The tire-only mark is unchanged. The 32 small-size and monochrome proofs are technical verification evidence; they are not separate design options for the owner to select.

## Exact source proposal

| Role | Candidate source under private `candidate/assets/source/` | SHA-256 | Treatment |
| --- | --- | --- | --- |
| Full master | `full-clear-square.svg` | `9fda1a0c266af644c1e5727e8c5ddc1af8361983cc67ffdf74050f0b9fe6e4e6` | Transparent 512x512 canvas, original red tire and black wording. |
| Full light | `full-white-square.svg` | `4c1e15521370be928ced3584bed2875db1062e0d2536df916b51d6888b5a2191` | Same pixels over a true `#FFFFFF` square. |
| Full dark | `full-dark-square.svg` | `2ea434a6cd8b4a3d16d51255e0eb557f2bd367e8451bd7a74db9765027fab03f` | Same red tire pixels; original black wording alpha is painted white over a true `#000000` square. |
| Reduced | `reduced-original.svg` | `358cd2ab99034d89935be7e1eb1b5df59c01afb0defda204203a9ff47439601b` | Supplied tire-only motif, unchanged from r1. |

The supplied Full PNG already has transparent pixels and black wording; the apparent off-white area in r1 came from the candidate's added plate. All three r2 Full sources embed the supplied 25,908-byte PNG byte for byte (SHA-256 `b556a49f5c04f3afbe69114a4a7dbef4ef10ad01e2f3161849b652bca410621a`). A passive SVG color filter uses its existing pixel classes and alpha to turn only black wording white for the dark variant. A generative edit was rejected because it changed tire and letter geometry. At 512 pixels, read-only inspection classified 25,858 red pixels and 5,440 black-wording pixels; all retained their intended red or became white with zero opaque class errors. The Reduced embedded PNG remains `e5c3ced0ea3f829b97d4411a2a249b89c1e31dd6c4397b0d0bf22fe33eb62b36`.

The existing authoritative source contract binds the clear square as the Full master, the dark square to the `color` Full colourway, and the white square to the `light` Full colourway. It binds the same Reduced source as r1. No ZIP directory or asset naming becomes a kit schema. The production threshold remains 128 pixels: use the Reduced motif at smaller sizes because the Full wording collapses at 64 pixels and below. Source inventory, view boxes, framing, original masks, topology, and allowed transformations are recorded in the packet.

## Palette and proofs

The candidate keeps bright red `#ED1B24` for the tire and other non-text emphasis and deep red `#7D0B13` for proposed readable red text/action on white. Bright red on white measures 4.3904:1, below the 4.5:1 ordinary-text floor, so that use is excluded. The new Full backgrounds are exactly white or black, with black or white wording respectively at 21:1. The packet contains the sRGB roles, recomputed OKLCH values, semantic and color-vision rationale, surface and single-ink checks, and measured pairings. Gate 2 must qualify its actual text and interface compositions.

The production renderer is `node-resvg` version `v26.5.0`, settings digest `23e65649bf2f3b34c4dcd1b5da67ce404b98f2da9c1e5001ae6e65d3d90e8397`. The packet includes Full and Reduced at 256, 64, 32, and 16 pixels on dark, light, black, and white, yielding 32 PNGs. A second production staging run matched all 32 proof hashes exactly. Every proof has side-by-side, alpha-overlay, silhouette-XOR, and color-difference evidence. The 16 Reduced proof hashes are identical to r1. `full-variants-review.png`, `full-contact.png`, and `reduced-contact.png` are local review sheets in `dist/scruggs-gate1-r2/`.

## Decision requested

Judge only whether the single Full logo in `full-white-square.png` has the desired existing tire, lettering, spacing, and true white background. The clear and dark exports follow that choice mechanically. If the primary logo is right, an exact Gate 1 approval can then bind all four source files, the Full and Reduced master roles, palette, framing, topology, renderer, and proof matrix, with exact wording, approver, date, scope, candidate ID, and packet digest recorded after the decision. Gate 2 will separately review assembled fundamentals and a social share image before production kit compilation. No approval is inferred from the archive, prior r1 packet, or silence.
