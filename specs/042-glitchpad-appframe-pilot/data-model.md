# Data Model: Glitchpad AppFrame Adoption Pilot

## Pilot Adoption Record

| Field | Type | Validation |
| --- | --- | --- |
| `pilot_id` | string | Exactly `S042-glitchpad-appframe` |
| `upstream_issue` | URL | Upstream issue #219 |
| `downstream_issue` | URL | Glitchpad issue #196 |
| `upstream_revision` | full commit SHA | Candidate revision that generated the adopted bytes |
| `consumer_baseline_revision` | full commit SHA | `3d9a560...` baseline |
| `consumer_candidate_revision` | full commit SHA | Downstream PR head after adoption |
| `versions` | version map | Brand Canon, Interface Canon, recipes, Web adapter, compiler, and brand all required |
| `environment` | object | Renderer, host, Android targets, Windows target, viewport profiles |
| `evidence` | evidence map | Reference, Android actual-host, Windows actual-host, accessibility, fresh-session, handover |
| `observations` | observation list | All six common pilot classes required |
| `limitations` | string list | No empty or implied limitations |
| `status` | enum | `baseline`, `candidate`, `verified`, `blocked` |

### State transitions

`baseline` becomes `candidate` after exact kit import and consumer implementation. `candidate` becomes `verified` only after both repositories' required checks, Android consumer-host checks, Windows consumer-host checks, contract integrity, and evidence review pass. Any missing actual-host evidence, checksum mismatch, or review blocker moves the record to `blocked` until corrected.

## Pinned Consumer Contract

The existing generated schema remains authoritative. S042 changes these version values:

| Domain | Baseline | S042 candidate |
| --- | --- | --- |
| Brand Canon | `1.2.1` | `1.2.1` |
| Interface Canon | `1.0.0` | `1.0.0` |
| Component recipes | `1.0.0` | `1.1.0` |
| Web/React adapter | `1.0.0` | `1.1.0` |
| egui adapter | `1.0.0` | `1.0.0` |
| BrandBuilder compiler | `1.2.1` | `1.3.0` |
| Glitchpad brand | `1.1.0` | `1.1.0` |

The generated contract remains a candidate and unadopted upstream. Glitchpad's `INTEGRATION.json` and the pilot record establish the named downstream adoption without rewriting generated upstream lifecycle claims.

## AppFrame Layout Variant

| Field | Values | Rule |
| --- | --- | --- |
| `layout` | `contained`, `full-bleed` | Default is `contained`; unknown values are impossible through generated types |
| `host` | `browser`, `tauri`, `wails` | Selects responsibility profile, not operating-system behavior |
| `header` | optional React node | Shared frame position, product composition stays downstream |
| `children` | React node | Rendered inside the single main landmark |

`full-bleed` removes generated content max-width and gutters only. It does not expose class names, raw styles, route composition, or arbitrary layout values.

## Inset Ownership Map

| Responsibility | Glitchpad owner | Evidence |
| --- | --- | --- |
| Safe-area edges | AppFrame | Generated profile, DOM marker, computed geometry, known-bad mutation rejection |
| Dynamic viewport | AppFrame | `100dvh`, real WebView resize and orientation checks |
| Root scrolling | AppFrame | Body locked, one frame scroll root, document-local scrolling remains product composition |
| Fixed chrome | AppFrame boundary, Glitchpad content | Header slot inside governed safe geometry |
| IME obstruction | AppFrame environment bridge | VisualViewport measurement and real WebView keyboard check |
| Native titlebar regions | Tauri host | Explicit CSS custom-property handoff, zero duplicate Web padding |
| Global focus | AppFrame | Skip link, main target, visible focus, keyboard checks |

## Host Evidence Record

| Field | Required content |
| --- | --- |
| `evidence_class` | `reference-host`, `android-consumer-host`, `windows-consumer-host`, or `browser-consumer` |
| `consumer_revision` | Exact Glitchpad candidate SHA for consumer classes |
| `host` and `renderer` | Exact runtime names and versions where available |
| `target` | API level, ABI, Windows edition/build, and architecture as applicable |
| `profile` | Portrait, landscape, cutout, IME, narrow desktop, normal desktop, text scale, or input mode |
| `result` | `pass`, `fail`, `blocked`, or `unsupported` |
| `artifact` | CI job, log marker, report path, or receipt |
| `limitations` | Explicit list, never inferred from absent fields |
