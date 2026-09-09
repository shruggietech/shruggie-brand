# Quickstart: Verify S024

## Focused archive tests

```powershell
python scripts/test_package_release.py
python scripts/test_release_contract.py
python scripts/test_prepare_site.py
```

Expected result: the six-brand inventory, deterministic atomic writer, manifest and license validation, site archive publication, and negative path/integrity cases pass.

## Rebuild production kits and archives

```powershell
python scripts/build_all.py
$version = python scripts/release_contract.py current
python scripts/package_release.py --version $version
python scripts/release_contract.py notes --version $version --output release/release-notes.md
python scripts/release_contract.py verify --version $version --release-dir release --notes release/release-notes.md
```

Expected result: all six production kits report zero verification problems and zero glyph failures; release output contains the skill bundles plus six verified brand archives.

## Site type check and export

```powershell
pnpm --dir site lint
pnpm --dir site build
```

If the Windows environment denies the Turbopack child process after content preparation, use the repository-supported webpack path:

```powershell
pnpm --dir site prepare:content
pnpm --dir site exec next build --webpack
```

## Rendered interaction and accessibility contract

```powershell
pnpm --dir site test
```

Expected result: every archive downloads from the correct brand action with ZIP media/signature checks; desktop cards retain fixed geometry and expose only two actions; mobile disclosures pass keyboard, hidden-focus, breakpoint, zoom, theme, reduced-motion, and WCAG checks; exactly one generated third-party notice appears.

## Aggregate repository gate

```powershell
python scripts/build_all.py
```

Expected result: the full repository build, archive, site, Spec Kit, accessibility, encoding, and hygiene checks pass without committing generated output.

## Encoding and change review

```powershell
git diff --check
git status --short
```

Confirm authored text is UTF-8 without BOM, uses LF endings, contains no mojibake, and contains no unnecessary em dash.
