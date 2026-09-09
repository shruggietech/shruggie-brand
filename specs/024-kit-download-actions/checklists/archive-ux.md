# Archive and Portfolio UX Checklist: Complete Kit Downloads and Explicit Brand Actions

**Purpose**: Review whether the archive and interaction requirements are complete, measurable, internally consistent, and traceable before implementation
**Created**: 2026-09-09
**Feature**: [spec.md](../spec.md)

**Note**: This custom checklist is a reviewer-owned requirements-quality review artifact. Mark an item `[x]` only when the reviewer determines the requirements-quality criterion is satisfied.
**Review Ownership**: `[x]` means the criterion has been reviewed and satisfied for requirements quality. It does not mean implementation work is complete.

## Archive Authority and Completeness

- [x] CHK001 Is the authoritative source for the complete distributable inventory identified without permitting a second hand-maintained site inventory? [Spec §Assumptions, FR-001, FR-002]
- [x] CHK002 Are archive failure conditions exhaustive for missing, stale, corrupt, empty, unsafe, duplicate-normalized, out-of-root, and unrecorded entries? [Spec FR-003; Data Model §ProductionBrandArchive]
- [x] CHK003 Are redistribution exceptions required to identify both the omitted delivery and its reason? [Spec FR-004]
- [x] CHK004 Are archive determinism requirements measurable across paths, ordering, timestamps, permissions, compression, metadata, and bytes? [Spec FR-005, SC-002; Contract §Archive contract]
- [x] CHK005 Is verification-before-replacement explicit enough to prevent a failed build from replacing the last valid archive? [Research Decision 2; Data Model §State Transitions]
- [x] CHK006 Is the relationship between the release archive and site archive unambiguous for identical inputs? [Contract §Archive contract]
- [x] CHK007 Are stable public path, version-aware filename, media type, and browser download behavior all specified for static hosting? [Spec FR-005, FR-006; Research Decision 3]

## Desktop Interaction

- [x] CHK008 Does the specification make exactly two anchors the only interactive card elements and exclude implicit navigation from all remaining card space? [Spec FR-008, FR-009]
- [x] CHK009 Are hover-to-action pointer continuity and keyboard focus-within behavior both covered? [Spec US2 scenarios 1-2, FR-010]
- [x] CHK010 Is card geometry invariance measurable across rest, hover, and keyboard focus states? [Spec SC-003]
- [x] CHK011 Are readable transition and reduced-motion requirements stated without depending on a particular decorative animation? [Spec FR-010, FR-018]

## Mobile Disclosure

- [x] CHK012 Are collapsed and expanded contents specified in exact reading order? [Spec FR-011, FR-013]
- [x] CHK013 Are disclosure semantics, expanded state, controlled content, focus visibility, and touch target requirements complete? [Spec FR-012]
- [x] CHK014 Does the closed-state requirement exclude hidden action controls from pointer and sequential keyboard access? [Spec US3 scenario 3, FR-013]
- [x] CHK015 Are narrow viewport, 200% zoom, long-name, and breakpoint-transition cases covered? [Spec Edge Cases, FR-018]
- [x] CHK016 Is no-JavaScript availability required for both guidelines and download actions? [Spec FR-019]

## Shared Data and Attribution

- [x] CHK017 Is one generated portfolio record required to supply identical brand content and destinations to both responsive presentations? [Spec FR-014; Contract §Generated portfolio record]
- [x] CHK018 Is marker applicability derived solely from authoritative vendor-boundary data? [Spec FR-017; Research Decision 6]
- [x] CHK019 Are exactly-one placement, full notice wording, accessible association, and non-applicable brand behavior all specified? [Spec FR-016, FR-017, SC-006]

## Verification and Traceability

- [x] CHK020 Do automated requirements collectively cover file integrity, mappings, interaction states, accessibility, static export, and repository hygiene? [Spec FR-020, SC-007]
- [x] CHK021 Does every success criterion define an observable result rather than an implementation detail? [Spec §Success Criteria]
- [x] CHK022 Are GitHub issues #173 and #174 mapped to their applicable requirements and outcomes? [Spec §Traceability]
- [x] CHK023 Are neighboring backlog items #175, #179, and #180 explicitly excluded to prevent navigation scope creep? [Spec §Assumptions]

## Notes

- Mark items `[x]` only after review confirms the requirement-quality criterion is satisfied.
- Leave items unchecked when they still require clarification, correction, or reviewer evaluation.
- `$speckit-implement` reads checklist checkbox state as a gate and must not modify markers.
- `checklists/requirements.md` has a separate built-in lifecycle maintained by `$speckit-specify` and `$speckit-clarify`.
