# Research: v1.2.0 Publication and Production Certification

## Decision 1: Publish from the squash-merged main revision

**Decision**: Treat `39b65b5daf9ea74c317132d26347566a9e4959d5` as the only valid v1.2.0 tag target after proving its tree matches the reviewed S010 head and repeating the candidate gate.

**Rationale**: Pull request #127 was squash-merged, so ancestry alone does not preserve the feature commit chain. Tree equality plus complete validation proves the owner-approved content reached main.

**Alternatives considered**: Tagging the former feature head was rejected because it is not the merged main revision. Rebuilding release assets locally for upload was rejected because GitHub Actions is the sole publisher.

## Decision 2: Reuse the existing browser contract against production

**Decision**: Add a narrow origin-selection module and allow `verify-site.mjs` to target `https://brand.shruggie.tech` through `SITE_VERIFY_BASE_URL`.

**Rationale**: The existing verifier already owns the complete route, metadata, discovery, resource, responsive, theme, and accessibility contract. Reusing it prevents drift between local and public certification.

**Alternatives considered**: A second production-only script was rejected because it would duplicate a large browser contract. Manual-only requests were rejected because they would not be reproducible or complete.

## Decision 3: Fail closed on remote origins

**Decision**: Accept only HTTPS and the exact hostname `brand.shruggie.tech` for remote mode. When the environment variable is absent, preserve the existing local static-server path.

**Rationale**: The verifier performs many requests and screenshots. Restricting its remote target avoids accidental use against arbitrary hosts while keeping local CI unchanged.

**Alternatives considered**: Allowing arbitrary URLs was rejected as unnecessary capability. Hardcoding production with no local mode was rejected because current CI depends on local static output.

## Decision 4: Defer closure until the evidence PR merges

**Decision**: Attach operational evidence to #118 and #119 immediately after it passes, but use the S011 pull request to close #116, #118, #119, and #129 on owner merge.

**Rationale**: The evidence record and verifier improvement are part of the completion definition. Merge-time closure keeps GitHub state aligned with reviewed repository state.

**Alternatives considered**: Manual closure before review was rejected as premature. Keeping fulfilled children open after evidence merge was rejected because it obscures actual status.
