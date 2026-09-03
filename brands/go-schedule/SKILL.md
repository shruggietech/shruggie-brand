---
name: go-schedule-brand
description: Generate on-brand interfaces, assets, and docs for go-schedule (a cross-platform scheduler in Go, a ShruggieTech sub-brand). Contains colors, type, fonts, logos, design tokens, and UI components.
user-invocable: true
---

Read `README.md` for the full brand system, then explore the files below.

If you are building visual artifacts (mocks, prototypes, slides), copy assets out
and produce static HTML that links `styles.css` and `components/components.css`.
If you are working in production code, copy the tokens and components and follow
the rules in `README.md`.

## Quick reference
- **Mode:** dark-first. Base Night `#071014`; Panel `#0D171C`; neutral Line rails `#28414B`. Paper `#F6F8F7` is the light reading surface.
- **Accents:** Interval Mint `#62D9B7` (recurrence/success) · Anchor Blue `#58A6FF` (run point/links/focus) · Hold Amber `#F2B84B` (rare) · Stop Red `#E05F5F` (failure only). On Paper, use the Deep variants.
- **Type:** Space Grotesk (display 500/700, tracking -0.025em) · Geist (body 400/500) · Geist Mono (commands, schedules, labels).
- **Voice:** operator explaining a runbook. Exact nouns, explicit policy. Cron is a reference frame, never the punchline. Endorsement: "A ShruggieTech project" in mono.
- **Logo:** wordmark is outlined Space Grotesk Bold (never re-typeset). Mark = terminal prompt over five cron cells. Load the system by linking `styles.css`.
