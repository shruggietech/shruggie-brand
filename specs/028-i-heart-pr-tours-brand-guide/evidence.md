# Verification Evidence: S028 I Heart PR Tours Brand Guide

## Gate 1 intake

**Recorded**: 2026-09-10

**State**: Gate 2 candidate `iheartpr-g2-r4` is approved with a private, zero-public-surface classification. Authorized repository publication and bounded review are in progress.

- Branch: `codex/028-i-heart-pr-tours-brand-guide`
- Issue: #188
- Synchronized baseline: `435019dbc37e754fd1f0b16228a576c985e9468a`
- Dependencies: S027 issue #185 and authoritative-logo issue #151
- Spec Kit prerequisites: passed; `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, and `tasks.md` are present.
- Requirements checklist: 16 of 16 requirements-quality items pass.
- Reviewer intake checklist: 0 of 35 reviewer-owned decisions are checked. These remain open until the owner approves one exact Gate 1 revision.
- Production source boundary: `brands/i-heart-pr-tours/` is absent.
- Generated review boundary: `.specify/feature.json` and `dist/` are ignored.
- Private path boundary: committed specification prose contains no workstation input path.
- Intake scope: the explicitly supplied Brand Assets ZIP contains 68 safe entries, including seven SVG identity sources, two PDF references, redundant PNG and favicon exports, and three font bundles.
- Archive SHA-256: `e37283c40cd40955f96a6d888a40aa4bfed56ab1400bf8ca1542d1f682d26154`.
- Package inventory SHA-256: `d25e01be417db197d883d2fbca0532517f322f615aace49b6276c7bd63a63949`.
- Authority disposition: exact SVGs are proposed as production masters. PNG, favicon, guide, and logo-PDF files remain lower-authority private evidence.
- Passive-SVG result: every source contains zero active or external references and renders successfully with the production resvg adapter. A narrow self-contained PNG data-URI allowance is proposed because source rewriting is prohibited.
- Typography result: supplied OFL bundles bind exact Poppins Bold, Source Sans 3 Regular and Semibold, and Courier Prime Regular candidates.
- Review contact sheets: package overview and unchanged SVG renders were generated under ignored `dist/i-heart-pr-tours/gate-1/`.
- Gate 1 decision packet: exact candidate `iheartpr-g1-r2` was generated under ignored `dist/i-heart-pr-tours/gate-1/`, explicitly approved, and later invalidated by the rejected Gate 2 revision request.
- Gate 1 manifest SHA-256: `aafbbfaf255aafd59154e9d7cbb393a79020cc1e905cde3b192f33db3ba3898b`.
- Package contact-sheet SHA-256: `0b29bcc49e0da1c61bb2e5772a6210227975aae872d2eb3672f1c7dd0e58254a`.
- SVG contact-sheet SHA-256: `c35cd0802fd907a877341f22b55df138a92693dfc247e4ef4af4f0e5e7faa2e1`.
- Palette measurement SHA-256: `d555e3bd5af4c6bb59dc539762aec14f4362f0a25f83995eced7594a4924c4fa`.
- Context evidence SHA-256: `cb8a5badc462e3d090b42686db6f5629725fcefbd1e974c62eae7d48d860faa4`.

## Cross-artifact analysis

The pre-implementation analysis found no critical conflict among the specification, plan, research, data model, contracts, quickstart, and tasks. At that time all 25 functional requirements and 10 measurable outcomes had an implementation or verification path. The 2026-09-11 rejection adds FR-026 through FR-031, and live favicon verification adds FR-032. Cross-artifact analysis reopens after revised Gate 1 implementation. Candidate `iheartpr-g1-r4` binds the changed copy, palette, surface mode, transformation, expressions, favicon and app-icon authority, source hashes, and private publication state.

## Halt record

T016 completed when the repository owner answered `Yes. Continue.` to the exact candidate approval request on 2026-09-11. The response binds candidate `iheartpr-g1-r2` and its pre-approval manifest SHA-256 `aafbbfaf255aafd59154e9d7cbb393a79020cc1e905cde3b192f33db3ba3898b`. Production ingestion and private derivative generation are now authorized. Commit, push, pull-request publication, and every public brand surface remain prohibited until Gate 2 approval.

## Implementation red baseline

The first focused authoritative-source test failed as expected on 2026-09-11. `test_authoritative_colourways_and_supplied_lockups_bind_exact_sources` raised `KeyError: 'full_colourways'`, proving that the pre-S028 contract could not bind supplied per-surface full marks or supplied horizontal and vertical lockups. This is the narrow generator and contract gap addressed by T025.

## Gate 2 implementation and verification

**Recorded**: 2026-09-11

- Approved-source promotion completed with canonical source binding `d24c57abc4ad831cc9300e2e5ac8421cb6e533cb5ce473ecdda8ff3ce39059aa` and continuity record digest `da3bf1534cfbf40b05c37c5bd6c6bcb398bfa51053c19b6b3affdda3774c6e56`.
- All seven approved source SVGs and four approved font files match their Gate 1 SHA-256 values after promotion.
- The authoritative contract now accepts multiple supplied lockups, per-colourway full sources, an explicit derivative-family omission ledger, and strictly self-contained base64 PNG data inside otherwise passive SVGs.
- The generator emits eight exact-source SVG derivatives: dark and light vertical marks, dark and light stacked lockups, dark and light horizontal lockups, and the unchanged heart for both reduced surface labels. Wordmark-only, white, black, and monochrome masters are not generated.
- Deliberate implementation deviation: approved SVG files are copied directly into SVG delivery slots instead of being nested inside new SVG wrappers. The wrapper approach changed renderer behavior for the embedded Canva PNG content and was weaker than direct byte preservation. Direct copying preserves every source byte and is independently asserted by regression tests.
- Deliberate palette qualification: black and ink-neutral UI surfaces replace identity-blue canvas roles where supplied light blues or fixed red failed WCAG 2.1 AA. All eight supplied identity colors remain governed legacy palette values, and the guide prohibits failing text and control pairings.
- Focused suites pass: 44 brand-contract tests, 20 identity-continuity tests, 15 icon-suite tests, 53 pipeline tests, and 30 site-preparation tests, for 162 passing tests total.
- The private production build is clean: 0 verifier problems, 0 glyph failures, 0 affiliation problems, 0 image-QC problems, 0 PDF-QC problems, and 0 pagination problems.
- Visual inspection passed for the logo sheet, desktop and 390px guide views, seven-page guide contact sheet, typography specimen, and the complete 256/64/32/16 pixel continuity proof matrix. The diagnostic full lockup becomes unreadable below its 96px declared minimum, as expected, while the approved reduced heart remains recognizable at the smaller sizes.
- Public exclusion is regression-tested. The affiliation remains independent third-party and private, Gate 2 surfaces remain empty, and public showcase, registry, hosted guide, release, deployment, and service credit remain disabled.
- Gate 2 candidate: `iheartpr-g2-r1`.
- Gate 2 manifest SHA-256: `71e6e7da062cd69a314b4c5ae82e596e1c8799da0eb2c79a6cea72dd02f6891c`.
- Gate 2 derivative manifest SHA-256: `0576fe9bed192560875802a7a194f6b157b1c9edbec492cc0b20b36898d3272d`.
- Gate 2 provenance SHA-256: `7c8827361de370c3f1e411735e1b70e2ba5cff6177b7adaade06849787ec7e9c`.

## Gate 2 rejection and revised Gate 1

T038 completed with rejection on 2026-09-11. The owner required exact replacement copy, a palette grounded in the live site and supplied brochures, a white-paper light guide, deterministic black and white variants, and inclusion of the supplied sandy compositions. These changes affect copy, color, surface mode, and transformation scope, so FR-018 invalidates the affected `iheartpr-g1-r2` approval and returns S028 to Gate 1. No commit, push, pull request, registry entry, hosted guide, release, deployment, or public showcase work has begun.

### Context and diagnosis

- Exact revised slogan: `Experience Puerto Rico`.
- Exact revised description: `Thoughtfully guided tours on the island we love.`
- Live-site computed values: white `#FFFFFF`, ink `#111111`, muted ink `#555555`, action red `#C5342C`, support blue `#1C5B8D`, sky `#68A9DD`, and pale sky `#A1CFF4`.
- Both owner-supplied brochure masters independently quantize to dominant `#1C5B8D` or `#1C5B8E` fields and earth clusters at `#5A4A4A` and `#5D4A46`. Revised Gate 1 selects `#5D4A46` for the occasional brown support role.
- Contrast on white: ink 18.88:1, muted ink 7.46:1, red 5.38:1, blue 7.17:1, brown 8.29:1, sky 2.53:1, and pale sky 1.65:1. The lighter blues are decorative or require a compliant dark foreground.
- The brochures support a warm, local, specific, and unhurried voice organized around heartfelt tours, expert local insight, thoughtful guidance, discovery, island stories, and memorable photography.
- Root cause for the light-theme failure is systemic: PDF generation hard-codes full-bleed dark pages and dark tokens, portable guidelines force a dark body, the hosted site forces a dark root, and brand-card descendants retain dark-biased styles. Issue #193 records the reusable fix.
- Root cause for missing sandy content is also systemic: schema, generator, site-copy, and guide-topic contracts enumerate fixed technical families without an optional expressive or mood-art family. Issue #194 records the reusable fix and future digital-brand artwork path.
- Literal recoloring of every opaque source pixel retains the supplied raster shadow and fills the white star and stripes. Candidate r3 instead suppresses the shadow, converts near-white details into transparent knockouts, and recolors the remaining visible pixels to exact black or white. The review proof retains the heart contour, star, stripes, letterforms, and clean antialiasing without tracing or source mutation.
- The live page declares `favicon-32x32-1.png` for 32 × 32 favicon, nominal 192 × 192 favicon, and Apple touch roles. The original live bitmap has SHA-256 `8ceee25ac489c10f99a7530685fbe914cf2d93e9b72ba4416edd1c69a6476e1d`, dimensions 32 × 32, and visible bounds `(2, 3, 30, 30)`.
- The supplied package's `favicon-32x32.png` has SHA-256 `008c8f1b9cc7fa1bd380baa6371f16dec075fa97dd755dbf2f19349c91ba5c9c`, dimensions 32 × 32, visible bounds `(1, 3, 31, 30)`, and only 0.6764 mean RGB error from the live optimizer output after white compositing. The rejected Gate 2 generated favicon differs by 37.7393 and occupies the entire 32 × 32 alpha bounds, proving its framing was wrong.
- Candidate `iheartpr-g1-r3` was superseded before approval. Candidate `iheartpr-g1-r4` binds exact supplied colored-heart favicon and platform targets where available and a measured safe-area transform from unchanged `heart.svg` for missing modern sizes. Monochrome substitution is prohibited for app-icon and favicon roles.

