# Quickstart: S011 Certification

Run commands from the repository root. Generated output remains ignored and disposable.

## Merged-main release candidate

```powershell
python scripts/release_contract.py current
python -m unittest discover -s scripts -p "test_*.py"
python scripts/build_all.py
python scripts/package_release.py
python scripts/release_contract.py notes --version 1.2.0 --output release/release-notes.md
python scripts/release_contract.py verify --version 1.2.0 --release-dir release --notes release/release-notes.md
python skill/templates/sync_agents_md.py skill
pnpm --dir site lint
pnpm --dir site exec next build --webpack
pnpm --dir site test
python scripts/check_markdown.py
```

## Public release

After confirming no conflicting tag or release, create and push annotated tag v1.2.0 at verified main. Wait for the Release workflow, then download the public assets into a newly created `release/public-v1.2.0/` directory and run:

```powershell
python scripts/release_contract.py verify --version 1.2.0 --release-dir release/public-v1.2.0 --notes release/release-notes.md
```

## Production

After confirming the Pages run targets verified main, run the same complete site contract against production:

```powershell
$env:SITE_VERIFY_BASE_URL = "https://brand.shruggie.tech"
pnpm --dir site test
Remove-Item Env:SITE_VERIFY_BASE_URL
```

Inspect the four representative screenshots under ignored `site/test-results/visual/`, then record only sanitized results and public URLs in `evidence.md`.
