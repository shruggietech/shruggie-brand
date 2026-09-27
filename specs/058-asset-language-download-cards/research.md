# S058 Research and Decisions

## Existing data path

`gen_logo.py` writes logo provenance and a Gate 2 approval manifest. `gen_guidelines.asset_deliveries` reads those outputs and platform manifests; `group_asset_deliveries` drives both `portal.json` and portable HTML. `scripts/prepare_site.py` copies verified kit files into the hosted download tree; React renders generated catalog records. The grouping key omits layout, and titles concatenate raw technical values, yielding merged wide/stacked cards and repeated labels.

## Decision 1: preserve approved geometry and inventory

Keep all approved derivative paths and SHA-256 digests exactly as they are, including S057 social-image and legacy social-preview records. Create separate byte-identical descriptive publication aliases after derivative generation and verify their mapping. All eight Gate 2 ledgers bind the derivative inventory. Renaming approved derivatives would demand new creative approval without changing artwork.

## Decision 2: one semantic grammar

Map existing provenance into explicit purpose, form, layout, treatment, actual background, recommended surface, and ink axes; append size and format at delivery level. A paired mark/wordmark is a lockup, `horizontal` is publicly `wide`, and a social image has its own purpose. Deriving labels from filename stems in the site would duplicate generator authority and cannot reliably separate meanings.

## Decision 3: publish aliases and keep recovery

Give descriptive aliases separate paths and an explicit old-to-new map, retaining original files. Record canonical/alias roles and byte digests. Site redirects alone cannot satisfy pinned ZIP consumers.

## Decision 4: documentation and version policy

Place the glossary in the governed main manual, project a short first-use explanation/link into brand guides, and render generated catalog data in hosted and portable libraries. Bump compiler/site from 2.4.0 to 2.5.0, leave Brand Canon 1.6.0. The change is a backward-compatible delivery and verifier capability, not an identity revision.

## Evidence sources

- Issues #283 and #284 define vocabulary, card, compatibility, and accessibility requirements.
- `skill/templates/gen_guidelines.py` lines 73-95 and 153-165 expose grouping and label defects.
- `skill/templates/gen_logo.py` lines 563-598 and `skill/templates/verify.py` lines 1893-1923 bind Gate 2 derivative paths.
- `skill/references/documentation-contract.json` governs manual pages and source dispositions.
- `skill/references/version-policy.json` defines backward-compatible compiler minor changes.
