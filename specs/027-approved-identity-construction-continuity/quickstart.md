# Quickstart: Approved Identity Construction Continuity

Run from the repository root on `codex/027-approved-identity-construction-continuity` with `.specify/feature.json` selecting this specification. Generated evidence remains beneath ignored `dist/` paths.

## 1. Focused contract and security tests

```powershell
.\.venv\Scripts\python.exe skill\templates\test_identity_continuity.py
.\.venv\Scripts\python.exe scripts\test_identity_continuity_audit.py
.\.venv\Scripts\python.exe skill\templates\test_brand_contract.py
.\.venv\Scripts\python.exe skill\templates\test_pipeline.py
```

Expected: valid canonical and historical records pass; every source, method, geometry, topology, framing, palette, renderer, proof, transition, traversal, symlink, duplicate, malformed-hash, and unauthorized-destination case has an explicit passing regression test.

## 2. Audit migrated identities

```powershell
.\.venv\Scripts\python.exe scripts\audit_identity_continuity.py --check --output dist\identity-continuity-audit.json
```

Expected: all seven production brands have one valid classification and unchanged current-source snapshot; Cueson is the corrected regression baseline; Covarity is a documented legacy construction; no record claims retrospective approval; zero identity path, palette, framing, or public-eligibility drift is present.

## 3. Exercise the synthetic Cueson regression

```powershell
.\.venv\Scripts\python.exe skill\templates\test_identity_continuity.py IdentityContinuityTests.test_cueson_equivalent_renderer_fixture_passes
.\.venv\Scripts\python.exe skill\templates\test_identity_continuity.py IdentityContinuityTests.test_cueson_reconstruction_and_framing_drift_fails
```

Expected: the equivalent production construction passes exact structural and edge-aware checks; the rejected alternate construction or occupancy shift fails before derivative eligibility. Reviewable side-by-side, overlay, XOR, and color-difference fixtures are emitted only to a temporary or ignored directory.

## 4. Run the Python and contract matrix

```powershell
.\.venv\Scripts\python.exe skill\templates\test_glyphkit.py
.\.venv\Scripts\python.exe scripts\test_package_release.py
.\.venv\Scripts\python.exe scripts\test_release_contract.py
.\.venv\Scripts\python.exe scripts\test_prepare_site.py
.\.venv\Scripts\python.exe skill\templates\test_brand_contract.py
.\.venv\Scripts\python.exe skill\templates\test_iconkit.py
.\.venv\Scripts\python.exe skill\templates\test_pipeline.py
.\.venv\Scripts\python.exe scripts\check_markdown.py
```

Expected: every test passes on the supported local runtime, with minimum Python 3.8 compatibility covered by hosted CI.

## 5. Build and verify all production kits

```powershell
.\.venv\Scripts\python.exe skill\templates\probe.py
.\.venv\Scripts\python.exe scripts\build_all.py
```

Expected: all seven production identities validate continuity before derivatives, every kit reports zero verification problems, all applicable marks report zero glyph failures, and generated continuity reports match committed source records.

## 6. Certify release metadata without publishing

```powershell
$version = & .\.venv\Scripts\python.exe scripts\release_contract.py current
.\.venv\Scripts\python.exe scripts\package_release.py --version $version
.\.venv\Scripts\python.exe scripts\release_contract.py notes --version $version --output release\release-notes.md
.\.venv\Scripts\python.exe scripts\release_contract.py verify --version $version --release-dir release --notes release\release-notes.md
```

Expected: current archives and metadata certify successfully. No tag or release is created.

## 7. Validate generated agent contract and site

```powershell
.\.venv\Scripts\python.exe skill\templates\sync_agents_md.py skill
git diff --exit-code -- skill\AGENTS.md
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: the generated agent instructions are synchronized, the static site exports successfully, all browser route checks pass, and WCAG 2.1 AA reports zero violations.

## 8. Audit repository hygiene

Confirm tracked text is UTF-8 without BOM with LF endings, contains no mojibake or private workstation paths, and generated `dist/`, `release/`, site export, browser result, cache, archive, PDF, PNG, registry, and `.specify/feature.json` content remains untracked. `git diff --check` and the final branch status must be clean after commit.
