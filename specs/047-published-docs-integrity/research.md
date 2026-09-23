# Research: Published Documentation and Guideline Integrity

## Decision: Derive public prose scope from existing inventories

**Rationale**: Fifteen manual pages are enumerated in `skill/references/documentation-contract.json`; `scripts/prepare_site.py` transforms them into MDX. Production kit discovery and `scripts/build_all.py` define brand source files copied into archives. Source and prepared-output checks together catch authoring leaks and transformation defects. The current publication audit checks structure, not prose.

**Alternatives considered**: Scan the entire repository (false positives in specs and provenance); check only built HTML (misses kit files and source drift); check only source Markdown (misses transformation corruption).

## Decision: Use exact editorial rules and narrow exceptions

**Rationale**: Slice codes and historical anecdotes are invalid in reader guidance, but `historical-baseline`, `legacy-constructed`, technical `may`, and actual Spec Kit instructions can be current contracts. Enforce objectively detectable patterns with exact reviewed exceptions and record human editorial review for semantic quality.

**Alternatives considered**: Ban all hedging words (damages technical meaning); rely only on manual review (no regression protection).

## Decision: Correct guide preview semantics in the generator

**Rationale**: `gen_guidelines.py` chooses a dark well for default appearance without verifying visibility, and dark-well CSS lacks a contrasting foreground. Generated portable HTML is copied to the site; changing site output would not repair downloadable kits. Use visible pixels or declared surface evidence for visual assets, explicit well colors, and a separate nonvisual treatment. Do not alter embedded asset bytes.

**Alternatives considered**: Invert or recolor assets (violates identity); make all wells light (white artwork disappears); patch one generated guide (regresses on rebuild).

## Decision: Keep pagination links native

**Rationale**: Fumadocs 16.15.11 renders bottom links through the Next link adapter. The site declares smooth scrolling on `html` but omits the Next 16 opt-in that lets route transitions temporarily disable it. Add the opt-in and a scoped destination focus handoff for pagination activation; let Next retain fragment and history semantics.

**Alternatives considered**: Manual `router.push` or blanket route-change `scrollTo(0,0)` (risk fragments/history); CSS-only change (does not move focus).

## Decision: Prepare 2.0.2 as an untagged patch candidate

**Rationale**: A generated portable-guide fix changes kit bytes, so the published 2.0.1 immutable identity cannot be reused. Version policy classifies compatible deterministic output and verifier fixes as compiler patches. Full candidate validation can run before owner merge without cutting a tag.

**Alternatives considered**: Keep 2.0.1 (identity collision); require a major or minor bump (no contract expansion warrants it).
