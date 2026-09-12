# Verification Evidence: Hosted ZIP MIME Compatibility

## Baseline

- **Issue**: [#198](https://github.com/shruggietech/shruggie-brand/issues/198)
- **Branch**: `codex/031-zip-mime-alias`
- **Base revision**: `aac9a02` (`fix(ci): establish verified publication pipeline (S030) (#197)`)
- **Observed production response**: On 2026-09-12, `https://brand.shruggie.tech/i-heart-pr-tours/downloads/i-heart-pr-tours-brand-1.0.0.zip` returned HTTP 200, `Content-Type: application/x-zip-compressed`, `Content-Length: 31687021`, and `Server: GitHub.com`.
- **Pre-change contract**: `.zip` accepted only `application/zip`; ZIP bodies independently required the local-file signature and an end-of-central-directory record.
- **Initial focused suite**: `node --test site/tests/payload-contract.test.mjs` passed 4 of 4 existing tests before the new alias regression was added.

## Spec Kit Analysis

- Specification, plan, tasks, data model, contract, and quickstart use one exact two-value ZIP allowlist and preserve the existing structure checks.
- All 10 functional requirements and 6 measurable success criteria map to implementation or verification tasks.
- No ambiguity, duplication, uncovered buildable requirement, constitution conflict, or unmapped task was found.
- The requirements-quality checklist was reviewed with 14 of 14 criteria satisfied.

## Test-Driven Implementation

- **Red phase**: After adding the required ZIP matrix, `node --test site/tests/payload-contract.test.mjs` failed 2 of 5 tests. The valid production-style alias produced `has content type application/x-zip-compressed, expected application/zip`, and the malformed alias case exposed the same unwanted metadata failure alongside the expected structure failure.
- **Negative baseline**: Valid ZIP bytes labeled `application/octet-stream` or `text/html` remained rejected on media type without a structure false positive. Malformed canonical ZIP cases remained rejected on structure.
- **Green phase**: After adding the alias to the exact ZIP allowlist, the focused suite passed 5 of 5 tests. Coverage includes both supported types, mixed-case and parameter normalization, the maximum ZIP-comment boundary, malformed, empty, HTML, opening-only, and end-only bodies, and valid ZIP bytes under two unsupported types.
- **Diagnostics**: Unsupported media types identify the received value and state `expected application/zip or application/x-zip-compressed`; invalid archive evidence continues to report the ZIP signature and end-record failure independently.

## Local and Production Verification

- **Pinned tools**: Python 3.12.14, Node 24.11.0 for the approved renderer contract, pnpm 10.28.2, resvg 2.6.2, and Playwright Chromium 1234.
- **Focused contract**: 5 of 5 tests passed.
- **Static site**: TypeScript lint and the 81-route Next.js static export passed.
- **Complete local verifier**: 12 of 12 origin/payload contract tests passed, followed by 76 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- **Production response**: The live I Heart PR Tours archive returned HTTP 200 and `application/x-zip-compressed` from GitHub Pages.
- **Production-origin verifier**: All 76 live HTML routes and required downloads passed at desktop and mobile widths with zero WCAG 2.1 AA violations. The hosted ZIP alias produced no payload failure.

## CI-Parity Validation

- `python -m compileall -q scripts skill/templates`: passed.
- `python scripts/build_all.py --list`: reported all eight production brands.
- Publication workflow: 17 tests passed with the expected Windows symlink-privilege skip.
- Package release: 5 tests passed.
- Release contract: 15 tests passed.
- Site preparation: 30 tests passed.
- Identity continuity audit: 4 tests passed.
- Brand contract: 53 tests passed.
- Identity continuity: 22 tests passed.
- Icon kit: 17 tests passed.
- Glyph kit: 34 checks passed with zero failures.
- Full pipeline: 58 tests passed under the exact Node 24.11.0 identity-proof runtime.
- Markdown prose policy: passed.
- `python scripts/build_all.py`: all eight production kits built clean with zero reported problems, including 0 verifier, image-QC, PDF-QC, and pagination failures for I Heart PR Tours.
- Release certification: all 9 v1.2.1 assets and generated notes passed.
- Generated agent contract: unchanged.
- Site lint, static export, local verifier, and production-origin verifier: passed.
- Publication artifact audit: 8 kit markers and 8 site markers passed.
- Python 3.8 itself is not installed on this Windows host; all commands from the compatibility job were exercised under Python 3.12.14, while hosted CI remains the authoritative Python 3.8 gate.
