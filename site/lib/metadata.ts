import type { Metadata } from 'next';

export const siteUrl = 'https://brand.shruggie.tech';
export const siteDescription = 'Explore ShruggieTech brand identities, standards, assets, and the repeatable system behind them.';

export function pageMetadata(title: string, description: string, path = '/'): Metadata {
  const url = new URL(path, siteUrl).toString();
  return {
    title,
    description,
    alternates: { canonical: url },
    openGraph: { type: 'website', url, title: `${title} | ShruggieTech`, description, siteName: 'ShruggieTech', images: [{ url: '/social-preview.png', width: 1280, height: 640, type: 'image/png', alt: 'ShruggieTech brand portfolio' }] },
    twitter: { card: 'summary_large_image', title: `${title} | ShruggieTech`, description, images: ['/social-preview.png'] },
  };
}
