# Quickstart: Portfolio Card Consistency

## Prerequisites

- Work from the repository root on `codex/033-portfolio-card-consistency`.
- Use the existing local Python environment and installed site dependencies.
- Chromium and the document renderers required by the full repository pipeline must be available.

## 1. Run focused source checks

```powershell
node site/tests/site.test.mjs
```

Expected: portfolio surface eligibility, exact generic notice, marker association, explicit action destinations, and style-source contracts pass.

## 2. Build and run the site verifier

```powershell
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: all portfolio cards use the dark presentation family and white visible copy; actions pass contrast, focus, hidden-focus, target-size, spacing, geometry, zoom, reduced-motion, and mobile disclosure checks; exactly one generic notice appears; all routes produce zero WCAG 2.1 AA violations.

## 3. Inspect the homepage

- Review the eight desktop cards at wide and narrow widths.
- Review every mobile disclosure and action at 200 percent zoom.
- Confirm I Heart PR Tours uses the dark portfolio treatment while its guideline pages remain light-first.
- Confirm long descriptions and both-action stacks have visible bottom clearance.
- Confirm the footer under the portfolio contains only `* Third-party projects are independently owned and operated.`

## 4. Run CI-parity verification

Run the commands documented by `.github/workflows/build.yml`, including Python 3.8 compatibility suites, Python 3.12 publication and generator suites, capability probing, all-kit generation, release certification, generated-agent diff, site lint/build/test, publication audit, Markdown audit, and repository hygiene.

Expected outcomes:

- all eight production kits report zero verification problems and zero glyph failures;
- the 81-page static export and 76-route browser matrix pass;
- source identity and detailed vendor-boundary metadata remain unchanged;
- no generated output is staged for commit.
