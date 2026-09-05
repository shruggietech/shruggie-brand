# Feature Specification: Native Icon Delivery and Favicon Integrity

**Feature Branch**: `codex/008-native-icon-delivery`

**Created**: 2026-09-05

**Status**: Draft

**Input**: Deliver GitHub issues #106 and #110 as one Spec Kit slice: generate organized, platform-compliant application icon suites for web, Android, Apple mobile, macOS, and Windows; migrate existing favicon consumers safely; repair the ShruggieTech brand site's icon suite; and add behavioral integrity gates.

## Clarifications

### Session 2026-09-05

- Q: Which open issues define S008? → A: S008 closes #106 and #110 only; documentation rendering, documentation theming, and page-aware metadata remain in #108, #109, and #111.
- Q: How should existing `favicons/` consumers migrate? → A: Keep a generated compatibility mirror while making the categorized `icons/` tree authoritative, with both locations validated from one manifest.
- Q: What happens when a host cannot create an optional binary container? → A: Raster-capable production builds must create every declared suite; lower capability tiers may record an explicit skip and must never leave stale files.
- Q: Which visual source governs site icons? → A: Canonical brand mark geometry and an explicit brand-level icon background govern every derivative; the ShruggieTech site uses its approved opaque light tile treatment without redrawing the mark.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Find the Right Icon Immediately (Priority: P1)

A designer or developer opens a generated brand kit and can immediately distinguish browser favicons, Android launcher resources, store artwork, Apple asset catalogs, macOS deliverables, and Windows package assets without guessing from filenames.

**Why this priority**: The kit is only useful if humans can reliably select the correct asset for the intended platform and avoid shipping a browser image as a native application icon.

**Independent Test**: Build one production kit and inspect its icon index, platform directories, placement instructions, and machine-readable manifest. Every declared category can be located and its intended destination is stated.

**Acceptance Scenarios**:

1. **Given** a complete production kit, **When** a user opens its icon index, **Then** the web, Android, Apple mobile, macOS, and Windows suites are separately labeled and linked.
2. **Given** a platform directory, **When** a user reads its instructions, **Then** each file's role, required destination, appearance, size, and compatibility status are stated.
3. **Given** an existing consumer that still reads `favicons/`, **When** the kit is rebuilt, **Then** compatible web favicon paths remain available and match the authoritative web suite.

---

### User Story 2 - Integrate Native Application Icons (Priority: P1)

A mobile or desktop developer can copy a generated platform suite into an Android, Apple, macOS, or Windows project and receive correctly named resources, metadata, sizes, appearance variants, and store artwork derived from the approved brand mark.

**Why this priority**: Native application deliverables are the principal missing capability tracked by #106 and must be complete enough to remove manual resizing and package guesswork.

**Independent Test**: Generate a kit from canonical brand inputs and validate each platform suite against its declared platform matrix, including resource metadata and container contents.

**Acceptance Scenarios**:

1. **Given** a raster-capable build, **When** Android icons are generated, **Then** it contains density-aware legacy launcher resources, adaptive foreground/background/monochrome layers, resource declarations, and a separate compliant Google Play listing image.
2. **Given** a raster-capable build, **When** Apple icons are generated, **Then** it contains iOS and iPadOS asset-catalog data with current appearance inputs plus a macOS all-sizes asset catalog and a multi-representation application icon container.
3. **Given** a raster-capable build, **When** Windows icons are generated, **Then** it contains the classic multi-entry application icon and modern package scale, target-size, theme, and store assets with placement guidance.
4. **Given** a brand with supplied mark geometry, **When** any platform suite is generated, **Then** every derivative preserves the supplied geometry and only changes canvas, scale, background, color role, or file encoding as declared.

---

### User Story 3 - Receive a Working Brand-Site Favicon (Priority: P1)

A visitor opening the brand homepage or any documentation route sees a recognizable ShruggieTech icon instead of a broken image, blank tile, or generic framework icon.

**Why this priority**: #110 is a public identity defect, and the brand site must demonstrate the same asset quality promised by the generator.

