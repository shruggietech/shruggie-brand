# Publication Contract

## Candidate builds

Pushes to `main`, pull requests, and manual validation may build and retain verified candidate artifacts. They MUST NOT deploy the production Pages environment or claim a formal release identity.

Generated publication metadata carries `status: candidate` for untagged builds and `status: release` only when the build ref is the exact matching version tag. The production gate accepts only `release`.

## Formal release publication

For a `vMAJOR.MINOR.PATCH` tag, publication MUST proceed in this order:

1. Build and verify all production kits, the skill archive, release notes, checksums, and site export from the tagged revision.
2. Validate that the tag, BrandBuilder metadata, changelog boundary, source revision, bundle records, asset names, and exact site destinations agree.
3. Publish the GitHub release from the verified build outputs.
4. Deploy the already verified site artifact to production Pages.

Any failed or skipped prerequisite blocks later publication stages.

## Public destinations

The production site's skill action MUST resolve to the exact release represented by the site. No production source or generated metadata may use `/releases/latest`. Kit actions use the canonical immutable filename from each bundle record.

## Authorization boundary

S043 prepares and verifies publication behavior. It does not create a version tag, publish a GitHub release, or deploy a new production release without separate owner authorization.
