# Quickstart: Verify the Glitchpad AppFrame Adoption Pilot

## 1. Validate upstream contracts

Run from `A:/Code/shruggie-brand`:

```powershell
.venv\Scripts\python.exe skill/templates/test_component_contract.py
.venv\Scripts\python.exe skill/templates/test_web_react_adapter.py
.venv\Scripts\python.exe skill/templates/test_interface_contract.py
.venv\Scripts\python.exe skill/templates/test_pipeline.py
.venv\Scripts\python.exe scripts/test_release_contract.py
.venv\Scripts\python.exe scripts/test_package_release.py
```

Expected: full-bleed layout, dependency-free environment entry, compatibility, recovery, provenance, negative mutations, and existing adapter behavior all pass.

## 2. Rebuild every production kit

```powershell
.venv\Scripts\python.exe scripts/build_all.py
```

Expected: all eight production kits report `BUILD CLEAN`, zero verifier problems, and zero glyph failures. Generated output remains under ignored `dist/`.

## 3. Import the exact candidate downstream

After the upstream pull-request Build run succeeds, download its `verified-brand-kits` artifact and run Glitchpad's existing importer with the exact upstream revision, workflow run ID, artifact ID, and retrieval date. Never copy or edit individual generated files.

Expected: `brand/manifest.json` and `brand/INTEGRATION.json` bind the adopted bytes and upstream candidate. `pnpm check:brand` reports no drift.

## 4. Validate the Glitchpad consumer

Run Glitchpad's focused checks through its approved hidden Docker launcher on Windows, then run the aggregate gate:

```powershell
scripts/invoke-docker-hidden.ps1 -DockerArguments @('run', '--rm', '--volume', "${PWD}:/workspace", '--workdir', '/workspace', 'glitchpad-validation', 'pnpm', 'run', 'check:brand')
scripts/invoke-docker-hidden.ps1 -DockerArguments @('run', '--rm', '--volume', "${PWD}:/workspace", '--workdir', '/workspace', 'glitchpad-validation', 'pnpm', 'run', 'check:frontend')
scripts/invoke-docker-hidden.ps1 -DockerArguments @('run', '--rm', '--volume', "${PWD}:/workspace", '--workdir', '/workspace', 'glitchpad-validation', 'pnpm', 'run', 'check:shell-layout')
scripts/invoke-docker-hidden.ps1 -DockerArguments @('run', '--rm', '--volume', "${PWD}:/workspace", '--workdir', '/workspace', 'glitchpad-validation', 'cargo', 'xtask', 'check')
```

Expected: brand integrity, frontend, shell layout, accessibility, documentation, Rust, packaging, and aggregate checks pass without a visible console window.

## 5. Verify actual consumer hosts in CI

- Android API 24 and API 36 jobs build the x86_64 Tauri application and run AppFrame ActivityScenario/WebView instrumentation for portrait, landscape, IME, menu, scroll-root, and ownership evidence. API 36 also exercises an available system display-cutout overlay.
- Windows jobs build the Tauri host and run the existing narrow, normal, scale, keyboard, menu, and document lifecycle smoke with AppFrame assertions.

Expected: both evidence classes identify the exact Glitchpad candidate revision and pass independently. A missing or substituted class blocks completion.

## 6. Verify evidence and repository hygiene

```powershell
.venv\Scripts\python.exe scripts/check_markdown.py
git diff --check
git status --short
```

Expected: `evidence.md` links both pull requests and host results, records all six pilot observations and limitations, no `.specify/feature.json` is staged, and no upstream generated kit, screenshot, archive, site export, or native target is tracked.
