# ShruggieTech migration notes

The parent brand source was migrated from `A:\_tmp\branding\shruggietech-brand`.

- No vector mark exists in the supplied kit, `_ds_bundle.js`, or the authoritative CDN index. Tracing the paid antialiased PNG would change its geometry, so the source PNG masks remain authoritative and generated SVGs embed those masks without tracing.
- The four logo PNGs are committed as necessary source binaries. This is a ground-truth exception to the source-tree preference for font binaries only.
- Bright green `#2BCC73` measures 1.98:1 on the light reading surface and cannot be used there for text or links. The migrated kit uses accessible green `#037B40`, which measures 5.05:1. Bright green remains the signature identity color on dark surfaces and in exempt logo artwork.
- The parent uses the `direct-witty` register and accepts the shruggie flourish for at most one restrained moment per view.
- The original README and React UI source are retained. The canonical build does not depend on the legacy compiled design-system bundle.
- Generated exports are rebuilt by CI and are not committed here.

See [`../../LICENSE-BRAND`](../../LICENSE-BRAND) for the reserved brand-asset terms.
