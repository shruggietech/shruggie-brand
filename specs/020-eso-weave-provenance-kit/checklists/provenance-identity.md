# Provenance and Identity Requirements Quality Checklist: ESO Weave

**Purpose**: Review whether S020 requirements are complete, precise, and internally consistent enough to prevent provenance overclaiming, identity drift, false affiliation, stale approval, and premature publication.
**Created**: 2026-09-07
**Audience**: Pull-request and owner reviewers before implementation and at both approval gates
**Ownership**: `[x]` means a reviewer determined that the requirements-quality criterion is satisfied. It does not indicate implementation completion. `$speckit-implement` reads this state but does not modify it.

## Provenance Completeness

- [ ] CHK001 Does the specification distinguish every operator-supplied provenance fact from independently observable public history? [Completeness, Spec §FR-003]
- [ ] CHK002 Are synchronized revision, retrieval timing, path mapping, and hash-comparison requirements defined for every authoritative input? [Completeness, Spec §FR-001 through FR-004]
- [ ] CHK003 Does the inventory requirement cover identity masters, fonts, licensing, reproduction material, rendered references, product voice, and historical specification evidence? [Coverage, Spec §FR-002]
- [ ] CHK004 Is the treatment of moved or removed upstream paths explicit enough to prevent stale evidence from being silently recreated? [Clarity, Spec §FR-004]
- [ ] CHK005 Are source-drift and mid-slice upstream-advance cases tied to approval invalidation rules? [Recovery, Spec §FR-009 and Edge Cases]

## Identity Preservation

- [ ] CHK006 Is the prohibition on modifying authoritative SVG bytes and path data absolute and testable? [Clarity, Spec §FR-005]
- [ ] CHK007 Are the load-bearing characteristics and proof contexts required before any constructed derivative is approved? [Completeness, Spec §FR-012]
- [ ] CHK008 Does every required derivative have a stated source dependency, allowed transformation boundary, forbidden transformation boundary, measurement set, and recommendation? [Completeness, Spec §FR-012 through FR-014]
- [ ] CHK009 Is reduced-use behavior specified for the case where the badge-less glyph fails at small sizes? [Edge Case, Spec §User Story 2 and Edge Cases]
- [ ] CHK010 Is the specification explicit that inability to comply faithfully causes a stop rather than an approximation? [Exception Flow, Spec §FR-014]

## Affiliation and Legal Boundaries

- [ ] CHK011 Is third-party ownership separated from showcase permission, inheritance, endorsement, service credit, and parentage? [Consistency, Spec §FR-006]
- [ ] CHK012 Is the sole permitted ShruggieTech credit exact, and are ownership, endorsement, maintenance, and warranty claims expressly forbidden? [Clarity, Spec §FR-006 through FR-007]
- [ ] CHK013 Are independent emphasis and action colors required without accidental inheritance of house orange? [Consistency, Spec §FR-008]
- [ ] CHK014 Are the contexts requiring the game-vendor disclaimer defined broadly enough to prevent implied official status? [Coverage, Spec §FR-017]
- [ ] CHK015 Do negative-test requirements cover every prohibited affiliation combination and forbidden generated claim? [Coverage, Spec §FR-018]

## Typography and Input Governance

- [ ] CHK016 Are fixed-font hash, internal metadata, license, local-delivery, and offline-use requirements complete? [Completeness, Spec §FR-010]
- [ ] CHK017 Is additional-font ingestion blocked on a distinct evidence-backed owner approval instead of inferred from naming or availability? [Clarity, Spec §FR-011]
- [ ] CHK018 Are color-profile and usage-basis fields required for both authoritative and reference-only visual inputs? [Completeness, Spec §FR-002]

## Publication and Completion

- [ ] CHK019 Is the second approval packet defined with every artifact needed to judge the completed representation and exact public scope? [Completeness, Spec §FR-021]
- [ ] CHK020 Is publication fail-closed before approval and after any approved hash drifts? [Recovery, Spec §FR-022 and User Story 4]
- [ ] CHK021 Are generated-output boundaries consistent with the constitution and the need to retain auditable approval evidence? [Consistency, Spec §FR-020]
- [ ] CHK022 Are glyph, kit, accessibility, full-build, CI, and review completion signals all objective and non-waivable? [Measurability, Spec §FR-019 and FR-024]
- [ ] CHK023 Is the exact public-surface set defined as an approval object rather than an open-ended permission? [Clarity, Spec §FR-021 through FR-023]
- [ ] CHK024 Does issue traceability make closure contingent on the entire provenance-plus-kit outcome rather than a partial artifact? [Traceability, Spec §FR-025]

## Notes

- This checklist intentionally focuses on the two irreversible risks in S020: identity movement and misleading public affiliation.
- Items remain reviewer-owned and unchecked until reviewed.
