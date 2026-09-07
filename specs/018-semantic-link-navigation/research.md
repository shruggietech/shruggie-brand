# Research: Semantic Link and Documentation Navigation

## Decision: Use a role taxonomy rather than one ordinary-link rule

**Rationale**: The official company site varies interaction by component, and the defect comes from combining a generated global `a:hover` underline with site decoration. Explicit roles prevent cascade leakage and make exclusions testable.

**Alternatives considered**: Strengthening the existing `.text-link` selector would still leave cards and generated consumers vulnerable. One universal underline would contradict the supplied authority and the owner-approved pagination direction.

## Decision: Keep editorial links persistent and standalone actions cue-based

**Rationale**: Editorial prose needs a non-color-only resting affordance. Standalone actions already have layout context and can follow official accent text with a directional cue and color transition.

**Alternatives considered**: Removing every underline would weaken prose affordance. Keeping the orange animated underline on actions would preserve the reported defect and superseded design.

## Decision: Use neutral pagination surfaces and stable semantic descendants

**Rationale**: Fumadocs renders one anchor with a direction label, destination title, and description. Neutral surface and text tokens preserve hierarchy across themes. Narrow selectors tied to the observed semantic positions prevent the former `p:first-of-type` rule from styling both title and description.

**Alternatives considered**: Replacing Fumadocs pagination markup would duplicate routing. CTA-tinted cards conflict with the owner direction. Custom client state adds no value.

## Decision: Test computed decoration and descendant leakage

**Rationale**: The old browser gate only measured a background animation and missed native `text-decoration`. Assertions must inspect computed text decoration, background or pseudo-element treatment, descendants, focus, motion, target dimensions, wrapping, and theme colors.

**Alternatives considered**: Screenshot-only review cannot reliably detect every state or cascade interaction. CSS source assertions would not prove runtime behavior.
