# Work Order: shruggie-brand repository, CI, and brand.shruggie.tech

Status: ready to execute
Author: prepared for handoff to a code agent
Audience: AI coding agent, any provider
Format: pure Markdown, UTF-8 without BOM

## 0. What you are building

One repository that holds the ShruggieTech brand system: the
`shruggie-brandbuilder` skill, the source of every brand kit built with it, the
CI that rebuilds and verifies all of them on every push, and a static site
published at `https://brand.shruggie.tech` that serves both the documentation
and the live shadcn registries every kit points at.

Four outcomes define done:

1. Changing a generator in the skill re-runs every kit and fails the build if any
   kit regresses. This is the primary value; everything else is secondary.
2. `npx shadcn@latest add @covarity/theme` works against a real URL.
3. Releases ship the two skill bundles, built by CI from a tag.
4. `A:\_tmp\branding` can be deleted without losing anything.

Read this whole file before starting. Work the phases in order. Each phase has
acceptance criteria; do not begin the next phase until the current one meets
them.

## 1. Ground rules

- Do not commit generated output. Sources in git, artifacts published. The
  single exception is `assets/fonts/`, which is a binary source.
- Do not byte-diff rebuilt artifacts in CI. Chromium stamps PDFs and rsvg
  versions shift PNG bytes. Assert `verify.py` reports 0 problems and
  `validate_glyph.py` reports 0 failures instead.
- Do not redraw any existing logo. The five shipped marks are correct and in
  use. Section 5 says exactly how to bring legacy geometry across without
  touching it.
- Accessibility is never exemptable. Section 6.5. A WCAG AA failure is fixed,
  never grandfathered, whatever else it costs.
- Write every text file UTF-8 without BOM, LF line endings.
- Avoid em-dashes in prose you author. Use parentheses, commas or hyphens.
- Every skill fix you make belongs in `skill/templates/`, never in a kit. If a
  kit needs a patched generator, that is a defect in the skill.
- If a step needs a decision that is not in this document, take the most
  reasonable option, record it in `docs/decisions.md` with the reasoning, and
  keep moving. Do not stall.

## 2. Preflight

### 2.1 Confirm your tooling

Report the version of each and stop if any required one is missing:

- `git`, `gh` (required, authenticated)
- Cloudflare CLI (required, authenticated). Detect which is installed:
  `wrangler`, `flarectl`, or `cf`. If none is on PATH, check for a configured
  API token in the environment and use the Cloudflare REST API over `curl`
  instead. Section 8 specifies the end state, not the exact commands, so any of
  these paths is acceptable.
- `python3` or `python`, 3.8 or newer (required)
- `node` 20 or newer and a package manager (required for the site)
- `rsvg-convert` or `resvg`, ImageMagick (`magick` or `convert`), and Playwright
  Chromium (optional locally, required in CI)

### 2.2 Read the sibling projects

Three ShruggieTech repositories live under `A:\Code`:

- `A:\Code\fragcap`
- `A:\Code\go-schedule`
- `A:\Code\glitchpad`

**You must inspect all three and replicate their project management conventions
in the new repository.** Do not invent conventions. Extract at minimum:

- `.github/` in full: workflows, issue templates, PR template, CODEOWNERS,
  dependabot config, labels defined as code if present
- Label set and colours. If not in the repo, read them from the live repo with
  `gh label list --repo shruggietech/<name> --json name,color,description`
