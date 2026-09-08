# Verification Evidence: ESO Weave Provenance and Current-Spec Kit

## Current Status

- Slice: S020
- Issue: [#153](https://github.com/shruggietech/shruggie-brand/issues/153)
- Branch: `codex/020-eso-weave-provenance-kit`
- Gate: Gate 2 approved, exact public projection authorized
- Production derivative geometry created: yes, only the Gate 1-approved set
- Public ESO Weave site or registry output created: yes, only the eight Gate 2-approved generated surfaces

## Repository Synchronization

- Shruggie Brand `main` was synchronized at merge commit `322be97dbf83ad4b604b612ba5eda1af198843c6` before the branch was created.
- ESO Weave remote `main` was fetched without switching or modifying its unrelated local working branch.
- Current upstream commit: `a165091d93b687100dc7471bbf5b7dd5f9d4c1e9`.
- Issue intake commit: `1280dfec2cfac67f70be65a2aa806f18bf982588`.
- Gate 1 refresh on 2026-09-07 still resolved to `a165091d93b687100dc7471bbf5b7dd5f9d4c1e9`.
- Result: upstream advanced, but authoritative identity and font hashes did not drift.

## Source Inventory

The machine-readable [source inventory](source-inventory.json) contains 39 acquired records and zero missing, byte-size, or SHA-256 mismatches.

### Authoritative identity masters

| Role | Contained source | SHA-256 | Byte result |
| --- | --- | --- | --- |
| Badge-less glyph for ink-background lockups | `brands/eso-weave/assets/source/eso-weave-glyph.svg` | `552f3203f0001b15e3adea9b720cb2f78be1427a12410f3e304170d973fef5ea` | Exact match to current upstream and intake |
| Badged universal mark and reduced candidate | `brands/eso-weave/assets/source/eso-weave-mark.svg` | `696d256c4ec0eae9aed315a1b489bbf5115ec33827e966a6e993708bf3f3109f` | Exact match to current upstream and intake |

### Fixed typography

| File | Measured metadata | SHA-256 |
| --- | --- | --- |
| `Inter-Regular.ttf` | Inter, Regular, 400, normal, static TTF | `529be850e06f62f8904f22bda77e45bde4834498fdbec4ff4201fa3177447a3a` |
| `Inter-Medium.ttf` | Inter, Medium, 500, normal, static TTF | `6df88fcb83ac96582350f801355c6eff55f15710093e9627fb431caa40521151` |
| `Inter-SemiBold.ttf` | Inter, Semi Bold, 600, normal, static TTF | `2de533bda937a063c595b07c6bd9b70c8c5087d0649a1c8330f7ac11fcc05602` |
| `OFL.txt` | SIL Open Font License 1.1 | `4d7d9c95e7d7f2f0ebf76d5e0b344826b74e903a34028ee18ab54bb639e45906` |

The current kit contract requires a mono role that upstream does not supply. Gate 1 proposes the repository's existing Geist Mono Regular 400 (`990f0e094fe02b8872429209c09abf4c03d22183c33c2a2ddb891dc7f086271c`) under the existing Geist OFL record (`942560b236adfa83745b2c64e5fc09ebaf91cb331751b1157eb92187e5d6e930`). It would be limited to code, values, and technical metadata.

### Path reconciliation

- Intake `docs/brand/ESO-Weave-Brand-v1.md` is now `docs/src/development/brand-standard.md`.
- Intake `docs/ESO-Weave-Specification.md` no longer exists as one document. The current `docs/src/` manual and `docs/project/` governance records supersede it.
- S020 acquired the current brand standard, README, responsible-use and input-safety guidance, five representative feature documents, `theme.rs`, `ui.rs`, reproduction instructions, all 10 named rendered references, and the complete S012 Spec Kit directory.

## Provenance Classification

- Public repository evidence proves the introducing commit, the S012 decisions, authoritative files, reproduction recipe, current brand standard, product voice, and legal boundary.
- The statement “The ESO Weave identity originated through the ShruggieTech brand-building system” is supplied by the repository owner through issue #153.
- The public commit history does not independently prove that service relationship. S020 will not claim that it does.

## Load-Bearing Character

- Two opposed monoline carets form one interwoven W-like symbol.
- Gold is the primary downward strand. Teal is the supporting upward strand.
- A short teal overlay segment creates the over-under crossing without a clipping path.
- Source centerlines, stroke widths, crossing order, rounded caps, and rounded joins are identity-bearing.
- The universal mark adds a 96-unit rounded ink square, 24-unit corner radius, dark vertical gradient, and restrained gold border.
- Upstream limits the badge-less glyph to ink backgrounds and uses the badged mark for arbitrary surfaces and small icons.

Measured glyph path bounds are `(24, 30)` through `(76, 74)`, with visual stroke bounds `(18.5, 24.5)` through `(81.5, 79.5)` at stroke width 11. The mark's badge visual bounds are `(1.4, 1.4)` through `(98.6, 98.6)` on its 100-unit square view box. Both sources remain centered and undistorted.

## Gate 1 Recommendations

The complete structured proposal is [gate-1-proposal.json](gate-1-proposal.json).

| Proposal | Transformation boundary | Measured difference | Recommendation |
| --- | --- | --- | --- |
| Reduced and platform mark | Embed the badged mark unchanged; resize proportionally and encode required containers | Zero source geometry, silhouette, aspect-ratio, and color change | Approve at 16 px and above |
| Horizontal lockup | Ink uses unchanged glyph; light uses unchanged badged mark; outlined Inter SemiBold wordmark is added | Source geometry and paint unchanged; only outlined wordmark and layout are new | Approve at 160 px and above |
| Stacked lockup | Same contextual source selection centered above the same wordmark, with visible source bounds fitted at 1.6 times the base proof size and transparent SVG margins normalized for placement | Source geometry and paint unchanged; only outlined wordmark, enlarged placement, and layout are new | Approve at 144 px and above |
| Wordmark-only | Outline exact `ESO Weave` text in Inter SemiBold with light tracking; ESO uses text color and Weave uses contextual gold | New geometry is limited to font-derived outlines required by the current contract | Approve at 120 px and above |
| Single-ink | Preserve centerlines, stroke widths, caps, joins, and silhouette; collapse both strands into one uninterrupted ink with no crossing overlay or knockout | Source silhouette and centerlines remain unchanged; paint roles collapse with no added geometry | Approve only at 32 px and above; use the color badge below 32 px |

No production SVG derivative, outlined wordmark, or source `brand.json` has been created. The displayed compositions are ignored raster proofs only.

## Palette Recommendation

- Source gold: `#F2B03C`, retained in authoritative artwork and dark identity roles.
- Source teal: `#2DD4BF`, retained in authoritative artwork and dark supporting emphasis.
- Deep gold: `#D18F22`, retained from the upstream dark standard.
- AA light-role gold: `#986000`, re-derived for 4.81:1 contrast on `#F7F5F0` rather than using upstream `#C6871F`, which measures only 2.80:1.
- Independent semantics: emphasis `#2DD4BF`, action `#986000`. No ShruggieTech house orange is inherited.
- Body pairs: `#E6EDF3` on `#0E1116` measures 16.00:1; `#14110B` on `#F7F5F0` measures 17.29:1.

Accessibility causes the only proposed palette deviation. It changes a derived light text and focus role, not the supplied SVG artwork.

Wordmark-only proofs are composited onto their declared surface before RGB export. This prevents transparent pixels from becoming an unintended black background and preserves the measured light-surface contrast pairing.

## Comparison Proofs

The renderer produced 40 exact contexts: five proposal families at 256, 64, 32, and 16 pixels on both `#0E1116` and `#F7F5F0`. Each overview isolates the two authoritative source files in a clearly labeled first row. Every subsequent row is one complete, non-production proposal containing no comparison image. The original paired layout was rejected because its unframed source and proposal reads as one duplicated lockup; it was replaced without changing any identity proposal.

| Sheet | SHA-256 |
| --- | --- |
| `dist/eso-weave-approval/gate-1/gate-1-overview-256.png` | `57c92ff6be46bf5285481a54e94b914d9b5ea77890286ed51af6792c2ddf90b4` |
| `dist/eso-weave-approval/gate-1/gate-1-overview-64.png` | `fcadcbc4d01151b73e1772f05ff917ff9c0a2e339826f6f4645eb5dc3ff95d2f` |
| `dist/eso-weave-approval/gate-1/gate-1-overview-32.png` | `77329a51cf933fea780353b7dd9f91cac1b2366aaad0a9c6f7bc186b27906946` |
| `dist/eso-weave-approval/gate-1/gate-1-overview-16.png` | `add094307fefb31310d29a341355b176818bebe12cbf6772379ec7a7b27063fa` |

The ignored manifest records every exact context and confirms `production_derivative_geometry_created: false`.

## Gate 1 Decision

Approved by the identity owner on 2026-09-07 after three proof corrections: comparison sources were isolated from proposal outputs, the artificial single-ink crossing overlay was removed, stacked visible-source placement was enlarged to 1.6 times the base proof size, and wordmark-only proofs were composited onto their declared surfaces. The approval binds the five named derivative proposals, canonical palette, AA light-role gold, Inter display and body roles, Geist Mono technical role, transformation boundaries, and authoritative SVG hashes recorded above. Post-review enforcement binds those derivative-producing settings to canonical SHA-256 `759802b32ea908c9f2585b76cdcd3943c4e0e3175c2437ab315679863ebeea58` and requires the approval scope to name all five generated families.

## Private Kit Verification

The private kit was built with `.venv\\Scripts\\python.exe scripts/build_all.py eso-weave`. The corrected build produced 285 files and completed with zero verifier problems, zero glyph failures, zero affiliation-scan problems, zero image-QC problems, zero PDF-QC problems, and zero pagination problems. The four glyph warnings identify unchanged imported SVG elements and their declared provenance boundary; they are not failures or waivers.

The focused approval, legal-boundary, source-inventory, and brand-contract suite passed 35 tests. The publication projection suite passed 26 tests. The complete pipeline suite passed 45 tests, including the production ESO Weave regression that requires exactly one source image per horizontal and stacked lockup, two uninterrupted paths in the single-ink mark, the approved `#14110B` plus `#986000` light wordmark pairing, and byte-complete derivative provenance.

Visual inspection covered the full logo comparison sheet, desktop and 390 px guideline views, desktop and 390 px UI-specimen views, and the seven-page PDF contact sheet. The corrected outputs contain no duplicated visible marks, no synthetic single-ink crossing segment, no clipped wordmark, and no illegal light-surface wordmark pairing.

The deterministic source-inventory validator checked all 39 records against the repository with zero missing files, duplicate identifiers, duplicate contained paths, byte-count changes, or SHA-256 changes.

Running `.venv\\Scripts\\python.exe scripts/prepare_site.py` while Gate 2 remained pending prepared the existing five kits and nine reference documents. `site/public/brands/eso-weave` remained absent, and no ESO Weave entry appeared in public site source, data, or registry output.

## Gate 2 Packet

The ESO Weave upstream `main` reference was refreshed immediately before Gate 2 and remained `a165091d93b687100dc7471bbf5b7dd5f9d4c1e9`. The authoritative glyph and mark hashes therefore remain identical to the Gate 1 bindings.

The ignored packet at `dist/eso-weave-approval/gate-2/` contains the rendered derivative comparison, guideline views, UI specimen, PDF contact sheet, portable guidelines, complete brand guide PDF, source inventory, approval ledger, derivative provenance, kit manifest, verification report, and exact publication-surface record. Its derivative provenance SHA-256 is `f99e01a666f9242457742467aeeebd308aae37f8411f32fc52186e2c3f1516c4`; its corrected private-kit manifest SHA-256 is `510063e4489dccdaeea39af18f39323082711493f9bbe85a85485445a3fa0105`.

Gate 2 proposed these exact generated public surfaces: `showcase-card`, `brand-landing-page`, `guideline-topics`, `downloads`, `registry-endpoints`, `public-metadata`, `structured-data`, and `social-preview`. No source repository evidence, historical S012 file, raw approval ledger, or private review packet will be published. First-round review identified that the approved provenance manifest bound source identity and transformation labels but not derivative bytes. The provenance manifest now records and verifies every derivative SHA-256. A separate deterministic approval manifest binds every exact SVG master hash and every PNG to its verified SVG rendering source, avoiding platform-specific PNG encoding drift while covering the full derivative set. The rendered derivative files did not change.

### Product-language correction

The first Gate 2 presentation was rejected because its generic workflow-manager framing did not describe ESO Weave. The correction uses the official repository description, current README, documentation home, scope and platform model, game-observation model, feature index, and live-interface reference. The owner selected “Unofficial automation for ESO” as the public slogan and “Cross-platform desktop companion for The Elder Scrolls Online” as the public description. Supporting copy covers the actual offline-first companion; focus-scoped combat weaving; PixelBeacon-assisted fishing and Auto Potion; live status; and the explicit boundary against reading game memory or network traffic. The invented workflow, character, run-history, and daily-writ concepts were removed from the UI specimen and source contract. The corrected packet was regenerated and approved.

## Gate 2 Decision

Approved by the identity owner on 2026-09-07 after the product-language correction. The decision is bound to deterministic derivative approval manifest SHA-256 `86ead2c4f4dae3d065045db4cbe292db8ee05cf8fad7a5b819a6610bce6c906b`, the corrected slogan and description, and these exact surfaces: `showcase-card`, `brand-landing-page`, `guideline-topics`, `downloads`, `registry-endpoints`, `public-metadata`, `structured-data`, and `social-preview`. The post-review manifest strengthening changed only approval metadata, not any owner-reviewed derivative byte. Publication of the raw source inventory, historical evidence, approval packet, or approval ledger remains unauthorized.

## Final Publication and Validation

After Gate 2 approval, site preparation produced six public kits and nine reference documents. ESO Weave appears through exactly the eight approved surface classes. Verification revalidates `logos/provenance.json`, including every derivative content hash and its complete correspondence with `logos/approval.json`; publication binds the deterministic approval manifest. Negative regression tests prove that changed derivative bytes, a stale approval-manifest hash, or incomplete surface approval suppresses the public projection.

The public wording is exactly “Unofficial automation for ESO” and “Cross-platform desktop companion for The Elder Scrolls Online”. Desktop and mobile inspection covered the ESO Weave landing page in light and dark themes and the six-card home page. The final layouts preserve one mark per lockup, the approved contextual mark treatment, legible status rows, and the AA light-role gold.

The complete local matrix passed 34 glyph-kit checks, 2 package-release checks, 13 release-contract checks, 26 site-preparation checks, 35 brand-contract checks, 14 icon-kit checks, 45 pipeline tests, Markdown validation, six clean production-kit builds, site lint, a 76-page static production build, and 71 desktop-and-mobile HTML route checks with zero WCAG 2.1 AA violations. The ordinary local Turbopack build encountered a Windows process-spawn `Access is denied` error; the equivalent Next.js webpack production build completed successfully, and hosted Linux CI remains the authoritative canonical-build result.

Spec Kit cross-artifact analysis mapped all 25 functional requirements and 9 success criteria across the 51 implementation tasks. It found zero CRITICAL or HIGH inconsistencies, ambiguities, or coverage gaps.

Repository hygiene confirmed the authoritative glyph and mark SHA-256 values remain unchanged, generated kits and site exports are ignored, `.specify/feature.json` is untracked, committed text is UTF-8 without BOM using LF line endings, and no mojibake marker is present.
