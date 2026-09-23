# Research: Native Host Icon and State Conformance

## R1. ESO status text belongs to a consumer-local call site

**Decision**: Treat `Capture Unavailable` as meaningful status text, not an inactive button. ESO Weave `src/app/ui.rs:2685` calls `ui.strong(history_diagnostic_heading(...))`. Its `src/app/theme.rs` assigns `on_primary` to the active widget text, and egui 0.36.1 `Visuals::strong_text_color()` returns `widgets.active.text_color()`. ESO already has a `label_strong` helper in `src/app/widgets.rs` that uses the correct palette text. Record this exact attribution; strengthen BrandBuilder's native guidance and tests, and require downstream call-site adoption for field closure.

**Rationale**: A global text override does not affect `RichText::strong()`. Treating the label as a disabled control would apply the wrong normative contrast category.

**Alternative rejected**: Declare a BrandBuilder-only fix sufficient for the installed screen. BrandBuilder does not own the consumer call.

## R2. Windows resources have separate roles

**Decision**: Test the ESO Weave Win32 executable's `assets/icon.ico` separately from MSIX assets. Its `build.rs:220` embeds that ICO. Use transparent outside-mark pixels for unplated taskbar roles, including Win32 frames and MSIX target-size variants; retain explicit plated tile and Store roles. Check 16, 24, 32, and 48 pixels against light and dark surfaces.

**Rationale**: The current `_write_windows` fills every ICO frame with the same dark background, producing the reported square. Microsoft's construction guidance distinguishes taskbar target-size/unplated and tile/store artwork: [Windows icon construction](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction), [Windows icon design](https://learn.microsoft.com/en-us/windows/apps/design/iconography/app-icon-design).

**Alternative rejected**: Make every Windows asset transparent. Some tile and Store surfaces use intentional plates.

## R3. Android adaptive layers and listing art are distinct

**Decision**: Follow the APK's actual `android:icon` and optional `android:roundIcon` mapping. Keep adaptive foreground within the 66/108 safe area, fill background fully, qualify monochrome separately, and avoid contrasting double-framing in circle, rounded-square, and squircle previews. Legacy launcher and Play listing artwork use their own compositions. Use approved Glitchpad role colors and preserve the source enclosure path.

**Rationale**: The generator currently puts a yellow inset enclosure over a dark full background. The system circular mask exposes dark wedges. Android requires full-size adaptive background and safe foreground, while Play expects a full-square independent listing asset: [adaptive icons](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive), [Play icon specification](https://developer.android.com/distribute/google-play/resources/icon-design-specifications).

**Alternative rejected**: Enlarge the enclosed source until it touches the canvas edge. That changes approved geometry or violates foreground safe containment.

## R4. PWA purpose needs independent qualification

**Decision**: Generate separate `any` and `maskable` PNGs, with edge-filled background and essential art inside the central 80%-diameter circle for maskable, then validate manifest mapping and masks.

**Rationale**: The current manifest gives identical PNGs `purpose: "any maskable"` even when `transparent_web_icons` allows transparent artwork. The [living Web App Manifest specification](https://www.w3.org/TR/appmanifest/) defines the maskable safe zone; [web.dev guidance](https://web.dev/articles/maskable-icon) recommends distinct role artwork.

**Alternative rejected**: Mark existing transparent PNGs maskable without measuring their edge fill or safe region.

## R5. Apple role checks do not require a new asset system

**Decision**: Keep flat asset catalogs and containers, verify their declared mappings, host masking and sizes, and document the limits of local preview versus actual Apple host proof. [Apple App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons), [Xcode app icon configuration](https://developer.apple.com/documentation/xcode/configuring-your-app-icon).

**Rationale**: The current kit generates flattened iOS and macOS assets. Modern layered Icon Composer is available but is not mandatory for this contract; changing to it would expand scope and compatibility risk.

**Alternative rejected**: Convert all platforms to one transparency rule or require layered Apple icons in S048.
