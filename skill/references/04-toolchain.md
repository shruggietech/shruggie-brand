# Toolchain

**Probe first, then pick. Never assume a tool is present and never fail
silently when it is missing.**

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

**Google Fonts at build time.** Not a tool choice so much as a trap.
`fonts.gstatic.com` is blocked by the egress proxy in the Claude sandbox while
`fonts.googleapis.com` resolves, so the fetch appears to work and then dies at
the binary step. Fonts are bundled. See `01-canon.json` typography.sourcing.

## S007 contract commands

Run `templates/validate_brand.py` before any renderer. It rejects incomplete affiliation, inheritance, typography, supplied-input, palette-approval, path, hash, SVG-safety, license, and font metadata. Run `templates/analyze_inputs.py` only after validation, and run `templates/scan_affiliation.py` after generation to reject false ownership claims. `templates/ingest_font.py` is the only network-capable font path and is never called by an ordinary build.

## S008 icon delivery

`templates/gen_logo.py` calls `templates/iconkit.py` only after canonical full and reduced SVG masters exist. A raster-capable build must produce the complete web, Android, iOS and iPadOS, macOS, and Windows suites under `icons/`; a core build produces the self-contained web SVG index and records why binary suites were skipped. `verify.py` decodes the images, parses native metadata, checks platform matrices and safe areas, inspects ICO and ICNS entries, rejects undeclared files, and proves every legacy `favicons/` alias is byte-identical to its authoritative web target.

## Image generation

**Encouraged, for ideation.** Use the frontier image generation available in
whatever agent is running the skill to explore logo directions, mood, and
visual language with the operator. It is genuinely good at opening up a concept
space quickly, and it beats describing shapes in prose.

**Never for shipped artwork.** Every mark that ships is hand-authored vector on
a declared grid. The generated images are conversation, and the SVG is the
deliverable.

## When a tool is missing

Say which asset is affected, name the fallback being used, and note any quality
difference. If no fallback exists, produce everything else, list the gap
explicitly in `VERIFY.md`, and do not quietly ship a worse substitute as though
it were the real thing.

A build that silently degrades reads as complete when it is not, and that is
the failure mode this whole system exists to prevent.
