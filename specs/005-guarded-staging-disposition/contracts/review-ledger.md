# Contract: Bounded Codex Review Ledger

The S005 pull request body carries exactly these review rows:

```markdown
## Codex review ledger

| Round | Trigger | Signal | Actionable comments | State |
| --- | --- | --- | ---: | --- |
| 1 | Automatic on PR publication | Pending | Pending | Pending |
| 2 | One explicit `@Codex` comment after round 1 | Not requested | Pending | Pending |

Review request ceiling: 2 rounds. No third request is authorized.
```

## Round completion rules

1. Identify the arrival signal as a review, review thread, Codex thumbs-up reaction, explicit no-findings behavior, or a terminal environment-unavailable response that produced zero findings and zero threads.
2. File every negative finding as a GitHub issue with labels, milestone, source link, rationale or reproduction, and acceptance criteria.
3. Give every review comment a substantive disposition and link its issue when negative.
4. Implement every warranted correction and run focused plus proportionate aggregate verification.
5. Push corrections before resolving the affected review thread.
6. Resolve every addressed thread and re-query for late feedback.
7. Record the final signal, finding count, issue links, and state in the pull request and `evidence.md`.

A terminal environment-unavailable response completes the attempted round as an infrastructure outcome, not as a successful code review. It authorizes neither a finding issue nor a replacement review beyond the existing two-round ceiling.

## Trigger rules

- Pull-request publication is the only round 1 trigger.
- Post one and only one `@Codex` pull-request comment after round 1 is complete.
- Correction pushes receive no additional review-request comment.
- Late feedback is processed within its originating authorized round.
- After round 2, only CI completion and owner handoff remain.

## Response format

```markdown
Tracked in #<issue> and addressed in `<commit>`.

Disposition: <specific correction or evidence-backed reason no change was needed>
Verification: <focused test or check and result>
```
