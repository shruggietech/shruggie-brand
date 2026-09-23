# Research: Repository Front Door and v2.0.3 Release Readiness

## Canonical brand destinations

**Decision**: Validate README site links against `site/generated/routes.json` after the existing site preparation step. The site route builder declares each brand overview at `/{slug}/guidelines/`, not `/{slug}/`.

**Rationale**: The generated route contract is already the source consumed by the site. A second slug list would recreate the drift that broke the README. The CI build already prepares this artifact before site export.

**Alternatives considered**: Hard-coded eight-link allowlist (stale on new brand), live HTTP checking in CI (network and deployment timing flakiness), route parsing from source text (brittle).

**Review refinement**: Keep navigation links distinct from image resources and include both angle-bracket Markdown autolinks and bare GitHub-autolinked URLs. An image URL cannot satisfy a required brand or release destination even when the target itself is valid. Reject percent-encoded URL authorities before host trust checks, since browser normalization can turn one into the canonical site host.

## Release guidance during source-versus-publication lag

**Decision**: Point public README downloads to the official latest release page, describe asset roles without fixed-version filenames, and leave exact-version pinning to release assets and checksums.

**Rationale**: Source is 2.0.3 while the latest published release is v2.0.1. A fixed candidate URL in a pre-merge README would be broken until tag publication.

**Alternatives considered**: Link directly to anticipated v2.0.3 assets (premature), retain 2.0.0 names (stale), automatically query GitHub at CI time (network coupling).

## README branding and badges

**Decision**: Use the existing approved `logo-lightbg.png` and `logo-darkbg.png` with theme-aware GitHub HTML and a text heading fallback. Show Build, latest-release, and explicitly code-only Apache-2.0 badges.

**Rationale**: Existing approved artwork avoids identity edits. A code-only license label prevents a false impression that brand marks are freely licensed. Badge links target the workflow, release landing page, and code license.

**Alternatives considered**: New banner rendering (unapproved identity derivative), one logo for both themes (illegible text), a generic license badge (ambiguous brand-rights claim).

## Issue scope and release sequence

**Decision**: Trace S049 to issue #259. Leave #193 (light-first brand systems), #194 (custom imagery), and downstream repins out of scope. Complete release readiness in the PR; tag and publish only after owner merge.

**Rationale**: #193 and #194 require separate generator/identity contracts; source 2.0.3 already has its own release identity. The existing tag workflow certifies main ancestry and builds exact-revision assets.

**Alternatives considered**: Bundle either open issue into the release PR (would change kit bytes and release identity), verify consumer adoption (outside this repository's ownership), publish before merge (violates exact-main gate).
