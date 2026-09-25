# Changelog

All notable changes to the Shruggie brand system are documented in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.0] - 2026-09-25

### Changed

- Added source-referenced formal identity colors, approved artwork combinations, correct-use examples, and measured dark/light interface cues to every production kit, hosted color guide, portable guide, and PDF.
- Allowed owned sub-brands to choose independent palettes and unrelated brands to opt into shared colors without changing parentage or endorsement. Removed mandatory sibling and parent-orange hue exclusion while retaining WCAG AA pairings.
- Advanced BrandBuilder to 2.2.0 and Brand Canon to 1.5.0. Existing approved brand hex values, logo path bytes, and adapter APIs remain unchanged.
- Corrected the main manual's stale portfolio and kit-anatomy claims, made the repository README evergreen, and bound the generated manual to exact reference and release-candidate bytes.

### Decisions

- On 2026-09-25, retained `shruggietech-house` as an explicit compatibility choice for the historical shared orange pair, independent of ownership and typography. Generated color role records reference approved values instead of copying them into a second source.
- On 2026-09-25, rejected role-only cue overrides until all token and adapter generators can emit them consistently; approved accent and semantic source choices remain the way to set cue colors. Contrast floors use unrounded measurements.
- On 2026-09-25, kept S054's documentation corrections in the still-unpublished v2.2.0 candidate and derived manual identity from existing publication facts. Tagged preflight now checks exact reference and prepared-page hashes rather than trusting a visible version label.

## [2.1.0] - 2026-09-25

### Changed

- Completed light-first guide and hosted presentation across PDF, portable, cards, and download surfaces with measured contrast gates.
- Governed optional custom assets with provenance, approval, rights, accessibility and publication metadata; projected eligible expressions into guides, hosted navigation, asset library, and downloads.
- Repaired shadcn registry catalogs and installable endpoints, added pinned schema and clean-consumer gates, and documented the bundled local-font setup.
- Advanced BrandBuilder to 2.1.0 and Brand Canon to 1.4.0 for the compatible light-guide and custom-asset source fields. Advanced I Heart PR Tours to 1.1.0 for its approved optional sand expressions; other approved brand package versions remain unchanged.

### Decisions

- On 2026-09-23, kept custom expressions separate from canonical logo authority and excluded non-public source bytes from public archives; the supplied I Heart PR Tours sand SVGs remain unchanged.
- On 2026-09-25, treated the public registry as a discovery catalog plus direct install endpoints and removed its unsupported local-font item; the complete kit remains the authority for bundled offline fonts.
- On 2026-09-25, selected a minor BrandBuilder and Brand Canon release for the new compatible generator and source-contract capabilities. Approved logo geometry and the separate Interface Canon and adapter versions remain unchanged.

## [2.0.3] - 2026-09-23

### Changed

- Separated ordinary and maskable web icon roles, added mask-safe Android presentation, and made ESO Weave Windows taskbar icons unplated while preserving source logo geometry.
- Advanced the Brand Canon to 1.3.0, BrandBuilder to 2.0.3, egui adapter to 1.0.2, Glitchpad brand package to 1.1.1, and ESO Weave brand package to 1.0.2.
- Documented native host icon and egui status roles with explicit consumer repin and application call-site boundaries.
- Prepared the repository front door with approved theme-aware branding, canonical brand destinations, stable latest-release guidance, and release/status badges.

### Fixed

- Added generated-role verification for maskable web icons, Android masks, Windows taskbar frames, and egui status contrast.
- Repaired the repository README's eight noncanonical brand links and stale skill-download guidance, and added deterministic local and generated-route link checks to CI.

### Changed

- On 2026-09-22, prepared S047 as a publication-bound documentation and guideline integrity correction with a new immutable compiler patch candidate.
- On 2026-09-23, made the canonical-host Gate 2 proof export tolerate one transient exact-manifest mismatch by regenerating from a clean destination; repeated or unrelated failures still block CI and retain diagnostic artifacts.

### Decisions

