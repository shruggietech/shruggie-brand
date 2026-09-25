# The shadcn Binding

**This layer maps approved brand decisions into the names a shadcn consumer uses.**

An agent working in a Next.js project reaches for `--primary`, `bg-card`, `text-muted-foreground`, and `--ring`. The generated binding gives those slots approved source values and measurable pairings instead of leaving a consumer to choose a substitute.

Generator: `templates/gen_nextjs.py`. Inspect the exact generated `nextjs/` directory in the selected kit for delivered values.

## What gets emitted

```
nextjs/
  globals.css               Tailwind v4, @theme inline, :root and .dark in OKLCH
  fonts.ts                  next/font/local against bundled faces
  providers.tsx             next-themes, dark by default
  components.json.snippet   the registries entry a consumer pastes
  registry/
    registry.json           the catalog
    theme.json              registry:theme carrying every cssVar
    <component>.json        installable registry:ui payloads
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
does not automatically clear the light-surface contrast floor. The generator
derives and measures the accessible light variant before publication.

`--primary-foreground` is measured, never assumed. White on ShruggieTech green
is 2.10:1; black is 9.99:1.

## The chart formula and its checks

Rotate hue by 0, -52, +52, -104, +104 off the identity accent, hold chroma at
0.92x for entries two through five, then **solve lightness against the actual
surface**, taking the value closest to the target that still clears 4.5:1.

Solve against the real surface in each theme. A value that passes on black may fail on a light ground. Take the nearest passing lightness rather than pushing every entry to an extreme, and do not darken a value twice after the light-theme variant has already been derived. Read measured current entries from the selected kit's tokens and `VERIFY.md`.

## Distribution

The public `registry.json` is a discovery catalog. A consuming Next.js/Tailwind v4 project installs direct item endpoints with the pinned shadcn CLI:

```bash
npx shadcn@4.21.0 registry add @shruggietech=https://brand.shruggie.tech/shruggietech/brand/r/{name}.json
npx shadcn@4.21.0 add @shruggietech/theme
```

Private registries authenticate through `components.json`'s `registries`
object with `${ENV_VAR}` expansion in headers, so an internal namespace needs
no special client work.

Two things this unlocks beyond convenience:

- Each item endpoint is checked against the pinned registry schema and installed in a clean consumer fixture before publication. A catalog entry mirrors that endpoint rather than acting as an empty placeholder.
- The CLI does not install the whole kit or its enforcement instructions. Download the complete kit to obtain those files, local fonts, and the wider brand guidance.

## Fonts

`fonts.ts` uses `next/font/local` for the role faces selected by `typography.mode`. House mode emits Geist, Geist Mono, and Space Grotesk. Fixed mode emits only the declared local faces and their measured weights and styles. Copy the kit's `nextjs/fonts.ts` and `fonts/` tree together, preserving their relative paths, then apply `fontVariables` to `<html>`. A `registry:font` item cannot deliver these bundled faces with shadcn 4.21.0 because its schema only permits a Google provider. The catalog therefore does not advertise one. This manual step makes no font-network request.

The generated theme also resolves `brand-emphasis` and `brand-cta` from the explicit inheritance contract. House inheritance uses ShruggieTech orange. Independent inheritance uses the brand's required semantic colors and does not receive the house pair.

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
