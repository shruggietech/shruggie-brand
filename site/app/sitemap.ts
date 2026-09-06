import type { MetadataRoute } from 'next';
import { routeRecords } from '@/lib/routes';

export const dynamic = 'force-static';
export default function sitemap(): MetadataRoute.Sitemap { return routeRecords.map((route) => ({ url: route.canonical, changeFrequency: 'weekly', priority: route.pathname === '/' ? 1 : .7 })); }
