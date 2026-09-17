# Quickstart: Verify Native egui and Version Contracts

## 1. Run focused contract tests

```powershell
.venv\Scripts\python skill/templates/test_egui_adapter.py
.venv\Scripts\python skill/templates/test_interface_contract.py
.venv\Scripts\python scripts/test_release_contract.py
.venv\Scripts\python scripts/test_package_release.py
```

Expected result: deterministic native generation, complete support classification, independent version policy, compatibility failures, authority paths, provenance, archive certification, and exact recovery all pass. Negative fixtures fail with the named domain or path.

## 2. Generate and exercise one native crate

```powershell
.venv\Scripts\python skill/templates/gen_egui.py brands/shruggietech/brand.json dist/shruggietech
cargo test --manifest-path dist/shruggietech/native/egui/Cargo.toml --locked
```

Expected result: the generated Rust crate compiles with exact egui dependencies and `egui_kittest` proves input, focus, selection, invalid state, density, and scaling behavior.

## 3. Build every production kit

```powershell
.venv\Scripts\python scripts/build_all.py
```

Expected result: every production brand generates the native crate, reports zero verifier and glyph failures, and carries matching Brand Canon, Interface Canon, recipe, web adapter, egui adapter, compiler, and brand versions.

## 4. Run release and repository gates

```powershell
.venv\Scripts\python scripts/package_release.py
.venv\Scripts\python scripts/check_markdown.py
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected result: release certification rejects missing or incompatible version domains, the existing site remains green, and no generated output is tracked.

## 5. Run full CI parity

Run every command in `CONTRIBUTING.md` and `.github/workflows/build.yml`, including Python 3.8 checks, focused Rust generation, all template and script suites, all-brand generation, generated Rust tests, synchronized instructions, site checks, publication audit, mojibake and LF/BOM checks, `git diff --check`, and tracked-generated-artifact checks. Commit no `dist/`, Cargo target, release, or site export content.