- Milestone naming and how they map to releases
- Whether GitHub Projects (v2) boards are used, their field schema, and their
  automation rules
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`
- Commit message convention: run `git log --oneline -80` in each and infer the
  pattern (conventional commits or otherwise). Match the dominant one.
- Branch naming: `git branch -a` and `git log --merges --oneline -40`
- `CHANGELOG.md` format and how release notes are generated
- Versioning scheme and tag format
- Branch protection and required checks, via
  `gh api repos/shruggietech/<name>/branches/main/protection`

Write what you found to `docs/decisions.md` under a heading "Conventions
inherited from sibling projects", naming which repository each convention came
from. Where the three disagree, prefer the most recent one (`glitchpad`) and say
so.

### 2.3 Back up before you touch anything

Create `A:\_tmp\branding-backup-<YYYYMMDD>.zip` containing the whole of
`A:\_tmp\branding`. Do not delete anything from that folder at any point before
Phase 10, and not until CI is green.

## 3. Source material, with absolute paths

Everything below is on the local machine. Paths are exact.

### 3.1 The skill, version 1.1.0, canon 1.1.0

`A:\_tmp\branding\.agents\skills\shruggie-brandbuilder\`

41 files. This is the authoritative source. It contains:

- `SKILL.md` and `AGENTS.md` (the second is generated from the first by
  `templates/sync_agents_md.py`; never hand-edit `AGENTS.md`)
- `references/00-variance-contract.md` through `references/09-portability.md`
- `references/01-canon.json`, the machine-readable inheritance root
- `templates/`, 21 files including `glyphkit.py`, `validate_glyph.py`,
  `test_glyphkit.py`, `probe.py`, `mk_paths.example.py`, `gen_*.py`, `qc_*.py`,
  `verify.py`, `build_kit.py`, `rsvg-convert.js`
- `LICENSE` (Apache-2.0, canonical text), `NOTICE`, `LICENSE-BRAND.md`
- `examples/shruggietech/`, a reference generated instance

Prebuilt bundles of the same tree, for reference only. CI must rebuild these
rather than committing them:

- `A:\_tmp\branding\.agents\skills\shruggie-brandbuilder.skill` (zip, Claude
  upload format, has `SKILL.md` with frontmatter)
- `A:\_tmp\branding\.agents\shruggie-brandbuilder-portable.zip` (same tree,
  `SKILL.md` removed, `AGENTS.md` is the only entry point, plus a `README.md`)
- `A:\_tmp\branding\.agents\_sbb-source.zip` (transport copy, redundant, delete
  in Phase 10)

Sanity check before you rely on it:

```
cd A:\_tmp\branding\.agents\skills\shruggie-brandbuilder
python3 templates/test_glyphkit.py     # expect: 28 checks, 0 failures
python3 templates/probe.py             # expect: a tier line
```

### 3.2 The five brand kits

| Path | brand.json | canon | mk_paths.py | On-disk size | State |
| --- | --- | --- | --- | --- | --- |
| `A:\_tmp\branding\shruggietech-brand\` | no | pre-canon | no | 1.1 MB | Original parent kit. Different shape entirely: `_ds_bundle.js`, `_ds_manifest.json`, `scraps\`, `uploads\`, `thumbnail.html`, `assets\`. No `logos\svg`. |
| `A:\_tmp\branding\fragcap-brand\` | no | pre-canon | no | 1.8 MB | 17 SVGs in `logos\svg`. Carries 12 bespoke build scripts in `build\` including `geometry.py`, `build_logos.py`, `outline.py`, `typeset.py`, `print_pdf.js`, `check_pages.js`. |
| `A:\_tmp\branding\go-schedule-brand\` | no | pre-canon | no | 2.0 MB | 14 SVGs in `logos\svg`. No `build\` at all. |
| `A:\_tmp\branding\glitchpad-brand\` | yes | 1.0.0 | no | 24 MB | Canon-era. Its `build\` scripts are the ones the skill 1.1.0 templates were promoted from. |
| `A:\_tmp\branding\covarity-brand\` | yes | 1.0.0 | **yes** | 4.9 MB | The only kit built the current way. Use it as the reference for what a migrated kit looks like. |

Zipped snapshots of the same kits, superseded by the repository once Phase 4 is
done: `shruggietech-brand.zip`, `fragcap-brand.zip`, `go-schedule-brand.zip`,
`glitchpad-brand.zip`, `covarity-brand.zip`, all directly in
`A:\_tmp\branding\`.

### 3.3 Fonts

Five faces plus two OFL licences, currently duplicated in every kit:

`A:\_tmp\branding\covarity-brand\fonts\` (use this copy as canonical)

- `ttf\Geist-Regular.ttf`, `ttf\Geist-Medium.ttf`, `ttf\GeistMono-Regular.ttf`,
  `ttf\SpaceGrotesk-Medium.ttf`, `ttf\SpaceGrotesk-Bold.ttf`
- `woff2\` with the same five faces
- `licenses\OFL-Geist.txt`, `licenses\OFL-Space-Grotesk.txt`
- `fonts.css`, `README.md`

Verify the other kits carry byte-identical copies before deduplicating. If any
differ, keep the newest and record the discrepancy in `docs/decisions.md`.

### 3.4 Everything else in that folder

- `A:\_tmp\branding\.glitchpad-brandbuilder-runtime\` contains a Python venv,
  `node_modules` with `@resvg/resvg-js`, and `tools\rsvg-convert.js` plus
  `tools\rsvg-convert.cmd`. Regenerable. Do not commit. The two `tools\` files
  are worth comparing against `skill/templates/rsvg-convert.js`.
- `A:\_tmp\branding\_archive\` (3.8 MB): dry-run PDFs, before-and-after
  comparison PNGs, three early Glitchpad mark SVGs, a screenshot. Historical.
- `A:\_tmp\branding\go-schedule-v091-tooltip-research\` (20 MB): unrelated to
  branding. Belongs in the go-schedule repository, not here.
- `A:\_tmp\branding\covarity\covarity-research-and-architecture-blueprint.pdf`:
  belongs to the Covarity project, not the brand system.
- `A:\_tmp\branding\shruggietech-styles1.css` and `shruggietech-styles2.css`:
  the provenance source the canon was lifted from. Keep as
  `docs/provenance/` reference material.
- `A:\_tmp\branding\Claude outputs\`: assorted session output. Triage in
  Phase 10.

## 4. Phase 1: repository scaffold and GitHub configuration

### 4.1 Create the repository

Name: `shruggie-brand`, under the same owner as the sibling projects. Confirm
against sibling naming before creating; if they use a different prefix
convention, match it and record the deviation.

**Visibility: public.** The stated goal is a public GitHub Pages site, and Pages
from a private repository requires a paid plan. State this assumption at the top
of your first status report. If the owner later wants it private, the site host
has to change.

### 4.1.1 Licensing: Apache-2.0, required

**The repository is licensed under the Apache License 2.0.** This is decided, not
a choice to make. Do not substitute MIT, do not dual-licence, and do not carry
the old "Proprietary. Internal ShruggieTech use." wording anywhere.

Apache-2.0 is the right fit for a published brand system specifically because
its section 6 grants no trademark rights, so the marks stay reserved by the
licence itself rather than by a bolted-on exception.

Three files, all of which **already exist in `skill/`** and must be lifted to the
repository root as well:

- `LICENSE`, the full canonical Apache-2.0 text. Copy it verbatim from
  `skill/LICENSE`. Do not retype it, do not reflow it, do not trim the appendix.
- `NOTICE`, the Apache attribution notice. The copy in `skill/NOTICE` is written
  for the skill alone; extend it at the repository root to cover the kits and the
  site, and keep the bundled-font section.
- `LICENSE-BRAND.md`, which states what the Apache grant does not cover. Copy
  `skill/LICENSE-BRAND.md` and extend it as kits are added.

The boundary that file draws, and which you must preserve:

- **Reserved:** the ShruggieTech and Shruggie names, every sub-brand name, every
  wordmark and logo in any format, the endorsement lockup, and the **logo path
  data** committed in `brand.json` under `logo.paths` together with any
  `build/mk_paths.py` that generates it. Logo geometry is the mark expressed as
  numbers and is reserved on the same terms as the rendered artwork. This matters
  because the geometry is one of the few brand assets that *is* committed.
- **Apache-2.0:** everything else, including all of `skill/templates/`, all of
  `skill/references/`, the generators, the verification and QC scripts, the site
  source, and the token structure and methodology.

Fonts keep their SIL Open Font License 1.1 and ship with their licence texts,
which is already the case in every generated kit. Neither `LICENSE` nor
`LICENSE-BRAND.md` alters those terms.

Also required:

- Link `LICENSE`, `NOTICE` and `LICENSE-BRAND.md` from `README.md`, and link
  `LICENSE-BRAND.md` from every kit's README.
- Add the standard Apache short-form header to source files if, and only if, the
  sibling projects do. Match them; do not introduce a convention they lack.
- `skill/SKILL.md` frontmatter `license:` is already updated to the Apache
  wording. If you change it, regenerate the entry point with
  `python3 skill/templates/sync_agents_md.py skill`.
- Set the repository licence metadata so GitHub detects it:
  `gh repo edit --license apache-2.0` if supported by your `gh` version,
  otherwise confirm detection after the first push with
  `gh api repos/{owner}/shruggie-brand --jq .license.spdx_id`, which must return
  `Apache-2.0`.

### 4.2 Configure it with `gh`

Do as much as possible without touching the web UI:

- `gh repo create` with description and homepage `https://brand.shruggie.tech`
- `gh repo edit` to set: squash merge only, delete head branch on merge, disable
  wiki if the siblings do, enable issues, set topics
