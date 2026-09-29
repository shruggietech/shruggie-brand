# Validation Quickstart: DanceWithMe865 Brand Restart

Run from the repository root in a headless, noninteractive terminal.

1. Confirm `codex/065-dancewithme865-restart` is the active branch and review `specs/065-dancewithme865-brand/` and `brands/dancewithme865/assets/source/`.
2. Inspect the ignored Gate 1 packet and all 32 production proofs. Check the light stacked source against the owner image, including upright DANCEWITHME and the red 865 block. Record the owner's exact Gate 1 decision before promotion.
3. After Gate 1, inspect the ignored Gate 2 packet, including lockups and a separate social share image. Record exact social copy and the owner's Gate 2 decision before compilation.
4. Run `python scripts/build_all.py dancewithme865`; require the generated kit's `verify.py` to report zero problems and `validate_glyph.py` to report zero failures.
5. Run the documented aggregate validation and site lint, build, and test commands from `CONTRIBUTING.md` and `.github/workflows/build.yml`. Check no generated `dist/` files are tracked and confirm UTF-8, LF, and mojibake checks.
6. Inspect the local generated site page and manifest for independent-client ownership and the approved source geometry. Commit sources only, then stop before push under the active Spec Kit skill.

The run stops at the applicable owner approval gate if that decision has not yet been given for this new candidate.
