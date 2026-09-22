# Quickstart: Validate the 2.0.1 Release Candidate

Run from the repository root on a headless, non-interactive environment with the documented Python and Node toolchains.

1. `python scripts/test_publication_workflow.py` must pass the browser-provisioning and publication fail-closed contract.
2. `pnpm --dir site install --frozen-lockfile`, `pnpm --dir site lint`, `pnpm --dir site build`, and `pnpm --dir site test` must pass.
3. Run the full test and kit-build commands listed in `.github/workflows/build.yml`; require zero verifier problems, zero glyph failures, complete PDFs, and passing release archive certification.
4. On the official PR, require successful `python-38-compatibility`, `approved-identity-proofs`, `verified-build`, and terminal `build` checks. Process all review threads and reaction-only bot outcomes.
5. After owner merge, confirm `v2.0.1` points to the merged `main` commit. Wait for tag-run `release-preflight`, `publish-release`, and `deploy-pages`, then inspect official release assets and checksums.
