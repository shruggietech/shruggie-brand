# Research: Native Icon Delivery and Favicon Integrity

## Decision 1: One authoritative icon tree with compatibility aliases

**Decision**: Generate `icons/` as the authoritative tree and retain `favicons/` as a generated compatibility mirror of `icons/web/`.

**Rationale**: Issue #106 requires a human-navigable archive, while existing sites and kit consumers already depend on `favicons/`. A generated mirror provides a safe migration without allowing two independently authored sources. The top-level icon manifest records aliases and verification compares their bytes.

**Alternatives considered**:

- Remove `favicons/` immediately. Rejected because it creates an unnecessary breaking change for existing downloads and generated UI kits.
- Keep `favicons/` authoritative and add platform siblings. Rejected because a browser-specific legacy name cannot clearly own native application deliverables.

## Decision 1a: Preserve pre-existing domain symbols in a labeled subcategory

**Decision**: When a source brand already has product interface symbols under the legacy `icons/` path, move those bytes into generated `icons/domain/`, record them in the authoritative manifest, and preserve that subcategory across repeated generation.

**Rationale**: On-the-ground inspection found Fragcap's six established product symbols in the same source path selected for S008's generated application assets. Clearing the whole directory would violate geometry immutability and silently delete shipped assets. A generated `domain/` category resolves the namespace collision, makes the archive easier to navigate, and retains exact-manifest enforcement.

**Alternatives considered**:

- Delete or overwrite the existing symbols. Rejected because source-owned geometry is immutable and the files remain valid product assets.
- Exempt undeclared root SVGs from verification. Rejected because this weakens the exact-inventory contract and leaves stale files indistinguishable from intentional assets.
- Change every source brand to a new directory in this slice. Rejected because source migration is unnecessary when generation can preserve and categorize the bytes deterministically.
- Duplicate generation logic for both locations. Rejected because independently generated outputs can drift.

## Decision 2: Canonical geometry plus a declarative icon background

**Decision**: Use the existing full and reduced mark geometry as the only foreground source, add an optional `logo.application_icon.background` color to the brand contract, and default it to the canonical base surface.

**Rationale**: Every platform needs a canvas treatment, but changing canvas, scale, or a declared color role does not require modifying mark geometry. A brand-level background allows ShruggieTech to select the approved light tile while third-party brands retain their own canonical surfaces.

**Alternatives considered**:

- Hard-code white for ShruggieTech in generator code. Rejected because it makes ownership-specific assumptions in the shared skill.
- Infer a background from logo pixels. Rejected because S007 already established explicit, reviewable brand contracts and inference would be unstable.
- Add independent backgrounds for every platform. Deferred because there is no demonstrated brand need for five unrelated treatments, and it would increase approval surface.

## Decision 3: Android adaptive, legacy, and store outputs remain distinct

**Decision**: Generate legacy launcher resources for mdpi through xxxhdpi, adaptive foreground/background/monochrome layers and XML under conventional `res/` paths, plus a separate Google Play 512-pixel listing image.

**Rationale**: Current Android guidance requires adaptive layers on a 108 by 108 unit canvas, reserves the outer 18 units on each side for masking and effects, and keeps essential artwork within the inner 66 by 66 unit safe zone. Google Play independently requires a 512 by 512, 32-bit sRGB PNG, full square, no platform mask or shadow, and no more than 1,024 KB. Treating the store image as a launcher icon would violate that distinction.

**Primary sources**:

