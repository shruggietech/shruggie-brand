# Data Model: DanceWithMe865 Brand Restart

## Client brand source

The `brands/dancewithme865/brand.json` record identifies an independent third-party client, palette, typography, source bindings, derivative settings, vendor boundary, and approval ledger. It follows `skill/references/canon.schema.json`; no ZIP field or directory is added to that schema.

## Authoritative input

Each selected SVG is a passive, byte-preserved source under `brands/dancewithme865/assets/source/`, with one stable input ID, role, SHA-256, usage basis, and allowed transformations. Full and Reduced are distinct DWM sources. Light, dark, and single-ink treatments are bound to reviewed source or to a declared deterministic derivative. Supplied lockups preserve the upright outlined wordmark and boxed 865.

## Identity candidate and approval

An identity continuity record moves from candidate to approved canonical only after the owner accepts the exact Full and Reduced sources, palette qualification, renderer, and 32 proofs. Source revisions and packet hashes prevent approval reuse after drift. The abandoned S065 branch has no standing in this record.

## Assembled derivative

The private Gate 2 packet binds approved source to wide and stacked lockups, standalone wordmark, icon set, formal palette, interface cues, typography, representative applications, and a separate social share image. The owner approved its manifest and selected `DanceWithMe865` as the only social image wording.

## Generated kit and site projection

The generated kit is ignored `dist/` output with a verified manifest. The site registry consumes that kit and renders the independent client's name, artwork, guide, downloads, and ownership boundary. A pending candidate is not registered as public output.

## State transitions

`direction-selected` → `canonical-candidate` → `canonical-approved` → `derivatives-pending` → `derivatives-approved` → `verified-kit` → `site-eligible`. A changed master returns to `canonical-candidate`. A changed derivative returns to `derivatives-pending`.
