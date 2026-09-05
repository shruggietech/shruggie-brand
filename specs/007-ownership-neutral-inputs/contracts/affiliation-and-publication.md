# Contract: Affiliation and Publication

## Source

Every brand definition contains an explicit `affiliation` object. Missing values have no compatibility fallback.

```json
{
  "affiliation": {
    "ownership": "third-party",
    "showcase": "public",
    "parent": null,
    "inheritance": "independent",
    "endorsement": "none",
    "service_credit": "brand-system-by-shruggietech"
  },
  "semantic_colors": {
    "emphasis": "#8B5CF6",
    "action": "#6D28D9"
  }
}
```

## Valid combinations

| Ownership | Parent | Inheritance | Endorsement | Service credit | Meaning |
| --- | --- | --- | --- | --- | --- |
| `shruggietech-owned` | `ShruggieTech` | `shruggietech-house` | `shruggietech-project` | `none` | Owned child with the fixed project endorsement |
| `shruggietech-owned` | null | `shruggietech-house` | `none` | `none` | ShruggieTech parent identity |
| `third-party` | null | `independent` or `shruggietech-house` | `none` | `none` | Client identity with no public ShruggieTech credit |
| `third-party` | null | `independent` or `shruggietech-house` | `none` | `brand-system-by-shruggietech` | Client identity with the fixed neutral service credit |

`showcase` is independently `public` or `private` for every valid row.

`shruggietech-house` explicitly adopts the house semantic orange pair. `independent` requires explicit `semantic_colors.emphasis` and `semantic_colors.action` values and excludes house orange from generated brand tokens and framework bindings.

## Output

- `shruggietech-project` emits exactly `A ShruggieTech project`.
- `brand-system-by-shruggietech` emits exactly `Brand system by ShruggieTech`.
- `none` emits no affiliation line.
- Manifests and registries use null or absent parentage for third-party work.
- Generated prose may document prohibited phrases as examples, but deliverable output for a third-party fixture must contain no owned-project claim.
- Site preparation publishes only explicit `public` records and removes stale public output when a source becomes private.

## Failure

Missing fields, unknown values, two simultaneous claims, third-party parentage, owned service credit, parent self-endorsement, unsupported parentage, or independent inheritance without complete semantic colors all stop before generator output.