- Labels: replicate the sibling set with `gh label create`. Add at minimum
  `skill`, `kit:<slug>` for each of the five, `site`, `ci`, `canon`, `migration`
- Milestones via `gh api -X POST repos/{owner}/shruggie-brand/milestones`, one
  per phase of this work order
- A GitHub Project board if the siblings use one, with the same field schema
- Branch protection on `main` via
  `gh api -X PUT repos/{owner}/shruggie-brand/branches/main/protection`,
  requiring the `build` check from Phase 6 and matching the siblings' review
  requirements
- Open one issue per phase of this document, assigned to its milestone, with the
  acceptance criteria copied in

### 4.3 Layout

```
shruggie-brand/
  README.md
  AGENTS.md
  CHANGELOG.md
  LICENSE                    Apache-2.0, verbatim
  NOTICE                     Apache attribution, plus bundled font licences
  LICENSE-BRAND.md           what the Apache grant does not cover
  CONTRIBUTING.md
  .github/
    workflows/
    ISSUE_TEMPLATE/
  skill/                     the brandbuilder, verbatim from 3.1
  assets/fonts/              one copy, shared by every kit
  brands/
    shruggietech/
    fragcap/
    go-schedule/
    glitchpad/
    covarity/
  fixtures/
    example-brand/           the demo run, doubles as the end-to-end test
  site/                      Next.js source
  docs/
    decisions.md
    provenance/
  .gitignore                 must ignore dist/ and every generated kit directory
```

