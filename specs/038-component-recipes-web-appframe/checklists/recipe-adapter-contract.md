# Recipe and Adapter Contract Checklist: Component Recipes and Web AppFrame

**Purpose**: Review whether the S038 requirements fully constrain the bounded recipe grammar, accessible Web/React adapter, and single-owner AppFrame boundary
**Created**: 2026-09-17
**Feature**: [spec.md](../spec.md)

**Note**: This is a reviewer-owned requirements-quality artifact. An unchecked marker records pending reviewer evaluation, not incomplete implementation.

## Recipe Boundary

- [ ] CHK001 Does the specification name every initial component family and exclude arbitrary screen composition clearly enough to prevent grammar expansion by implication? [Completeness, Spec FR-002, FR-004]
- [ ] CHK002 Does each required recipe dimension have an independently verifiable meaning, including variants, densities, states, semantics, keyboard behavior, target size, icons, naming, focus, motion, responsiveness, and overrides? [Clarity, Spec FR-003]
- [ ] CHK003 Are invalid role references, raw values, state combinations, invariant overrides, and unbounded composition covered by explicit rejection requirements? [Coverage, Spec FR-004 to FR-006]
- [ ] CHK004 Are brand expression and invariant accessibility boundaries distinguished without permitting identity or affiliation drift? [Consistency, Spec FR-006]

## Adapter and Accessibility

- [ ] CHK005 Does the specification distinguish framework-neutral token consumption from React component consumption? [Clarity, Spec FR-008, FR-009]
- [ ] CHK006 Are server-safe and client-interactive boundaries explicit for both Next.js and Vite consumers? [Coverage, Spec FR-009, FR-012]
- [ ] CHK007 Are keyboard, focus, naming, relationship, target, announcement, dismissal, validation, reduced-motion, forced-color, and scaled-text requirements stated for the components that need them? [Completeness, Spec FR-011, FR-018]
- [ ] CHK008 Is the headless dependency decision constrained so BrandBuilder remains authoritative regardless of the selected implementation? [Consistency, Spec FR-020]

## AppFrame Ownership

- [ ] CHK009 Does every application-level responsibility have exactly one declared owner, including safe areas, titlebar avoidance, root scrolling, fixed chrome, IME obstruction, and global focus? [Completeness, Spec FR-014, FR-015]
- [ ] CHK010 Are browser, Tauri-style, and Wails-style host handoffs defined by capability and ownership rather than operating-system identity? [Clarity, Spec FR-013, FR-016]
- [ ] CHK011 Are duplicate and missing ownership declarations required to fail closed? [Edge Case, Spec FR-015]

## Verification and Scope

- [ ] CHK012 Do success criteria require deterministic output, complete catalog coverage, all-brand verification, and traceability to semantic roles? [Measurability, Spec SC-001 to SC-010]
- [ ] CHK013 Is S038's specimen work clearly separated from the cross-runtime conformance system in #217 and final compatibility policy in #218? [Scope, Spec Out of Scope]

## Notes

- Reviewers mark items only after evaluating requirements quality.
