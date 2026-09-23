# Toolchain

> [!NOTE]
> **Probe first, then pick. Never assume a tool is present and never fail
> silently when it is missing.**

Every tool below is open source and installable from a standard package
manager. The agent's job at the start of a build is to find out what it
actually has, say so, and route each asset to the best available producer.

## Probing

**Run `python3 templates/probe.py <kit-dir>` and route off what it reports.** It
prints the capability block, classifies the machine into the core, raster or
full tier from `09-portability.md`, and writes `<kit>/qc/probe.json` so the
generators and `VERIFY.md` read measured facts rather than assumptions.

The core tier, Python and its standard library alone, must always succeed. The
glyph gate in particular carries its own rasteriser precisely so it never
degrades to a skip.

The equivalent by hand, when you want to see it yourself:

```bash
for t in inkscape rsvg-convert resvg magick convert potrace oxipng pngquant \
         cwebp avifenc svgo pdffonts qpdf soffice pandoc ffmpeg mmdc \
         oxlint stylelint node npx python3; do
  command -v "$t" >/dev/null 2>&1 && printf '%-14s %s\n' "$t" "$( "$t" --version 2>&1 | head -1 )" \
                                  || printf '%-14s MISSING\n' "$t"
done
python3 - <<'PY'
for m in ("coloraide","fontTools","PIL","playwright","pikepdf"):
    try:
        __import__(m); print(f"{m:12} present")
    except ImportError: print(f"{m:12} MISSING")
PY
```

State the findings in one short block, then proceed with the fallback chain.
Do not narrate each individual miss.

## The matrix

Asset on the left, first choice first. Later entries are the fallback chain.

| Asset to produce | Reach for | Fallback | Notes |
| --- | --- | --- | --- |
| Logo and icon vector masters | hand-authored SVG | none | The agent writes path data on a declared grid. There is no tool shortcut and no tracing. |
| Outline live text in an SVG | `inkscape --export-text-to-path` | `fonttools` glyph extraction | Mandatory before any SVG ships. A shipped SVG must never depend on an installed font. |
| SVG to PNG at N sizes | `rsvg-convert` | `resvg`, then `inkscape --export-type=png` | ImageMagick's SVG delegate shells out to rsvg anyway and does it worse. Do not use `magick` for this. |
| Application-icon composition | `templates/iconkit.py` plus Pillow | vector-only web index at core tier | Composes every platform from the canonical full and reduced SVG masters, the declared background, and measured raster capability. Native suites are required whenever raster output is available and record explicit skips otherwise. |
| Multi-resolution `.ico` and `.icns` | deterministic writers in `templates/iconkit.py` | none after raster composition | The writers assemble validated per-size PNGs directly, so output does not depend on platform-specific ImageMagick behavior. Assert the exact entry matrix afterwards. Never resample one large mark for every small target. |
| Raster compositing, social previews | ImageMagick | Pillow | |
| Palette extraction from a supplied logo | `magick in.png -colors 8 -format %c histogram:info:` | Pillow + k-means | Reference only. The accent still has to pass every canon check. |
| Deterministic authoritative-input evidence | `templates/analyze_inputs.py` | none | Reads validated local inputs, ignores fully transparent pixels, and writes hash-linked candidates under `qc/`. |
| Raster concept to vector | `potrace` | `autotrace`, Inkscape trace | **Ideation input only.** Output is never shipped. |
| PNG optimisation | `oxipng -o4 --strip safe` | `zopflipng`, `pngquant` | pngquant is lossy. Use it only for previews. |
| WebP / AVIF | `cwebp` / `avifenc` | Pillow | |
| SVG cleanup | `svgo` | manual | Never let it collapse a viewBox or drop `currentColor`. |
| Font subsetting, ttf to woff2 | `pyftsubset` (fonttools) | `woff2_compress` | |
| Font QA | `fontbakery`, `ttx` | fonttools inspection | Confirms the weights a face actually contains before a stylesheet asks for one. |
| Controlled font ingestion | `templates/ingest_font.py` | none | Explicit operator action only. Requires an authoritative HTTPS or controlled local source, expected hash, license evidence, contained destination, measured metadata, and atomic placement. |
| Colour math, OKLCH, contrast | `coloraide` (Python) | none | Never hand-roll a contrast ratio. Canon's numbers came from here. This is the only hard dependency beyond the standard library, and without it no colour work can proceed. |
| Mark geometry and its gate | `templates/glyphkit.py` and `templates/validate_glyph.py` | none needed | Standard library only, by design. No renderer, no Pillow, no browser, no vision. See `08-glyph-construction.md`. |
| Brand guide PDF | headless Chromium via Playwright, print-to-PDF | Typst, then Pandoc plus LaTeX | The HTML-to-PDF route keeps the guide rendered from the live system. |
| PDF verification | `pikepdf`, `pdffonts` | qpdf | Catches non-embedded fonts, wrong page count, missing bookmarks. |
| Screenshots of rendered output | Playwright headless | none | This is how the agent checks its own work. Do it before claiming a gate passed. |
| Accessibility audit of rendered pages | `axe-core` via Playwright | `pa11y` | |
| JS/TSX adherence lint | `oxlint` with the generated config | ESLint | Already house practice. |
| CSS adherence lint | `stylelint` | none | |
| Documents and decks | LibreOffice headless (`soffice --headless --convert-to`) | Pandoc | LibreOffice is the maintained successor to OpenOffice. Prefer it. |
| Diagrams | `mmdc` (mermaid-cli) | hand-authored SVG | |
| Motion reference | `ffmpeg` | none | Rare. Logo animation reference clips only. |
| Checksums and manifest | Python `hashlib` | `sha256sum` | |

