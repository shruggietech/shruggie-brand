#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reject false ShruggieTech ownership claims in third-party generated output."""

import sys

from brand_contract import load_brand, scan_affiliation_output


def main():
    if len(sys.argv) != 3:
        print("usage: scan_affiliation.py <brand.json> <kit-dir>", file=sys.stderr)
        return 2
    brand = load_brand(sys.argv[1])
    problems = scan_affiliation_output(brand, sys.argv[2])
    for problem in problems:
        print("FAIL %s" % problem)
    if problems:
        print("%d false-affiliation problem(s)" % len(problems))
        return min(len(problems), 125)
    print("0 false-affiliation problems")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
