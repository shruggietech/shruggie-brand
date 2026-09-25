# Research: shadcn Registry Delivery

## Contract observed on 2026-09-25

- The [official catalog guide](https://ui.shadcn.com/docs/registry/registry-json) says catalog items implement the registry-item schema. Its source/build use case expects real file paths, while this project's static `/r/registry.json` is a discovery endpoint and direct `/r/{name}.json` endpoints provide install payloads.
- The [official item schema](https://ui.shadcn.com/schema/registry-item.json) allows a `registry:theme` item to carry `cssVars` without files. UI files require path/type and useful content for this project's delivery claim.
- The same schema permits only `google` as a `registry:font` provider and requires `font.import`. The current generated `provider: local` payload is invalid. Switching to Google would violate the bundled local-font contract; remove this advertised item and document manual local setup.
- `npm view shadcn version` returned `4.21.0` on 2026-09-25. Pin consumer integration to that version and preserve schema snapshots with provenance for reproducible validation. Do not use `@latest` in supported commands.
- The saved official schema snapshots are `skill/references/shadcn/registry.json` (SHA-256 `e716ebe595bbc189db2627cb75f0484cd765a09eb397a89b1f1c49074220d4bb`) and `registry-item.json` (SHA-256 `cdf0fba75a26ebf594018264eff2d55407ec14deb3071d0fce0e2b20848e5d44`). Both came from `https://ui.shadcn.com/schema/` on 2026-09-25, use JSON Schema draft 7, and are validated offline with `jsonschema==4.17.3`.
- `skill/references/shadcn/LICENSE.md` preserves the upstream [MIT license](https://github.com/shadcn-ui/ui/blob/main/LICENSE.md) alongside those schema snapshots.

## Current producer and publication path

- `skill/templates/gen_nextjs.py` writes full direct theme and component payloads, then creates catalog stubs independently. The font payload claims unsupported CLI behavior.
- `scripts/prepare_site.py::validate_registry` currently checks schema URL strings and names/types only; `scripts/test_prepare_site.py` accepts payloads with no implementation. Site preparation copies `nextjs/registry` to public routes after this check.
- `scripts/prepare_site.py::install_registry_theme` extracts CSS variables directly for the parent site. This proves the parent site can consume tokens, not that shadcn can install a registry item.

## Decision

Create one item collection in the generator, serialize each direct payload and derive catalog entries from those same objects. Validate both JSON Schemas and project semantics offline using pinned schema snapshots. Add a pinned shadcn CLI consumer test with an ephemeral local HTTP server, temporary Next.js/Tailwind context, and no production-repository mutation. Keep font binaries and `fonts.ts` as a manual bundle step. A future compatible font registry contract can replace that step without falsely describing current support.

## Follow-on boundary

Issue #269 examines every generated artifact family and component semantics. S052 records registry evidence and negative tests but does not claim that wider audit is complete.
