# ESO Weave Brand System

**Status:** Gate 1 and Gate 2 approved, production publication authorized

**Ownership:** Independent third-party identity

**Service credit:** Brand system by ShruggieTech

ESO Weave is a cross-platform, offline-first desktop companion for The Elder Scrolls Online. It runs beside the game and provides focus-scoped combat weaving, PixelBeacon-assisted fishing and Auto Potion, and a live status interface. It does not read or write game memory or inspect game network traffic.

Combat weaving combines a configured skill press with a basic attack while ESO is focused. Fishing can cast, observe a bite, reel, and recast. Auto Potion can use the active quickslot when a watched resource is low. PixelBeacon supplies the visible screen telemetry used by Fishing, Auto Potion, weapon-bar timing, and latency adaptation.

## Identity

The badge-less woven glyph is the authoritative full mark for dark identity surfaces. The existing rounded badge is the authoritative reduced mark and the required light-surface form. Both SVG sources are embedded unchanged. Horizontal and stacked lockups add an outlined Inter SemiBold wordmark. Single-ink reproduction preserves the approved source centerlines, stroke widths, caps, joins, and silhouette without adding a crossing overlay or knockout.

Do not edit, normalize, trace, simplify, recolor, or replace the authoritative paths. Do not use the badge-less glyph directly on light surfaces. Do not combine the ESO Weave and ShruggieTech marks into one lockup.

## Color

- Teal `#2DD4BF` identifies active game or application state and emphasis on dark surfaces.
- Gold `#F2B03C` belongs to the authoritative artwork and dark wordmark.
- Accessible gold `#986000` carries actions and the wordmark accent on the light surface `#F7F5F0`.
- Ink `#0E1116` is the primary surface. Primary text is `#E6EDF3` on dark and `#14110B` on light.

Bright gold is not legal text on the light surface. Use the accessible gold token there. Status must also include text or shape, and every interactive control requires a visible focus indicator.

## Typography

Inter is fixed for display, body, and interface copy at the delivered 400, 500, and 600 weights. Geist Mono 400 is reserved for identifiers, timestamps, event output, and technical metadata. All faces are local and routine generation requires no network access.

## Voice

Lead with the current game or application state, the available capability, or the safety condition governing an action. Use direct procedural language. State limitations and uncertainty plainly. Never claim official game support, authorization by game terms, protection from account action, or concealed behavior.

## Vendor and trademark boundary

ESO Weave is an independent third-party project and is not affiliated with, endorsed by, maintained by, or supported by ZeniMax Online Studios, ZeniMax Media Inc., Bethesda Softworks, or Microsoft. The Elder Scrolls and related marks are property of ZeniMax Media Inc. Users are responsible for applicable terms and consequences.

## Kit entry points

- `brand.json` is the machine-readable source contract and approval ledger.
- `SKILL.md` is the compact agent-facing contract.
- `ui_kits/eso-weave-desktop/` is the representative desktop specimen.
- Generated assets, guidelines, registries, platform suites, and PDFs are produced under `dist/` and are never committed.
