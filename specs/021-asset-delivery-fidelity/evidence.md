# Evidence: Asset Delivery Fidelity

## Baseline

- Branch: `codex/021-asset-delivery-fidelity`
- Scope: GitHub issues #166 and #165 only.
- Glitchpad full-path canonical JSON SHA-256: `2b636e5423084ee495d0e958bbbf564f5f62b4f0b59408f880d96d5f97977664`
- Glitchpad reduced-path canonical JSON SHA-256: `5c2840d897bee48fca6cef103ddb64d28df9eda0c605118bf694b2d113c684cd`
- Pre-fix comparison-set logo-delivery manifest SHA-256: `576de12e876c20f735c81a78359eeb0531239ab8954a5eeb5f10ebd51c741dd4`. This early comparison set excluded the four reported lockups but still included standalone monochrome square derivatives affected by the same shared mask correction, so it is not used as presentation-only stability evidence.
- The pre-fix Glitchpad production build reported zero verifier problems despite the visible defect.
- At 1024 px delivery width, each horizontal black/white mark occupied only 37 pixels vertically (`y=28..65`) inside its mark region. Each stacked black/white mark occupied only 102 pixels vertically (`y=53..155`) inside its mark region.
- Visual inspection of `glitchpad-horizontal-white-1024.png` confirmed that only the square's top strip and page-fold fragment remained beside the wordmark.
- Root cause: the square-knockout mask declared `maskUnits="userSpaceOnUse"` without explicit local `x`, `y`, `width`, `height`, or `maskContentUnits`. The default percentage mask region resolved against the outer lockup viewport and clipped the nested 1000-unit square construction.

## Test-First Record

- The focused square-enclosure regression failed before implementation because every black and white mark, horizontal lockup, and stacked lockup omitted `maskContentUnits` and explicit local mask bounds.
- The existing static site contract failed before implementation because neither asset cards nor guideline logo examples exposed a shared `asset-preview-media` boundary.
- Negative regressions cover a missing mask-region declaration, an undersized mask extent, a missing mask reference, rendered mark collapse, preview overflow, off-center artwork, and divider overlap.

## Corrected Output

- Every square-knockout mask now declares `maskUnits="userSpaceOnUse"`, `maskContentUnits="userSpaceOnUse"`, and the explicit local region `0 0 1000 1000`.
- At 1024 px delivery width, corrected horizontal black and white marks extend from `y=28` through at least `y=230` in the isolated mark region, compared with only `y=28..65` before correction.
- At 1024 px delivery width, corrected stacked black and white marks extend from `y=53` beyond the `y=260` inspection crop, compared with only `y=53..155` before correction.
- Visual inspection confirmed that the white horizontal and stacked deliveries contain the complete square, paper-and-G construction, and wordmark. Black deliveries use the same measured mask geometry and pass equivalent alpha-bound assertions.
- The Glitchpad production build reports zero verifier problems and zero glyph failures.
- Source path hashes remain `2b636e5423084ee495d0e958bbbf564f5f62b4f0b59408f880d96d5f97977664` for Full and `5c2840d897bee48fca6cef103ddb64d28df9eda0c605118bf694b2d113c684cd` for Reduced.
- Asset cards and guideline logo examples now use the same bounded `asset-preview-media` wrapper and exact existing preview URLs.
- The complete generated `dist/` tree SHA-256 remained `de8acbf86a11bb0ee24eb77a3661e5d6a16ab05315fa43bb2555f105c725d67c` before and after site preparation, proving that the presentation-only projection changed zero delivery bytes.

## Full Validation

- `skill/templates/test_pipeline.py`: 45 tests passed.
- Glyphkit: 34 checks passed; package-release: 2 tests passed; release-contract: 13 tests passed; prepare-site: 26 tests passed; brand-contract: 35 tests passed; iconkit: 14 tests passed.
- Markdown prose line policy passed.
- All six production kits rebuilt with zero reported problems and zero glyph failures.
- Site type-check and 76-page static export passed.
- Browser verification covered 71 HTML routes plus all-brand preview measurements at 360, 768, and 1280 pixels, both themes, and 200 percent zoom with zero WCAG 2.1 AA violations.
- The first hosted Python 3.8 run exposed a test-harness capability error: the new regression declared raster support even though the minimum-version job intentionally does not install the Node rasterizer. The test now runs the real capability probe, always verifies SVG structure, and performs rendered PNG assertions only when an SVG renderer is actually available. The focused regression passes locally at full capability and remains valid at the core tier.
- First-round Codex review requested required-geometry comparison and observation of computed preview presentation. Generated lockups now declare mark and wordmark component boundaries; verification compares monochrome mark paths with the governed source geometry and wordmark paths with the generated wordmark master. Browser verification now checks the actual image/media boxes plus computed `object-fit`, `object-position`, and transform state before measuring content containment and centering. Missing-mark and missing-wordmark regressions, the Glitchpad build, and the complete browser matrix pass after these changes.
- The authorized second and final Codex review requested transform-aware lockup validation and portable raster comparison. Verification now re-derives horizontal and stacked component transforms, canvas dimensions, scaling, and placement from the declared lockup contract, rejecting collapsed marks and off-canvas wordmarks. Cross-backend SVG-to-PNG comparison now allows only one-pixel antialiasing-edge variance while requiring matching dimensions, visible bounds, coverage, and mutually dilated alpha topology. Focused transform and raster-equivalence regressions pass, and Glitchpad again builds with zero verifier problems.

## Hygiene

- Generated kits, public copies, static exports, test screenshots, and local Spec Kit state remain ignored.
- The final 21-file source and Spec Kit set passes UTF-8 decoding, has no BOM, uses LF line endings, and contains no mojibake indicators.
- `git diff --check` passes and no generated kit, site export, raster, PDF, registry, release archive, or `.specify/feature.json` appears in the tracked change set.
