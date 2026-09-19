# Contract: Glitchpad AppFrame Adoption

## Upstream obligations

1. Generate AppFrame with a backward-compatible `layout="full-bleed"` option while preserving contained layout as the default.
2. Generate a dependency-free React environment entry for IME and VisualViewport observation and preserve current client re-exports.
3. Declare the new entry and version values in adapter, consumer, documentation, release, recovery, and provenance records.
4. Reject unsupported layout values, version disagreement, missing entries, source drift, duplicate inset ownership, and invalid host evidence.
5. Rebuild and verify every production brand with no identity changes and no committed generated output.

## Downstream obligations

1. Import the complete verified Glitchpad kit from the exact upstream candidate revision through the repository's existing importer.
2. Keep generated kit files immutable and consume AppFrame, its environment bridge, tokens, and component styles directly from `brand/`.
3. Render Glitchpad's application menu and tab strip through the AppFrame header boundary and keep document surfaces and overlays downstream.
4. Declare `viewport-fit=cover`, select the Tauri ownership profile, and apply no native safe-area content padding that duplicates AppFrame.
5. Extend unit, browser-shell, Android WebView, and Windows host checks so bypassing the generated shell or duplicating ownership fails.
6. Record the exact consumer revision, target details, CI evidence, observations, fresh-session result, handover contents, and limitations.

## Evidence boundaries

- Upstream browser and Tauri fixtures prove generated contract behavior only.
- Glitchpad Vitest and Chromium shell checks prove consumer browser composition only.
- Glitchpad API 24 and API 36 ActivityScenario/WebView instrumentation proves Android consumer-host behavior.
- Glitchpad Windows Tauri build and lifecycle smoke proves Windows consumer-host behavior.
- No evidence class may populate another class's slot.

## Failure conditions

Adoption fails when any of the following is true:

- exact imported bytes do not match the upstream artifact manifest;
- the consumer uses an unpinned latest version or lacks offline recovery;
- safe-area, IME, titlebar, root-scroll, fixed-chrome, or focus ownership is absent or duplicated;
- a required control leaves usable geometry in any declared profile;
- AppFrame is bypassed by the production application root;
- product composition is copied upstream or generated contract files are patched downstream;
- Android or Windows actual-host evidence is missing but reported as complete;
- WCAG 2.1 AA, identity, verification, encoding, mojibake, or repository-hygiene gates fail.
