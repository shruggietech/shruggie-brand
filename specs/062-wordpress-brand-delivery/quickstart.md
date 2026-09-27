# Quickstart: S062 verification

1. Run `python skill/templates/test_wordpress.py` for generator, namespace, mapping, archive, and tamper cases.
2. Run `python scripts/build_all.py`, then confirm eight `VERIFY.md` reports have zero problems and all `validate_glyph.py` gates passed.
3. Run the pinned WordPress fixture driver against the generated go-schedule theme at both declared core/PHP pairs. Install the ZIP, activate, insert/save/reopen patterns, compare native editor and front-end values, check non-root assets, preserve saved overrides through an update, and inspect the drift report.
4. Run site lint/build/tests and publication audits from the documented CI workflow.
5. Review the generated `wordpress/README.md`, adapter manifest, inventory, and ZIP together. Generated artifacts remain outside Git.
