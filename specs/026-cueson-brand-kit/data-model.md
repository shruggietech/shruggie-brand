# Data Model: Cueson Brand Kit

## Product Evidence Snapshot

**Fields**: `repository`, `revision`, `retrieved_at`, `source_paths`, `claims`, `excluded_visual_inputs`, `notes`.

**Rules**:

- Contains one Shruggie Brand default-branch revision and one Cueson default-branch revision.
- Separates factual claims from excluded visual characteristics.
- A material claim or source revision change is evaluated before each gate and recorded as relevant, irrelevant, or approval-invalidating drift.

## Identity Criterion

**Fields**: `id`, `product_truth`, `visual_implication`, `required_proof`, `failure_condition`.

**Rules**:

- Identifiers are stable lower-kebab-case values.
- Every glyph candidate maps explicitly to each criterion as met, partial, or unmet.
- Required criteria cover timing, structured content, interchange, preservation, format breadth, bitmap/OCR distinction, small-size behavior, and cliché avoidance.

## Glyph Candidate

**Fields**: `id`, `revision`, `name`, `status`, `concept`, `represented_criteria`, `geometry`, `full_variant`, `reduced_variant`, `single_ink_variant`, `size_proofs`, `surface_proofs`, `silhouette_metrics`, `risks`, `tradeoffs`, `source_sha256`, `proof_manifest_sha256`.

**Rules**:

- Gate 1 contains three to five candidates and exactly one recommendation.
- Every candidate supplies proofs at 256, 64, 32, and 16 pixels on light and dark surfaces.
- `status` is one of `exploring`, `recommended`, `revising`, `approved`, or `rejected`.
- Only one exact candidate revision may transition to `approved` after explicit owner wording is recorded.

## Color-System Candidate

**Fields**: `id`, `revision`, `status`, `roles`, `light_roles`, `dark_roles`, `single_ink`, `contrast_matrix`, `color_vision_matrix`, `parent_relationship`, `rationale`, `risks`, `configuration_sha256`.

**Rules**:

- Exactly one color system is recommended in Gate 1.
- Every declared text or fill relationship records a threshold and measured result.
- Identity, emphasis, warning, success, and failure roles remain distinguishable by more than hue alone.
- Canonical eligibility begins only after explicit Gate 1 approval.

## Approval Ledger Entry

**Fields**: `gate`, `status`, `candidate_ids`, `source_hashes`, `configuration_sha256`, `manifest_sha256`, `surfaces`, `displayed_evidence`, `owner_wording`, `approved_by`, `approved_at`, `supersedes`.

**Rules**:

- `gate` is `gate-1` or `gate-2`; `status` is `pending`, `approved`, `rejected`, or `stale`.
- Gate 1 approval requires the exact glyph revision, palette revision, producing-configuration hash, evidence paths, owner wording, identity, and timestamp.
- Gate 2 approval requires the exact derivative-manifest hash and complete public surface set.
- A changed bound hash transitions the record from `approved` to `stale`; it never updates approval silently.

## Cueson Brand Source

**Fields**: affiliation, descriptors, audience, voice, accent, surfaces, typography, components, logo geometry, wordmark rules, minimum sizes, role colors, guide content, approval ledger, canon version.

**Rules**:

- Does not exist as a production source before Gate 1 approval.
- Uses ShruggieTech-owned public affiliation and house inheritance.
- Uses only Gate 1-approved master geometry and palette and Gate 2-approved derivative-producing metrics.
- Any later identity geometry change requires a new explicit owner decision and comparison evidence.

## Derivative Asset

**Fields**: `id`, `family`, `variant`, `source_ids`, `source_hashes`, `transformation`, `dimensions`, `surface`, `sha256`, `validation_results`.

**Rules**:

- `family` belongs to the current required derivative family set.
- Every derivative traces to the approved Gate 1 master and configuration.
- A reduced master is separate geometry only when measurements justify it and Gate 2 approves it explicitly.
- All generated derivatives are ignored artifacts and are reproducible from committed source.

## Consumer Handoff Manifest

**Fields**: `brand_revision`, `approval_ids`, `source_assets`, `generated_assets`, `consumer_destinations`, `licenses`, `integration_issue`, `integration_slice`, `domain_boundary`, `sha256`.

**Rules**:

- Every intended asset is hash-addressed and carries a license or usage basis.
- Cueson destinations are proposals until a later Cueson issue and Spec Kit slice approve import.
- The manifest states that `cueson.io`, DNS, and Cloudflare are unchanged.

## Review Ledger

**Fields**: `pull_request`, `check_runs`, `review_rounds`, `threads`, `security_findings`, `responses`, `resolutions`, `final_state`.

**Rules**:

- Automatic review is round 1; at most one explicit `@Codex review` request creates round 2.
- Every received comment or thread has an actionable, non-actionable, or superseded disposition with evidence.
- `final_state` can become `owner-review-ready` only when required checks are green and all received reviews are satisfied.

## State Transitions

```text
researched -> gate-1-pending -> gate-1-revising -> gate-1-approved
gate-1-approved -> gate-2-pending -> gate-2-revising -> gate-2-approved
gate-2-approved -> verified -> pull-request-open -> reviews-in-progress -> owner-review-ready
approved -> stale when any bound producing source or manifest hash changes
```
