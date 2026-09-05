# Legacy staging disposition

S005 retired the private migration workspace on 2026-09-04 after verifying its pre-disposition archive, governed repository sources, provenance records, live site, and published v1.1.2 release. The execution inventory contained 19 top-level entries and 2,481 files. Every entry below reached a verified recoverable destination, the source workspace finished with zero files and zero directories, and no item was permanently deleted.

Exact source roots, destination roots, archive identity, provider identifiers, and recovery commands are retained only in the operator-held private recovery record.

## Disposition ledger

| Entry | Classification | Governed coverage verified before movement | Destination class | Recoverability | Final state |
| --- | --- | --- | --- | --- | --- |
| Historical artifact collection | Generated dry runs, comparisons, early marks, and screenshots | Nine files were covered byte-for-byte by the pre-disposition archive; the collection is intentionally excluded from Git | Governed cold storage | Cold-storage copy plus verified archive | Verified moved |
| Private skill workspace | Legacy 41-file skill, upload bundle, portable bundle, and source transport bundle | All 41 non-cache files are represented by the newer 45-file governed `skill/` tree; v1.1.2 publishes both supported distributions | Recoverable deletion staging | Verified archive and governed source/release | Verified moved |
| Disposable build runtime | Virtual environment, dependency tree, smoke output, and SVG wrapper | Staged helper behavior matches `skill/templates/rsvg-convert.js`; dependencies regenerated and completed the six-target full-tier build | Recoverable deletion staging | Verified archive and reproducible dependencies | Verified moved |
| Private session output | Two generated visual documents | Both files are archive-covered and intentionally remain outside the public repository | Governed cold storage | Cold-storage copy plus verified archive | Verified moved |
| Covarity research | Unrelated architecture research | Owning-repository destination was unavailable; archive coverage was exact | Governed cold storage | Cold-storage copy plus verified archive | Verified moved |
| `covarity-brand` directory | Superseded generated kit | Governed `brands/covarity/` source rebuilt with zero problems and zero glyph failures; v1.1.2 contains the current verified archive | Recoverable deletion staging | Verified archive, governed source, and release | Verified moved |
| `covarity-brand.zip` snapshot | Superseded generated snapshot | Current Covarity release asset was independently verified | Recoverable deletion staging | Verified archive and release | Verified moved |
| `fragcap-brand` directory | Superseded generated kit with historical construction source | Governed source rebuilt cleanly; 13 construction files and three master SVGs match `docs/provenance/fragcap/` byte-for-byte; v1.1.2 contains the current archive | Recoverable deletion staging | Verified archive, governed source/provenance, and release | Verified moved |
| `fragcap-brand.zip` snapshot | Superseded generated snapshot | Current Fragcap release asset was independently verified | Recoverable deletion staging | Verified archive and release | Verified moved |
| `glitchpad-brand` directory | Superseded generated kit | Governed `brands/glitchpad/` source rebuilt with zero problems and zero glyph failures; v1.1.2 contains the current verified archive | Recoverable deletion staging | Verified archive, governed source, and release | Verified moved |
| `glitchpad-brand.zip` snapshot | Superseded generated snapshot | Current Glitchpad release asset was independently verified | Recoverable deletion staging | Verified archive and release | Verified moved |
| `go-schedule-brand` directory | Superseded generated kit | Governed `brands/go-schedule/` source and provenance rebuilt with zero problems and zero glyph failures; v1.1.2 contains the current verified archive | Recoverable deletion staging | Verified archive, governed source/provenance, and release | Verified moved |
| `go-schedule-brand.zip` snapshot | Superseded generated snapshot | Current Go Schedule release asset was independently verified | Recoverable deletion staging | Verified archive and release | Verified moved |
| Go Schedule release research | Unrelated installer and checksum research | The owning repository exists but no collision-free governed research destination was established; archive coverage was exact | Governed cold storage | Cold-storage copy plus verified archive | Verified moved |
| `shruggietech-brand` directory | Superseded legacy kit | Governed `brands/shruggietech/` source and raster-mask provenance rebuilt with zero problems and zero glyph failures; v1.1.2 contains the current verified archive | Recoverable deletion staging | Verified archive, governed source/provenance, and release | Verified moved |
| `shruggietech-brand.zip` snapshot | Superseded generated snapshot | Current ShruggieTech release asset was independently verified | Recoverable deletion staging | Verified archive and release | Verified moved |
| First parent-brand CSS source | Provenance source | Byte-identical to `docs/provenance/shruggietech/shruggietech-styles1.css` and referenced by the canon/accessibility decision record | Recoverable deletion staging | Verified archive and governed provenance | Verified moved |
| Second parent-brand CSS source | Provenance source | Byte-identical to `docs/provenance/shruggietech/shruggietech-styles2.css` and referenced by the canon/accessibility decision record | Recoverable deletion staging | Verified archive and governed provenance | Verified moved |
| Operator work directive | Private operational source of requirements | Requirements were translated into the public phase and issue hierarchy; the original remains private and archive-covered | Governed cold storage | Cold-storage copy plus verified archive | Verified moved |

## Verification summary

- The archive contained 2,479 files. Every archived file matched its live counterpart by normalized path, byte count, and SHA-256, with zero archived-only files and zero differences.
- Two live-only files were generated Python bytecode caches. Their governed source templates were archive-covered and remain in `skill/templates/`; the caches were classified as reproducible, non-authoritative runtime content.
- All five production brands and the fixture completed a full-tier clean rebuild. Every `verify.py` result reported zero problems, every `validate_glyph.py` result reported zero failures, image and PDF QC reported zero problems, and pagination reported zero split elements.
- Seventeen generated contact sheets were inspected together. No new identity, layout, contrast, or reduction defect was observed.
- The HTTPS site and all five production registry catalogs returned successful valid responses. The published v1.1.2 release remained public with exactly two skill distributions and five production-kit archives.
- Every move used an exact resolved source under the intended workspace, an exact destination under one approved recovery class, and a collision-free destination. Post-move fingerprints matched for 19 of 19 entries.

## GitHub traceability

This ledger supplies the shared evidence for Phase 1 issues #41 and #42, Phase 10 issues #76 through #86, parents #6 and #15, program #37, and S005 issue #95. Toolchain-specific evidence for #39 and review/CI evidence remain in the S005 evidence ledger. These items remain open until the reviewed S005 change reaches `main` and their current-main state policies are satisfied.
