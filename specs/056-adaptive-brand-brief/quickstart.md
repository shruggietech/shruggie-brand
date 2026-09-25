# Validation Guide

1. Read `skill/references/03-interview.md` with sparse and extensive source material. Confirm only unanswered, decision-relevant follow-ups are asked.
2. Walk new and supplied-logo cases through `06-logo-protocol.md` and `identity-continuity.md`. Confirm concept selection is not Gate 1 and source drift invalidates approval.
3. Walk an unresponsive operator through both gates. Confirm neither defaults to approved.
4. Inspect Gate 2 packet guidance. Confirm exact slogan, optional approved description, layout, social image, formal palette, and interface cues appear before final compilation. Confirm review output is private.
5. Run `python skill/templates/test_pipeline.py`, `python skill/templates/sync_agents_md.py skill`, `python scripts/build_all.py`, and site lint/build/test from `.github/workflows/build.yml`. Record results in `evidence.md`.
