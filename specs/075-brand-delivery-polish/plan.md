# Implementation Plan: Brand Messaging and Delivery Polish

**Branch**: `codex/075-brand-delivery-polish` | **Date**: 2026-11-09 | **Spec**: [spec.md](spec.md)

## Summary

Resolve #328 and #353 through shared message projection and one coordinated patch candidate. Their released/live acceptance is complete. Phase 11 resumes #352 with the existing authenticated browser and DNS token, after its original independent access blocker.

## Technical Context

- **Language/Version**: Python 3.8+ compiler, Node.js 20+ static Next.js site, pinned pnpm 10.28.2.
- **Dependencies**: Existing messaging/essentials, Chromium, PyMuPDF, coloraide and publication pipeline.
- **Storage**: Canonical source and Spec Kit evidence in Git; generated proofs/builds in ignored dist or isolated temporary directories.
- **Testing**: Focused projection/layout regressions, full contributor and CI-parity checks, thirteen kit builds, site/accessibility/publication contracts.
- **Target**: A4 PDF/print HTML, portable/hosted guidelines, desktop/mobile portfolio, Cloudflare edge alias.
- **Performance**: Preserve static delivery without additional client network requests.
- **Constraints**: Exact copy, unchanged logo geometry, WCAG AA, hidden noninteractive Windows subprocesses, UTF-8 without BOM/LF, source-only commits.
- **Scale**: Thirteen production kits, three issues, one patch candidate.

## Constitution Check

P1: Generated output stays ignored and fixtures temporary. P2: No identity redesign. P3: Measure text contrast and layout. P4: Rebuild all production kits and run full documented checks. P5: Site consumes generated approved messages. P6: Installed Spec Kit and version/migration metadata stay synchronized. No exceptions; post-design review reaches the same result.

## Research and Decisions

- Prefer label-free cover per owner direction; supersede S067 only for opening presentation, retaining reference labels and semantic roles.
- Slogan uses 23pt declared display face/weight. Supporting copy uses 13.5pt body, 1.5 leading and foreground on declared page ground with measured AA contrast.
- Explicit data-message-value content is compared exactly within data-message-role wrappers. Optional reference labels stay separate; legacy labeled reference output remains accepted. Duplicate/nested roles and unauthorized text remain errors.
- Measure cover layout before PDF export. Overflow uses identified continuation sheets at unchanged readable sizes. Whole roles move first; unusually long individual roles split at word boundaries with explicit ordered fragments whose reconstructed text must match exactly. This stays confined to opening messages, not a general layout engine.
- DanceWithMe865 short-description uses include visual-guide, strategy-reference, site-metadata and consumer-data, following the requested existing surfaces. Social-image copy/composition remains unchanged.
- Cloudflare research agent confirmed zone discovery succeeds, but DNS, redirect entrypoint and ruleset reads return 403. No mutation is attempted. Record required DNS Edit and Single Redirect Edit access and remaining work in cloudflare.md.
- Prepare v3.1.2 compiler/site and affected kit patch metadata under existing version policy, retaining Brand Canon/adapter versions. Honor the usual pre-push halt; live completion requires subsequent authorized tagged publication.
- Custom checklist markers remain reviewer-owned. The explicit autopilot kickoff authorizes proceeding after analysis without an additional inter-step permission request.

## Implementation Order

1. Complete specify, clarify, checklist, plan and tasks, then blocking analyze.
2. Preserve Local Media Gallery before proof; add exact-message and rendered layout tests before implementation.
3. Update canonical copy/continuity hashes, shared generator/verifier, tests and superseded prose/contracts.
4. Document exact Cloudflare blocker and reconciliation/rollback procedure.
5. Coordinate metadata, rebuild all kits, run documented validation, inspect renders and audit source/encoding hygiene.
6. Commit locally and present pre-push review. PR/release/Pages and issue closure remain pending authorization and live evidence.

## Project Structure

Source: brands/dancewithme865/brand.json and continuity record; skill/templates/gen_guide_pdf.py, verify.py and focused cover-layout helper/tests; S067 projection contract/prose; existing release metadata/history sources. Evidence: specs/075-brand-delivery-polish/. New behavior remains in shared templates.

## Complexity Tracking

No constitution exceptions. No unrelated dependency upgrades.

## Validation Follow-up Decision

The required WordPress fixture audit discovered current transitive findings. T016/T017 add a bounded validation-only repair with exact patched versions and a real glob/rimraf filesystem compatibility check; the existing audit threshold remains unchanged. This is necessary to complete the documented gate, rather than an expansion into the unrelated dependency PR backlog. Supplemental cross-artifact analysis confirms coverage under FR-009/FR-010 and no new constitution conflict.

## Initial Publication Outcome

The owner authorized remote/publication work on 2026-11-10. PR #354 passed review and CI, merged, and its exact v3.1.2 tag published the verified official release. Three Pages attempts failed to finalize despite a verified artifact. Live acceptance and #328/#353 closure remain pending the recovery in [deployment.md](deployment.md); #352 retains its independent permission blocker. No done-gate was weakened or external completion inferred from artifact checks.

