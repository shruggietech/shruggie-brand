# S075 Validation Guide

Use the repository virtual environment and pinned pnpm 10.28.2 through hidden, redirected, noninteractive launchers.

1. Run focused messaging/cover tests. Approved label-free covers pass; wrong/duplicate roles, text drift and unauthorized values fail.
2. Rebuild thirteen kits using `python scripts/build_all.py`; run full CONTRIBUTING.md validation and `.github/workflows/build.yml` CI parity. Require zero verifier, glyph and applicable PDF QC failures.
3. Inspect Local Media Gallery before/after and representative light/dark, wrapping/rich and sparse covers. Record typography, contrast and bounds rather than byte-comparing PDF/PNG output.
4. Run site lint/build/test; inspect exact DanceWithMe865 copy on desktop/mobile, 200% text enlargement and 320 CSS-pixel reflow on changed responsive surfaces.
5. Verify coordinated release/package metadata and source-only Git, UTF-8 without BOM/LF and mojibake hygiene.
6. Follow [cloudflare.md](cloudflare.md) for #352; denied DNS/rule access is a blocker, not completion.
7. Present local commit evidence at the pre-push checkpoint. After explicit publication authorization, require exact-head CI/review, tagged release/Pages and direct live checks before issue closure.

## Qualified-artifact Recovery Validation

Run scripts/test_pages_recovery.py and scripts/test_publication_workflow.py through the hidden launcher. Exercise the helper resolve/prepare phases against original run 42764281217 and tag v3.1.2 in a new ignored staging directory; require original source, official release and TAR transport checks to pass. After reviewed main contains the recovery jobs, dispatch Build on main with recovery_tag=v3.1.2 and recovery_run_id=42764281217. Wait for explicit recovery deployment success, then run the prepared HTTP/archive/PDF and eighteen-case browser acceptance. Restore and verify GitHub HTTPS enforcement before declaring recovery complete. Never dispatch the old tag as the new controller or overwrite its platform SHA.

If a fresh controller also stalls, retain the official ten-minute cap and explicit success requirement. Capture Pages API response request IDs and cancellation status; a debug-enabled job retry can add action diagnostics. The pinned action ignores timeout values above ten minutes, matching the documented service limit.

After reviewed USTAR support is merged, the conditional packaging test adds recovery_ustar=true to the same main dispatch. The helper must prove ordered full-member content/metadata equivalence, preserve the original archive and record both TAR hashes. Keep the normal ten-minute action cap and require explicit succeed plus live acceptance.

Normal publication now selects USTAR only for the official Pages upload step, then runs verify-archive against RUNNER_TEMP/artifact.tar. Exercise the CLI against a valid USTAR TAR and the original GNU TAR; require success and explicit rejection respectively. Required hosted CI must validate its real producer archive.

For the alias continuation, use the existing CF_DNS_API_TOKEN in process or Windows User scope. Run scripts/test_cloudflare_alias.py before operational use. scripts/cloudflare_alias.py apply --state-dir dist/private/s075/cloudflare-alias writes a private receipt and redacted change count; a repeat should report zero changes. Use rollback --receipt with the first change receipt to exercise only the recorded alias changes, then apply again. verify requires eight exact one-hop redirects with normal TLS validation and canonical destination 200. Keep private receipts/IDs/tokens outside Git.
