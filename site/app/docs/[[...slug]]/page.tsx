import { source } from '@/lib/source';
import { DocsBody, DocsDescription, DocsPage, DocsTitle } from 'fumadocs-ui/page';
import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import { getMDXComponents } from '@/mdx-components';
import { pageMetadata } from '@/lib/metadata';
import { routeByPath } from '@/lib/routes';
import { StructuredData } from '@/components/structured-data';
import { DocumentationNoScriptNav } from '@/components/hierarchy-no-script';
import { documentationPagination } from '@/lib/documentation';

export default async function Page({ params }: { params: Promise<{ slug?: string[] }> }) { const page = source.getPage((await params).slug); if (!page) notFound(); const route = routeByPath(page.url); const MDX = page.data.body; return <DocsPage id="content" className="docs-page" toc={page.data.toc} full={page.data.full} footer={{ className: 'docs-pagination', items: documentationPagination(route.pathname) }}><StructuredData route={route} /><DocumentationNoScriptNav currentPath={route.pathname} /><DocsTitle>{page.data.title}</DocsTitle><DocsDescription>{page.data.description}</DocsDescription><DocsBody><MDX components={getMDXComponents()} /></DocsBody></DocsPage>; }
export function generateStaticParams() { return source.generateParams(); }
export async function generateMetadata({ params }: { params: Promise<{ slug?: string[] }> }): Promise<Metadata> { const page = source.getPage((await params).slug); if (!page) notFound(); return pageMetadata(routeByPath(page.url)); }