Each `brands/<slug>/` holds **sources only**:

```
brands/<slug>/
  brand.json
  build/mk_paths.py          when the mark is authored with glyphkit
  README.md
  SKILL.md
  ui_kits/<slug>-web/        hand-authored demo surface
  icons/                     only when the brand draws domain icons
  NOTES.md                   migration notes, legacy quirks, accepted warnings
```

Nothing else. `tokens/`, `components/`, `nextjs/`, `logos/`, `favicons/`,
`specimens/`, `guidelines/`, `fonts/`, `brand-guide.pdf`, `manifest.json`,
`VERIFY.md` and `qc/` are all generated into `dist/` and gitignored.

**Acceptance:** repository exists, is configured, `main` is protected, labels and
milestones match the siblings, `gh api repos/{owner}/shruggie-brand --jq
.license.spdx_id` returns `Apache-2.0`, and `docs/decisions.md` records what was
inherited from where.

## 5. Phase 2: import the skill and the fonts

1. Copy `A:\_tmp\branding\.agents\skills\shruggie-brandbuilder\` to `skill/`
   verbatim. Do not restructure it.
2. Copy the font set from `A:\_tmp\branding\covarity-brand\fonts\` to
   `assets/fonts/`, preserving the `ttf/`, `woff2/` and `licenses/` split.
3. Add a build step that stages `assets/fonts/` into each kit's `fonts/`
   directory at build time. The skill expects `<kit>/fonts/` to exist; do not
   change the skill to read from a shared path, because a kit has to remain
   self-contained when it is exported.
4. Run `python3 skill/templates/test_glyphkit.py`. It must report 28 checks and
   0 failures.

**Acceptance:** the self-test passes from a clean clone on a machine that has
only Python and its standard library.

## 6. Phase 3: migrate the five kits

This is the largest phase. Work one kit at a time, easiest first, and commit
each separately.

**Order: covarity, glitchpad, go-schedule, fragcap, shruggietech.**

### 6.1 Do not redraw any mark

The five marks are shipped and in use. Re-deriving them parametrically risks
silent drift, and a brand mark that changes because a build script was rewritten
is a serious defect. The rule:

- A kit whose geometry already exists as path data keeps that path data.
- Only author a `build/mk_paths.py` when the mark is genuinely being changed, or
  when a kit has no usable path data at all.
- `covarity` already has `mk_paths.py`. Bring it across unchanged.

### 6.2 Add a provenance flag to the skill

`validate_glyph.py` fails any path using a command outside absolute M, L, C, Z.
Legacy SVGs will contain arcs, `H` and `V`. That check must not force a redraw.

Add to `brand.json` a `logo.geometry_provenance` field with two values:

- `"glyphkit"` (default) means the geometry came from `mk_paths.py` and the
  command rule is enforced as a failure.
- `"imported"` means the geometry predates the skill. The command rule
  downgrades to a warning, and `VERIFY.md` records the kit as carrying imported
  geometry with the reason.

Implement this in `skill/templates/validate_glyph.py` and
`skill/templates/verify.py`, document it in
`skill/references/08-glyph-construction.md`, and register it in
`skill/references/01-canon.json` under `glyph`. Bump canon to 1.1.2 and the
skill to 1.1.2, and add a `CHANGELOG.md` entry. (1.1.1 is already taken by the
accessibility floor, see section 3.5.)

Every kit that uses `"imported"` must say so in its `NOTES.md`, with a line on
what it would take to move it to `"glyphkit"` later.

### 6.3 Per kit

For `covarity` and `glitchpad`, which already have `brand.json`:

1. Copy `brand.json`, `README.md`, `SKILL.md`, `ui_kits/`, and (covarity only)
   `build/mk_paths.py` into `brands/<slug>/`.
2. Strip `measured` and `color` from `brand.json`. Those are written back by
   `enrich_brand.py` at build time and must not be committed.
3. Set `"canon": "1.1.1"`.
4. Set `registry_base` (see 6.4).
5. Build and verify.

For `go-schedule`, `fragcap` and `shruggietech`, which have no `brand.json`:

1. Author `brand.json` by reading the existing kit. The values you need are all
   present in its `tokens/`, `styles.css`, `README.md`, `SKILL.md` and
   `VERIFY.md`. `A:\_tmp\branding\covarity-brand\brand.json` is the schema
   reference; `skill/references/01-canon.json` is the authority on which fields
   are constrained.
2. Extract the mark path data from the existing SVGs in `logos\svg\` into
   `logo.paths.full` and `logo.paths.reduced`, and set
   `"geometry_provenance": "imported"`. `fragcap` has 17 SVGs and
   `go-schedule` has 14; identify the full mark, the reduced master and the
   wordmark. `shruggietech-brand` has no `logos\svg` directory, so look in
   `assets\` and in `_ds_bundle.js`.
3. Preserve every measured colour value exactly, **except where a value fails
   WCAG AA**. See section 3.5: accessibility corrections are required and
   pre-authorised. Do not re-solve an accent for taste, and do not re-derive a
   chart palette by hand. `enrich_brand.py` recomputes the contrast numbers; if
   a recomputed number disagrees with the shipped `VERIFY.md`, the shipped one
   was wrong. Record each correction in `NOTES.md` rather than silently
   accepting it.
4. `fragcap` and `shruggietech` decline or accept the shruggie flourish and use
   specific voice registers already stated in their `SKILL.md`. Carry those
   across verbatim.
5. `fragcap` draws six bespoke capture-domain icons. They live in
   `A:\_tmp\branding\fragcap-brand\icons\`. Copy them into
   `brands/fragcap/icons/` as sources.
6. Delete nothing from the original folders yet.

Expect the older kits to surface real defects when they first pass through
`verify.py`. That is the point. Fix the kit's data, not the checker, unless the
checker is demonstrably wrong, in which case fix it in `skill/templates/` and
say so in the commit message.

### 6.4 Point every registry at the subdomain

Set `registry_base` in all five kits to:

```
https://brand.shruggie.tech/<slug>/brand
```

so that the resolved registry URL is
`https://brand.shruggie.tech/<slug>/brand/r/{name}.json`.

