# Research: Cueson Brand Kit

## Decision 1: Freeze current repositories without disturbing the Cueson worktree

**Decision**: Use Shruggie Brand `origin/main` commit `d50317f6acdf4d4492c3b25cdcd7bb3ec7a29ab9` and Cueson `origin/main` commit `d66d6a0cca92fc0a62f0e26df0ec5b9460ef22d6` as the Gate 1 S026 evidence snapshot. The Cueson remote advanced from the initial planning revision `29038240d0528165510b1e4a5d77d202e62e2d45` during proposal preparation, so the study was regenerated against the refreshed revision. Re-fetch before each approval gate and leave the neighboring Cueson checkout on its current user branch.

**Rationale**: Both remotes were fetched on 2026-09-09. Recording remote objects supplies current evidence without switching, merging, or modifying the user's active Cueson worktree.

**Alternatives considered**: Switch Cueson to `main` (disturbs unrelated work); use the local feature-branch head as product authority (not the default branch); rely on issue-intake hashes without re-fetching (stale-prone).

## Decision 2: Derive the brief from product authority and exclude intake styling

**Decision**: Ground the identity in Cueson's ratified README, architecture, schema, CLI contract, working project specification, representative Cue JSON, and media-format guide. Treat the three explainer images only as evidence that Cueson makes timed language directly addressable while preserving original text, XML, binary, or bitmap sources and keeping OCR derived rather than authoritative.

**Rationale**: The source documents consistently define the differentiator as a lossless common interchange layer, not a caption editor, transcription brand, or visual subtitle styling tool. The operator explicitly excluded every visual characteristic of the screenshots.

**Alternatives considered**: Match the screenshots' black, green, and orange presentation (disallowed); emphasize AI transcription (misstates current scope); use a generic accessibility badge (does not express interchange or source preservation).

## Decision 3: Present four materially different concept directions

**Decision**: Gate 1 will compare four directions:

1. **Cueframe (recommended)**: Opposing timing brackets preserve an outer source envelope while three measured cue rails expose structured content. The open bracket terminals prevent the form from becoming a closed-caption badge, and the reduced form keeps the bracket-to-rail relationship.
2. **Parallel Source**: Two offset caption plates, one preserved outline and one normalized fill, express original and common representations traveling together. It is immediately readable but risks generic layers or copy symbolism.
3. **Timing Spine**: Staggered cue rails attach to one exact vertical timing datum. It strongly communicates timed structure but says less about lossless source preservation.
4. **Interchange Aperture**: Four open corner gates align around a central cue, expressing multiple formats meeting one addressable surface. It is compact but risks resemblance to crop, focus, or scanning symbols.

**Rationale**: The set explores container, paired representation, timing, and many-to-one interchange as separate visual hypotheses. Cueframe covers the most product truth with the fewest elements and retains a strong silhouette at small size.

**Alternatives considered**: A `CC` badge (generic and associated with the conventional closed-caption symbol); an AI sparkle (misstates the product); a play triangle (media playback rather than content interchange); literal arrows between file icons (diagram, not durable identity); a speech bubble (conversation rather than structured subtitle data).

## Decision 4: Recommend the Cue Iris color system

**Decision**: Recommend a cool ink and periwinkle system led by Cue Iris `#8D98FF` on Archive Night `#080A14`, with accessible light-surface Iris Deep `#5360D6`, Paper `#F7F8FC`, Ink `#14172A`, Card `#101425`, Secondary `#181D33`, Hover `#222944`, dark muted text `#A7AEC7`, and dark primary text `#F4F6FF`. Retain inherited ShruggieTech orange only for scarce emphasis and warning semantics, never as the Cueson identity accent.

**Rationale**: Indigo-periwinkle suggests an intermediary technical layer without leaning on the green/orange screenshots, cyan-heavy capture tooling, or the conventional black-and-white `CC` badge. The initial measured pairs are 7.58:1 for Cue Iris on Archive Night, 5.23:1 for Iris Deep on white, 8.95:1 for muted text on Archive Night, and 18.30:1 for primary text on Archive Night. Separating identity iris from inherited orange, success green, and failure red keeps identity and state semantics distinct.

