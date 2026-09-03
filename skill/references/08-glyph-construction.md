# Glyph Construction

**The agent does not type path data. It writes a short parametric script, and
then measures what came out.**

`06-logo-protocol.md` says what a mark must be: hand-authored vector on a
declared grid, filled paths, no live text, a separate reduced master. This file
says how to actually produce one without the result being wrong.

## Why this file exists

The construction step is where runs fail, and it fails the same way every time.
An agent decides on a shape, writes SVG path data straight into `brand.json`,
and has no way to tell whether the numbers it just wrote describe the shape it
had in mind. Sometimes it renders a PNG and looks; often it cannot, because the
provider has no vision, or the sandbox has no rasteriser, or the image comes
back and the defect is a two percent centring error that no one sees. Either
way the run either ships broken geometry or loops producing variants with no
stopping rule.

The fix is not better prose telling the agent to be careful. It is removing the
opportunity: geometry gets composed from primitives that cannot be malformed,
and correctness is decided by a number.

## The three artifacts

| File | What it is | Who writes it |
| --- | --- | --- |
| `templates/glyphkit.py` | Primitives, an absolute-only path builder, exact bbox, optical centring | Ships with the skill. Do not edit per brand. |
| `<kit>/build/mk_paths.py` | This brand's mark, as named parameters and a few primitive calls | The agent, once, per brand |
| `templates/validate_glyph.py` | The measured gate | Ships with the skill. Run it before anything else. |

`mk_paths.py` is the master. The `logo.paths` block in `brand.json` is generated
output. When the mark changes, the parameters in `mk_paths.py` change and
`brand.json` is regenerated. Editing path data in `brand.json` by hand is the
same error as editing a compiled binary.

## The procedure

### 1. Say the shape in words and numbers, before drawing anything

Write the parameter block first, with a comment per line saying what the number
controls. For an aperture C that is a centre, an outer radius, a ring thickness,
an aperture angle, and wherever the mark is split, a slot angle. For a monogram
in a container it is a container size, a corner radius, an inset, and a stroke
weight.

If the shape cannot be written as eight or ten named numbers, it is too
complicated to be a logo. That is a useful early signal, not an obstacle.

### 2. Compose it with primitives

    import glyphkit as G

    GRID   = 1000
    R_OUT  = 420      # outer radius
    R_IN   = 252      # 168-unit ring
    APERT  = (318, 42)

    full = [{"role": "accent",
             "d": G.ring_band(500, 500, R_OUT, R_IN, APERT[1], APERT[0])}]

The vocabulary is deliberately small: `ring_band`, `ring`, `wedge`, `disc`,
`rect`, `rounded_rect`, `capsule`, `polygon`, and a `Path` builder for anything
else. Angles are degrees, counter-clockwise, zero pointing right, and the module
handles the SVG y-flip. Reach for `Path` only when no primitive fits, and when
you do, use `.arc()` rather than working out control points yourself.

**Never write an `A`, `H`, `V`, `S`, `Q` or `T` command, and never a lowercase
relative one.** Tools in this kit read path data positionally, pairing numbers
as coordinates. `A` carries three non-coordinate numbers mid-list and `H` and
`V` carry one where a pair is expected, so both corrupt the reader silently:
the bbox comes back wrong, the assertion passes when it should fail, and the
mark clips at render time. `glyphkit` emits only absolute M, L, C and Z, and
`validate_glyph.py` fails any path that does not.

### 3. Centre the ink, do not centre the construction

A mark with an aperture, a descender, a folded corner, or any asymmetry is not
centred by putting its construction centre at `GRID / 2`. Compose it wherever
the maths is clearest, then finish with:

    full = G.center_ink(full, GRID)

This measures the flattened ink bounding box and translates. Do not nudge a
constant until a preview looks right: that is unrepeatable, and it encodes an
error nobody can later explain. Covarity's mark is constructed around x = 554
rather than 500 for exactly this reason, and the number is derived, not chosen.

### 4. Build the reduced master by deleting, not shrinking

At and below roughly 32 px, fine detail turns into noise. The reduced master is
a genuinely separate shape that removes whole elements. fragcap drops its four
reticle corners and keeps the F. Covarity drops the orange terminal and the
adjudication slot and runs one thicker ring.

