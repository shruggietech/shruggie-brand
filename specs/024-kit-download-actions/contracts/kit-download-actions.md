# Contract: Kit Downloads and Portfolio Actions

## Archive contract

For every public production brand, site preparation MUST publish:

```text
/<slug>/downloads/<slug>-brand-<brand-version>.zip
```

The archive is byte-identical to the corresponding release archive created from the same verified inputs. Its entries are deterministically ordered and carry stable timestamps, regular-file permissions, and compression settings. The archive contains the complete verified kit tree plus canonical `LICENSE`, `NOTICE`, and `LICENSE-BRAND.md` when those files are not already present.

Publication fails before destination replacement when identity/version/canon metadata disagrees, a required file is absent, an entry path is unsafe or duplicated, manifest coverage is incomplete, a byte count or SHA-256 hash differs, or a repository license differs.

## Generated portfolio record

Each public record MUST expose:

```json
{
  "guidelinesPath": "/<slug>/guidelines/",
  "kitArchive": "/<slug>/downloads/<slug>-brand-<brand-version>.zip",
  "kitArchiveFilename": "<slug>-brand-<brand-version>.zip"
}
```

These fields are derived from the same slug and version that were verified inside the archive. No hand-authored homepage URL map is permitted.

## Desktop interaction contract

- The card container is an article, not a link or button.
- Resting content contains mark, name, and descriptor.
- Hover or focus within reveals exactly `Guidelines` and `Download Kit`, in that order, inside the descriptor's reserved region.
- The actions target the generated guidelines and archive paths. Download Kit declares the generated filename through the anchor download attribute.
- Unused space, mark, name, and descriptor do not navigate.
- Revealing actions does not change the outer card bounds or grid position.
- Reduced motion removes animated displacement.

## Mobile interaction contract

- Each public brand maps to one native disclosure.
- The collapsed summary contains only the mark and name.
- The expanded panel contains descriptor, Guidelines, and Download Kit, in that order.
- The summary has a visible focus indicator and at least a 44 by 44 CSS-pixel target.
- Closed panel anchors are not visible, clickable, or sequentially focusable.
- The mobile and desktop variants use the same generated record and exact destinations.

## Vendor-boundary contract

- An asterisk appears only beside a brand with a generated `vendorBoundary`.
- The marker carries screen-reader text and references the portfolio vendor notice.
- Exactly one vendor-notice aside appears after the complete portfolio list.
- The aside contains each unique applicable generated notice without paraphrase.
- No card or disclosure repeats a vendor-boundary paragraph.

## Verification contract

- Python tests prove archive determinism, safety, completeness, verification-before-replacement, production inventory, and site publication.
- Source tests prove exact labels, non-interactive card containers, native disclosure, generated destinations, download filenames, and one disclaimer source.
- Rendered tests prove pointer and keyboard action reveal, fixed desktop geometry, mobile disclosure/focus behavior, breakpoint changes, 200% zoom, reduced motion, WCAG AA, archive response type, and ZIP signature.
