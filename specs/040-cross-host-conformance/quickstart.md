# Quickstart: Validate Cross-Host Conformance

Run from the repository root with the declared Python, Node, Rust, Go, and rendering dependencies installed.

## 1. Contract and generator checks

```powershell
python skill/templates/test_conformance.py
python skill/templates/test_web_react_adapter.py
python skill/templates/test_egui_adapter.py
python skill/templates/test_pipeline.py
```

Expected: the canonical policy, known-bad and corrected traces, evidence substitution, diagnostics, baseline decisions, deterministic generation, existing Web adapter, egui adapter, and full pipeline tests pass.

## 2. Build every production kit

```powershell
python scripts/build_all.py
```

Expected: all eight production brands report `BUILD CLEAN`, zero `verify.py` problems, zero glyph failures, and complete generated conformance manifests. Generated output remains under ignored `dist/`.

## 3. Execute generated host fixtures

```powershell
cargo test --manifest-path dist/glitchpad/conformance/hosts/tauri-android/Cargo.toml --locked
go -C dist/go-schedule/conformance/hosts/wails-windows test ./...
cargo test --manifest-path dist/eso-weave/native/egui/Cargo.toml --locked
```

Expected: Tauri rejects the canonical known-bad trace and passes the corrected trace, Wails passes titlebar and resize traces, and egui passes native rendered-state evidence. Each result remains reference-fixture evidence rather than consumer adoption.

## 4. Build and verify the public browser reference

```powershell
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: `/conformance/` lists every production brand, every `/conformance/{slug}/` route uses staged generated kit data, required profiles pass Playwright and axe checks, and screenshot candidates are written below ignored `site/test-results/visual/`.

## 5. Verify publication and repository hygiene

```powershell
python scripts/audit_publication_artifacts.py --kits dist --site site/out
python scripts/check_markdown.py
git status --short
```

Expected: publication contains exactly the governed production brands and verified site data, Markdown passes, and no generated kit, screenshot, host target, site export, or `.specify/feature.json` is staged.
