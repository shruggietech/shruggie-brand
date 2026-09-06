# Quickstart: Validate v1.2.1 Release and Production Certification

## Prerequisites

- Python 3.8 or newer with repository requirements installed
- Node.js 20 or newer and pnpm 10.28.2
- Native renderers for the full production-kit gate
- Site dependencies and Chromium installed as documented by CI

## Source and release checks

```powershell
python skill/templates/test_glyphkit.py
python scripts/test_package_release.py
python scripts/test_release_contract.py
python scripts/test_prepare_site.py
python skill/templates/test_brand_contract.py
python skill/templates/test_iconkit.py
python skill/templates/test_pipeline.py
python scripts/check_markdown.py
python scripts/release_contract.py current
```

Expected: all checks pass and current release discovery prints `1.2.1`.

## Complete candidate

```powershell
python scripts/build_all.py
python scripts/package_release.py --version 1.2.1
python scripts/release_contract.py notes --version 1.2.1 --output release/release-notes.md
python scripts/release_contract.py verify --version 1.2.1 --release-dir release --notes release/release-notes.md
python skill/templates/sync_agents_md.py skill
git diff --exit-code -- skill/AGENTS.md
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: five production kits have zero problems and glyph failures, exactly seven assets pass, generated agent instructions remain synchronized, and every site check passes.

## Public release

After verified-main tagging, download the release body and all assets into a new ignored directory under `release/`, then run the same release verifier against those downloads. The public release must be non-draft, non-prerelease, target verified main, and contain exactly seven assets.

## Production

```powershell
$env:SITE_VERIFY_BASE_URL = "https://brand.shruggie.tech"
pnpm --dir site test
Remove-Item Env:SITE_VERIFY_BASE_URL
```

Expected: every public route passes at 360px and 1280px with zero failures and zero WCAG 2.1 AA violations.

## Repository hygiene

```powershell
git diff --check
git status --short
```

Expected: no generated output in the change set, UTF-8 without BOM and LF-only text, no mojibake, no private paths or secrets, and only intended release source, test, changelog, and Spec Kit files.
