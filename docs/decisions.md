# Decisions

## Conventions inherited from sibling projects

The audit was performed on 2026-09-03 against `A:\Code\fragcap`, `A:\Code\go-schedule`, and `A:\Code\glitchpad`, plus their live GitHub repositories where those repositories existed.

### Repository owner

Go Schedule and Glitchpad are owned by the `ShruggieTech` organization. Fragcap remains under `h8rt3rmin8r`, and `ShruggieTech/fragcap` does not exist. The work order's singular "same owner" premise is therefore false. This repository uses `ShruggieTech`, following the two newer repositories and the instruction to prefer Glitchpad where siblings disagree.

### Source control and pull requests

- Go Schedule and Glitchpad use `codex/NNN-slug` feature branches, Spec Kit directories with matching sequential numbers, and squash-oriented pull request history. This repository inherits that pattern.
- Conventional Commit subjects are preferred. Recent sibling squash subjects also use `SNNN: summary (#PR)`, so a slice number is included whenever one exists.
- `main` is governed by the ShruggieTech organization ruleset named `default-branch PR gate`. It blocks deletion and non-fast-forward updates, requires a pull request with zero mandatory approvals, and permits squash or rebase. The work order additionally requires the `build` status check here.
- The classic branch-protection endpoint returns 404 for both newer siblings because the organization ruleset is the effective control. This repository will use a repository ruleset to add the required check rather than attempting to replace the inherited organization rule.

### Project management

- Glitchpad and Fragcap have no repository-linked Projects v2 board. The organization project `Iterative Development` contains only Go Schedule and Shruggie Graph items, and its Go Schedule coverage is stale after issue 42. A Project board is therefore not created for this repository.
- The reusable organization project schema is recorded for reference: Status (`Backlog`, `Ready`, `In progress`, `In review`, `Done`), Size (`XS`, `S`, `M`, `L`, `XL`), numeric Estimate, 14-day Iteration, and text Slice. Its workflow internals are not available through GitHub's public GraphQL schema.
- Work is tracked with GitHub Issues, one milestone per work-order phase, and Spec Kit artifacts. This follows the reliable planning surfaces used by all three siblings.

### Labels

The base taxonomy follows the newer Go Schedule and Glitchpad repositories: `area:` labels, `priority: P0` through `priority: P3`, `effort: XS` through `effort: XL`, and the standard `bug`, `documentation`, `enhancement`, `security`, and `task` types. Repository-specific labels are `skill`, `kit:shruggietech`, `kit:fragcap`, `kit:go-schedule`, `kit:glitchpad`, `kit:covarity`, `site`, `ci`, `canon`, and `migration`. Broken sibling references to nonexistent `triage` and Dependabot labels are not copied.

### Community, security, and ownership

- Contributor Covenant 2.1 is inherited from Go Schedule and Glitchpad.
- `CODEOWNERS` uses `* @h8rt3rmin8r`, following Glitchpad.
- Private vulnerability reporting with `info@shruggie.tech` fallback follows Go Schedule. Glitchpad's private-reporting link is currently disabled, so its broken state is not copied.

### Dependencies, releases, and changelog

- Dependabot covers GitHub Actions and the active package ecosystems. Go Schedule's grouped update convention is used where packages share a runtime.
- Keep a Changelog and Semantic Versioning are common to all three siblings. Tags use annotated `vMAJOR.MINOR.PATCH`, following the newer Go Schedule release process. Glitchpad has no tags yet.
- Releases are built from tags in CI. Release notes state skill version, canon version, and migration requirements. Hand-built archives are never release inputs.

### Spec Kit

Glitchpad is the newest complete reference: committed Spec Kit, Codex integration, PowerShell scripts, sequential feature numbering, and skills mode. This repository was initialized with official Spec Kit 1.0.4 using those choices. Glitchpad carries 1.0.1, while the pre-existing local CLI was 0.13.4. The CLI was upgraded from the official `github/spec-kit` v1.0.4 tag before initialization. `.specify/feature.json` remains ignored machine-local state.

## Ground-truth deviations from the work order

- The authoritative skill tree contains 45 files, not 41.
- The authoritative skill and canon are already version 1.1.1, not 1.1.0. Version 1.1.1 contains the accessibility floor described later in the work order, so the provenance change advances both to 1.1.2.
- Section 11 calls the provenance release 1.1.1, contradicting section 6.2 and the actual 1.1.1 source. Section 6.2 and the source tree take precedence.
- No Cloudflare CLI or token environment variable is present. The authenticated Cloudflare API connector has access to the ShruggieTech account and will be used as the permitted REST API path.
- The work order requires Phase 1 branch protection to name a `build` check that is only created in Phase 5. The local scaffold, skill import, and build workflow must therefore exist before that final Phase 1 acceptance check can be configured.
- The canonical Covarity font binaries are byte-identical to Glitchpad, Go Schedule, and Fragcap. Their `README.md` or `fonts.css` text differs in two older kits. ShruggieTech predates the shared font bundle and has no comparable font tree. The Covarity copy remains canonical as directed.
- The runtime `rsvg-convert.js` comparison will be recorded after its two source paths are inspected during toolchain migration.

## Public repository assumption

The repository is public because the required GitHub Pages site must be available without relying on a private-repository Pages entitlement. Changing the repository to private requires choosing and configuring a different public site host.