**Independent Test**: Export the static site, load the homepage, documentation index, and one nested documentation route, and validate every declared icon and manifest reference from the emitted files.

**Acceptance Scenarios**:

1. **Given** any site route, **When** its icon metadata is inspected, **Then** it declares one shared SVG, PNG, ICO, Apple touch, and manifest icon contract.
2. **Given** the preferred SVG favicon, **When** all image references are resolved, **Then** it is self-contained or every dependency exists at its deployed URL.
3. **Given** Apple touch and manifest icons, **When** their pixels are inspected, **Then** they use the approved opaque background, preserve a safe area, and contain visible canonical ShruggieTech artwork.

---

### User Story 4 - Reject Broken or Mispackaged Icons (Priority: P2)

A maintainer receives a deterministic build failure when an icon is missing, corrupt, empty, incorrectly sized, assigned to the wrong platform role, dependent on a missing file, or inconsistent with the generated manifest.

**Why this priority**: File existence alone allowed #110 to pass. Behavioral validation is required to prevent the same class of defect from reaching a kit or the public site again.

**Independent Test**: Mutate one generated fixture at a time and prove that the appropriate kit or site validator rejects each missing, malformed, transparent, mis-sized, stale, or cross-linked artifact.

**Acceptance Scenarios**:

1. **Given** a declared PNG, **When** its dimensions, encoding, alpha policy, or visible bounds violate its role, **Then** verification fails with the exact file and expected contract.
2. **Given** an icon manifest, asset catalog, Android resource, ICO, or application icon container, **When** an entry is missing or malformed, **Then** verification fails rather than recording success from file presence.
3. **Given** a relocated SVG favicon with an unresolved nested dependency, **When** the static export is verified, **Then** verification fails with the unresolved URL.
4. **Given** a lower capability build after a richer build, **When** the generator runs, **Then** stale raster or binary icon artifacts are removed and every unavailable capability is recorded explicitly.

### Edge Cases

