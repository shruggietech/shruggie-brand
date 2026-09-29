# S069 Research and Decisions

## Current state

At kickoff, `main` is `14aa915fd1da88aaada5e138026622248f7b3261`, S068 PR #307 is merged, issues #298 and #299 are Done, and there are no open PRs or issues. The latest published release is `v2.8.0`; `v3.0.0` is neither tagged nor released. Source metadata already declares BrandBuilder 3.0.0 and Brand Canon 2.0.0. S067 is in the 3.0.0 changelog section; S068 remains in Unreleased even though its source is now merged. The S068 verification document still describes external gates as pending.

The release contract lists eight `RELEASE_AUTHORIZED_BRANDS`, while `scripts/build_all.py`, site publication, and the CI artifact inventory cover eleven production brands. The formal release will preserve the existing eight archive boundary. DanceWithMe865, I Heart PR Tours, and Scruggs Tire & Alignment remain verified public hosted kits without GitHub release assets. This is the documented current contract, not a judgment about a client's right to use its own assets.

## Decision: publish the existing 3.0.0 candidate

`3.0.0` is already the source version and has no public tag. Moving S068 release-facing notes into the 3.0.0 section and updating its migration and release-impact text makes that candidate accurately describe the final bytes without making a new, unused 3.0.1 package identity. A patch bump would be necessary after 3.0.0 publication, not before it.

## Decision: preserve the release asset boundary

The viable options were to retain eight release-authorized archives or expand the release allowlist to all eleven hosted brands. The current contract and tests explicitly distinguish formal release assets from hosted client packages. Expansion would change release publication semantics for three client brands and is not required to deliver the current formal release. Retaining eight preserves the established invariant and still publishes all eleven verified guides and site downloads. The release notes must make the distinction visible.

## Publication sequence

Complete release prep on a feature branch, pass local contract and full GitHub PR checks, resolve two Codex review rounds and any security findings, then merge the PR. Verify the merged source and its exact candidate, create `v3.0.0` on that commit, and allow the tag workflow to run `release-preflight`, `publish-release`, and `deploy-pages`. Check uploaded file names and checksum bytes against the CI candidate, then check the live site's exact version link and source-bound guide content. If a workflow job fails, inspect the exact failed stage and resume only after comparing the existing tag and release inventory. No replacement from a later `main` revision is acceptable.

## Risks

- The GitHub release publish job uses `gh release create`; a rerun after partial upload may find an existing draft or release. Inspect tag, assets, and checksums before any manual recovery.
- `main` or new issues may change during review. Reassess release blockers before tagging; do not advance the tag target silently.
- The full build is long. Batch release-note and metadata corrections before the PR run; avoid starting a redundant full workflow for each text adjustment.
