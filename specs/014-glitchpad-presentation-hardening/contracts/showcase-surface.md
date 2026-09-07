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
- Unconfigured brands omit the property.
- Site components set `--brand-showcase-surface` only for configured brands.

## Presentation

- A configured landing card and portfolio hero use the resolved surface for their large identity background.
- Configured cards suppress accent-tinted showcase glow.
- Unconfigured brands retain the existing accent-derived fallback treatment.
- Focus, text, functional-status, and identity-accent roles remain independent.
