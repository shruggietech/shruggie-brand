# S053 Verification Scenarios

1. Build an isolated owned-child source with `inheritance: independent`, authored semantic colors, a sibling-matching accent, and valid AA pairings. Validate its source contract, generate theme tokens and roles, and verify its AA pairing. Confirm no house orange is injected and truthful affiliation persists.
2. Change the fixture's foreground/fill or light accent to fail AA. Confirm `verify.py` rejects measured contrast. Change a role reference to a nonexistent path and confirm source validation rejects it before derivative output.
3. Use a third-party fixture that deliberately shares a house hex. Confirm the palette is accepted while ownership and endorsement remain third-party/none.
4. Build all eight production kits, check zero verifier/glyph problems, and compare source colors and logo path bytes with the pre-S053 baseline.
5. Inspect one multi-color owned brand and one independent brand in `color-roles.json`, hosted guideline JSON, portable HTML, and PDF text. Confirm formal combinations and artwork references, distinct headings, correct/misuse examples, both themes, measured pairs, and non-color cues.
6. Run the documented Python tests, site lint/build/tests, publication audits, Markdown checks, UTF-8/LF/mojibake checks, and Git source-only diff review. Treat local proof-toolchain limitations separately from CI's pinned toolchain.
