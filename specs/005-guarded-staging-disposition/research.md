# Research: Guarded Staging Disposition and Program Closure

## R1. Existing backup sufficiency

**Decision**: Reuse the existing dated pre-disposition archive rather than creating a duplicate.

**Rationale**: Streaming comparison found 2,479 archive files with zero missing live counterparts, zero extra archived files, zero byte-count differences, and zero SHA-256 differences. The live workspace has two additional files, both Python bytecode caches generated after the archive. They contain no authoritative or historical source and are reproducible from governed Python templates.

**Alternative rejected**: Create a second roughly 138 MB archive. It would preserve only two disposable bytecode caches and add redundant storage without improving recovery coverage.

## R2. Cloudflare preflight without a local CLI

**Decision**: Treat the authenticated Cloudflare API integration as the permitted API access path and verify it with an account-scoped read.

**Rationale**: The local CLI and token environment variable are absent, but the integration returned a successful authenticated response for the intended organization account. The work order permits REST API access and does not require a particular client binary.

**Alternative rejected**: Install another CLI or expose a token solely to satisfy a tool-name expectation. That would expand scope and create unnecessary credential risk.

## R3. Public and private evidence boundary

**Decision**: Maintain a private exact recovery record and a separate sanitized repository ledger.

**Rationale**: Recovery requires exact paths, hashes, collision checks, and move destinations. The public repository and GitHub issues explicitly prohibit workstation layout, backup locations, raw session output, credentials, and provider identifiers.

**Alternative rejected**: Redact a single shared ledger after execution. Redaction is easier to get wrong and would make the recovery copy less operationally useful.

## R4. Cold storage versus owning repositories

**Decision**: Use governed cold storage for historical bulk output, private materials, and unrelated research unless an exact collision-free owning-project destination is already established.

**Rationale**: Go Schedule has an owning repository, but selecting a new internal destination would mutate another project on inference. The Covarity repository is not present locally. Cold storage preserves the material without contaminating or overwriting another codebase.

**Alternative rejected**: Create new folders or commits in sibling projects. That is unnecessary for this slice and could misclassify research ownership.

## R5. SVG runtime helper authority

**Decision**: Retain the repository template as authoritative and classify the staged runtime helper as regenerable.

**Rationale**: The staged and governed JavaScript helpers differ only in ternary-expression formatting. Their argument handling, renderer construction, fit mode, output behavior, and failure semantics are equivalent. The repository copy is newer and is referenced by generator probes and raster/QC code.

**Alternative rejected**: Import the staged formatting variant or retain the entire runtime as source. Neither preserves unique behavior.

## R6. Historical and provenance preservation

**Decision**: Keep small source-level provenance in Git and bulk generated history in cold storage.

**Rationale**: The repository already contains Fragcap construction scripts and masters, Go Schedule masters, and two parent-brand CSS sources. PDFs, comparison images, screenshots, and early generated marks are valuable history but violate the source-only boundary if committed.

**Alternative rejected**: Commit the historical archive or rely only on the recovery ZIP. The former violates repository policy; the latter loses a deliberate searchable history class after cleanup.

## R7. Closure timing

**Decision**: Keep S005-dependent children, parents, milestones, and program #37 open until the owner merges the reviewed pull request.

**Rationale**: Their state policies require current-main evidence. The operational moves may finish on the branch, but `docs/disposition.md` and S005 evidence are not authoritative repository records until merged.

**Alternative rejected**: Close work after local execution. That would repeat the earlier project-management error of treating branch evidence as current-main completion.
