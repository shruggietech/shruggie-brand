# Contract: Visual Candidate and Baseline Review

## Candidate generation

Browser checks capture PNG candidates under ignored local or CI paths. Each image has a normalized JSON manifest containing its SHA-256 digest, brand and brand version, complete contract versions, source revision, host, profile, viewport, fonts and load state, renderer version, device scale, color scheme, contrast mode, motion preference, and `pending-human-review` state.

The candidate identity is the SHA-256 digest of the image bytes plus normalized metadata. A content or environment change necessarily produces a different identity.

## Human-only decision

An accepted or rejected decision must name the exact candidate identity, human reviewer, reason, UTC timestamp, source revision, and environment copied from the candidate. Automation-like reviewer identities, absent reasons, stale candidate identities, mismatched metadata, and unknown decisions fail closed.

Candidate generation and CI never write an accepted decision. Agents may generate candidates and report their locations but cannot promote them.

## Repository boundary

PNG candidates, generated manifests, and host build output remain ignored. The source decision ledger contains explicit decisions only and never embeds raster bytes. Empty ledgers are valid before the first human acceptance. A pending candidate does not fail functional conformance; it remains visibly pending until the PR or later baseline ritual records a human decision.

## Regression behavior

Measured accessibility, interaction, geometry, ownership, and contract failures always fail CI independently of visual review. Screenshot review supplements those gates and cannot waive them. A previously accepted decision applies only to an exact candidate identity and becomes stale when source, contract, environment, font, or image bytes change.
