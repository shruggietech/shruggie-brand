# S075 Validation Guide

Use the repository virtual environment and pinned pnpm 10.28.2 through hidden, redirected, noninteractive launchers.

1. Run focused messaging/cover tests. Approved label-free covers pass; wrong/duplicate roles, text drift and unauthorized values fail.
2. Rebuild thirteen kits using `python scripts/build_all.py`; run full CONTRIBUTING.md validation and `.github/workflows/build.yml` CI parity. Require zero verifier, glyph and applicable PDF QC failures.
3. Inspect Local Media Gallery before/after and representative light/dark, wrapping/rich and sparse covers. Record typography, contrast and bounds rather than byte-comparing PDF/PNG output.
4. Run site lint/build/test; inspect exact DanceWithMe865 copy on desktop/mobile, 200% text enlargement and 320 CSS-pixel reflow on changed responsive surfaces.
5. Verify coordinated release/package metadata and source-only Git, UTF-8 without BOM/LF and mojibake hygiene.
6. Follow [cloudflare.md](cloudflare.md) for #352; denied DNS/rule access is a blocker, not completion.
7. Present local commit evidence at the pre-push checkpoint. After explicit publication authorization, require exact-head CI/review, tagged release/Pages and direct live checks before issue closure.
