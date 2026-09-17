# Contract: Component Recipe Catalog

The catalog is a closed JSON document validated before adapter generation. Public recipe keys are `AppFrame`, `Button`, `IconButton`, `Toolbar`, `Tabs`, `Menu`, `Dialog`, `Field`, `FormControls`, `ListRow`, `SplitPane`, `Toast`, `StatusBadge`, `Card`, and `EmptyState`. `Field` and `FormControls` jointly implement the issue's core form controls family.

Every recipe contains all required dimensions. Role values use `$role.<interface-role>` references. A recipe cannot contain color syntax, physical lengths, font-family strings, CSS properties, renderer APIs, route definitions, navigation trees, page regions beyond AppFrame responsibilities, or free-form nested child recipes.

The validator resolves every role through Interface Canon, proves each recipe and coverage row appears exactly once, checks required states, enforces the 44 logical-unit control target, and rejects brand overrides outside each recipe's allowlist. AppFrame additionally requires exactly one owner for every shell responsibility in every host profile.

Generated kits receive byte-identical copies of the catalog and schema under `enforcement/` and a resolved adapter copy under `web/`.