Thinning everything is the wrong move and `validate_glyph.py` says so: a reduced
master with a smaller ink thickness and no fewer pieces than the full one gets a
warning naming both numbers.

### 5. Measure, and let the numbers decide

    python3 templates/validate_glyph.py <kit>/build/mk_paths.py

Every check is a number computed from a pure-Python rasterisation of the paths.
No renderer, no ImageMagick, no Pillow, no browser, no font. It reads the same
on a provider with vision and one without.

| Check | Fails or warns when |
| --- | --- |
| `commands` | a path uses anything but absolute M, L, C, Z |
| `ink-inside-grid` | flattened ink leaves the grid and will be clipped |
| `optical-centring` | the ink bbox centre sits more than 1.5 percent off |
| `coverage` | under 6 percent ink, or over 62 percent |
| `ink-thickness` | mean stroke thickness under 3.5 percent of the grid, or 6 for a reduced master |
| `smallest-piece` | the smallest element at 16 px is under two pixels |
| `components` | the number of separate pieces changes at 32 or 16 px |
| `counters` | an enclosed hole closes at 32 or 16 px |
| `reduced-master` | absent, identical to the full master, or thinner without being simpler |

Failures block. Warnings are judgement calls and several are legitimate: a mark
whose two pieces deliberately read as one silhouette at favicon size will warn
on `components`, and that can be the right design. Say why in `brand.json`
`assumptions` and move on.

### 6. Stop when it passes

**Zero failures is the stopping condition.** Not "looks good", not "one more
variant". An agent that can see images should still open `qc/logo-sheet.png`
after the build, because taste is not measurable and the sheet is one second of
looking. An agent that cannot see images is finished at zero failures and must
not pretend otherwise.

If the gate keeps failing on the same check after two attempts, the shape is
wrong rather than the numbers. Change one parameter at a time, or go back to
step 1 and pick a simpler shape. Do not generate a third and fourth variant
hoping one passes.

### 7. Write the paths into brand.json

`mk_paths.py` is imported and its `full` and `reduced` lists are serialised into
`logo.paths`. Record the parameters too, under `logo`, so the guide can print
the construction table without anybody retyping numbers:

    "logo": {
      "grid": 1000,
      "outer_radius_units": 420,
      "inner_radius_units": 252,
      "aperture_degrees": 84,
      "clear_space_units": 100,
      "reduced_below_px": 32,
      "construction": "One sentence describing how the shape is built.",
      "paths": { "full": [...], "reduced": [...] }
    }

## Roles, not colours

Every path carries a `role`, one of `accent`, `dim`, `emphasis`. The colourway
generator remaps roles; it never recolours a path by hand. A mark that names a
hex value in its geometry cannot produce a single-ink black variant, and every
kit needs one.

## Ideation

Image generation is welcome for exploring what the mark should feel like, and it
is the right use of the tool. It produces conversation, not artwork. The moment
a direction is agreed, the shape is rebuilt from primitives on the declared
grid. Never trace a diffusion output into shipped geometry, and never rasterise
a large mark down at runtime to make a favicon.

If the operator supplies a concept, describe back in words what is load-bearing
about it before redrawing. If they disagree with the description, the redraw
would have been wrong, and one sentence has saved the whole step.

## The two rules an agent most often breaks

**Two subpaths wound the same way do not make a hole.** Under fill-rule nonzero
they fill solid. `glyphkit.ring()` winds its inner circle backwards so the hole
appears under both fill rules; if you build a counter yourself with `Path`, wind
the inner contour in the opposite direction or declare `"fill_rule": "evenodd"`
on that path. This failure is invisible in a text diff and looks correct in
editors that default to evenodd.

**A cubic is not a circle.** The control-point distance for an arc of angle
theta is `4/3 * tan(theta/4)` times the radius, not a fixed 0.5523, which is
only right for a 90 degree quadrant. `glyphkit` splits arcs at 45 degrees and
computes the constant per segment. An agent doing this by hand gets flattened
curves that look almost right and measure wrong.
