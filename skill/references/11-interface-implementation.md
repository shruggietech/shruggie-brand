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

## Native WordPress

The generated WordPress adapter lives at `wordpress/adapter.json`, with a support matrix, inspectable theme source, inventory, and installable ZIP beside it. `theme.json` format 3 binds approved identity and interface cue roles to namespaced native presets and block styles; `styles/dark.json` offers the approved dark interface as an optional Site Editor variation. A content-scoped supplement handles focus, Card styling, and responsive behavior in the site and editor content surface. Install the exact ZIP, set the Site Logo from its approved PNG alternative, and compose pages with core blocks and patterns. The [WordPress delivery guide](wordpress.md) explains pinned core/PHP test pairs, saved Global Styles precedence, client customization, update, and rollback. It does not imply that classic themes or third-party builders and plugins were tested.

## Consumer sequence

Read `enforcement/consumer-contract.json` first. Confirm the exact version tuple and authority paths. Read `enforcement/IMPLEMENTATION.md` for offline operational guidance. Integrate the declared adapter for the target renderer, then run both verification entry points. A successful implementation reports zero verifier problems and zero glyph failures.

## Apply a recipe to a web control

For a search field, choose a native labeled input, keep the label visible, and connect it programmatically as in the [React form example](references.md#ref-web-react). Use the recipe's semantic focus and error roles, then inspect keyboard behavior against [WCAG keyboard guidance](references.md#ref-a11y-keyboard), visible focus against [focus guidance](references.md#ref-a11y-focus), and any custom widget against the [ARIA patterns](references.md#ref-a11y-apg). [Nielsen](references.md#ref-ux-nielsen) and [Shneiderman](references.md#ref-ux-shneiderman) offer advisory review questions about feedback and recovery. [Next.js](references.md#ref-web-next) and [Radix](references.md#ref-web-radix) document their framework responsibilities; verify the actual exported host rather than assuming a library establishes conformance.

## Select the platform reading path

- **Supported web:** Start with the pinned Web/React adapter and support matrix. Use [shadcn theming](references.md#ref-web-shadcn), [Tailwind state guidance](references.md#ref-web-tailwind), and [CSS custom properties](references.md#ref-web-variables) for the consuming host. Keep [HTML semantics](references.md#ref-web-html) and unique [document IDs](references.md#ref-web-id) intact; inspect [selector specificity](references.md#ref-web-specificity) before overriding styles.
- **Supported native egui:** Start with the pinned adapter and lockfile. [egui architecture](references.md#ref-egui-architecture) explains its immediate-mode responsibilities, and the [accessibility guide](references.md#ref-egui-access) identifies host and platform bridge concerns. Use [egui_kittest 0.36.1](references.md#ref-egui-test) for version-matched state checks; accessible output still depends on the actual host integration.
- **Android host:** The kit ships identity assets but no generated Compose UI adapter. A host can use [adaptive layout](references.md#ref-android-layout), [Material components](references.md#ref-android-components), [custom Compose systems](references.md#ref-android-custom), [insets](references.md#ref-android-insets), and [Compose accessibility](references.md#ref-android-access) to map supplied assets and semantic roles. Record the mapping and verify it in the host. [Material 3](references.md#ref-android-m3) is a host theme option, not authority to change approved artwork.
- **WordPress host:** Start with the pinned `wordpress/adapter.json`, theme ZIP, inventory, and support matrix. [Global Settings and Styles](references.md#ref-wp-global), the [versioned format](references.md#ref-wp-format), [color presets](references.md#ref-wp-color), [typography](references.md#ref-wp-type), and the [style hierarchy](references.md#ref-wp-hierarchy) explain how native defaults and saved edits interact. Compare editor and front-end output with [editor asset loading](references.md#ref-wp-editor-assets) and [block stylesheets](references.md#ref-wp-block-css). Use [theme structure](references.md#ref-wp-structure), [patterns](references.md#ref-wp-patterns), [child-theme customization](references.md#ref-wp-child), and pinned [wp-env](references.md#ref-wp-env) when extending it. Editor [curation](references.md#ref-wp-curation) or [style variations](references.md#ref-wp-variations) are optional decisions for an approved product brief.
