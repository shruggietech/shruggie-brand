#!/usr/bin/env python3
"""Construct the Local Companion orbit candidate from named glyphkit primitives."""

from __future__ import annotations

import json
import sys
from pathlib import Path

for ancestor in Path(__file__).resolve().parents:
    templates = ancestor / "skill" / "templates"
    if (templates / "glyphkit.py").is_file():
        sys.path.insert(0, str(templates))
        break
else:
    raise RuntimeError("BrandBuilder glyphkit was not found")

import glyphkit as G


GRID = 512                 # square construction grid
CENTER = GRID / 2          # shared orbital center
OUTER_RADIUS = 202         # outside of both full orbit arcs
INNER_RADIUS = 164         # 38-unit full arc thickness
CORE_RADIUS = 70           # central companion workspace
LEFT_START = 70            # first full arc begins above right
LEFT_END = 200             # first full arc ends below left
RIGHT_START = 240          # second full arc begins below left
RIGHT_END = 390            # second full arc ends above right
REDUCED_OUTER_RADIUS = 206
REDUCED_INNER_RADIUS = 153 # wider reduced arc
REDUCED_CORE_RADIUS = 78  # bolder center at favicon scale
REDUCED_START = 55        # one opening remains at upper right
REDUCED_END = 355
CLEAR_SPACE = 48
REDUCED_BELOW_PX = 32


full = [
    {"role": "ink", "d": G.ring_band(CENTER, CENTER, OUTER_RADIUS, INNER_RADIUS,
                                      LEFT_START, LEFT_END, cap="round")},
    {"role": "accent", "d": G.ring_band(CENTER, CENTER, OUTER_RADIUS, INNER_RADIUS,
                                         RIGHT_START, RIGHT_END, cap="round")},
    {"role": "accent", "d": G.disc(CENTER, CENTER, CORE_RADIUS)},
]

reduced = [
    {"role": "accent", "d": G.ring_band(CENTER, CENTER, REDUCED_OUTER_RADIUS,
                                         REDUCED_INNER_RADIUS, REDUCED_START,
                                         REDUCED_END, cap="round")},
    {"role": "accent", "d": G.disc(CENTER, CENTER, REDUCED_CORE_RADIUS)},
]

full = G.center_ink(full, GRID)
reduced = G.center_ink(reduced, GRID)


def write_brand(path):
    target = Path(path)
    brand = json.loads(target.read_text(encoding="utf-8"))
    logo = brand.setdefault("logo", {})
    logo["grid"] = GRID
    logo["clear_space_units"] = CLEAR_SPACE
    logo["reduced_below_px"] = REDUCED_BELOW_PX
    logo["paths"] = {"full": full, "reduced": reduced}
    target.write_text(json.dumps(brand, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8", newline="\n")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--write":
        write_brand(sys.argv[2])
    else:
        print(json.dumps({"full": full, "reduced": reduced}, indent=2))