- [Android adaptive icons](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive)
- [Google Play icon design specifications](https://developer.android.com/distribute/google-play/resources/icon-design-specifications)

**Alternatives considered**:

- Provide only 192 and 512 browser-oriented Android images. Rejected because those do not form an Android application resource set.
- Bake a rounded mask into all Android images. Rejected because launchers and Google Play apply their own masks.

## Decision 4: Current Apple mobile inputs plus complete macOS sizes

**Decision**: Generate an iOS and iPadOS `AppIcon.appiconset` using 1024-pixel default, dark, and tinted appearance images, and generate a macOS all-sizes catalog plus `.iconset` and `.icns` delivery.

**Rationale**: Current Xcode guidance permits a single 1024-pixel image for iOS and iPadOS and supports dark and tinted appearances. macOS still requires each size. The generator can create deterministic PNG derivatives and use Pillow as the cross-platform `.icns` writer already present in the raster-capable dependency tier.

**Primary sources**:

- [Configuring an app icon using an asset catalog](https://developer.apple.com/documentation/xcode/configuring-your-app-icon)
- [Apple app icon guidance](https://developer.apple.com/design/human-interface-guidelines/app-icons/)

**Alternatives considered**:

- Generate the older exhaustive iPhone and iPad slot matrix. Rejected as the default because current Xcode can generate those variations from 1024-pixel inputs; it adds volume without improving current integration.
- Require Icon Composer output. Rejected because it requires proprietary tooling unavailable in cross-platform CI and would make the production gate non-reproducible.
- Omit `.icns` outside macOS. Rejected because Pillow supports deterministic cross-platform ICNS writing at the repository's supported raster tier.

## Decision 5: Windows minimum complete package set

**Decision**: Generate a seven-entry classic ICO, `Square44x44Logo` and `Square150x150Logo` at 100, 200, and 400 percent scales, the documented target-size list for default, dark-unplated, and light-unplated appearances, StoreLogo scale assets, and a manifest fragment.

**Rationale**: Microsoft currently identifies 16, 24, 32, 48, and 256 pixels as the bare minimum classic coverage and recommends scale assets at 100, 200, and 400 percent for the two principal MSIX logos. The documented target-size list prevents unwanted backplates and improves exact-size selection. Retaining 64 and 128 in the classic ICO preserves this repository's stronger existing coverage.

**Primary sources**:

- [Construct your Windows app's icon](https://learn.microsoft.com/en-us/windows/apps/design/iconography/app-icon-construction)
- [Windows app icon design](https://learn.microsoft.com/en-us/windows/apps/design/iconography/app-icon-design)

**Alternatives considered**:

- Generate every optional Windows 10 tile and splash asset. Rejected because it greatly expands the kit without a declared application target; the selected contract covers the reusable application and store baseline.
- Keep only `favicon.ico`. Rejected because a browser ICO is not a modern MSIX resource suite.

## Decision 6: Role-specific image composition and alpha rules

**Decision**: Compose all platform images from a transparent canonical mark raster. Plated application and store images use a full opaque configured background; adaptive foreground, monochrome, and Windows unplated assets retain transparency; small browser images select the reduced mark at the declared threshold.

**Rationale**: One composition engine can enforce visible bounds, safe areas, and background rules while preserving exact source geometry. Platform masks remain external. The distinction is machine-verifiable and prevents transparent Apple touch icons or incorrectly plated adaptive layers.

**Alternatives considered**:

- Resize the existing favicon PNG into every platform role. Rejected because it bakes browser canvas decisions into unrelated platform assets.
- Reconstruct vector paths per platform. Rejected by constitution P2.

## Decision 7: Manifest-driven verification

**Decision**: Generate a versioned top-level `icons/manifest.json`, platform manifests or native metadata, and validate files from those declarations rather than from directory-name heuristics alone.

**Rationale**: Exact path, size, role, appearance, format, alpha, and source-variant metadata makes output auditable and future platform additions additive. Verification can reject missing, extra, malformed, colliding, stale, or misclassified assets without byte-comparing rendered images.

**Alternatives considered**:

- Hard-code every path only in the verifier. Rejected because documentation and validation would drift.
- Rely on native IDE compilation. Rejected because Android Studio and Xcode are not available in all CI environments and do not validate kit navigability.

## Decision 8: The public site consumes the generated web suite

**Decision**: Site preparation copies the ShruggieTech `icons/web/` suite, declares SVG, PNG, ICO, Apple touch, and manifest relationships in the shared root layout, and verifies the emitted static export by decoding artwork and resolving SVG dependencies.

**Rationale**: Constitution P5 requires the site to consume generated kits. The issue #110 failure occurred because file and link presence were treated as proof of rendering. Static-export validation must exercise the deployed path context and role-specific image integrity.

**Alternatives considered**:

- Commit manually repaired favicon files under `site/public`. Rejected because they would become a second identity source.
- Keep fallbacks to raw ShruggieTech source images when the generated kit is incomplete. Rejected because production builds must fail rather than silently publish unverified substitutes.
