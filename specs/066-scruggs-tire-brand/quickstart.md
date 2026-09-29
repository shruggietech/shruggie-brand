# Quickstart: S066 Implementation and Verification

1. Read [spec.md](spec.md), [research.md](research.md), [plan.md](plan.md), and [approval-and-publication.md](contracts/approval-and-publication.md). Confirm the current website claims that will appear in public copy.
2. Inventory only the ZIP base-level assets needed for named design decisions. Preserve the archive and source hashes in the working brief; leave `Brand/old/greertires.com.7z` unopened unless a later decision specifically requires it.
3. Prepare the exact Full and Reduced production candidates and 32 proofs. Record explicit Gate 1 approval before production source promotion.
4. Assemble provisional fundamentals and a separate social share image in ignored output. Run the repository's authoring-brief and Gate 2 packet validator. Record explicit Gate 2 approval before final kit compilation.
5. Build using the documented `python scripts/build_all.py` flow. Run the generated kit's `verify.py` and `validate_glyph.py` and retain zero-problem evidence. Run the full checks listed in `CONTRIBUTING.md` and `.github/workflows/build.yml`, then inspect all eight public site surfaces.
6. Review the Git inventory. Only source and Spec Kit evidence belong in the PR. Never stage `dist/`, the ZIP, legacy `.7z`, or `.specify/feature.json`.

At the current planning stage, steps 3 through 5 have not occurred. This document is an execution guide, not verification evidence.
