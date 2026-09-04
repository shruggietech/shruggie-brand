#!/usr/bin/env python3
"""Read the measured capability contract written by probe.py."""

import json
import os


def load_capabilities(kit):
    path = os.path.join(os.path.abspath(kit), "qc", "probe.json")
    if not os.path.isfile(path):
        raise RuntimeError("capability probe is missing; run probe.py for this kit first")
    with open(path, encoding="utf-8") as handle:
        capabilities = json.load(handle)
    tier = capabilities.get("tier")
    if tier not in {"core", "raster", "full"}:
        raise RuntimeError("capability probe has invalid tier %r" % tier)
    return capabilities
