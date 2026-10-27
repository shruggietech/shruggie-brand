# S073 Verification Quickstart

1. From the S073 checkout, compare the source diff with `origin/main` and confirm it contains only the three issue surfaces, Spec Kit records, tests, and a proportional changelog entry.
2. Run the documentation-reference validator and Markdown policy checker. Confirm 68 reference IDs and four fields per entry, with every original link target retained.
3. Run the site source tests, lint, build, and rendered site verifier. Measure the desktop DanceWithMe865 title and marker against the card content box; exercise a temporary longer-title case.
4. Inspect the homepage at the narrowest desktop grid width, 390px, 320px, and 200% text enlargement. Check heading order, intro grouping, title clearance, marker association, and absence of horizontal page scrolling.
5. Inspect the References page at desktop, 390px, 320px, and 200% enlargement. Check representative short and long entries, all field labels, anchor navigation, long URL wrapping, selection, and keyboard focus.
6. Run the repository's full documented production-kit and accessibility validation. Require zero production `verify.py` problems and zero `validate_glyph.py` failures. Record unavailable capabilities as unverified, never as passes.
7. Check UTF-8 without BOM, LF endings, mojibake, and `git diff --check`. Commit only sources and Spec Kit evidence.
