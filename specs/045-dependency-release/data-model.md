# Data Model: Dependency and Release Intake

| Record | Fields | Validation and state |
| --- | --- | --- |
| Dependabot intake | PR number, source head, group, direct updates, CI status, disposition | One row per open kickoff PR; disposition remains pending until the combined slice merges. |
| Combined dependency candidate | Manifest versions, lockfile resolutions, frozen-install result | Every direct update from both intake rows must be present and install reproducibly. |
| Browser client | Python or Node owner, Playwright version, required Chromium revision, launch result | Both clients must launch before release archives are certified. |
| Release candidate | Version, merged source revision, notes, archive list, checksums, main-ancestry status | Candidate becomes publishable only after merge and successful preflight. |
| Review state | Comment threads, bot reactions, CI conclusions, extra Codex request count | All actionable threads resolved, all required checks green, extra request count at most one. |

No user data schema, persistent database, or migration is introduced.
