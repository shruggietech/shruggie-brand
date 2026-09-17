# Contract: Native egui Adapter

## Generated crate

- `native/egui/Cargo.toml` pins `egui` exactly and pins `egui_kittest` exactly for development evidence.
- `native/egui/Cargo.lock` pins the complete resolved dependency graph so the documented `cargo test --locked` command never performs an unlocked first resolution.
- `src/tokens.rs` exposes typed semantic colors, measurements, theme selection, logical-unit conversion, and density transforms.
- `src/components.rs` exposes ordinary egui functions and closure-based helpers. Public results use egui types such as `Response`, `InnerResponse`, `Ui`, and `Context`.
- `src/lib.rs` exports runtime capability and support types without introducing a renderer-neutral component tree.
- `tests/adapter.rs` drives real egui frames and accessibility output through `egui_kittest`.

## Support classification

Every component recipe has exactly one support record. Supported and adapted records name their Rust symbol and evidence. Unsupported records name the missing host or egui capability and have no callable symbol. A generator or verifier must reject missing, duplicate, unknown, or over-claimed records.

## Runtime and units

The adapter converts Interface Canon logical units to egui points using the declared transform, then applies the selected density multiplier. Pixels-per-point remains owned by egui and the host. Runtime decisions consume observed capabilities and explicit host geometry; operating-system routing is forbidden.

## Verification

Python tests validate deterministic generation, exact versions, complete recipe coverage, safe source, and tamper rejection. Cargo tests compile the generated crate and use `egui_kittest` to exercise input, focusability, selection, validation/error state, density, pixels-per-point scaling, and unsupported records. No generated Rust source, lockfile, rendered image, or kit is committed.
