# Decisions

## Conventions inherited from sibling projects

The audit was performed on 2026-09-03 against local checkouts of Fragcap, Go Schedule, and Glitchpad, plus their live GitHub repositories where those repositories existed.

### Repository owner

Go Schedule and Glitchpad are owned by the `ShruggieTech` organization. Fragcap remains in a personal namespace, and `ShruggieTech/fragcap` does not exist. The work order's singular "same owner" premise is therefore false. This repository uses `ShruggieTech`, following the two newer repositories and the instruction to prefer Glitchpad where siblings disagree.

### Source control and pull requests

- Go Schedule and Glitchpad use `codex/NNN-slug` feature branches, Spec Kit directories with matching sequential numbers, and squash-oriented pull request history. This repository inherits that pattern.
- Conventional Commit subjects are preferred. Recent sibling squash subjects also use `SNNN: summary (#PR)`, so a slice number is included whenever one exists.
- `main` is governed by the ShruggieTech organization ruleset named `default-branch PR gate`. It blocks deletion and non-fast-forward updates, requires a pull request with zero mandatory approvals, and permits squash or rebase. The work order additionally requires the `build` status check here.
- The classic branch-protection endpoint returns 404 for both newer siblings because the organization ruleset is the effective control. This repository will use a repository ruleset to add the required check rather than attempting to replace the inherited organization rule.
- Repository ruleset `required brand build` (ID `22231594`) now requires the `build` context against the latest target branch before `main` can advance.

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
- No Cloudflare CLI or token environment variable is present. The authenticated Cloudflare API connector was used as the permitted REST API path.
- The work order requires Phase 1 branch protection to name a `build` check that is only created in Phase 5. The local scaffold, skill import, and build workflow must therefore exist before that final Phase 1 acceptance check can be configured.
- The canonical Covarity font binaries are byte-identical to Glitchpad, Go Schedule, and Fragcap. Their `README.md` or `fonts.css` text differs in two older kits. ShruggieTech predates the shared font bundle and has no comparable font tree. The Covarity copy remains canonical as directed.
- The runtime `rsvg-convert.js` differs from the authoritative skill copy only in ternary-expression formatting. The skill copy is newer, functionally equivalent, and remains authoritative. The runtime wrapper is not committed.

## Public repository assumption

The repository is public because the required GitHub Pages site must be available without relying on a private-repository Pages entitlement. Changing the repository to private requires choosing and configuring a different public site host.

## Migration and publication decisions

### Authoritative mark preservation

- Fragcap, Go Schedule, and Glitchpad retain imported vector path geometry. Unsupported glyphkit command forms remain visible as warnings and never become silent conversions.
- ShruggieTech has no authoritative vector source in the migration material. Its paid raster artwork is preserved as deterministic alpha/luminance masks inside SVG wrappers. Reconstructing or tracing a replacement would invent geometry and violate the work order's no-redraw rule.
- The generator was extended proportionally to preserve native rectangles, strokes, joins, and raster images. Glyphkit-authored marks continue to receive the stricter path-command gate.

### Fixture identity scope

The synthetic fixture reuses parent green and is declared with `kind: fixture`. It exercises contrast and every artifact gate but is excluded from sibling hue allocation because it is not a product identity. Treating it as a sixth identity would consume scarce hue space for test data and contradict the variance contract.

### Site as a kit consumer

The site stages generated outputs into ignored build directories. Next.js 16 prevents `next/font/local` imports from traversing above the site build root, so `scripts/prepare_site.py` copies the exact canonical WOFF2 bytes from `assets/fonts/` into `site/generated/fonts/` before compilation. No font copy is committed, and the resulting bytes remain identical to the kits.

The same preparation step installs the generated ShruggieTech shadcn registry theme into CSS, imports the parent vanilla token layer, and copies guidelines, registry JSON, PDFs, masters, favicons, and specimens into the static export. Registry files are copied without transformation and verified by hash locally.

### Linux renderer dependencies

