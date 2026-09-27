# Research and Classification

## Existing checks

`skill/templates/verify.py` checks icon platform manifests, logo provenance and aliases, consumer and adapter contracts, conformance evidence, and manifest entry hashes. `registry_contract.py` validates catalog/direct item parity and usable UI payloads. `scripts/release_contract.py` checks exact archive membership, versions, provenance, recovery distribution, and release asset inventory. `scripts/prepare_site.py` validates portal deliveries before copying. The exported-tree audit in `scripts/audit_publication_artifacts.py` currently checks symlink/hardlink/hidden paths and eight icon markers; it does not bind every copied file to kit bytes.

## Findings

| Classification | Source and downstream effect | Disposition |
| --- | --- | --- |
| Demonstrated defect | `verify.c_manifest` iterates `files` without requiring a nonempty list. A syntactically valid empty manifest yields a passing checksum report although it certifies no kit files. | Require a populated, unique, safe, identity-matched inventory with file checks. |
| Demonstrated defect | `audit_publication_artifacts` accepts eight markers even if public registries or downloads are absent or altered after site preparation. | Compare exact candidate public trees and advertised indexes with kit source and check staged release copies. |
| Legitimate optional | A brand can lack custom expressions, a capability can be explicitly unsupported, and conformance baseline decisions can be empty pending human proof. | Preserve declared empty/unsupported states; require mandatory artifacts and reasons where the existing contract does. |
| Legitimate static component with bounded use evidence | The pre-#263 generic-row claim was stale. Current `gen_nextjs.py` calls each row a static data row for a suitable grid or table, and the emitted item contains nonempty TSX. The isolated shadcn install compiles the 24 UI items, but it does not establish arbitrary downstream container behavior. | Record the exact consumer-test boundary; no interactive keyboard claim or new defect is inferred. Open a focused issue only if an actual container integration fails. |
| Related open work | Guideline fact and bundle values can be certified as data, while the full reader-task and content quality audit is broader. | Keep #270 open. |

## Clarifications resolved from source

There is no required new public endpoint in #269. Existing public registry item URLs, download files, documentation publication JSON, and conformance fixtures are the consumer surfaces. Semantic completeness means these advertised surfaces resolve with the expected content and versions. The existing source record governs optional states. No owner decision is needed to distinguish these cases.
