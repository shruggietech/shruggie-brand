# Quickstart: CTA Role Consistency

## Prerequisites

- Work from the repository root on `codex/032-cta-role-consistency`.
- Use the existing local Python environment and installed site dependencies.
- Chromium, PDF rendering tools, and the approved I Heart PR Tours identity proof bundle must be available for full parity.

## 1. Run focused generator regressions

```powershell
.\.venv\Scripts\python.exe skill\templates\test_pipeline.py
```

Expected: CTA token, portable-guide, PDF semantic, language, and existing pipeline tests pass.

## 2. Rebuild I Heart PR Tours

```powershell
.\.venv\Scripts\python.exe skill\templates\build_kit.py brands\i-heart-pr-tours
```

Expected: `verify.py` reports zero problems and `validate_glyph.py` reports zero failures. Generated artifacts remain under ignored `dist/` output.

## 3. Inspect the generated artifacts

- Open `dist/i-heart-pr-tours/guidelines/i-heart-pr-tours-portable-guidelines.html` and confirm every primary CTA uses the red token in both theme wells and Type and components.
- Render `dist/i-heart-pr-tours/brand-guide.pdf` to page images and inspect every page.
- Extract PDF text and confirm `#C5342C`, the CTA role, and American-English forms appear as specified.
- Confirm logo source bytes and identity-continuity evidence are unchanged.

## 4. Build and verify publication output

Run the commands documented by `.github/workflows/build.yml`, including Python compatibility suites, all-kit generation, release certification, generated-agent diff, site lint/build/test, publication audit, Markdown audit, and repository hygiene.

Expected outcomes:

- all eight production kits build cleanly;
- CTA foreground/fill pairs meet WCAG 2.1 AA;
- the portable guide's computed CTA states pass browser checks;
- every PDF page passes visual and text inspection;
- all site routes pass desktop/mobile accessibility verification;
- no generated outputs are staged for commit.