This replaces `https://covarity.ai/brand` and `https://glitchpad.com/brand`.
Every sub-brand now resolves through the parent domain, which is deliberate: it
reinforces the "A SHRUGGIETECH PROJECT" endorsement across the family, it works
before a product has its own domain, and it means one build and one place. A
product site can proxy or redirect to a vanity URL later.

Update `skill/references/05-shadcn-binding.md` so the documented URL shape
matches.

**Acceptance:** `python3 skill/templates/build_kit.py dist/<slug>` succeeds for
all five, each reporting 0 problems from `verify.py` and 0 failures from
`validate_glyph.py`. Warnings are allowed and must be explained in that kit's
`NOTES.md`.

## 6.5 Accessibility is not negotiable

**Decided by the owner. Treat it as a constraint, not a preference.**

WCAG 2.1 AA at rendered size is a floor that nothing waives: no conformance
level, no legacy grandfathering, no operator override, no deadline. A kit that
cannot meet AA is not shippable, and the resolution is always to change the
value. Canon 1.1.1 records this under `accessibility.exemptions` and names four
checks as non-exemptable: `aa-floor`, `accent-rule`, `globals-slots` and
`contrast-rederived`.

Understand why `aa-floor` was added, because it changes what migration finds.
`contrast-rederived` only asks whether a stated contrast number is honest. It
passes a token that accurately declares 3.2:1, and it skips entirely on a kit
that states no numbers at all, which is the case for all three pre-canon kits.
`aa-floor` asks whether the value is legal, reading canon's per-colour `aa`
declaration for whether a colour is used as text and on which surface.

