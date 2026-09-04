# Portability

**This skill has to produce the same kit on Claude, on Codex, and on a bare
checkout with nothing installed. Every rule here exists because one of those
three broke.**

## The capability model

Do not assume. Probe once, at the start, and record what you found:

    python3 templates/probe.py

It prints a capability block and writes `<kit>/qc/probe.json`. Everything
downstream routes off that. A missing tool gets named in `VERIFY.md` as a skip
with a reason; it never gets silently substituted, and it never gets quietly
skipped.

Three capability tiers, and what each can still finish:

| Tier | What is present | What you get |
| --- | --- | --- |
| **Core** | Python 3.8+ and its standard library. Nothing else. | brand.json, all tokens, the Next.js binding, enforcement, the guidelines page, the specimen, the manifest, `verify.py` and the full glyph gate |
| **Raster** | Core, plus a rasteriser and Pillow for required compositing | Everything above, plus PNG exports and the favicon set; a measured ICO writer adds the multi-entry `.ico` |
| **Full** | Raster, plus headless Chromium | Everything above, plus the brand guide PDF and the QC contact sheets |

**The Core tier must always succeed.** If a step cannot run at Core, it is
written wrong. That is why `validate_glyph.py` carries its own rasteriser and
why no gate depends on an agent being able to view an image.

## Vision is a bonus, never a gate

The house rule is still "look at every rendered artifact before shipping it",
and an agent that can see images must still open the contact sheets. But no
build is *blocked* on somebody having eyes, because on Codex nobody does.

Every quality question therefore has a measured form:

| The question | The measured answer |
| --- | --- |
| Is the mark correct? | `validate_glyph.py`, all numbers, zero external tools |
| Does it survive a favicon? | component and counter counts at 32 and 16 px |
| Is the guide usable? | `qc_render.py` ink coverage, density, largest empty run, folio presence |
| Do elements split across pages? | `qc_paginate.py`, DOM-level, exact |
| Is the contrast legal? | `coloraide` at build time, never a typed number |

When a rendered artifact cannot be produced at all, say so in `VERIFY.md` and in
the handoff. "The PDF was skipped because Chromium is unavailable" is a fine
outcome. "The PDF looks good" from an agent that never rendered it is not.

## Python

- Invoke as `sys.executable` from inside a script and as `python3` from a shell,
  falling back to `python` when `python3` is absent. Windows installs are
  usually `python` only.
- Target 3.8. No structural pattern matching, no `tomllib`, no `|` unions in
  annotations.
- Open every file with an explicit `encoding="utf-8"` and, on write,
  `newline="\n"`. Windows defaults to cp1252 and CRLF, and both corrupt a
  checksummed manifest.
- Install with `pip install --user`, and treat failure as normal rather than
  fatal: drop to a lower tier and record the skip.
- The only third-party dependency any *token* work has is `coloraide`. Guard the
  import and say what is unavailable rather than raising a traceback.

## Shell and paths

- Build every path with `os.path.join`. Never interpolate `/` into a path.
- Never depend on the working directory. Resolve relative to
  `os.path.dirname(os.path.abspath(__file__))`.
- Do not pipe, glob or chain in `subprocess`. Pass an argument list.
- Do not assume a POSIX utility exists. `find`, `sed`, `md5sum` and `unzip` are
  all absent somewhere.
- Some sandboxes cannot delete files. Prefer overwrite-in-place to
  delete-then-write, and if a directory has to be replaced, write the new files
  over the old ones rather than removing the tree first.

## External tools

Probe for every one of these and route to the first that answers:

| Job | First choice | Then | Then |
| --- | --- | --- | --- |
| SVG to PNG | `rsvg-convert` | `resvg` | the bundled `rsvg-convert.js` on Node with `@resvg/resvg-js` |
| Multi-entry ICO | `magick` | `convert` | Pillow, with the per-size PNGs already rendered |
| PDF | headless Chromium via Playwright | none: skip and record it | |
| PDF inspection | `pikepdf` | `pdffonts` | skip |

Two specific traps, both of which have cost a run:

**ImageMagick 6 has no `magick`.** It ships `convert`. A probe that tests only
for `magick` reports the ICO step as a skip on every ImageMagick 6 host, and a
skip reads as "not applicable" rather than "your favicon is broken".

**Google Fonts is a trap, not a tool.** `fonts.googleapis.com` resolves inside
the sandbox while `fonts.gstatic.com` is blocked, so a CSS fetch appears to
succeed and the build dies at the binary step with a confusing error. Fonts are
bundled in the kit. Copy them from a sibling kit; never fetch at build time.

## Network

Assume there is none. Nothing in the pipeline may require a network call to
succeed. Package installs, font fetches and CDN references are all conveniences
that must degrade to a recorded skip.

## Frontmatter and entry points

Different hosts read different things, so the skill ships both:

- `SKILL.md` with frontmatter limited to `name`, `description`, `license`,
  `compatibility`, `metadata` and `allowed-tools`. Anything else, `user-invocable`
  in particular, hard-fails claude.ai and Skills-API upload validation.
- `AGENTS.md` at the root, plain Markdown with no frontmatter at all, saying the
  same thing in the same order. This is what a Codex or an agent working from a
  bare checkout reads. It must stay in step with `SKILL.md`: when the routing
  table changes, both change.

Write instructions as file paths and shell commands, not as tool names. "Read
`references/08-glyph-construction.md`" works everywhere. "Use the Read tool on"
works in one product.

## The single most portable habit

Prefer a script that a human could run over an instruction a model has to
follow. `python3 templates/build_kit.py .` behaves identically on every
provider. A paragraph telling the agent what order to do six things in does not.

Every time a step turns out to be provider-dependent, the fix is to move it into
a template and have the prose call the template.
