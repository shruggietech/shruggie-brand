import { notFound } from 'next/navigation';
import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import type { ReactNode } from 'react';
import { guidelineBySlug, guidelineTree } from '@/lib/guidelines';

export default async function GuidelineLayout({ children, params }: { children: ReactNode; params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const portal = guidelineBySlug(slug);
  if (!portal) notFound();
  return <DocsLayout tree={guidelineTree(portal)} nav={{ title: <span className="guide-nav-title"><strong>{portal.brand.title}</strong><small>Brand guidelines</small></span>, url: `/${slug}/guidelines/`, transparentMode: 'none' }} searchToggle={{ enabled: false }} themeSwitch={{ enabled: false }} sidebar={{ defaultOpenLevel: 1 }} containerProps={{ className: 'guideline-layout' }}>{children}</DocsLayout>;
}
