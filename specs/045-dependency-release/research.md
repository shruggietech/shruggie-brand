# Research: Dependency Integration and 2.0.1 Release

## Decision: Combine the two pending groups

**Evidence**: PR #225 proposes Next 16.3.5, React/React DOM 19.3.0, and matching React types. PR #226 proposes Playwright 1.63.0, Tailwind/PostCSS 4.3.3, Node types 26.6.2, Fumadocs MDX 15.4.1, and TypeScript 7.0.2. Both modify only `site/package.json` and `site/pnpm-lock.yaml`. Their kickoff heads are `3400a23c44e494be27424be2a30a417625f591f4` and `72f90bd274c4fe65f8da4eda3d4fc0dcd00d15e1`.

**Rationale**: One generated lockfile is required for a consistent combined install. The runtime PR is green independently; the tooling PR fails release packaging because browser provisioning is incomplete.

**Alternative**: Merge both bot PRs separately. Rejected because the tooling PR is red and their combined dependency graph would not be tested as one release candidate.

**Integration finding**: The first combined site build failed because `fumadocs-mdx` 15.4.1 imports `fumadocs-core/server`, absent from the pinned Core 16.14.3. Its declared peer range starts at Core 16.15.3. Pair Core and UI at 16.15.11, then rerun the complete site gates. This is a required compatibility companion to #226, not an unrelated update.

## Decision: Preserve separate Playwright versions, install both browsers

**Evidence**: The failed PR #226 build installed the Node Playwright 1.63.0 Chromium revision, while the Python verifier pinned to Playwright 1.62.0 reported headless Chromium unavailable and omitted `brand-guide.pdf`. Release archive verification then failed. [Playwright's browser documentation](https://playwright.dev/python/docs/browsers) states that each Playwright version needs its own browser binary and documents multi-version browser garbage collection.

**Rationale**: Installing both browser revisions is the smallest correction and keeps each existing client pinned. Suppressing browser garbage collection during the two installs prevents one client install from removing the other's revision.

**Alternative**: Advance Python Playwright to 1.63.0. Deferred because that broadens the Python dependency surface beyond the pending site PRs and is unnecessary for the release.

## Decision: Publish after owner merge

**Evidence**: `.github/workflows/build.yml` release preflight requires the tag name to equal the current version and its source commit to be an ancestor of `origin/main`; the publisher consumes the same-run verified candidate.

**Rationale**: Preserve the existing exact-revision and main-ancestry release contract. `v2.0.1` is not yet tagged; 2.0.1 changelog and migration notes already exist from S044.

**Alternative**: Tag the feature branch before final review. Rejected because the release contract would fail main ancestry.
