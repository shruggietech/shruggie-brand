#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mk_paths.py: this brand's mark, as parameters.

COPY THIS FILE to <kit>/build/mk_paths.py and edit the parameter block. It is
the master for the logo geometry. `logo.paths` in brand.json is generated from
it and is never edited by hand.

    python3 build/mk_paths.py                  # print the measurements
    python3 build/mk_paths.py --write ../brand.json
    python3 templates/validate_glyph.py build/mk_paths.py

The example below is Covarity's aperture C: one ring broken once, with the long
arc in the identity accent and a short terminal segment in the inherited orange.
Replace the parameter block and the two composition lines; leave the rest.

Read references/08-glyph-construction.md before changing anything here.
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "templates"))
try:
    import glyphkit as G
except ImportError:                                   # running from the skill itself
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import glyphkit as G


# ------------------------------------------------------------------ parameters
# Every number the mark depends on, named, with what it controls. If the shape
# cannot be described in about ten of these, it is too complicated to be a logo.

GRID        = 1000        # square construction grid, declared in the README
R_OUT       = 420         # outer radius of the ring
R_IN        = 252         # inner radius, so the ring is 168 units thick
R_IN_REDUCED = 230        # the reduced master runs a heavier 190-unit ring

APERTURE    = (318, 42)   # the opening, from lower terminal to upper, 84 degrees
SLOT        = (78, 88)    # the break in the ring, 10 degrees

CLEAR_SPACE = 100         # one clear-space unit, 10 percent of the grid
REDUCED_BELOW_PX = 32     # below this size the reduced master takes over


# ---------------------------------------------------------------- composition
# Angles are degrees, counter-clockwise, zero pointing right. The module handles
# the SVG y-flip, so 90 is the top of the canvas.

_cx = _cy = GRID / 2.0

full = [
    {"role": "accent",
     "d": G.ring_band(_cx, _cy, R_OUT, R_IN, SLOT[1], APERTURE[0])},
    {"role": "emphasis",
     "d": G.ring_band(_cx, _cy, R_OUT, R_IN, APERTURE[1], SLOT[0])},
]

# The reduced master DELETES: no slot, no second colour, one heavier ring.
reduced = [
    {"role": "accent",
     "d": G.ring_band(_cx, _cy, R_OUT, R_IN_REDUCED, APERTURE[1], APERTURE[0])},
]

# An aperture removes ink from one side, so the drawn shape is not centred by
# construction. Measure the real ink and translate. Never nudge a constant until
# a preview looks right.
full = G.center_ink(full, GRID)
reduced = G.center_ink(reduced, GRID)


# ---------------------------------------------------------------------- output

def report():
    for name, paths in (("full", full), ("reduced", reduced)):
        x0, y0, x1, y1 = G.bbox(paths)
        print("%-8s bbox %7.1f %7.1f %7.1f %7.1f   %.0f x %.0f units   %d path(s)"
              % (name, x0, y0, x1, y1, x1 - x0, y1 - y0, len(paths)))
    print("")
    print("Now run the gate:")
    print("  python3 templates/validate_glyph.py %s"
          % os.path.relpath(os.path.abspath(__file__)))


def write(brand_path):
    """Merge the geometry into brand.json without disturbing anything else."""
    B = json.load(open(brand_path, encoding="utf-8"))
    lg = B.setdefault("logo", {})
    lg["grid"] = GRID
    lg["clear_space_units"] = CLEAR_SPACE
    lg["reduced_below_px"] = REDUCED_BELOW_PX
    lg["paths"] = {"full": full, "reduced": reduced}
    with open(brand_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(B, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote logo.paths into %s" % brand_path)


if __name__ == "__main__":
    if "--write" in sys.argv:
        write(sys.argv[sys.argv.index("--write") + 1])
    report()
