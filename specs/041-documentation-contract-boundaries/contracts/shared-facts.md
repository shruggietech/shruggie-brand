# Contract: Shared Documentation Facts

## Required equality

The hosted portal and bundled implementation projection for one kit must agree on:

- brand slug, title, version, and affiliation;
- Brand Canon, Interface Canon, component recipe, Web/React adapter, egui adapter, compiler, and brand versions;
- Web tokens, Web/React adapter, egui adapter, support-matrix, recipe, and Interface Canon paths;
- ordered authority paths and permitted exception categories;
- verification entry points and zero-failure success rule;
- recovery distribution path, SHA-256, extraction destination, and exact-version rule;
- capability-gap record path and submission authorization boundary;
- documentation contract version and system-manual destination.

## Generation order

1. Generate Web/React and egui adapters.
2. Validate the brand and resolve all independent versions.
3. Emit the consumer contract and its offline recovery distribution.
4. Generate the documentation fact record from the completed consumer contract and copied documentation policy.
5. Render `IMPLEMENTATION.md` from the fact record plus brand-specific governed rules.
6. Generate the guideline portal and embed the fact record unchanged.
7. Verify all three records and then stage the hosted portal.

## Failure rules

- Missing or extra required facts fail.
- A fact that disagrees with the consumer contract fails.
- A path outside the kit, a symlink, an absent file, or an unsafe public path fails.
- A rendered `IMPLEMENTATION.md` that does not identify the fact record and its exact version set fails.
- A portal that alters or omits the fact record fails.
- A recovery rule that requires network access when delivered bytes exist fails.