- On 2026-09-22, retained governed manual and brand source as the authority for public prose and generated preview treatment, and kept internal history outside the reader-facing audit.
- On 2026-09-23, preserved the approved derivative hash as the sole Gate 2 acceptance value after a merged-build flake, without changing identity sources, generated-kit bytes, or the 2.0.2 candidate.
- On 2026-09-23, made README link validation consume the generated route contract after site preparation, using isolated negative fixtures instead of a duplicated slug list or live HTTP checks in CI.
- On 2026-09-23, kept public README downloads on the latest published release rather than naming an unpublished 2.0.3 candidate; exact-version assets remain governed by release metadata and checksums.

## [2.0.2] - 2026-09-22

### Changed

- Rewrote published documentation and delivered kit guidance as present-version instructions while retaining active compatibility, identity, provenance, accessibility, licensing, and recovery rules.
- Advanced BrandBuilder to 2.0.2 for changed generated documentation and preview bytes with an immutable package identity.

### Fixed

- Corrected integration preview well contrast and nonvisual-resource labels without changing approved asset bytes.
- Corrected bottom documentation pagination to land at the destination heading with accessible focus while preserving fragments and history.

## [2.0.1] - 2026-09-22

### Changed

- On 2026-09-21, separated fine-pointer native control density from conservative coarse, mixed, unknown, and touch interaction targets, retaining the 44-unit target where imprecise input may occur while deriving compact desktop height from governed target and hit-slop values.
- On 2026-09-22, integrated the pending site runtime and tooling updates from Dependabot PRs #225 and #226, paired Fumadocs Core and UI with the updated MDX package, and kept the verified release candidate on one reproducible dependency lockfile.
- On 2026-09-22, required CI to install the browser revisions for both the pinned Python and updated Node Playwright clients, preserving full-tier PDF and archive evidence after the site tooling update.
- On 2026-09-22, incorporated the eight post-merge Dependabot updates (#242-#249): five verified workflow-action revisions and current-runtime fontTools, Playwright, and pikepdf pins, while retaining Python 3.8-compatible versions.
- On 2026-09-22, synchronized the workflow's immutable action revision contract with exact upstream version comments. The existing pinned-source gate remains enforced; publication of 2.0.1 waits for this combined follow-up candidate to merge.

### Fixed

- Corrected the generated egui density regression for issue #239 and S044: ordinary desktop buttons, selectors, switches, checkboxes, and radio-style controls now use restrained shared padding and 28-point comfortable or 22.96-point compact sizing, text scaling can grow controls without clipping, Live Log-style rows use at most 2 points of compact vertical spacing, and adapter 1.0.1 preserves 44-point conservative targets.
- Stabilized conformance iframe measurement by waiting for the selected profile document to finish loading before browser geometry assertions run.
- Corrected the release candidate's incompatible Fumadocs MDX/Core pairing and Playwright browser mismatch discovered while integrating S045 dependencies.
- Corrected Dependabot's site and generator label names to match the repository's existing labels.

## [2.0.0] - 2026-09-20

### Added

- Added immutable kit package identities, exact release-backed publication metadata, generated bundle bills of materials, and release-impact guidance for issues #233 through #235 and slice #222.
- Added the S041 documentation contract boundary for issue #213, including one governed manual inventory, complete source and route dispositions, generated exact-version facts shared by hosted and bundled guidance, four operational system chapters, and accessible ownership, operating-mode, and capability-loop overviews.
- Added the S040 cross-host conformance contract for issue #217, including generated browser, Tauri Android, Wails Windows, and egui evidence tracks, seven required capability profiles, known-bad and corrected host traces, non-substitutable evidence classes, explicit diagnostics, human-reviewed screenshot candidates, and deterministic per-brand verification.
- Added the S039 native egui adapter and independent version contracts for issues #216 and #218, including generated typed Rust tokens, idiomatic immediate-mode helpers, explicit support and gap records, `egui_kittest` rendered-state evidence, machine-validated compatibility, and exact checksummed recovery.
- Added the S037 Interface Contract foundation for issues #210, #211, and #212, including a renderer-neutral Interface Canon, contextual Author, Implementation, and Audit routing, generated consumer authority manifests, deterministic merge-safe instructions, checksummed exact-version offline recovery, and authorization-preserving capability-gap records.
- Added the identity-locked public I Heart PR Tours source system for issue #188, including exact supplied source and favicon authority, locally licensed typography, a light-first guide, deterministic single-ink derivatives, optional sand expressions, complete continuity evidence, and full brand-website publication.
- Added source-bound identity continuity records, canonical approval packets, exact-byte promotion, pre-derivative drift rejection, calibrated visual comparison evidence, and truthful historical baselines for all seven production brands for issue #185.
- Added the approved Cueson production identity and seventh public brand kit for issue #184, including exact Cueframe source continuity, Cue Teal color governance, complete lockups and application icons, generated guidelines and specimen, and a manifest-certified future consumer handoff.
- Added deterministic, manifest-certified complete brand-kit downloads for all seven public production brands, with staged verification and atomic publication shared by release and static-site builds.
- Added the independent ESO Weave production brand kit and public showcase for issue #153, with byte-preserved authoritative SVG sources, fixed Inter typography, approved lockups and single-ink derivatives, complete provenance evidence, native platform assets, guidelines, UI specimen, and vendor-safe public metadata.
- Added generated portal payloads, canonical multi-page brand guideline routes, focused topic navigation, compact HEX-first color references, purpose-led asset libraries, rendered platform instructions, and portable offline guide downloads for issues #157 through #161.
- Added manifest-derived guideline asset catalogs, copyable governed color references, scoped dark/light specimens, compact section navigation, and progressive back-to-top behavior for issues #147, #148, and #149.
- Added explicit constructed and authoritative logo source modes, separate Full and Reduced source bindings, deterministic derivative provenance, hash-bound mask approval, and fail-closed source, metadata, operation, placement, raster, icon, and mask-topology verification.
- Added issue #151 regressions for unrelated geometry, construction helpers, stale hashes, role and usage mismatches, reduced-mark substitution, undeclared transformations, incomplete provenance, and changed authoritative silhouettes.
- Added optional validated square-enclosure composition, source-owned contextual wordmark roles, and renderer-portable monochrome knockout support for generated marks, lockups, and application icons.
- Added visible-ink square-containment regressions for portrait, landscape, asymmetric-canvas, empty, standalone-master, and platform-specific occupancy cases.

### Changed

- Changed production Pages publication from moving `main` output to exact formal releases and replaced downstream adoption tracking with publisher-owned compatibility and migration facts.
- Added the upstream S042 Glitchpad AppFrame contract for issue #219, including a bounded full-bleed application-shell layout, a dependency-free environment bridge entry, and exact cross-repository artifact pinning for the downstream host-evidence pilot.
- Advanced component recipes and the Web/React adapter to `1.1.0`, and advanced BrandBuilder to `2.0.0` for the incompatible package identity and consumer-contract layout.
- On 2026-09-19, added generated API 24 WebView fallbacks for AppFrame root ownership, dynamic viewport height, and IME measurement while retaining the modern `:has()`, `100dvh`, and VisualViewport paths.
- On 2026-09-17, separated main-manual system authority, current hosted child-brand presentation, and exact pinned bundled implementation authority while preserving every existing documentation, guideline, topic, and download route.
- On 2026-09-17, made conformance evidence host- and profile-specific, prohibited browser emulation from satisfying actual-host or consumer-adoption claims, and kept screenshot baseline approval as an explicit human decision with source, version, viewport, font, renderer, and image identity.
- On 2026-09-17, separated Brand Canon identity authority from Interface Canon semantic UI authority, defined precise brand, canon, interface, and compiler version meanings, and made delivered exact bytes the first recovery source for fresh consumer sessions.
- On 2026-09-15, made exact-byte base64 data URIs the governed transport for image-backed specimen marks, with contained source resolution, explicit media types, byte-identical verified-kit-to-site publication, and preference for an already approved supplied horizontal color lockup when declared.
- On 2026-09-12, defined `application/zip` and GitHub Pages' `application/x-zip-compressed` as the exact accepted ZIP media types while retaining independent opening-signature and end-record validation.
- On 2026-09-11, corrected S028's mistaken private-publication assumption: every production brand built with the skill is now required in the public website inventory, generated brand export directories are ignored generically, and I Heart PR Tours uses the complete governed website surface set with a white showcase card and colored heart icon.
- On 2026-09-11, reused the hash-bound portable Gate 2 comparison during static-site preparation so equivalent cross-platform PNG encodings do not invalidate canonical Windows approval.
- On 2026-09-11, marked the supplied I Heart PR Tours favicon index as a path-specific binary source so Git cannot normalize its approved CRLF bytes and invalidate source continuity; all authored repository text remains UTF-8 with LF endings.
- On 2026-09-09, separated nonbinding logo direction selection from canonical production-source approval and prohibited Gate 2 from reconstructing or first revealing identity geometry.
- On 2026-09-09, separated external clear-space governance from optional variant-specific standalone presentation padding so approved Full and Reduced concept framing can survive deterministic production export.
- On 2026-09-09, consolidated each brand portal into the approved Overview, Voice, Identity, Components, Assets, and Integration hierarchy, grouped project documentation into its approved five-section table of contents, and removed redundant brand-root pages while preserving every nested guideline, download, registry, and asset endpoint for issues #175, #179, and #180.
- On 2026-09-09, replaced implicit homepage card navigation with explicit Guidelines and Download Kit actions, native compact mobile disclosures, stable desktop geometry, and one generated shared third-party notice for issues #173 and #174.
- On 2026-09-08, made the six shared footer destinations an explicit ordered policy, preserving Company as same-tab while limiting safe separate-context navigation to Download the skill, Source, and License.
- On 2026-09-08, established one bounded, clipped media viewport for guideline logo examples and asset-library previews, with measured centering and divider containment across all production brands, themes, responsive widths, and 200 percent zoom.
- On 2026-09-07, bound Gate 1 approval to a canonical digest of every derivative-producing brand setting and required its scope to cover all five derivative families.
- On 2026-09-07, introduced hash-bound two-gate approval for third-party source identities and public surfaces, with fail-closed source-inventory, derivative-provenance, vendor-boundary, and site-publication enforcement.
- On 2026-09-07, superseded S017's hosted single-page guideline presentation with brand-owned Fumadocs portals backed by one validated typed registry, while retaining generated standalone HTML as a download-only artifact.
- On 2026-09-07, replaced the superseded universal orange link decoration with explicit editorial, text-action, navigation, utility, card, button, identity, and contextual-navigation roles, and rebuilt documentation pagination with neutral surfaces and restrained green border feedback for issues #142 and #143.
- On 2026-09-07, made generated logo provenance and platform icon manifests the only guideline inventory authority, with portable relative asset links rewritten only by the hosted publication step.
- On 2026-09-07, bound ShruggieTech Full and Reduced marks to their separately approved immutable raster masters while preserving all source bytes, constructed identity paths, colors, and public presentation.
- On 2026-09-07, approved Glitchpad's permanent square identity using a sulfur square with charcoal page on dark surfaces and a charcoal square with sulfur page on light surfaces, retaining the slate fold and protected page paths while prohibiting muddy or darkened yellow variants.
- On 2026-09-07, introduced an optional brand-source showcase-surface role that resolves through existing governed surfaces and is omitted for unconfigured brands, keeping site presentation policy out of slug-specific CSS and preserving sibling treatments.
- On 2026-09-07, made visible-alpha bounds the shared standalone square-raster composition authority while retaining each platform's established safe-area ratio and preserving canonical vector geometry.

### Fixed

- Embedded the missing I Heart PR Tours logo in its generated type specimen for issue #204 and applied the owner's wider stacked-lockup correction, preserving authoritative artwork and proportions while adding unresolved-reference, decoded-byte, lockup-selection, rendered-pixel, direct-hosted, offline, and publication-copy regression gates.
- Normalized the homepage portfolio for issues #199 and #200 with dark card surfaces, exact white card copy, accessible explicit actions, reliable lower spacing, and one concise generic third-party notice.
- Corrected I Heart PR Tours CTA guidance for issues #201 and #203: primary controls now use the governed `#C5342C` fill, secondary controls use the matching red-outline treatment with surface-aware AA text, the PDF documents both action roles and states, and shared reader-facing guide prose uses American English.
- Accepted GitHub Pages' ZIP MIME alias in the shared local and production payload verifier, with fail-closed regressions for malformed bodies and unsupported media types, for issue #198.
- Replaced the divergent Pages and Release rebuilds with one SHA-pinned verified Build workflow that preserves the exact protected `build` context, uploads SHA-qualified same-run Pages and checksummed release artifacts, preflights tag ancestry, rejects unsafe publication trees, and limits write credentials to checkout-free publisher jobs for issue #196.
- Bound approved Gate 2 records to their generated derivative manifest during verification and publication, preserved approved supplied icon targets at core capability without changing the Gate 1 identity renderer, required downstream `color` and `light` logo variants, and added canonical-host proof and Gate 2 evidence export plus hash-bound measured comparison for cross-platform CI, including defined color sampling for tiny proofs with no non-edge interior and decoded-pixel equivalence for differently encoded embedded PNGs.
- Restored Python 3.8 compatibility in the guide typography regression and skipped the exact raster-derivation integration test when no measured SVG renderer is available.
- Measured light-surface contrast against each brand's configured base, validated supplied icon dimensions before generation, rejected supplied-lockup configurations that could be overwritten by generated wordmarks, and required a white colourway for enabled monochrome platform icons.
- Replaced the universal dark-guide rule with an explicit declared reading-surface contract, retaining dark as the default while allowing owner-approved, fully measured light-first guides to pass matching PDF ground verification.
- Corrected light-guide typography so Source Sans 3 carries footers, page numbers, labels, tables, and metadata while Courier Prime remains limited to literal code blocks, and bound dark-source logo previews to visible dark wells.
- Removed the shared marketing footer from every documentation page so contextual previous and next navigation follows the content directly, while preserving the homepage footer contract and dedicated brand-guideline navigation for issue #191.
- Prevented approved constructed glyphs from being redrawn during production handoff by reusing the exact Gate 1 centerlines through `glyphkit.capsule`, binding the result to source hashes, and adding cross-renderer silhouette, bounds, and centroid checks.
- Centered documentation pagination chevrons with wrapped and unwrapped labels, preserved right-to-left rotation through independent optical translation, and restored pointer plus disabled cursor treatment and minimum targets for shared theme controls.
- Restored complete Glitchpad black and white horizontal and stacked lockups by giving the shared square-knockout mask an explicit local coordinate extent, then added structural, rendered-height, and SVG-to-PNG verification for the failure.
- Made Gate 2 approval portable across rendering environments by binding raster derivatives to their verified SVG masters, and added pre-emission and final-verifier checks for constructed single-ink geometry.
- Bound Gate 2 approval to every derivative file hash and projected the required ESO Weave vendor and trademark boundary across visible pages, metadata, structured data, registry records, and social previews.
- Corrected clipped brand landing headings, unstable color disclosure layouts, unbounded asset previews, blank nonvisual asset cards, raw integration Markdown, and conflated guideline footer controls across responsive and 200 percent zoom layouts.
- Removed the generated global anchor hover underline that could combine with site-owned decoration, and corrected pagination title and description selectors so each retains its intended hierarchy.
- Rejected square-enclosure configurations whose measured source paths exceed the safe content area, and distinguished composed external clear space from protected internal glyph measurements in generated guidance.
- Preserved the permanent page-and-G knockout in Android adaptive monochrome and iOS tinted exports by routing platform recoloring through the generated one-color master instead of the full-color alpha silhouette.
- Centered non-square portfolio marks inside a constrained square image box and replaced Glitchpad's diluted yellow landing-card and portfolio-hero surfaces with its governed charcoal card surface, including accessible light-theme text and no decorative yellow glow.

## [1.2.1] - 2026-09-06

### Changed

- On 2026-09-05, made the canonical ShruggieTech brand record the source of the black-background browser icon suite and selected the existing colored horizontal lockups for light and dark site chrome without changing logo geometry.
- Standardized the public documentation root as "Documentation" and its first numbered page as "Variance Contract", reduced landing navigation to viewport-specific approved destinations, and applied the generated orange and green roles to actions, links, code strings, list markers, and pagination affordances.
- Added fail-closed production-origin verification that reuses the complete local route, resource, payload, metadata, responsive, theme, and accessibility contract, validates downloadable formats and media types, and recognizes safe permanent redirects from GitHub Pages.

### Fixed

- Added fail-closed pixel and ICO-frame checks for canonical black favicons, a 12-cell visual regression matrix, minimum mobile navigation targets, reduced-motion link behavior, persistent documentation pagination affordances, and non-overlapping documentation footer spacing.
- Updated Brotli from 1.1.0 to 1.2.0 to remediate GHSA-2qfp-q593-8484 (CVE-2025-6176).

## [1.2.0] - 2026-09-05

### Added

- Added one validated route descriptor graph for exact canonical, Open Graph, Twitter, JSON-LD, breadcrumb, sitemap, and route-specific social-preview discovery across every public page.
- Added deterministic documentation notice transformation and browser verification for code copying, syntax distinction, strict canonical paths, both themes, responsive layouts, and route metadata parity.
- Added generated web, Android, iOS and iPadOS, macOS, and Windows application-icon suites with exact manifests, native integration metadata, and human-navigable packaging.
- Added emitted-site favicon integrity checks and direct categorized icon-suite downloads for every generated brand.
- Added fail-closed affiliation, showcase, inheritance, authoritative-input, palette-approval, and fixed-font contracts for owned and third-party brand work.
- Added deterministic source evidence, controlled atomic font ingestion, and complete third-party ownership-safety regression coverage.
- Added a responsive ShruggieTech brand portfolio with generated identity cards, direct asset access, and a prominent skill download path.
- Added a searchable Fumadocs documentation experience generated from the authoritative skill references.
- Added complete route metadata, social previews, favicons, a web manifest, robots policy, sitemap, and browser-level WCAG 2.1 AA verification.

### Changed

- Applied the generated ShruggieTech theme and existing light and dark lockups to the documentation shell with compact type hierarchy, branded orientation states, and responsive navigation.
- Migrated all five production brands to explicit house inheritance and typography while making generated wording, semantic tokens, framework bindings, guides, and site metadata contract-driven.
- Aligned the brand site with ShruggieTech's visual system and approved public message, including the headline "We build comprehensive brands".
- Restricted normal build and publication discovery to the five production sources under `brands/`.
- Amended repository governance to require isolated temporary data for synthetic generator tests.

### Fixed

- Restored native Fumadocs code panels and copy controls, preserved syntax colors and overflow behavior, rendered explicit source notices as semantic callouts, and removed the duplicate documentation navigation link.
- Rebuilt the mislabeled Space Grotesk Medium and Bold WOFF2 files from their authoritative local TTF faces so internal family and weight metadata match their declarations.
- Made generated wrappers self-contained so authoritative raster marks remain visible in PNG, favicon, social-preview, and contact-sheet exports, with empty raster output now rejected.

### Removed

- Removed the committed and publicly listed example brand, its generated route assumptions, and its active test references.

## [1.1.2] - 2026-09-04

### Added

- Added `logo.geometry_provenance` with `glyphkit` and `imported` values so legacy geometry remains unchanged while its origin is visible in verification.
- Added repository-wide CI, deterministic release automation, and a generated documentation and registry site.
- Added five migrated production kits and a synthetic pipeline fixture.
- Added Spec Kit 1.0.4 with Codex skills integration and PowerShell scripts.

### Changed

- Imported path command violations are warnings for legacy geometry and remain failures for glyphkit-authored geometry.
- Preserved native SVG primitives and raster-only authoritative identity art through generated exports.
- Scoped sibling hue allocation to production identities while retaining contrast checks for fixtures.

### Fixed

- Replaced ShruggieTech's `#2BCC73` light-surface link color, measured at 1.98:1, with `#037B40`, measured at 5.05:1, to meet WCAG 2.1 AA.
- Corrected the shadcn binding documentation to use the published `/brand/r/{name}.json` route.
- Restored Python 3.8 kit discovery and added a minimum-version CI job.
- Replaced generated font-network imports with local bundled bindings and aligned the `fonts.json` registry route.
- Made unexpected full-tier PDF and page-QC failures block builds and releases.
- Made the core tier preserve vector output while explicitly recording raster and PDF skips.
- Verified renderer fallbacks before advertising them as available.
- Suppressed project-owned Windows console subprocesses and disabled their interactive input.
- Forwarded native required state from generated form controls and removed nested interactive CTA markup.
- Removed private workstation paths and Cloudflare resource identifiers from public planning records.
- Cleared generated PDFs, raster exports, and favicons before capability-tier downgrade skips so stale artifacts cannot enter a later manifest or release.
- Verified favicon ICO output against its independently measured writer capability.
- Enforced the repository's single-physical-line Markdown prose policy in public planning records and CI.
- Made the pipeline regression fixtures Python 3.8-compatible and run them in the minimum-version hosted job.
- Included Pillow compositing in the measured raster capability instead of allowing a late import failure.
- Cleared stale generated QC sheets before full-tier capture or lower-tier skips.
- Recolored image-backed SVG master masks through a standard-library PNG path so core-tier generation does not import Pillow.
- Cleared stale PDF contact sheets and extracted pages before lower-tier skips or replacement attempts.
- Deferred Pillow imports in image QC so core-tier named skips execute on hosts without Pillow.
- Aligned SVG-renderer capability reporting with the governed librsvg, resvg, Inkscape, and Node resvg chain; removed ImageMagick SVG fallbacks; rejected the unrelated Windows `convert.exe` utility; and made ICO generation reuse the validated ImageMagick or Pillow result.
- Corrected the Glitchpad fixture's token and class prefixes and added narrow-screen overflow guards.
- Corrected ShruggieTech's narrow-screen header layout and removed the remaining nested interactive contact control.
- Generated release notes from the exact versioned changelog section and added a reusable seven-archive metadata, licensing, PDF, and checksum contract.
- Corrected generated kit manifests to carry each kit's declared version instead of a constant 1.0.0.
- Rejected source and archive canon metadata that differs from the authoritative release canon.
- Finalized kit manifests after verification and QC so every published verification artifact is size- and checksum-protected.

## [1.1.1] - 2026-09-03

### Added

- Added the non-exemptable WCAG AA floor for all canon-declared text and fill roles.
- Added canon rules for accessible ShruggieTech green on light surfaces.

## [1.1.0] - 2026-09-02

### Added

- Added the glyph construction layer, portability tiers, per-brand chart hue rotations, promoted generators, and standard-library geometry tests.

### Changed

- Relicensed the brandbuilder code, templates, and reference documentation from proprietary terms to Apache-2.0 while reserving names and marks.

[Unreleased]: https://github.com/ShruggieTech/shruggie-brand/compare/v2.0.1...HEAD
[2.0.1]: https://github.com/ShruggieTech/shruggie-brand/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/ShruggieTech/shruggie-brand/compare/v1.2.1...v2.0.0
[1.2.1]: https://github.com/ShruggieTech/shruggie-brand/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/ShruggieTech/shruggie-brand/compare/v1.1.2...v1.2.0
[1.1.2]: https://github.com/ShruggieTech/shruggie-brand/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/ShruggieTech/shruggie-brand/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/ShruggieTech/shruggie-brand/releases/tag/v1.1.0
