#!/usr/bin/env python3
"""Validate every generated registry and install its advertised items in a clean consumer."""

from __future__ import annotations

import argparse
import functools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skill" / "templates"))
from registry_contract import validate_registry


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


class RegistryServer(ThreadingHTTPServer):
    request_queue_size = 128
    daemon_threads = True

    def handle_error(self, *_args):
        pass


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def run(command, cwd: Path, timeout: int = 300) -> str:
    executable = shutil.which(command[0])
    if not executable:
        raise RuntimeError("missing consumer tool: %s" % command[0])
    env = dict(os.environ, CI="1", NEXT_TELEMETRY_DISABLED="1", npm_config_yes="true")
    kwargs = {"cwd": str(cwd), "env": env, "stdin": subprocess.DEVNULL,
              "stdout": subprocess.PIPE, "stderr": subprocess.STDOUT,
              "text": True, "encoding": "utf-8", "errors": "replace", "timeout": timeout}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        startup = subprocess.STARTUPINFO()
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        kwargs["startupinfo"] = startup
    result = subprocess.run([executable, *command[1:]], **kwargs)
    if result.returncode:
        raise RuntimeError("%s failed (%d):\n%s" % (" ".join(command), result.returncode, result.stdout[-5000:]))
    return result.stdout


def inspect_kits(kits: Path, site: Optional[Path] = None):
    brands = sorted(path for path in kits.iterdir() if (path / "brand.json").is_file())
    expected = {path.parent.name for path in (ROOT / "brands").glob("*/brand.json")}
    if {path.name for path in brands} != expected:
        raise ValueError("kit inventory does not match production brands")
    inventories = {}
    for kit in brands:
        registry = kit / "nextjs" / "registry"
        validate_registry(registry, kit.name)
        catalog = json.loads((registry / "registry.json").read_text(encoding="utf-8"))
        inventories[kit.name] = catalog["items"]
        helper = (kit / "nextjs" / "fonts.ts").read_text(encoding="utf-8")
        faces = re.findall(r'path: "\.\./([^"]+)"', helper)
        if not faces or any(not face.startswith("fonts/") or not (kit / face).is_file() for face in faces):
            raise ValueError("%s: generated local font helper has a missing face" % kit.name)
        if "next/font/local" not in helper or "next/font/google" in helper:
            raise ValueError("%s: generated font helper does not use local faces" % kit.name)
        if site:
            public = site / kit.name / "brand" / "r"
            original = {path.name: path.read_bytes() for path in registry.glob("*.json")}
            published = {path.name: path.read_bytes() for path in public.glob("*.json")}
            if original != published:
                raise ValueError("%s: exported registry inventory differs from generated kit" % kit.name)
    return inventories


def consumer_fixture(directory: Path) -> None:
    write(directory / "package.json", json.dumps({
        "name": "s052-registry-consumer", "version": "0.0.0", "private": True,
        "scripts": {"build": "next build", "typecheck": "tsc --noEmit"},
        "dependencies": {"next": "16.3.5", "react": "19.3.0", "react-dom": "19.3.0",
                         "tailwindcss": "4.3.3", "@tailwindcss/postcss": "4.3.3"},
        "devDependencies": {"typescript": "7.0.2", "@types/node": "26.6.2",
                            "@types/react": "19.3.0", "@types/react-dom": "19.3.0"}}, indent=2) + "\n")
    write(directory / "components.json", json.dumps({
        "$schema": "https://ui.shadcn.com/schema/components.json", "style": "new-york", "rsc": True,
        "tsx": True, "iconLibrary": "lucide", "tailwind": {"config": "", "css": "app/globals.css",
        "baseColor": "neutral", "cssVariables": True}, "aliases": {"components": "@/components",
        "utils": "@/lib/utils", "ui": "@/components/ui", "lib": "@/lib", "hooks": "@/hooks"}}, indent=2) + "\n")
    write(directory / "tsconfig.json", json.dumps({"compilerOptions": {"target": "ES2017", "lib": ["dom", "esnext"],
        "allowJs": False, "skipLibCheck": True, "strict": True, "noEmit": True,
        "esModuleInterop": True, "module": "esnext", "moduleResolution": "bundler", "jsx": "react-jsx",
        "paths": {"@/*": ["./*"]}}, "include": ["**/*.ts", "**/*.tsx"]}, indent=2) + "\n")
    write(directory / "postcss.config.mjs", 'export default { plugins: { "@tailwindcss/postcss": {} } };\n')
    write(directory / "next.config.mjs", 'export default { output: "export" };\n')
    write(directory / "global.d.ts", 'declare module "*.css";\n')
    write(directory / "app" / "globals.css", '@import "tailwindcss";\n')


