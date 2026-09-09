import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { DocsBody, DocsDescription, DocsPage, DocsTitle } from 'fumadocs-ui/page';
import { GuideFooter } from '@/components/guidelines/guide-footer';
import { TopicContent } from '@/components/guidelines/topic-content';
import { StructuredData } from '@/components/structured-data';
import { GuidelineNoScriptNav } from '@/components/hierarchy-no-script';
import { guidelineBySlug, guidelinePortals, guidelineTopic, topicToc } from '@/lib/guidelines';
import { brandBySlug } from '@/lib/brands';
import { pageMetadata } from '@/lib/metadata';
import { routeByPath } from '@/lib/routes';

type Params = { slug: string; topic?: string[] };
function resolve(params: Params) { const portal = guidelineBySlug(params.slug); if (!portal) return; const topic = guidelineTopic(portal, params.topic); if (!topic || topic.key === 'assets') return; return { portal, topic }; }
function pathname(params: Params) { return params.topic?.length ? `/${params.slug}/guidelines/${params.topic[0]}/` : `/${params.slug}/guidelines/`; }

export const dynamicParams = false;
export function generateStaticParams() { return guidelinePortals.flatMap((portal) => portal.topics.filter((topic) => topic.key !== 'assets').map((topic) => ({ slug: portal.brand.slug, topic: topic.key === 'overview' ? [] : [topic.key] }))); }
export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> { const value = await params; if (!resolve(value)) notFound(); return pageMetadata(routeByPath(pathname(value))); }

export default async function GuidelinePage({ params }: { params: Promise<Params> }) {
  const value = await params;
  const resolved = resolve(value);
  const brand = brandBySlug(value.slug);
  if (!resolved || !brand) notFound();
  const { portal, topic } = resolved;
  const route = routeByPath(pathname(value));
  return <DocsPage id="content" className="guideline-page" toc={topicToc(portal, topic)} footer={{ enabled: false }} breadcrumb={{ enabled: false }} style={{ '--guide-accent': brand.accent } as React.CSSProperties}><StructuredData route={route} /><GuidelineNoScriptNav portal={portal} currentPath={topic.path} /><header className="guide-heading"><p className="guide-eyebrow">{portal.brand.title} guidelines</p><DocsTitle id="guide-title">{topic.title}</DocsTitle><DocsDescription>{topic.description}</DocsDescription></header><DocsBody><TopicContent portal={portal} topic={topic} /></DocsBody>{portal.brand.affiliation && <p className="guide-affiliation">{portal.brand.affiliation}</p>}{portal.brand.vendorBoundary && <p className="vendor-boundary">{portal.brand.vendorBoundary}</p>}<GuideFooter /></DocsPage>;
}
