# Contract: S010 Codex Review Ledger

| Round | Trigger | Maximum | Completion signal |
| --- | --- | ---: | --- |
| 1 | Automatic on official pull-request publication | 1 | Codex review, explicit no-findings message, or thumbs-up signal after review records and threads are checked |
| 2 | One explicit `@Codex review` comment after round 1 completes | 1 | Codex review, explicit no-findings message, or thumbs-up signal after review records and threads are checked |

## Finding disposition

1. Read every review, comment, and inline thread.
2. For every negative finding, create a milestone 22 issue with source linkage, labels, risk or reproduction, and acceptance criteria.
3. Respond substantively to every comment, including disagreements and no-change dispositions.
4. Implement and locally verify every warranted correction before pushing it.
5. Resolve an inline thread only after the correction or justified disposition is posted.
6. Record immutable links and the reviewed head revision in `evidence.md`.

No event permits a third `@Codex` request. Late feedback from either authorized round is processed without extending the ledger.