def install_consumer(kits: Path, inventories: dict) -> None:
    with tempfile.TemporaryDirectory(prefix="s052-consumer-") as temporary:
        consumer = Path(temporary) / "consumer"
        consumer.mkdir()
        consumer_fixture(consumer)
        handler = functools.partial(QuietHandler, directory=str(kits))
        server = RegistryServer(("127.0.0.1", 0), handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            base = "http://127.0.0.1:%d" % server.server_address[1]
            namespace = "@shruggietech"
            template = "%s/shruggietech/nextjs/registry/{name}.json" % base
            run(["npx", "--yes", "shadcn@4.21.0", "registry", "add", namespace + "=" + template], consumer)
            discovered = run(["npx", "--yes", "shadcn@4.21.0", "search", namespace, "--json"], consumer)
            if '"theme"' not in discovered:
                raise ValueError("pinned CLI did not discover the theme from the catalog")
            run(["npx", "--yes", "shadcn@4.21.0", "add", "-y", namespace + "/theme"], consumer, timeout=300)
            urls = []
            ui_items = []
            for slug, items in inventories.items():
                for item in items:
                    if item["type"] == "registry:ui":
                        if slug == "shruggietech" and item["name"] == "project-row":
                            run(["npx", "--yes", "shadcn@4.21.0", "add", "-y", namespace + "/project-row"], consumer)
                        else:
                            urls.append("%s/%s/nextjs/registry/%s.json" % (base, slug, item["name"]))
                        ui_items.append((slug, item))
            for start in range(0, len(urls), 4):
                run(["npx", "--yes", "shadcn@4.21.0", "add", "-y", *urls[start:start + 4]], consumer, timeout=300)
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=10)
        css = (consumer / "app" / "globals.css").read_text(encoding="utf-8")
        theme = inventories["shruggietech"][0]
        if any(value not in css for value in (theme["cssVars"]["light"]["background"], theme["cssVars"]["dark"]["background"])):
            raise ValueError("CLI did not install both theme token sets")
        for slug, item in ui_items:
            for source in item["files"]:
                target = source["target"].replace("@components/", "components/")
                installed = consumer / target
                if not installed.is_file() or source["content"].strip() not in installed.read_text(encoding="utf-8"):
                    raise ValueError("CLI did not install %s/%s at %s" % (slug, item["name"], target))
        kit = kits / "shruggietech"
        shutil.copytree(kit / "fonts", consumer / "fonts")
        (consumer / "nextjs").mkdir()
        shutil.copy2(kit / "nextjs" / "fonts.ts", consumer / "nextjs" / "fonts.ts")
        write(consumer / "app" / "layout.tsx", 'import "./globals.css";\nimport { fontVariables } from "../nextjs/fonts";\nimport type { ReactNode } from "react";\nexport default function Layout({ children }: { children: ReactNode }) { return <html lang="en" className={fontVariables}><body>{children}</body></html> }\n')
        write(consumer / "app" / "page.tsx", 'import { ProjectRow } from "../components/shruggietech/project-row";\nexport default function Page() { return <main><h1>Registry consumer</h1><div role="table"><ProjectRow name="Project" category="Brand" status="Ready" repository="repo" owner="Owner" updated_at="Today" /></div></main> }\n')
        run(["npm", "install", "--ignore-scripts", "--no-audit", "--no-fund"], consumer, timeout=600)
        run(["npm", "run", "typecheck"], consumer, timeout=300)
        run(["npm", "run", "build"], consumer, timeout=600)
        html = (consumer / "out" / "index.html").read_text(encoding="utf-8")
        if "Registry consumer" not in html or "Project" not in html:
            raise ValueError("representative installed component did not render")
        print("pinned shadcn CLI installed %d UI items, theme tokens, and local-font consumer build" % len(ui_items))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kits", type=Path, default=ROOT / "dist")
    parser.add_argument("--site", type=Path)
    parser.add_argument("--inventory-only", action="store_true")
    args = parser.parse_args()
    inventories = inspect_kits(args.kits, args.site)
    print("validated %d production registry catalogs and local font bundles" % len(inventories))
    if not args.inventory_only:
        install_consumer(args.kits, inventories)


if __name__ == "__main__":
    main()
