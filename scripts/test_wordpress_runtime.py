#!/usr/bin/env python3
"""Install and exercise the generated native theme on pinned WordPress/PHP pairs."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from urllib.request import urlopen

from coloraide import Color
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "scripts" / "wordpress-runtime"
PAIRS = (("6.9.9", "8.2", 18889), ("7.1.2", "8.3", 18890))


def run(args, cwd=FIXTURE, timeout=900):
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    result = subprocess.run(args, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace", timeout=timeout,
                            creationflags=flags, check=False)
    if result.returncode:
        raise RuntimeError("%s exited %d:\n%s" % (args, result.returncode, result.stdout[-8000:]))
    return result.stdout


def browser_probe(port, page_id, fixture_root, version):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
        try:
            page.goto("http://localhost:%d/?page_id=%d" % (port, page_id), wait_until="networkidle")
            page.screenshot(path=str(fixture_root / ("front-%s-debug.png" % version)), full_page=True)
            if page.get_by_text("Tell your story").count() == 0 or page.get_by_text("Get in touch").count() == 0:
                raise RuntimeError("Published pattern page missing at %s: %s" % (page.url, page.locator("body").inner_text()[:1200]))
            if page.get_by_text("Client footer preserved").count() == 0:
                raise RuntimeError("Saved template-part override did not render on the published page")
            if page.locator("main").count() != 1 or page.locator("header").count() < 1:
                raise RuntimeError("Published page lacks expected landmarks")
            local_font_loaded = page.evaluate("async () => { await document.fonts.ready; return [...document.fonts].some(face => face.family.includes('Geist') && face.status === 'loaded'); }")
            if not local_font_loaded:
                raise RuntimeError("Bundled local body font did not load in the published page")
            home = page.locator("nav a").filter(has_text="Home")
            if home.count() != 1 or not home.get_attribute("href").startswith("http://localhost:%d" % port):
                raise RuntimeError("Native Home navigation link did not resolve to the site origin")
            preview = page.locator(".stbb-go-schedule-sample-media img")
            if preview.count() != 1 or not preview.evaluate("image => image.complete && image.naturalWidth > 0 && image.currentSrc.includes('social-preview-1280.png')"):
                raise RuntimeError("Approved, self-contained social preview did not load in the media pattern")
            if page.evaluate("document.documentElement.scrollWidth > innerWidth + 1"):
                raise RuntimeError("Published page overflows the narrow viewport")
            page.locator("main p").first.evaluate("element => element.textContent = 'longword'.repeat(70)")
            if page.evaluate("document.documentElement.scrollWidth > innerWidth + 1"):
                raise RuntimeError("Long unbroken text overflows the narrow viewport")
            page.reload(wait_until="networkidle")
            front_token = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--wp--preset--color--stbb-go-schedule-cue-action').trim()")
            if not front_token:
                raise RuntimeError("Published page lacks generated action preset")
            axe_source = ROOT / "site" / "node_modules" / "axe-core" / "axe.min.js"
            if not axe_source.is_file():
                raise RuntimeError("Install the locked site dependencies before the WordPress AA check")
            page.add_script_tag(path=str(axe_source))
            findings = page.evaluate("async () => await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] } })")
            (fixture_root / ("axe-%s.json" % version)).write_text(json.dumps({"violations": findings["violations"]}, indent=2) + "\n", encoding="utf-8")
            if findings["violations"]:
                raise RuntimeError("WordPress starter AA violations: %s" % [item["id"] for item in findings["violations"]])
            page.locator(".wp-block-button__link").first.focus()
            page.keyboard.press("Tab")
            if page.evaluate("getComputedStyle(document.activeElement).outlineStyle") == "none":
                raise RuntimeError("Keyboard focus indicator is missing")
            card_border = page.evaluate("""() => {
                const card = document.createElement('div');
                card.className = 'wp-block-group is-style-stbb-go-schedule-card';
                document.querySelector('main').append(card);
                const style = getComputedStyle(card);
                const result = [style.borderTopWidth, style.borderTopStyle, style.borderTopColor];
                card.remove();
                return result;
            }""")
            if card_border[0] != "1px" or card_border[1] != "solid" or card_border[2] in ("transparent", "rgba(0, 0, 0, 0)"):
                raise RuntimeError("Generated card border has invalid width or color: %s" % card_border)
            dark = json.loads((ROOT / "dist" / "go-schedule" / "wordpress" / "theme" / "stbb-go-schedule" / "styles" / "dark.json").read_text(encoding="utf-8"))
            dark_palette = {item["slug"]: item["color"] for item in dark["settings"]["color"]["palette"]}
            dark_focus = dark_palette["stbb-go-schedule-focus-ring"]
            dark_background = dark_palette["stbb-go-schedule-surface-background"]
            if Color(dark_focus).contrast(dark_background, method="wcag21") < 3:
                raise RuntimeError("Dark variation focus indicator falls below 3:1")
            dark_outline = page.evaluate("""async hex => {
                const variable = '--wp--preset--color--stbb-go-schedule-focus-ring';
                document.documentElement.style.setProperty(variable, hex);
                document.body.style.setProperty(variable, hex);
                const site = document.querySelector('.wp-site-blocks');
                site.style.setProperty(variable, hex);
                const control = document.querySelector('.wp-block-button__link');
                control.focus();
                await new Promise(resolve => setTimeout(resolve, 250));
                const actual = getComputedStyle(control).outlineColor;
                const sample = document.createElement('div');
                sample.style.color = hex;
                document.body.append(sample);
                const expected = getComputedStyle(sample).color;
                sample.remove();
                document.documentElement.style.removeProperty(variable);
                document.body.style.removeProperty(variable);
                site.style.removeProperty(variable);
                return [actual, expected];
            }""", dark_focus)
            if dark_outline[0] != dark_outline[1]:
                raise RuntimeError("Focus outline does not follow the selected dark variation: %s" % dark_outline)
            page.screenshot(path=str(fixture_root / ("front-%s-390.png" % version)), full_page=True)
            page.set_viewport_size({"width": 1440, "height": 900})
            wide_findings = page.evaluate("async () => await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] } })")
            (fixture_root / ("axe-wide-%s.json" % version)).write_text(json.dumps({"violations": wide_findings["violations"]}, indent=2) + "\n", encoding="utf-8")
            if wide_findings["violations"]:
                raise RuntimeError("Wide WordPress starter AA violations: %s" % [item["id"] for item in wide_findings["violations"]])
            page.screenshot(path=str(fixture_root / ("front-%s-1440.png" % version)), full_page=True)
            page.goto("http://localhost:%d/?s=stbb-no-results-fixture" % port, wait_until="networkidle")
            if page.get_by_text("No matching results. Try another search.").count() == 0:
                raise RuntimeError("Native search empty state did not render")
            page.goto("http://localhost:%d/?cat=1" % port, wait_until="networkidle")
            if not page.locator("body").evaluate("body => body.classList.contains('archive')") or page.locator("main .wp-block-query").count() == 0:
                raise RuntimeError("Native category archive template did not render")
            page.goto("http://localhost:%d/?p=99999999" % port, wait_until="networkidle")
            if page.get_by_text("Page not found").count() == 0:
                raise RuntimeError("Native 404 template did not render")
            page.goto("http://localhost:%d/wp-login.php" % port)
            page.locator("#user_login").fill("admin")
            page.locator("#user_pass").fill("password")
            page.locator("#wp-submit").click()
            page.goto("http://localhost:%d/wp-admin/post.php?post=%d&action=edit" % (port, page_id), wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            editor_text = " ".join(frame.locator("body").inner_text(timeout=10000) for frame in page.frames if frame.locator("body").count())
            if "Tell your story" not in editor_text or "Get in touch" not in editor_text:
                raise RuntimeError("Native editor did not load saved pattern content")
            if "This block contains unexpected or invalid content" in editor_text or "Attempt recovery" in editor_text:
                raise RuntimeError("Native editor reported invalid generated blocks")
            editor_tokens = [frame.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--wp--preset--color--stbb-go-schedule-cue-action').trim()")
                             for frame in page.frames if frame.locator("body").count()]
            if front_token not in editor_tokens:
                raise RuntimeError("Editor and published action presets disagree")
            saved = page.evaluate("""async () => {
                const editor = wp.data.select('core/editor');
                const original = editor.getEditedPostContent();
                if (!original.includes('Replace this text with your own message.')) return false;
                wp.data.dispatch('core/editor').editPost({content: original.replace('Replace this text with your own message.', 'Updated in the Site Editor.')});
                await wp.data.dispatch('core/editor').savePost();
                return !wp.data.select('core/editor').isEditedPostDirty();
            }""")
            if not saved:
                raise RuntimeError("Native editor did not save the edited pattern page")
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            reopened = " ".join(frame.locator("body").inner_text(timeout=10000) for frame in page.frames if frame.locator("body").count())
            if "Updated in the Site Editor." not in reopened or "Attempt recovery" in reopened:
                raise RuntimeError("Edited native pattern did not reopen cleanly")
            page.screenshot(path=str(fixture_root / ("editor-%s.png" % version)), full_page=True)
            page.goto("http://localhost:%d/?page_id=%d" % (port, page_id), wait_until="networkidle")
            if page.get_by_text("Updated in the Site Editor.").count() == 0:
                raise RuntimeError("Saved editor change did not publish")
        finally:
            browser.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", choices=("6.9.9", "7.1.2"), required=True)
    args = parser.parse_args()
    version, php, port = next(pair for pair in PAIRS if pair[0] == args.pair)
    kit = ROOT / "dist" / "go-schedule"
    wp = kit / "wordpress"
    archive = wp / "go-schedule-stbb-theme.zip"
    if not archive.is_file():
        raise SystemExit("build go-schedule before the WordPress runtime fixture")
    fixture_root = ROOT / "dist" / "wordpress-runtime"
    fixture_root.mkdir(parents=True, exist_ok=True)
    update_archive = fixture_root / "go-schedule-stbb-theme-update.zip"
    with zipfile.ZipFile(str(archive)) as original, zipfile.ZipFile(str(update_archive), "w") as updated:
        for member in original.infolist():
            data = original.read(member.filename)
            if member.filename.endswith("/assets/css/stbb-content.css"):
                data += b"\n/* STBB_FIXTURE_UPDATED */\n"
            updated.writestr(member, data)
    config = fixture_root / ("wp-%s.json" % version)
    config.write_text(json.dumps({"core": "https://wordpress.org/wordpress-%s.zip" % version,
                                  "phpVersion": php, "port": port, "testsEnvironment": False,
                                  "mappings": {"wp-content/stbb-fixture": str(wp),
                                               "wp-content/stbb-fixture-update.zip": str(update_archive),
                                               "wp-content/stbb-probe.php": str(FIXTURE / "probe.php")}},
                                 indent=2) + "\n", encoding="utf-8")
    node = os.environ.get("GP_NODE") or shutil.which("node")
    if not node:
        raise SystemExit("Node.js is required for the pinned wp-env fixture")
    command = [node, str(FIXTURE / "node_modules" / "@wordpress" / "env" / "bin" / "wp-env"),
               "--config=" + str(config)]
    started = False
    try:
        print("Starting WordPress %s / PHP %s" % (version, php), flush=True)
        print(run(command + ["start"], timeout=1200)[-2000:], flush=True)
        started = True
        def cli(*values):
            return run(command + ["run", "cli", "wp"] + list(values), timeout=300)
        actual = cli("core", "version")
        if version not in actual:
            raise RuntimeError("WordPress fixture version mismatch: %s" % actual)
        cli("theme", "install", "/var/www/html/wp-content/stbb-fixture/" + archive.name, "--force")
        cli("theme", "activate", "stbb-go-schedule")
        page_id = None
        drift_records = []
        for phase in ("baseline", "updated", "rollback"):
            if phase == "updated":
                cli("theme", "install", "/var/www/html/wp-content/stbb-fixture-update.zip", "--force")
            elif phase == "rollback":
                cli("theme", "install", "/var/www/html/wp-content/stbb-fixture/" + archive.name, "--force")
            output = cli("eval-file", "/var/www/html/wp-content/stbb-probe.php", phase)
            expected = "STBB_PROBE_OK %s %s %s" % (phase, version, php)
            if expected not in output:
                raise RuntimeError("WordPress fixture assertion missing: %s\n%s" % (expected, output))
            drift_match = re.search(r"STBB_DRIFT (\{[^\r\n]+\})", output)
            if not drift_match:
                raise RuntimeError("WordPress fixture omitted the client-vs-generated drift report")
            drift_records.append(json.loads(drift_match.group(1)))
            if phase == "baseline":
                match = re.search(r"STBB_PAGE_ID (\d+)", output)
                if not match:
                    raise RuntimeError("WordPress fixture did not report a saved page ID")
                page_id = int(match.group(1))
        asset_uri = cli("eval", "add_filter( 'content_url', function( $url ) { return str_replace( 'http://localhost:%d/', 'http://localhost:%d/clients/site/', $url ); } ); echo get_theme_file_uri( 'assets/css/stbb-content.css' );" % (port, port))
        if "/clients/site/wp-content/themes/stbb-go-schedule/assets/css/stbb-content.css" not in asset_uri:
            raise RuntimeError("Non-root theme asset URL was not composed correctly: %s" % asset_uri)
        with urlopen("http://localhost:%d/wp-content/themes/stbb-go-schedule/assets/css/stbb-content.css" % port, timeout=20) as response:
            if response.status != 200 or b"focus-visible" not in response.read():
                raise RuntimeError("Published theme content CSS did not resolve")
        cli("eval", "update_option( 'permalink_structure', '' );")
        (fixture_root / ("drift-%s.json" % version)).write_text(json.dumps(drift_records, indent=2) + "\n", encoding="utf-8")
        browser_probe(port, page_id, fixture_root, version)
        print("WordPress %s / PHP %s: ZIP install, native patterns, update/rollback, non-root URL composition, and live asset fetch passed" % (version, php), flush=True)
    finally:
        if started:
            print(run(command + ["stop"], timeout=300)[-1000:], flush=True)


if __name__ == "__main__":
    main()
