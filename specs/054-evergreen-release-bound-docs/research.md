# Research and Decisions

`documentation-contract.json` enumerates the 15 main-manual sources and routes. `prepare_site.py` derives MDX from those references and reads `release-impact.json` for its skill URL. Verified kit bundles already provide version, tag, status, and source revision through `publication_record()`. The tagged workflow checks exact revision and release status.

The README is a front door linked to the live site and latest release. The manual explains the system and may use bounded examples. Individual brand guidelines have a separate owner.

Editable page-version headers would recreate #265. A badge without content inventory would permit stale pages. A derived record with source/prepared hashes and existing release identity gives an exact comparison without a competing authority.

Main and PR builds are candidates. They must visibly say so even when prospective tag links are known. Tagged builds become releases only after exact-tag preflight.
