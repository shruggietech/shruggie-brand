# Research: Native egui Adapter and Versioned Contracts

## R1. Native adapter boundary

**Decision**: Generate a standalone Rust library crate under `native/egui/` with typed tokens and immediate-mode helper functions. Consume the shared recipe catalog at generation time, then emit ordinary egui code rather than a renderer-neutral runtime component tree.

**Rationale**: Issue #216 requires shared semantics without React emulation. A generated crate gives Rust consumers native types, closures, `egui::Response`, and host-provided `egui::Context` while preserving traceability to the shared contract.

**Alternatives considered**: A JSON-driven runtime renderer would become a cross-renderer DSL. A React-like virtual component hierarchy would fight egui's immediate-mode model. Hand-maintained Rust copies would drift from BrandBuilder authority.

## R2. egui and test harness versions

**Decision**: Pin `egui = 0.36.1` and `egui_kittest = 0.36.1`, with generated Rust MSRV 1.88 and edition 2024.

**Rationale**: The official egui repository describes `egui_kittest` as its AccessKit-based test harness. The published 0.36.1 harness supports `Harness::new_ui_state`, accessibility-tree queries, pointer and keyboard actions, `set_pixels_per_point`, and rendering. The 0.36 line requires Rust 1.88. Exact matching versions avoid duplicate egui types and make recovery reproducible.

**Primary sources**: [egui architecture](https://github.com/emilk/egui/blob/main/ARCHITECTURE.md), [egui_kittest 0.36.1 documentation](https://docs.rs/egui_kittest/0.36.1/egui_kittest/), [egui_kittest changelog](https://github.com/emilk/egui/blob/main/crates/egui_kittest/CHANGELOG.md).

**Alternatives considered**: Snapshot-only testing adds GPU and platform image variance. Source inspection does not prove the generated widgets appear in the accessibility tree or preserve interaction state.

## R3. Component support classification

**Decision**: Classify every shared recipe as `supported`, `adapted`, or `unsupported`, with a reason, generated symbol, verified states, and evidence identifiers. Native egui primitives cover direct controls; composite web semantics are adapted to immediate-mode helpers; unsupported browser-only behavior remains explicit.

**Rationale**: Honest partial support is safer than claiming parity. Consumers can reject an unsupported requirement before integration, and later adapter releases can change classifications independently of recipes or brands.

**Alternatives considered**: Omitting unsupported entries hides gaps. Requiring identical web and native semantics would either distort egui or create a lowest-common-denominator DSL.

## R4. Logical units, density, and scaling

**Decision**: Resolve Interface Canon `lu` through its egui transform into points, then apply a closed density multiplier (`comfortable` or `compact`). Leave `pixels_per_point` to the egui context and host, and never counter-scale user text or display scaling.

**Rationale**: egui layouts use points and its context owns pixel scaling. This preserves the Interface Canon logical unit contract without inferring an operating system or hard-coding physical pixels.

**Alternatives considered**: Converting directly to device pixels would double-apply scaling. OS presets would violate the capability-based runtime contract.

## R5. Runtime capability handoff

**Decision**: Generate a closed `RuntimeCapabilities` Rust struct carrying viewport, pointer, hover, keyboard, touch, text scale, motion, colors, safe-area, IME, titlebar, theme, and density inputs. Host-specific behavior is expressed through these observed values and documented handoffs.

**Rationale**: This follows Interface Canon and lets embedded hosts report what they can actually do. It also makes unsupported behavior testable without pretending egui owns native window chrome or IME geometry.

**Alternatives considered**: Host or OS name switches are brittle and explicitly prohibited. Reading global process state inside helpers would make tests and embedding nondeterministic.

## R6. Rendered-state evidence

**Decision**: Generate `egui_kittest` integration tests that query AccessKit nodes and render frames for button input, selected controls, invalid fields, focusable controls, both densities, and two pixels-per-point settings. Use structural image dimensions and state assertions rather than committed binary snapshots.

**Rationale**: This is rendered evidence without committing generated PNGs or creating cross-platform golden-image noise. The tests still drive real egui layout, accessibility output, and state transitions.

**Alternatives considered**: Committed snapshots violate the generated-artifact boundary and are platform-sensitive. Pure Python string checks cannot establish rendered behavior.

## R7. Independent version policy

**Decision**: Add a governed `version-policy.json` that names Brand Canon, Interface Canon, component recipes, Web/React adapter, egui adapter, compiler, and brand as independent SemVer domains. Each domain declares meaning, patch, minor, and major triggers, compatibility keys, publication boundary, and recovery identity.

**Rationale**: Issue #218 requires precise independent lifecycles. A machine-readable policy allows generator, verifier, and archive certification to agree while avoiding synchronized bumps for unrelated changes.

**Alternatives considered**: Prose-only policy is easy to drift. A single suite version obscures which contract changed. Coupling adapter versions to brand versions would force unnecessary kit upgrades.

## R8. Compatibility records

**Decision**: Consumer contracts carry exact versions plus a compatibility record derived from the policy and adapter manifests. Generation fails when declared compatibility excludes a resolved dependency. Verification re-derives the same relationships from bundled authority.

**Rationale**: Exact pins alone identify bytes but do not say whether combinations are valid. Compatibility ranges alone cannot recover exact bytes. Both are needed.

**Alternatives considered**: Implicit compatibility through release date or compiler version is ambiguous. Automatically selecting the newest adapter violates exact recovery.

## R9. Recovery and release separation

**Decision**: Keep delivered offline BrandBuilder bytes as the primary recovery source, add exact contract identities and checksums, and distinguish contract compatibility, artifact publication, and consumer adoption in policy and guidance.

**Rationale**: A later repository release must not prevent rebuilding or auditing an older consumer handoff. Publication does not imply that a consumer adopted the new contract.

**Alternatives considered**: A `latest` recovery path is non-reproducible. Treating GitHub publication as adoption would erase consumer-controlled rollout state.

## R10. Scope boundary

**Decision**: S039 closes #216 and #218 only. It does not claim the multi-host golden fixture matrix in #217 and does not modify downstream product repositories for pilot issues.

**Rationale**: The native adapter and version policy are prerequisites. Real host certification and consumer adoption need separately authorized repositories and evidence.

**Alternatives considered**: Bundling downstream changes would exceed current authorization and blur compiler evidence with consumer rollout.
