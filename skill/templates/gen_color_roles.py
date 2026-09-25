#!/usr/bin/env python3
"""Emit measured role records shared by kit and guideline renderers."""

import json
import sys
from pathlib import Path

from color_roles import resolve_color_roles
from interface_contract import load_brand_canon


def main():
    if len(sys.argv) != 3:
        print("usage: gen_color_roles.py <brand.json> <kit-dir>", file=sys.stderr)
        return 2
    brand = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    roles = resolve_color_roles(brand, load_brand_canon())
    path = Path(sys.argv[2]) / "color-roles.json"
    path.write_text(json.dumps(roles, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print("generated %s: %d formal colors and %d interface cues" %
          (path, len(roles["identity"]), len(roles["interface"]["dark"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
