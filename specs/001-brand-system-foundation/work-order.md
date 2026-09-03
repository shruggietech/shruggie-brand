# Public implementation directive

The original handoff document was supplied privately and contained workstation paths, staging inventory, and operational identifiers. Those details are not required to understand, build, or govern this public repository, so they are intentionally excluded here.

The complete public translation is maintained as phase issues. Each issue contains its objective, deliverables, acceptance criteria, current evidence, and known follow-up work:

| Phase | Public tracker |
| --- | --- |
| Repository scaffold and governance | [#6](https://github.com/shruggietech/shruggie-brand/issues/6) |
| Brandbuilder skill and shared fonts | [#7](https://github.com/shruggietech/shruggie-brand/issues/7) |
| Five production-kit migrations | [#8](https://github.com/shruggietech/shruggie-brand/issues/8) |
| Synthetic end-to-end fixture | [#9](https://github.com/shruggietech/shruggie-brand/issues/9) |
| Build, Pages, and release automation | [#10](https://github.com/shruggietech/shruggie-brand/issues/10) |
| Static documentation and registry site | [#11](https://github.com/shruggietech/shruggie-brand/issues/11) |
| DNS, custom domain, and live acceptance | [#12](https://github.com/shruggietech/shruggie-brand/issues/12) |
| README, changelog, and release notes | [#13](https://github.com/shruggietech/shruggie-brand/issues/13) |
| Clean-environment verification | [#14](https://github.com/shruggietech/shruggie-brand/issues/14) |
| Guarded staging disposition | [#15](https://github.com/shruggietech/shruggie-brand/issues/15) |

Post-merge review findings are tracked separately in [#17 through #31](https://github.com/shruggietech/shruggie-brand/issues?q=is%3Aissue%20milestone%3A%2A). They are release blockers where linked from the phase issues.

## Definition of done

1. A generator change rebuilds and verifies every production kit and the synthetic fixture.
2. The deployed Covarity registry theme installs through the current shadcn CLI.
3. Version tags publish two skill bundles and five licensed production-kit archives.
4. Every private staging item has a documented, recoverable disposition.

The implementation specification, plan, and task ledger in this directory are the repository-local source of truth. Private machine inventory remains in the operator-held directive and backup archive.