**Alternatives considered**: Bright cyan (too close to Fragcap and capture-tool conventions); green (too visually close to the excluded explainer styling and success semantics); orange or coral (too close to ShruggieTech identity and warning/failure roles); purple-magenta (too close to Covarity); grayscale only (does not provide a distinct portfolio identity).

## Decision 5: Use house typography and approve its identity application at Gate 2

**Decision**: Use the existing ShruggieTech house families, with an outlined Space Grotesk Bold wordmark, Geist for prose, and Geist Mono for Cue JSON, timecodes, hashes, and format labels. Gate 1 does not approve wordmark construction; Gate 2 approves the exact outlined wordmark, spacing, and lockups.

**Rationale**: Cueson is ShruggieTech-owned, the house font contract is already licensed and delivered locally, and the technical mono role is directly useful. The iris palette and glyph carry product distinction while shared typography maintains portfolio kinship.

**Alternatives considered**: Introduce a new fixed family (adds license and asset scope without evidence); set the wordmark in live text (not portable identity geometry); use a subtitle-display face (overstates media presentation and weakens infrastructure credibility).

## Decision 6: Extend approval-ledger validation narrowly for a constructed identity

**Decision**: Reuse the existing approval ledger and derivative-configuration fingerprint. Permit an empty `source_hashes` object only when `logo.source_mode` is `constructed` and no approved imported mark source exists. Continue requiring exact imported-source hashes for authoritative logos. Store the richer candidate identifiers, proposal hashes, displayed evidence, owner wording, scope, and timestamp in S026 approval evidence, while `brand.json` carries the compatibility ledger and configuration fingerprint.

**Rationale**: A new constructed brand has no pre-existing authoritative image to hash. The derivative-configuration fingerprint already binds the approved palette, typography, and geometry that produce outputs. Allowing a fabricated source hash would be dishonest; removing approval validation would fail closedness.

