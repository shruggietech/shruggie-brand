import type { MetadataRoute } from 'next';
import { brands } from '@/lib/brands';
import { source } from '@/lib/source';
import { siteUrl } from '@/lib/metadata';

export const dynamic = 'force-static';
export default function sitemap(): MetadataRoute.Sitemap { const paths = ['/', ...brands.flatMap((brand) => [`/${brand.slug}/`, `/${brand.slug}/downloads/`, `/${brand.slug}/guidelines/`]), ...source.getPages().map((page) => page.url)]; return paths.map((path) => ({ url: new URL(path, siteUrl).toString(), changeFrequency: 'weekly', priority: path === '/' ? 1 : .7 })); }
