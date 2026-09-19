# System Architecture and Documentation Ownership

BrandBuilder is a source compiler for brand systems. Governed brand records, shared canons, component recipes, and version policy are the inputs. Templates turn those inputs into deterministic brand kits. Verification evaluates generated behavior and provenance before publication. Generated files are evidence and delivery artifacts, not a second source of truth.

## Authority layers

The Brand Canon defines shared identity defaults and immutable boundaries. Each `brands/<slug>/brand.json` supplies one brand's approved values, affiliation, asset sources, and declared exceptions. The Interface Canon defines renderer-neutral semantic roles and runtime capability inputs. Component recipes constrain reusable interaction patterns. Adapter generators translate those contracts into Web/React and egui deliverables without changing their meaning.

When authorities conflict, follow the exact precedence recorded in the generated consumer contract. Do not repair a generator defect by editing `dist/`. Change the owning source or template, regenerate, and run the complete verifier.

## Three documentation surfaces

The main manual owns architecture, operating modes, contracts, generator behavior, verification, versions, release, installation, agent integration, and extension procedures. It does not own a child brand's identity expression or the exact bytes of an older kit.

A hosted child-brand reference owns current approved identity presentation, assets, specimens, bindings, affiliation, and the exact contract versions carried by that site build. Shared system topics link back to this manual. A hosted reference does not replace the bundled contract for an older kit.

The bundled implementation contract owns exact delivered paths, version pins, constraints, verification commands, recovery bytes, checksum, and capability-gap procedure. Its `consumer-contract.json` is machine authority. Its `documentation-facts.json` is the shared fact projection. Its `IMPLEMENTATION.md` is the offline human-readable projection.

## Generator flow

1. Validate brand source and resolve shared canon values.
2. Generate Web/React and egui adapters from the same semantic contracts.
3. Emit the consumer contract, exact recovery bundle, and documentation fact record.
4. Render bundled implementation guidance and the hosted portal from those facts.
5. Verify versions, paths, checksums, provenance, accessibility, and cross-surface equality.
6. Publish only after all required gates report zero failures.

The policy in `documentation-contract.json` inventories every main-manual page and documentation-related route. Adding a page or route without a disposition is an error, which prevents quiet duplication and stale ownership.
