# Quickstart: Embed Specimen Logo

## Prerequisites

- Work from the repository root on `codex/034-embed-specimen-logo`.
- Use Python 3.8 or newer with the repository requirements installed.
- Use Node.js 20 or newer with site dependencies and Playwright Chromium installed.
- Make an SVG rasterizer available through the existing capability probe for rendered-pixel evidence.

## 1. Run the focused generator regression

```powershell
python skill/templates/test_pipeline.py
```

Expected: the isolated image-based specimen embeds exact source bytes, prefers an approved supplied horizontal lockup when declared, preserves the canonical fallback otherwise, rejects unresolved dependencies, and executes or explicitly skips the rendered mark-pixel check according to the probed capability.

## 2. Build and inspect I Heart PR Tours

```powershell
python scripts/build_all.py i-heart-pr-tours
```

Expected: `verify.py` reports zero problems and `validate_glyph.py` reports zero failures. The generated specimen contains no relative or external references. Its `href` values are data payloads or internal fragments only.

Open `dist/i-heart-pr-tours/specimens/i-heart-pr-tours-type-specimen.svg` directly. The approved wider stacked mark from `horizontal_darkbg.svg` must appear centered in the upper-left header with no source asset directory dependency. Its serialized image geometry is `x=39`, `y=95.625`, `width=297`, and `height=183.75` inside the unchanged outer header transform.

## 3. Build and verify the publication path

```powershell
python scripts/build_all.py
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: all production kits pass, the hosted specimen matches the verified kit bytes, and Playwright confirms visible mark pixels through direct HTTP navigation and an offline local `file:` opening.

## 4. Run complete CI parity

Run every command in `.github/workflows/build.yml`, including Python 3.8 compatibility suites, publication and release tests, identity tests, Markdown audit, capability probe, all-kit build, release certification, generated-agent diff, site lint/build/test, and publication audit.

Expected outcomes:

- all eight production kits report zero verification problems and zero glyph failures;
- the I Heart PR Tours authoritative source artwork and brand contract hashes remain unchanged, while the generated specimen uses the centered native proportions of the approved horizontal lockup;
- the archive, site copy, browser, and SVG-renderer paths use the same self-contained specimen;
- no generated output is staged for commit.
