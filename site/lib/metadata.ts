import type { Metadata } from 'next';
import type { RouteRecord } from '@/lib/routes';

export const siteUrl = 'https://brand.shruggie.tech';
export const siteDescription = 'Explore ShruggieTech brand identities, standards, assets, and the repeatable system behind them.';

export function pageMetadata(route: RouteRecord): Metadata {
  return {
    title: route.title,
    description: route.description,
    alternates: { canonical: route.canonical },
    openGraph: { type: 'website', url: route.canonical, title: route.documentTitle, description: route.description, siteName: 'ShruggieTech', images: [{ url: route.social.url, width: route.social.width, height: route.social.height, type: route.social.type, alt: route.social.alt }] },
    twitter: { card: 'summary_large_image', title: route.documentTitle, description: route.description, images: [{ url: route.social.url, alt: route.social.alt }] },
  };
}
