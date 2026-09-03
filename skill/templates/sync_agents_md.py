#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_agents_md.py: keep AGENTS.md in step with SKILL.md.

    python3 templates/sync_agents_md.py [<skill-root>]

Two entry points exist because hosts differ. Claude reads SKILL.md and its
frontmatter. Codex, and anything working from a bare checkout, reads AGENTS.md
and would choke on the frontmatter. Maintaining both by hand guarantees they
drift, and a routing table that disagrees with itself is worse than one entry
point, so AGENTS.md is generated: frontmatter stripped, a short preamble added,
and the body copied verbatim.

Run it after any edit to SKILL.md. `verify.py` checks the two are in step.
"""
import hashlib
import os
import sys

PREAMBLE = """<!-- GENERATED from SKILL.md by templates/sync_agents_md.py. Do not edit. -->

# Agent instructions: shruggie-brandbuilder

You are working inside the `shruggie-brandbuilder` skill, or in a project that
vendored it. This file is the entry point for hosts that do not read skill
frontmatter; `SKILL.md` carries the same content plus that metadata.

Read this file, then follow the routing table below into `references/`. Paths
are relative to this directory. Everything is invoked as a shell command, so
nothing here depends on a particular host's tool names.

Before anything else:

    python3 templates/probe.py <kit-dir>

If `python3` is not on PATH, try `python`. If `coloraide` will not import, stop
and say so: contrast numbers are measured rather than typed, so no colour work
can proceed without it.

---

"""


def body_of(skill_md):
    text = open(skill_md, encoding="utf-8").read()
    if text.startswith("---"):
        end = text.index("\n---", 3)
        text = text[end + 4:]
    return text.lstrip("\n")


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..")
    skill = os.path.join(root, "SKILL.md")
    agents = os.path.join(root, "AGENTS.md")
    body = body_of(skill)
    # The H1 is the skill name in SKILL.md and the preamble already carries one.
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    out = PREAMBLE + "\n".join(lines).rstrip() + "\n"
    old = open(agents, encoding="utf-8").read() if os.path.exists(agents) else None
    with open(agents, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print("%s AGENTS.md (%d bytes, body sha %s)"
          % ("unchanged" if old == out else "wrote", len(out),
             hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
