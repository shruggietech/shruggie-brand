# Quickstart: Validate Compact egui Desktop Density

## Focused generator and native checks

```powershell
.venv\Scripts\python skill/templates/test_egui_adapter.py
```

Expected result: deterministic generation passes, adapter version is 1.0.1, generated Cargo tests pass, fine-pointer compact controls remain at most 24 points, conservative targets remain at least 44 points, and compact vertical row spacing remains at most 2 points.

## Build and verify ESO Weave

```powershell
.venv\Scripts\python scripts/build_all.py eso-weave
.venv\Scripts\python dist/eso-weave/build/verify.py dist/eso-weave
.venv\Scripts\python dist/eso-weave/build/validate_glyph.py dist/eso-weave
```

Expected result: ESO Weave reports `BUILD CLEAN`, zero verifier problems, zero glyph failures, egui adapter 1.0.1, and unchanged approved identity sources. Inspect the generated native adapter only; do not commit `dist/`.

## Full CI parity

Run the commands in `.github/workflows/build.yml`: Python 3.8 compilation and contract tests, Python 3.12 generator/publication tests, approved proof generation, all production kit builds, release certification, generated-agent diff, site lint/build/test, and publication audit.

Expected result: every documented gate passes with generated output remaining ignored.

## Consumer adoption note

Downstream native consumers regenerate or install the corrected kit, verify the pinned `native/egui/adapter.json` reports 1.0.1, and replace the prior generated adapter bytes. ESO Weave-specific resource meters and application layout remain consumer-owned and unchanged by this slice.
