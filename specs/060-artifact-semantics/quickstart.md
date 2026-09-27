# Validation Quickstart

Run focused negative tests first: `python skill/templates/test_pipeline.py` and `python scripts/test_publication_workflow.py`. Build the eight production kits with `python scripts/build_all.py`, then run the documented site and release checks in `.github/workflows/build.yml`. Run `python scripts/audit_publication_artifacts.py --kits dist --site site/out --semantic --release release` against the exact generated outputs. In CI, run the candidate mode after staging and checksum creation, before upload. Inspect `verification.md` for measured local and CI results.
