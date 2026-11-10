# S075 Cloudflare Access and Remaining Work

## Observed Access

The machine-scope registrar credential authenticates and discovers the active shruggie.tech zone. The returned permissions are domain read and zone read only. Reads of alias DNS records, the Single Redirect phase entrypoint and zone rulesets each return HTTP 403. No DNS/rule mutation or write attempt occurred. Credentials and account/zone/record identifiers were not printed or committed.

Process/User credential variables and standard Cloudflare/Wrangler configuration locations did not provide a second usable credential. Available Cloudflare MCP tools provide documentation, not zone mutation.

## Public Baseline

The alias brands.shruggie.tech fails public DNS resolution (ENOTFOUND), so HTTP/HTTPS requests cannot reach it. The canonical HTTPS root returns 200. This is baseline evidence, not successful redirect verification.

## Required Capability

Authenticated access scoped to this zone needs DNS Edit and Single Redirect Edit (Dynamic URL Redirects Write), retaining zone discovery/read. Provisioning and verification can then run without manual dashboard changes.

## Exact Remaining Operations

1. Inspect existing alias DNS and redirect configuration, preserving a private snapshot of affected objects.
2. Reconcile a proxied A record for brands.shruggie.tech using the documented redirect-only 192.0.2.1 address and automatic TTL.
3. Reconcile one stable-reference Single Redirect in http_request_dynamic_redirect, matching exactly `http.host eq "brands.shruggie.tech"`, with target `concat("https://brand.shruggie.tech", http.request.uri.path)`, status 301 and preserve_query_string true.
4. Preserve unrelated records/rules and prefer individual-rule updates over replacing an entire ruleset.
5. Verify proxying, valid alias TLS, root/nested/query requests over both schemes, exact one-hop destination and unchanged canonical routes.
6. Run reconciliation again and prove no duplicate record/rule or unnecessary mutation.
7. Record redacted before/after evidence and rollback. Rollback restores only affected objects from their snapshots and deletes only objects created by this operation.

All provisioning, TLS/redirect checks, repeat-run proof and exercised rollback remain outstanding. Issue #352 remains open.

## Official References

- [Redirect-only DNS and hostname redirect](https://developers.cloudflare.com/fundamentals/manage-domains/redirect-domain/)
- [Single Redirect API and permissions](https://developers.cloudflare.com/rules/url-forwarding/single-redirects/create-api/)

## Certificate Restoration Access, 2026-11-10

The saved GitHub-linked browser profile signs in but has no domains. The other saved profile reaches a two-factor authenticator challenge; the owner was asked to complete it while independent Pages work continues. No DNS/rule mutation occurred and the API permission blocker remains.

Separately, GitHub reports certificate bad_authz despite valid current edge/origin TLS. An unchanged-domain Pages API save unexpectedly cleared https_enforced, and GitHub rejects restoring true because certificate issuance is incomplete. The documented same-domain provisioning reset did not restore eligibility. DNS health sees Cloudflare proxying and is_https_eligible=false, with no CAA or current HTTPS error. Canonical configuration inspection and actual HTTPS-flag restoration remain outstanding; this certificate state has not been established as the cause of Pages syncing timeouts. The alias/redirect work above remains open and untouched.
