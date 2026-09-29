# Gate 1 Review: Scruggs Tire & Alignment

**Prepared**: 2026-09-29 | **Candidate**: `scruggs-g1-r1` | **Status**: Owner decision pending

This is a private candidate for the exact production Full and Reduced sources. It does not authorize promotion, a publishable kit, or a public website change. The complete local review packet is `dist/scruggs-gate1-candidate/gate1-packet.json` (ignored by Git), with canonical content digest `3c5771a96bb391db46b315ddccd292bfdaf0c2b53026a73dd4df1b0e79025faf`. The governed identity snapshot inside it is `5adfd4f346f8fe6092b4755408e9c3d957f088d938253cb89103479956c32979`.

## Exact source proposal

| Role | Candidate source | SHA-256 | Construction |
| --- | --- | --- | --- |
| Full | `candidate/assets/source/full-white-plate.svg` | `ccdeeaee75e6fbafa5a2d0d7917891c6cf27bd64b73ec8e38ac5304c6a3269f6` | Passive 416x236 SVG with a white plate and the supplied transparent PNG embedded byte for byte. |
| Reduced | `candidate/assets/source/reduced-original.svg` | `358cd2ab99034d89935be7e1eb1b5df59c01afb0defda204203a9ff47439601b` | Passive 180x180 SVG with the supplied favicon PNG embedded byte for byte. |

The embedded Full PNG is also byte identical to the current website logo. Its SHA-256 is `b556a49f5c04f3afbe69114a4a7dbef4ef10ad01e2f3161849b652bca410621a`; the embedded Reduced PNG is `e5c3ced0ea3f829b97d4411a2a249b89c1e31dd6c4397b0d0bf22fe33eb62b36`. The white plate is a visible candidate treatment for the black wordmark on dark backgrounds, so it is included in the exact source subject to owner approval. Neither supplied image was traced or redrawn. The allowed source vocabulary is `rect` plus `image` for Full, and `image` for Reduced.

The preferred mode is authoritative source binding because it preserves the live identity's supplied pixels and allows both marks through the existing production source contract. A newly constructed vector master would reinterpret the existing geometry and is not proposed for this candidate. The full production threshold is 128 pixels: the Full wordmark becomes too small to read in its 64, 32, and 16 pixel proofs, while the Reduced tire motif remains the intended small icon. The original Full mask measures 35 components and 5 holes at native resolution; the Reduced mask measures 14 components and 0 holes. Full and Reduced canvas bounds, masks, framing, source bytes, and all per-proof metrics are in the packet.

## Palette and proof scope

The candidate binds the base CSS bright red `#ED1B24` to mark and other non-text emphasis, deep red `#7D0B13` to proposed readable text/action on white, and separate dark surface roles. Bright red measures 4.3904:1 on white, below the 4.5:1 ordinary-text floor, so this packet excludes that pairing. Deep red on white measures 10.885:1; white on the darkest proposed surface measures 15.91:1. The packet contains every declared sRGB role, recomputed OKLCH values, semantic use and color-vision rationale, surface and single-ink checks, and the measured pairings. Gate 2 must still qualify its actual text and interface compositions.

The production proof renderer is `node-resvg` version `v26.5.0`, settings digest `23e65649bf2f3b34c4dcd1b5da67ce404b98f2da9c1e5001ae6e65d3d90e8397`. Full and Reduced were each rendered at 256, 64, 32, and 16 pixels on dark, light, black, and white, yielding 32 PNGs. An independent second staging run produced the same SHA-256 for every proof. Each coordinate has side-by-side, alpha-overlay, silhouette-XOR, and color-difference PNG evidence under the ignored `dist/scruggs-gate1-candidate/evidence/` directory. `full-contact.png` and `reduced-contact.png` are review sheets made from the exact proof PNGs; the packet lists every proof and comparison hash.

## Decision requested

Review the two contact sheets and packet, then either approve `scruggs-g1-r1` exactly or identify revisions. An approval must cover the Full and Reduced master bytes, palette, framing, topology, renderer, and complete proof matrix, and the exact wording, approver, date, candidate ID, and packet hash will be recorded. Approval of this source packet is Gate 1 only. Gate 2 will separately review the complete assembled fundamentals and social share image before production kit compilation. No approval is inferred from the source archive or silence.
