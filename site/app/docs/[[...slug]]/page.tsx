import { source } from '@/lib/source';
import { DocsBody, DocsDescription, DocsPage, DocsTitle } from 'fumadocs-ui/page';
import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import { getMDXComponents } from '@/mdx-components';
import { Footer } from '@/components/footer';
import { pageMetadata } from '@/lib/metadata';
import { routeByPath } from '@/lib/routes';
import { StructuredData } from '@/components/structured-data';

export default async function Page({ params }: { params: Promise<{ slug?: string[] }> }) { const page = source.getPage((await params).slug); if (!page) notFound(); const route = routeByPath(page.url); const MDX = page.data.body; return <DocsPage id="content" className="docs-page" toc={page.data.toc} full={page.data.full}><StructuredData route={route} /><DocsTitle>{page.data.title}</DocsTitle><DocsDescription>{page.data.description}</DocsDescription><DocsBody><MDX components={getMDXComponents()} /></DocsBody><Footer /></DocsPage>; }
export function generateStaticParams() { return source.generateParams(); }
export async function generateMetadata({ params }: { params: Promise<{ slug?: string[] }> }): Promise<Metadata> { const page = source.getPage((await params).slug); if (!page) notFound(); return pageMetadata(routeByPath(page.url)); }
