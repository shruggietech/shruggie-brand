# Quickstart: Hosted ZIP MIME Compatibility

## Prerequisites

- Work from `codex/031-zip-mime-alias` with the repository's pinned Node.js and pnpm versions and installed site dependencies.
- Keep `.specify/feature.json`, `dist/`, `release/`, and `site/out/` uncommitted.
- Production-origin validation requires network access to `https://brand.shruggie.tech`.

## 1. Run the focused payload contract

```powershell
node --test site\tests\payload-contract.test.mjs
```

Expected: valid fixtures pass for `application/zip` and `application/x-zip-compressed`; malformed bodies fail under both; a valid ZIP with an unsupported media type fails; established non-ZIP cases pass.

## 2. Run the complete local site verifier

```powershell
pnpm --dir site test
```

Expected: production-origin policy tests, payload-contract tests, and the complete local generated-site verification pass with zero failures.

## 3. Verify the production origin

```powershell
$env:SITE_VERIFY_BASE_URL = 'https://brand.shruggie.tech'
node site\scripts\verify-site.mjs
Remove-Item Env:SITE_VERIFY_BASE_URL
```

Expected: all required routes and downloads pass. Hosted ZIP responses labeled `application/x-zip-compressed` produce no media-type failures, while their archive bodies continue to satisfy the ZIP signature and end-record checks.

## 4. Run repository CI parity

Run the complete command set documented by `.github/workflows/build.yml`, including Python compatibility, generator, identity, release, site preparation, static build, browser, payload, production-origin policy, accessibility, publication artifact, Markdown, and repository-hygiene gates.

Expected: every suite passes with zero verifier problems, zero glyph failures, zero accessibility violations, and no generated artifact or local Spec Kit state staged for commit.

## 5. Inspect repository hygiene

```powershell
git diff --check
git status --short
```

Expected: only S031 source, test, specification, evidence, and changelog files are tracked; generated outputs remain ignored.
