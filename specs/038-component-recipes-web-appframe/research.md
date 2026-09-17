# Research: Component Recipes and Web AppFrame

## R1. Recipe authority and vocabulary

**Decision**: Add one versioned `component-recipes.json` reference with a closed 15-recipe catalog. The issue's `core form controls` family is represented by separate `Field` and `FormControls` recipes because labeling, description, validation, and message association are distinct from native control behavior.

**Rationale**: Issue #214 requires a bounded, machine-validatable grammar. A separate contract keeps component behavior coordinated with Interface Canon without turning semantic roles into a product-screen DSL. Each recipe names variants, densities, states, roles, keyboard behavior, targets, icon policy, semantics, motion, responsive behavior, overrides, ownership, and verification identifiers.

**Alternatives considered**: Embedding recipes in Interface Canon would couple token and component API evolution. Copying recipes into each brand would drift. An open component map could express arbitrary screens and navigation.

## R2. Adapter generator boundary

**Decision**: Add `gen_web_react.py` after existing vanilla output and before Next.js and enforcement generation.

**Rationale**: `gen_vanilla.py` mixes legacy JSX samples with tokens, while `gen_nextjs.py` is a shadcn and Tailwind binding. A dedicated adapter treats CSS custom properties as canonical, keeps React optional, and exposes stable generated paths to browser, Next.js, Vite, Tauri, and Wails consumers.

**Alternatives considered**: Expanding `gen_nextjs.py` would make Next.js canonical. Replacing legacy components creates unrelated migration risk, so they are labeled compatibility output and the new adapter is authoritative for recipe conformance.

## R3. Accessible headless dependency

**Decision**: Adopt `radix-ui` 1.6.7 (MIT) for Toolbar, Tabs, Menu, Dialog, and Toast. Its published peer range covers React and React DOM 16.8 through 19, including React 19 release candidates. Generate native-semantic React for AppFrame, Button, IconButton, Field, FormControls, ListRow, SplitPane, StatusBadge, Card, and EmptyState.

**Rationale**: Focus containment and return, roving focus, typeahead, layered dismissal, and announcement timing are mature state machines. Radix publishes accessible WAI-ARIA patterns, SSR guidance, React 19 compatibility, MIT licensing, and tree-shakeable primitives. BrandBuilder still owns the public recipes, semantic styles, bounded properties, portal target, packaging, and verification. No generator-time fetch occurs.

**Alternatives considered**: React Aria offers a broader abstraction than the bounded grammar needs. Reimplementing all behavior locally would create avoidable accessibility risk. The adapter does not expose Radix `asChild`, because open-ended element replacement can bypass bounded semantics.

## R4. Server and client entry points

**Decision**: Generate `server.tsx` for structural native components, `client.tsx` with an explicit `use client` boundary for stateful components and the environment bridge, and `index.ts` that documents direct entry use without collapsing server boundaries.

**Rationale**: Next.js can retain server components where possible, while Vite imports the same files. Browser APIs occur only inside effects or handlers. React and the pinned headless package are declared exactly in adapter metadata.

**Alternatives considered**: One all-client barrel would hydrate static UI unnecessarily. Separate per-component packages add complexity without proportional value.

## R5. AppFrame ownership

**Decision**: AppFrame owns safe-area consumption, dynamic viewport sizing, root scrolling, fixed chrome placement, IME obstruction exposure, titlebar avoidance, and global focus by default. Host profiles transfer an individual boundary only through a declared handoff.

**Rationale**: The main failure is double padding or an unowned boundary when browser CSS and native shells both compensate. A closed owner map makes this machine-verifiable. Radix portals target the AppFrame overlay root instead of defaulting silently to `document.body`.

**Alternatives considered**: OS presets conflate host and capabilities. Letting ordinary page components consume environment insets makes ownership untraceable.

## R6. Web token durability

**Decision**: Emit public `--bb-*` semantic custom properties in `tokens/interface.css` that alias governed brand values and resolved Interface Canon roles.

**Rationale**: Stable role names work across brands without React. Existing prefixed tokens remain compatible. Tailwind may consume these variables but is not authoritative.

**Alternatives considered**: Tailwind configuration is not portable. Inlining resolved literals into component CSS breaks role traceability. Renaming existing tokens would disrupt consumers.

## R7. Generated verification specimen

**Decision**: Generate one self-contained HTML specimen using the exact emitted tokens and component CSS, with minimal browser behavior mirroring declared keyboard and focus outcomes.

**Rationale**: Python tests validate contracts and deterministic source. Playwright and axe exercise actual focus, keyboard, resize, safe-area, forced-color, reduced-motion, scaling, and IME variables. The specimen is reusable evidence for #217 but does not establish cross-runtime golden screenshots.

**Alternatives considered**: Source inspection alone does not satisfy #215. A second standalone JavaScript test project would duplicate the existing site browser toolchain.

## R8. Support records

**Decision**: Generate records for the actual Playwright Chromium run plus Windows 11 webview-style and Android Chrome-style simulated profiles, with exact engine, host, configuration, checks, and limitations.

**Rationale**: Capability behavior remains authoritative, while #215 requires concrete records. The matrix must not claim native Android WebView, Tauri, or Wails certification that belongs to #217 and consumer pilots.

**Alternatives considered**: Prose compatibility claims are not machine-checkable. OS-based adapter branches violate Interface Canon.

## R9. Version coordination

**Decision**: Upgrade the closed consumer contract to schema version 2 and add `component_recipe_version` and `web_react_adapter_version`, both initially `1.0.0`. Keep compiler and Brand Canon `1.2.1` and Interface Canon `1.0.0`.

**Rationale**: The existing schema permits exactly four version fields, so adding two is a contract shape change. Consumers need exact identities now, while #218 owns the final lock-step policy.

**Alternatives considered**: Reusing `interface_canon_version` hides component API changes. Publishing a project release is outside S038.

## R10. Security and integrity

**Decision**: Validate authored references before output, generate from fixed templates, prohibit raw styling properties and open-ended element replacement, keep paths contained, checksum copied contracts, and run no implicit network activity.

**Rationale**: Relevant threats are contract escape, arbitrary composition, ungoverned visual input, unsafe recovery, generated-source injection, and output drift. The exact dependency record includes package, version, license, React range, and install prerequisite.

**Alternatives considered**: Arbitrary `className`, `style`, or recipe composition would defeat the bounded contract. Vendoring headless internals would obscure maintenance and license provenance.
