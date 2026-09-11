# Quickstart: Documentation Footer Removal

## Prerequisites

- Python dependencies from `requirements.txt`
- pnpm 10.28.2 and Node.js 20 or newer
- Site dependencies installed with the checked-in lockfile
- Chromium installed for Playwright verification

## Focused validation

From the repository root:

```powershell
node --test site/tests/site.test.mjs
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected result: the source contract rejects documentation footer composition, every exported documentation route contains zero global site footers, representative desktop and narrow documentation pages retain reachable pagination, and the homepage footer contract remains unchanged.

## Full repository gate

```powershell
python -m compileall -q scripts skill/templates
python scripts/test_package_release.py
python scripts/test_release_contract.py
python scripts/test_prepare_site.py
python scripts/test_identity_continuity_audit.py
python skill/templates/test_brand_contract.py
python skill/templates/test_identity_continuity.py
python skill/templates/test_glyphkit.py
python skill/templates/test_iconkit.py
python skill/templates/test_pipeline.py
python scripts/check_markdown.py
python scripts/build_all.py
python skill/templates/sync_agents_md.py skill
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected result: all tests and builds complete successfully, every production kit reports zero verification problems and zero glyph failures, the generated agent contract is unchanged, the site export and browser checks pass, and no generated artifact is staged for commit.
