# Kit Anatomy

**Find the authoritative files and generated delivery layers in a BrandBuilder kit.** A kit is a versioned package: its own `brand.json`, `enforcement/bundle.json`, and `manifest.json` tell a consumer which identity and compiler produced it. Use the delivered inventory rather than assuming a sibling kit has identical optional assets.

## The delivery layers

| Layer | Purpose | Where to start |
| --- | --- | --- |
| Canon | Shared constraints and version domains | `enforcement/consumer-contract.json`, `enforcement/interface-canon.json` |
| Identity | Approved brand source and use rules | `brand.json`, `README.md`, `logos/` |
| Bindings | Platform-ready tokens, assets, and adapters | `tokens/`, `nextjs/`, `web/`, `native/`, `icons/` |
| Enforcement | Exact paths, checks, and recovery | `enforcement/`, `VERIFY.md`, `manifest.json` |
| Proof | Inspectable measurements and examples | `qc/`, `specimens/`, `guidelines/`, `conformance/` |

Do not replace a declared token with an arbitrary platform default. Read the exact generated binding for the target platform and run its named verifier.

## Primary files and directories

| Path | What it supplies |
| --- | --- |
| `SKILL.md` | Consume-mode instructions and portable skill metadata. |
| `README.md` | Brand-specific orientation and integration entry points. |
| `brand.json` | Affiliation, approved inputs, logo source mode, palette choices, typography, roles, and constrained decisions. |
| `manifest.json` | Exact packaged file inventory, byte lengths, and SHA-256 digests. |
| `VERIFY.md` | Generated measurements, checks, and explicit capability skips. |
| `NOTES.md` | Build and migration notes relevant to this delivery. |
| `styles.css`, `tokens/`, `components/` | Generated vanilla styles, token JSON/CSS, and component examples. |
| `nextjs/` | Next.js and Tailwind entry points, local font wiring, app icons, and shadcn registry items. |
| `web/`, `native/` | Renderer-neutral and platform-specific adapter contracts and support matrices. |
| `enforcement/` | Bundle identity, consumer contract, implementation guidance, migration impact, schemas, local recovery distribution, and generated checks. |
| `logos/`, `icons/`, `favicons/` | Approved mark outputs, categorized application icons, and compatibility favicon aliases. |
| `fonts/`, `specimens/` | Bundled faces and licenses, plus typographic specimen output. |
| `guidelines/`, `brand-guide.pdf` | Portable HTML and printable guidance projected from the generated kit. |
| `ui_kits/`, `conformance/` | Interface examples and inspectable browser/reference evidence. |
| `qc/`, `build/` | Measured proof, capability records, and build-only sources or render intermediates. |

The file list is a navigation guide. `manifest.json` is the authority for exact delivered bytes. A conditional capability or approved custom asset can add files; its absence is explained by the corresponding support or capability record.

## Source, generated output, and recovery

Authoritative brand decisions live in source `brand.json`, approved assets, and, for a newly constructed mark, its approved `build/mk_paths.py`. An authoritative supplied mark binds exact Full and Reduced source inputs and forbids `mk_paths.py`. Imported or legacy constructed geometry remains byte-identical. See `06-logo-protocol.md` and `08-glyph-construction.md` before changing any mark.

`tokens/`, `components/`, `nextjs/`, the platform adapters, and the guides are generated projections. Change the owning source or `skill/templates/`, rebuild, and verify instead of patching one projection. `enforcement/consumer-contract.json` states exact paths, version relationships, checks, and an offline recovery distribution; `enforcement/IMPLEMENTATION.md` explains how to consume them.

### Portable skill entry

`SKILL.md` frontmatter uses the portable keys `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. A `user-invocable` key is outside this contract. The repository-vendored portable archive starts at `AGENTS.md` instead of `SKILL.md`.

### Platform bindings

`nextjs/globals.css` and `tokens/` project the same source colors and spacing into different consumption contexts. Use the generated `nextjs/registry/registry.json` catalog and direct item endpoints for installable shadcn resources. Local bundled fonts remain a separate setup step; they are not a registry font item. `web/support-matrix.json` and `native/egui/support-matrix.json` identify which adapter behavior is delivered and which host validation remains local.

### Assets and accessibility

`icons/` groups web and native integration suites with manifests and local instructions. `favicons/` contains byte-identical compatibility aliases for web icons. Approved optional custom assets are published only when their source declaration permits publication; use the generated asset inventory rather than assuming every source asset is public.

`VERIFY.md` and the kit verifiers report measured contrast, geometry, and other declared gates. A recorded capability skip names the missing optional tool. It never waives the WCAG 2.1 AA floor or a failed mandatory check. PDF and PNG byte identity is not a correctness gate; check measured behavior and declared conformance instead.
