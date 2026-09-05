#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compose, package, and describe cross-platform application icon suites."""

from __future__ import annotations

import base64
import json
import os
import shutil
import struct
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

from brand_contract import application_icon_profile


SCHEMA_VERSION = "1.0.0"
ANDROID_DENSITIES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
WINDOWS_TARGETS = (16, 20, 24, 30, 32, 36, 40, 48, 60, 64, 72, 80, 96, 256)
ICO_SIZES = (16, 24, 32, 48, 64, 128, 256)
MAC_ROLES = ((16, 1), (16, 2), (32, 1), (32, 2), (128, 1), (128, 2), (256, 1), (256, 2), (512, 1), (512, 2))
GENERATION_MARKER = ".iconkit-generated.json"


def _pillow():
    """Load Pillow only for raster work so core-tier vector generation remains usable."""
    from PIL import Image, ImageChops, PngImagePlugin
    return Image, ImageChops, PngImagePlugin


def write_text(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def safe_reset(kit, target):
    root = Path(kit).resolve()
    resolved = Path(target).resolve()
    allowed = {root / "icons", root / "favicons"}
    if resolved not in allowed:
        raise ValueError("refusing to clear non-icon generated directory %s" % resolved)
    if resolved.exists():
        shutil.rmtree(str(resolved))
    resolved.mkdir(parents=True, exist_ok=True)


def _collect_domain_icons(icons_root):
    """Preserve source-owned interface symbols while replacing generated suites."""
    icons_root = Path(icons_root)
    if not icons_root.is_dir():
        return []
    generated = ((icons_root / "manifest.json").is_file()
                 or (icons_root / GENERATION_MARKER).is_file()
                 or any((icons_root / name).exists() for name in ("web", "android", "apple", "windows")))
    domain_root = icons_root / "domain"
    if generated:
        candidates = [path for path in domain_root.rglob("*") if path.is_file()] if domain_root.is_dir() else []
        return [(path.relative_to(domain_root), path.read_bytes()) for path in candidates]
    candidates = [path for path in icons_root.rglob("*") if path.is_file()]
    return [(path.relative_to(icons_root), path.read_bytes()) for path in candidates]


def inspect_png(path, background=None):
    Image, ImageChops, _ = _pillow()
    path = Path(path)
    with Image.open(str(path)) as source:
        source.verify()
    with Image.open(str(path)) as source:
        rgba = source.convert("RGBA")
        alpha = rgba.getchannel("A")
        extrema = alpha.getextrema()
        content_bbox = None
        if background is not None:
            plate = Image.new("RGB", rgba.size, _hex_rgb(background))
            content_bbox = ImageChops.difference(rgba.convert("RGB"), plate).getbbox()
        return {
            "size": rgba.size,
            "mode": source.mode,
            "srgb": "srgb" in source.info,
            "has_transparency": extrema[0] < 255,
            "visible_bbox": alpha.getbbox(),
            "content_bbox": content_bbox,
        }


def _hex_rgb(value):
    return tuple(int(value[index:index + 2], 16) for index in (1, 3, 5))


def _visible_crop(image):
    rgba = image.convert("RGBA")
    box = rgba.getchannel("A").getbbox()
    if box is None:
        raise ValueError("canonical icon foreground has no visible pixels")
    return rgba.crop(box)


def _contain(mark, size, ratio, color=None):
    Image, _, _ = _pillow()
    source = _visible_crop(mark)
    maximum = max(1, int(round(size * ratio)))
    scale = min(maximum / source.width, maximum / source.height)
    dimensions = (max(1, int(round(source.width * scale))), max(1, int(round(source.height * scale))))
    source = source.resize(dimensions, Image.Resampling.LANCZOS)
    if color is not None:
        fill = Image.new("RGBA", source.size, _hex_rgb(color) + (255,))
        fill.putalpha(source.getchannel("A"))
        source = fill
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(source, ((size - source.width) // 2, (size - source.height) // 2))
    return canvas


def _plated(mark, size, background, ratio=0.72, color=None):
    Image, _, _ = _pillow()
    canvas = Image.new("RGBA", (size, size), _hex_rgb(background) + (255,))
    canvas.alpha_composite(_contain(mark, size, ratio, color))
    return canvas


def _png_bytes(image):
    with tempfile.SpooledTemporaryFile() as handle:
        image.save(handle, format="PNG", optimize=True, pnginfo=_srgb_metadata())
        handle.seek(0)
        return handle.read()


def _save_png(image, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(str(path), format="PNG", optimize=True, pnginfo=_srgb_metadata())


def _srgb_metadata():
    _, _, PngImagePlugin = _pillow()
    metadata = PngImagePlugin.PngInfo()
    metadata.add(b"sRGB", b"\x00")
    return metadata


def _write_ico(entries, output):
    Image, _, _ = _pillow()
    payloads = []
    for size, image in entries:
        payloads.append((size, _png_bytes(image.resize((size, size), Image.Resampling.LANCZOS))))
    offset = 6 + len(payloads) * 16
    directory = []
    data = []
    for size, payload in payloads:
        encoded = 0 if size == 256 else size
        directory.append(struct.pack("<BBBBHHII", encoded, encoded, 0, 0, 1, 32, len(payload), offset))
        data.append(payload)
        offset += len(payload)
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_bytes(struct.pack("<HHH", 0, 1, len(payloads)) + b"".join(directory) + b"".join(data))


def _write_icns(images, output):
    types = {16: b"icp4", 32: b"icp5", 64: b"icp6", 128: b"ic07", 256: b"ic08", 512: b"ic09", 1024: b"ic10"}
    chunks = []
    for size in sorted(types):
        payload = _png_bytes(images[size])
        chunks.append(types[size] + struct.pack(">I", len(payload) + 8) + payload)
    body = b"".join(chunks)
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_bytes(b"icns" + struct.pack(">I", len(body) + 8) + body)


def _svg_wrapper(source, background, ratio=0.72):
    encoded = base64.b64encode(Path(source).read_bytes()).decode("ascii")
    inset = (1.0 - ratio) * 512.0 / 2.0
    extent = 512.0 - inset * 2.0
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">\n'
        '  <rect width="512" height="512" fill="%s"/>\n'
        '  <image x="%g" y="%g" width="%g" height="%g" preserveAspectRatio="xMidYMid meet" '
        'href="data:image/svg+xml;base64,%s"/>\n'
        '</svg>\n' % (background, inset, inset, extent, extent, encoded)
    )


class Writer:
    def __init__(self, kit, brand, profile, capabilities):
        self.kit = Path(kit)
        self.brand = brand
        self.profile = profile
        self.capabilities = capabilities
        self.artifacts = []
        self.suites = []

    def relative(self, path):
        return Path(path).relative_to(self.kit).as_posix()

    def record(self, path, platform, role, fmt, width=None, height=None,
               appearance=None, alpha=None, source_variant="metadata", destination="See suite README"):
        item = {
            "path": self.relative(path), "platform": platform, "role": role,
            "format": fmt, "width": width, "height": height,
            "appearance": appearance, "alpha": alpha,
            "source_variant": source_variant, "destination": destination,
        }
        self.artifacts.append(item)
        return item

    def text(self, path, content, platform, role, fmt="markdown", destination="See suite README"):
        write_text(path, content)
        return self.record(path, platform, role, fmt, destination=destination)

    def png(self, path, image, platform, role, appearance="default", alpha="either",
            source_variant="full", destination="See suite README"):
        _save_png(image, path)
        return self.record(path, platform, role, "png", image.width, image.height,
                           appearance, alpha, source_variant, destination)

    def platform_manifest(self, root, platform, entries, status="generated", reason=None):
        path = Path(root) / "manifest.json"
        content = {
            "schema_version": SCHEMA_VERSION,
            "brand": self.brand["slug"],
            "platform": platform,
            "status": status,
            "reason": reason,
            "artifacts": [item for item in entries],
        }
        write_text(path, json.dumps(content, indent=2) + "\n")
        self.record(path, platform, "platform-manifest", "json")
        return path


def _suite_readme(title, summary, locations):
    rows = "\n".join("| `%s` | %s |" % pair for pair in locations)
    return "# %s\n\n%s\n\n| Path | Use |\n|---|---|\n%s\n" % (title, summary, rows)


def _write_web(writer, full_svg, reduced_svg, full_mark, reduced_mark, raster):
    root = writer.kit / "icons" / "web"
    start = len(writer.artifacts)
    background = writer.profile["background"]
    for name, source, variant in (("favicon.svg", reduced_svg, "reduced"), ("favicon-full.svg", full_svg, "full")):
        path = root / name
        write_text(path, _svg_wrapper(source, background))
        writer.record(path, "web", "favicon", "svg", 512, 512, "default", "opaque", variant, "Web root or document icon link")
    readme = root / "README.md"
    writer.text(readme, _suite_readme(
        "Web icons",
        "Browser, touch, and installable-web assets. `favicon.svg` is preferred; PNG and ICO files are fallbacks.",
        (("favicon.svg", "Preferred reduced-mark browser favicon"), ("favicon-full.svg", "Full-mark vector alternative"),
         ("favicon.ico", "Classic multi-size fallback"),
         ("apple-touch-icon.png", "Apple touch icon"), ("site.webmanifest", "Installable web metadata")),
    ), "web", "instructions")
    if not raster:
        entries = writer.artifacts[start:]
        manifest = writer.platform_manifest(root, "web", entries, "generated", "vector-only at core tier")
        writer.suites.append({"id": "web", "root": "icons/web", "readme": writer.relative(readme),
                              "manifest": writer.relative(manifest), "status": "generated", "reason": "vector-only at core tier"})
        return
    sizes = (16, 24, 32, 48, 64, 128, 180, 192, 256, 512)
    images = {}
    for size in sizes:
        variant = "reduced" if size <= writer.profile["reduced_below_px"] else "full"
        mark = reduced_mark if variant == "reduced" else full_mark
        image = _plated(mark, size, background, 0.72)
        images[size] = image
        writer.png(root / ("favicon-%dx%d.png" % (size, size)), image, "web", "favicon", alpha="opaque", source_variant=variant, destination="Web root")
    writer.png(root / "apple-touch-icon.png", images[180], "web", "apple-touch", alpha="opaque", destination="Web root")
    for size in (192, 512):
        writer.png(root / ("android-chrome-%dx%d.png" % (size, size)), images[size], "web", "installable", alpha="opaque", destination="Web root")
    ico = root / "favicon.ico"
    _write_ico([(size, images[size]) for size in ICO_SIZES], ico)
    writer.record(ico, "web", "favicon-ico", "ico", appearance="default", alpha="opaque", source_variant="mixed", destination="Web root")
    webmanifest = root / "site.webmanifest"
    write_text(webmanifest, json.dumps({
        "name": writer.brand["title"], "short_name": writer.brand["title"],
        "display": "standalone", "background_color": background, "theme_color": background,
        "icons": [
            {"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    }, indent=2) + "\n")
    writer.record(webmanifest, "web", "web-manifest", "json", destination="Web root")
    entries = writer.artifacts[start:]
    manifest = writer.platform_manifest(root, "web", entries)
    writer.suites.append({"id": "web", "root": "icons/web", "readme": writer.relative(readme),
                          "manifest": writer.relative(manifest), "status": "generated", "reason": None})


def _write_android(writer, full_mark):
    root = writer.kit / "icons" / "android"
    start = len(writer.artifacts)
    background = writer.profile["background"]
    readme = root / "README.md"
    writer.text(readme, _suite_readme(
        "Android icons", "Copy the `app/src/main/res` tree into an Android application and upload the separate Play image in Play Console.",
        (("app/src/main/res", "Launcher and adaptive resources"), ("play-store/google-play-512.png", "Google Play listing artwork")),
    ), "android", "instructions")
    res = root / "app" / "src" / "main" / "res"
    for density, size in ANDROID_DENSITIES.items():
        writer.png(res / ("mipmap-%s" % density) / "ic_launcher.png", _plated(full_mark, size, background, 0.72),
                   "android", "legacy-launcher", alpha="opaque", destination="Android res/mipmap-%s" % density)
    foreground = _contain(full_mark, 432, 66.0 / 108.0)
    monochrome = _contain(full_mark, 432, 66.0 / 108.0, "#FFFFFF")
    writer.png(res / "drawable-nodpi" / "ic_launcher_foreground.png", foreground, "android", "adaptive-foreground", alpha="transparent", destination="Android res/drawable-nodpi")
    writer.png(res / "drawable-nodpi" / "ic_launcher_monochrome.png", monochrome, "android", "adaptive-monochrome", alpha="transparent", destination="Android res/drawable-nodpi")
    background_xml = '<?xml version="1.0" encoding="utf-8"?>\n<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle"><solid android:color="@color/ic_launcher_background"/></shape>\n'
    writer.text(res / "drawable" / "ic_launcher_background.xml", background_xml, "android", "adaptive-background", "xml", "Android res/drawable")
    adaptive = '<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@drawable/ic_launcher_background"/><foreground android:drawable="@drawable/ic_launcher_foreground"/><monochrome android:drawable="@drawable/ic_launcher_monochrome"/></adaptive-icon>\n'
    writer.text(res / "mipmap-anydpi-v26" / "ic_launcher.xml", adaptive, "android", "adaptive-declaration", "xml", "Android res/mipmap-anydpi-v26")
    colors = '<?xml version="1.0" encoding="utf-8"?>\n<resources><color name="ic_launcher_background">%s</color></resources>\n' % background
    writer.text(res / "values" / "ic_launcher_colors.xml", colors, "android", "color-resource", "xml", "Android res/values")
    writer.png(root / "play-store" / "google-play-512.png", _plated(full_mark, 512, background, 0.75),
               "android", "play-store", alpha="opaque", destination="Google Play Console")
    entries = writer.artifacts[start:]
    manifest = writer.platform_manifest(root, "android", entries)
    writer.suites.append({"id": "android", "root": "icons/android", "readme": writer.relative(readme),
                          "manifest": writer.relative(manifest), "status": "generated", "reason": None})


def _write_ios(writer, full_mark):
    root = writer.kit / "icons" / "apple" / "ios"
    start = len(writer.artifacts)
    background = writer.profile["background"]
    readme = root / "README.md"
    writer.text(readme, _suite_readme(
        "iOS and iPadOS icons", "Copy `Assets.xcassets/AppIcon.appiconset` into an Xcode asset catalog and select it as the primary app icon set.",
        (("Assets.xcassets/AppIcon.appiconset", "Current single-size default, dark, and tinted inputs"),),
    ), "apple-ios", "instructions")
    catalog = root / "Assets.xcassets" / "AppIcon.appiconset"
    images = (
        ("AppIcon-1024.png", _plated(full_mark, 1024, background, 0.72), None),
        ("AppIcon-1024-dark.png", _plated(full_mark, 1024, "#000000", 0.72), "dark"),
        ("AppIcon-1024-tinted.png", _plated(full_mark, 1024, "#FFFFFF", 0.72, "#000000"), "tinted"),
    )
    rows = []
    for name, image, appearance in images:
        writer.png(catalog / name, image, "apple-ios", "app-icon", appearance or "default", "opaque", destination="Xcode AppIcon.appiconset")
        row = {"filename": name, "idiom": "universal", "platform": "ios", "size": "1024x1024"}
        if appearance:
            row["appearances"] = [{"appearance": "luminosity", "value": appearance}]
        rows.append(row)
    contents = catalog / "Contents.json"
    write_text(contents, json.dumps({"images": rows, "info": {"author": "xcode", "version": 1}}, indent=2) + "\n")
    writer.record(contents, "apple-ios", "asset-catalog", "json", destination="Xcode AppIcon.appiconset")
    entries = writer.artifacts[start:]
    manifest = writer.platform_manifest(root, "apple-ios", entries)
    writer.suites.append({"id": "apple-ios", "root": "icons/apple/ios", "readme": writer.relative(readme),
                          "manifest": writer.relative(manifest), "status": "generated", "reason": None})


def _write_macos(writer, full_mark):
    root = writer.kit / "icons" / "apple" / "macos"
    start = len(writer.artifacts)
    background = writer.profile["background"]
    readme = root / "README.md"
    writer.text(readme, _suite_readme(
        "macOS icons", "Use the asset catalog in Xcode, the conventional iconset with `iconutil`, or the ready `AppIcon.icns` container.",
        (("Assets.xcassets/AppIcon.appiconset", "Xcode all-sizes catalog"), ("AppIcon.iconset", "Conventional iconset"), ("AppIcon.icns", "Application icon container")),
    ), "apple-macos", "instructions")
    catalog = root / "Assets.xcassets" / "AppIcon.appiconset"
    iconset = root / "AppIcon.iconset"
    rows = []
    icns_images = {}
    for points, scale in MAC_ROLES:
        pixels = points * scale
        image = _plated(full_mark, pixels, background, 0.72)
        suffix = "@2x" if scale == 2 else ""
        name = "icon_%dx%d%s.png" % (points, points, suffix)
        writer.png(catalog / name, image, "apple-macos", "asset-catalog-icon", alpha="opaque", destination="Xcode AppIcon.appiconset")
        writer.png(iconset / name, image, "apple-macos", "iconset-icon", alpha="opaque", destination="macOS AppIcon.iconset")
        rows.append({"filename": name, "idiom": "mac", "scale": "%dx" % scale, "size": "%dx%d" % (points, points)})
        icns_images[pixels] = image
    contents = catalog / "Contents.json"
    write_text(contents, json.dumps({"images": rows, "info": {"author": "xcode", "version": 1}}, indent=2) + "\n")
    writer.record(contents, "apple-macos", "asset-catalog", "json", destination="Xcode AppIcon.appiconset")
    icns = root / "AppIcon.icns"
    _write_icns(icns_images, icns)
    writer.record(icns, "apple-macos", "icns", "icns", appearance="default", alpha="opaque", source_variant="full", destination="macOS application bundle")
    entries = writer.artifacts[start:]
    manifest = writer.platform_manifest(root, "apple-macos", entries)
    writer.suites.append({"id": "apple-macos", "root": "icons/apple/macos", "readme": writer.relative(readme),
                          "manifest": writer.relative(manifest), "status": "generated", "reason": None})


def _write_windows(writer, full_mark, reduced_mark):
    root = writer.kit / "icons" / "windows"
    start = len(writer.artifacts)
    background = writer.profile["background"]
    readme = root / "README.md"
    writer.text(readme, _suite_readme(
        "Windows icons", "Use `classic/app.ico` for Win32 and the `msix` directory for packaged Windows applications.",
        (("classic/app.ico", "Classic application icon"), ("msix/Assets", "MSIX scale, target-size, and store assets"),
         ("msix/ApplicationVisualElements.fragment.xml", "Merge into Applications/Application"),
         ("msix/PackageProperties.fragment.xml", "Merge into Package for the Store logo")),
    ), "windows", "instructions")
    ico_images = {}
    for size in ICO_SIZES:
        mark = reduced_mark if size <= writer.profile["reduced_below_px"] else full_mark
        ico_images[size] = _plated(mark, size, background, 0.72)
    ico = root / "classic" / "app.ico"
    _write_ico([(size, ico_images[size]) for size in ICO_SIZES], ico)
    writer.record(ico, "windows", "classic-ico", "ico", appearance="default", alpha="opaque", source_variant="mixed", destination="Win32 application")
    assets = root / "msix" / "Assets"
    for base, label in ((44, "Square44x44Logo"), (150, "Square150x150Logo")):
        for scale in (100, 200, 400):
            pixels = base * scale // 100
            writer.png(assets / ("%s.scale-%d.png" % (label, scale)), _plated(full_mark, pixels, background, 0.72),
                       "windows", "msix-scale", alpha="opaque", destination="MSIX Assets")
    for size in WINDOWS_TARGETS:
        mark = reduced_mark if size <= writer.profile["reduced_below_px"] else full_mark
        writer.png(assets / ("Square44x44Logo.targetsize-%d.png" % size), _plated(mark, size, background, 0.72),
                   "windows", "target-size", alpha="opaque", source_variant="reduced" if mark is reduced_mark else "full", destination="MSIX Assets")
        writer.png(assets / ("Square44x44Logo.targetsize-%d_altform-unplated.png" % size), _contain(mark, size, 0.72),
                   "windows", "target-size", "dark-unplated", "transparent", "reduced" if mark is reduced_mark else "full", "MSIX Assets")
        writer.png(assets / ("Square44x44Logo.targetsize-%d_altform-lightunplated.png" % size), _contain(mark, size, 0.72),
                   "windows", "target-size", "light-unplated", "transparent", "reduced" if mark is reduced_mark else "full", "MSIX Assets")
    for scale in (100, 200, 400):
        pixels = 50 * scale // 100
        writer.png(assets / ("StoreLogo.scale-%d.png" % scale), _plated(full_mark, pixels, background, 0.72),
                   "windows", "store-logo", alpha="opaque", destination="MSIX Assets")
    title = str(writer.brand["title"])
    visual_elements = ('<?xml version="1.0" encoding="utf-8"?>\n'
                       '<uap:VisualElements xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10" '
                       'DisplayName=%s Description=%s BackgroundColor=%s '
                       'Square44x44Logo="Assets\\Square44x44Logo.png" '
                       'Square150x150Logo="Assets\\Square150x150Logo.png" AppListEntry="default"/>\n'
                       % (quoteattr(title), quoteattr("%s application" % title), quoteattr(background)))
    writer.text(root / "msix" / "ApplicationVisualElements.fragment.xml", visual_elements,
                "windows", "manifest-fragment", "xml", "Merge into Applications/Application")
    properties = ('<?xml version="1.0" encoding="utf-8"?>\n'
                  '<Properties xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10">'
                  '<DisplayName>%s</DisplayName><PublisherDisplayName>%s</PublisherDisplayName>'
                  '<Description>%s</Description><Logo>Assets\\StoreLogo.png</Logo></Properties>\n'
                  % (escape(title), escape(title), escape("%s application" % title)))
    writer.text(root / "msix" / "PackageProperties.fragment.xml", properties,
                "windows", "manifest-fragment", "xml", "Merge into Package")
    entries = writer.artifacts[start:]
    manifest = writer.platform_manifest(root, "windows", entries)
    writer.suites.append({"id": "windows", "root": "icons/windows", "readme": writer.relative(readme),
                          "manifest": writer.relative(manifest), "status": "generated", "reason": None})


def _write_skipped(writer, platform, root, reason):
    start = len(writer.artifacts)
    readme = root / "README.md"
    writer.text(readme, "# %s icons\n\nNot generated at this capability tier: %s\n" % (platform, reason), platform, "instructions")
    entries = writer.artifacts[start:]
    manifest = writer.platform_manifest(root, platform, entries, "skipped", reason)
    writer.suites.append({"id": platform, "root": writer.relative(root), "readme": writer.relative(readme),
                          "manifest": writer.relative(manifest), "status": "skipped", "reason": reason})


def generate_icon_suites(brand, kit, full_svg, reduced_svg, render_svg, capabilities):
    """Generate the authoritative platform tree and legacy web aliases."""
    kit = Path(kit).resolve()
    full_svg = Path(full_svg).resolve()
    reduced_svg = Path(reduced_svg).resolve()
    domain_icons = _collect_domain_icons(kit / "icons")
    safe_reset(kit, kit / "icons")
    safe_reset(kit, kit / "favicons")
    profile = application_icon_profile(brand)
    writer = Writer(kit, brand, profile, capabilities)
    marker = kit / "icons" / GENERATION_MARKER
    writer.text(marker, json.dumps({"generator": "shruggie-iconkit", "schema_version": SCHEMA_VERSION}, indent=2) + "\n",
                "web", "icon-index", "json", "Generation ownership marker")
    for relative, payload in domain_icons:
        target = kit / "icons" / "domain" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        suffix = target.suffix.lower()
        writer.record(target, "domain", "product-symbol", "svg" if suffix == ".svg" else "markdown" if suffix == ".md" else "binary", source_variant="source-preserved", destination="Product interface")
    root_readme = kit / "icons" / "README.md"
    writer.text(root_readme, _suite_readme(
        "%s application icons" % brand["title"],
        "Choose the platform directory below. Browser assets remain mirrored in `../favicons/` for compatibility.",
        (("web", "Browser, touch, and installable web"), ("android", "Android launcher and Play Store"),
         ("apple/ios", "iOS and iPadOS asset catalog"), ("apple/macos", "macOS catalog, iconset, and ICNS"),
         ("windows", "Win32 ICO and MSIX package assets"), ("domain", "Source-preserved product interface symbols, when supplied")),
    ), "web", "icon-index", destination="Kit root navigation")
    raster_capable = bool(capabilities.get("svg_raster"))
    full_mark = reduced_mark = None
    if raster_capable:
        Image, _, _ = _pillow()
        with tempfile.TemporaryDirectory(prefix="iconkit-", dir=str(kit)) as temporary:
            full_path = Path(temporary) / "full.png"
            reduced_path = Path(temporary) / "reduced.png"
            render_svg(full_svg, full_path, 1024)
            render_svg(reduced_svg, reduced_path, 1024)
            with Image.open(str(full_path)) as image:
                full_mark = image.convert("RGBA")
            with Image.open(str(reduced_path)) as image:
                reduced_mark = image.convert("RGBA")
    _write_web(writer, full_svg, reduced_svg, full_mark, reduced_mark, raster_capable)
    if raster_capable:
        _write_android(writer, full_mark)
        _write_ios(writer, full_mark)
        _write_macos(writer, full_mark)
        _write_windows(writer, full_mark, reduced_mark)
    else:
        reason = capabilities.get("raster_reason", "SVG raster capability unavailable")
        _write_skipped(writer, "android", kit / "icons" / "android", reason)
        _write_skipped(writer, "apple-ios", kit / "icons" / "apple" / "ios", reason)
        _write_skipped(writer, "apple-macos", kit / "icons" / "apple" / "macos", reason)
        _write_skipped(writer, "windows", kit / "icons" / "windows", reason)
    aliases = {}
    web = kit / "icons" / "web"
    for source in sorted(web.iterdir()):
        if not source.is_file() or source.name in {"README.md", "manifest.json"}:
            continue
        target = kit / "favicons" / source.name
        shutil.copy2(str(source), str(target))
        aliases[writer.relative(target)] = writer.relative(source)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "brand": brand["slug"],
        "profile": profile,
        "capability": {"tier": capabilities.get("tier", "core"), "svg_raster": raster_capable},
        "suites": writer.suites,
        "artifacts": writer.artifacts,
        "aliases": aliases,
    }
    write_text(kit / "icons" / "manifest.json", json.dumps(manifest, indent=2) + "\n")
    return manifest


def parse_xml(path):
    return ET.parse(str(path)).getroot()
