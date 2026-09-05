# Research: Ownership-Neutral Authoritative Inputs

## Decision 1: Pair JSON Schema with one runtime contract module

**Decision**: Add the missing `canon.schema.json` using JSON Schema Draft 2020-12, then enforce cross-field and filesystem rules through `brand_contract.py` and the first-step `validate_brand.py` preflight.

**Rationale**: Every current brand already advertises the absent schema path. Draft 2020-12 is the current published JSON Schema dialect and supports conditional structural rules, but file hashes, path containment, font internals, SVG active content, approval freshness, and generated-output checks require runtime inspection. One shared runtime module prevents each generator from inventing its own interpretation.

**Sources**: [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12), [JSON Schema specification](https://json-schema.org/specification)

**Alternatives considered**: Schema only cannot inspect bytes or relationships outside the JSON document. Runtime validation only would leave authoring tools attached to a broken `$schema` reference. Adding a new JSON Schema package would expand CI dependencies without removing the need for custom checks.

## Decision 2: Model affiliation facts independently and fail closed

**Decision**: Use one explicit `affiliation` object with closed ownership, showcase, inheritance, endorsement, and service-credit values plus nullable parentage. House inheritance retains ShruggieTech semantic colors. Independent inheritance requires explicit brand-specific emphasis and action colors. Reject missing fields and invalid combinations before generation.

**Rationale**: Ownership, hierarchy, attribution, and permission to publish answer different questions. Combining them recreates the original false-ownership defect. Fail-closed configuration protects future third-party work, while explicit migration preserves each current owned brand intentionally.

**Alternatives considered**: A single `third_party` boolean cannot represent private owned work, public client work, parent brands, or optional neutral credit. Defaulting missing data to owned would keep the dangerous behavior. Inferring ownership from parent text would make free-form copy authoritative.

## Decision 3: Keep neutral credit closed and fixed

**Decision**: Allow only `none` or the fixed neutral output `Brand system by ShruggieTech`, with the latter permitted only for third-party work. Owned product endorsement remains the separate fixed output `A ShruggieTech project`.

**Rationale**: Closed values make output scanning reliable and prevent arbitrary claims from entering generated metadata. Separating credit from endorsement prevents service-provider credit from implying ownership.

**Alternatives considered**: Free-form credit text is impossible to classify reliably and risks confidential or legally misleading wording. Reusing the owned endorsement for clients is the defect S007 exists to remove.

## Decision 4: Validate fixed font binaries through OpenType metadata

**Decision**: Use fontTools `TTFont`, the OpenType naming table, `OS/2.usWeightClass`, and `OS/2.fsSelection` to verify declared family, weight, and style. Require approved local face records with hashes and licensing facts, and reject unsupported variable faces in S007.

**Rationale**: Extensions and filenames do not prove a font's identity. The OpenType specification defines family preference, weight class, and italic or oblique selection flags, while fontTools exposes the required tables without another dependency. Rejecting variable fonts keeps generated weight behavior deterministic until axis pinning has a dedicated design.

**Repository finding**: Measured validation found that the existing Space Grotesk Medium and Bold WOFF2 binaries reported the internal family `Space Grotesk Light`. They were rebuilt from the authoritative local TTF faces and remeasured as `Space Grotesk` at weights 500 and 700. This is a derived webfont correction, not an identity change.

**Sources**: [fontTools naming table](https://fonttools.readthedocs.io/en/latest/ttLib/tables/_n_a_m_e.html), [OpenType OS/2 table](https://learn.microsoft.com/en-us/typography/opentype/spec/os2)

**Alternatives considered**: Trusting filenames permits silent substitution. Reading CSS metadata does not verify the binary. Accepting variable fonts without declared axis coordinates would make measured weight and generated use ambiguous.

## Decision 5: Separate controlled ingestion from ordinary builds

**Decision**: `ingest_font.py` accepts a local source or HTTPS URL only when invoked explicitly, requires an expected SHA-256 and licensing metadata, limits payload size and redirects, validates in temporary storage, and uses atomic replacement inside `assets/fonts/`. No generator imports or invokes network code.

**Rationale**: Python's standard URL API supports HTTPS requests, timeouts, and response inspection, but network availability must never become a build dependency. A temporary file followed by validated replacement prevents partial approved state after interruption.

**Source**: [Python `urllib.request`](https://docs.python.org/3.11/library/urllib.request.html)

**Alternatives considered**: Fetching during `build_all.py` breaks deterministic offline builds. Requiring manual copying loses hash and metadata verification. Adding a package manager would not cover proprietary or client-licensed authoritative sources.

## Decision 6: Preserve supplied inputs and permit passive SVG only

**Decision**: Treat each supplied file as immutable input evidence. Validate containment and SHA-256, reject scripts, event handlers, live text, external URLs, and externally referenced resources in SVG, and allow only explicitly listed non-identity transformations such as recoloring a raster mask or embedding unchanged artwork.

**Rationale**: SVG supports scripting and external resources, so accepting arbitrary documents into generated sites or renderers creates a security and reproducibility risk. The repository already supports imported raster masters; S007 makes that exception explicit without redrawing or normalizing them.

**Repository finding**: The Node resvg fallback did not resolve relative `<image>` resources, which made ShruggieTech's preserved raster mark disappear from PNG exports while the pipeline still reported success. Generated wrappers now embed approved derived raster masks or unchanged passive SVG bytes as contained data, and raster output fails when it has no visible pixels.

**Sources**: [SVG Integration](https://www.w3.org/TR/svg-integration/), [SVG 2 conformance and external resources](https://www.w3.org/TR/SVG2/conform.html)

**Alternatives considered**: Sanitizing and rewriting supplied SVG would violate byte preservation. Trusting any SVG would admit live text, network dependencies, and active content. Rasterizing the master would be a lossy identity transformation.

## Decision 7: Generate palette evidence deterministically and require approval freshness

**Decision**: For raster inputs, convert visible pixels to RGBA, discard alpha zero, count exact RGB values, and rank by count then hex value. For SVG, count declared solid paint colors from passive markup. Evidence records the source hash, method, visible sample count, ignored transparent count, candidate values, and limitations. Canonical use requires a human approval whose source hash and selected candidate still match that evidence.

**Rationale**: Exact counting is deterministic and easy to audit. It avoids presenting color quantization as objective truth. Human approval remains the identity decision, and existing downstream contrast checks remain mandatory.

**Source**: [Pillow image reference](https://pillow.readthedocs.io/en/stable/reference/Image.html)

**Alternatives considered**: Automatic canonical selection would outsource an identity decision to sampling heuristics. K-means without pinned implementation details can drift. Ignoring alpha would promote invisible matte pixels into brand colors.

## Decision 8: Keep generated evidence out of source declarations

**Decision**: Write measured supplied-input and palette evidence to generated kit output under `qc/authoritative-inputs.json`. Store only the operator approval linkage in source `brand.json`.

**Rationale**: Evidence is reproducible from immutable source bytes, while approval is an authoritative human decision. This division follows the repository rule that generated artifacts stay out of version control and prevents measured values from becoming stale source data.

**Alternatives considered**: Committing extracted candidates creates drift and review noise. Keeping approvals only in generated output would lose the operator decision on the next clean build.

## Decision 9: Filter private kits at the site boundary

**Decision**: Production source discovery and generation may include private brands, but `prepare_site.py` publishes only validated records with `affiliation.showcase == public` and removes previously generated public directories that are no longer eligible.

**Rationale**: A brand can legitimately need a kit without public portfolio permission. Treating a private kit as an unexpected build artifact would conflate generation with publication.

**Alternatives considered**: Excluding private sources from all builds would reduce verification. Publishing every `dist` directory repeats the rights defect. Maintaining a second site allowlist would drift from the authoritative brand record.

## Decision 10: Do not amend the constitution

**Decision**: Keep constitution 2.0.0 unchanged.

**Rationale**: The constitution already requires source integrity, identity preservation, WCAG AA, verified publication, generated-site consumption, and Spec Kit traceability. S007 implements those principles without changing governance.

**Alternatives considered**: Adding feature-specific affiliation fields to the constitution would overfit policy to one schema revision.
