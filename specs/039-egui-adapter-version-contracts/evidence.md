# Verification Evidence: Native egui Adapter and Versioned Contracts

**Baseline**: `a01bbd01893a2e3c41c9a5028b674a254f654c1c` on `main`

**Branch**: `codex/039-egui-adapter-version-contracts`

**Issues**: #216 and #218

## Chronological verification record

1. The Spec Kit requirements and native/version review checklists completed with every item satisfied. Primary egui 0.36.1, `egui_kittest` 0.36.1, Rust 1.88, and SemVer evidence was recorded before implementation.
2. Test-first contracts were added for deterministic native generation, complete recipe coverage, rendered egui state, independent version policy, compatibility failure, recovery integrity, archive authority, and release provenance. The new tests initially failed because the native crate, policy, schema v3 fields, and archive requirements did not exist.
3. The generator, consumer contract, verification, recovery, release certification, CI, and documentation changes were implemented. Focused suites then passed: 13 interface-contract tests, 5 component-contract tests, 4 Web adapter tests, 3 native adapter tests including generated Cargo execution, 7 package-release tests, and 19 release-contract tests.
4. Convergence review found that compact density reduced the declared interaction-target floor and that icon-button glyphs retained the wrong accessible name. The generator was corrected so density changes spacing only, every target preserves the governed minimum, and icon buttons publish their explicit accessible label.
5. Convergence review found that logical-unit and runtime transforms did not yet enforce the specification's fail-closed behavior. The generated Rust API now rejects non-finite or non-positive units, malformed viewport, safe-area, obstruction, window-class, and text-scale inputs. Text scaling starts from stable theme defaults and system theme remains host-owned.
6. Convergence review found that dependency rules constrained dependency versions but not the dependent contract generation. Compatibility edges now constrain the dependent major and fail with an explicit migration or policy-publication direction.
7. Convergence review found that compatibility validation incorrectly claimed publication and consumer adoption. Generated handoffs now record candidate and unadopted states, while immutable publication and named downstream adoption remain separate later lifecycle states.
8. The pinned full pipeline completed 68 tests with zero failures. Expected negative-fixture messages and legacy `ResourceWarning` output remained contained inside passing tests.
9. All eight production brands rebuilt with Node 24.11.0 for approved proof rendering. Every kit reported `BUILD CLEAN`, zero `verify.py` problems, zero glyph failures, and a generated native egui adapter. No brand source or approved identity geometry changed.
10. Site lint, static export, Node contract tests, Playwright route checks, and axe WCAG 2.1 AA checks completed against the rebuilt kits. The publication audit found exactly eight governed kit markers and eight governed site markers in a production-only ignored staging tree.

## Requirement coverage

| Contract | Evidence |
| --- | --- |
| Native semantic traceability | Every adapter manifest pins Brand Canon, Interface Canon, recipes, compiler, brand, egui, and version policy identities. Every recipe has a support record and generated Rust symbol. |
| Native behavior and accessibility | Generated Cargo tests exercise button input, accessible names, selection, visible validation errors, focus styling, density, text scale, pixels-per-point, system theme, and invalid runtime rejection. Unsupported host live-region and window-chrome behavior remains explicit. |
| Independent versions | The governed policy defines meaning, patch/minor/major rules, compatibility edges, lifecycle states, and publication ownership for seven domains. Consumer schema v3 records exact versions and validated compatibility. |
| Exact recovery | Checksummed provenance covers the policy, native manifests, support records, implementation guidance, and deterministic recovery bundle. Package and release tests reject missing, drifted, incompatible, or noncanonical bytes. |
| Full production safety | Eight production builds and site verification completed without source identity changes or committed generated output. |

## Scope and artifact boundary

- No consumer repository was modified and no downstream adoption is claimed.
- Cross-host golden fixtures remain tracked by #217.
- Generated kits, Cargo locks, Cargo targets, site exports, release archives, and publication-audit staging remain ignored and uncommitted.
