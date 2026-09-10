# Publication and Review Contract

## Public eligibility

Cueson remains absent from published site and registry output while Gate 2 is pending, rejected, or stale. After exact Gate 2 approval, the complete public surface set is eligible only when it consumes the current verified generated kit and the derivative manifest hash matches approval.

The public surface set is:

- showcase card;
- brand landing page;
- guideline topics;
- downloads;
- registry endpoints;
- public metadata;
- structured data;
- social preview.

## Verification entry gate

Before push and pull-request creation:

- every approved constructed derivative reports zero glyph failures;
- the Cueson kit reports zero verification problems;
- every text-bearing and declared fill role passes WCAG 2.1 AA without waiver;
- identity-study, approval, contract, generator, pipeline, site, archive, encoding, and repository-hygiene checks pass;
- the complete multi-brand build succeeds from source;
- representative Cueson proofs, guidelines, UI specimen, PDF, icons, and site surfaces receive visual inspection;
- no generated artifact is tracked;
- the Cueson repository and domain boundary remain unchanged.

## Authorized publication workflow

After both gates and the local entry gate, S026 may commit, push `codex/026-cueson-brand-kit`, and open one official pull request that closes #184 without a separate pre-push halt. This authorization does not include merge, release, tag, deployment, consumer import, domain activation, or production configuration changes.

## Review rounds

- The automatic Codex review triggered by pull-request creation is round 1.
- Security-bot, continuous-integration, and human feedback do not increase the Codex round count but every received item requires a disposition.
- For each actionable finding, reproduce it, add or identify a failing regression where practical, implement the smallest warranted correction, verify it, reply with evidence, and resolve the thread when allowed.
- For each non-actionable or stale finding, reply with concrete current-branch evidence and resolve the thread when allowed.
- After all round-1 Codex findings are resolved, S026 may post exactly one `@Codex review` request for round 2.
- No command, comment, edit, automation, or retry may request a third Codex review.
- A thumbs-up reaction on the pull-request body with no review threads is recorded as a satisfied review signal, not converted into an invented finding.

## Final halt

S026 returns to the owner for the final review and merge ritual only when all required checks are green, every received review item is answered and resolved appropriately, security findings are cleared or accurately documented, the review-round count is within the two-round limit, and the branch head is the exact verified head. The agent never merges the pull request.
