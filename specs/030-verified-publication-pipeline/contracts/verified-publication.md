# Verified Publication Contract

## Authoritative workflow

- `.github/workflows/build.yml` is the sole entry point for pull-request validation, main publication, manual main recovery, and `v*` tag release publication.
- `.github/workflows/pages.yml` and `.github/workflows/release.yml` do not exist after migration.
- The workflow accepts `pull_request`, `push` limited to `main` and `v*`, and `workflow_dispatch`.
- The externally required status remains exactly `build` and cannot succeed until Python 3.8 compatibility, canonical proof export, the authoritative Linux build, release certification, site validation, and artifact audits succeed.

## Verification permissions

- Workflow default: `contents: read` and no other permission.
- Checkout uses the triggering SHA with persisted credentials disabled.
- Verification jobs do not receive Pages, OIDC, release-write, issue-write, pull-request-write, action-write, or secret permissions.
- The workflow does not use `pull_request_target`, `workflow_run`, inherited secrets, cross-run artifact discovery, or user-selected artifact paths.

## Renderer and proof contract

- Node version is exactly `24.11.0` and `@resvg/resvg-js` is exactly `2.6.2` in both proof export and authoritative build.
- Native `rsvg-convert` is absent from the production path.
- The Windows proof artifact name includes the triggering SHA and contains only the expected canonical evidence tree.
- The Linux build downloads that exact same-run artifact, sets `GP_APPROVED_PROOF_ROOT` for continuity tests, kit generation, and site preparation, and preserves all existing fail-closed comparisons.

## Pages artifact and deployment

- The verified build uploads `site/out` directly with the Pages artifact action after all site tests and artifact audits pass.
- The Pages artifact name includes the triggering SHA and includes the allowlisted hidden icon manifests.
- The artifact contains no symbolic or hard links.
- Pull requests and tags may produce the artifact as evidence but cannot deploy it.
- The deploy job positively requires either a push to `refs/heads/main` or manual dispatch on that exact ref, depends on the authoritative `build` result, and passes the exact SHA-qualified artifact name to the deployment action.
- The deploy job has only `contents: read`, `pages: write`, and `id-token: write`; it performs no checkout, dependency installation, build, test, or repository-script execution.

## Release candidate and publication

- The verified build packages and certifies the repository's current release metadata and archives before upload.
- The SHA-qualified release artifact contains a source-revision marker, a SHA-256 file inventory, release notes, and the certified release files.
- A read-only preflight runs only for a `push` to a `refs/tags/v*` ref, downloads the exact same-run artifact, verifies source SHA, version, inventory, file hashes, expected release contents, and tagged-commit ancestry on `origin/main`.
- The publish job depends on both the authoritative `build` result and release preflight, has only `contents: write`, performs no checkout or repository-script execution, rechecks the transport inventory using standard runner tools, and creates the release with tag verification.
- Pull requests, main pushes, manual runs, non-version tags, failed preflights, and cancelled superseded runs create no release.

## Artifact audit

- `dist/` and `site/out/` must be real directories below the repository root.
- Neither tree may contain symbolic links.
- Hidden paths are rejected except for `.iconkit-generated.json` files in the governed per-brand icon locations.
- The Pages tree contains exactly one governed hidden icon marker per public production brand.
- Artifact uploads use hidden-file inclusion only after the audit passes.

## Action provenance

- Every external `uses:` reference in the authoritative workflow is a full 40-character commit SHA with an adjacent readable version comment.
- Local actions are allowed only by explicit repository-relative path.

## Failure behavior

- Any failed or skipped prerequisite makes `build` non-successful and blocks both publishers.
- Missing, renamed, altered, extra, wrong-revision, or unsafe artifacts fail before publication credentials are exercised.
- A failed Pages run leaves the last successful deployment active.
- A failed release run creates no release and never moves or recreates a tag.
