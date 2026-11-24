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

This project opts into the `workflowy` skill and its private agent workspace.
Load the skill when available. Use the operator's project link or find this
repo or folder under **AI Agent Workspace > PROJECTS**. Reuse its branch or
insert it alphabetically. Search **STANDARDS** by title or topic tag. Read the
applicable rules, defaults, and scopes before governed work.

Use normal bullets for candid discussion, drafts, decisions, and evidence.
Never store work in Workflowy comments or comment drafts. Give `info` exactly
three direct children: `tags`, `links`, and `details`. Put purpose, current state,
next actions, blockers, and supporting evidence under `details`.
Use lowercase letters and underscores for reusable field names. Use inline
code for exact technical literals. Link to the exact canonical finding or evidence.
Git and the established tracker govern official progress where used.
Otherwise use the project artifacts. The operator decides what is published.

In `notes`, keep major sessions and substantive updates as a flat, oldest-first
list. Use only the ISO 8601 date or timestamp as the title. Retain the finest
supported precision and offset. Put the description, scope tags, and prose
under `title`, `tags`, and `details`. Use label-only field bullets with each
value or link nested in its own bullet. Require the Workflowy bullet format
for fields and values. Only the contents of `details` may use other formats.
Keep tags out of names and other fields. Use one hashtag per `tags` value.
Put any project-level tags in `info > tags`. Link related updates. The operator
owns timeline construction. Agents record dates without creating timeline
metadata, views, saved searches, or exports.

For Spec Kit, use one direct `spec-kit` bullet per formal slice in code order.
Use only its code and short title. Nest the verified date under `date` and
the documented epic under `epic` when applicable. Use the skill for shared
reference records, migration, and precise field rules.

Desktop MCP requires a running, signed-in Workflowy app with Local MCP
enabled and a connected client. A cloud or other nonlocal agent uses a
separately configured, operator-authorized connector when available. Confirm
the destination and read back writes. If no connector is available, continue
under the available instructions and provide an appropriately private,
ready-to-paste nested outline with its exact destination. Mark it unsynced.

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
