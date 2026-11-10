# S075 Research and Decisions

## Baseline

Fetched clean main is `661fde256724a36530523096e6f3a2ef2ab2006a`; latest official release is v3.1.1. Three issues (#328/#352/#353) are open. Eleven dependency PRs are outside this slice.

## Presentation

Decision: label-free cover, actual slogan 23pt and supporting copy 13.5pt/1.5 leading. Rationale: the owner explicitly prefers this hierarchy. Secondary labels were considered but no demonstrated reader need outweighs the preferred presentation. Reference sections retain labels.

Decision: validate explicit message-value content rather than require a visible role-label prefix. Rationale: present validation hardcodes labels in both HTML and PDF. Simply dropping checks was rejected; exact copy, role/use equality, duplicates and unauthorized substitution remain enforced.

Decision: measure cover bounds in Chromium and paginate rich copy without shrinking. Rationale: fixed A4 pages currently use overflow:hidden, so larger text alone can silently clip. Truncation and global font reduction were rejected.

## Copy Approval

Decision: approve `Learn to dance with Greg "Krucial" Carney.` dated 2026-11-09 with issue #353 provenance. Existing desktop/mobile components already consume approvedMessaging.short_description. Independent social-image approval remains unchanged.

## External Access and Publication

Decision: report #352 blocked by management permissions. Machine-scope registrar authentication discovers the active zone but DNS/redirect/ruleset reads return 403; no write was attempted. See [cloudflare.md](cloudflare.md).

Decision: prepare one coordinated patch candidate and honor the autopilot pre-push checkpoint. Pages deploys only after tagged release publication, so a local commit cannot establish live completion. Existing hidden process utilities and foreground awaited checks remain in use.

## Required Validation-Fixture Audit Follow-up

The documented npm audit gate found nine findings in the pinned WordPress fixture (eight moderate, one high). Exact overrides now select glob 14.0.2, minimatch 11.0.1 and isomorphic-git 1.38.6. Existing request/download/Git/YAML tests and a real matching/rimraf deletion regression pass (12/12), and the moderate audit threshold reports zero vulnerabilities. Node 26.5.0/npm 11.17.0 satisfy the existing Playground dependencies; Node 24.11.0 emitted engine warnings. Consumer adapter APIs and the unrelated dependency PR backlog remain unchanged.

Primary references: [glob advisory](https://github.com/advisories/GHSA-3g3m-2fjr-6pw4), [minimatch advisory](https://github.com/advisories/GHSA-g3hv-75wg-m249), [isomorphic-git advisory](https://github.com/advisories/GHSA-9qw7-j9xw-fv9c), and [glob API changes](https://github.com/isaacs/node-glob/blob/main/changelog.md). The API changes are why the real fixture matching/deletion regression is required rather than relying only on a green audit.

## Pages Recovery, 2026-11-10

Official deploy-pages uses the executing workflow GITHUB_SHA as deployment version and resolves artifacts from the current run. Official upload-pages-artifact delegates upload of artifact.tar to upload-artifact, and custom compliant artifacts are supported. Therefore a fresh reviewed main controller can transport the original unchanged TAR while keeping released content identity inside it. This is an operational recovery experiment; stale-context causation is not proven before activation. See [official context](https://github.com/actions/deploy-pages/blob/368f82528645a54fb793d4d04e342629a3f51346/src/internal/context.js), [API client](https://github.com/actions/deploy-pages/blob/368f82528645a54fb793d4d04e342629a3f51346/src/internal/api-client.js), [artifact contract](https://github.com/actions/upload-pages-artifact#artifact-validation) and [custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages). A research agent independently checked these interfaces without mutations.

GitHub documents same-domain remove/re-add for certificate provisioning reset, but no separate supported ACME force/retry endpoint. HTTPS enforcement can remain unavailable until issuance completes. GET pages/health is an asynchronous diagnostic, not a certificate-reset operation. Current edge/origin TLS remains valid; enforcement restoration is separately tracked after the settings API cleared it. No causal claim joins bad_authz to activation failure.
