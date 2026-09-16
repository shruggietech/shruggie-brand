# Verification Evidence: Embed Specimen Logo

## Traceability

- Slice: S034
- Issue: [#204, I Heart PR Tours specimen missing embedded logo](https://github.com/shruggietech/shruggie-brand/issues/204)
- Branch: `codex/034-embed-specimen-logo`
- Baseline revision: `71ef159`
- Acceptance source read from GitHub on 2026-09-15.

## Baseline reproduction

- Ran `skill/templates/build_specimen.py` against an isolated temporary copy of the I Heart PR Tours source and shared fonts.
- The generated specimen succeeded syntactically but emitted both `href="../assets/source/vertical_darkbg.svg"` and `xlink:href="../assets/source/vertical_darkbg.svg"`.
- This reproduces the issue's broken published resolution while keeping synthetic and generated material outside the repository.

## Identity baseline

| Item | Baseline |
| --- | --- |
| `brands/i-heart-pr-tours/assets/source/vertical_darkbg.svg` SHA-256 | `bcd03c0784b442a2c38836f9b2e6c312149a9cc1bddd3c1480fae28ea9b5f045` |
| `brands/i-heart-pr-tours/assets/source/horizontal_darkbg.svg` SHA-256 | `2f50fcafa8a422ad0271e583108b79e4ace6065445b0f4615d96fa8f822ab7f3` |
| `brands/i-heart-pr-tours/brand.json` SHA-256 | `da5bbe93ac85b8b19e8e0bbc5f51075d32647b04871fdec2df681bc4373ac49f` |
| Full mark element | `image` |
| Full mark source | `assets/source/vertical_darkbg.svg` |
| Full mark placement | `x=94.125`, `y=57.375003123`, `width=186.75`, `height=260.249993754` |
| Logo grid | `375` |
| Specimen header placement | `translate(66,66)`, height `170`, uniform scale `170 / 375` |

No authoritative source file, source hash, brand path entry, component geometry, color, transparency, or approval record is authorized to change. The later owner correction authorizes only selecting and centering a different already approved source in generated specimen output.

## Owner correction: wider stacked lockup

- After reviewing the initial portable specimen, the owner asked why the canonical full mark was used and requested the wider stacked version instead.
- The initial selection followed the pre-existing `logo.paths.full` contract, whose single image component points to `vertical_darkbg.svg`. That choice was mechanically correct for the original contract but was not the best header treatment once the owner stated the intended use.
- The governed brand source already declares `supplied_lockup_input_ids.horizontal.color` as `horizontal-dark-lockup`, an approved authoritative lockup at `assets/source/horizontal_darkbg.svg` with `embed-unchanged` and `resize` permissions. No new approval, asset, or brand-source edit was needed.
- An attempted specimen-only brand setting was rejected during development by the existing stale-derivative and source-inventory gates. The final design instead derives selection from the existing approved lockup declaration in the shared contract.
- The wider-lockup regression failed before implementation because the generated payload decoded to the vertical source. After implementation, generic and production tests prove approved horizontal selection, exact bytes, centered native proportions, and unchanged full/reduced fallback behavior.

## Environment

- Repository-local Python 3.12 virtual environment created from the bundled workspace runtime.
- Repository-pinned Python dependencies installed into ignored `.venv/`.
- Exact minimum-version dependencies installed into ignored `.venv38/` with managed Python 3.8.20.
- Site dependencies installed from the frozen lockfile into ignored `site/node_modules/` with repository-pinned pnpm 10.28.2. The package manager reported its expected ignored-build-script policy for `esbuild`; lint and production build subsequently passed.
- The approved proof renderer used Node.js 24.11.0 and `@resvg/resvg-js` 2.6.2. Playwright Chromium was installed for direct hosted, offline, PDF, and site rendering.
- The repository has no authentication, private data, mutable user input, or tenant boundary. S034 security evidence covers contained source resolution, fail-closed media types, self-contained URI references, and publication provenance.

## TDD evidence

- Added isolated image-backed specimen regressions before changing generator or verifier behavior.
- Focused pre-implementation run exited 1 as expected:
  - generated output had no stable `specimen-mark` group;
  - `verify.py` had no specimen portability/rendered-pixel gate;
  - the site publication module had no byte-equivalence helper for specimen copies.
- The first publication test invocation also documented the required direct-script import context; subsequent focused runs use the repository's documented script entry point or an explicit `PYTHONPATH=scripts` equivalent.

## Focused verification

- The focused specimen tests pass after implementation. The synthetic fixtures prove identical `href` and `xlink:href` data payloads, exact decoded bytes, governed horizontal-lockup preference, unchanged canonical fallback geometry, centered native proportions, contained path resolution, actionable rejection of a relative dependency, and rejection of a blank rendered mark.
- `scripts/test_prepare_site.py` passes 31 tests, including deliberate post-copy corruption that raises `hosted specimen differs from the verified kit specimen`.
- The repaired production specimen contains two self-contained data references, one stable `specimen-mark` group, one image component, identical modern and legacy links, and no relative, filesystem, or network reference.
- The final decoded production payload SHA-256 is `2f50fcafa8a422ad0271e583108b79e4ace6065445b0f4615d96fa8f822ab7f3`, exactly matching the approved `horizontal_darkbg.svg` bytes.
- Final generated serialized placement is `x=39`, `y=95.625`, `width=297`, `height=183.75`, `preserveAspectRatio=xMidYMid meet`, inside the unchanged `translate(66,66) scale(0.453333)` header transform. The shared helper preserves the source's `297` by `183.74999559` native proportions and centers it within the existing `375` grid.
- The terminal all-kit build's `verify.py` report contains 25 checks, zero skips, and zero problems. Its specimen rows report `2 references self-contained; 1 image sources byte-exact` and `3056 non-background pixels` in the mark region.
- Direct `validate_glyph.py` reports 4 checks, 4 documented imported-geometry warnings, and 0 failures. The warnings state that owner-approved SVG bytes are preserved unchanged and native image elements are not redrawn by the filled-path measurement gate.

## Full validation

- Python 3.12: all 231 unit tests across publication workflow, packaging, release contract, site preparation, identity audit, brand contract, identity continuity, icon generation, and the 67-test pipeline passed. The Windows-only unprivileged symlink case skipped as declared. `test_glyphkit.py` passed 34 checks with zero failures. An initial pipeline invocation inherited host Node 24.11.1 and correctly rejected renderer drift; the authoritative rerun with repository-pinned Node 24.11.0 passed all 67 tests.
- Python 3.8.20: `compileall`, eight-kit discovery, the same minimum-version CI test matrix, and Markdown policy passed. The 67-test pipeline passed at the CI-style core capability tier with the existing exact-raster derivation test skipped because `GP_NODE` intentionally named an unavailable renderer.
- Full capability probe completed at the `full` tier with Pillow, fontTools, coloraide, pikepdf, Playwright, and launchable Chromium.
- `scripts/build_all.py` built all 8 production kits with zero reported problems. Every kit completed its verifier, glyph, image-QC, PDF-QC, pagination, and manifest gates; I Heart PR Tours reported 434 manifest-covered files.
- Release packaging emitted and verified 9 v1.2.1 assets plus validated generated notes.
- `sync_agents_md.py` reported `unchanged AGENTS.md (18392 bytes, body sha 8ab27545f9c4)`.
- Pinned pnpm 10.28.2 site lint passed, the Next.js production export generated 81 static pages, and the site test passed 12 Node contract tests plus 76 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- The browser verifier passed direct hosted navigation with HTTP 200 and SVG MIME, local `file:` navigation, self-contained reference enumeration, exact embedded SVG links, and visible non-background pixels for the exact published I Heart PR Tours artifact.
- `audit_publication_artifacts.py --kits dist --site site/out` reported 8 governed kit markers and 8 governed site markers.
- The post-correction Spec Kit analysis found zero critical, high, medium, or low consistency findings: all 17 functional requirements and 8 measurable success criteria map to the 36-task ledger, the constitution remains satisfied, and no placeholders or unmapped owner-correction work remain.

## Final identity and hygiene evidence

- Authoritative source SHA-256 after implementation remains `bcd03c0784b442a2c38836f9b2e6c312149a9cc1bddd3c1480fae28ea9b5f045`.
- Authoritative horizontal lockup SHA-256 after implementation remains `2f50fcafa8a422ad0271e583108b79e4ace6065445b0f4615d96fa8f822ab7f3`.
- Authoritative `brand.json` SHA-256 after implementation remains `da5bbe93ac85b8b19e8e0bbc5f51075d32647b04871fdec2df681bc4373ac49f`.
- The verified kit specimen and hosted specimen both have SHA-256 `be500f3d4a8aeb3d3c39251827b4077d446863d57e9c5b3950e7064315ed9479`.
- No file under `brands/i-heart-pr-tours/`, no shared font, and no authoritative identity record is modified. The implementation changes governed templates, tests, publication enforcement, site verification, changelog, and S034 records only.
- Generated kits, site exports, proof matrices, release archives, browser screenshots, virtual environments, package dependencies, and synthetic fixtures remain ignored and uncommitted.
- Markdown policy passes. Final LF/UTF-8, mojibake, whitespace, ignored-artifact, staged-file, and clean post-commit checks are recorded by the pre-commit closeout.
