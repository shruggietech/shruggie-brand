#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emit deterministic audit evidence for validated authoritative inputs."""

import json
import sys
from pathlib import Path

from brand_contract import ContractError, authoritative_inputs, load_brand, validate_brand


def main():
    if len(sys.argv) != 3:
        print("usage: analyze_inputs.py <brand.json> <kit-dir>", file=sys.stderr)
        return 2
    brand_path = Path(sys.argv[1]).resolve()
    kit = Path(sys.argv[2]).resolve()
    try:
        brand = load_brand(brand_path)
        evidence = validate_brand(brand, kit)
        inputs = authoritative_inputs(brand, kit)
    except (ContractError, OSError, ValueError) as error:
        print("authoritative-input failure: %s" % error, file=sys.stderr)
        return 1
    output = {
        "brand": brand["slug"],
        "inputs": [
            {
                "id": record["id"],
                "role": record["role"],
                "path": record["path"],
                "format": record["format"],
                "sha256": record["sha256"],
                "color_profile": record["color_profile"],
                "usage_status": record["usage_status"],
                "license": record["license"],
                "approved_transformations": record["approved_transformations"],
            }
            for record, _ in inputs
        ],
        "palette_evidence": evidence,
    }
    destination = kit / "qc" / "authoritative-inputs.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(output, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")
    print("wrote %s" % destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
