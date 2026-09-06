# Data Model: v1.2.0 Publication and Production Certification

## Publication Record

| Field | Meaning | Validation |
| --- | --- | --- |
| main revision | Owner-merged source revision | Exact 40-character commit ID and clean synchronized main |
| tag | Annotated v1.2.0 tag | Tag object resolves to the main revision |
| workflow | Tag-triggered Release run | Completed successfully for v1.2.0 |
| release | Public GitHub release | Non-draft, non-prerelease, target v1.2.0 |
| notes | Generated release body | Matches repository-generated notes |
| assets | Public asset inventory | Exact seven expected filenames |
| verification | Shared contract result | Seven of seven pass with zero failures |

## Production Record

| Field | Meaning | Validation |
| --- | --- | --- |
| Pages workflow | Merged-main deployment run | Completed successfully for the main revision |
| origin | Public site root | Exactly `https://brand.shruggie.tech` |
| route graph | Generated public route inventory | Every route returns directly and matches metadata |
| resources | Downloads, registries, icons, discovery files | Expected status, content type, and valid non-empty content |
| accessibility | axe-core WCAG result | Zero WCAG 2.1 AA violations |
| responsive matrix | 360 and 1280 pixel checks | Zero horizontal overflow |
| theme matrix | Light and dark representative screenshots | Both themes settle correctly with no material regression |

## Review Round

| Field | Meaning | Validation |
| --- | --- | --- |
| ordinal | Automatic round one or explicit round two | Integer 1 or 2 only |
| signal | Review, comment, or thumbs-up URL | Immutable GitHub URL |
| findings | Actionable negative comments | Each has a linked issue before resolution |
| dispositions | Response and correction result | Every comment answered |
| trigger | Explicit second-round request | Zero or one URL total |
| completion | Round status | No unresolved actionable threads |

## State Transitions

`MERGED_MAIN_VERIFIED -> TAG_PUSHED -> RELEASE_WORKFLOW_SUCCEEDED -> PUBLIC_ASSETS_VERIFIED -> PRODUCTION_VERIFIED -> EVIDENCE_PR_REVIEWED -> OWNER_MERGED`

A failed gate prevents advancement. Issue closure becomes effective only at `OWNER_MERGED` through pull-request closure keywords.
