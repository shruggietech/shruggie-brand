# Research: Portfolio Card Consistency

## Homepage surface boundary

**Decision**: Preserve a generated showcase surface only when its generated legal foreground is exactly white; otherwise use the existing accent-derived dark fallback for the homepage portfolio.

**Rationale**: Generated white foreground is already the repository's measured signal that the governed surface supports white normal text. Cueson, ESO Weave, and Glitchpad retain their approved dark surfaces, while I Heart PR Tours keeps its light-first identity on brand routes but joins the homepage's dark showcase family.

**Alternatives considered**: Ignore all governed surfaces, hardcode an I Heart PR Tours slug exception, or parse surface luminance in the client. Ignoring every surface would undo prior dark-brand decisions, a slug exception would encode policy as a brand name, and client color parsing would duplicate the generator's measured foreground decision.

## Visible-copy contract

**Decision**: Set titles, descriptions, mobile copy, and action labels explicitly to `#FFFFFF` within the portfolio scope.

**Rationale**: The owner explicitly requested all visible portfolio text to be white. A local explicit value prevents inherited muted or governed foregrounds from reintroducing mixed hierarchy while remaining measurable in rendered verification.

**Alternatives considered**: Continue using muted text, inherit a per-brand foreground, or apply opacity. Each conflicts with the requested uniform white treatment or risks computed colors that are no longer white.

## Keyboard reveal and hidden focus

**Decision**: Make each desktop article a labeled keyboard focus stop, hide its actions with `visibility: hidden` and pointer suppression at rest, and reveal them when the card is hovered or focused within.

**Rationale**: Pointer-only hover is inaccessible, while opacity alone leaves invisible anchors in the tab order. Focusing the article exposes the controls before a user tabs into them. Existing Escape dismissal can return focus to the article without moving layout.

**Alternatives considered**: Keep opacity-only anchors, add a separate reveal button, or show actions permanently. Opacity-only controls violate hidden-focus requirements, another button adds an unnecessary interaction and tab stop, and permanently visible controls discard the existing approved reveal behavior.

## Action appearance and focus

**Decision**: Use a dark neutral action fill with white labels, an accent border, a white inner focus outline, and an accent outer ring. Retain non-color hover and active cues and remove transforms under reduced motion.

**Rationale**: A dark stable fill guarantees white text contrast across arbitrary brand accents. The dual focus treatment remains visible against both the control and surrounding card, while border, inset, and position cues avoid color-only state communication.

**Alternatives considered**: Use accent-filled controls or inherited card colors. Arbitrary brand accents do not guarantee white-text contrast, and inherited colors caused the reported inaccessible combinations.

## Card geometry and breathing room

**Decision**: Increase the fixed desktop card height and action-stage minimum, reserve an explicit bottom inset inside the absolute stage, and measure content-to-border clearance for both descriptions and actions.

**Rationale**: Two 44-pixel actions plus their gap require more than the current 5.5-rem stage, and longer descriptions need a stable buffer. Reserving stage space preserves the no-layout-shift reveal model.

**Alternatives considered**: Let cards auto-size, truncate descriptions, or reduce target sizes. Auto-sized rows can shift the grid, truncation removes content, and smaller targets violate the established accessibility floor.

## Third-party notice

**Decision**: Compute a boolean `hasThirdPartyProjects` and conditionally render one paragraph with the exact copy `* Third-party projects are independently owned and operated.`

**Rationale**: Notice presence still follows generated applicability, while its length and count no longer depend on distinct per-brand legal strings. Existing marker associations can continue to reference the one notice ID.

**Alternatives considered**: Deduplicate the detailed strings, choose the first vendor boundary, or add a new generated summary field. All three preserve or relocate unnecessary legal detail instead of meeting the requested generic homepage disclosure.

## Regression boundary

**Decision**: Combine source-contract assertions with computed-style and geometry checks in the existing browser verifier, plus the complete site and repository pipeline.

**Rationale**: Source assertions can prove fixed copy and conditional structure, while only a browser can prove computed white text, dark surfaces, focus visibility, hidden focusability, spacing, zoom, reduced motion, and no layout shift.

**Alternatives considered**: Screenshot snapshots or generated-output diffs. They are brittle, do not directly measure accessibility semantics, and conflict with the repository's measured-behavior approach.

## Security and tenancy applicability

**Decision**: Retain exact explicit action destinations and download attributes, reject implicit full-card navigation and hidden interactive controls, and record tenancy as not applicable to this static public component.

**Rationale**: The feature adds no authentication, private data, storage, user input, or tenant context. The relevant safety boundary is preventing destination drift and inaccessible hidden controls.

**Alternatives considered**: Add synthetic authentication or tenancy fixtures. Those would test nonexistent behavior and expand scope without improving the public portfolio's security.