- The canonical mark can be rectangular, raster-backed, or supplied rather than constructed, so safe-area fitting must not assume a square glyph or editable vector paths.
- A reduced mark can differ from the full mark and remains the required source below its declared size threshold.
- Transparent marks can contain empty canvas around visible pixels; visibility and safe-area checks must measure pixels rather than file dimensions alone.
- Platform filenames can intentionally repeat at different directory depths; the manifest must use normalized relative paths and reject collisions at the same path.
- Android adaptive masks can crop the outer 18 units of a 108-unit layer, so all essential foreground artwork must fit the inner 66-unit safe zone.
- Store artwork must remain distinct from launcher resources and must not contain a baked platform mask or platform-applied shadow.
- Site publication can relocate an SVG away from its generator directory, so no relative dependency may silently become invalid.
- A failed or interrupted generation must not leave a mixture of current and stale platform assets.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every raster-capable production kit MUST contain an authoritative `icons/` tree with separately labeled `web`, `android`, `apple/ios`, `apple/macos`, and `windows` categories.
- **FR-002**: Every icon tree MUST contain a human-readable top-level index and a machine-readable manifest that enumerate every generated icon artifact, its platform, role, dimensions, format, appearance, alpha policy, and intended destination.
- **FR-003**: Every platform category MUST contain concise placement instructions that distinguish launcher icons, store artwork, browser icons, touch icons, package assets, and binary containers.
- **FR-004**: The generator MUST retain a `favicons/` compatibility mirror derived from the authoritative web suite and document it as a migration path rather than a second source of truth.
- **FR-005**: All icon derivatives MUST originate from canonical full or reduced mark sources without redrawing, normalizing, or modifying shipped identity geometry.
- **FR-006**: The brand contract MUST permit an explicit application-icon background color and MUST fall back deterministically to an existing canonical surface when no override is supplied.
- **FR-007**: Raster-capable builds MUST generate browser SVG and PNG favicons, a multi-entry ICO, an Apple touch icon, installable manifest icons, and a web application manifest in the authoritative web suite.
- **FR-008**: The preferred SVG favicon MUST be self-contained after publication and MUST contain visible canonical artwork.
- **FR-009**: Browser icons at and below the brand's declared reduced-mark threshold MUST use the reduced mark when one exists.
- **FR-010**: Touch and installable web icons that require an opaque platform surface MUST have no transparent pixels and MUST preserve a declared safe area around visible artwork.
- **FR-011**: Android output MUST contain legacy launcher PNGs for mdpi, hdpi, xhdpi, xxhdpi, and xxxhdpi resource buckets.
- **FR-012**: Android output MUST contain adaptive foreground, background, and monochrome layers on a 108-unit canvas, with essential foreground artwork constrained to the central 66-unit safe zone.
- **FR-013**: Android output MUST contain valid adaptive-icon and color resource declarations using conventional resource directories and names.
- **FR-014**: Android output MUST contain a separate 512 by 512 pixel, 32-bit, sRGB Google Play listing PNG with a full square canvas, no baked launcher mask, no platform-applied shadow, and a file size no larger than 1,024 KB.
- **FR-015**: Apple mobile output MUST contain a valid application-icon asset catalog with a 1024 by 1024 default image and current dark and tinted appearance inputs, each explicitly declared in catalog metadata.
- **FR-016**: Apple mobile output MUST preserve opaque backgrounds for application icons and MUST leave platform corner masking to the operating system.
- **FR-017**: macOS output MUST contain a valid all-sizes application-icon asset catalog covering 16, 32, 128, 256, and 512 point roles at their required scales, including the 1024-pixel store representation.
- **FR-018**: A raster-capable production build MUST produce a valid multi-representation macOS application icon container from the same canonical artwork, or fail with an explicit capability error rather than silently omit it.
- **FR-019**: Windows output MUST retain a valid classic ICO with at least 16, 24, 32, 48, 64, 128, and 256 pixel representations.
- **FR-020**: Windows output MUST contain modern `Square44x44Logo` and `Square150x150Logo` assets at 100, 200, and 400 percent scales.
- **FR-021**: Windows output MUST contain required application-list target-size assets from 16 through 256 pixels, including default, dark-unplated, and light-unplated appearances.
- **FR-022**: Windows output MUST contain required Microsoft Store logo scales and a valid package-manifest fragment that references the generated base assets.
- **FR-023**: Each platform suite MUST include a machine-readable manifest whose entries agree with the top-level icon manifest and the files on disk.
- **FR-024**: Icon generation MUST replace only approved generated directories, reject unsafe deletion targets, and remove stale platform artifacts before writing current output.
- **FR-025**: Lower capability tiers MUST preserve vector deliverables, remove stale raster or binary assets, and record explicit skips for unavailable output categories.
- **FR-026**: Kit verification MUST decode every declared PNG, validate exact dimensions and color mode, measure visible pixel bounds, enforce role-specific alpha requirements, and reject empty artwork.
- **FR-027**: Kit verification MUST validate JSON and XML metadata, exact manifest-to-file agreement, path normalization, platform naming, required entries, and cross-platform path collisions.
- **FR-028**: Kit verification MUST inspect ICO and macOS application icon containers by their internal representations rather than trusting their extensions.
- **FR-029**: Site preparation MUST publish the ShruggieTech web suite from generated kit output and MUST NOT substitute an unrelated or unverified fallback when generated production assets are expected.
- **FR-030**: The brand site's root layout MUST declare SVG, 16 and 32 pixel PNG, ICO, Apple touch, and web manifest icon relationships shared by the homepage and documentation application.
- **FR-031**: Static-site verification MUST fetch and decode every declared icon and manifest asset, resolve nested SVG references, validate dimensions, validate ICO entries, measure visible artwork, and enforce opaque touch and installable-icon backgrounds.
- **FR-032**: Static-site verification MUST cover the homepage, documentation index, and at least one nested documentation route at desktop and mobile widths.
- **FR-033**: Generated download surfaces and kit documentation MUST direct users to the categorized icon suites without mislabeling a browser favicon as a generic application icon.
- **FR-034**: Regression tests MUST cover generation, manifest contracts, migration aliases, corruption detection, stale cleanup, site relocation, static export, and all production brand kits.
- **FR-035**: Production publication MUST still require zero `verify.py` problems and zero `validate_glyph.py` failures for every production brand.
- **FR-036**: S008 MUST close only #106 and #110 after merge evidence; #108, #109, and #111 remain open for later slices.
- **FR-037**: Existing source-owned product interface symbols under a brand's legacy `icons/` directory MUST retain byte-identical geometry and content under generated `icons/domain/`, remain declared in the exact icon manifest, and survive repeated generation without being mistaken for stale platform output.

