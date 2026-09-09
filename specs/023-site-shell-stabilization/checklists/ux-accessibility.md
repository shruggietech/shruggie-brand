# Requirements Quality Checklist: UX, Accessibility, and Layout Stability

**Purpose**: Reviewer-owned checks for whether the S023 requirements are complete, unambiguous, and measurable before acceptance.

## Homepage hierarchy and copy

- [ ] CHK001 Are the exact hero labels, semantic order, destinations, and visual hierarchy stated without relying on subjective interpretation? [Completeness, Spec §FR-001–FR-004]
- [ ] CHK002 Is the required separation and decorative-arrow accessibility behavior specified in measurable or directly inspectable terms? [Clarity, Spec §FR-003]
- [ ] CHK003 Are the portfolio heading, required phrase, unchanged anchor, unchanged card scope, and removed callout all explicitly bounded? [Completeness, Spec §FR-005–FR-006]

## Shared chrome policy

- [ ] CHK004 Are desktop and mobile navigation requirements applied consistently to the main site and all docs pages? [Consistency, Spec §FR-007–FR-008]
- [ ] CHK005 Is the surface-specific Company target policy distinguished from Download Skill, Source, and License without contradiction? [Clarity, Spec §FR-008–FR-010]
- [ ] CHK006 Is the neutral per-brand guidelines exclusion explicit enough to prevent incidental promotional chrome changes? [Scope, Spec §FR-011]

## Stability and responsive behavior

- [ ] CHK007 Do the requirements prohibit route-specific offsets while naming the shared shell behavior that must replace them? [Constraint, Spec §FR-012–FR-014]
- [ ] CHK008 Are the compared routes, elements, conditions, and one-CSS-pixel tolerance sufficient to detect the reported navigation drift? [Measurability, Spec §FR-016]
- [ ] CHK009 Are docs pages with and without the right table of contents both covered without weakening sticky-rail usability? [Coverage, Spec §FR-013, FR-016]
- [ ] CHK010 Are short/tall content, light/dark themes, desktop/narrow viewports, scale emulation, and horizontal overflow covered? [Coverage, Spec §FR-014, FR-016]

## Verification and governance

- [ ] CHK011 Do source checks and rendered-browser checks together cover regeneration, semantics, interaction, and visual stability? [Completeness, Spec §FR-015–FR-017]
- [ ] CHK012 Are WCAG 2.1 AA, keyboard behavior, touch targets, reduced motion, static export, and repository hygiene non-optional acceptance gates? [Constitution, Spec §FR-004, FR-017]
- [ ] CHK013 Is each included GitHub issue traceable to at least one functional requirement and measurable success criterion? [Traceability, Spec §Traceability]

## Notes

- This checklist evaluates requirements quality, not implementation completion. Reviewers own the checkmarks.
