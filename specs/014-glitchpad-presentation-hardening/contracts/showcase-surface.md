# Contract: Generated Showcase Surface

## Source

A brand may declare optional `showcase_surface` as the name of one role already present in its `surfaces` object.

## Validation

- The reference is a non-empty string.
- The referenced role exists in `surfaces`.
- The resolved value is a six-digit hexadecimal color.
- Invalid references fail brand validation and site preparation.

## Generated binding

- Configured brands emit `showcaseSurface` with the resolved hexadecimal value.
- Configured brands emit `showcaseForeground` as whichever of black or white has the higher WCAG contrast against the resolved surface.
- Unconfigured brands omit the property.
- Site components set `--brand-showcase-surface` and `--brand-showcase-foreground` only for configured brands.

## Presentation

- A configured landing card and portfolio hero use the resolved surface for their large identity background.
- A configured landing card uses the derived foreground for readable heading and body text on both dark and light governed surfaces.
- Configured cards suppress accent-tinted showcase glow.
- Unconfigured brands retain the existing accent-derived fallback treatment.
- Focus, text, functional-status, and identity-accent roles remain independent.
