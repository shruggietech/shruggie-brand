# Release Candidate Contract

1. `site/package.json` and `site/pnpm-lock.yaml` encode the same combined direct dependency versions from intake PRs #225 and #226, and a frozen install succeeds.
2. The verified build provisions a Chromium revision for both the pinned Python and updated Node Playwright clients. A missing client browser is a failure, not a skipped full-tier release candidate.
3. Existing kit verification, glyph validation, site lint/build/test, WCAG checks, archive contract, and publication audit remain mandatory.
4. `v2.0.1` is pushed only for the exact reviewed commit after that commit is merged to `main`; the existing tag-triggered workflow alone publishes the official release assets.
5. The PR may receive one automatic and at most one requested additional Codex review round. Every actionable review thread is answered and resolved before owner merge notification.
