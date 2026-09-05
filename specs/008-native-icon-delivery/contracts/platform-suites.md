# Platform Suite Contract

## Web

The authoritative `icons/web/` directory contains self-contained SVG and PNG favicons, `favicon.ico`, `apple-touch-icon.png`, installable icons, `site.webmanifest`, and a README. Small outputs use the reduced mark at the declared threshold. Opaque touch and installable roles use the effective application-icon background.

## Android

The `icons/android/` directory contains:

- `app/src/main/res/mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/ic_launcher.png`
- `app/src/main/res/drawable-nodpi/ic_launcher_foreground.png`
- `app/src/main/res/drawable-nodpi/ic_launcher_monochrome.png`
- `app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml`
- `app/src/main/res/values/ic_launcher_colors.xml`
- `play-store/google-play-512.png`
- README and platform manifest

The adaptive layer canvas is 108 units at a four-pixel-per-unit reference export. Essential foreground pixels remain within the centered 66-unit safe zone. The Google Play image is a distinct opaque 512-pixel sRGB PNG with no rounded mask or platform shadow.

## Apple mobile

The `icons/apple/ios/Assets.xcassets/AppIcon.appiconset/` directory contains 1024-pixel default, dark, and tinted PNGs plus valid `Contents.json`. Each image is opaque and leaves corner masking to the operating system.

## macOS

The `icons/apple/macos/` directory contains:

- `Assets.xcassets/AppIcon.appiconset/` with 16, 32, 128, 256, and 512 point roles at 1x and 2x
- `AppIcon.iconset/` with conventional iconset filenames
- `AppIcon.icns` with internally readable representations
- README and platform manifest

Duplicate pixel sizes required by different point and scale roles may reference the same filename only when native metadata permits it and the manifest retains every semantic role.

## Windows

The `icons/windows/` directory contains:

- `classic/app.ico` with 16, 24, 32, 48, 64, 128, and 256 pixel entries
- `msix/Assets/Square44x44Logo.scale-{100,200,400}.png`
- `msix/Assets/Square150x150Logo.scale-{100,200,400}.png`
- `msix/Assets/Square44x44Logo.targetsize-{16,20,24,30,32,36,40,48,60,64,72,80,96,256}.png`
- Dark and light unplated counterparts for every target-size asset
- `msix/Assets/StoreLogo.scale-{100,200,400}.png`
- `msix/ApplicationVisualElements.fragment.xml`, a schema-shaped `uap:VisualElements` element that references the `Square44x44Logo` and `Square150x150Logo` logical resource basenames
- `msix/PackageProperties.fragment.xml`, a foundation `Properties` element that references the `StoreLogo` logical resource basename
- README and platform manifest

## Compatibility

`favicons/` mirrors the authoritative web files used by existing kit consumers. It contains no independently composed assets, and verification compares every alias byte for byte.

## Product interface symbols

Source-owned product interface icons that predate the application suite are preserved byte for byte under `icons/domain/`. They are not an application platform suite, but every file is declared in the top-level exact manifest so existing identity geometry survives generation without creating an undeclared-file exception.
