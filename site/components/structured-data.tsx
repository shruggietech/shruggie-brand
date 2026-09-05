import type { RouteRecord } from '@/lib/routes';

export function StructuredData({ route }: { route: RouteRecord }) {
  const payload = JSON.stringify(route.structuredData).replace(/</g, '\\u003c');
  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: payload }} />;
}