### Revised candidate evidence

- Candidate: `iheartpr-g1-r4`.
- Candidate JSON SHA-256: `b9227a150963b9736b2998f8fffde5d5f119b1f97de5f0be8e60f9ee2fad3759`.
- Candidate manifest SHA-256: `6b25b935b9e8420463f4e56c102e16d8da31dcd2ef729602a051db30debd72be`.
- Direction board SHA-256: `2faf1dad9ba27035f94c41aca6e2e4f6e01ea7438ec67493f7ab5256916f55db`.
- Monochrome proof SHA-256: `a6aee4a0f3184aaddf0d9a3cb6d92fe3a1c300f0577416ab34a45a589932b567`.
- Expressions preview SHA-256: `1ed9f3c1695a5d8b79a1fb4a26e6b4a13f2ea10e734637d36e12eb8aa02dde29`.
- Favicon proof SHA-256: `ce5da11774e4c4977d7d3a8c854879399b95ef7197fc7917fea2e3e5944aa840`.
- Light-theme issue: #193, `https://github.com/shruggietech/shruggie-brand/issues/193`.
- Custom-assets issue: #194, `https://github.com/shruggietech/shruggie-brand/issues/194`.

T044 completed when the repository owner answered `looks good. continue` to the exact `iheartpr-g1-r4` approval request on 2026-09-11. The response binds manifest SHA-256 `6b25b935b9e8420463f4e56c102e16d8da31dcd2ef729602a051db30debd72be` and authorizes revised production implementation. Commit, push, pull-request publication, and every public brand surface remain prohibited until revised Gate 2 approval.

