# Quickstart: Native Host Conformance

1. Generate a focused ESO Weave and Glitchpad kit in temporary output and inspect the icon manifests, PWA purpose mapping, Win32 ICO frames, Android adaptive XML/layers, and role previews against [native-role-contract.md](contracts/native-role-contract.md).
2. Run the focused generator and verifier regressions, including intentionally malformed mask and resource fixtures. Expected: correct assets pass and each negative fixture reports a role-specific failure.
3. Inspect the locally available ESO Weave source/executable icon and Glitchpad release APK manifest/resources. Record exact pinned hashes and any need to repin downstream; do not alter those repositories in this slice.
4. Rebuild all production kits through the documented build path. Expected: every `verify.py` report has zero problems and every `validate_glyph.py` report has zero failures.
5. Run the full CI-equivalent pipeline, site checks, release-contract tests, encoding/mojibake audit, and repository hygiene checks. Record versions, commands, outputs, and skips in `evidence.md`.