## Pages Recovery Investigation, 2026-11-10

The original artifact and tagged publication are qualified; the serving origin remains at v3.1.1. The pinned deploy-pages SHA is actually upstream v5.0.1 (its existing version comment is stale), and it correctly requires succeed. Certificate metadata reports bad_authz while current origin TLS still validates; causation is unproven. First re-save only the already configured cname, workflow build type and HTTPS flag through the Pages API, preserving a private before/after snapshot. This low-impact diagnostic requests settings/provisioning refresh without domain removal, DNS mutation or HTTPS disable. Observe API and public state before retrying. If it does not resolve activation, design a fresh deployment-controller context that transports only the original CI-qualified release artifact, then run a supplemental analysis before implementation. Do not retag, replace official assets, accept intermediate states as success or add unverified main content to the released site.

### Certificate refresh finding

The unchanged-setting PUT with HTTPS=true was rejected because the certificate has not finished being issued. Re-saving only cname/build_type succeeded but unexpectedly cleared https_enforced; restoring that flag alone is rejected with the same certificate error. Public HTTP still redirects to HTTPS and current TLS validates. The initial no-domain-reset choice is superseded by the demonstrated need to restore enforcement: use GitHub's documented same-domain remove/re-add provisioning reset, paired immediately through the API with the existing private snapshot, then restore HTTPS as soon as issuance allows. Preserve all DNS and release/artifact state. This changes the operational repair method, not the required final hostname or HTTPS behavior.

## Qualified-artifact Recovery Design

Add main-only manual recovery preparation and Pages deployment jobs to the existing Build workflow. Existing PR/main/tag verification and normal publishers retain their gates. Manual dispatch inputs select a published tag and its original Build run; the helper validates repository, push-tag event, immutable commit, completed required verification/preflight/publication jobs, unexpired SHA-qualified artifacts and artifact digests. Export the immutable tagged source through git archive and run its own release/publication/documentation contracts against the downloaded original candidate. Compare the candidate with official release asset digests, checksums and notes. Validate the original Pages envelope, member paths/types, publication identity and hosted release ZIP hashes. Default to re-uploading artifact.tar byte-for-byte under a recovery-specific name; the separately specified USTAR representation test may change headers only, with complete member equivalence. Never regenerate the site or rewrite its publication record.

The official deployment action runs under the new legitimate controller GITHUB_SHA. Record controller revision separately from released content revision; do not override platform identity. This isolates stale deployment context while retaining qualified content. Preparation has read permissions; the deployment job has Pages/OIDC permissions, uses the github-pages environment and contains only the pinned official action. Both Pages jobs share non-canceling concurrency. Workflow-level main cancellation applies only to push events so a manual recovery cannot cancel main verification. No official release write occurs in recovery. Normal QA still runs on dispatch; original source qualification is validated before artifact promotion.

Alternatives rejected: another immediate retry retains the failed deployment context; accepting finished_file_sync would fake success; changing the published tag/assets breaks immutability; rebuilding main would change released content. A separate unguarded workflow would duplicate publication authority. The chosen path stays in Build and reuses existing tagged contracts. Root cause remains an operational hypothesis until the same qualified TAR succeeds under the new context.

## Fresh-controller Result and Supported Diagnostics, 2026-11-10

PR #357 passed exact-head review and full CI, then merged as 084db71ce50aab496e4addd80a2742e8c2300463 with the identical reviewed tree. Recovery run 42794179226 passed its hosted source/artifact/release preflight and uploaded unchanged TAR SHA-256 6bcf0f5a7b0e958a6717ff3bc071b5ea80ab3f93e55524c35fd9385aa7eb4879 as artifact 13753053015. The official deployment still remained syncing_files and timed out at ten minutes. Reusing the original controller is therefore insufficient to explain the failure. Content, certificate and backend causes remain unproven.

A proposed longer timeout was rejected during research before implementation: pinned deployment.js clamps timeout to MAX_TIMEOUT=600000 and GitHub documents a ten-minute service limit. An 1800000 input would be ineffective; a custom controller would exceed the documented service envelope and add unsupported publication maintenance. Retain the official action and existing explicit-success semantics. Collect API request IDs/statuses, confirm cancellation, and perform one debug-enabled retry of only the original deployment job. Keep normal source verification running and preserve the existing live site, tag and release assets.

Browser investigation found the saved GitHub-linked Cloudflare profile has no domains. The other saved profile reaches an authenticator challenge; the owner was asked to complete sign-in while independent Pages/CI work continues. No DNS/rule mutation occurred. HTTPS restoration remains an explicit outstanding regression until GitHub accepts it and readback confirms true.

## Conditional Format-only Packaging Test, 2026-11-10

