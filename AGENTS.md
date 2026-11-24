# Shruggie Brand Agent Instructions

## Source and artifact boundary

- Commit brand sources under `brands/`, shared fonts under `assets/fonts/`, generator code under `skill/`, and site source under `site/`. Create synthetic test inputs only in temporary test directories.
- Never commit generated kits, site exports, release archives, PDFs, raster exports, registries, or other contents of `dist/`.
- Make generator fixes in `skill/templates/`. Do not patch a generated kit to compensate for a generator defect.
- Never redraw or normalize shipped logo path data. Imported geometry remains byte-for-byte source data unless the owner explicitly approves an identity change.

## Required workflow

- Use the repository-installed Spec Kit workflow for features, architecture changes, generator changes, migrations, site behavior, CI, and releases.
- Specifications live under `specs/NNN-slug/`. Keep the specification, plan, tasks, verification evidence, and implementation in sync.
- `.specify/feature.json` is machine-local state and must never be committed.
- Prefer `codex/NNN-slug` branches and Conventional Commit subjects with the slice number when one exists.

## Workflowy

This project opts into the `workflowy` skill and Workflowy Desktop MCP for
substantive work. Load the skill when available. A running, signed-in desktop
app with Local MCP enabled and a connected agent session is required.

- Read **AI Agent Workspace → ABOUT** and locate the project under **PROJECTS**.
  Reuse its branch or insert it alphabetically. Use **PROJECTS → _general** for
  work without a named project. Confirm the destination before writing.
- Keep named projects in `info`, `notes`, and `spec-kit` when the project uses
  Spec Kit. Keep `info` current and link its claims to evidence. Use `notes` for
  candid drafts, decisions, questions, and sessions in chronological order.
  Start each major session and substantive update title with one local
  ISO 8601 timestamp and its offset, followed by a short fragment. Keep
  updates and replies with their session or discussion.
- Put each formal slice directly under `spec-kit` in code order. Its title
  contains only the formal code and short title, like `S094 Check source order`.
  Add a `Date` child and an `Epic` child when applicable. Put scope, outcome, and
  links in children. Use the native Workflowy date and project hashtag
  together on the timeline child for dated records.
- Find the existing record by meaning and source before writing. Link to
  the exact finding or authoritative Git, tracker, or project artifact.
  Add new evidence or a delta in place and preserve the original node ID.
  Follow ABOUT for shared catalog fields, alphabetical order, and link roles.
- Keep private work with the operator and their authorized agents. The
  operator decides what is published. Read back MCP edits and check titles,
  parents, order, links, dates, and duplicates. If MCP is unavailable,
  continue the work and report what still needs to be saved.

## Quality gates

- WCAG 2.1 AA is a non-exemptable floor. Fix failing values instead of adding waivers.
- A kit is shippable only when `verify.py` reports zero problems and `validate_glyph.py` reports zero failures.
- Do not byte-compare generated PDFs or PNGs. Verify measured behavior and declared gates.
- Run the full documented validation before claiming a change is complete.

## Files and prose

- Save text as UTF-8 without BOM with LF line endings.
- Check downloadable artifacts and text for mojibake before delivery.
- Avoid em dashes in authored prose. Use commas, parentheses, or hyphens.
- Keep Markdown prose paragraphs on one physical line unless Markdown syntax requires a break.
- Use top-to-bottom Mermaid layouts when a diagram is materially useful.

## Windows command execution

- Foreground, flashing, and focus-stealing console windows are prohibited.
- Use non-interactive commands with redirected output. Project-owned child-process launchers must set `CREATE_NO_WINDOW` or an equivalent hidden-process guarantee.
- Invoke `git` and `gh` directly through the Codex command runner. Do not wrap them in another shell solely for repository operations.