## Revised Gate 2 implementation and verification

**Recorded**: 2026-09-11

- Candidate `iheartpr-g2-r2` implements the exact slogan `Experience Puerto Rico` and description `Thoughtfully guided tours on the island we love.`
- The guide declares `light` surface mode and renders as an eight-page white-paper document. The portable guide is light-first at desktop and 390px widths.
- The approved action red is `#C5342C`, the supporting blue is `#1C5B8D`, the occasional brown is `#5D4A46`, and light surfaces are governed by `#FFFFFF`, `#F8F6F2`, `#EEF4F8`, `#111111`, and `#555555`. Lighter sky values remain decorative with governed dark foregrounds.
- Color and light logo files preserve approved source bytes. Black and white files are generated by the approved shadow-suppressed, knockout-aware transform and retain the heart silhouette, star, stripes, lettering, and transparent negative space.
- The exact supplied colored-heart favicon files replace matching generated targets byte-for-byte. Missing modern sizes use the same reduced heart with declared framing. Transparent web icons are an explicit IHPRT-only contract, and monochrome platform substitution remains disabled.
- The supplied vertical and horizontal sandy compositions appear in the optional `Expressions and atmosphere` section with guidance that they do not replace the core logo masters.
- Deliberate scope correction: transparent favicon generation is opt-in so existing brands keep their plated web-icon behavior. This prevents the client-specific source treatment from leaking into other brand kits.
- Deliberate private-boundary correction: public registry validation now runs only after public eligibility is established. A private client brand is buildable without inventing a registry endpoint, while all public brands remain fully validated.
- Focused suites pass: 46 brand-contract tests, 20 identity-continuity tests, 16 icon-suite tests, 54 pipeline tests, and 30 site-preparation tests.
- Repository-wide suites pass: 34 glyphkit checks, 5 package-release tests, 14 release-contract tests, and 4 continuity-audit tests.
- All eight production brand kits complete with zero verifier, glyph, affiliation, image-QC, PDF-QC, and pagination problems after the cross-brand source-icon distinction was corrected and Fragcap was rebuilt.
- Site lint, TypeScript, static production build, and browser verification pass. The browser verifier covered 68 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. IHPRT remains absent from the seven-kit public route inventory.
- Visual inspection passed for the eight-page PDF contact sheet, the colored logo sheet, desktop and mobile portable guide, exact favicon sheet, typography page, sandy expressions page, black and white derivative proof, and the 256/64/32/16 continuity matrix.
- The kit verifier reports 0 problems, the identity continuity record is source-bound, and `git diff --check` passes.
- Revised Gate 2 packet: ignored `dist/i-heart-pr-tours/gate-2-r2/`.
- Revised Gate 2 packet manifest SHA-256: `a8b887f5b3f265e96b4e8f4e7ab587f3d56eeaff2d9dce214f7120dc970869c2`.
- Kit manifest SHA-256: `2d4fe839ade75cc3d2aa91ae87fe13166335717e2f9d2e1457efbd7cf089f496`.
- Logo provenance SHA-256: `9721f26fdc7757324c41f486aec45aa5bdf6581cd4991b24b0f07fdcdd2e91af`.
- Icon manifest SHA-256: `c0e403a9ef36dbff74cf2d410d427f9adb342d6e7992a7978e861c3d7a36477d`.
- Publication classification is private with zero public surfaces. Showcase, hosted guide, registry, release, deployment, public metadata, structured data, and social preview remain disabled.

