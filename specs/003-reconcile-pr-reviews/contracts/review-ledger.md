# Contract: Bounded Codex Review Ledger

The S003 pull request body starts with both review entries and updates them without adding a third:

```markdown
## Codex review ledger

| Round | Trigger | Signal | Actionable comments | State |
|---|---|---|---:|---|
| 1 | Automatic on PR publication | Pending | Pending | Pending |
| 2 | One explicit `@Codex` comment after round 1 | Not requested | Pending | Pending |

Review request ceiling: 2 rounds. No third request is authorized.
```

## Round completion rules

A round is complete only when:

1. Its arrival signal is identified as a review, one or more threads, a Codex thumbs-up reaction, or confirmed no-findings behavior.
2. Every actionable comment is linked to a disposition.
3. Every warranted change is covered by a regression or other reproducible check.
4. Every comment receives a substantive response.
5. Every addressed review thread is resolved.
6. The final pushed commit passes local verification.

## Trigger rules

- Publishing the pull request is the only trigger for round 1.
- Round 2 is triggered by exactly one pull-request comment containing `@Codex` after round 1 is complete.
- Correction pushes do not receive another `@Codex` comment.
- Late feedback from either permitted round is processed without triggering a new round.
- Once round 2 is complete, the only remaining gates are required CI success and owner handoff.

## Review response format

```markdown
Addressed in `<commit>`.

Disposition: `<what changed or why no change was needed>`
Verification: `<focused test or check and result>`
Tracking: `<linked issue or S003 task>`
```

Responses must be specific to the comment. A generic acknowledgement does not satisfy the contract.
