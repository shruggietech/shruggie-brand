# Data Model

`brand.custom_assets` is an optional array of distinct records. Each record has `id`, `title`, `description`, `role`, `source` (`path`, `format`, `sha256`), `provenance` (`kind`, `owner`, `detail`), `approval` (`status`, `publication_eligible`), `transformations` (allowed operations), `usage` (`use`, `avoid`), `accessibility` (`alt`, `legibility`, `text_overlay`, `reduced_motion`), `credit` (`attribution`, `license`), and `preview` (`well`, `fit`). Empty or absent means no expression output.

The eligible set is records with `approval.status == approved` and `approval.publication_eligible == true`, after full validation. The generator preserves declared ordering. `id` is stable and unique; `source.path` is unique within the collection. Delivery copies preserve source bytes. An expression never changes `logo` roles or canonical identity records.
