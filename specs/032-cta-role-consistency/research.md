# Research: CTA Role Consistency

## Existing semantic source

**Decision**: Retain `brands/i-heart-pr-tours/brand.json` `semantic_colors.action` as the authoritative CTA fill.

**Rationale**: The value is already `#C5342C`, the brand contract requires the independent-brand action role, enrichment measures it, and Next.js token generation already exposes it as `brand-cta`. The defect is downstream consumption and incomplete documentation, not missing brand data.

**Alternatives considered**: Add a second CTA field, hardcode the color in document templates, or replace the general primary identity role. Each would either duplicate the source of truth or recolor unrelated semantics.

## CTA foreground

**Decision**: Publish a `brand-cta-foreground` token derived through the existing legal-foreground measurement and verify it as a required pair with `brand-cta`.

**Rationale**: `#C5342C` measures approximately 5.38:1 against white and 3.90:1 against black. White is therefore the legal normal-text foreground. Deriving it preserves shared generator behavior for any future independent brand action value.

**Alternatives considered**: Hardcode white in the guides or borrow `primary-foreground`. Hardcoding loses the measured contract, while the general primary foreground belongs to identity blue and may differ.

## Interaction states

**Decision**: Keep the governed CTA fill and foreground stable across hover and active states, using border, inset, and positional cues. Use a dual black/white focus treatment.

**Rationale**: Darkening or lightening arbitrary future CTA colors can invalidate their measured foreground. Non-color state cues remain accessible, deterministic, and compatible with reduced motion. A dual-tone focus treatment remains visible on both light and dark surrounding surfaces.

## Secondary CTA treatment

**Decision**: Match the live I Heart PR Tours secondary-action role with a transparent control and CTA-red outline. Use CTA red for text only when it clears 4.5:1 on the current surface; otherwise use the legal surface foreground. Hover uses the governed red fill and filled-control foreground.

**Rationale**: `#C5342C` measures 5.38:1 on white but only 3.48:1 on the dark brand surface. Keeping the red outline in both themes preserves the intended identity, while a surface-aware text token prevents the dark example from failing WCAG 2.1 AA.

**Alternatives considered**: Red text on both surfaces fails normal-text contrast on the dark surface. A neutral outline omits the live-site treatment. A second hardcoded dark-theme red would create another source of truth.

**Alternatives considered**: Fixed brand-specific state colors, `color-mix()` variants, opacity, or the existing identity-blue ring. These either require new governed values, weaken contrast predictability, or fail to guarantee focus separation from both the red fill and surrounding surface.

## PDF presentation

**Decision**: Add CTA to the page-four palette and semantic table, then show compact labeled default, hover, active, and focus-visible specimens with explicit separation from destructive, identity, focus, and chart roles.

**Rationale**: The issue identifies page four as the missing implementation reference. Keeping the complete CTA contract together makes it discoverable while preserving the eight-page guide structure if layout validation passes.

**Alternatives considered**: Add a ninth page or mention only the hex in prose. A new page is unnecessary unless measured layout forces it, while prose alone does not provide the requested palette role or visual demonstration.

## Language normalization

**Decision**: Convert reader-facing generated guide prose to American English while preserving internal schema and API identifiers.

**Rationale**: The user-facing defect is mixed dialect. Renaming stable keys such as `colourway` would create a broad migration unrelated to the visible copy and risk breaking existing kit contracts.

**Alternatives considered**: Rename all code identifiers or patch only I Heart PR Tours output. The first expands scope materially; the second leaves shared generated guides inconsistent.

## Regression boundary

**Decision**: Combine source-level generator assertions, exact computed-style browser checks on the generated portable guide, PDF text extraction, page rendering, and existing all-kit verification.

**Rationale**: String-only tests cannot prove computed styles or PDF layout, while browser-only tests cannot prove semantic source boundaries. The combined gates cover the failure modes reported in #201 and #203.

**Alternatives considered**: Snapshot generated files or byte-compare PDFs. Both conflict with the repository's measured-behavior approach and generated-artifact policy.
