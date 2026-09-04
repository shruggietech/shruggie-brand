# Data Model: S003 Evidence and Review State

## ReviewFinding

Represents one inherited negative review observation.

| Field | Type | Rules |
|---|---|---|
| `task_id` | string | Unique, `003-T001` through `003-T019` |
| `issue_number` | integer | Unique GitHub issue, #17 through #25 or #27 through #36 |
| `source_pr` | integer | #16 or #26 |
| `source_thread_url` | URL | Immutable GitHub discussion link |
| `acceptance` | list | Complete published issue acceptance criteria |
| `focused_checks` | list | Reproducible tests or commands |
| `implementation_ref` | commit or `none` | Existing correction or new S003 commit |
| `disposition` | enum | `fixed-on-main`, `fixed-in-s003`, `not-reproducible`, `blocked` |
| `reply_url` | URL | Required before completion |
| `thread_state` | enum | `unresolved`, `resolved` |

Validation: completion requires passing focused checks, a substantive reply URL, and `thread_state=resolved`. `blocked` is not a successful terminal state for S003.

## IssueCertification

Represents an issue-level closure decision.

| Field | Type | Rules |
|---|---|---|
| `issue_number` | integer | Unique within the ledger |
| `verified_commit` | SHA | Must identify current `origin/main` for closure evidence |
| `criteria` | list of CriterionResult | One entry per published checkbox or acceptance statement |
| `evidence` | list of EvidenceRecord | At least one reproducible record per satisfied criterion |
| `decision` | enum | `close`, `keep-open` |
| `missing_proof` | list | Required when `decision=keep-open` |
| `comment_url` | URL | Required after GitHub state update |

Validation: `decision=close` is valid only when every criterion is satisfied on current main and `missing_proof` is empty.

## CriterionResult

| Field | Type | Rules |
|---|---|---|
| `criterion` | string | Exact or faithful summary of the public requirement |
| `status` | enum | `pass`, `fail`, `not-proven` |
| `evidence_refs` | list | Non-empty when status is `pass` |

## EvidenceRecord

| Field | Type | Rules |
|---|---|---|
| `kind` | enum | `file`, `test`, `artifact`, `workflow`, `deployment`, `review-reply` |
| `reference` | string or URL | Public and reproducible |
| `result` | string | Concise observed result |
| `commit` | SHA or `not-applicable` | Required for repository evidence |
| `sensitive_scan` | enum | `pass` required for public prose |

## ReviewRound

| Field | Type | Rules |
|---|---|---|
| `ordinal` | integer | Only 1 or 2 |
| `trigger` | enum | Round 1 `automatic`, round 2 `manual-@Codex` |
| `trigger_url` | URL or `automatic` | Round 2 must record exactly one comment URL |
| `arrival_signal` | enum | `review`, `threads`, `thumbs-up`, `no-findings-confirmed` |
| `comments` | list | Every actionable and non-actionable review item |
| `changes` | list | Correction commits, if any |
| `state` | enum | `pending`, `processing`, `complete` |

State transitions:

```text
round-1-pending -> round-1-processing -> round-1-complete
round-1-complete -> round-2-requested -> round-2-processing -> review-complete
```

There is no state transition from `review-complete` to another request.

## PhaseClosure

| Field | Type | Rules |
|---|---|---|
| `parent_issue` | integer | One of #6 through #15 |
| `children` | list of issue numbers | Must match the parent issue's public ledger |
| `closed_children` | list | Derived from GitHub after child updates |
| `decision` | enum | `close`, `keep-open` |
| `summary_url` | URL | Parent progress or closure comment |

Validation: `decision=close` requires set equality between `children` and `closed_children`.
