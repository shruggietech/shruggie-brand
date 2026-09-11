# Data Model: Verified Publication Pipeline

## Verified revision

- **Identity**: Immutable Git commit SHA from the triggering event.
- **Attributes**: event type, full ref, branch or tag name, run id, attempt number, required-check result.
- **Validation**: Checkout HEAD equals the event SHA; Pages eligibility requires main; release eligibility requires a `v*` tag whose commit is an ancestor of main.
- **Relationships**: Produces one approved proof bundle, verified kit artifact, Pages artifact, and release candidate within one workflow run.

## Approved proof bundle

- **Identity**: SHA-qualified artifact name plus the committed canonical proof hashes.
- **Attributes**: source revision, canonical-host runtime and renderer, exactly 32 proof PNGs, proof-coordinate inventory.
- **Validation**: Existing continuity code checks each hash against the approved record before cross-platform comparison; missing, extra, stale, unsafe, or altered inputs fail closed.
- **Lifecycle**: Exported on the canonical Windows host, uploaded read-only, downloaded by the authoritative Linux build, validated, then retained only as workflow evidence.

## Verified kit artifact

- **Identity**: SHA-qualified artifact name produced after all kit verification gates.
- **Attributes**: Eight production kit trees, final manifests, governed hidden icon markers.
- **Validation**: Every kit has zero verifier problems and zero glyph failures; hidden paths are allowlisted; no symlinks or unrelated generated studies are present.
- **Consumers**: Maintainer inspection and release/site generation evidence. It is never a source input for a later revision.

## Pages artifact

- **Identity**: SHA-qualified Pages artifact name within one workflow run.
- **Attributes**: Compressed static export, source SHA, complete eight-brand route and download tree, governed hidden markers.
- **Validation**: Created only after static build, payload/origin tests, browser verification, and artifact audit; contains no symbolic or hard links.
- **State transitions**: `generated` -> `validated` -> `uploaded` -> `eligible` -> `deployed`, or any pre-deploy state -> `rejected`. Pull requests stop at `uploaded`.

## Release candidate

- **Identity**: SHA-qualified normal artifact name within one workflow run.
- **Attributes**: Certified `.skill` and `.zip` files, release notes, source-revision marker, SHA-256 inventory.
- **Validation**: Repository release contract passes before upload; read-only release preflight rechecks version, inventory, hashes, source SHA, and main ancestry after download.
- **State transitions**: `generated` -> `certified` -> `uploaded` -> `preflight-passed` -> `published`, or any pre-publication state -> `rejected`. Non-tag events stop at `uploaded`.

## Publication job

- **Identity**: Event-guarded downstream job in the same workflow run.
- **Attributes**: Target environment, exact permissions, required upstream jobs, artifact name, result URL.
- **Validation**: Pages requires a main push or manual main dispatch; Release requires a `v*` tag push and passed preflight. Publisher jobs contain no checkout, dependency install, or repository script execution.
- **Relationships**: Consumes exactly one artifact from the same verified revision and records one publication outcome.

## Invariants

1. No publisher can run for a pull request.
2. No publisher rebuilds or mutates its consumed artifact.
3. Write and OIDC permissions never exist in a source-executing job.
4. The required `build` status represents all compatibility, proof, kit, release, site, and accessibility gates.
5. Artifact source revision equals the triggering revision and the eventual publication revision.
6. Identity approvals, proof hashes, tolerances, and geometry remain unchanged.
