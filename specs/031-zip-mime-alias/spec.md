# Feature Specification: Hosted ZIP MIME Compatibility

**Feature Branch**: `codex/031-zip-mime-alias`

**Created**: 2026-09-12

**Status**: Ready for Planning

**Issue**: [#198](https://github.com/shruggietech/shruggie-brand/issues/198)

**Input**: User description: "Accept the GitHub Pages ZIP MIME alias in the production verifier while preserving fail-closed archive validation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Verify valid hosted ZIP downloads (Priority: P1)

As a maintainer, I can verify production ZIP downloads when the hosting service labels them with either of the two established ZIP media types, so a valid deployment is not rejected because of equivalent response metadata.

**Why this priority**: Production verification currently fails for every hosted brand ZIP even though the archive bodies are valid, blocking trustworthy publication checks.

**Independent Test**: Serve the same valid ZIP body once as `application/zip` and once as `application/x-zip-compressed`, then confirm that both responses pass the payload contract.

**Acceptance Scenarios**:

1. **Given** a valid ZIP body labeled `application/zip`, **When** the payload contract evaluates it, **Then** the response passes ZIP media-type and archive-body validation.
2. **Given** a valid ZIP body labeled `application/x-zip-compressed`, **When** the payload contract evaluates it, **Then** the response passes ZIP media-type and archive-body validation.
3. **Given** the production site serves valid brand ZIPs using the hosting service's ZIP alias, **When** production-origin verification runs, **Then** those downloads do not fail solely because of that alias.

---

### User Story 2 - Reject mislabeled or malformed downloads (Priority: P2)

As a maintainer, I can rely on verification to reject a response whose declared type or archive bytes are invalid, even when one half of the contract appears acceptable.

**Why this priority**: Expanding the accepted metadata must not allow error pages, truncated archives, or unrelated payloads to pass as release downloads.

**Independent Test**: Exercise both accepted media types with malformed bodies, and exercise a valid ZIP body with an unsupported media type, then confirm that every response fails with the applicable diagnostic.

**Acceptance Scenarios**:

1. **Given** either accepted ZIP media type with a body missing a valid ZIP signature or end record, **When** the payload contract evaluates it, **Then** validation fails on archive structure.
2. **Given** a structurally valid ZIP body labeled with an unsupported media type, **When** the payload contract evaluates it, **Then** validation fails on media type.
3. **Given** an HTML error body labeled with an accepted ZIP media type, **When** the payload contract evaluates it, **Then** validation fails on archive structure.

---

### User Story 3 - Preserve all other payload contracts (Priority: P3)

As a maintainer, I can adopt the ZIP compatibility correction without changing validation behavior for documents, images, fonts, metadata, or other downloadable file types.

**Why this priority**: The repair should be narrowly scoped so established production safeguards remain stable.

**Independent Test**: Run the complete payload-contract and site-verification regression suites and confirm that all non-ZIP expectations and diagnostics continue to pass.

**Acceptance Scenarios**:

1. **Given** a non-ZIP production payload, **When** the corrected contract evaluates it, **Then** its existing media-type and body checks are unchanged.
2. **Given** an unsupported ZIP media type, **When** validation fails, **Then** the diagnostic identifies the declared media type and the accepted ZIP types.

### Edge Cases

- An accepted ZIP media type includes a charset or other response parameter.
- An accepted ZIP media type uses different letter casing.
- A valid ZIP has its end-of-central-directory record near the maximum permitted comment boundary.
- A response starts with a ZIP local-file signature but has no end-of-central-directory record.
- A response has a ZIP end record but no valid local-file signature.
- A valid ZIP body is served as a generic binary stream or another unsupported media type.
- A hosted response is empty, truncated, or contains an HTML error page.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The ZIP payload contract MUST accept `application/zip` and `application/x-zip-compressed` as equivalent supported media types.
- **FR-002**: Media-type comparison MUST preserve the existing normalization of letter casing and response parameters.
- **FR-003**: A ZIP response using either supported media type MUST still contain both the required ZIP opening signature and an end-of-central-directory record within the permitted search boundary.
- **FR-004**: A structurally valid ZIP body with any media type other than the two explicitly supported ZIP media types MUST fail validation.
- **FR-005**: A malformed, empty, truncated, or HTML body MUST fail ZIP validation even when labeled with a supported ZIP media type.
- **FR-006**: Validation failures MUST continue to distinguish unsupported media-type evidence from invalid archive-body evidence.
- **FR-007**: The correction MUST apply to both local payload-contract checks and production-origin verification through their shared validation boundary.
- **FR-008**: Validation behavior for every non-ZIP extension and payload type MUST remain unchanged.
- **FR-009**: Regression coverage MUST exercise both supported ZIP media types with valid and malformed bodies, plus a valid ZIP body with an unsupported media type.
- **FR-010**: The correction MUST NOT modify brand sources, identity artwork, generated kits, release archives, or committed production exports.

### Key Entities

- **ZIP payload contract**: The combined declaration and archive-structure rules applied to a requested ZIP download.
- **Normalized media type**: The response media type after the existing case and parameter normalization is applied.
- **Supported ZIP media type**: Either `application/zip` or `application/x-zip-compressed`.
- **ZIP structure evidence**: The opening local-file signature and end-of-central-directory record required for an archive body to pass.
- **Production-origin verification**: The hosted-site check that fetches production downloads and applies the shared payload contract.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Valid ZIP fixtures pass in 100 percent of regression cases when labeled with either supported ZIP media type.
- **SC-002**: Malformed ZIP fixtures fail in 100 percent of regression cases under both supported ZIP media types.
- **SC-003**: A valid ZIP fixture labeled with each covered unsupported media type fails in 100 percent of regression cases.
- **SC-004**: The complete existing payload-contract and site-verification test suites pass with zero regressions.
- **SC-005**: Production-origin verification reports zero ZIP media-type failures when the hosted brand archives are valid and labeled `application/x-zip-compressed`.
- **SC-006**: The completed slice changes zero brand-source, identity-artwork, generated-kit, or release-archive files.

## Assumptions

- GitHub Pages continues to serve the production brand ZIP downloads as `application/x-zip-compressed`.
- `application/zip` remains the canonical ZIP media type used by local fixtures and other conforming servers.
- The existing media-type normalization and ZIP signature/end-record rules remain authoritative.
- Generic binary media types such as `application/octet-stream` remain unsupported for ZIP downloads.
- The production origin remains `https://brand.shruggie.tech`.

## Scope

### In scope

- The ZIP media-type allowlist in the shared payload contract.
- Focused regression coverage for accepted aliases, malformed archives, and unsupported types.
- Local and production-origin verification evidence for the corrected behavior.

### Out of scope

- Changes to hosting configuration, server headers, archive generation, or release packaging.
- Relaxation or replacement of ZIP structure checks.
- Changes to non-ZIP media-type contracts.
- Brand presentation, identity assets, downloadable artifact contents, or generated exports.

## Done When

- Both supported ZIP media types pass for valid ZIP bodies and fail for malformed ZIP bodies.
- Unsupported ZIP media types remain rejected even when the archive body is valid.
- Focused and full documented validation pass with zero problems.
- Production-origin verification succeeds against the hosted ZIP responses.
- Specification, plan, tasks, implementation, verification evidence, and changelog remain synchronized.
