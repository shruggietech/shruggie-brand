#!/usr/bin/env python3
"""Focused tests for production-only site materialization."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from PIL import Image

import prepare_site
from brand_contract import derivative_configuration_sha256


def write_minimal_portal(source: Path, slug: str = "alpha", title: str = "Alpha") -> None:
    guideline = source / "guidelines"
    guideline.mkdir(parents=True, exist_ok=True)
    (guideline / "index.html").write_text("<!doctype html><title>Portable guide</title>\n", encoding="utf-8")
    (guideline / "portal.json").write_text(json.dumps({
        "schema_version": "1.0",
        "brand": {"slug": slug, "title": title, "descriptor": "Alpha.", "idea": "Alpha.", "affiliation": ""},
        "topics": [
            {"key": "overview", "title": "Overview and foundations", "label": "Overview", "section": "Overview", "order": 0, "path": f"/{slug}/guidelines/", "description": "Start here."},
            {"key": "voice", "title": "Voice and messaging", "label": "Voice", "section": "Voice", "order": 0, "path": f"/{slug}/guidelines/voice/", "description": "Voice."},
            {"key": "logos", "title": "Logo system and usage", "label": "Logo", "section": "Identity", "order": 0, "path": f"/{slug}/guidelines/logos/", "description": "Logo."},
            {"key": "color", "title": "Color", "label": "Color", "section": "Identity", "order": 1, "path": f"/{slug}/guidelines/color/", "description": "Palette."},
            {"key": "typography", "title": "Typography", "label": "Typography", "section": "Identity", "order": 2, "path": f"/{slug}/guidelines/typography/", "description": "Type."},
            {"key": "components", "title": "Components and examples", "label": "Components", "section": "Components", "order": 0, "path": f"/{slug}/guidelines/components/", "description": "Components."},
            {"key": "assets", "title": "Assets", "label": "Assets", "section": "Assets", "order": 0, "path": f"/{slug}/downloads/", "description": "Downloads."},
            {"key": "integration", "title": "Platform integration", "label": "Integration", "section": "Integration", "order": 0, "path": f"/{slug}/guidelines/integration/", "description": "Integration."},
        ],
        "content": {"overview": {}, "voice": {}, "logos": {}, "typography": {}, "components": {}},
        "palettes": {"dark": [], "light": []},
        "asset_families": [], "resources": [], "instructions": [], "capability_suites": [], "aliases": {},
        "portable_guide": "guidelines/index.html",
    }) + "\n", encoding="utf-8")


class PrepareSiteTests(unittest.TestCase):
    def test_cueson_source_exposes_only_the_approved_public_surface_set(self):
        path = prepare_site.ROOT / "brands" / "cueson" / "brand.json"
        brand = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual("Universal captions and subtitles", brand["brand_idea"])
        self.assertEqual(
            "A lossless, structured interchange layer for subtitle and caption content.",
            brand["descriptor"],
        )
        self.assertEqual("public", brand["affiliation"]["showcase"])
        self.assertEqual(
            {"showcase-card", "brand-landing-page", "guideline-topics", "downloads",
             "registry-endpoints", "public-metadata", "structured-data", "social-preview"},
            set(brand["approval_ledger"]["gate_2"]["surfaces"]),
        )
        self.assertTrue(prepare_site.public_showcase(brand))

    def test_i_heart_pr_tours_source_exposes_every_approved_public_surface(self):
        path = prepare_site.ROOT / "brands" / "i-heart-pr-tours" / "brand.json"
        brand = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual("third-party", brand["affiliation"]["ownership"])
        self.assertEqual("public", brand["affiliation"]["showcase"])
        self.assertEqual("approved", brand["approval_ledger"]["gate_2"]["status"])
        self.assertEqual("repository owner", brand["approval_ledger"]["gate_2"]["approved_by"])
        self.assertEqual("2026-09-11", brand["approval_ledger"]["gate_2"]["approved_on"])
        self.assertEqual(
            "9aae47141e989c34ea64e460a3594179192e2443012e15922dd3f6e49bccd41b",
            brand["approval_ledger"]["gate_2"]["derivative_manifest_sha256"],
        )
        self.assertEqual(
            {"showcase-card", "brand-landing-page", "guideline-topics", "downloads",
             "registry-endpoints", "public-metadata", "structured-data", "social-preview"},
            set(brand["approval_ledger"]["gate_2"]["surfaces"]),
        )
        self.assertTrue(prepare_site.public_showcase(brand))
        self.assertEqual("https://brand.shruggie.tech/i-heart-pr-tours/brand", brand["registry_base"])
        self.assertEqual("#FFFFFF", prepare_site.showcase_surface(brand))
        self.assertIn("I Heart PR Tours owns its trademarks", brand["vendor_boundary"]["notice"])

    def test_copy_kit_emits_only_explicit_governed_showcase_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "kit"
            public = root / "public"
            for name in ("guidelines", "nextjs/registry", "logos/svg", "favicons", "icons", "specimens"):
                (source / name).mkdir(parents=True, exist_ok=True)
            write_minimal_portal(source)
            (source / "brand-guide.pdf").write_bytes(b"%PDF-test")
            (source / "specimens" / "sample.svg").write_text("<svg/>\n", encoding="utf-8")
            public.mkdir()
            original_public = prepare_site.PUBLIC
            prepare_site.PUBLIC = public
            archive_writer = mock.patch.object(prepare_site, "write_brand_archive").start()
            try:
                brand = {
                    "slug": "alpha", "title": "Alpha", "kind": "sub-brand",
                    "descriptor": "Alpha.", "brand_idea": "Alpha.", "version": "1.0.0",
                    "accent": {"bright": "#FFD900", "accessible": "#867100"},
                    "surfaces": {"card": "#121416"},
                    "affiliation": {"ownership": "shruggietech-owned", "showcase": "public", "parent": "ShruggieTech", "inheritance": "shruggietech-house", "endorsement": "shruggietech-project", "service_credit": "none"},
                }
                record = prepare_site.copy_kit(source, brand)
                self.assertNotIn("showcaseSurface", record)
                self.assertNotIn("showcaseForeground", record)
                self.assertEqual("/alpha/guidelines/", record["guidelinesPath"])
                self.assertEqual("/alpha/downloads/alpha-brand-1.0.0.zip", record["kitArchive"])
                self.assertEqual("alpha-brand-1.0.0.zip", record["kitArchiveFilename"])
                self.assertEqual("1.2.1", archive_writer.call_args.kwargs["expected_canon"])
                brand["showcase_surface"] = "card"
                record = prepare_site.copy_kit(source, brand)
                self.assertEqual("#121416", record["showcaseSurface"])
                self.assertEqual("#FFFFFF", record["showcaseForeground"])
                brand["surfaces"]["card"] = "#F4F5F6"
                record = prepare_site.copy_kit(source, brand)
                self.assertEqual("#000000", record["showcaseForeground"])
                brand["vendor_boundary"] = {"required": True, "notice": "Acme is independent. Users are responsible.", "entities": ["Acme"], "trademark_owner": "Acme", "terms_responsibility": "Users are responsible."}
                record = prepare_site.copy_kit(source, brand)
                self.assertEqual(brand["vendor_boundary"]["notice"], record["vendorBoundary"])
                self.assertNotIn("vendorBoundarySummary", record)
                self.assertEqual(4, archive_writer.call_count)
            finally:
                mock.patch.stopall()
                prepare_site.PUBLIC = original_public

    def test_authoritative_canon_is_not_derived_from_brand_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reference = root / "skill" / "references"
            reference.mkdir(parents=True)
            (reference / "01-canon.json").write_text('{"version":"9.4.0"}\n', encoding="utf-8")
            self.assertEqual("9.4.0", prepare_site.authoritative_canon(root))

    def test_showcase_permission_is_independent_and_fail_closed(self):
        brand = {"kind": "sub-brand", "affiliation": {"ownership": "third-party", "showcase": "private", "parent": None, "inheritance": "independent", "endorsement": "none", "service_credit": "none"}}
        self.assertFalse(prepare_site.public_showcase(brand))
        brand["affiliation"]["showcase"] = "public"
        self.assertTrue(prepare_site.public_showcase(brand))
        brand["approval_ledger"] = {
            "source_hashes": {"mark": "a" * 64},
            "gate_1": {"status": "approved", "approved_by": "owner", "approved_on": "2026-09-07", "scope": sorted(["reduced-and-platform", "horizontal-lockup", "stacked-lockup", "wordmark-only", "single-ink"]), "derivative_config_sha256": ""},
            "gate_2": {"status": "pending", "approved_by": None, "approved_on": None, "derivative_manifest_sha256": None, "surfaces": []},
        }
        brand["approval_ledger"]["gate_1"]["derivative_config_sha256"] = derivative_configuration_sha256(brand)
        self.assertFalse(prepare_site.public_showcase(brand))
        brand["approval_ledger"]["gate_2"] = {"status": "approved", "approved_by": "owner", "approved_on": "2026-09-07", "derivative_manifest_sha256": "b" * 64, "surfaces": ["showcase-card", "brand-landing-page", "guideline-topics", "downloads", "registry-endpoints", "public-metadata", "structured-data", "social-preview"]}
        self.assertTrue(prepare_site.public_showcase(brand))
        brand["affiliation"]["showcase"] = "private"
        brand["approval_ledger"]["gate_2"]["surfaces"] = []
        with self.assertRaisesRegex(ValueError, "must be published"):
            prepare_site.public_showcase(brand)
        brand["affiliation"]["showcase"] = "public"
        brand["approval_ledger"]["gate_2"]["surfaces"] = ["showcase-card"]
        with self.assertRaisesRegex(ValueError, "complete public surface"):
            prepare_site.public_showcase(brand)
        del brand["affiliation"]["showcase"]
        with self.assertRaisesRegex(ValueError, "exactly"):
            prepare_site.public_showcase(brand)

    def test_source_dirs_require_exact_production_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp)
            for slug in ("alpha", "stale"):
                target = dist / slug
                target.mkdir()
                (target / "brand.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unexpected.*stale"):
                prepare_site.source_dirs(dist, {"alpha"})
            (dist / "stale" / "brand.json").unlink()
            self.assertEqual([path.name for path in prepare_site.source_dirs(dist, {"alpha"})], ["alpha"])

    def test_source_dirs_reject_missing_production_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "missing.*alpha"):
                prepare_site.source_dirs(Path(tmp), {"alpha"})

    def test_source_identity_requires_matching_unique_slug(self):
        source = Path("alpha")
        with self.assertRaisesRegex(ValueError, "must match"):
            prepare_site.validate_source_identity(source, {"slug": "beta"}, set())
        seen = {"alpha"}
        with self.assertRaisesRegex(ValueError, "duplicate"):
            prepare_site.validate_source_identity(source, {"slug": "alpha"}, seen)

    def test_portal_projection_rewrites_safe_downloads_and_rejects_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "alpha"
            asset = source / "icons" / "web" / "favicon.svg"
            asset.parent.mkdir(parents=True)
            asset.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>\n', encoding="utf-8")
            write_minimal_portal(source)
            payload = json.loads((source / "guidelines" / "portal.json").read_text(encoding="utf-8"))
            delivery = {"path": "icons/web/favicon.svg", "format": "svg", "role": "web-icon", "platform": "web", "appearance": "default", "width": 32, "height": 32, "destination": "Web root", "sha256": hashlib.sha256(asset.read_bytes()).hexdigest()}
            payload["asset_families"] = [{"key": "web", "title": "Web icons", "summary": "For browsers.", "assets": [{"id": "web-icon", "title": "Web icon", "role": "web-icon", "platform": "web", "appearance": "default", "surface": "dark", "summary": "Use in browsers.", "formats": ["svg"], "variants": ["reduced"], "preview": dict(delivery), "deliveries": [delivery]}]}]
            projected = prepare_site.project_portal(source, payload)
            self.assertEqual("/alpha/downloads/files/icons/web/favicon.svg", projected["asset_families"][0]["assets"][0]["preview"]["url"])
            self.assertEqual("/alpha/downloads/files/icons/web/favicon.svg", projected["asset_families"][0]["assets"][0]["deliveries"][0]["url"])
            payload["resources"] = [{"id": "duplicate", "title": "Duplicate", "resource_kind": "code-or-container", **delivery}]
            with self.assertRaisesRegex(ValueError, "duplicate portal delivery"):
                prepare_site.project_portal(source, payload)

    def test_instruction_markdown_becomes_safe_semantic_blocks(self):
        blocks = prepare_site.markdown_blocks("# Web icons\n\nUse `favicon.svg`.\n\n- Copy the file\n- Keep the name\n\n| Path | Use |\n| --- | --- |\n| `favicon.svg` | Preferred |\n\n```xml\n<link rel=\"icon\">\n```\n")
        self.assertEqual(["heading", "paragraph", "list", "table", "code"], [block["type"] for block in blocks])
        self.assertEqual("favicon.svg", blocks[1]["segments"][1]["text"])
        self.assertEqual(["Path", "Use"], blocks[3]["headers"])
        self.assertEqual("xml", blocks[4]["language"])
        for unsafe in ("[bad](javascript:alert(1))", "[escape](../../outside.txt)"):
            with self.assertRaisesRegex(ValueError, "unsafe Markdown link"):
                prepare_site.markdown_blocks(unsafe)

    def test_topic_routes_are_generated_for_every_portal_topic(self):
        brands = [{"slug": "alpha", "title": "Alpha", "descriptor": "Alpha identity.", "icon": "/alpha/mark.svg", "accent": "#2BCC73"}]
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "alpha"
            write_minimal_portal(source)
            portals = [json.loads((source / "guidelines" / "portal.json").read_text(encoding="utf-8"))]
        routes = prepare_site.build_routes(brands, [], portals)
        guide_routes = [route for route in routes if route["kind"] in {"guidelines", "guidelines-topic"}]
        self.assertEqual(["/alpha/guidelines/", "/alpha/guidelines/voice/", "/alpha/guidelines/logos/", "/alpha/guidelines/color/", "/alpha/guidelines/typography/", "/alpha/guidelines/components/", "/alpha/guidelines/integration/"], [route["pathname"] for route in guide_routes])
        self.assertEqual(["overview", "voice", "logos", "color", "typography", "components", "integration"], [route["guideTopic"] for route in guide_routes])
        self.assertFalse(any(route["kind"] == "brand" or route["pathname"] in {"/alpha/", "/alpha/guidelines/assets/"} for route in routes))
        self.assertEqual("assets", next(route for route in routes if route["kind"] == "downloads")["guideTopic"])

    def test_vendor_boundary_reaches_routes_metadata_and_structured_data(self):
        notice = "Acme is independent. Users are responsible."
        brands = [{"slug": "alpha", "title": "Alpha", "descriptor": "Alpha identity.", "icon": "/alpha/mark.svg", "accent": "#2BCC73", "vendorBoundary": notice}]
        route = next(item for item in prepare_site.build_routes(brands, []) if item["kind"] == "guidelines")
        self.assertEqual(notice, route["vendorBoundary"])
        self.assertEqual("https://brand.shruggie.tech/alpha/guidelines/", route["vendorBoundaryUrl"])
        entity = next(item for item in route["structuredData"]["@graph"] if item.get("@type") == "Brand")
        self.assertEqual(notice, entity["disambiguatingDescription"])
        self.assertEqual(route["vendorBoundaryUrl"], entity["usageInfo"])

    def test_stale_generated_public_brand_is_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            public = Path(tmp)
            stale = public / "stale"
            (stale / "brand" / "r").mkdir(parents=True)
            (stale / "downloads" / "files").mkdir(parents=True)
            (stale / "brand" / "r" / "registry.json").write_text("{}\n", encoding="utf-8")
            unrelated = public / "unrelated"
            unrelated.mkdir()
            self.assertEqual(prepare_site.remove_stale_public_brands(public, {"alpha"}), ["stale"])
            self.assertFalse(stale.exists())
            self.assertTrue(unrelated.exists())

    def test_guideline_metadata_is_complete_and_absolute(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "index.html"
            page.write_text("<html><head><title>Guide</title></head><body><span data-host-exit></span></body></html>", encoding="utf-8")
            brands = [{"slug": "alpha", "title": "Alpha", "descriptor": "One & only.", "icon": "/alpha/mark.svg", "accent": "#2BCC73"}]
            route = next(item for item in prepare_site.build_routes(brands, []) if item["kind"] == "guidelines")
            prepare_site.add_guideline_metadata(page, route)
            content = page.read_text(encoding="utf-8")
            self.assertIn("<title>Alpha guidelines | ShruggieTech</title>", content)
            self.assertIn('rel="canonical" href="https://brand.shruggie.tech/alpha/guidelines/"', content)
            self.assertIn('property="og:title"', content)
            self.assertIn('property="og:image:width" content="1280"', content)
            self.assertIn('property="og:image:alt" content="Alpha guidelines page preview on Brands | ShruggieTech"', content)
            self.assertIn('name="twitter:card"', content)
            self.assertIn('type="application/ld+json"', content)
            self.assertIn('"BreadcrumbList"', content)
            self.assertIn("One &amp; only.", content)

    def test_guideline_publication_rewrites_validated_assets_and_adds_one_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "alpha"
            page = root / "guidelines" / "index.html"
            asset = root / "downloads" / "files" / "logos" / "mark.svg"
            page.parent.mkdir(parents=True); asset.parent.mkdir(parents=True)
            asset.write_text("<svg/>", encoding="utf-8")
            page.write_text('<html><head><title>Guide</title></head><body><a data-kit-asset href="../logos/mark.svg">mark</a><span data-host-exit></span></body></html>', encoding="utf-8")
            brands = [{"slug": "alpha", "title": "Alpha", "descriptor": "Guide.", "icon": "/alpha/mark.svg", "accent": "#2BCC73"}]
            route = next(item for item in prepare_site.build_routes(brands, []) if item["kind"] == "guidelines")
            prepare_site.add_guideline_metadata(page, route)
            content = page.read_text(encoding="utf-8")
            self.assertIn('href="/alpha/downloads/files/logos/mark.svg"', content)
            self.assertEqual(1, content.count('class="host-exit"'))
            self.assertIn('>All brands</a>', content)

    def test_guideline_publication_rejects_unsafe_or_missing_assets(self):
        brands = [{"slug": "alpha", "title": "Alpha", "descriptor": "Guide.", "icon": "/alpha/mark.svg", "accent": "#2BCC73"}]
        route = next(item for item in prepare_site.build_routes(brands, []) if item["kind"] == "guidelines")
        for href in ("../../secret.txt", "../logos/missing.svg"):
            with self.subTest(href=href), tempfile.TemporaryDirectory() as tmp:
                page = Path(tmp) / "alpha" / "guidelines" / "index.html"
                page.parent.mkdir(parents=True)
                page.write_text('<html><head><title>Guide</title></head><body><a data-kit-asset href="%s">bad</a><span data-host-exit></span></body></html>' % href, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "guideline asset"):
                    prepare_site.add_guideline_metadata(page, route)

    def test_public_markdown_rewrites_prose_and_preserves_literal_code(self):
        source = "# Canon contract\n\nThe canon guides decisions for A ShruggieTech project.\n\n`canon` and `A ShruggieTech project` stay literal.\n\n```json\n{\"canon\": \"1.1.2\", \"endorsement\": \"A ShruggieTech project\"}\n```\n"
        title, body = prepare_site.derive_public_markdown(source)
        self.assertEqual(title, "Brand system contract")
        self.assertIn("The brand system guides decisions for Brand system by ShruggieTech.", body)
        self.assertIn("`canon` and `A ShruggieTech project` stay literal.", body)
        self.assertIn('{"canon": "1.1.2", "endorsement": "A ShruggieTech project"}', body)

    def test_public_markdown_promotes_explicit_alerts_only(self):
        source = """# Alerts

