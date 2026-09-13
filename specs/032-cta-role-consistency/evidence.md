# Verification Evidence: CTA Role Consistency

## Baseline

Recorded on 2026-09-13 from `main` commit `6b018b912b34226e3360eb5e31ea65b31c396f45` before implementation.

- The generated portable guide publishes `--brand-cta: #C5342C` in both theme scopes, but `.btn-primary` consumes `--primary` and `--primary-foreground`. The three primary specimens therefore render blue instead of the declared CTA red.
- The generated PDF is eight pages. Extracted text contains no `#C5342C`, while page 4 labels the section and semantic table with British English and omits the CTA swatch, foreground, and state contract.
- Visual inspection of baseline page 4 found no clipping or corruption. It confirmed that the palette shows identity blue, emphasis blue, and destructive red without the separate CTA red role.
- Baseline SHA-256: `54e4279867259302bc215bc0b1279b519713a1a3b40b3b786dff6403819d82f9` for `dist/i-heart-pr-tours/brand-guide.pdf` and `da90abde5afe1d2f5c920cf3d560f7849b2ed1bfe71b04577633e00534b9eb79` for the portable guide in `site/out/`.
- The seven governed logo source hashes match the approval ledger: heart submark `c341b9d3f61f9037b5007b459b87cb91ac452cfd58769c021d67bd323a7ef148`; horizontal dark `2f50fcafa8a422ad0271e583108b79e4ace6065445b0f4615d96fa8f822ab7f3`; horizontal light `9334768b68e3c3d1dace13088c8a8cb2f6ac29c6f288c602029c52cd10d9e969`; horizontal sand `7e117230b1605e5bc023a5157758429c7fc1a5ac6486f523de0eb2e4bb48c7d6`; vertical dark `bcd03c0784b442a2c38836f9b2e6c312149a9cc1bddd3c1480fae28ea9b5f045`; vertical light `7da9be465100e91cd0cc82019e1b2afcfc7e734ff6e11a53fd23675ef2dbed80`; vertical sand `f53fc580aaab858cb1e1bef2ff4bdd0f635959d39e96827d7add9f703a5cc04b`.

## Repository Boundaries

- `.gitignore` excludes `dist/`, `site/out/`, generated site inputs, Python caches and bytecode, Node dependencies and build caches, Playwright results, release output, environment files, and editor state.
- `.specify/.gitignore` and the root ignore file exclude machine-local `.specify/feature.json`.
- PDF render evidence is stored below ignored `dist/`, so no generated PDF, raster, site export, or temporary QA output can enter the commit.

## Test-Driven Implementation

- The first focused run executed four new generator tests. It failed exactly at the absent contract: one error for missing `brand-cta-foreground`, one failure for the portable buttons still consuming identity `primary`, one failure for missing PDF CTA semantics and states, and one failure for British reader-facing prose.
- The portable browser verifier now measures all three specimens at computed-style level. It requires exact `rgb(197, 52, 44)` fill, white measured foreground, default border parity, hover border and movement cues, active inset cue, dual-tone keyboard focus, retained reduced-motion cues, and a WCAG 2.1 AA axe pass.
- No production source was changed before the expected-red regression run.
- The secondary-action amendment began with a focused regression that failed at the missing `brand-cta-outline-foreground` token. Measured source values confirmed `#C5342C` at 5.38:1 on white and 3.48:1 on the dark `#08131D` surface, so the contract retains the red outline in both themes while selecting white text on dark and red text on light.

## Generated Artifact Review

- The regenerated I Heart PR Tours kit reports zero verifier problems and zero glyph failures. PDF QC reports zero problems, and pagination reports zero split elements across eight pages.
- Page four now shows `brand-cta` as `#C5342C`, white filled-control text, the primary default, hover, active, and focus-visible specimens, and a labeled secondary red-outline specimen. The role boundary now states that CTA red fills primary actions and outlines secondary actions.
- The portable guide shows filled-red primary and red-outline secondary actions in both theme wells and Type and components. Computed defaults are transparent with `rgb(197, 52, 44)` borders; text is white on the dark `#08131D` surface and CTA red on light surfaces.
- A first PDF build with the new secondary specimen detected page four touching the bottom trim. The specimen grid was compacted, then rebuilt to zero PDF QC problems without removing any state or role guidance.
- The complete site browser verifier checked 76 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. Secondary checks cover exact default, hover, active, focus-visible, reduced-motion, and computed contrast behavior.

## Full Validation

- All eight production kits rebuilt with approved identity proofs and reported zero verifier problems, zero glyph failures, zero PDF QC problems, and zero pagination splits.
- The Python glyph, publication, package, release-contract, site-preparation, identity-continuity, brand-contract, icon, generator, and Markdown suites passed. Two initially reported pipeline failures were diagnosed: one test process used Node v24.11.1 instead of the record-bound v24.11.0 renderer, and the new I Heart-specific PDF block had been projected into a compact generic client guide. The renderer test passed with the record-bound runtime, and the PDF block was scoped to I Heart PR Tours; both affected regressions then passed.
- The production site compiled, passed TypeScript, and generated 81 static pages. Twelve origin and payload contract tests passed.
- The complete browser verifier checked 76 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- Publication audit found exactly eight governed kit markers and eight governed site markers.

## Final Hygiene

- `git diff --check` passes, all S032 tasks are complete, and no generated kit, site export, release archive, PDF, raster, dependency directory, or machine-local feature selector appears in Git status.
- The I Heart PR Tours source is 19,484 bytes with SHA-256 `da5bbe93ac85b8b19e8e0bbc5f51075d32647b04871fdec2df681bc4373ac49f`; the continuity record recomputes to its stored digest `bd86a13ac69032fe4ccbb8c95f07f001c734758f47d03e7b5596cda6c4732784`.
- Authored files are UTF-8/LF, the changed reader-facing sources contain no detected mojibake, and generated outputs remain ignored.
- The working tree is intentionally uncommitted pending the owner's visual approval. No push has occurred.
