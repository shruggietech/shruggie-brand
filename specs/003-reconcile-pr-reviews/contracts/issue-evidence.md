# Contract: GitHub Issue Evidence

Every S003 issue disposition comment uses this public structure:

```markdown
## S003 verification

- Verified baseline: `<full current-main SHA>`
- Acceptance result: `<pass or incomplete>`
- Evidence:
  - `<criterion-specific file, command, workflow, artifact, or hosted check and result>`
- S003 pull request: `<URL when available>`
- Remaining proof: `<none, or explicit unmet criterion/dependency>`

Decision: `<closed because every criterion is satisfied on current main, or kept open>`
```

## Required behavior

- Preserve the issue's existing body and history.
- Cite evidence for each criterion, not only an aggregate workflow result.
- Use a full commit SHA for the verified current-main baseline.
- Use public repository-relative paths and public URLs. Never include a private absolute path.
- For review-finding issues, include the source-thread reply URL and focused regression name.
- Close only after the evidence comment is successfully posted.
- If a correction exists only in S003, record it as branch evidence and keep a current-main-gated issue open.
- If any criterion is not proven, state it under `Remaining proof` without softening the published requirement.

## Parent phase summary

```markdown
## S003 phase status

- Closed children: `<complete list>`
- Open children: `<complete list>`
- Acceptance result: `<pass or incomplete>`
- Evidence ledger: `<S003 pull request or committed evidence path>`

Decision: `<closed only when all children and phase acceptance pass, otherwise kept open>`
```
