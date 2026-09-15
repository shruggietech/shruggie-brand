# Contract: Integration Preview Presentation

## Group classification

- A delivery group with at least one PNG or SVG is visual.
- When generic appearance requires measurement, the exact measured PNG delivery becomes the embedded preview delivery. If a group is SVG-only, the original SVG remains the embedded preview and a bounded rasterization is used only for scoring.
- A group with no PNG or SVG is nonvisual.
- A mixed group remains visual and lists nonvisual siblings exactly once in its delivery inventory.

## Visual well

A visual well MUST emit:

```html
<div class="preview light-well" data-preview-kind="visual" data-preview-surface="light" data-preview-basis="measured" data-preview-contrast="8.91">
  <span class="surface-label">Light surface</span>
  <img src="data:image/png;base64,..." alt="... preview">
</div>
```

The surface can be `light` or `dark`. When measurable output is available, `data-preview-basis` MUST be `measured`, `data-preview-contrast` MUST be finite, and the selected well MUST maximize significant-pixel coverage at 3:1 before using median contrast as a tie-breaker. A recognized black, white, light-target, or dark-target appearance can use `data-preview-basis="declared"` only when no measurable visual delivery is available. The affected I Heart PR Tours guide MUST record at least `3.00`; another approved asset whose intrinsic alpha cannot meet that threshold on either supported well MUST retain the stronger well and its honest measured score rather than being altered or blocking an unrelated kit. The decoded data URI MUST equal the selected delivery bytes. CSS MUST NOT apply `filter`, inversion, recoloring, cropping, or presentation transforms to the asset.

## Nonvisual well

A nonvisual well MUST emit no `<img>` and MUST use explicit resource semantics:

```html
<div class="preview nonvisual-well" data-preview-kind="nonvisual" data-preview-surface="nonvisual" data-preview-basis="nonvisual">
  <div class="nonvisual-resource"><strong>Nonvisual resource</strong><span>XML adaptive declaration</span></div>
</div>
```

Format labels distinguish at least JSON metadata, XML metadata or declaration, ICO container, and ICNS container. The resource role is included after humanization. The presentation MUST NOT call the resource an image preview.

## Color pairs

| Well | Background | Foreground | Minimum |
| --- | --- | --- | --- |
| Light | `#F5F5F5` | `#111111` | 4.5:1 text |
| Dark | `#090909` | `#F5F5F5` | 4.5:1 text |
| Nonvisual | `#F5F5F5` | `#111111` | 4.5:1 text |

Meaningful visual output MUST measure at least 3:1 against the selected light or dark background.

## Failure behavior

- A visual candidate with no meaningful visible pixels fails generation with a path-specific error.
- A generic visual group with no measurable candidate fails generation rather than using an unchecked surface.
- A measurable visual group for which neither supported well reaches 3:1 uses the stronger well and exposes the measured score; release acceptance enforces the threshold for the affected guide.
- Missing files and manifest dimension disagreements retain their existing fail-closed behavior.

## Preservation

- Source and delivery bytes are read-only.
- Base64 preview content is derived directly from `read_bytes()` on the selected delivery.
- Group IDs, download destinations, formats, dimensions, embedded sizes, and delivery inventory remain intact.
- Synthetic fixtures are created only under temporary test directories and are never production-discoverable.
