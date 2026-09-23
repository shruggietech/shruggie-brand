# S048 Verification Evidence

## Consumer attribution (2026-09-23)

- ESO Weave `src/app/ui.rs:2685` renders `Capture Unavailable` with `ui.strong(history_diagnostic_heading(...))`, not a disabled button. `src/app/theme.rs:165-180` sets active widget foreground to `on_primary`, black in dark theme. egui 0.36.1 `Visuals::strong_text_color()` reads active widget text color, bypassing the ordinary text override. ESO has a local `label_strong` helper in `src/app/widgets.rs:329-343` that uses palette text, but this call site does not use it. The application correction is downstream and is not claimed by this PR.
- ESO Weave `build.rs:218-223` and WiX `wix/main.wxs:114` use `assets/icon.ico`. Its SHA-256 is `3b3830fb98662d7e1fb0277e38d94072bfc67f9eac81a2f03433e6f11ee3c20a`, matching the pinned BrandBuilder adoption record. The local debug EXE's RT_GROUP_ICON has 16, 24, 32, 48, 64, 128, and 256-pixel frames; each embedded frame matches the corresponding ICO frame. Every frame has an opaque `#0E1116` top-left pixel. This is a BrandBuilder-generated backplate; actual OS scale selection remains unobserved.
- Official Glitchpad v0.1.3 ARM64 APK SHA-256 is `543e4210a84de2d3a8996e94da242bcbd379dec655fa27519ac7023296202fca`. Its manifest declares `android:icon=@mipmap/ic_launcher` and no `android:roundIcon`. API 26+ maps the icon to adaptive XML with foreground, background, and monochrome layers. The foreground is 432 square with yellow bounds (84,84)-(347,347), within 66/108 safe content; background is opaque `#0B0C0D`. The legacy mdpi icon is 48 square, fully opaque dark with yellow bounds (6,6)-(40,40). Thus generator composition explains the dark wedge. The specific Android details viewer's runtime selection was not directly observed. The APK predates the current BrandBuilder pin, so a new kit alone will not change that installed APK.

## Approval-bound implementation decisions

- Glitchpad's source already approves sulfur `#FFD900` as its square-enclosure frame role. The generator derives the adaptive and maskable background from that role, keeping the continuity snapshot and imported paths unchanged.
- ESO Weave's Gate 1 derivative approval rejects a new `windows_unplated` brand field. The generator instead applies the general taskbar policy for a mark without an approved square enclosure; ESO's source approval record stays intact. Tile and Store roles keep their plated policy.
- I Heart PR Tours proof qualification compares all 32 approved raster proofs exactly. Its historical renderer fingerprint included the entire iconkit module; S048 retains that fingerprint only while the proof-used functions and top-level module setup AST are unchanged. A proof-function or setup edit returns the live source hash and causes the approval gate to fail.

## Gates

- Focused Python contract and unit suites: 245 tests passed. The full pipeline suite passed 70 tests after the final native adapter source correction.
- Generated ESO Weave egui adapter: 11 Rust tests passed with pinned egui 0.36.1. The generated paint-shape test checks actual disabled-label vertex alpha and 4.5:1 contrast in both themes, plus strong status, hover, focus, and enabled roles.
- `scripts/build_all.py`: eight production kits built cleanly with zero verifier problems and zero glyph failures. The affected ESO Weave, Glitchpad, and Shruggietech logo and desktop/mobile page sheets were opened and inspected; ESO's transparent taskbar composite was also inspected on a light surface.
- Candidate v2.0.3 packaging and `release_contract.py verify`: nine assets and generated notes verified. No tag or release was published.
- Pinned Node 24.11.0 and pnpm 10.28.2 site lint and 95-page production build passed. The final clean-rebuild site test passed 12 Node tests and verified 90 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- `check_markdown.py`, `audit_public_documentation.py --sources`, generated-agent-contract sync, and `git diff --check` passed. No BOM or common mojibake markers found in changed prose; tracked changed text uses LF. Approved logo path data was not edited.
- PR #258 opened at `https://github.com/shruggietech/shruggie-brand/pull/258` from commit `be98870`; external CI and bot reviews are running.

## Review ledger

- PR #258 was opened at `be98870`; the automatic Codex code review is round one. Maximum two Codex review rounds, including any manually requested second round.
- The first PR CI run exposed a Python 3.8-only fingerprint mismatch: `ast.dump()` produced version-dependent proof-helper serialization. S048 replaced that internal compatibility fingerprint with exact source segments, leaving the mandatory 32-image approval comparison intact. The 23 identity continuity tests pass locally after the correction; CI rerun and bot reviews remain pending.
