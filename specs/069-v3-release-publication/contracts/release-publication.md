# S069 Release Publication Contract

1. The formal tag is `v3.0.0` and points to the reviewed release-preparation commit after it reaches `main`.
2. Candidate metadata, source revision, archive manifests, documentation record, and site publication record agree with the exact tag.
3. Formal uploaded files are `shruggie-brandbuilder-3.0.0.skill`, `shruggie-brandbuilder-3.0.0-portable.zip`, eight canonical brand ZIPs, and `SHA256SUMS`. The release body comes from the generated release notes.
4. `SHA256SUMS` includes each distribution file exactly once and validates the uploaded bytes. The release must not contain unexpected assets.
5. Eleven brand guides and site packages derive from the eleven verified kits. The three hosted-only brands retain candidate bundle publication status and are not declared as formal GitHub release archives.
6. `release-preflight`, `publish-release`, and `deploy-pages` must complete successfully for the exact tag. The site manual links to the existing exact release.
7. A retry inspects any existing tag, draft/release record, asset names, and checksums. It may resume only with the same source revision and byte inventory.
