# Example Brand fixture

This pipeline fixture is separate from the sibling product identities. It does not consume an identity hue slot.

The fixture deliberately reuses ShruggieTech green because only two legal gaps remain in the sibling hue circle. Its full and reduced marks are authored in [`build/mk_paths.py`](build/mk_paths.py) with glyphkit capsules and a polygon.

Build it from the repository root:

```powershell
.\.venv\Scripts\python.exe scripts\build_all.py example
```

Generated output is written to `dist/example-brand/` and is not committed.
