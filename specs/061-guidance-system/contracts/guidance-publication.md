# Guidance publication contract

## References

`/docs/references/` is a canonical manual page and search result. A local source citation `references.md#ref-id` is converted only for hosted MDX to `/docs/references/#ref-id`. The packaged skill retains its relative link. IDs are lower-case generated anchors from unique `REF-*` headings. The local validator checks IDs and targets without requiring network access.

## Public facts

`/{brand}/facts/documentation.json` is a static copy of the verified kit's `enforcement/documentation-facts.json`. Its `documentation_contract_version` declares the schema family, and its `bundle` and `versions` fields distinguish the current published projection from pinned download bytes. A guideline link to this path must resolve in the site export and the content must compare byte for byte with the kit fact source.

## Reader surface

Each topic states its purpose, effective rule, when or how to apply it, and authority/action. Empty optional fields use truthful explanatory language. Interface overrides name the default and effective value only when those values exist in generated facts. Version and binding names are human labels with exact technical values preserved. Current hosted guidance, portable HTML, PDF, and offline implementation guidance must not claim a different authority.
