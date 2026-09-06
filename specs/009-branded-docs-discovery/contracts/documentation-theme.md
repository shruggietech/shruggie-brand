# Documentation Theme Contract

## Typography

- Marketing display typography is scoped to marketing surfaces.
- Documentation `h1` uses a compact responsive size no larger than 2.5rem at supported desktop widths.
- Documentation `h2` uses a compact responsive size no larger than 1.875rem at supported desktop widths.
- Lower headings form a descending hierarchy and body text remains readable from 360 through 1280 CSS pixels.
- At 1280 by 900 CSS pixels, the documentation index title, description, introductory content, and start of the next meaningful element fit in the first viewport.

## Semantic colors

- Fumadocs background, foreground, muted, popover, card, border, primary, accent, ring, and status variables map to canonical ShruggieTech roles or documented derived mixtures.
- Dark and light values remain distinct and pass rendered WCAG 2.1 AA checks.
- Bright green is reserved for dark-surface identity and orientation roles; accessible green is used for light-surface text and links.
- No project-owned near-match hex palette duplicates canonical roles.

## Orientation and focus

- Active sidebar and table-of-contents states use canonical green and a non-color cue such as weight, border, underline, or rail thickness.
- Every keyboard-focusable documentation control displays a visible focus indicator.
- Hover, active, current, visited, disabled, and focus states remain distinguishable where applicable.
- Reduced-motion preference disables nonessential transitions and smooth scrolling.

## Identity

- The sidebar header uses a theme-appropriate existing ShruggieTech lockup at a legible scale.
- The lockup source remains generated from shipped geometry and is not cropped, traced, normalized, or redrawn.

## Visual evidence

- `/docs/` and `/docs/04-toolchain/` are captured at 360 by 900 and 1280 by 900 CSS pixels in light and dark themes.
- Screenshots are generated under an ignored repository-local test-results path and reviewed during the slice.
- Durable automated gates assert computed typography, geometry, overflow, semantic colors, state cues, and WCAG behavior.
