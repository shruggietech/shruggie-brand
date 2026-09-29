# Tasks: DanceWithMe865 Brand Restart

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [identity and delivery contract](contracts/identity-and-delivery.md)

## Phase 1: Fresh source baseline

- [x] T001 [US1] Create `codex/065-dancewithme865-restart` in a separate managed worktree from `origin/main` and leave the prior S065 worktree untouched.
- [x] T002 [US1] Compare Natalie's image with the ZIP artwork; audit passive SVG safety and source hashes without adopting the archive layout.
- [x] T003 [US1] Stage byte-identical candidate SVG sources in `brands/dancewithme865/assets/source/`.

## Phase 2: General source contract support

- [x] T004 [US1] Add regression coverage for distinct authoritative Reduced colorway bindings and supplied standalone wordmark without rewriting supplied lockups in `skill/templates/test_brand_contract.py` and `skill/templates/test_pipeline.py`.
- [x] T005 [US1] Implement the smallest corresponding source-contract and generator changes in `skill/templates/brand_contract.py` and `skill/templates/gen_logo.py`.
- [x] T006 [US1] Verify selected SVG bytes remain unchanged and all generated logo families point to their reviewed source inputs.

## Phase 3: Gate 1 candidate

- [x] T007 [US1] Create pending standard `brands/dancewithme865/brand.json` source bindings, palette roles, and private authoring brief without transferring abandoned approvals or unverified ZIP claims.
- [x] T008 [US1] Complete formal palette qualification, including rendered contrast for the red 865 block, using the production renderer.
- [x] T009 [US1] Render the exact Full and Reduced 256, 64, 32, and 16 pixel proofs on dark, light, black, and white, then generate all four comparison artifacts per proof.
- [x] T010 [US1] Record source inventory, snapshot, renderer, framing, topology, proof hashes, and packet hash in a private Gate 1 proposal; present the light stacked source beside Natalie's image.
- [x] T011 [US1] Record the owner's approval of r1, its supersession after the private delivery check, and exact approval of revised candidate `dwm865-s065-g1-r2`.

## Phase 4: Gate 2 fundamentals

- [x] T012 [US3] Promote the approved canonical bytes and continuity record without redrawing or normalizing geometry.
- [x] T013 [US3] Assemble the standard wordmark, lockup, icon, palette, interface cue, typography, application, and distinct social image review surfaces.
- [x] T014 [US3] Record exact approved social wording, validate the private authoring brief and Gate 2 packet, and present measured derivatives for the owner's new exact Gate 2 approval.

## Phase 5: Standard delivery

- [x] T015 [US2] Compile the approved kit to ignored `dist/`; require zero `verify.py` problems and zero `validate_glyph.py` failures.
- [x] T016 [US2] Register the verified kit through existing `scripts/build_all.py` and `site/` source paths, including truthful independent-client ownership.
- [x] T017 [US2] Run the full documented aggregate and site validation; check UTF-8 LF, mojibake, generated-file exclusion, and branch diff.
- [x] T018 [US2] Update `specs/065-dancewithme865-brand/evidence.md` and changelog, then commit source-only work with a Conventional Commit subject. The owner explicitly authorized push and PR creation after the local commit.

## Dependencies

T004-T006 precede Gate 1 proofs because the production renderer digest binds generator code. T007-T010 precede T011. T012-T014 require T011 approval. T015-T018 require both owner approvals. A changed master returns to T007-T011; a changed derivative returns to T013-T014.