## Tools deliberately demoted

**GIMP.** Its script-fu batch interface is fragile and awkward to drive from an
agent, and every job it would do here is done more reliably by ImageMagick or
Pillow. GIMP stays on the list as a tool for a human doing interactive
touch-up, and it is not an agent target.

**ImageMagick for SVG rasterisation.** Covered above. It delegates to librsvg
and loses fidelity on the way. Call librsvg directly.

**Google Fonts at build time.** Ordinary generation uses bundled, locally
licensed font files and must not fetch fonts over the network. Use the
controlled ingestion command before a build when an approved fixed face is
missing. See `01-canon.json` typography.sourcing.

## Contract commands

Run `templates/validate_brand.py` before any renderer. It rejects incomplete affiliation, inheritance, typography, supplied-input, palette-approval, path, hash, SVG-safety, license, and font metadata. Run `templates/analyze_inputs.py` only after validation, and run `templates/scan_affiliation.py` after generation to reject false ownership claims. `templates/ingest_font.py` is the only network-capable font path and is never called by an ordinary build.

## Icon delivery

`templates/gen_logo.py` calls `templates/iconkit.py` only after canonical full and reduced SVG masters exist. A raster-capable build must produce the complete web, Android, iOS and iPadOS, macOS, and Windows suites under `icons/`; a core build produces the self-contained web SVG index and records why binary suites were skipped. `verify.py` decodes the images, parses native metadata, checks platform matrices and safe areas, inspects ICO and ICNS entries, rejects undeclared files, and proves every legacy `favicons/` alias is byte-identical to its authoritative web target.

### Native host role matrix

An asset is qualified for the role and host named below, not for every surface that accepts its file format. Check the application's resource declaration and pinned package bytes separately from the generated kit. A Windows executable may embed `classic/app.ico` while an MSIX package selects target-size assets; an Android details view may resolve an adaptive resource while an older launcher uses a legacy density PNG. Generated assets do not update an installed application until the consumer repins and rebuilds it.