### This will change the parent brand and the live site

`shruggietech-brand` ships bright green `#2BCC73` as its light-mode link colour.
That measures **1.98:1** on the light surface. It fails, it has always failed,
and the shipped kit never derived an accessible variant. Migration substitutes
`#037B40` at 5.05:1 wherever green is used as text on a light surface.

Two consequences you must handle:

1. The rebuilt `shruggietech-brand` will differ from the shipped one in that
   value. This is correct. Record it in `brands/shruggietech/NOTES.md` and in
   `CHANGELOG.md` as an accessibility correction with both measured numbers.
2. **The live site is downstream and also wrong.** `shruggie.tech` sets the
   bright green as its light-mode link colour in its own stylesheet. Fixing the
   kit does not fix the site. Open a tracking issue against whichever repository
   owns that stylesheet, link it from `docs/decisions.md`, and reference the
   provenance CSS at `A:\_tmp\branding\shruggietech-styles1.css` and
   `A:\_tmp\branding\shruggietech-styles2.css`, which is where the value came
   from. Do not edit the live site yourself as part of this work order.

### How the identity gate treats it

Section 6.1 forbids changing identity values during a rebuild, and an
accessibility correction is an identity change. The gate resolves this by
category rather than by exception: a change required to reach AA is
**pre-authorised**. `compare_identity.py` records it and proceeds. Every other
identity difference still blocks and needs an explicit accept flag with a
written reason.

Expect the two oldest kits to surface further AA failures when they first pass
through `verify.py`. Fix every one. Do not open an exemption, do not add a
conformance-level escape, and do not defer any of them to a follow-up issue.

## 7. Phase 4: the fixture brand

Build `fixtures/example-brand/` as a complete, deliberately synthetic kit whose
only job is to demonstrate and regression-test the pipeline end to end.

- It is explicitly a fixture, not a sibling product, and does not consume an
  identity hue slot. Say this in its `brand.json` `assumptions` and in its
  `README.md`.
- Its mark is authored with `glyphkit` in `build/mk_paths.py`, using different
  primitives from any real kit, so the primitive vocabulary is exercised.
- It is the worked example the documentation site links to, and the thing a new
  operator copies when starting a kit.

Note for context: the identity hue circle is nearly full. With the inherited
orange at 38.3 and accents at 96.2, 153, 215.7, 253.3 and 311.8, the 30-degree
minimum separation leaves only two legal gaps, roughly 183 to 185.7 and roughly
341.8 to 8.3. The fixture must not take one of them. Give it an accent that
knowingly violates the sibling rule and mark it as a fixture exemption, or reuse
the parent green. Record which you chose and why.

**Acceptance:** a clean checkout can run one documented command and produce the
fixture kit with 0 problems.

## 8. Phase 5: continuous integration

Author workflows in `.github/workflows/`, matching the sibling repositories'
style and naming.

### 8.1 `build.yml`, on push and pull request

1. Set up Python, install `coloraide` and the optional extras, install
   Playwright Chromium, install `rsvg-convert` and ImageMagick.
2. `python3 skill/templates/test_glyphkit.py`
3. `python3 skill/templates/probe.py` and print the tier, so a degraded runner is
   visible in the log.
4. For each kit in `brands/` and `fixtures/`: stage sources plus
   `assets/fonts/` into `dist/<slug>/`, then run
   `python3 skill/templates/build_kit.py dist/<slug>`.
5. Fail the job if any kit reports a non-zero problem count.
6. Assert `AGENTS.md` is in step: run
   `python3 skill/templates/sync_agents_md.py skill` and fail if it reports a
   change, since that means `SKILL.md` was edited without regenerating.
7. Upload `dist/` as an artifact.

This is the regression suite. It is the reason the repository exists. The
generators drifted two versions ahead of the skill precisely because nothing
ever re-ran the older kits.

### 8.2 `pages.yml`, on push to `main`

Builds the site (Phase 6) and deploys with `actions/deploy-pages` from the build
artifact. Do not publish from a committed `/docs` directory: the site is
generated, and committing the largest generated artifact would undercut the rule
everywhere else.

