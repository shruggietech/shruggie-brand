# Native Roles Checklist: Native Host Icon and State Conformance

**Purpose**: Reviewer-owned quality review of native-role requirements before merge.
**Created**: 2026-09-23
**Feature**: [spec.md](../spec.md)

**Review Ownership**: `[x]` means the reviewer has approved requirements quality, not implementation completion. New items remain unchecked for reviewer evaluation.

## Requirement Completeness

- [ ] CHK001 Are each PWA, Android, Apple, Win32, and MSIX role and host surface explicitly identified? [Completeness, Spec §FR-008]
- [ ] CHK002 Are enabled, disabled, status, hover, focus, and theme text/state requirements defined without conflating semantic states? [Completeness, Spec §FR-002]
- [ ] CHK003 Are consumer resource selection and repin boundaries defined separately from generated-kit correctness? [Completeness, Spec §FR-004]

## Requirement Clarity and Consistency

- [ ] CHK004 Are alpha, background, and safe-content rules unambiguous for transparent foregrounds versus opaque backgrounds? [Clarity, Spec §FR-005-007]
- [ ] CHK005 Are logo geometry preservation and approved-color reuse consistent with the proposed composition changes? [Consistency, Spec §FR-010]
- [ ] CHK006 Are normative WCAG thresholds distinguished from the additional disabled-label readability requirement? [Clarity, Spec §FR-002]

## Acceptance and Edge Cases

- [ ] CHK007 Can mask coverage and small-size appearance be objectively measured for the three specified mask types and two themes? [Measurability, Spec §SC-002]
- [ ] CHK008 Are older pinned packages and absent optional raster capability addressed without false pass claims? [Coverage, Spec §Edge Cases]
- [ ] CHK009 Are role-specific negative scenarios specified for accidental plates, uncovered masks, and wrong declarations? [Coverage, Spec §FR-009]
- [ ] CHK010 Is the all-kit, glyph, source-continuity, and CI completion signal sufficient for the final owner review? [Acceptance Criteria, Spec §FR-010-012]

## Notes

Reviewer may mark items only after assessing the written requirements. This checklist is not an implementation task list.
