#!/usr/bin/env python3
"""Visible-ink layout for explicitly configured horizontal wordmark rows."""
from brand_contract import horizontal_wordmark_lines


def horizontal_lockup(brand, font_path, colourway, roles, mark_markup, mark_box, outline, bbox):
    """Return an outlined, vertically centred row block beside the source mark."""
    profile = horizontal_wordmark_lines(brand)
    if profile is None or not font_path:
        raise ValueError("horizontal wordmark lines require an outlined font source")
    rows = []
    for row in profile["lines"]:
        path, _ = outline(row["text"], font_path, row["font_size_units"])
        box = bbox(path)
        if box is None or box[2] <= box[0] or box[3] <= box[1]:
            raise ValueError("horizontal wordmark row has no measurable ink")
        rows.append((row, path, box))
    height = profile["canvas_height_units"]
    mark_height = profile["mark_height_units"]
    padding = profile["padding_units"]
    block_height = sum(box[3] - box[1] for _, _, box in rows) + profile["line_gap_units"] * (len(rows) - 1)
    if mark_height > height - 2 * padding or block_height > height - 2 * padding:
        raise ValueError("horizontal mark or wordmark rows exceed the canvas")
    scale = mark_height / (mark_box[3] - mark_box[1])
    mark_width = (mark_box[2] - mark_box[0]) * scale
    word_x = padding + mark_width + profile["gap_units"]
    width = word_x + max(box[2] - box[0] for _, _, box in rows) + padding
    parts = ['  <g transform="translate(%g,%g) scale(%g) translate(%g,%g)">\n%s\n  </g>'
             % (padding, (height - mark_height) / 2, scale, -mark_box[0], -mark_box[1], mark_markup)]
    top = (height - block_height) / 2
    for index, (row, path, box) in enumerate(rows):
        ink = ("#000000" if colourway == "black" else "#FFFFFF" if colourway == "white"
               else roles[row["role"]])
        parts.append('  <g data-wordmark-line="%d" transform="translate(%g,%g)"><path fill="%s" d="%s"/></g>'
                     % (index + 1, word_x - box[0], top - box[1], ink, path))
        top += box[3] - box[1] + profile["line_gap_units"]
    return "\n".join(parts), width, height
