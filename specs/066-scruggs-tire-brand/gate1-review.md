# Gate 1 Review: Scruggs Tire & Alignment

**Prepared**: 2026-09-29 | **Approved production record**: `scruggs-g1-r4` | **Status**: Gate 1 approved and exact sources promoted; Gate 2 pending

Revision r2 responded to the owner's direction to retain the tire-only mark and change the Full lockup's backgrounds and wording color surgically. Revision r3 completed native-canvas lockups and licensed guide typography, then received exact owner approval. A private full-kit preview exposed a WCAG AA failure in the dark palette. Revision r4 changes the dark base from `#222222` to `#000000` and dark emphasis from deep red to the existing tire red. All seven SVG source hashes remain byte-identical to r3. The 24 proofs outside the dark background also remain identical; the eight dark-background proofs were rerendered and replayed exactly. The approved private packet is `dist/scruggs-gate1-r4/gate1-packet.json` (ignored by Git), digest `3f9a932c157e3b69b8df453d59f0447f1320d5437e911712fd1e6a56efa55206`, snapshot `4c28e4270a602702fac3d1bbbef6694044671014849a505dc3e3db2db077eae7`.

## One image to judge

The single design review image is `dist/scruggs-gate1-r2/full-white-square.png`: the red tire with the existing black wording on a true white square. The transparent square contains the same logo pixels without a background. The dark square contains the same red tire and wording shapes, with the wording turned white so it reads on black. These are exports of one identity, not competing logos. The tire-only mark is unchanged. The 32 small-size and monochrome proofs are technical verification evidence; they are not separate design options for the owner to select.

The owner's exact reply to the single white-square preview on 2026-09-29 was "yes that looks good". The owner then explicitly approved use of the matching transparent and dark versions and the unchanged tire-only mark as final production artwork. After the complete r3 record was shown as the same logo with native-canvas bindings and licensed guide fonts, the owner selected "Approve complete record". When the AA issue was reported with the unchanged logo sources and measured correction, the owner selected "Approve corrected palette" for r4 digest `3f9a932c157e3b69…`. The canonical continuity record stores this exact latest reply, full digest, scope, date, source snapshot, and 32 proofs. Its record digest at promotion was `39e5381f1553d62c65e5e1851de477985102b4992d8c1b90212be42b6c7af720`. A later non-identity approval-label correction refreshed only the `brand.json` receipt, producing current record digest `44ea8b1fae8b85557aa74415eb2ece0d73fa6aed1405133009b252826e20ab4e`; the source binding remains `2ee8452bd60e1fbc5428000f0042e3a43ac7a28bf174f3f7f5e2ed70c62df26b`.

## Exact source proposal

| Role | Promoted source under `brands/scruggs-tire-alignment/assets/source/` | SHA-256 | Treatment |
| --- | --- | --- | --- |
| Full master | `full-clear-square.svg` | `9fda1a0c266af644c1e5727e8c5ddc1af8361983cc67ffdf74050f0b9fe6e4e6` | Transparent 512x512 canvas, original red tire and black wording. |
| Full light | `full-white-square.svg` | `4c1e15521370be928ced3584bed2875db1062e0d2536df916b51d6888b5a2191` | Same pixels over a true `#FFFFFF` square. |
| Full dark | `full-dark-square.svg` | `2ea434a6cd8b4a3d16d51255e0eb557f2bd367e8451bd7a74db9765027fab03f` | Same red tire pixels; original black wording alpha is painted white over a true `#000000` square. |
| Reduced | `reduced-original.svg` | `358cd2ab99034d89935be7e1eb1b5df59c01afb0defda204203a9ff47439601b` | Supplied tire-only motif, unchanged from r1. |

The supplied Full PNG already has transparent pixels and black wording; the apparent off-white area in r1 came from the candidate's added plate. All three r2 Full sources embed the supplied 25,908-byte PNG byte for byte (SHA-256 `b556a49f5c04f3afbe69114a4a7dbef4ef10ad01e2f3161849b652bca410621a`). A passive SVG color filter uses its existing pixel classes and alpha to turn only black wording white for the dark variant. A generative edit was rejected because it changed tire and letter geometry. At 512 pixels, read-only inspection classified 25,858 red pixels and 5,440 black-wording pixels; all retained their intended red or became white with zero opaque class errors. The Reduced embedded PNG remains `e5c3ced0ea3f829b97d4411a2a249b89c1e31dd6c4397b0d0bf22fe33eb62b36`.

The authoritative source contract binds the clear square as the Full master, the dark square to the `color` Full colourway, and the white square to the `light` Full colourway. Native 416x236 wrappers of the same unchanged Full PNG serve the horizontal bindings; the square wrappers serve stacked bindings. No ZIP directory or asset naming becomes a kit schema. The production threshold remains 128 pixels: use the Reduced motif at smaller sizes because the Full wording collapses at 64 pixels and below. Source inventory, view boxes, framing, original masks, topology, and allowed transformations are recorded in the packet.

## Palette and proofs

The approved palette uses bright red `#ED1B24` for the tire and readable dark-surface emphasis on true black, and deep red `#7D0B13` for readable text/actions on white. Bright red on white measures 4.3904:1, below the 4.5:1 ordinary-text floor, so that use is excluded. The Full logo grounds are exactly white or black, with black or white wording respectively at 21:1. The packet contains sRGB roles, recomputed OKLCH values, semantic and color-vision rationale, surface and single-ink checks, and measured pairings. Gate 2 must qualify actual text and interface compositions.

The production renderer is `node-resvg` version `v26.5.0`, settings digest `23e65649bf2f3b34c4dcd1b5da67ce404b98f2da9c1e5001ae6e65d3d90e8397`. The packet includes Full and Reduced at 256, 64, 32, and 16 pixels on dark, light, black, and white, yielding 32 PNGs. A second production staging run matched all 32 proof hashes exactly. Every proof has side-by-side, alpha-overlay, silhouette-XOR, and color-difference evidence. Technical review sheets remain private in ignored `dist/` and are not additional logo options.

## Promotion and next gate

The repository promotion command validated the r4 approved record and copied `brand.json`, `README.md`, seven exact SVG sources, and `identity-continuity.json` into `brands/scruggs-tire-alignment/`. The promotion bundle digest is `eaad721dfe077594b2f1487132fcc8b3f6533de3106970186dec0a123165bc2f`; every installed source hash matched the approved bundle. The owner subsequently approved the revised assembled social image under Gate 2 packet digest `4ff5f087267495989ca5984a0a5660549666d8cbc8819e3c683e02073e9943cb`. The Gate 1 canonical source binding remains `2ee8452bd60e1fbc5428000f0042e3a43ac7a28bf174f3f7f5e2ed70c62df26b`.