### Key Entities

- **Icon Profile**: The brand-level icon presentation contract, including canonical foreground source, full and reduced behavior, background, safe area, and appearance derivation.
- **Icon Artifact**: One generated file with a normalized path, platform, role, dimensions, format, appearance, alpha policy, source variant, and destination guidance.
- **Platform Suite**: A separately packaged group of related icon artifacts, metadata, and human instructions for web, Android, Apple mobile, macOS, or Windows.
- **Icon Manifest**: The authoritative inventory linking the top-level icon index, platform manifests, compatibility mirror, and files on disk.
- **Capability Record**: The measured build tier and renderer/container capabilities that determine whether raster and binary outputs are mandatory or explicitly skipped.
- **Site Icon Contract**: The shared set of root URLs, metadata declarations, manifest entries, artwork rules, and emitted-file integrity checks used by every public route.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can identify the correct web, Android, iOS or iPadOS, macOS, or Windows icon directory and placement instructions in no more than two navigation steps from the kit root.
- **SC-002**: One raster-capable kit build produces five separately labeled platform suites with zero unclassified icon files and zero duplicate authoritative paths.
- **SC-003**: Every generated platform manifest has 100 percent agreement with its files, the top-level manifest, declared dimensions, format, appearance, and alpha policy.
- **SC-004**: Android validation covers all five legacy density buckets, all three adaptive layers, both required resource declarations, and one distinct Play listing asset with zero violations.
- **SC-005**: Apple validation covers all declared mobile appearances, all macOS size and scale roles, and every internal application-icon container representation with zero missing entries.
- **SC-006**: Windows validation covers all seven classic ICO sizes, the six minimum square-logo scale assets, every declared target-size appearance, the store-logo scales, and the package-manifest references with zero missing entries.
- **SC-007**: The homepage, documentation index, and nested documentation route each load the same valid preferred favicon and complete icon metadata with zero failed requests or unresolved nested dependencies.
- **SC-008**: Apple touch and installable web icons have 100 percent opaque pixels, non-empty visible artwork, exact declared dimensions, and the configured ShruggieTech icon background.
- **SC-009**: Corruption tests reject 100 percent of the required missing-file, wrong-size, undecodable, empty, unsafe-path, malformed-metadata, unresolved-SVG, bad-container, and stale-output fixtures.
- **SC-010**: Every production kit completes with zero verification problems and zero glyph failures, and the static site exports with zero WCAG 2.1 AA violations.
- **SC-011**: All repository text changed by S008 is UTF-8 without BOM, uses LF line endings, and contains zero detected mojibake sequences.
- **SC-012**: Every pre-existing product interface icon survives aggregate generation byte for byte under `icons/domain/`, while undeclared generated icon files still fail verification.

## Assumptions

- Current platform guidance is interpreted as of 2026-09-05 and is recorded in `research.md`; the generated manifest is versioned so later platform-matrix changes can be deliberate.
- Browser favicons remain available at their historical `favicons/` paths for compatibility, but all new documentation identifies `icons/web/` as authoritative.
- The existing reduced-mark threshold remains the source-selection rule for small browser and classic desktop representations.
- The existing raster capability is sufficient to produce PNG suites, and Pillow is the cross-platform container writer used by production CI where native platform tooling is unavailable.
- Android, Apple, and Windows project compilation is outside S008; this slice validates their documented resource and metadata contracts without requiring proprietary IDEs or stores.
- Documentation visual repair, documentation theme refinement, structured data, route-specific social previews, and sitemap parity remain outside S008 under #108, #109, and #111.
