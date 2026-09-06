# Data Model: Phase 13 Brand Site Polish

## Identity Asset Contract

| Field | Meaning | Validation |
| --- | --- | --- |
| role | Favicon, touch icon, manifest icon, dark lockup, or light lockup | One approved role per destination |
| canonical source | Generated path derived from ShruggieTech source | Must exist inside the verified ShruggieTech kit |
| background | Application-icon plate color | Exact canonical void value for applicable icons |
| appearance | Colored dark-surface or colored light-surface lockup | Monochrome variants rejected for affected destinations |
| dimensions | Declared output width and height | Must match platform and metadata declaration |
| geometry provenance | Authoritative imported mark and generated wordmark paths | Must remain unchanged |

## Responsive Navigation Contract

| Surface | Viewport class | Ordered visible items | Exclusions |
| --- | --- | --- | --- |
| Landing header | Desktop | Documentation | Portfolio, Download the Skill, View on GitHub |
| Landing menu | Mobile | Documentation, Download the Skill, View on GitHub | Portfolio |
| Documentation shell | Desktop and mobile | Existing page tree, search, theme, and home identity | Duplicate docs-root header item |

Each item has one exact label, destination, internal or external status, supported Fumadocs display filter, active behavior, and minimum target size.

## Canonical Terminology Contract

| Concept | Accepted display name | Rejected display names | Stable path |
| --- | --- | --- | --- |
| Documentation root | Documentation | How we build brands; How we build | `/docs/` |
| First numbered document | Variance Contract | The ShruggieTech Variance Contract; ShruggieTech Variance Contract; The Variance Contract | `/docs/00-variance-contract/` |

The accepted name propagates from source through headings, page trees, breadcrumbs, search records, pagination, social metadata, and structured data. Rejected names are compared case-insensitively on public surfaces.

## Interaction Role Contract

| Role | Resting treatment | Interactive treatment | Reduced motion | Exclusions |
| --- | --- | --- | --- | --- |
| Primary CTA | CTA-safe orange fill and compliant foreground | Distinct hover and focus with visible outline | Static color and outline change | Status and destructive controls |
| Secondary action | Surface-appropriate green emphasis | Distinct hover and focus | Static state change | Primary CTA |
| Ordinary text link | Readable text with orange underline affordance | Left-to-right underline over 120ms to 300ms | Immediate underline state | Buttons, cards, logos, heading anchors, disabled links |
| Documentation pagination card | Persistent branded border, label, and destination treatment | Distinct hover, active, and contained keyboard focus | Static treatment | Inline paragraph links |
| Documentation marker or code string | Approved green accent plus semantic context | Not interaction-dependent | Not applicable | Non-string syntax tokens |

## Visual Evidence Matrix

| Route | Widths | Themes | Required observations |
| --- | --- | --- | --- |
| `/` | 360px, 1280px | Light, dark | Lockup, navigation inventory, CTAs, inline link, no overflow |
| `/docs/` | 360px, 1280px | Light, dark | Lockup, Documentation naming, inline link, pagination resting state, footer |
| `/docs/00-variance-contract/` | 360px, 1280px | Light, dark | Canonical title, list and code accents, pagination and focus affordance, footer |

The matrix produces 12 screenshots. Every cell also receives semantic, overflow, and WCAG 2.1 AA inspection.

## Review Round

| Field | Validation |
| --- | --- |
| ordinal | Integer 1 or 2 only |
| trigger | Automatic PR integration for round one or one explicit comment for round two |
| findings | Every negative finding links to a GitHub issue created before resolution |
| responses | Every comment has a substantive reply or recorded disposition |
| threads | Zero unresolved threads at handoff |
| checks | Required checks successful on the final head |
