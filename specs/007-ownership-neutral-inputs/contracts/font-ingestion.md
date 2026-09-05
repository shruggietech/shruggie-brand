# Contract: Fixed Fonts and Controlled Ingestion

## Ordinary generation

Ordinary build, verification, documentation, release, and site commands read local files only. They do not call the ingestion command and do not open network connections. House mode resolves the repository's existing approved faces explicitly. Fixed mode resolves only declared approved faces.

## Controlled ingestion

The operator invokes `ingest_font.py` with a local source or HTTPS URL, expected SHA-256, destination under `assets/fonts/`, expected family, weight, style, license, and provenance. The command:

1. Validates request syntax and destination containment before reading data.
2. Streams at most the documented size limit into repository-independent temporary storage.
3. Rejects insecure schemes, unexpected redirects, short or oversized responses, and hash mismatch.
4. Opens the temporary binary with fontTools and compares format, family, weight, style, and unsupported variable axes.
5. Requires a non-empty reviewed license and public-safe provenance.
6. Places the file atomically only after every check succeeds.
7. Removes temporary state on success, rejection, or interruption.

An existing destination is unchanged on failure. Replacement requires an exact validated request and occurs atomically.

## Fixed-font generation

Every fixed family role declares its approved faces. Generated CSS, Next.js bindings, registry metadata, guideline HTML, PDF CSS, SVG specimens, logo wordmarks, and enforcement rules derive names, weights, styles, and local paths from this contract. Missing required faces fail instead of substituting house fonts or synthesizing a weight.

## Failure

Missing license, bad hash, wrong family, unsupported weight or style, corrupt binary, unsupported variable face, insecure source, destination escape, incomplete response, or partial request stops before approved placement or publication.
