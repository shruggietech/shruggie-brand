# Contributing

Changes are specification-first and enter `main` through a reviewed pull request. Open or select the relevant issue, create a `codex/NNN-slug` branch, and keep the corresponding Spec Kit artifacts under `specs/NNN-slug/` current. Use Conventional Commit subjects and include the slice number when one exists.

## Prerequisites

- Git and GitHub CLI, authenticated for repository work
- Python 3.8 or newer
- Node.js 20 or newer and pnpm
- `coloraide` for measured color work
- Playwright Chromium, ImageMagick, Poppler (`pdftoppm`), and an SVG rasterizer for complete local artifacts

Create an isolated Python environment and install the required color dependency:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
pnpm --dir site install --frozen-lockfile
pnpm --dir site exec playwright install chromium
```

## Verification

Run the geometry unit tests, probe the toolchain, build every kit, and build the static site:

```powershell
.\.venv\Scripts\python skill/templates/test_glyphkit.py
.\.venv\Scripts\python skill/templates/probe.py
.\.venv\Scripts\python scripts/build_all.py
pnpm --dir site build
```

Every kit must report zero verification problems and zero glyph failures. Missing optional renderers must appear as explicit skips. Review generated contact sheets whenever the local capability tier produces them.

## Pull requests and releases

Complete the pull request template with issue traceability, Spec Kit artifacts, verification evidence, accessibility impact, and documentation impact. Tags use `vMAJOR.MINOR.PATCH`. Release workflows build artifacts from the tag and must never publish hand-built archives.

Report vulnerabilities privately through GitHub's security advisory flow as described in [SECURITY.md](SECURITY.md).
