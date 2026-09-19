# Interface Implementation

Interface implementation starts from semantic roles and bounded component behavior, never from screenshots or inferred platform conventions. The same resolved contract must remain recognizable across browser, desktop, touch, keyboard, narrow, wide, reduced-motion, and forced-color environments.

## Interface Canon

`interface-canon.json` defines renderer-neutral roles, invariants, permitted overrides, state pairs, themes, and runtime capability inputs. Runtime decisions use measured capabilities such as viewport, pointer precision, hover, touch, keyboard, text scale, safe area, reduced motion, forced colors, and title-bar regions. They do not branch on an operating-system name.

Brand affiliation does not grant permission to borrow a parent's identity values. Only declared inheritance and permitted overrides cross that boundary. Contrast requirements remain mandatory and are resolved before adapters are emitted.

## Component recipes

`component-recipes.json` defines the shared component grammar and behavior contract. Recipes name semantic inputs, states, keyboard behavior, layout rules, and validation evidence. They do not prescribe one framework's component tree. When a consumer needs a reusable behavior absent from the recipes, record a capability gap instead of creating an undocumented permanent fork.

## Web and React

The generated Web/React adapter lives at `web/adapter.json`, with its support matrix at `web/support-matrix.json`. Generated token files, registry resources, and reference components bind semantic roles to browser behavior. AppFrame adapts to declared runtime capabilities, including title-bar regions, safe areas, input precision, and narrow viewports. The generated support matrix identifies native, adapted, unsupported, and proof states explicitly.

## Rust and egui

The generated egui adapter lives at `native/egui/adapter.json`, with its support matrix and locked Rust dependencies beside it. It preserves the same recipe and semantic-role versions while documenting renderer-specific adaptations. Use the supplied crate, lockfile, and verification fixtures. Do not translate browser-only assumptions into native code.

## Consumer sequence

Read `enforcement/consumer-contract.json` first. Confirm the exact version tuple and authority paths. Read `enforcement/IMPLEMENTATION.md` for offline operational guidance. Integrate the declared adapter for the target renderer, then run both verification entry points. A successful implementation reports zero verifier problems and zero glyph failures.
