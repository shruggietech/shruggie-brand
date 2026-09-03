import { notFound } from "next/navigation";
import brands from "../../../generated/brands.json";

export function generateStaticParams() {
  return brands.map((brand) => ({ slug: brand.slug }));
}

export default async function DownloadsPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const brand = brands.find((item) => item.slug === slug);
  if (!brand) notFound();
  const base = `/${brand.slug}/downloads/files`;
  return (
    <div className="shell">
      <p className="eyebrow">Verified artifacts</p>
      <h1>{brand.title} downloads</h1>
      <p className="lede">These files are copied from the same build that passed geometry, accessibility, rendering, and manifest checks.</p>
      <ul className="download-list">
        <li><a href={`${base}/${brand.slug}-brand-guide.pdf`}><strong>Brand guide</strong><br /><span className="meta">PDF</span></a></li>
        <li><a href={`${base}/logos/svg/${brand.slug}-mark-color.svg`}><strong>Logo mark</strong><br /><span className="meta">SVG master</span></a></li>
        <li><a href={`${base}/logos/svg/${brand.slug}-horizontal-color.svg`}><strong>Horizontal lockup</strong><br /><span className="meta">SVG master</span></a></li>
        <li><a href={`${base}/favicons/favicon.ico`}><strong>Favicon package</strong><br /><span className="meta">ICO entry point</span></a></li>
        <li><a href={brand.specimen}><strong>Type specimen</strong><br /><span className="meta">Outlined SVG</span></a></li>
        <li><a href={`/${brand.slug}/brand/r/theme.json`}><strong>shadcn theme</strong><br /><span className="meta">Registry JSON</span></a></li>
      </ul>
    </div>
  );
}
