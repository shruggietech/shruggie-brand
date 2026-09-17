# Contract: Interface Canon

## Authority boundary

Brand Canon owns identity, affiliation, artwork, brand colors, typography, provenance, and approval. Interface Canon consumes those governed values and owns renderer-neutral semantic roles, logical measures, runtime capability vocabulary, accessibility and behavior invariants, and permitted override mechanics. Interface Canon cannot alter or reinterpret Brand Canon.

## Reference grammar

Every alias or override value is a string beginning with one allowed root:

- `$primitive.<path>` resolves inside Interface Canon primitives.
- `$alias.<role>` resolves another semantic role and participates in cycle detection.
- `$brand.<path>` resolves a governed brand source value.
- `$brand_canon.<path>` resolves an immutable or constrained Brand Canon value.
- `$resolved.<path>` resolves a deterministic derived value such as accessible action foreground.

Unknown roots, missing paths, non-string aliases, product composition, renderer property names, and raw override values are invalid.

## Validation order

1. Validate source shape, versions, exact top-level keys, role identifier syntax, and required runtime keys.
2. Require role catalog and alias keys to match, then require every required role.
3. Resolve every alias with explicit recursion tracking and reject cycles.
4. Apply only declared brand overrides and reject invariant, unknown, raw, or cross-affiliation references.
5. Resolve the brand context and measure every declared foreground/background state pair against its minimum contrast.
6. Return the resolved semantic contract only after every check passes.

## Compatibility

An existing brand without an `interface` object uses the shared defaults. A declared `interface.canon` must equal the source Interface Canon version. A declared override must be listed in `permitted_overrides` and use an allowed reference root. Unsupported compatibility or an invalid override requires an explicit migration before generation.

## Adapter boundary

Adapters receive resolved semantic roles, logical measures, and a validated runtime profile. They translate logical units and semantic names into renderer syntax. Adapters do not derive behavior from operating-system names and do not add canon roles, brand values, or product layouts.