### 8.3 `release.yml`, on tag

1. Rebuild both skill bundles from `skill/`:
   - `shruggie-brandbuilder-<version>.skill`, the tree including `SKILL.md`
   - `shruggie-brandbuilder-<version>-portable.zip`, the same tree with
     `SKILL.md` removed and the portable `README.md` added
2. Zip each built kit as `<slug>-brand-<version>.zip` and attach it.
3. Generate release notes from `CHANGELOG.md`, following whatever convention the
   siblings use. Every release must state both the skill version and the canon
   version, and must carry an explicit line on whether existing kits need
   migrating.

**Acceptance:** a tagged commit produces a release with both bundles and five kit
archives, all built by CI rather than by hand.

## 9. Phase 6: the site

Next.js, App Router, `output: 'export'`, `images: { unoptimized: true }`.

Next.js is the right choice here for one specific reason: the site is the
reference implementation of the binding layer the skill ships. It installs its
own theme from its own registry during its build, so a malformed registry breaks
the build rather than shipping quietly.

### 9.1 The rule that keeps it honest

**The site consumes the kits. It never restates them.**

`gen_guidelines.py` already emits "the system rendered from itself" and
`verify.py` checks it. If the site re-authors the palette page in MDX you get two
descriptions of the brand system and only one is verified. So:

- Next.js owns the shell: home, brand index, the brandbuilder documentation
  rendered from `skill/references/*.md`, and the ShruggieTech-branded chrome.
- Per-brand guidelines pages, brand guide PDFs, logo masters, favicons, type
  specimens and registry JSON are copied verbatim from `dist/` into the export.

### 9.2 Fonts

Use `next/font/local` against `assets/fonts/`, not `next/font/google`. The reason
is fidelity rather than network: the brand guide PDF, the type specimen and the
site must render the same bytes of Space Grotesk, and Google's copy can drift
from the bundled one.

While you are there, fix a real inconsistency in the skill: the generated
`skill/templates/gen_nextjs.py` emits a `fonts.ts` whose header comment reads
"Fonts come from bundled/npm sources, never a build-time network fetch" and then
imports `Space_Grotesk` from `next/font/google`, which is exactly a build-time
network fetch. Canon rank 2 permits the practice for generated projects, so the
import can stay, but the comment is wrong. Correct the comment to state what it
actually does and why canon allows it.

### 9.3 Routes

- `/` ShruggieTech brand system landing, wearing the parent identity
- `/docs/...` the brandbuilder documentation, from `skill/references/`
- `/<slug>/` per-brand overview
- `/<slug>/guidelines/` the generated guidelines page, served as-is
- `/<slug>/brand/r/{name}.json` the shadcn registry, copied verbatim
- `/<slug>/downloads/` PDF, logo masters, favicons, specimen

Serve all five accents together somewhere on the landing page. It is the only
surface where they appear side by side, it makes the variance contract visible,
and it makes the hue exhaustion obvious rather than something rediscovered on the
next brand.

**Acceptance:** the site builds statically, installs its theme from its own
registry, and `npx shadcn@latest add @covarity/theme` succeeds against the
deployed URL.

## 10. Phase 7: DNS and custom domain

Do this without asking the owner for anything. The Cloudflare CLI is installed
and authenticated.

### 10.1 Required end state

Zone `shruggie.tech`:

- One `CNAME` record, name `brand`, target `<owner>.github.io`, TTL auto.
- **Create it DNS-only, with the Cloudflare proxy disabled.** GitHub cannot
  provision its TLS certificate while the record is proxied, and enabling the
  orange cloud too early is the standard way this fails. Leave it unproxied.
- Once GitHub reports the certificate as issued, you may optionally enable the
  proxy with SSL mode Full (strict). If you do, verify HTTPS still resolves and
  record the change in `docs/decisions.md`. If in any doubt, leave it DNS-only.

Use whichever CLI is present (`wrangler`, `flarectl`, `cf`) or the Cloudflare
REST API with the configured token. The end state above is what matters, not the
command you used. Record the command you actually ran.

### 10.2 GitHub side

- Add a `CNAME` file containing `brand.shruggie.tech` to the published artifact,
  or set the custom domain through the API:
  `gh api -X PUT repos/{owner}/shruggie-brand/pages -f cname=brand.shruggie.tech`
- Enforce HTTPS:
  `gh api -X PUT repos/{owner}/shruggie-brand/pages -F https_enforced=true`
