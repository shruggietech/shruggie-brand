# go-schedule migration notes

The brand source was migrated from the operator's legacy generated kit.

- The existing 512-unit mark remains imported SVG geometry. Rounded rectangles, open paths, stroke widths, caps, joins, and relative commands are preserved.
- The reduced master comes directly from the shipped SVG favicon.
- The unchanged reduced elements now serve as the current primary Full role. The former framed cron mark remains historical source in Git and is not delivered as a current identity.
- Anchor Blue remains the identity accent. Interval Mint remains a semantic recurrence and success color.
- The original README, skill guidance, and web UI kit are carried forward as source material.
- Generated exports are rebuilt by CI and are not committed here.

See [`../../LICENSE-BRAND`](../../LICENSE-BRAND) for the reserved brand-asset terms.
