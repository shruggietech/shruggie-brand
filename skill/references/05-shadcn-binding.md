# The shadcn Binding

**This is the layer that closes the gap. Everything else in a kit describes the
brand; this makes the brand the path of least resistance.**

An agent working in a Next.js project reaches for `--primary`, `bg-card`,
`text-muted-foreground`, `--ring`. A kit that publishes only `--brand-green`
gets read, agreed with, and then bypassed. Mapping canon onto shadcn's own slot
names is the whole fix.

Generator: `templates/gen_nextjs.py`. Worked output: `examples/shruggietech/`.

## What gets emitted

```
nextjs/
  globals.css               Tailwind v4, @theme inline, :root and .dark in OKLCH
  fonts.ts                  next/font against bundled and npm faces
  providers.tsx             next-themes, dark by default
  components.json.snippet   the registries entry a consumer pastes
  registry/
    registry.json           the catalog
    theme.json              registry:theme carrying every cssVar
    fonts.json              registry:font
  README.md                 install instructions and the rules that outlive them
```

## Four decisions worth understanding

### 1. Keep shadcn's `:root` = light, `.dark` = dark convention

ShruggieTech is dark-first, and the tempting move is to invert those two blocks
so dark is the default. **Do not.** Every third-party shadcn block, every
copy-pasted component, and next-themes itself assume the standard convention.
Inverting it breaks all of them for no gain.

Dark-first is expressed in `providers.tsx` with `defaultTheme="dark"` and
`enableSystem={false}`. Same outcome, nothing broken.

### 2. Radius pegs are set explicitly

shadcn derives its whole radius scale from one `--radius` by fixed ratios
(sm 0.6x, md 0.8x, lg 1x, xl 1.4x). That derivation cannot land 6/8/12 at once.
The generator writes the steps directly:

```css
--radius-sm: 6px;   /* chips */
--radius-md: 8px;   /* Button, Input, Select, Popover, Dropdown */
--radius-lg: 10px;
--radius-xl: 12px;  /* Card, Dialog */
--radius-2xl: 16px;
```

The values are chosen so each canon peg lands on the component that actually
uses that utility. The pegs are non-negotiable; shadcn's ratio is not.

### 3. Every colour ships as OKLCH with the hex in a trailing comment

Hex stays canonical in `brand.json` for print, vinyl, and legal use. OKLCH is
what reaches the browser, matching current shadcn practice and making
programmatic derivation sane. The comment lets a human read the file and lets
`verify` assert the round-trip.

### 4. The accent appears twice, differently

`--primary` in `.dark` is the bright accent. `--primary` in `:root` is the
**accessible** variant. This is not a nicety. ShruggieTech's bright green
measures 1.98:1 on the light surface and is currently set as the light-mode
link colour on the live site. The generator makes that mistake unrepresentable.

`--primary-foreground` is measured, never assumed. White on ShruggieTech green
is 2.10:1; black is 9.99:1.

## The chart formula, and two ways it goes wrong

Rotate hue by 0, -52, +52, -104, +104 off the identity accent, hold chroma at
0.92x for entries two through five, then **solve lightness against the actual
surface**, taking the value closest to the target that still clears 4.5:1.

Both failure modes were hit while building this and both are now guarded:

- **Tuning for one surface.** A palette solved against black is too pale to
  read on near-white. The first generated light palette measured 3.79 to 4.21
  and failed. Solve against the real surface.
- **Overshooting.** A naive solve walks lightness to whichever extreme passes
  first and produces near-monochrome entries at 9:1 that satisfy the check and
  lose the brand entirely. Take the closest passing value, not the first.
- **Double-darkening.** The light path already receives the accessible variant.
  Darkening it again reproduces the overshoot.

Current output for ShruggieTech:

| Surface | Entries | Ratios |
| --- | --- | --- |
| dark | `#2BCC73 #C2AE00 #00C3D3 #FE8840 #75AEFF` | 9.99 · 9.35 · 9.75 · 8.81 · 9.25 |
| light | `#037B40 #746700 #00747E #9C4E1C #3566AA` | 5.05 · 5.36 · 5.20 · 5.61 · 5.44 |

## Distribution

Publish the catalog and let a consuming project install with one command:

```bash
npx shadcn@latest registry add @shruggietech=https://brand.shruggie.tech/shruggietech/brand/r/{name}.json
npx shadcn@latest add @shruggietech/theme @shruggietech/fonts
```

Private registries authenticate through `components.json`'s `registries`
object with `${ENV_VAR}` expansion in headers, so an internal namespace needs
no special client work.

Two things this unlocks beyond convenience:

- **The shadcn MCP server** (`npx shadcn mcp init --client claude`) works
  against any valid registry with no extra server code. An agent can ask what
  is in the namespace and install from it conversationally.
- **Registries carry non-component files**, including `AGENTS.md` and agent
  rule files. The enforcement layer ships down the same pipe as the tokens, so
  the brand and its rules arrive together via the command the agent was already
  going to run.

## Fonts

`fonts.ts` uses `next/font/local` for Geist, Geist Mono, and Space Grotesk. Keep it beside the exported kit's `fonts/` tree so a Next.js build makes no font-network request.

The generated README carries the warning that matters: never fetch fonts at
build time inside a sandbox. `fonts.gstatic.com` is blocked by the egress proxy
while `fonts.googleapis.com` resolves, so the fetch appears to succeed and then
dies at the binary step.

## Verification

`verify` re-parses the generated `globals.css` and asserts:

1. Every OKLCH value round-trips to its stated hex
2. Every foreground/background pair meets 4.5:1, both modes
3. `destructive` and `ring` are legible on their surface, both modes
4. All five chart entries clear 4.5:1 on their surface, both modes
5. The radius pegs are present and exact
6. Dark-first comes from the provider and `:root` is still light

All six pass on the ShruggieTech instance. Check 4 is in the list because it
caught a real failure during development.
