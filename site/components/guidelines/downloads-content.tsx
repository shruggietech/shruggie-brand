import type { GuidelinePortal } from '@/lib/guidelines';
import type { Brand } from '@/lib/brands';
import { AssetLibrary } from './asset-library';

export function DownloadsContent({ brand, portal }: { brand: Brand; portal: GuidelinePortal }) {
  const root = `/${brand.slug}/downloads/files`;
  return <><section className="guide-section" aria-labelledby="direct-downloads"><h2 id="direct-downloads">Direct downloads</h2><ul className="download-list">
    <li><a href={brand.kitArchive} download={brand.kitArchiveFilename}><strong>Complete brand kit</strong><span>Verified archive containing every distributable delivery</span></a></li>
    <li><a href={`${root}/${brand.slug}-brand-guide.pdf`}><strong>Brand guide</strong><span>PDF standards and usage guidance</span></a></li>
    <li><a href={brand.portableGuide}><strong>Portable guidelines</strong><span>Standalone HTML reference for offline use</span></a></li>
    <li><a href={`${root}/logos/svg/${brand.slug}-mark-color.svg`}><strong>Logo mark</strong><span>Primary SVG master</span></a></li>
    <li><a href={`${root}/logos/svg/${brand.slug}-horizontal-color.svg`}><strong>Horizontal lockup</strong><span>Primary SVG master</span></a></li>
    <li><a href={`${root}/icons/manifest.json`}><strong>Application icon suites</strong><span>Web, Android, Apple, macOS, and Windows asset index</span></a></li>
    <li><a href={`${root}/icons/web/favicon.ico`}><strong>Web favicon bundle</strong><span>Classic multi-size browser ICO</span></a></li>
    <li><a href={`${root}/icons/windows/classic/app.ico`}><strong>Windows application icon</strong><span>Classic multi-size desktop ICO</span></a></li>
    <li><a href={brand.specimen}><strong>Type specimen</strong><span>Outlined SVG reference</span></a></li>
    <li><a href={`/${brand.slug}/brand/r/registry.json`}><strong>shadcn catalog</strong><span>Discover installable theme and component items</span></a></li>
    <li><a href={`/${brand.slug}/brand/r/theme.json`}><strong>shadcn theme</strong><span>Install with shadcn 4.21.0 in a Next.js and Tailwind v4 project</span></a></li>
  </ul><p>For a Next.js and Tailwind v4 project with shadcn, add the registry namespace and install the theme:</p><pre><code>{`npx shadcn@4.21.0 registry add @${brand.slug}=https://brand.shruggie.tech/${brand.slug}/brand/r/{name}.json\nnpx shadcn@4.21.0 add @${brand.slug}/theme`}</code></pre><p>The catalog lists direct theme and component endpoints. Confirm the theme by checking the light and dark variables in your global stylesheet. For local fonts, download the complete kit and copy <code>nextjs/fonts.ts</code> with its <code>fonts/</code> tree. The shadcn CLI does not install those files. Projects without shadcn can use the kit's vanilla CSS and assets directly.</p></section><section className="guide-section" aria-labelledby="asset-library"><h2 id="asset-library">Asset library</h2><AssetLibrary portal={portal} /></section></>;
}
