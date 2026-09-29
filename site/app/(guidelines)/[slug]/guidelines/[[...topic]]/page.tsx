import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { DocsBody, DocsDescription, DocsPage, DocsTitle } from 'fumadocs-ui/page';
import { GuideFooter } from '@/components/guidelines/guide-footer';
import { TopicContent } from '@/components/guidelines/topic-content';
import { DownloadsContent } from '@/components/guidelines/downloads-content';
import { LegacyRouteBridge } from '@/components/legacy-route-bridge';
import { StructuredData } from '@/components/structured-data';
import { GuidelineNoScriptNav } from '@/components/hierarchy-no-script';
import { guidelineBySlug, guidelinePortals, guidelineTopic, topicToc } from '@/lib/guidelines';
import { brandBySlug } from '@/lib/brands';
import { pageMetadata, siteUrl } from '@/lib/metadata';
import { routeByPath } from '@/lib/routes';

type Params = { slug: string; topic?: string[] };
function resolve(params: Params) { const portal = guidelineBySlug(params.slug); if (!portal) return; const topic = guidelineTopic(portal, params.topic); if (!topic) return; return { portal, topic }; }
function legacyDestination(params: Params) {
  const portal = guidelineBySlug(params.slug);
  if (!portal) return;
  if (!params.topic?.length) return { path: portal.topics.find((topic) => topic.key === 'overview')?.path, label: 'Brand essentials' };
  if (params.topic.length === 1 && params.topic[0] === 'overview') return { path: portal.topics.find((topic) => topic.key === 'overview')?.path, label: 'Brand essentials' };
  if (params.topic.length === 1 && params.topic[0] === 'logos') return { path: portal.topics.find((topic) => topic.key === 'logos')?.path, label: 'Logo' };
}

export const dynamicParams = false;
export function generateStaticParams() { return guidelinePortals.flatMap((portal) => [...portal.topics.map((topic) => ({ slug: portal.brand.slug, topic: [topic.path.split('/').at(-2)!] })), { slug: portal.brand.slug, topic: [] }, { slug: portal.brand.slug, topic: ['overview'] }, { slug: portal.brand.slug, topic: ['logos'] }]); }
export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const value = await params;
  const legacy = legacyDestination(value);
  if (legacy?.path) return { title: `${legacy.label} moved`, robots: { index: false, follow: true }, alternates: { canonical: `${siteUrl}${legacy.path}` } };
  const resolved = resolve(value);
  if (!resolved) notFound();
  return pageMetadata(routeByPath(resolved.topic.path));
}

export default async function GuidelinePage({ params }: { params: Promise<Params> }) {
  const value = await params;
  const legacy = legacyDestination(value);
  if (legacy?.path) return <LegacyRouteBridge destination={legacy.path} label={legacy.label} />;
  const resolved = resolve(value);
  const brand = brandBySlug(value.slug);
  if (!resolved || !brand) notFound();
  const { portal, topic } = resolved;
  const route = routeByPath(topic.path);
  return <DocsPage id="content" className={`guideline-page${topic.key === 'assets' ? ' assets-page' : ''}`} toc={topicToc(portal, topic)} footer={{ enabled: false }} breadcrumb={{ enabled: false }} style={{ '--guide-accent': portal.presentation.primary } as React.CSSProperties}><StructuredData route={route} /><GuidelineNoScriptNav portal={portal} currentPath={topic.path} /><header className="guide-heading"><p className="guide-eyebrow">{portal.brand.title} guidelines</p><DocsTitle id="guide-title">{topic.key === 'assets' ? 'Assets' : topic.title}</DocsTitle><DocsDescription>{topic.description}</DocsDescription></header><DocsBody>{topic.key === 'assets' ? <DownloadsContent brand={brand} portal={portal} /> : <TopicContent portal={portal} topic={topic} />}</DocsBody>{portal.brand.affiliation && topic.key !== 'overview' && <p className="guide-affiliation">{portal.brand.affiliation}</p>}{portal.brand.vendorBoundary && <p className="vendor-boundary">{portal.brand.vendorBoundary}</p>}<GuideFooter /></DocsPage>;
}
