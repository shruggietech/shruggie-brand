# Custom Asset Contract

The manifest is the only source of public custom asset inventory. All records are fully validated, including private records, because their committed source and ownership claims must be sound. Public output requires both an approved status and explicit publication eligibility. A `publication_eligible: true` record without approved status is rejected, not silently published.

`source.path` is a brand-relative file under the committed brand tree. Absolute paths, URI schemes, `..`, backslash escapes, symlink escapes, missing files, query strings, fragments, wrong magic/extension, stale SHA-256, active SVG, and unsupported public formats fail validation. A source used by `authoritative_inputs` may be referenced without altering that record. The public kit retains the eligible source at its declared path, and the hosted download mirror copies those bytes unchanged.

Every published record appears once in the PDF, portable gallery, hosted Expressions and atmosphere topic, and the asset library/download inventory. No topic or category exists for an empty eligible set. Public previews are contained, never cropped or recolored; their declared well gives adequate text/control contrast. Attribution and license accompany each downloadable entry.