Candidate `iheartpr-g2-r2` was superseded by the owner's focused typography revision before Gate 2 approval. No commit, push, pull request, public surface, or release action began from that candidate.

## Gate 2 typography revision

**Recorded**: 2026-09-11

- The owner accepted the rest of candidate `iheartpr-g2-r2` and requested one focused correction: remove preformatted Courier Prime styling from section labels and table row or column headings.
- Computed live-site styles use Poppins at weight 700 for most primary H2 and H3 headings, usually in `#111111`. Supporting text uses Source Sans Pro, and occasional uppercase eyebrow labels use `#1C5B8D`.
- The corrected delivery uses the already approved and supplied Poppins Bold for primary headings and Source Sans 3 Semibold for section labels, table headings, key labels, surface labels, and badges. Courier Prime remains limited to code-like values, file paths, identifiers, and measurements.
- The focused regression first failed on the missing semantic font contract, then passed after the PDF and portable guide generators were corrected. The full pipeline suite passes 55 tests.
- All eight production kits rebuilt cleanly with zero verifier, glyph, affiliation, image-QC, PDF-QC, and pagination problems. The I Heart PR Tours verifier reports 0 problems and its glyph validator reports 0 failures.
- Visual inspection passed for the revised eight-page contact sheet, full-size typography page, desktop and 390px portable guide, logo sheet, and colored-heart favicon sheet. Headings and table labels are legible at rendered size, and no approved logo, palette, copy, expression, favicon, or publication value changed.
- Revised Gate 2 packet: ignored `dist/i-heart-pr-tours/gate-2-r3/`.
- Revised Gate 2 packet manifest SHA-256: `d8b69b1a0a6086c43d29e5a3655141a7dfb5d33dc564647e68313578639c1b4d`.
- Kit manifest SHA-256: `cac7ea72110617a0ae42674fafc2fd8fab90a786a6b4bfc12b76493b204f7a51`.
- Logo provenance SHA-256: `9721f26fdc7757324c41f486aec45aa5bdf6581cd4991b24b0f07fdcdd2e91af`.
- Icon manifest SHA-256: `c0e403a9ef36dbff74cf2d410d427f9adb342d6e7992a7978e861c3d7a36477d`.
- Publication classification remains private with zero public surfaces.

