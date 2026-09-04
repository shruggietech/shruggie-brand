#!/usr/bin/env python3
"""Cross-platform subprocess defaults for project-owned console launchers."""

import os
import subprocess


def hidden_process_kwargs():
    """Disable prompts and suppress console windows without changing POSIX behavior."""
    kwargs = {"stdin": subprocess.DEVNULL}
    if os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    return kwargs
