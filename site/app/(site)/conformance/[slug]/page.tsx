import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { conformanceBySlug, conformanceRecords } from '@/lib/conformance';
import { pageMetadata } from '@/lib/metadata';
import { routeByPath } from '@/lib/routes';
import { StructuredData } from '@/components/structured-data';
import { ConformanceReference } from '@/components/conformance-reference';
import { brandBySlug } from '@/lib/brands';

export const dynamicParams = false;
export function generateStaticParams() { return conformanceRecords.map((record) => ({ slug: record.slug })); }
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> { const { slug } = await params; const record = conformanceBySlug(slug); if (!record) notFound(); return pageMetadata(routeByPath(`/conformance/${slug}/`)); }

export default async function ConformancePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params; const record = conformanceBySlug(slug); const brand = brandBySlug(slug); if (!record || !brand) notFound(); const route = routeByPath(`/conformance/${slug}/`);
  return <div className="shell conformance-page"><StructuredData route={route} /><header className="hero"><p className="eyebrow">Generated browser reference</p><h1>{record.title} interface conformance</h1><p className="lede">Exact source {record.sourceRevision.slice(0, 12)}, brand {record.brandVersion}, conformance contract {record.contractVersion}.</p>{brand.vendorBoundary ? <p className="vendor-boundary">{brand.vendorBoundary}</p> : null}</header><ConformanceReference record={record} /></div>;
}