> [!NOTE]
> Probe before selecting a renderer.

> [!WARNING]
> Missing capabilities must remain visible.

> [!CAUTION]
> Never ship generated concept artwork.

> An ordinary blockquote stays a blockquote.

```markdown
> [!WARNING]
> Literal sample.
```
"""
        _, body = prepare_site.derive_public_markdown(source)
        self.assertIn('<Callout type="info">\nProbe before selecting a renderer.\n</Callout>', body)
        self.assertIn('<Callout type="warn">\nMissing capabilities must remain visible.\n</Callout>', body)
        self.assertIn('<Callout type="error">\nNever ship generated concept artwork.\n</Callout>', body)
        self.assertIn("> An ordinary blockquote stays a blockquote.", body)
        self.assertIn("> [!WARNING]\n> Literal sample.", body)

    def test_public_markdown_rejects_unsupported_alert_marker(self):
        with self.assertRaisesRegex(ValueError, "unsupported documentation alert"):
            prepare_site.derive_public_markdown("# Alerts\n\n> [!IMPORTANT]\n> Unsupported.\n")

    def test_public_markdown_promotes_multiline_alert(self):
        _, body = prepare_site.derive_public_markdown("# Alerts\n\n> [!NOTE]\n> First line.\n>\n> Second line.\n")
        self.assertIn('<Callout type="info">\nFirst line.\n\nSecond line.\n</Callout>', body)

    def test_write_docs_derives_frontmatter_navigation_and_source_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            references = root / "references"
            output = root / "generated"
            references.mkdir()
            (references / "00-start.md").write_text(
                "# Start here\n\nUse this reference.\n\n| A | B |\n| --- | --- |\n| one | two |\n",
                encoding="utf-8",
            )
            records = prepare_site.write_docs(references, output, {"00-start": "Start description."}, {"00-start": ("Foundation", 1, "Contract", 0)})
            self.assertEqual(records, [{"slug": "00-start", "title": "Start here", "description": "Start description.", "navigation": {"section": "Foundation", "sectionOrder": 1, "label": "Contract", "order": 0, "path": "/docs/00-start/", "paginationOrder": 1}}])
            page = (output / "00-start.mdx").read_text(encoding="utf-8")
            self.assertIn('title: "Start here"', page)
            self.assertIn("| one | two |", page)
            self.assertNotIn("# Start here", page)
            meta = json.loads((output / "meta.json").read_text(encoding="utf-8"))
            self.assertEqual("Documentation", meta["title"])
            self.assertEqual(meta["pages"], ["index", "00-start"])
            navigation = json.loads((output.parent / "documentation.json").read_text(encoding="utf-8"))
            self.assertEqual("Overview", navigation[0]["navigation"]["label"])
            self.assertEqual("Contract", navigation[1]["navigation"]["label"])
            self.assertEqual([0, 1], sorted(record["navigation"]["paginationOrder"] for record in navigation))
            index = (output / "index.mdx").read_text(encoding="utf-8")
            self.assertIn('title: "Documentation"', index)
            self.assertNotRegex(index, r"(?i)how we build(?: brands)?")

    def test_route_contract_is_complete_canonical_and_page_aware(self):
        brands = [{"slug": "alpha", "title": "Alpha", "descriptor": "Alpha identity.", "icon": "/alpha/mark.svg", "accent": "#2BCC73"}]
        docs = [{"slug": "04-toolchain", "title": "Toolchain", "description": "Tools and gates."}]
        routes = prepare_site.build_routes(brands, docs)
        self.assertEqual(5, len(routes))
        self.assertEqual(5, len({route["key"] for route in routes}))
        self.assertEqual(5, len({route["canonical"] for route in routes}))
        for route in routes:
            self.assertTrue(route["pathname"].startswith("/"))
            self.assertTrue(route["pathname"].endswith("/"))
            self.assertEqual(f"https://brand.shruggie.tech{route['pathname']}", route["canonical"])
            self.assertEqual(route["canonical"], route["structuredData"]["@graph"][2]["url"])
            self.assertNotEqual("ShruggieTech brand portfolio", route["social"]["alt"])
        doc = next(route for route in routes if route["kind"] == "docs-page")
        self.assertEqual(["Brands", "Documentation", "Toolchain"], [item["name"] for item in doc["breadcrumbs"]])
        docs_root = next(route for route in routes if route["kind"] == "docs-index")
        self.assertEqual("Documentation | ShruggieTech", docs_root["documentTitle"])
        self.assertEqual("TechArticle", doc["structuredData"]["@graph"][2]["@type"])
        brand = next(route for route in routes if route["kind"] == "guidelines")
        graph_text = json.dumps(brand["structuredData"])
        self.assertIn('"@type": "Brand"', graph_text)
        self.assertNotIn("owner", graph_text.lower())

    def test_registry_catalog_resolves_every_unique_typed_item(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            registry = source / "nextjs" / "registry"
            registry.mkdir(parents=True)
            brand = {"slug": "alpha", "registry_base": "https://brand.shruggie.tech/alpha/brand"}
            items = [{"name": "theme", "type": "registry:theme", "files": []}, {"name": "fonts", "type": "registry:font", "files": []}]
            (registry / "registry.json").write_text(json.dumps({"$schema": "https://ui.shadcn.com/schema/registry.json", "items": items}), encoding="utf-8")
            for item in items:
                (registry / f"{item['name']}.json").write_text(json.dumps({"$schema": "https://ui.shadcn.com/schema/registry-item.json", "name": item["name"], "type": item["type"]}), encoding="utf-8")
            prepare_site.validate_registry(source, brand)
            (registry / "fonts.json").unlink()
            with self.assertRaisesRegex(ValueError, "advertised registry item is missing"):
                prepare_site.validate_registry(source, brand)
            (registry / "fonts.json").write_text(json.dumps({"$schema": "https://ui.shadcn.com/schema/registry-item.json", "name": "fonts", "type": "registry:ui"}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "type mismatch"):
                prepare_site.validate_registry(source, brand)

    def test_route_contract_rejects_unsafe_or_duplicate_records(self):
        route = {"key": "duplicate", "kind": "home", "pathname": "/", "canonical": "https://brand.shruggie.tech/", "title": "Brands", "documentTitle": "Brands | ShruggieTech", "description": "Description", "social": {"path": "/social/duplicate.png", "url": "https://brand.shruggie.tech/social/duplicate.png", "width": 1280, "height": 640, "type": "image/png", "alt": "Preview", "eyebrow": "Portfolio"}, "breadcrumbs": [], "brandSlug": None, "docsSlug": None}
        with self.assertRaisesRegex(ValueError, "duplicate route key"):
            prepare_site.validate_routes([route, dict(route)])
        bad = dict(route, key="unsafe", pathname="/../escape/", canonical="https://brand.shruggie.tech/../escape/")
        with self.assertRaisesRegex(ValueError, "unsafe route pathname"):
            prepare_site.validate_routes([bad])
        external = dict(route, key="external", canonical="https://example.com/")
        with self.assertRaisesRegex(ValueError, "canonical URL"):
            prepare_site.validate_routes([external])
        unsafe_key = dict(route, key="../preview")
        with self.assertRaisesRegex(ValueError, "unsafe route key"):
            prepare_site.validate_routes([unsafe_key])
        unsafe_preview = dict(route, key="unsafe-preview", social=dict(route["social"], path="/social/../escape.png"))
        with self.assertRaisesRegex(ValueError, "unsafe social preview path"):
            prepare_site.validate_routes([unsafe_preview])
        wrong_dimensions = dict(route, key="wrong-dimensions", social=dict(route["social"], path="/social/wrong-dimensions.png", url="https://brand.shruggie.tech/social/wrong-dimensions.png", width=1200))
        with self.assertRaisesRegex(ValueError, "invalid social preview contract"):
            prepare_site.validate_routes([wrong_dimensions])

    def test_social_previews_are_rebuilt_with_exact_dimensions(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            public = root / "public"
            stale = public / "social" / "stale.png"
            stale.parent.mkdir(parents=True)
            Image.new("RGBA", (1, 1), (0, 0, 0, 0)).save(stale)
            mark = root / "mark.png"
            Image.new("RGBA", (200, 120), (43, 204, 115, 255)).save(mark)
            display_font = Path(__file__).resolve().parents[1] / "assets" / "fonts" / "ttf" / "SpaceGrotesk-Bold.ttf"
            body_font = Path(__file__).resolve().parents[1] / "assets" / "fonts" / "ttf" / "Geist-Medium.ttf"
            route = prepare_site.build_routes([], [])[0]
            prepare_site.generate_social_previews([route], public, mark, display_font, body_font)
            preview = public / route["social"]["path"].lstrip("/")
            self.assertFalse(stale.exists())
            with Image.open(preview) as image:
                self.assertEqual((1280, 640), image.size)
                self.assertEqual("RGBA", image.mode)

    def test_active_source_paths_do_not_reference_retired_fixture(self):
        root = Path(__file__).resolve().parents[1]
        active = [
            root / "README.md",
            root / ".gitignore",
            root / "scripts" / "build_all.py",
            root / "scripts" / "prepare_site.py",
            root / "skill" / "templates" / "test_pipeline.py",
            root / "site" / "app",
        ]
        needle = "example" + "-brand"
        found = []
        for target in active:
            paths = target.rglob("*") if target.is_dir() else [target]
            for path in paths:
                if path.is_file() and path.suffix in {".md", ".py", ".ts", ".tsx", ".css", ".json"}:
                    if needle in path.read_text(encoding="utf-8"):
                        found.append(str(path.relative_to(root)))
        self.assertEqual(found, [])

    def test_active_public_sources_do_not_reference_retired_labels(self):
        root = Path(__file__).resolve().parents[1]
        active = [root / "skill" / "references", root / "site" / "app", root / "site" / "components", root / "site" / "lib"]
        retired = [
            "how we " + "build brands",
            "how we " + "build",
            "the shruggietech " + "variance contract",
            "shruggietech " + "variance contract",
            "the " + "variance contract",
        ]
        found = []
        for target in active:
            for path in target.rglob("*"):
                if path.is_file() and path.suffix in {".md", ".mdx", ".ts", ".tsx", ".json"}:
                    content = path.read_text(encoding="utf-8").lower()
                    for phrase in retired:
                        if phrase in content:
                            found.append(f"{path.relative_to(root)}: {phrase}")
        self.assertEqual(found, [])

    def test_authoritative_variance_contract_title_is_canonical(self):
        root = Path(__file__).resolve().parents[1]
        source = root / "skill" / "references" / "00-variance-contract.md"
        self.assertEqual(source.read_text(encoding="utf-8").splitlines()[0], "# Variance Contract")

    def test_site_identity_requires_and_copies_generated_web_suite(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "kit"
            public = root / "public"
            web = source / "icons" / "web"
            logos = source / "logos" / "svg"
            logo_png = source / "logos" / "png"
            web.mkdir(parents=True)
            logos.mkdir(parents=True)
            logo_png.mkdir(parents=True)
            public.mkdir()
            (web / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"><rect width="1" height="1"/></svg>\n', encoding="utf-8")
            for name, size in (("favicon-16x16.png", 16), ("favicon-32x32.png", 32),
                               ("apple-touch-icon.png", 180), ("android-chrome-192x192.png", 192),
                               ("android-chrome-512x512.png", 512)):
                Image.new("RGBA", (size, size), (0, 0, 0, 255)).save(web / name)
            (web / "favicon.ico").write_bytes(b"\x00\x00\x01\x00test")
            (web / "site.webmanifest").write_text(json.dumps({
                "name": "ShruggieTech", "short_name": "ShruggieTech", "display": "standalone",
                "background_color": "#000000", "theme_color": "#000000",
                "icons": [{"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"}],
            }) + "\n", encoding="utf-8")
            (logos / "shruggietech-horizontal-color.svg").write_text('<svg data-appearance="colored-dark"/>\n', encoding="utf-8")
            (logos / "shruggietech-horizontal-light.svg").write_text('<svg data-appearance="colored-light"><path/></svg>\n', encoding="utf-8")
            Image.new("RGB", (1200, 630), (0, 0, 0)).save(logo_png / "shruggietech-social-preview-1280.png")

            prepare_site.copy_site_identity(source, public)

            self.assertEqual((web / "favicon.svg").read_bytes(), (public / "favicon.svg").read_bytes())
            self.assertEqual((web / "favicon.ico").read_bytes(), (public / "favicon.ico").read_bytes())
            self.assertEqual((logos / "shruggietech-horizontal-color.svg").read_bytes(), (public / "shruggietech-logo-dark.svg").read_bytes())
            self.assertEqual((logos / "shruggietech-horizontal-light.svg").read_bytes(), (public / "shruggietech-logo-light.svg").read_bytes())
            manifest = json.loads((public / "site.webmanifest").read_text(encoding="utf-8"))
            self.assertEqual("Brands | ShruggieTech", manifest["name"])
            self.assertEqual("#000000", manifest["background_color"])

    def test_site_identity_does_not_mask_missing_generated_assets(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "kit"
            public = root / "public"
            source.mkdir()
            public.mkdir()
            with self.assertRaisesRegex(ValueError, "generated site identity asset"):
                prepare_site.copy_site_identity(source, public)


if __name__ == "__main__":
    unittest.main(verbosity=2)
