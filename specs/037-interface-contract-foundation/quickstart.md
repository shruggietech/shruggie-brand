# Quickstart: Verify the Interface Contract Foundation

## 1. Run focused contract tests

```powershell
.venv\Scripts\python skill/templates/test_interface_contract.py
.venv\Scripts\python skill/templates/test_pipeline.py
.venv\Scripts\python scripts/test_package_release.py
```

Expected result: canon validation, mixed runtime profiles, mode routing, instruction synchronization, deterministic generation, governed-block preservation, checksum mutation, offline recovery, and archive certification all pass.

## 2. Validate every production source

```powershell
.venv\Scripts\python scripts/build_all.py --list
.venv\Scripts\python scripts/build_all.py
```

Expected result: every production brand resolves the shared Interface Canon without an identity migration and every build completes cleanly.

## 3. Inspect one generated consumer contract

Open `dist/shruggietech/enforcement/consumer-contract.json` and confirm exact Brand Canon, Interface Canon, compiler, and brand versions; renderer and host declarations; adapter versions; governed provenance checksums; offline bundled distribution path and hash; verification entry point; and capability-gap path.

Confirm `dist/shruggietech/enforcement/AGENTS.md` contains exactly one governed marker pair and points to `IMPLEMENTATION.md`. Generate a second time and compare the contract outputs byte-for-byte.

## 4. Run production gates

```powershell
.venv\Scripts\python skill/templates/verify.py dist/shruggietech
.venv\Scripts\python skill/templates/validate_glyph.py dist/shruggietech/brand.json
.venv\Scripts\python scripts/package_release.py
```

Expected result: zero verification problems, zero glyph failures, and release archive certification that requires and validates the consumer contract and exact recovery distribution.

## 5. Run full repository parity

Run every command documented in `CONTRIBUTING.md` and `.github/workflows/build.yml`, including Python compilation, all script and template suites, all-kit generation, synchronized instruction diff, site lint/build/test, and publication audit. Delete no source files and commit no generated output.