T050 remains the active halt. No commit, push, pull request, public surface, or release action may begin until the repository owner explicitly approves candidate `iheartpr-g2-r3` and manifest SHA-256 `d8b69b1a0a6086c43d29e5a3655141a7dfb5d33dc564647e68313578639c1b4d`, including the private publication classification.

## Gate 2 small-text, shorthand, and preview-surface revision

**Recorded**: 2026-09-11

- Candidate `iheartpr-g2-r3` was superseded before approval after the owner identified remaining Courier Prime use in the footer, page numbers, and cover metadata, requested exact footer wording, requested `IHPRT` shorthand guidance, and reported two apparently incomplete page-3 previews.
- Root cause of the page-3 previews was a surface mismatch. The first two authoritative assets contain white lettering for dark surfaces, but the guide placed them on white cards, so only their colored hearts remained visible. Candidate r4 preserves the source files unchanged and assigns dark preview wells to those two assets.
- The footer now reads exactly `I Heart PR Tours | Brand System`. Footer text, page numbers, the cover eyebrow, cover metadata, section labels, table headings, keys, measurements, and other small semantic roles use Source Sans 3. Poppins remains the display and major-heading family.
- Courier Prime is now reserved exclusively for literal code blocks. The `Load the system` command block retains its previously approved regular 400 weight and sizing. The portable guide contains no Courier Prime styling because it contains no literal code block.
- The written-form contract permits `IHPRT` for casual shorthand and general prose after the full name is established. It prohibits using `IHPRT` as a substitute logo or altering supplied identity artwork.
- The regression sequence demonstrated meaningful failures for the stale written-form contract, lingering small-text mono styling, and missing dark preview wells. The corrected focused tests pass, followed by all 56 pipeline tests.
- The `brand.json` prose addition changed only source metadata bytes. The continuity record was refreshed to digest `eb59efbe64941498eb73048ccf085a987ff964dc87abeff9852028a3a952f215`; the approved identity snapshot, source artwork, topology, framing, palette, and Gate 1 proposal digest remain unchanged.
- All eight production kits rebuild cleanly with zero reported verifier, glyph, affiliation, image-QC, PDF-QC, or pagination problems. The I Heart PR Tours kit contains 434 manifest entries, its verifier reports 0 problems, and its glyph validator reports 0 failures.
- Visual inspection passed for all eight PDF pages, the complete contact sheet, logo sheet, favicon desktop and mobile sheet, and portable-guide desktop and 390px sheet. The first two page-3 lockups are fully visible and centered on their dark wells, and the literal page-8 command block remains correctly monospaced.
- Revised Gate 2 packet: ignored `dist/i-heart-pr-tours/gate-2-r4/`.
- Revised Gate 2 packet manifest SHA-256: `40e8bf2a5ac24b6fed3842f1bfd4299f54bf6bc68c1593e95487cc3c94347f98`.
- Kit manifest SHA-256: `ffed291646cdef588055a1ae46a0369a0442cfa9ee80890483881460169b389b`.
- Logo provenance SHA-256: `9721f26fdc7757324c41f486aec45aa5bdf6581cd4991b24b0f07fdcdd2e91af`.
- Icon manifest SHA-256: `c0e403a9ef36dbff74cf2d410d427f9adb342d6e7992a7978e861c3d7a36477d`.
- Publication classification remains private with zero public surfaces. Showcase, hosted guide, registry, release, deployment, public metadata, structured data, and social preview remain disabled.