| Generated role and location | Host surface and composition | Measured acceptance | Platform authority |
| --- | --- | --- | --- |
| Web favicon SVG, PNG, ICO in `icons/web/` | Browser tab and document icon, natural square; alpha follows the declared web profile | Decode each size and ICO frame, retain the reduced mark where selected, check light and dark composites | [W3C app manifest](https://www.w3.org/TR/appmanifest/) |
| Web `apple-touch-icon.png` | iOS/iPadOS home-screen touch shortcut | Declared alpha or full plate follows the web profile; check the 180-pixel image under the host-rounded boundary | [Apple app icons](https://developer.apple.com/design/human-interface-guidelines/app-icons) |
| PWA `any` PNG in `icons/web/` | Installable app icon without maskable cropping; may be transparent when declared | Manifest maps only `any` to the ordinary asset; declared alpha and small-size silhouette agree | [web.dev maskable guidance](https://web.dev/articles/maskable-icon) |
| PWA `maskable` PNG in `icons/web/` | Edge-filled field under platform mask | All essential pixels remain inside the centered 80%-diameter safe circle, and the mask has no transparent edge | [W3C maskable safe zone](https://www.w3.org/TR/appmanifest/) |
| Android `mipmap-*` legacy PNGs | Pre-adaptive launcher density resources | Opaque field, correct density size, no contrasting second plate after circular crop | [Android adaptive icon guidance](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive) |
| Android adaptive foreground, background, and optional monochrome | API 26+ launcher and system details views via `@mipmap/ic_launcher`; optional `roundIcon` must be declared by the consumer if used | Foreground essential art inside central 66/108 region; background fills every circle, rounded-square, and squircle mask; monochrome retains the single-ink silhouette | [Android adaptive icon guidance](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive) |
| Android `play-store/google-play-512.png` | Play Console listing, not launcher resource | Full opaque 512-pixel square without a pre-rounded outer mask or outer shadow | [Google Play icon specification](https://developer.android.com/distribute/google-play/resources/icon-design-specifications) |
| iOS/iPadOS catalog default, dark, tinted | Xcode AppIcon appearance selected by the host | Catalog maps exact appearance and size, host mask retains essential art, declared opacity is checked per appearance | [Apple app icons](https://developer.apple.com/design/human-interface-guidelines/app-icons) |
| macOS catalog, iconset, ICNS | App bundle, Dock, Finder at point-size and scale | Every declared size decodes and remains recognizable at 16 and 32 points; catalog and container frames agree | [Xcode app icon configuration](https://developer.apple.com/documentation/xcode/configuring-your-app-icon) |
| Windows `classic/app.ico` | Win32 executable, title bar, taskbar, Alt+Tab, shortcut | Decode all frames; inspect alpha boundary and 16, 24, 32, 48-pixel light/dark composites; a plate must be explicitly approved | [Microsoft icon construction](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction) |
| MSIX `Square44x44Logo.targetsize-*` and unplated alternatives | Packaged taskbar and app list; light and dark host selection | Check exact-pixel resources, unplated alpha, and composite contrast; do not substitute a plated tile export | [Microsoft icon construction](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction) |
| MSIX scale, tile, and Store assets | Start tile and Store display | Intentional full plate, exact scale mapping, and declared background | [Microsoft icon design](https://learn.microsoft.com/en-us/windows/apps/design/iconography/app-icon-design) |

For Windows taskbar roles, BrandBuilder emits transparent outer pixels by default when the approved logo has no square enclosure. An approved square enclosure retains its plate unless a governed application-icon setting explicitly selects an unplated variant. MSIX scale, tile, and Store roles keep their independent plated compositions. Verify the embedded executable or package resource after repinning; a generated kit cannot prove which resource the application shipped.

For egui, treat status text as text even if its message describes an unavailable action. `ui.strong(...)` can select the active widget stroke color instead of the ordinary text override; do not use it for a dark-surface status without measuring its effective foreground and local background. A genuinely disabled control is exempt from WCAG 2.1 text contrast, but this project additionally requires its label to remain readable at 4.5:1 while its disabled state stays visually distinct. Enabled text requires 4.5:1 and meaningful control or state cues require 3:1 under [WCAG 2.1 contrast minimum](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum) and [non-text contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast). Render enabled, disabled, hover, focus, and light/dark states in the target egui version; token equality alone is insufficient.

## Image generation

**For ideation only.** Use available image generation to show possible logo
directions, mood, and visual language for operator discussion. Treat each image
as a nonbinding concept, not as production artwork or approved identity source.

> [!CAUTION]
> **Never for shipped artwork.** Every mark that ships is hand-authored vector on
> a declared grid. The generated images are conversation, and the SVG is the
> deliverable.

## When a tool is missing

> [!WARNING]
> Say which asset is affected, name the fallback being used, and note any quality
> difference. If no fallback exists, produce everything else, list the gap
> explicitly in `VERIFY.md`, and do not quietly ship a worse substitute as though
> it were the real thing.

A build that silently degrades reads as complete when it is not, and that is
the failure mode this whole system exists to prevent.
