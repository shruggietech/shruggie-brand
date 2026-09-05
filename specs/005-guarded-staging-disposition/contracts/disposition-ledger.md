# Contract: Sanitized Disposition Ledger

## Required public columns

`docs/disposition.md` contains one row per top-level item present at the execution inventory boundary:

| Entry | Classification | Governed coverage | Destination class | Recoverability | Final state |
| --- | --- | --- | --- | --- | --- |

## Completeness rules

1. Every top-level staging item has exactly one row, including any item not anticipated by the work order.
2. The five brand directories and five corresponding snapshot archives use separate rows.
3. Private skill subtrees and transport bundles may share one top-level row only when their individually verified components are enumerated in that row's coverage text.
4. The runtime, historical archive, each unrelated research group, each provenance CSS source, private session output, and operator directive remain distinct entries.
5. Every row states the external preservation proof used before movement and a final state.
6. The ledger includes aggregate counts and gate outcomes but no exact operational root.

## Public-data prohibition

The committed ledger MUST NOT contain drive-qualified paths, home-directory names, backup filenames or locations, raw session content, credentials, account IDs, zone IDs, record IDs, access tokens, or recovery instructions. GitHub comments and issue bodies follow the same boundary.

## Private recovery contract

The private recovery record contains the exact source and destination paths, archive SHA-256, path/size/content comparison result, move order, collision results, destination verification, and recovery instructions. It remains outside Git and is itself moved out of the retiring workspace.

## Completion rule

The public ledger is complete only when every row is `Verified moved` or `Verified retained`, the source workspace has zero files, and any remaining directory has a documented reason. A blocked row prevents the guarded-retirement issue from being satisfied.
