import { notFound } from 'next/navigation';
import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import type { HTMLAttributes, ReactNode } from 'react';
import { guidePresentationStyle, guidelineBySlug, guidelineTree } from '@/lib/guidelines';

export default async function GuidelineLayout({ children, params }: { children: ReactNode; params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const portal = guidelineBySlug(slug);
  if (!portal) notFound();
  const mode = portal.brand.surface_mode;
  const background = portal.presentation.background;
  if (!/^#[0-9A-Fa-f]{6}$/.test(background)) throw new Error(`${slug} lacks a valid guide background`);
  const containerProps = { className: 'guideline-layout', 'data-guide-mode': mode, style: guidePresentationStyle(portal) } as HTMLAttributes<HTMLDivElement>;
  return <>
    <style>{`html:has(.guideline-layout[data-guide-mode='${mode}']), body:has(.guideline-layout[data-guide-mode='${mode}']) { background: ${background}; color-scheme: ${mode}; }`}</style>
    <DocsLayout tree={guidelineTree(portal)} nav={{ title: <span className="guide-nav-title"><strong>{portal.brand.title}</strong><small>Brand guidelines</small></span>, url: `/${slug}/guidelines/`, transparentMode: 'none' }} searchToggle={{ enabled: false }} themeSwitch={{ enabled: false }} sidebar={{ defaultOpenLevel: 1 }} containerProps={containerProps}>{children}</DocsLayout>
  </>;
}
