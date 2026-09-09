import { notFound } from 'next/navigation';
import { DocsBody, DocsDescription, DocsPage, DocsTitle } from 'fumadocs-ui/page';
import { brands, brandBySlug } from '@/lib/brands';
import { guidelineBySlug } from '@/lib/guidelines';
import { pageMetadata } from '@/lib/metadata';
import { routeByPath } from '@/lib/routes';
import { StructuredData } from '@/components/structured-data';
import { DownloadsContent } from '@/components/guidelines/downloads-content';
import { GuideFooter } from '@/components/guidelines/guide-footer';
import { GuidelineNoScriptNav } from '@/components/hierarchy-no-script';

export function generateStaticParams() { return brands.map(({ slug }) => ({ slug })); }
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) { const brand = brandBySlug((await params).slug); if (!brand) notFound(); return pageMetadata(routeByPath(`/${brand.slug}/downloads/`)); }

export default async function Downloads({ params }: { params: Promise<{ slug: string }> }) {
  const brand = brandBySlug((await params).slug);
  const portal = guidelineBySlug((await params).slug);
  if (!brand || !portal) notFound();
  const route = routeByPath(`/${brand.slug}/downloads/`);
  return <DocsPage id="content" className="guideline-page assets-page" toc={[{ title: 'Direct downloads', url: '#direct-downloads', depth: 2 }, { title: 'Asset library', url: '#asset-library', depth: 2 }]} footer={{ enabled: false }} breadcrumb={{ enabled: false }} style={{ '--guide-accent': brand.accent } as React.CSSProperties}><StructuredData route={route} /><GuidelineNoScriptNav portal={portal} currentPath={`/${brand.slug}/downloads/`} /><header className="guide-heading"><p className="guide-eyebrow">{brand.title} guidelines</p><DocsTitle id="guide-title">Assets</DocsTitle><DocsDescription>Task-oriented access to every verified delivery.</DocsDescription></header><DocsBody><DownloadsContent brand={brand} portal={portal} /></DocsBody>{brand.vendorBoundary && <p className="vendor-boundary">{brand.vendorBoundary}</p>}<GuideFooter /></DocsPage>;
}
