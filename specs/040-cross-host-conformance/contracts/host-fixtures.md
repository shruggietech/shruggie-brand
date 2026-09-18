# Contract: Executable Host Fixtures

## Browser/React

The generated browser specimen contains all fifteen recipes, exact version identities, profile metadata, state controls, accessible names and relationships, and AppFrame ownership. The public site embeds or renders only verified staged kit output. Playwright executes the profile matrix and axe scans, exercises keyboard and focus transitions, measures target and usable-content geometry, and captures ephemeral review candidates.

## Tauri Android ownership

The generated Tauri fixture is a small Rust test crate representing the Android WebView host-envelope boundary. It consumes the canonical known-bad and corrected traces without product composition. Tests prove single ownership, safe-area and display-cutout handling, IME obstruction, orientation, resize, and input transitions. The known-bad trace must fail for duplicate consumption and obstructed content. The corrected trace must pass with positive usable geometry and reachable required controls.

The fixture is `tauri-reference-host` evidence. It does not claim a packaged Android application, physical-device proof, or Glitchpad adoption.

## Wails Windows ownership

The generated Wails fixture is a small Go test module representing the Windows WebView2 window-envelope boundary. It consumes normal and narrow window traces with titlebar control regions, resize, keyboard, pointer, hover, and touch changes. Tests prove that fixed chrome and required controls avoid native control regions and remain reachable.

The fixture is `wails-reference-host` evidence. It does not claim a packaged Wails application or go-schedule adoption.

## Native egui

The conformance manifest references the generated egui crate and its locked `cargo test --locked` entry point. Existing `egui_kittest` evidence covers input, focus, selection, visible validation error, density, text scale, pixels-per-point scale, and unsupported host capabilities. The result is `egui-reference-renderer` evidence and cannot claim ESO Weave adoption.

## Tool absence

Generation never downloads tools. A fixture runner records an unavailable optional tool as pending proof with an actionable command. Release certification and issue closure require the authoritative CI environment to execute all declared reference fixtures; local absence cannot be mislabeled as success.
