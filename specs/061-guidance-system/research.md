# Research and design decisions

## Canonical reference library

**Decision:** Author annotated references in `skill/references/references.md`, assign stable ID headings, register the page in `documentation-contract.json`, and validate local citation targets. Convert offline relative citations to hosted documentation routes during deterministic MDX rendering.

**Rationale:** The existing publication pipeline copies the same Markdown into the skill and hosted manual with exact archive verification. A separate manually maintained JSON catalog would duplicate titles and annotations. Stable heading IDs and a validator provide a checked catalog without another truth source.

**Alternatives considered:** A hosted-only page would leave agents offline without the explanation. A database or live link fetch would break deterministic builds. Duplicated Markdown and JSON source inventories would drift.

## Guideline fact authority

**Decision:** Project `enforcement/documentation-facts.json` from each verified kit to a stable static public path, preserving exact bytes. Explain rule values in hosted React and the source generators for portable and bundled guidance. Keep the pinned bundle's facts link distinct from the current hosted projection.

**Rationale:** The kit already supplies the canonical fact object and portal. This preserves P5 and gives readers an inspectable direct JSON artifact. Pure rendering changes do not require brand or identity source changes.

**Alternatives considered:** A newly authored site JSON schema would duplicate facts. A runtime route would conflict with static export and could diverge from the kit.

## Source use and support claims

**Decision:** Classify references as standards, platform guidance, implementation guides, advisory systems, or further reading. Apply each to an explicit local task. Mark Android/WordPress examples as guidance for future adapters until repository support is actually shipped. Inspect prior repo issue/PR/spec history and record coverage without claiming inaccessible conversation history.

**Rationale:** Source links alone do not tell a reader what to do, and platform documentation must not become an unsupported product claim.

**Alternatives considered:** A raw URL list or generic bibliography would not meet #271/#272. Treating every cited recommendation as mandatory would add unauthorized product restrictions.

## Accessibility and output parity

**Decision:** Replace one-line guideline sections with semantic headings, descriptive lists, and wrapping definition rows. Audit all brands and conditional states. Add focused browser and generator assertions plus a documented reader-task walkthrough. Use measured PDF content checks rather than PDF byte comparison.

**Rationale:** The current Overview exposes internal codes and generic filler. The existing full build already validates all eight kits and the static site; focused tests will catch the visible regression.

**Alternatives considered:** A metadata-only schema change would leave the confusing presentation unchanged. A visual snapshot alone cannot establish meaning or accessibility.

## Constitution recheck

All decisions preserve P1 through P6. No identity geometry, approved palette, or current adapter contract is changed. Sources and tests are committed, artifacts are rebuilt, and WCAG 2.1 AA remains the floor.
