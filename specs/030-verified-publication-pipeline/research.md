# Research: Verified Publication Pipeline

## Incident baseline

**Decision**: Treat the S028 Pages failure as workflow parity drift, not as an identity or site defect. Pages run `34633145579` selected native `rsvg-convert` and Node 24.20.0, while the approved I Heart PR Tours record requires `node-resvg` on Node 24.11.0. The same revision passed Build run `34633145470`, whose Windows proof export and Linux portable comparison matched the approval contract. Production remains on successful deployment `6382937945` at revision `6c858676396c1963ea2ea0403298aa1a830e13c0`.

**Rationale**: The continuity gate rejected publication before derivative generation, exactly as Constitution P2 and P4 require. Changing identity records or weakening the check would convert a CI configuration defect into unapproved identity drift.

**Alternatives considered**: Rebind the approval to the Pages renderer or loosen renderer equality. Rejected because both violate the approval contract and preserve divergent environments.

## Workflow topology

**Decision**: Consolidate pull-request verification, main Pages deployment, and tagged release publication into the existing `.github/workflows/build.yml`. The authoritative build produces all artifacts once; conditional downstream jobs only publish artifacts from the same run. Delete the independent Pages and Release workflows.

**Rationale**: A single workflow is smaller than a reusable workflow plus three callers, eliminates the exact three-way duplication that caused the incident, preserves same-run artifact lineage, and retains the active ruleset's exact required status context `build`. GitHub documents linking build and deploy jobs in one workflow and using artifacts to pass files between jobs.

**Alternatives considered**: Copy the fixed renderer setup into Pages and Release, rejected because it recreates the drift surface. Use a reusable workflow with thin callers, viable but more YAML and liable to change the visible required-check context. Use `workflow_run` to publish artifacts from another run, rejected because it complicates provenance and introduces a privileged untrusted-artifact boundary.

**References**: [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [workflow artifacts](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts), [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

## Event model and required status

**Decision**: Trigger on pull requests, pushes to `main`, pushes of `v*` tags, and manual dispatch. A manual dispatch is publication-eligible only when its ref is `main`. Remove unrestricted feature-branch push builds because an open pull request currently runs the expensive Build twice for the same revision. Rename the heavy Linux job and add an `always()` aggregate job with id `build` that explicitly fails unless Python 3.8 compatibility, canonical proof export, and authoritative Linux verification all succeed.

**Rationale**: These event filters cover all specified entry points while reducing redundant CI cost. Positive event and ref guards keep pull-request artifacts non-publishing. The repository ruleset `22231594` requires the exact context `build` with no bypass, and a skipped required job must not appear merge-safe.

**Alternatives considered**: Keep unrestricted push, rejected because it duplicates every pull-request head build and provides no additional merge evidence. Rename the required job and update the ruleset, rejected as unnecessary external configuration churn and merge risk. Make the heavy job wait for Python 3.8, viable but adds avoidable latency compared with an explicit aggregate gate.

## Concurrency

**Decision**: Use workflow-level dynamic concurrency that assigns every main run to the `pages` group with cancellation enabled, while assigning pull requests and tags unique groups that do not cancel each other.

**Rationale**: Deploy-job-only serialization cannot stop an older, slower build from reaching deployment after a newer run. GitHub documents workflow-level concurrency and cancellation of an in-progress run in the same group.

**Alternatives considered**: Retain concurrency only in the old Pages workflow or set one group for all events, rejected because the first is deleted and the second would cancel unrelated pull-request and release work.

**Reference**: [GitHub Actions concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency).

## Artifact lineage

**Decision**: Qualify approved-proof, verified-kit, Pages, and release-candidate artifact names with `${{ github.sha }}`. Upload the already-tested `site/out` directly with the Pages artifact action, then give the exact name to the deploy action. Package release files with a source-revision marker and SHA-256 inventory; recheck both after download before publication. Reject symlinks and unexpected hidden files before upload. Include the governed `.iconkit-generated.json` markers explicitly because upload actions exclude hidden files by default.

**Rationale**: Same-run job dependencies plus SHA-qualified names bind consumers to one verified revision. A post-download release inventory catches missing, altered, or extra files before a write token is used. The Pages artifact contract forbids symbolic and hard links, and the current site output intentionally contains eight hidden icon manifest markers.

**Alternatives considered**: Use unqualified artifact names, rely only on transport warnings, or omit hidden files. Rejected because each weakens auditability or silently changes the deployed download tree.

## Permission and supply-chain boundary

**Decision**: Keep workflow and verification jobs at `contents: read`. Grant `pages: write` and `id-token: write` only to the checkout-free Pages deploy job. Grant `contents: write` only to the checkout-free Release publish job. Pin every external action in the touched workflow to a full commit SHA with a readable version comment, disable persisted checkout credentials, and positively forbid `pull_request_target`, `workflow_run`, publisher checkout, and repository-script execution under write tokens.

**Rationale**: Current Pages and Release workflows expose publisher credentials to dependency installation and repository code. GitHub recommends explicit least privilege and identifies full commit SHAs as the immutable action reference. Pull requests remain on the read-only `pull_request` event and receive no secrets or publication path.

**Alternatives considered**: Keep workflow-wide write permissions or mutable major tags, rejected because both broaden the supply-chain blast radius without functional benefit.

**References**: [GitHub Actions security guidance](https://docs.github.com/en/code-security/tutorials/secure-your-organization/protect-against-threats), [Actions repository settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository).

## Release eligibility

**Decision**: Before the write-token publisher runs, use a read-only job to require the `v*` tag version to match certified release metadata, verify the downloaded archive inventory, and prove the tagged commit is an ancestor of `origin/main`. The publisher uses `gh release create --verify-tag` and does not checkout source.

**Rationale**: The repository currently has no tag ruleset. Without an ancestry gate, a correctly named tag on an unmerged commit could publish. The read-only preflight preserves the privileged job as a narrow upload operation.

**Alternatives considered**: Create a test tag, rejected because the owner did not authorize a release. Require a new tag ruleset as part of the code slice, rejected because it is external administration and not needed for the code-level gate; recommend it as defense in depth after S030.

## Validation strategy

**Decision**: Add a focused Python contract suite that reads the workflow and fails on duplicated build paths, obsolete renderer setup, floating runtime versions, mutable action references, broad permissions, unsafe event types, missing ref guards, publisher checkout or repository commands, incomplete dependencies, unqualified artifacts, and missing post-transfer verification. Add an artifact auditor for symlinks and hidden-file allowlisting. Run both in the Python 3.8 and authoritative build gates, then run the full documented repository validation and pinned `actionlint`.

**Rationale**: The failure escaped because Pages did not run on pull requests and no source-level contract related the workflows. The new regression makes the architectural boundary reviewable before merge, while the pull request produces the real Pages and release artifacts without publishing them.

**Alternatives considered**: Rely on YAML review or merge-time deployment alone, rejected because neither is an automated pre-merge regression.
