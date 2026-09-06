# Presentation Contract: S012

## Navigation and terminology

- At 1280px, the landing header has one visible text link: `Documentation` to `/docs/`.
- At 360px, the closed landing header is compact and the opened menu has exactly `Documentation`, `Download the Skill`, and `View on GitHub`.
- The documentation application does not duplicate the docs-root link in its header or sidebar.
- Public output uses only `Documentation` and `Variance Contract` for their respective concepts. Rejected case-insensitive variants fail source and emitted-site checks.
- `/docs/` and `/docs/00-variance-contract/` remain exact canonical routes.

## Color and interaction roles

- Primary CTAs resolve to canonical CTA-safe orange with a compliant foreground in both themes.
- Secondary actions and identity emphasis resolve to the correct bright or accessible green for their surface.
- Documentation list markers and syntax-highlighted string tokens use approved green while remaining semantically distinguishable.
- Eligible ordinary text links use an orange underline that grows from left to right over the generated normal motion duration.
- Reduced-motion mode removes the transition duration but retains a visible static hover and focus state.
- Buttons, cards, logo links, heading anchors, and disabled links do not receive the ordinary underline treatment.
- Documentation pagination cards expose persistent resting, hover, active, and focus treatments, with a visible action label or destination and a minimum 44px target.

## Browser evidence

- Semantic assertions cover exact labels, URLs, visibility, absence, focus, reduced motion, and component exclusions.
- Computed-style assertions cover CTA background and foreground, green markers and string tokens, orange link underline, and pagination states.
- The 12-cell visual evidence matrix covers `/`, `/docs/`, and `/docs/00-variance-contract/` at 360px and 1280px in light and dark themes.
- Every public route continues to receive overflow and WCAG 2.1 AA checks.
