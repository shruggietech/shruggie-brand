# Contextual Operating Modes

BrandBuilder has three operating modes. Infer the mode from the requested outcome, repository evidence, and pinned consumer contract. The operator does not need to use a command or name a mode.

## Author mode

Use Author mode when the task changes Brand Canon, Interface Canon, identity source, a brand contract, generator, adapter, recipe, schema, or governed instruction. The task must already authorize the proposed mutation. Run the repository-installed Spec Kit workflow before changing governed source. Retain identity approval, provenance, accessibility, publication, and release safeguards.

Evidence includes a checkout of the BrandBuilder source repository, changes under `brands/`, `skill/references/`, or `skill/templates/`, or an explicit request to extend a shared capability.

## Implementation mode

Use Implementation mode when the task applies an existing pinned brand and interface contract inside a consumer repository. Read `enforcement/consumer-contract.json`, then `enforcement/IMPLEMENTATION.md`. Use declared semantic roles and adapter versions, preserve identity and affiliation, and do not create a permanent parallel design system.

Evidence includes a generated kit, an existing consumer manifest, a product implementation request, or a repository that consumes BrandBuilder output without owning the shared canon.

When the skill is missing, use the exact delivered distribution named under `recovery.path`, verify its SHA-256, and install it through the host's local skill workflow. Do not substitute another version and do not require a network when delivered bytes exist.

## Audit mode

Use Audit mode when the task assesses conformance, accessibility, integrity, provenance, recovery, or adoption without remediation authorization. Audit is read-only. Report evidence and direct remediation to separately authorized Author or Implementation work.

Evidence includes review language, a request for findings only, absent mutation authorization, or a conformance report destination.

## Inference order

1. Identify whether the requested change targets governed BrandBuilder source, a consumer repository, or only an assessment.
2. Read repository evidence and any pinned consumer contract.
3. Confirm the task's existing mutation authority. Mode inference never grants authority.
4. Choose Author for authorized governed-source change, Implementation for authorized consumer change, or Audit for read-only assessment.
5. If intent genuinely conflicts, ask one narrow question about the exact mutation boundary.

## Conflict examples

- "Audit and fix, but do not change files" requires one clarification between read-only Audit and authorized remediation.
- "Apply this pinned kit and redesign its logo" requires separate Author authorization for identity work.
- "File an upstream issue" requires explicit upstream-submission authorization even when a local capability-gap record exists.
- A screenshot or legacy stylesheet that disagrees with the pinned contract is evidence of drift, not authority to reinterpret the brand.

## Handoffs

- Author to Implementation: publish an exact contract, verification entry point, adapter versions, and recovery bytes.
- Implementation to Author: create a local capability-gap record when a reusable semantic concept is missing. Product composition remains local.
- Audit to Author or Implementation: report evidence, affected authority, and recommended owning mode without making the change.
