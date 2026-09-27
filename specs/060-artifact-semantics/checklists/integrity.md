# Artifact Integrity Requirements Checklist

**Purpose**: Review requirement coverage for the publication boundary. These are review questions, not implementation results.

- [x] Does the spec distinguish required records from legitimate empty or unsupported states for every family?
- [x] Are file paths required to stay inside the declared kit or publication root, including symlink cases?
- [x] Are complete inventories and byte digests required after copying into the public tree?
- [x] Are brand, compiler, contract, and release versions compared across related records?
- [x] Is the exact staged candidate checked after copying, before upload or promotion?
- [x] Are negative cases named for empty, missing, changed, and optional data?
- [x] Does the evidence distinguish inspection, schema checks, consumer use, and production checks?

Reviewed against [spec.md](../spec.md) on 2026-09-27. These checks assess requirement coverage, not implementation status.
