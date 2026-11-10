# S075 Cloudflare Alias Contract

- Exact source brands.shruggie.tech; canonical destination https://brand.shruggie.tech.
- One proxied A record to redirect-only 192.0.2.1, TTL 1 (automatic).
- One enabled Single Redirect with ref s075_brands_canonical_redirect, expression `(http.host eq "brands.shruggie.tech")`, action redirect, dynamic target `concat("https://brand.shruggie.tech", http.request.uri.path)`, status_code 301 and preserve_query_string true. Place it first without changing relative order or definitions of unrelated rules.
- API uses existing CF_DNS_API_TOKEN, never prints credentials/private IDs, and cannot forward Authorization through HTTP redirects. DNS/redirect access failure is not an absent object.
- Apply inspects before mutation, records affected object state privately, preserves unrelated DNS/rules and canonical settings, and is a no-op when already correct. Ambiguous duplicate managed objects fail before writes.
- Rollback reverses only receipt-owned mutations after checking for managed-object drift. Preserve unrelated additions; do not replace an existing ruleset. Keep a private snapshot and redacted evidence.
- Verify eight HTTP/HTTPS root/nested/query cases with valid TLS and redirects disabled. Require exact 301 Location preserving raw path/query, then a canonical 200 with no extra redirect. Canonical routes and released identity must remain available.
- Exercise scoped rollback, reapply and zero-write repeat reconciliation. Close #352 only after operational evidence and required source review/qualification.

Known successful writes in a partial receipt can be rolled back only when live managed objects and rule position match the reconstructed applied state. Unknown write outcomes or intervening edits must fail before reversal.