- Verify with `gh api repos/{owner}/shruggie-brand/pages` and by fetching
  `https://brand.shruggie.tech/covarity/brand/r/theme.json`

**Acceptance:** the subdomain resolves over HTTPS, the registry JSON is fetchable,
and `npx shadcn@latest add @covarity/theme` works from a scratch project.

## 11. Phase 8: README and release notes

`README.md` must open with what the repository is, then carry a decision table
that is exactly two rows:

| You are | Take |
| --- | --- |
| Working in Claude, uploading to the Customize pipeline | `shruggie-brandbuilder-<version>.skill` |
| Working in Codex, or vendoring into a repository | `shruggie-brandbuilder-<version>-portable.zip`, entry point `AGENTS.md` |

Resist adding a third bundle. Every extra artifact is another thing that goes
stale, and the capability tiers are detected at runtime rather than packaged
separately.

Then: the five kits with links to their pages, how to build one, how to add a
new one, the licence split, and a link to the site.

`CHANGELOG.md` starts at 1.1.0 with the changes already made (the glyph
construction layer, the portability tiers, the per-brand chart hue rotations, the
promoted generators, and the relicensing from proprietary to Apache-2.0) and
continues with 1.1.1 for the provenance flag from Phase 3.

Both release bundles must contain `LICENSE`, `NOTICE` and `LICENSE-BRAND.md` at
their root. A vendored copy with no licence file is legally ambiguous, which
defeats the point of relicensing. Assert their presence in `release.yml`.

## 12. Phase 9: verify the whole thing from cold

On a clean machine or a clean container:

1. `git clone` the repository
2. Install dependencies as `CONTRIBUTING.md` describes
3. Build all five kits and the fixture
4. Confirm 0 problems across the board
5. Build the site
6. Confirm the deployed site serves every registry

Fix anything that required a step not written down, then repeat. The
documentation is wrong until this passes without improvisation.

## 13. Phase 10: clean up A:\_tmp\branding

Only after CI is green, the site is live, and the backup from 2.3 exists.

Produce `docs/disposition.md` listing every top-level item in
`A:\_tmp\branding` and its fate. Proposed dispositions, for you to confirm
against what actually landed in the repository:

| Item | Disposition |
| --- | --- |
| `.agents\skills\shruggie-brandbuilder\` | Migrated to `skill/`. Delete. |
| `.agents\skills\shruggie-brandbuilder.skill` | Rebuilt by CI. Delete. |
| `.agents\shruggie-brandbuilder-portable.zip` | Rebuilt by CI. Delete. |
| `.agents\_sbb-source.zip` | Redundant transport copy. Delete. |
| `shruggietech-brand\` | Sources migrated. Delete after confirming the rebuilt kit matches. |
| `fragcap-brand\` | Same. Keep `build\geometry.py` and the other bespoke scripts in `docs/provenance/fragcap/` first, as the record of how that mark was originally made. |
| `go-schedule-brand\` | Same. |
| `glitchpad-brand\` | Same. |
| `covarity-brand\` | Same. |
| `*-brand.zip` (five files) | Superseded by release assets. Delete. |
| `.glitchpad-brandbuilder-runtime\` | Regenerable venv and node_modules. Delete. Compare `tools\rsvg-convert.js` against the skill's copy first. |
| `_archive\` | Historical dry-run output. Move to cold storage, do not commit. |
| `go-schedule-v091-tooltip-research\` | Unrelated to branding. Move to `A:\Code\go-schedule` or cold storage. |
| `covarity\covarity-research-and-architecture-blueprint.pdf` | Belongs to the Covarity project. Move there. |
| `shruggietech-styles1.css`, `shruggietech-styles2.css` | Canon provenance. Commit to `docs/provenance/`. |
| `Claude outputs\` | Triage. Anything not referenced by the repository goes to cold storage. |

Do not delete anything you have not confirmed exists in the repository or in
cold storage. When in doubt, move to `A:\_tmp\_to_delete\` and report it rather
than deleting.

**Acceptance:** `A:\_tmp\branding` is empty or holds only items explicitly listed
as deliberately retained, and `docs/disposition.md` accounts for every one.

## 14. Reporting

Report at the end of each phase: what you did, what you decided that this
document did not specify, what failed and how you fixed it, and anything you
found that contradicts this work order. Treat contradictions as findings worth
raising, not obstacles to route around silently.
