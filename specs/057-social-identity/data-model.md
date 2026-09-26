# Data Model: S057

## Social copy

Each production brand owns `social_copy`: `slogan` (exact nonempty string), `layout` (`slogan-only` or `slogan-description`), `description_lines` (empty for slogan-only, at most three approved ordered strings otherwise), and `approval` (`approved_by`, `approved_on`, `source`). Validation rejects blanks, extra description for slogan-only, overlong layouts, and missing decision records. The generator measures outlined text against the canvas. A separate `social_image_approval` binds `approved_by`, `approved_on`, `source`, and exact assembled SVG and PNG SHA-256 values for all eight published brands.

## Mark role binding

Go-schedule `logo.paths.full` and `logo.paths.reduced` each contain exact copies of the former reduced array. Provenance records equivalent roles; the continuity snapshot hashes the current source. `current_mark_approval` binds the owner's new Gate 1 decision to that snapshot SHA-256, separately from the historical baseline. Older full geometry remains in Git history and is excluded from current outputs.

## Social delivery

Canonical vector: `logos/svg/<slug>-social-image.svg`; raster: `logos/png/<slug>-social-image-1280.png`. Compatibility aliases retain `social-preview` names. Provenance `kind: social-image` differs from lockup and alias records identify the canonical target. Downloads group them under Social images. Brand-page `/social/guidelines-<slug>.png` bytes equal the kit canonical PNG; unrelated route cards remain site-authored.