**Alternatives considered**: Commit a proposal screenshot as the authoritative mark (wrong authority); fabricate a pseudo-source record (invalid provenance); redesign the ledger broadly (unnecessary architecture); omit the ledger for an owned brand (cannot enforce issue #184's two gates).

## Decision 7: Generate proposal evidence deterministically under ignored output

**Decision**: Add `scripts/cueson_identity_study.py` and focused tests. The script emits four vector concepts, exact 256/64/32/16 pixel light and dark proofs, single-ink samples, palette swatches, contrast and geometry measurements, rationale, resemblance risks, recommendation, hashes, and contact sheets beneath `dist/.s026-cueson-study/`. It must refuse missing metadata or unacknowledged threshold failures.

**Rationale**: A deterministic study is reviewable, repeatable after feedback, testable before approval, and safely excluded from production discovery. It avoids relying on transient chat-only images as the sole decision evidence.

**Alternatives considered**: Hand-edit proposal images (not reproducible); use generated kit discovery before approval (could publish speculative identity); provide prose only (insufficient visual decision evidence).

## Decision 8: Bind Gate 2 to the generated derivative manifest and exact public surfaces

**Decision**: After Gate 1, generate the current derivative families and record their approval manifest hash. Gate 2 approves the exact manifest and the complete existing public surface set. Any producing-configuration or manifest drift makes approval stale and disables public showcase.

**Rationale**: Wordmark spacing, platform masks, reduced geometry, and copy compositions can fail even when the master glyph is sound. A second exact gate prevents an approved idea from becoming an unreviewed delivery.

**Alternatives considered**: Treat Gate 1 as approval of all future derivatives (too broad); approve only contact-sheet pixels (weak source traceability); publish privately before approval (violates issue #184).

## Decision 9: Keep Cueson import and domain activation outside S026

**Decision**: Produce a hash-addressed consumer handoff manifest, but do not modify `A:\Code\cueson`, open a Cueson integration pull request, activate `cueson.io`, or change DNS or Cloudflare. Those actions require later Cueson and post-v1 workflows.

**Rationale**: Cueson's own roadmap reserves external brand creation and requires a later approved import. It also makes public-domain activation a separate post-v1 slice.

**Alternatives considered**: Copy assets into Cueson during Gate 2 (crosses repository authority); redirect the dormant domain to the brand portal (unauthorized production mutation); omit handoff details (creates ambiguous future integration).

## Decision 10: Use the authorized two-round review protocol without a pre-push halt

**Decision**: After both gates and local verification, push and open the official pull request automatically. Process automatic Codex, security-bot, CI, and human feedback. If needed after first-round findings are resolved, request one second Codex review with `@Codex review`; never request another. Halt for the owner only when required checks are green and all received review items are resolved or accurately documented as non-actionable.

**Rationale**: This is the explicit exception granted in the kickoff. It preserves external review and human-only final merge authority while removing only the usual pre-push pause.

**Alternatives considered**: Halt before push (contradicts explicit authorization); merge after review (not authorized); repeatedly request reviews (explicitly prohibited).

## Decision 11: Treat identity-source safety as the security boundary and tenancy as inapplicable

**Decision**: Exercise the existing passive-SVG, contained-path, network-reference, generated-output, dependency, and repository-hygiene protections against all new Cueson identity data. Record tenancy as inapplicable because S026 introduces no authentication, accounts, user data, shared runtime, or tenant-partitioned state.

**Rationale**: Security coverage must follow the actual attack and integrity surfaces. Inventing tenant tests for a static source generator would be false assurance, while SVG and path safety, output containment, dependency scanning, and review-bot findings are concrete risks.

**Alternatives considered**: Declare all security testing irrelevant (misses passive content and path boundaries); add artificial tenant fixtures (no governed behavior to test); add runtime sandbox architecture (outside scope).

## Post-approval sibling-identity collision

**Decision required**: The private kit build found that approved Cue Iris `#8D98FF` sits 24.0 OKLCH hue degrees and 12.23 CIEDE2000 from go-schedule Anchor Blue `#58A6FF`. The current canon requires at least 30 hue degrees between sibling identity accents. Preserving the exact approved color would therefore require an architecture-level change to the family distinctness contract; retaining the current canon requires a new Gate 1 palette revision.

**Feasible current-canon regions**: Existing sibling accents leave only a narrow teal region around 184 degrees and a magenta region around 350 degrees. The fully tested teal pair is `#62BEB2` on `#080A14` with `#005D55` on `#F7F8FC`; the more saturated initial teal pair failed the tritanopia simulation against success green and was rejected before owner presentation. The representative magenta pair is `#E97AB2` on `#080A14` with `#9E366F` on `#F7F8FC`. Both surviving pairs clear contrast, sibling-hue, and color-vision gates, but either is a material identity change requiring owner approval.

**Alternative considered**: Lowering the hue threshold, hiding Cue Iris in a secondary token, or adding a one-brand waiver was rejected because each would weaken or evade a non-exemptable quality gate.

### Resolution: approve Cue Teal revision 1

**Decision**: Retain the exact approved `cueframe-r1` geometry and replace the superseded Cue Iris palette with owner-approved `cue-teal-r1`: `#62BEB2` on Archive Night and `#005D55` on Paper.

**Rationale**: Cue Teal passes 8.96:1 dark-surface and 7.34:1 light-surface contrast, retains at least 31.3 OKLCH hue degrees from sibling identity accents, and passes the declared simulated color-vision distance threshold. The owner approved the exact deterministic demo after rejecting the warm-magenta alternative.

## External Landscape Notes

- The conventional closed-caption symbol is commonly represented as two `C` characters in a screen-like enclosure, so S026 avoids badge geometry and `CC` lettering: https://fontawesome.com/icons/classic/solid/open-captioning
- Major caption products emphasize transcription, editing, accessibility, and multi-format export. Cueson's preservation-first interchange position is narrower and should remain visually distinct from creator-tool branding: https://www.closedcaptioncreator.com/ and https://www.telestream.com/captions/
- A search for the exact `Cueson` software and subtitle identity found no evident existing product mark at intake. This is a collision screen, not trademark clearance.
