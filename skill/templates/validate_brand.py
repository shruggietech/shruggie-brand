#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate a staged brand contract before any publishable generation."""

import json
import sys
from pathlib import Path

from brand_contract import ContractError, validate_brand_file


def main():
    if len(sys.argv) != 2:
        print("usage: validate_brand.py <brand.json>", file=sys.stderr)
        return 2
    try:
        brand, evidence = validate_brand_file(sys.argv[1])
    except (ContractError, OSError, ValueError) as error:
        print("contract failure: %s" % error, file=sys.stderr)
        return 1
    print("validated %s affiliation, typography, and %d palette evidence record(s)" % (brand["slug"], len(evidence)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
