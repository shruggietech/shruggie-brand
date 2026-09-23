# Research: Post-Merge Dependabot Refresh

**Intake time**: 2026-09-22 23:36 UTC, after #241 merged at 23:34 UTC. No `v2.0.1` tag or release existed at intake.

| PR | Bot head | Dependency | Proposed version | Verified revision or source |
| --- | --- | --- | --- | --- |
| #242 | `5a0a656` | pnpm/action-setup | 6.1.0 | `ea17c68df8912ef543352723c149a84f56e3d413` (peeled annotated tag) |
| #243 | `2127658` | actions/setup-python | 7.0.0 | `5fda3b95a4ea91299a34e894583c3862153e4b97` |
| #244 | `240993b` | fontTools | 4.65.0 | Dependabot Python requirements update |
| #245 | `0ea26b9` | actions/download-artifact | 8.0.1 | `3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c` |
| #246 | `b9d109e` | Playwright Python | 1.63.0 | Dependabot Python requirements update |
| #247 | `301aea5` | actions/checkout | 7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| #248 | `ff1e82c` | pikepdf | 10.13.0.post1 | Dependabot Python requirements update |
| #249 | `c47afb2` | actions/setup-node | 7.0.0 | `820762786026740c76f36085b0efc47a31fe5020` |

Upstream release-tag references were checked with GitHub's Git refs API; pnpm's annotated tag was peeled through the Git tags API. Each individual action PR changes a workflow SHA without changing `scripts/test_publication_workflow.py::EXPECTED_ACTIONS`, causing `python-38-compatibility` to fail. Grouping all eight updates and the policy expectation produces a meaningful combined gate. The Python 3.8-marked older package pins remain untouched.

**Disposition**: All eight requested updates are included in the S046 candidate. Their bot PRs remain open until the owner merges the combined candidate, then are closed as superseded so no unmerged update is represented as delivered.
