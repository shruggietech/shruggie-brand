# Research: Glitchpad AppFrame Adoption Pilot

## Decision 1: Add a bounded full-bleed AppFrame layout

**Decision**: Add `full-bleed` beside the existing contained AppFrame layout and emit the selection as a governed data attribute with generated CSS. Keep contained layout as the default.

**Rationale**: Live Glitchpad inspection shows that its application shell is a full-height grid with product-owned chrome and document surfaces. The generated AppFrame currently always centers and pads main content, forcing a consumer to override governed CSS or reconstruct the shell boundary. A named bounded variant expresses a recurring application-shell need without adding raw style props or moving product composition upstream.

**Alternatives considered**:

- Override generated padding and max width in Glitchpad CSS. Rejected because it creates the permanent local approximation the pilot is required to eliminate.
- Move Glitchpad's shell grid into BrandBuilder. Rejected because tabs, panels, and document composition belong downstream.
- Make every AppFrame full-bleed. Rejected because it would break the existing contained document behavior and require a major version.

## Decision 2: Split environment observation from optional headless controls

**Decision**: Generate `web/react/environment.tsx` containing `measureImeBlockEnd` and `AppFrameEnvironmentBridge`, then re-export those symbols from the existing client entry for compatibility.

**Rationale**: Glitchpad needs viewport and IME observation but does not need to adopt Radix controls in this slice. The current client entry imports `radix-ui` at module load, so using only the bridge imposes an unrelated dependency. A dependency-free entry preserves the existing client API while improving package boundaries for Vite and host consumers.

**Alternatives considered**:

- Add `radix-ui` to Glitchpad only to reach the bridge. Rejected as unnecessary dependency expansion.
- Copy the bridge into Glitchpad. Rejected as duplicate shared behavior.
- Move the bridge into the server entry. Rejected because it uses browser effects and must remain client-only.

## Decision 3: Vendor exact generated kit bytes downstream

**Decision**: Use Glitchpad's existing `scripts/sync-brand-kit.mjs` artifact import path against the successful upstream candidate workflow, recording the full upstream commit, workflow run, artifact ID, source manifest digest, integrated manifest digest, and governed file count.

**Rationale**: Glitchpad already treats `brand/manifest.json` and `brand/INTEGRATION.json` as the immutable kit and receipt boundary. Reusing that path provides checksum verification, deterministic legal-link handling, exact platform asset copies, offline guidance, and fresh-session discovery without inventing a second package manager.

**Alternatives considered**:

- Copy only AppFrame files. Rejected because partial copying breaks the consumer manifest and provenance graph.
- Fetch a future release or latest artifact. Rejected because the pilot must pin exact candidate bytes and cannot cut a release.
- Reference upstream source files directly from the consumer checkout. Rejected because it breaks offline handover and repository isolation.

## Decision 4: Use real existing consumer-host CI

**Decision**: Extend Glitchpad's existing Android `ActivityScenario` and WebView JavaScript instrumentation to inspect the adopted shell in API 24 and API 36 emulators, including a system display-cutout overlay where the platform supports it. Use the existing Windows desktop Tauri build and shell-layout smoke as the desktop actual-host boundary.

**Rationale**: These paths already build and execute the real Glitchpad consumer target. They can produce actual-host evidence without introducing a toy app or mislabeling browser simulation as adoption.

**Alternatives considered**:

- Treat upstream Tauri reference tests as consumer proof. Rejected by issue #219 and the conformance contract.
- Use only jsdom or Chromium viewport emulation. Rejected because neither executes Android WebView nor Windows Tauri.
- Require a local physical Android device. Rejected because the repository already defines hosted real-emulator acceptance and the local environment may lack compatible SDK state.

## Decision 5: Record prospective baseline limitations

**Decision**: Record code-derived baseline facts and observation counts available from this session, state that historical elapsed time and correction-round history cannot be reconstructed reliably, and collect comparable post-adoption measurements from the authorized S042 work.

**Rationale**: The common pilot protocol explicitly prohibits invented savings. A prospective baseline is honest, repeatable, and still useful for identifying repeated local exceptions and escaped defects.

**Alternatives considered**:

- Infer historical rounds from old pull-request comment counts. Rejected because comments do not map reliably to the same task scope.
- Omit the missing fields. Rejected because the protocol requires each observation class and a stated limitation.

## Decision 6: Publish two coordinated pull requests

**Decision**: Open one upstream PR and one downstream PR, link them bidirectionally, and present an ordered merge ritual with upstream first.

**Rationale**: The changes have different ownership, validation, and issue-closing boundaries. Glitchpad pins the upstream candidate commit, so upstream must merge first while the exact commit and generated checksums remain stable.

**Alternatives considered**:

- Put all changes in one repository. Rejected because it would violate the architecture boundary.
- Delay the downstream PR until after upstream merge. Rejected because it would prevent the requested end-to-end pilot and actual-host review in one session.
