# Verification Evidence: Compact egui Desktop Density

**Baseline**: `f974fbb` on `main`

**Branch**: `codex/044-compact-egui-density`

**Issue**: #239

**Pull request**: Pending

## Chronological verification record

1. Operator screenshots showed 44-point buttons, toggles, radio-style controls, and selectors surrounding 13-to-14-point body text, plus excessive Live Log row spacing. Health, Magicka, Stamina, and Ultimate meters were explicitly accepted and excluded.
2. Source inspection traced the regression to unconditional assignment of the Interface Canon 44-unit target to egui `interact_size` on both axes. Compact density scaled spacing but intentionally could not reduce the target.
3. Issue #239 recorded the regression, scope, accessibility boundary, and production verification gate.
4. S044 specified a capability-aware split: fine-pointer desktop controls derive a 28-point comfortable and 22.96-point compact visual height, while touch, coarse, mixed, and unknown profiles retain 44-point targets.
5. The existing focused suite passed three of three Python tests and the generated Cargo suite before new regressions were added. Markdown prose validation also passed.
6. Version-policy review classified the correction as egui adapter patch behavior because public symbols remain compatible. Compiler major 2 therefore needs an explicit compatibility edge for adapter 1.0.1.
7. Test-first regressions then failed as expected: the generated manifest still reported 1.0.0, comfortable fine-pointer height remained 44 instead of at most 28, compact height remained 44 instead of at most 24, and a 3x text scale did not grow the fixed target. Seven other generated Rust tests continued to pass, including conservative target retention.
8. The generator correction derived fine-pointer height from the canonical 44-point target minus two 8-point pointer-hit-slop margins. This produced 28 points comfortable and 22.96 points compact, while touch, coarse, mixed, and unknown pointer profiles retained 44 points.
9. Compact vertical item spacing became 1.64 points and the rendered two-label regression remained at or below the 2-point limit. Resource-meter source and brand identity inputs were not changed.
10. Focused verification passed three egui Python tests and ten generated Rust tests, 18 interface-contract tests, five component tests, 13 conformance tests, and the Markdown audit.
11. The complete Python workflow suite passed. Its pipeline suite reported 68 passing tests under the repository-pinned Node 24.11.0 renderer after 32 approved identity proofs were exported with the same renderer version.
12. The ESO Weave production kit and the repository-wide eight-kit build completed cleanly. Every kit reported zero verifier problems, zero image-QC problems, zero PDF-QC problems, zero pagination splits, and zero glyph failures. ESO Weave reported eight glyph checks with four expected warnings.
13. Release packaging and certification verified nine v2.0.0 assets and generated validated release notes. The capability probe reported the full tier, including a launching Chromium runtime.
14. Site lint and TypeScript validation passed, the static build emitted 95 pages, and 12 Node contract tests passed. The initial browser run exposed a deterministic navigation race in the verifier because it measured an iframe while the selected conformance profile was reloading it.
15. The verifier now waits for the selected profile URL and completed same-origin iframe document before measuring controls. The complete browser matrix then verified 90 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
16. Publication audit found all eight kit markers and all eight site markers. Generated `skill/AGENTS.md` remained byte-stable at 22,519 bytes with body SHA `c64da837d302`.
17. Cross-artifact analysis covered 11 functional requirements, five success criteria, and 20 tasks with no critical finding or constitution conflict.

## Verification results

- Fine-pointer comfortable control height: 28 points.
- Fine-pointer compact control height: 22.96 points.
- Compact vertical row spacing: 1.64 points, with rendered consecutive-label gap no greater than 2 points.
- Touch, coarse, mixed, and unknown control target: at least 44 points in comfortable and compact densities.
- Text scaling: a 3x body scale grows the minimum control height beyond the normal fine-pointer value.
- Focused generator and native evidence: PASS.
- Full Python contract and compatibility evidence: PASS.
- Eight-kit production build and validation: PASS with zero reported problems.
- Release contract, site lint/build/test, browser WCAG verification, publication audit, capability probe, and generated-agent stability: PASS.
- Repository encoding, line-ending, generated-artifact exclusion, mojibake, and whitespace hygiene: PASS.
- Pull request, one Codex review round, and hosted CI: Pending.
