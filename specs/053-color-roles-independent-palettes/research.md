# Research and Decisions: S053

## Existing authority

`brand.json` supplies accent, semantic colors, logo role colors, affiliation, and typography. `01-canon.json` supplies the shared orange/fault values and currently imposes hue distance. `interface-canon.json` resolves renderer-neutral roles. `gen_nextjs.py`, `gen_vanilla.py`, and native/web adapters consume those resolved values. The site projects `gen_guidelines.py` output; the portable and PDF generators independently present them.

## Decisions

1. Keep `affiliation.inheritance` as a legacy explicit palette choice: `shruggietech-house` opts into the historical orange pair, and `independent` requires authored `semantic_colors`. Remove the ownership restriction and the independent-brand ban on deliberately referencing a house color. This is smaller and more compatible than renaming a shipped field in S053. The field does not select typography; `typography.mode` remains separate.
2. Add `color_roles.identity` and approved `color_roles.combinations` to each brand source as named references to already approved values and artwork, without copied hex. Define shared `color.role_model.interface_cues` in the canon for action, warning, error, success, information, focus, selection, and disabled states. A single resolver checks references, measures dark/light fill/foreground and surface contrast, and exposes source, purpose, and non-color cue. Cue colors follow existing approved accent and semantic fields; an independent role-only override is rejected because current consumers cannot emit it. This avoids eight hand-maintained copies of common role definitions. The existing light `brand-emphasis` alias follows the action value; the warning role records that deliberate reuse while preserving the alias's hex.
3. Remove cross-brand accent and inherited-orange hue exclusion as acceptance tests. Preserve AA contrast, real foreground pairing, and semantic non-color cues. Historical sibling distances may appear only in provenance or archival notes, never in qualification or validation.
4. Preserve generated legacy token names and exact current values for all production brands. New role metadata augments the kit JSON and guides. No source mark geometry, approved hex, or existing logo construction changes.
5. Advance Brand Canon to 1.5.0 and BrandBuilder to 2.2.0 in this PR so rebuilt kits and recovery metadata have a coherent versioned contract. Formal tagging and release publication follow the later merge ritual.

## Alternatives rejected

- Renaming `inheritance` now would force an incompatible major migration and widen S053 beyond the owner's color decision.
- Treating every `accent` value as a formal identity color would mislabel UI variants such as the accessible light value; authored references are required.
- Adding raw hex duplicates to guideline prose would create multiple authorities and permit drift.
- Replacing hue distance with a softer minimum would retain the owner-rejected creative restriction.

## Clarification disposition

The owner decision in #268 resolves palette freedom. #267 resolves the identity/UI distinction and explicitly retains AA. The existing generated-token ABI and source geometry resolve migration behavior. No question requires another owner decision before implementation.