T050 remains the active halt. No commit, push, pull request, public surface, or release action may begin until the repository owner explicitly approves candidate `iheartpr-g2-r4` and manifest SHA-256 `40e8bf2a5ac24b6fed3842f1bfd4299f54bf6bc68c1593e95487cc3c94347f98`, including the private publication classification.

## Gate 2 approval and publication binding

**Recorded**: 2026-09-11

- The repository owner approved exact candidate `iheartpr-g2-r4` and manifest SHA-256 `40e8bf2a5ac24b6fed3842f1bfd4299f54bf6bc68c1593e95487cc3c94347f98` with the wording `Excellent. You nailed it. Gate 2 is green`.
- Approval binds the reviewed guide, source-faithful logo and icon variants, optional sand expressions, typography correction, `IHPRT` prose shorthand, literal-code exception, verification results, and private publication classification.
- The exact approved public-surface set is empty. Showcase, hosted guide, registry, release, deployment, public metadata, structured data, and social preview remain disabled.
- Repository commit, push, official pull-request publication, CI execution, and no more than two Codex review rounds are authorized by the S028 kickoff after both owner gates.
- Gate 2 derivative approval binds `logos/approval.json` SHA-256 `9aae47141e989c34ea64e460a3594179192e2443012e15922dd3f6e49bccd41b`. Recording the approval ledger does not change any approved source artwork, geometry, framing, palette, typography, transformation, or derivative bytes.
- Final cross-artifact analysis covered 32 functional requirements, 10 measurable outcomes, and 73 tasks with complete implementation coverage and no constitution conflict. Four stale lifecycle references were corrected to the approved r4 state.

