# Data Model: v1.1.2 Release and Publication Certification

## Release Metadata

| Field | Source | Validation |
| --- | --- | --- |
| `tag_version` | S004 invocation and Git tag | Semantic version `1.1.2`; tag is `v1.1.2` |
| `skill_version` | `skill/SKILL.md` metadata | Equals `tag_version` |
| `canon_version` | `skill/SKILL.md` and `skill/references/01-canon.json` | Both values equal `tag_version` |
| `migration_required` | Release contract constant for 1.1.2 | Explicit yes plus rebuild guidance |
| `release_changes` | Exact `CHANGELOG.md` version section | Section exists once and contains no placeholder |
| `release_notes` | Generated metadata header plus release changes | Reproducible from tagged source |

## Release Asset

| Field | Meaning | Validation |
| --- | --- | --- |
| `filename` | Published asset name | Member of the exact expected seven-name set |
| `kind` | Claude skill, portable skill, or production kit | Determines archive rules |
| `declared_version` | Skill release version or brand version | Matches filename and embedded metadata |
| `archive_entries` | Normalized ZIP member names | No absolute or parent-traversal entries; required roots present |
| `licenses` | Root licensing triplet | `LICENSE`, `NOTICE`, and `LICENSE-BRAND.md` all present |
| `manifest_checksums` | Recorded production-kit hashes | Every recorded path exists and matches byte count and SHA-256 |

## Review Round

| Field | Meaning | Validation |
| --- | --- | --- |
| `round` | 1 or 2 | No third row or trigger exists |
| `trigger` | Automatic PR publication or one explicit comment | Round 2 waits for round 1 completion |
| `signal_url` | Immutable review, reaction, or comment evidence | Present before round completion |
| `findings` | Actionable negative comments | Each has a GitHub issue and disposition |
| `thread_state` | Pending, addressed, resolved | Complete only when no actionable thread remains |

## Publication Evidence

| Field | Meaning | Validation |
| --- | --- | --- |
| `merged_main_sha` | Actual main revision after owner merge | Contains the S004 release-readiness tree |
| `tag_target_sha` | Commit referenced by v1.1.2 | Equals the verified merged main revision |
| `workflow_url` | Tagged Release workflow run | Concludes success |
| `release_url` | Public GitHub release | Tag is v1.1.2 and is neither draft nor prerelease |
| `download_directory` | New temporary inspection directory | Empty before download and outside committed source |
| `verification_result` | Shared release-contract result | Seven assets and release notes pass with zero failures |

## Issue Closure Set

| Parent | Required children | Final milestone |
| --- | --- | --- |
| #10 | #60, #61, #62, #63, #38 | Phase 5, milestone 15 |
| #13 | #71, #72, #73 | Phase 8, milestone 18 |

State transitions are `open -> evidenced -> closed` for children, then parents, then milestones. Failure or partial evidence remains `open` and records the missing proof.
