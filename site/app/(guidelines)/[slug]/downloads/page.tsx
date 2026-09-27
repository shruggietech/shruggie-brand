import { notFound } from 'next/navigation';
import { LegacyRouteBridge } from '@/components/legacy-route-bridge';
import { guidelineBySlug, guidelinePortals } from '@/lib/guidelines';
import { siteUrl } from '@/lib/metadata';

export function generateStaticParams() { return guidelinePortals.map((portal) => ({ slug: portal.brand.slug })); }

function assetsPath(slug: string) { return guidelineBySlug(slug)?.topics.find((topic) => topic.key === 'assets')?.path; }

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const path = assetsPath((await params).slug);
  if (!path) notFound();
  return { title: 'Assets moved', robots: { index: false, follow: true }, alternates: { canonical: `${siteUrl}${path}` } };
}

export default async function Downloads({ params }: { params: Promise<{ slug: string }> }) {
  const path = assetsPath((await params).slug);
  if (!path) notFound();
  return <LegacyRouteBridge destination={path} label="Assets" />;
}
