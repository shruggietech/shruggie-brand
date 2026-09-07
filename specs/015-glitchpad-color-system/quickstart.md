# Quickstart: Glitchpad Identity Color Approval

## Stage A: Generate decision evidence

From the repository root on `codex/015-glitchpad-color-system`:

```powershell
python scripts/glitchpad_color_study.py --output dist/.s015-color-study
```

Expected: protected geometry fingerprint passes; `comparison.html`, `comparison.svg`, and `measurements.json` are generated under the ignored output directory; the focused owner-approved Revision 3 direction and every required context are present; the study itself makes no production-source mutation.

Render the comparison document at its declared viewport and inspect the output at full size. Review exact role values and contrast dispositions in `measurements.json`. Verify that any failing relationship is visibly labeled rather than omitted.

Confirm the source boundary:

```powershell
git status --short
git diff -- brands/glitchpad/brand.json skill/templates/gen_logo.py skill/templates/iconkit.py
```

Expected before approval: only S015 source and Spec Kit work appears; the current Glitchpad production identity and production generator remain unchanged.

## Owner approval gate

Present the comparison, recommendation, exact role matrix, measurements, and tradeoffs. Halt. Continue only after the owner approves a direction or requests a bounded adjustment.

## Stage B: Post-approval focused gate

After the approved matrix is recorded, run tests for brand-contract validation, logo generation, icon generation, pipeline output, and site preparation before and after implementation. Confirm the pre-change protected geometry fingerprint remains unchanged.

## Stage B: Complete gate

Run the complete validation documented in `CONTRIBUTING.md` and `.github/workflows/build.yml`, including Python 3.8 compatibility in hosted CI, every production kit, glyph validation, release contracts, generated-agent synchronization, TypeScript, static export, browser verification, WCAG 2.1 AA, Markdown, UTF-8 without BOM, LF, mojibake, ignored artifacts, and `git diff --check`.
