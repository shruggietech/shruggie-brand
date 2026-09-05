import contract from '@/generated/routes.json';

export type RouteKind = 'home' | 'brand' | 'downloads' | 'guidelines' | 'docs-index' | 'docs-page';

export type RouteRecord = {
  key: string;
  kind: RouteKind;
  pathname: string;
  canonical: string;
  title: string;
  documentTitle: string;
  description: string;
  social: {
    path: string;
    url: string;
    width: number;
    height: number;
    type: 'image/png';
    alt: string;
    eyebrow: string;
  };
  breadcrumbs: Array<{ name: string; url: string }>;
  brandSlug: string | null;
  docsSlug: string | null;
  structuredData: Record<string, unknown>;
};

export const routeRecords = contract.routes as RouteRecord[];

export function normalizeRoutePath(pathname: string): string {
  const path = pathname.split(/[?#]/, 1)[0];
  if (!path.startsWith('/') || path.includes('..') || path.includes('\\')) throw new Error(`Unsafe route path: ${pathname}`);
  return path === '/' || path.endsWith('/') ? path : `${path}/`;
}

export function routeByPath(pathname: string): RouteRecord {
  const normalized = normalizeRoutePath(pathname);
  const route = routeRecords.find((candidate) => candidate.pathname === normalized);
  if (!route) throw new Error(`Missing generated route contract for ${normalized}`);
  return route;
}
