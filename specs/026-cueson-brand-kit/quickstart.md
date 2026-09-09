# Quickstart: Verify S026 Cueson Brand Kit

Run commands from the repository root with the local virtual environment and site dependencies installed as documented in `CONTRIBUTING.md`. All commands are non-interactive and write generated output only beneath ignored paths.

## Gate 1 proposal

```text
.\.venv\Scripts\python.exe scripts/test_cueson_identity_study.py
.\.venv\Scripts\python.exe scripts/cueson_identity_study.py --gate 1 --output dist/.s026-cueson-study/gate-1
```

Expected before owner approval:

- four concept directions and exactly one recommendation are present;
- each direction has vector, 256, 64, 32, and 16 pixel light, dark, and single-ink proofs;
- the approved Cue Teal palette includes measured contrast and color-vision evidence;
- the manifest reports no production Cueson identity source and no public eligibility;
- every output path is ignored;
- visual inspection is recorded in `evidence.md`;
- execution halts for Gate 1.

## Gate 2 proposal

After current Gate 1 approval is recorded:

```text
.\.venv\Scripts\python.exe skill/templates/test_brand_contract.py
.\.venv\Scripts\python.exe skill/templates/test_pipeline.py
.\.venv\Scripts\python.exe scripts/build_all.py cueson
.\.venv\Scripts\python.exe scripts/cueson_identity_study.py --gate 2 --output dist/.s026-cueson-study/gate-2
```

Expected before owner approval:

- the complete derivative family is generated from the approved master and configuration;
- every derivative carries its source relationship and hash;
- platform masks, crops, dimensions, wordmark spacing, reduced-size behavior, copy compositions, and public surfaces are visible in the packet;
- Cueson is still ineligible for public site preparation;
- execution halts for Gate 2.

## Focused source and site verification

After current Gate 2 approval is recorded:

```text
.\.venv\Scripts\python.exe scripts/test_cueson_identity_study.py
.\.venv\Scripts\python.exe scripts/test_package_release.py
.\.venv\Scripts\python.exe scripts/test_release_contract.py
.\.venv\Scripts\python.exe scripts/test_prepare_site.py
.\.venv\Scripts\python.exe skill/templates/test_glyphkit.py
.\.venv\Scripts\python.exe skill/templates/test_brand_contract.py
.\.venv\Scripts\python.exe skill/templates/test_iconkit.py
.\.venv\Scripts\python.exe skill/templates/test_pipeline.py
.\.venv\Scripts\python.exe scripts/check_markdown.py
.\.venv\Scripts\python.exe skill/templates/probe.py
.\.venv\Scripts\python.exe scripts/build_all.py
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected:

- seven production kits build successfully;
- every Cueson constructed derivative reports zero glyph failures;
- the Cueson kit reports zero verification problems;
- site preparation includes Cueson only after Gate 2 and consumes generated values;
- archive, registry, metadata, structured-data, download, social, and guideline coverage includes Cueson;
- the exact slogan and description are preserved;
- no generated output is tracked.

## Repository integrity

```text
git diff --check
git status --short
git ls-files dist site/out site/generated site/public/brand
```

Expected: no whitespace errors, no unexpected tracked generated output, UTF-8 without BOM, LF line endings, no mojibake, no private paths, and only intended S026 source, test, changelog, and Spec Kit changes.

## Pull request and hosted review

After the local gate passes, push the authorized branch and open the official pull request closing #184. Record the exact branch head, CI checks, security feedback, automatic Codex round, optional single second-round request, responses, thread resolution, and final owner-ready state in `evidence.md`. Do not merge, tag, release, deploy, import into Cueson, or activate `cueson.io`.