## Final local verification before publication

**Recorded**: 2026-09-11

- Focused suites pass: 47 brand-contract tests, 20 identity-continuity tests, 56 pipeline tests, and 30 site-preparation tests.
- Supporting suites pass: 34 glyphkit checks, 5 package-release tests, 14 release-contract tests, 4 continuity-audit tests, and 16 icon-suite tests.
- Python compilation and production discovery pass with eight production source brands.
- The full-capability probe reports Python, Pillow, Playwright, pikepdf, and Chromium available. All eight production kits rebuild with zero reported verifier, glyph, affiliation, image-QC, PDF-QC, or pagination problems.
- Release certification verifies nine expected v1.2.1 public assets and correctly excludes private I Heart PR Tours from release archives. Generated `AGENTS.md` synchronization is unchanged.
- Site lint and TypeScript pass. The static build produces 73 pages. Eleven production-origin and payload-contract tests pass, and browser verification covers 68 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- Public site preparation continues to report seven kits. I Heart PR Tours remains absent from public discovery after its private Gate 2 approval.
- Markdown policy and `git diff --check` pass. Mutable committed text contains no private workstation paths, BOM marker, CRLF, or detected mojibake, and generated `dist/`, `release/`, and site exports remain ignored. The supplied `assets/source/favicon/index.html` retains its approved CRLF bytes under one path-specific binary Git attribute so checkout normalization cannot invalidate its source hash.
- Post-commit continuity audit against `HEAD` passes all eight production brands with zero problems. I Heart PR Tours reports `approved-canonical`, canonical source SHA-256 `b04c0886c1e6ac09da6b470deeacdf839bf794bfacf5a54666691ea291704094`, and continuity record SHA-256 `17fb05c85befc541fc205961975cdd9cc17c9438fa3778eaa9fd46225302f8af`.

## Official pull request publication

**Recorded**: 2026-09-11

