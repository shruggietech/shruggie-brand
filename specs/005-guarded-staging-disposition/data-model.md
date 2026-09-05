# Data Model: Guarded Staging Disposition

## Disposition Entry

| Field | Meaning | Public |
| --- | --- | --- |
| Entry ID | Stable sanitized identifier for one top-level staging item | Yes |
| Classification | Authoritative copy, superseded copy, regenerable runtime, provenance source, history, unrelated research, or private material | Yes |
| Source facts | Item type, file count, byte count, and private resolved path | Counts only |
| Preservation proof | Repository source, provenance record, release asset, archive match, cold-storage copy, or reproducibility proof | Sanitized summary |
| Destination class | Repository, published release, governed cold storage, or recoverable deletion staging | Yes |
| Destination path | Exact private resolved destination | No |
| Recoverability | Archive and destination recovery methods | Category only |
| Final state | Retained, moved, verified, blocked, or deliberately retained | Yes |

### Validation rules

- Every top-level source has exactly one entry.
- Every entry reaches `verified` before the source workspace can be declared empty.
- A superseded or regenerable classification requires proof outside the source workspace.
- A private path or provider identifier makes a public entry invalid.
- A destination collision blocks the move rather than overwriting content.

## Archive Verification Record

| Field | Meaning |
| --- | --- |
| Archive identity | Private archive path and SHA-256 |
| Compared at | Timestamp before the first staging move |
| Archived count | Files treated as archive members |
| Live count | Files present at comparison time |
| Exact matches | Path, size, and SHA-256 matches |
| Transient exceptions | Live-only files proven to be regenerated caches |
| Mismatches | Missing, extra, size-different, or hash-different authoritative files |
| Gate result | Pass only when mismatches equal zero |

## Move Record

| Field | Meaning |
| --- | --- |
| Disposition entry | Parent entry identifier |
| Source | Exact resolved private source |
| Destination | Exact resolved private destination |
| Approved root | Cold-storage or recoverable-deletion root |
| Collision check | Destination absent before move |
| Pre-move fingerprint | File count, byte count, and aggregate evidence |
| Post-move fingerprint | Matching destination evidence |
| Source terminal state | Absent after move |

## Review Round

| Field | Meaning |
| --- | --- |
| Round | 1 or 2 only |
| Trigger | Automatic PR publication or the single explicit request |
| Signal | Review, thread, reaction, or explicit no-findings result |
| Findings | Linked GitHub issues for all negative comments |
| Responses | Substantive per-comment dispositions |
| Corrections | Commit and verification evidence when warranted |
| Resolution | Zero unresolved actionable threads |
| State | Pending, active, or complete |

## Closure Set

| Level | Members | Eligibility |
| --- | --- | --- |
| Phase 1 children | #39, #41, #42 | S005 merged and each acceptance criterion evidenced |
| Phase 10 children | #76 through #86 | S005 merged and each acceptance criterion evidenced |
| Phase parents | #6 and #15 | All listed children closed with current-main evidence |
| Milestones | 11 and 20 | Open issue count equals zero |
| Slice | S005 issue | Reviewed implementation merged and housekeeping complete |
| Program | #37 | Ten phase parents and required reconciliation slices complete; external downstream tracking remains linked but separately owned |
