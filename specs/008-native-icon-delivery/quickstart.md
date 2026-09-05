# Quickstart: Validate Native Icon Delivery and Favicon Integrity

Run every command from the repository root. Commands are non-interactive and write generated output only below ignored repository directories.

## 1. Focused Python contracts

```powershell
python skill/templates/test_brand_contract.py
python skill/templates/test_iconkit.py
python skill/templates/test_pipeline.py
python scripts/test_prepare_site.py
```

Expected: all tests pass, including platform matrices, exact manifests, corruption rejection, stale cleanup, compatibility aliases, and generated-site source selection.

## 2. Python 3.8 syntax and source checks

```powershell
python -m compileall -q scripts skill/templates
python scripts/check_markdown.py
python scripts/test_release_contract.py
```

Expected: no syntax, Markdown, or release-contract failures.

## 3. Generate one icon suite

```powershell
python scripts/build_all.py shruggietech
```

Expected:

- `dist/shruggietech/icons/manifest.json` declares five generated suites.
- `dist/shruggietech/icons/web/` contains the complete browser and installable-web set.
- `dist/shruggietech/icons/android/` contains legacy resources, adaptive resources, and distinct Play artwork.
- `dist/shruggietech/icons/apple/ios/` and `icons/apple/macos/` contain valid catalogs and macOS container output.
- `dist/shruggietech/icons/windows/` contains classic and modern assets.
- `dist/shruggietech/favicons/` is byte-identical to declared web aliases.
- Existing Fragcap product symbols are byte-identical under `dist/fragcap/icons/domain/` and declared by its top-level icon manifest.
- `verify.py` and `validate_glyph.py` report zero failures.

## 4. Validate key native metadata

```powershell
python -m json.tool dist/shruggietech/icons/manifest.json
python -m json.tool dist/shruggietech/icons/apple/ios/Assets.xcassets/AppIcon.appiconset/Contents.json
python -m json.tool dist/shruggietech/icons/apple/macos/Assets.xcassets/AppIcon.appiconset/Contents.json
```

Expected: each JSON document parses and every referenced filename exists.

## 5. Build every production kit

```powershell
python scripts/build_all.py
```

Expected: all five production kits finish with `BUILD CLEAN`, zero verification problems, and zero glyph failures.

## 6. Export and verify the site

```powershell
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: the static export succeeds; homepage, documentation index, and nested documentation routes share the complete icon contract; every icon decodes; SVG dependencies resolve; ICO entries are valid; required opaque images contain no transparent pixels; and WCAG 2.1 AA checks remain green.

## 7. Repository hygiene

```powershell
git status --short
git diff --check
git diff --exit-code -- dist site/out site/generated site/public
```

Expected: no generated kit, site export, generated content, or public materialization is staged. `.specify/feature.json` remains machine-local and uncommitted.
