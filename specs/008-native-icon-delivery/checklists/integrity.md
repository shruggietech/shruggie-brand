# Icon Contract Checklist: Native Icon Delivery and Favicon Integrity

**Purpose**: Review whether S008 requirements fully define platform packaging, geometry preservation, failure behavior, migration, and public-site integrity
**Created**: 2026-09-05
**Feature**: [spec.md](../spec.md)

**Review Ownership**: This checklist is a requirements-quality review artifact. The autopilot review recorded below evaluates specification quality, not implementation completion.

## Requirement Completeness

- [x] CHK001 Are all five platform suite boundaries and their required artifact roles explicitly defined? [Completeness, Spec FR-001 through FR-023]
- [x] CHK002 Are the human index, platform instructions, machine manifest, and native metadata obligations all specified? [Completeness, Spec FR-002, FR-003, FR-023]
- [x] CHK003 Is the legacy `favicons/` migration behavior defined without creating a second source of truth? [Completeness, Spec FR-004]
- [x] CHK004 Are lower capability and stale-output behaviors explicitly defined? [Completeness, Spec FR-024, FR-025]

## Geometry and Visual Integrity

- [x] CHK005 Are geometry-preservation rules consistent for constructed, supplied, rectangular, and raster-backed marks? [Consistency, Spec FR-005 and Edge Cases]
- [x] CHK006 Are reduced-mark selection and safe-area expectations measurable? [Clarity, Spec FR-009, FR-012]
- [x] CHK007 Are opaque and transparent roles distinguished for every platform context? [Clarity, Spec FR-010, FR-012, FR-016, FR-021]
- [x] CHK008 Is the application-icon background an explicit brand contract with a deterministic fallback? [Completeness, Spec FR-006]

## Native Platform Coverage

- [x] CHK009 Are Android legacy, adaptive, monochrome, XML, density, and Play listing requirements distinct and measurable? [Coverage, Spec FR-011 through FR-014]
- [x] CHK010 Are Apple mobile appearance inputs and macOS all-sizes, asset-catalog, and container requirements distinct? [Coverage, Spec FR-015 through FR-018]
- [x] CHK011 Are Windows classic, scale, target-size, appearance, store, and manifest requirements all specified? [Coverage, Spec FR-019 through FR-022]
- [x] CHK012 Are platform-applied masks and shadows explicitly excluded from source artwork where required? [Clarity, Spec FR-014, FR-016]

## Verification and Publication

- [x] CHK013 Are corrupt, empty, missing, wrong-size, wrong-alpha, malformed, unsafe, colliding, and stale cases all covered? [Coverage, Spec FR-024 through FR-028, FR-031, FR-034]
- [x] CHK014 Does the site contract require generated kit consumption and reject raw-source fallback masking? [Consistency, Spec FR-029]
- [x] CHK015 Are route coverage and every published icon relationship explicit? [Completeness, Spec FR-030 through FR-032]
- [x] CHK016 Are shippability, accessibility, source-only Git, and encoding gates preserved? [Consistency, Spec FR-034, FR-035, SC-010, SC-011]

## Scope and Traceability

- [x] CHK017 Is issue closure explicitly limited to #106 and #110? [Scope, Spec FR-036]
- [x] CHK018 Are #108, #109, and #111 explicitly excluded without weakening their future outcomes? [Scope, Spec Assumptions]
- [x] CHK019 Does the specification preserve pre-existing product icon bytes while retaining exact inventory enforcement? [Conflict resolution, Spec FR-037]

## Notes

- Requirements-quality review completed under the operator-authorized S008 autopilot protocol on 2026-09-05.
- `[x]` records requirements-quality approval only; implementation completion is tracked in `tasks.md`.