- Commit `7aec634f002b7f4b0c59c8e4c41876589925e958` was pushed to `codex/028-i-heart-pr-tours-brand-guide` after both owner gates.
- Official pull request [#195](https://github.com/shruggietech/shruggie-brand/pull/195), `feat(S028): add I Heart PR Tours brand system`, was opened against `main` and closes issue #188.
- The pull-request description records both approved candidate digests, the private zero-public-surface boundary, local verification, accessibility results, and release exclusion.
- Hosted CI and bounded Codex and security review processing are now in progress. No merge is authorized in this work slice.

## First external review round

**Recorded**: 2026-09-11

- The automatic Codex review completed on initial implementation commit `7aec634f002b7f4b0c59c8e4c41876589925e958` and opened five review threads: declared light PDF grounds, configured light-base contrast, supplied-icon target dimensions, supplied-lockup overwrite risk, and monochrome output without a white colourway.
- The dark-only guide instruction was the one finding whose proposed fixed-dark remedy conflicted with the owner-approved IHPRT brief. The governing rule now retains dark as the default while permitting an explicitly declared, owner-approved, AA-measured light guide, and PDF QC remains bound to the declared ground.
- Configured `light_surfaces.base` now drives enrichment, stated contrast re-derivation, accent validation, and the non-exemptable AA floor. IHPRT therefore measures its actual `#FFFFFF` reading surface rather than the former `#F8F8F6` fallback.
- Supplied PNG target dimensions, supplied-lockup versus generated-wordmark exclusivity, and monochrome white-colourway availability now fail in the source contract before generation. These pre-generation guards correct the invalid configurations without changing `gen_logo.py`, `iconkit.py`, any approved transformation, or the canonical Gate 1 renderer binding.
- Review-fix regressions pass: 49 brand-contract tests, the configured-light measurement test, the IHPRT exact-source generation test, and the full 143-test template suite. Fifty-three release, site-preparation, and continuity-audit tests pass.
- Seven sibling kits and the rerun IHPRT kit build cleanly. IHPRT retains 434 manifest entries, zero verifier and glyph failures, zero affiliation, image, PDF, or pagination problems, and PDF QC explicitly expects `light`.
- Site lint and TypeScript pass, the static build produces 73 pages, 11 production-origin and payload tests pass, and browser verification covers 68 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- The continuity audit passes all eight brands against `HEAD`; IHPRT retains canonical source SHA-256 `b04c0886c1e6ac09da6b470deeacdf839bf794bfacf5a54666691ea291704094` and continuity record SHA-256 `17fb05c85befc541fc205961975cdd9cc17c9438fa3778eaa9fd46225302f8af`.

## Second and final external review round

**Recorded**: 2026-09-11

- The one authorized manual `@Codex review` request was posted after the first-round fixes. Codex completed its second and final review on commit `38246eb0fb13256ea8028d0e9b5c6eec151a2acb`; no third review was requested or authorized.
- The second review opened three threads: approved private Gate 2 records were not compared with generated `logos/approval.json`, source-preserved platform targets were omitted when raster generation was unavailable, and explicitly configured colourways could omit the `color` or `light` masters required by downstream consumers.
- Approved Gate 2 records are now compared with the generated derivative manifest in both `public_showcase(..., kit)` and `verify.py`, including private brands with zero public surfaces. Focused regressions prove a matching private ledger remains unpublished and stale derivative bytes fail.
- The required `color` and `light` logo masters now fail closed in the source contract. The existing optional black and white rules remain unchanged, including the requirement for a white master only when monochrome platform output is enabled.
- Exact supplied PNG and ICO targets now pass through a separate post-generation packaging step that copies and records their approved bytes even at core capability, updates platform manifests, and mirrors web aliases. This separation is intentional: changing `iconkit.py` would silently alter the renderer digest in the already approved Gate 1 continuity record. The approved `gen_logo.py`, `iconkit.py`, source geometry, transformations, and canonical source binding remain byte-for-byte unchanged.
- The first hosted runs on commit `38246eb0fb13256ea8028d0e9b5c6eec151a2acb` exposed two compatibility defects. Python 3.8 rejected a test-only `Path.write_text(newline=...)` call and the exact IHPRT raster integration test attempted to run without a measured SVG renderer. The full job also rejected the native Linux `rsvg-convert` executable because the canonical proofs were approved with Node resvg, despite an existing cross-renderer equivalence contract.
- The Python 3.8 regression now uses the repository UTF-8 writer, and the raster integration test skips only when no renderer is measured. Hosted canonical proof generation is pinned to the approved Node resvg 2.6.2 implementation instead of preferring an unrelated native renderer. Continuity validation requires the approved settings hash and exact proof hashes for that implementation while treating the host Node version as non-output metadata; an alternate renderer remains eligible for the existing measured equivalence path only when approved proof files and identical governed settings are available.
- Final local review-fix validation passes 51 brand-contract tests, 17 icon-suite tests, 20 identity-continuity tests, 57 pipeline tests, 30 site-preparation tests, 5 package-release tests, 14 release-contract tests, 4 continuity-audit tests, and the 34-check glyph suite. All eight production kits rebuild with zero reported problems; IHPRT applies all 12 approved platform targets, retains 434 final manifest entries, and passes the light-ground PDF gate.
- Site lint and TypeScript pass, the static build produces 73 pages, 11 site contract tests pass, and browser verification covers 68 routes at desktop and mobile widths with zero WCAG 2.1 AA violations. Public preparation still includes seven kits and excludes private IHPRT.
- The continuity audit still reports IHPRT canonical source SHA-256 `b04c0886c1e6ac09da6b470deeacdf839bf794bfacf5a54666691ea291704094` and continuity record SHA-256 `17fb05c85befc541fc205961975cdd9cc17c9438fa3778eaa9fd46225302f8af` with zero problems.