The first hosted Ubuntu run proved that installing `librsvg2-bin` and ImageMagick was insufficient for the existing PDF visual gate: `qc_render.py` also invokes Poppler's `pdftoppm`. CI, Pages, and release jobs therefore install `poppler-utils` explicitly. This dependency is now part of the documented pipeline rather than an accidental feature of the Windows workstation.

### DNS publication

The authenticated Cloudflare connector was used in place of the absent CLI. The executed mutation was `POST /zones/{redacted-zone-id}/dns_records` with `{type: CNAME, name: brand, content: shruggietech.github.io, ttl: 1, proxied: false}`. Account, zone, and record identifiers are intentionally omitted from the public repository. The record remains DNS-only because that is the most predictable GitHub Pages TLS configuration.

GitHub Pages was enabled with `gh api --method POST repos/ShruggieTech/shruggie-brand/pages -f build_type=workflow`, then assigned the custom hostname with `gh api --method PUT repos/ShruggieTech/shruggie-brand/pages -f cname=brand.shruggie.tech`. Before the first deployment, GitHub correctly reports HTTPS enforcement as unavailable while the certificate is pending. Public DNS resolves the expected CNAME.

### Downstream accessibility correction

The canonical parent correction does not silently rewrite the live company site. The original `#2BCC73` foreground measured 1.98:1 on `#F8F8F6`; the replacement `#037B40` measures 5.05:1. The required downstream work is tracked in [shruggie-web issue 35](https://github.com/ShruggieTech/shruggie-web/issues/35), with links to the committed CSS provenance.

### Post-merge review and release hold

Codex review on PR #16 arrived after the foundation merge and identified nine actionable defects. They are tracked as issues #17 through #25. Release v1.1.2 was deliberately held before tagging so the published skill and kit archives do not preserve known portability, release-integrity, accessibility, or Windows process defects.

The correction reviews on PR #26 found ten additional defects, tracked as issues #27 through #36. The merge and release remain held while the branch removes stale outputs during capability downgrades, separates ICO verification from SVG raster verification, keeps image-backed core masters and core image QC independent of Pillow, includes Pillow compositing in the raster capability contract, clears stale image and PDF QC evidence, makes the repository's Markdown prose rule enforceable in CI, and executes regression tests on Python 3.8 rather than compiling them without running them.

The fixes distinguish missing capability from broken capability. A lower tier records a named skip and succeeds with the artifacts that tier promises. Once a probe confirms a renderer or full tier, any later export or QC failure is fatal. The Node resvg wrapper is now exercised during probing instead of treated as available because its script file exists.

The generated manual Next.js binding uses bundled files through `next/font/local`. The current shadcn `registry:font` schema supports only the Google provider, so `fonts.json` remains a standards-compliant registry item while its install note directs deterministic and offline consumers to the local binding. This limitation is documented by the upstream [registry item schema](https://ui.shadcn.com/docs/registry/registry-item-json).

### Public planning hygiene

The private work directive was originally copied into the public Spec Kit tree. It included workstation paths and operational resource identifiers that are not needed by contributors. The public copy has been replaced with a sanitized phase index, the full requirements are translated into issues #6 through #15, and the operator-held directive remains available outside the repository. This is an intentional deviation from preserving the attachment verbatim.

### S003 capability and fixture reconciliation

The Windows capability probe previously omitted ImageMagick's `magick` executable from its SVG-renderer decision even though raster generation already used it. Image QC also lacked the same fallback. S003 aligns the probe and both consumers around the implemented ImageMagick 7 path. The probe separately validates any `convert` executable as ImageMagick before using it for ICO capability, and ICO generation reuses that recorded result instead of rediscovering an executable from `PATH`. This prevents the unrelated Windows filesystem conversion utility from producing a false positive or overriding the Pillow fallback. ImageMagick 6 `convert` is not advertised as an SVG renderer because the generation and QC paths do not implement that fallback.

Manual narrow-screen inspection exposed two fixture defects that the earlier source scan did not cover. The Glitchpad fixture referenced nonexistent `gp` tokens and classes instead of its generated `gl` namespace, and the ShruggieTech header retained a nested interactive contact control plus an overflowing mobile navigation row. S003 corrects those consumers and adds regression coverage without changing any authoritative identity geometry.
