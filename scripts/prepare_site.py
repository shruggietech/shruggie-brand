#!/usr/bin/env python3
"""Materialize the static site from verified files in dist/."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SITE = ROOT / "site"
PUBLIC = SITE / "public"
GENERATED = SITE / "generated"


def source_dirs() -> list[Path]:
    return sorted(path for path in DIST.iterdir() if (path / "brand.json").is_file())


def replace_tree(source: Path, destination: Path) -> None:
    resolved = destination.resolve()
    try:
        resolved.relative_to(PUBLIC.resolve())
    except ValueError:
        raise ValueError(f"refusing to replace path outside site/public: {resolved}")
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def load_brand(source: Path) -> dict:
    return json.loads((source / "brand.json").read_text(encoding="utf-8"))


def validate_registry(source: Path, brand: dict) -> None:
    registry_dir = source / "nextjs" / "registry"
    catalog = json.loads((registry_dir / "registry.json").read_text(encoding="utf-8"))
    if catalog.get("$schema") != "https://ui.shadcn.com/schema/registry.json":
        raise ValueError(f"{brand['slug']}: registry schema is missing")
    names = {item["name"] for item in catalog.get("items", [])}
    if "theme" not in names or not (registry_dir / "theme.json").is_file():
        raise ValueError(f"{brand['slug']}: registry theme is missing")
    expected = f"https://brand.shruggie.tech/{brand['slug']}/brand"
    if brand.get("registry_base") != expected:
        raise ValueError(f"{brand['slug']}: registry_base must be {expected}")
    for path in registry_dir.glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))


def copy_kit(source: Path, brand: dict) -> dict:
    slug = brand["slug"]
    target = PUBLIC / slug
    target.mkdir(parents=True, exist_ok=True)
    replace_tree(source / "guidelines", target / "guidelines")
    replace_tree(source / "nextjs" / "registry", target / "brand" / "r")

    downloads = target / "downloads" / "files"
    downloads.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / "brand-guide.pdf", downloads / f"{slug}-brand-guide.pdf")
    for name in ("logos", "favicons", "specimens"):
        replace_tree(source / name, downloads / name)

    logo = f"/{slug}/downloads/files/logos/svg/{slug}-horizontal-color.svg"
    specimen_name = next((source / "specimens").glob("*.svg")).name
    return {
        "slug": slug,
        "title": brand["title"],
        "kind": brand.get("kind", "sub-brand"),
        "descriptor": brand["descriptor"],
        "idea": brand["brand_idea"],
        "version": brand["version"],
        "accent": brand["accent"]["bright"],
        "accentAccessible": brand["accent"]["accessible"],
        "logo": logo,
        "specimen": f"/{slug}/downloads/files/specimens/{specimen_name}",
    }


def docs() -> list[dict[str, str]]:
    result = []
    for path in sorted((ROOT / "skill" / "references").glob("*.md")):
        content = path.read_text(encoding="utf-8")
        title = next((line[2:] for line in content.splitlines() if line.startswith("# ")), path.stem)
        result.append({"slug": path.stem, "title": title, "content": content})
    return result


def install_registry_theme(source: Path) -> str:
    """Apply the registry theme into CSS using the shadcn registry contract."""
    item = json.loads((source / "nextjs" / "registry" / "theme.json").read_text(encoding="utf-8"))
    variables = item.get("cssVars", {})
    sections = []
    for selector, key in ((":root", "light"), (".dark", "dark")):
        values = variables.get(key, {})
        declarations = "\n".join(f"  --{name}: {value};" for name, value in values.items())
        sections.append(f"{selector} {{\n{declarations}\n}}")
    theme_values = variables.get("theme", {})
    declarations = "\n".join(f"  --{name}: {value};" for name, value in theme_values.items())
    sections.insert(1, f":root {{\n{declarations}\n}}")
    return "/* Installed from the generated ShruggieTech shadcn registry theme. */\n" + "\n".join(sections) + "\n"


def main() -> int:
    if not DIST.is_dir():
        raise SystemExit("dist/ is missing; run python scripts/build_all.py first")
    PUBLIC.mkdir(parents=True, exist_ok=True)
    GENERATED.mkdir(parents=True, exist_ok=True)

    brands = []
    for source in source_dirs():
        brand = load_brand(source)
        validate_registry(source, brand)
        brands.append(copy_kit(source, brand))

    expected = {"shruggietech", "fragcap", "go-schedule", "glitchpad", "covarity", "example-brand"}
    found = {brand["slug"] for brand in brands}
    if found != expected:
        raise ValueError(f"site needs {sorted(expected)}, found {sorted(found)}")

    parent = DIST / "shruggietech" / "tokens"
    parent_css = "\n".join(
        (parent / name).read_text(encoding="utf-8")
        for name in ("colors.css", "spacing.css", "typography.css", "base.css")
    )
    (GENERATED / "parent.css").write_text(parent_css, encoding="utf-8", newline="\n")
    (GENERATED / "registry-theme.css").write_text(
        install_registry_theme(DIST / "shruggietech"), encoding="utf-8", newline="\n"
    )
    generated_fonts = GENERATED / "fonts"
    if generated_fonts.exists():
        shutil.rmtree(generated_fonts)
    shutil.copytree(ROOT / "assets" / "fonts" / "woff2", generated_fonts)
    (GENERATED / "brands.json").write_text(
        json.dumps(brands, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    (GENERATED / "docs.json").write_text(
        json.dumps(docs(), indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"prepared {len(brands)} kits and {len(docs())} reference documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
