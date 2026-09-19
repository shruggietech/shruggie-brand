# Quickstart: Validate Documentation Contract Boundaries

Run from the repository root with the documented Python, Node, rendering, and site dependencies installed.

## 1. Contract and projection checks

```powershell
python skill/templates/test_documentation_contract.py
python skill/templates/test_interface_contract.py
python skill/templates/test_pipeline.py
python scripts/test_prepare_site.py
```

Expected: documentation schema, source ownership, topic coverage, navigation, route dispositions, shared facts, offline guidance, hosted projection, deterministic output, unsafe paths, and drift rejection all pass.

## 2. Build every production kit

```powershell
python scripts/build_all.py
```

Expected: all eight production brands report `BUILD CLEAN`, zero `verify.py` problems, zero glyph failures, complete offline implementation guidance, and exact documentation facts. Generated output remains under ignored `dist/`.

## 3. Inspect one offline contract

```powershell
python skill/templates/verify.py dist/glitchpad
python skill/templates/validate_glyph.py dist/glitchpad/brand.json
```

Expected: `dist/glitchpad/enforcement/consumer-contract.json`, `documentation-facts.json`, `IMPLEMENTATION.md`, and delivered recovery bytes resolve locally; both commands report zero failures.

## 4. Build and verify the documentation site

```powershell
pnpm --dir site lint
pnpm --dir site build
pnpm --dir site test
```

Expected: the expanded `/docs/` hierarchy, every hosted child-brand summary, all preserved routes, semantic graphics, no-script navigation, internal links, responsive conditions, and WCAG 2.1 AA checks pass.

## 5. Verify publication and repository hygiene

```powershell
python scripts/audit_publication_artifacts.py --kits dist --site site/out
python scripts/check_markdown.py
git status --short
```

Expected: publication contains exactly the governed production brands and documentation surfaces, Markdown passes, and no generated kit, site export, PDF, raster, archive, registry, synthetic fixture, or `.specify/feature.json` is staged.
