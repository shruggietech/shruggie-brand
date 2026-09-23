# ShruggieTech Brand System

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="brands/shruggietech/assets/logo-darkbg.png">
  <source media="(prefers-color-scheme: light)" srcset="brands/shruggietech/assets/logo-lightbg.png">
  <img src="brands/shruggietech/assets/logo-lightbg.png" alt="ShruggieTech logo" width="500">
</picture>

[![Build status](https://github.com/shruggietech/shruggie-brand/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/shruggietech/shruggie-brand/actions/workflows/build.yml) [![Latest official release](https://img.shields.io/github/v/release/shruggietech/shruggie-brand?label=release)](https://github.com/shruggietech/shruggie-brand/releases/latest) [![Code license: Apache 2.0](https://img.shields.io/badge/code-Apache--2.0-blue)](LICENSE)

This repository contains the ShruggieTech brand system: the `shruggie-brandbuilder` skill, source definitions for eight production brand kits, the pipeline that rebuilds and verifies them, and the release-backed [brand site](https://brand.shruggie.tech/). Brand assets and guidelines are available on the site; source and build tooling live here.

## Get the current release

Open the [latest official release](https://github.com/shruggietech/shruggie-brand/releases/latest) and choose the asset for your workflow:

| Use | Release asset |
| --- | --- |
| Claude Customize upload | The `shruggie-brandbuilder` `.skill` file |
| Codex or repository vendoring | The `shruggie-brandbuilder` portable `.zip`, starting with its `AGENTS.md` |
| One released brand kit | A brand-named `.zip` file listed in that release |

The release includes `SHA256SUMS` for exact-download verification. A showcased brand may not have an archive in every release; the release asset list is authoritative. Source on `main` can be newer than the latest published release, so use the release page rather than a source version number to identify downloadable assets.

## Brand kits

- [ShruggieTech](https://brand.shruggie.tech/shruggietech/guidelines/)
- [Fragcap](https://brand.shruggie.tech/fragcap/guidelines/)
- [Go Schedule](https://brand.shruggie.tech/go-schedule/guidelines/)
- [Glitchpad](https://brand.shruggie.tech/glitchpad/guidelines/)
- [Covarity](https://brand.shruggie.tech/covarity/guidelines/)
- [ESO Weave](https://brand.shruggie.tech/eso-weave/guidelines/)
- [Cueson](https://brand.shruggie.tech/cueson/guidelines/)
- [I Heart PR Tours](https://brand.shruggie.tech/i-heart-pr-tours/guidelines/)

Each brand page links to a generated multi-page guideline portal with focused voice, logo, color, typography, component, asset, and platform-integration topics. The downloads page also carries a standalone HTML guideline for offline use.

## Build

Install Python 3.8 or newer and the dependencies documented in [CONTRIBUTING.md](CONTRIBUTING.md), then build every production kit:

```powershell
python scripts/build_all.py
```

Build one kit by slug:

```powershell
python scripts/build_all.py covarity
```

Generated output is written to `dist/` and is intentionally ignored by Git.

Every canonical archive is named `<brand-slug>-brand-<brand-version>-bb<brandbuilder-version>.zip`. Production Pages advances only with an exact formal release; verified `main` output remains a reviewable CI candidate.

## Add a brand

Read the [variance contract](skill/references/00-variance-contract.md), then add source files only under `brands/<slug>/`. Register the kit in the site and build script, then run the complete validation. New production accents must satisfy the system hue-separation rule and every text-bearing color must clear WCAG 2.1 AA. Tests that require synthetic brand data must create it in a temporary directory.

## Licensing

Code, templates, reference documentation, and site source are licensed under [Apache License 2.0](LICENSE). Attribution is in [NOTICE](NOTICE). Names, wordmarks, logos, endorsement lockups, and logo path geometry remain reserved as described in [LICENSE-BRAND.md](LICENSE-BRAND.md). Bundled fonts retain the SIL Open Font License 1.1 terms included with the font sources.
