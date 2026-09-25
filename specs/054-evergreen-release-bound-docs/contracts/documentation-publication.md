# Documentation Publication Contract

The generated record is written to `site/generated/documentation-publication.json`, copied to `site/public/docs/publication.json` for static export, and staged beside `PUBLICATION.json` in the release candidate.

The build derives version, tag, revision, status, and exact destinations from the existing publication record. It hashes the catalog, every declared skill reference, and every generated MDX page. The route set exactly matches the catalog plus `/docs/`.

Release preflight requires `status=release`, exact tag and revision, valid local source and prepared-page hashes, and equality with reference bytes in both released skill archives. The exported public record matches the staged record byte for byte. Missing, extra, duplicate, or unsafe paths fail. Candidate builds display candidate status.

Independent brand and technical-contract versions are unaffected. The manual never uses an unqualified `latest` skill download.
