# Research: Cross-Host Conformance Fixtures

## Decision 1: One canonical policy, generated per-brand fixtures

**Decision**: Store the profile, host, evidence, diagnostic, trace, and baseline rules in one versioned JSON reference contract. Compile a per-brand conformance manifest and fixture tree after Web/React and egui adapter generation.

**Rationale**: This keeps BrandBuilder authoritative, binds every fixture to exact generated versions, makes all eight brands deterministic, and avoids reauthoring values in the site or host fixtures.

**Alternatives considered**:

- Hand-author fixture configuration in each runtime. Rejected because contracts would drift and brand/version identity would be duplicated.
- Treat the public site as the only fixture. Rejected because browser proof cannot certify Tauri, Wails, or egui boundaries.
- Create a general cross-renderer UI DSL. Rejected by the program architecture and unnecessary for bounded conformance states.

## Decision 2: Host-envelope fixtures are executable but composition-free

**Decision**: Generate a dependency-free Rust test crate for the Tauri Android envelope and a dependency-free Go test module for the Wails Windows envelope. Each consumes the same normalized geometry and ownership traces as the conformance contract. Keep egui evidence in the existing generated egui crate and browser evidence in the generated Web specimen plus public site.

**Rationale**: Small host-boundary fixtures execute in the language and entry point relevant to each host while avoiding heavyweight application shells, product composition, network resolution, or false downstream-adoption claims.

**Alternatives considered**:

- Build full Tauri Android and Wails applications in ordinary CI. Rejected because platform SDK and GUI-host setup would dominate a reference fixture and reduce determinism.
- Validate every host envelope only in Python. Rejected because it would not prove that host-specific fixture source compiles and agrees with the canonical contract.
- Use browser JavaScript to simulate all hosts. Rejected because it would violate the evidence substitution boundary.

## Decision 3: Evidence classes are non-substitutable

**Decision**: Use explicit `browser-reference`, `tauri-reference-host`, `wails-reference-host`, `egui-reference-renderer`, `actual-host`, and `consumer-adoption` evidence classes. A fixture can satisfy only its declared reference class. Actual-host and consumer-adoption remain pending until separately supplied.

**Rationale**: The status matrix can report useful readiness without claiming a browser run proves native hosting or that a BrandBuilder fixture proves a consumer product.

**Alternatives considered**:

- One generic `verified` flag. Rejected because it hides the difference among emulation, reference fixtures, actual hardware or OS proof, and adopted product evidence.
- Infer evidence from operating-system names. Rejected because runtime adaptation is capability-based and mixed-capability devices are expected.

## Decision 4: Visual candidates are ephemeral, decisions are governed

**Decision**: Generate screenshots and checksummed candidate manifests in ignored local or CI paths. Upload them as PR artifacts. Keep a source JSON decision ledger that is empty by default and accepts only explicit human decisions bound to an exact candidate identity and environment.

**Rationale**: Reviewers can inspect exact evidence, but agents cannot silently bless new pixels. The source/generated boundary remains intact and PNG byte identity is not used as the sole correctness gate.

**Alternatives considered**:

- Commit golden PNG files. Rejected by the repository artifact boundary and cross-platform raster instability.
- Auto-update visual baselines when tests change. Rejected because it turns regressions into accepted output.
- Omit screenshots and rely only on DOM measurements. Rejected because visual review remains necessary even when measured checks pass.

## Decision 5: Diagnostics stay separated at the source

**Decision**: Define four diagnostic classes: `visual`, `accessibility`, `interaction`, and `host-boundary`. Every failure contains one class plus brand, profile, host, subject, code, and message. Unknown classes fail validation.

**Rationale**: Reviewers can identify the owning layer and do not have to parse an undifferentiated failure stream.

**Alternatives considered**:

- Reuse the existing free-form verification report only. Rejected because it cannot guarantee class identity or support machine-readable evidence.
- Allow multiple primary classes per diagnostic. Rejected because it obscures ownership; related diagnostics should be separate records.

## Decision 6: Exact tool versions are recorded, minimums remain portable

**Decision**: Record the actual version in every executed fixture result while enforcing Python 3.8, Node.js 20, Rust 1.95, and Go 1.22 minimums. CI remains authoritative for supported build environments.

**Rationale**: The record is reproducible without increasing the project's minimums beyond existing adapter requirements. Local discovery on 2026-09-17 found Python 3.12.9, Node.js 26.5.0, pnpm 11.19.0, Rust 1.96.0, Cargo 1.96.0, and Go 1.24.2.

**Alternatives considered**:

- Pin local developer versions as new minimums. Rejected because they exceed documented consumer and CI floors without need.
- Record only minimum versions. Rejected because evidence must identify the toolchain that actually produced it.
