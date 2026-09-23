# Release Candidate Contract

The candidate includes the compatible updates proposed by #242-#249 and keeps immutable action SHAs synchronized with upstream release versions and the workflow regression allowlist. Every existing verification gate remains active. The PR is complete only when required CI checks are green and all actionable reviews are addressed. The owner performs final merge; the release tag must point to that exact merged main commit. CI, not a local build, publishes certified archives and checksums.