If the debug retry also stalls, use one main-dispatched recovery_ustar boolean input (default false) to test POSIX USTAR representation. Original TAR inspection found 916 valid GNU long-name records, 4,308 regular files and 750 directories. All effective paths fit USTAR prefix/name fields, with maximum path length 143 ASCII bytes. These GNU records are normal packaging, not proof of a defect. The test isolates archive representation while retaining the official action and ten-minute cap.

Stream original logical members directly into tarfile.USTAR_FORMAT, preserving effective names, member order, directory entries, types, real-member modes, ownership and timestamps. Reject unrepresentable names or metadata instead of truncating, renaming or extracting through the filesystem. Independently reopen both archives and require equal ordered member records with regular-file path, size and SHA-256, directory set and preserved metadata. Recheck qualified publication and hosted release ZIP binding. Retain the original archive, original/new TAR digests and both manifests privately; expose only content/controller/format/manifest provenance receipts in CI.

Default original transport stays unchanged. USTAR mode changes only the archive representation and resulting artifact identity, never site file bytes, release assets, approved source, publication identity or permissions. It is a controlled packaging hypothesis. If it also stalls, stop format experiments and seek GitHub-side investigation with the diagnostic packet.

## Standard Publication Format and Closeout, 2026-11-10

The controlled USTAR deployment succeeded at 11:11 UTC while Cloudflare remained in its original proxied state. Preserve the same pinned official upload/deploy actions and adopt step-local TAR_OPTIONS=--format=ustar for normal Linux Pages packaging. Upstream source has no conflicting format flag and retains RUNNER_TEMP/artifact.tar until job cleanup. Immediately validate that TAR through a read-only verify-archive CLI using the existing strict USTAR/member checks. This stays inside verified-build, so aggregate build, release preflight and normal publication require its success. Recovery transport remains original by default with explicit optional USTAR; future normal tags use the tested USTAR representation automatically.

Current paths and metadata fit USTAR. Unrepresentable future data must fail packaging/validation with an explicit error rather than silently alter names/content or fall back to another format. This is a representation limit, not a new brand-eligibility rule. The default format choice is supported by successful activation, but the exact GitHub backend cause of GNU-format stalls remains unproven. Keep all normal quality/security gates and permissions.

The owner subsequently approved a temporary canonical DNS-only window for certificate repair. GitHub then recognized HTTPS eligibility, same-domain reprovisioning produced an approved certificate through 2027-02-08, and HTTPS enforcement was restored/read back true. Cloudflare proxying, target, Auto TTL and comment were restored to their original values. Direct-origin HTTP now redirects 301 to canonical HTTPS. This separate repair occurred after successful Pages activation. Issues #328/#353 closed after live acceptance; #352 remains open with the machine API permission blocker and untouched alias/redirect work.

## Alias Completion, 2026-11-10

Continue US3/T014 on codex/075-cloudflare-alias. The environment inventory found existing CF_DNS_API_TOKEN in User scope; the registrar credential is not the DNS credential. The authenticated dashboard confirmed existing Zone Read/DNS Edit, and the owner approved adding a separate Single Redirect Edit policy scoped only to shruggie.tech. API access is now available. No new credential, canonical DNS change or publication is needed.

Implement scripts/cloudflare_alias.py using Python 3.8 standard-library HTTPS APIs and scripts/test_cloudflare_alias.py using isolated in-memory API fixtures. Commands apply, rollback and verify consume the existing token from process environment or Windows User environment. Store snapshots, object IDs and operation receipts only under ignored dist/private; emit redacted summaries. Disable API redirects so Authorization cannot follow another origin; report HTTP status/error codes without raw credential-bearing responses.

Discover the exact zone and snapshot its DNS and dynamic-redirect entrypoint. Treat 401/403 as failure; only an actual missing entrypoint 404 permits creation. Reconcile one proxied A record at brands.shruggie.tech to 192.0.2.1 with TTL 1. Reconcile one stable-ref exact-host 301 rule preserving path/query, using individual-rule operations and first position while retaining relative order and contents of other rules. Preserve DNS comments/tags and only replace the alias address fields. Abort ambiguous duplicate alias/rule identities.

Each apply writes a private before snapshot and operation receipt before proceeding. Record the affected objects after each successful write. Repeat correct reconciliation performs zero API writes. Scoped rollback reverses only recorded mutations after checking the current managed object still matches the applied definition; preserve newly added unrelated objects. Never overwrite a whole existing ruleset. Verify unrelated DNS/rules and canonical configuration unchanged after apply/rollback/reapply. A transport timeout does not establish that a write stopped: inspect current state before retrying.

Live verification uses normal TLS validation and redirect-disabled HTTP/HTTPS requests for root, nested paths and encoded/repeated/empty query parameters, requiring an exact one-hop 301 to canonical HTTPS and destination 200. Inspect public alias DNS, canonical routes and release identity. Preserve zone-wide HTTPS/security settings. Exercise rollback against only the newly provisioned alias objects, then reapply and verify the final no-op. Run focused isolation/auth/redaction/rollback tests, all applicable source checks and required hosted qualification/review before protected merge and issue closure. Existing release assets/tag remain unchanged.
