"""Parametric fixture mark used to exercise capsule and polygon primitives."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "skill", "templates"))
import glyphkit as G

GRID = 1000


def frame(stroke):
    return [
        {"role": "accent", "d": G.capsule(220, 180, 780, 180, stroke)},
        {"role": "accent", "d": G.capsule(220, 820, 780, 820, stroke)},
        {"role": "accent", "d": G.capsule(180, 220, 180, 780, stroke)},
        {"role": "accent", "d": G.capsule(820, 220, 820, 780, stroke)},
    ]


full = frame(88) + [
    {"role": "emphasis", "d": G.polygon([
        (500, 326), (674, 500), (500, 674), (326, 500)
    ])}
]

reduced = frame(112)
