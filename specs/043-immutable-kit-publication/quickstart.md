# Quickstart: Immutable Kit Publication

## Focused contract loop

```powershell
python scripts/test_release_contract.py
python scripts/test_package_release.py
python scripts/test_prepare_site.py
python scripts/test_publication_workflow.py
python skill/templates/test_interface_contract.py
python skill/templates/test_documentation_contract.py
python skill/templates/test_conformance.py
pnpm --dir site lint
pnpm --dir site test
```

## Generate and inspect one kit

```powershell
python skill/templates/build.py brands/eso-weave/brand.json --out dist/eso-weave
python dist/eso-weave/verify.py
python dist/eso-weave/validate_glyph.py
```

Confirm that `dist/eso-weave/enforcement/bundle.json`, the manifest, consumer contract, migration guidance, and canonical archive filename agree. The brand version remains `1.0.0`; the package identity includes BrandBuilder `2.0.0`.

## Full repository gate

```powershell
python scripts/build_all.py
```

The aggregate gate must report zero verifier problems, zero glyph failures, a successful static site build, passing accessibility audits, passing publication checks, no generated artifacts in Git, no encoding corruption, and no production deployment path from untagged `main`.

## Release simulation boundary

Run release-contract and workflow tests against a synthetic exact tag context. Do not create or push a real tag. A valid simulation proves that release publication precedes Pages deployment and that every public destination is exact and immutable.
