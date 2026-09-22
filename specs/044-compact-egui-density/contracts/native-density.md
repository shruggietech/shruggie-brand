# Contract: Native egui Density Correction

## Generated API compatibility

The generated public Rust functions, enums, structs, module names, crate dependency, MSRV, and file layout remain compatible with adapter 1.0.0. Adapter 1.0.1 changes generated style behavior only.

## Default style application

`apply_style` represents a fine-pointer desktop default. It applies the selected density to visual control height, button padding, and item spacing, then grows the height if scaled body text would clip.

## Capability-aware style application

`apply_capabilities` validates the runtime profile before applying style. Fine pointer without touch uses compact visual control height. Coarse, mixed, unknown, or touch-capable input uses the invariant 44-point minimum target. System theme continues to install both light and dark styles before selecting host preference.

## Density and spacing

- Comfortable fine-pointer control height is 28 points at normal text scale.
- Compact fine-pointer control height is 22.96 points at normal text scale and MUST NOT exceed 24 points.
- Compact vertical item spacing MUST NOT exceed 2 points at normal text scale.
- Coarse, mixed, unknown, and touch-capable targets remain at least 44 points in both densities.
- Text scaling increases final height whenever scaled body text plus generated padding exceeds the profile height.

## Verification

Python generation tests assert adapter identity, deterministic output, expected generated capability branches, and fail-closed tamper behavior. Generated Cargo tests use real egui frames and style inspection to cover comfortable and compact fine-pointer controls, coarse and touch targets, mixed input, text scaling, dense row spacing, focus, accessible names, invalid units, and invalid capabilities.

No generated crate or kit is committed.
