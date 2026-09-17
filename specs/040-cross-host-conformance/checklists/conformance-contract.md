# Cross-Host Conformance Requirements Checklist

**Purpose**: Review whether S040 requirements completely define host evidence, accessibility, safe-area regression, diagnostics, and baseline governance before implementation.
**Created**: 2026-09-17
**Feature**: [spec.md](../spec.md)

**Ownership**: `[x]` means a reviewer approved the requirements-quality criterion. Implementation work does not change these markers.

## Requirement Completeness

- [ ] CHK001 Are all required browser, Tauri, Wails, and egui evidence boundaries defined without allowing one renderer to substitute for another? [Completeness, Spec FR-007 through FR-015]
- [ ] CHK002 Are the full profile matrix and every expected capability transition specified? [Completeness, Spec FR-004 through FR-005]
- [ ] CHK003 Are known-bad, corrected, missing-proof, stale-proof, and conflicting-ownership outcomes all required? [Coverage, Spec FR-009 through FR-019]

## Requirement Clarity

- [ ] CHK004 Is the distinction among reference fixture evidence, actual host proof, and downstream consumer adoption unambiguous? [Clarity, Spec FR-008 through FR-015]
- [ ] CHK005 Are reachable controls, usable content, and single-owner boundaries expressed with measurable outcomes rather than subjective language? [Clarity, Spec FR-010 through FR-012, SC-002 through SC-003]
- [ ] CHK006 Is each baseline metadata and human-decision field stated explicitly? [Clarity, Spec FR-016 through FR-018]

## Requirement Consistency

- [ ] CHK007 Do the browser self-hosting requirements remain consistent with the prohibition on treating browser evidence as native-host proof? [Consistency, Spec FR-003, FR-009, FR-015]
- [ ] CHK008 Do ephemeral candidate requirements remain consistent with the prohibition on committed generated artifacts? [Consistency, Spec FR-016 through FR-018, FR-023]
- [ ] CHK009 Does coordination with issue #202 avoid absorbing or modifying its existing S035 scope? [Consistency, Spec FR-021 and Scope]

## Acceptance Criteria Quality

- [ ] CHK010 Can every profile, host track, diagnostic class, and baseline rejection be counted objectively? [Measurability, Spec SC-001 through SC-006]
- [ ] CHK011 Is deterministic generation separated from intentionally ephemeral screenshot and timestamp data? [Measurability, Spec SC-007]
- [ ] CHK012 Are full production rebuild, site, WCAG, and repository-hygiene completion signals explicit? [Measurability, Spec SC-008 through SC-009]

## Scenario and Edge-Case Coverage

- [ ] CHK013 Are orientation, resize, IME, display-cutout, system bars, titlebar regions, and mixed input changes all covered? [Coverage, Spec FR-010 through FR-014]
- [ ] CHK014 Are invalid geometry, overlapping obstruction, unsupported capability, and evidence-substitution cases addressed? [Edge Case, Spec Edge Cases]
- [ ] CHK015 Are machine-authored, incomplete, stale, mismatched, and unavailable candidate decisions covered by fail-closed requirements? [Recovery, Spec FR-016 through FR-019]

## Non-Functional Requirements

- [ ] CHK016 Are WCAG 2.1 AA, accessible diagnostics, reduced motion, forced-color status, and enlarged-text requirements complete? [Accessibility, Spec FR-004 through FR-006]
- [ ] CHK017 Are identity geometry, affiliation, provenance, and production-discovery boundaries preserved? [Governance, Spec FR-020 through FR-023]
- [ ] CHK018 Are UTF-8, LF, mojibake, deterministic output, and exact-version evidence requirements documented? [Quality, Spec FR-008, FR-024, SC-007 through SC-009]

## Dependencies and Assumptions

- [ ] CHK019 Are merged recipe, Web/React, AppFrame, egui, and version-contract dependencies identified as stable inputs? [Dependency, Spec Assumptions]
- [ ] CHK020 Are consumer repository mutation, documentation restructuring, release publication, and issue #202 explicitly excluded? [Boundary, Spec Scope]

## Notes

- This checklist is for pull-request requirements review. `$speckit-implement` reads but does not change its markers.
