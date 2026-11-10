# S075 Pages Deployment Blocker

## Verified Source and Release

[PR #354](https://github.com/shruggietech/shruggie-brand/pull/354) was squash merged at `47b7618f582659c01d39d4b5da10f5f1df220ed8`. Its source tree matches reviewed head `477519e122764b51c152c8cb881c85b86c2eb5c4` exactly: `648b30c83ef4a9cacc52752a3928dbd96f9d3ca3`. Annotated v3.1.2 tag object `f59dacb5e2dbb1acca948a9c18d38575f1d786ee` points to that merged commit.

The [official v3.1.2 release](https://github.com/shruggietech/shruggie-brand/releases/tag/v3.1.2) was published on 2026-11-10 and is public, stable and latest. All thirteen downloaded assets match GitHub SHA-256 metadata; the twelve distributions match SHA256SUMS. Exact-release archives and generated release notes verify against the tagged revision. No local archive was uploaded or release asset replaced.

## Deployment Attempts (Chronological)

All attempts used the same exact verified Pages artifact, ID `13740933879`, from [tag run 42764281217](https://github.com/shruggietech/shruggie-brand/actions/runs/42764281217). All prerequisite verification, build, release-preflight and publish-release jobs passed. The overall tag run failed only at Pages deployment.

| Attempt | Job | Observed server state | Result |
| --- | --- | --- | --- |
| 1 | [129674675968](https://github.com/shruggietech/shruggie-brand/actions/runs/42764281217/job/129674675968) | syncing_files | Ten-minute timeout; action canceled deployment |
| 2 | [129678855803](https://github.com/shruggietech/shruggie-brand/actions/runs/42764281217/job/129678855803) | finished_file_sync, without succeed | Ten-minute timeout; action canceled deployment |
| 3 | [129683004740](https://github.com/shruggietech/shruggie-brand/actions/runs/42764281217/job/129683004740) | Empty status, without succeed | Ten-minute timeout; action canceled deployment |

The pinned official action correctly waits for explicit deployment success and caps the wait at ten minutes. No success check, timeout, publication gate or security test was weakened. No fourth immediate retry or destructive Pages/domain reset was attempted.

## Artifact and Public-State Checks

- The downloaded Pages ZIP matches its published artifact digest `eea4200fb732f185a7f4abd8e314c32fa836106deec3efa47d4401b7599bddca`. It contains one artifact.tar with 4,308 regular files totaling 331,409,561 bytes, no hard/symbolic links or unusual file types, and no absolute/parent-traversal member paths.
- Its documentation record reports release v3.1.2 and the exact tagged revision. Its homepage and DanceWithMe865 guide PDF contain the exact approved sentence. These are artifact checks, not live-site acceptance.
- The canonical public documentation record still reports release v3.1.1 at `65af667461798738b0cf381b7c8bc4487afd853a` after the third attempt. A cache-busted request returns the same revision with Cloudflare DYNAMIC/age 0; a direct GitHub Pages origin request with full hostname/TLS validation also returns that old revision.
- Current edge TLS and direct-origin TLS validate. GitHub's certificate-renewal metadata separately reports bad_authz, while the serving origin certificate remains valid through 2026-12-02. Its relationship to the deployment stall is unproven. No DNS, custom-domain or TLS settings were changed.

## Exact Remaining Work

1. Obtain a successful GitHub Pages activation of the verified v3.1.2 artifact. The immediate supported recovery is retrying only the failed deploy-pages job after the external deployment condition changes. Do not recreate, overwrite or retag the already published release.
2. Verify public docs/publication.json reports release v3.1.2 and source revision `47b7618f582659c01d39d4b5da10f5f1df220ed8`.
3. Run the prepared direct HTTP/archive/PDF checks and eighteen live browser cases (desktop/mobile, both themes, 320px reflow, doubled description text and accessibility). Inspect the released cover and portfolio screenshots. Then close #328 and #353 with evidence.
4. Keep #352 open and follow [cloudflare.md](cloudflare.md) independently when DNS/Single Redirect permissions become available.

The Pages artifact expires at 2026-11-11 06:37:04 UTC (2026-11-11 01:37:04 America/New_York). If it expires first, recover through a workflow that rebuilds and verifies the exact immutable tag and preserves the existing official release; do not substitute a hand-built archive or blindly rerun publication against an existing release. Detailed downloaded artifacts, logs and prepared live verifiers are ignored under dist/private/s075/.

## 2026-11-10 Recovery Continuation

The owner authorized investigation, deployment recovery, live acceptance and closure of #328/#353, while retaining #352 as open. Source artifacts and current origin checks exclude an obvious malformed TAR and a Cloudflare cache-only explanation. The stale original deployment context remains a hypothesis to test with the same payload and a fresh main controller. No timeout or explicit-success check is weakened.

An idempotent Pages configuration PUT failed when including https_enforced=true because GitHub reports certificate authorization bad_authz. A subsequent PUT of only the unchanged cname/build_type unexpectedly reset https_enforced to false. This is an observed API side effect and an outstanding regression. The documented remove/re-add procedure restored the same hostname immediately but did not clear bad_authz. Public HTTP still redirects to HTTPS and both edge and origin TLS validate; these observations do not establish restoration of the GitHub flag. No Cloudflare DNS/rule change was made. Further blind hostname resets are not justified.

The guarded helper successfully qualified original run 42764281217, downloaded both original artifacts, checked their GitHub digests, exported the immutable tagged contracts, validated official release distributions/notes and documentation, and verified hosted release ZIP identity. Unchanged artifact.tar SHA-256 is `6bcf0f5a7b0e958a6717ff3bc071b5ea80ab3f93e55524c35fd9385aa7eb4879`, with 4,308 regular files and 331,409,561 content bytes. The controller at this local rehearsal was 5e92a3e585a548be551906f02f2cde195b55b007; it does not replace the content revision 47b7618f582659c01d39d4b5da10f5f1df220ed8.

The github-pages environment already permits main and v* tags. The recovery implementation adds no protection exception. Main-only manual preparation uses read-only repository/actions permissions; only the official deployment action receives Pages/id-token permissions. Recovery cannot republish release assets or cancel main verification. Twelve recovery tests and thirty publication-workflow tests pass locally. Successful new activation, HTTPS flag restoration and full live acceptance remain pending.
