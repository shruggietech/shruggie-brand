import Link from 'next/link';
import { conformanceRecords } from '@/lib/conformance';
import { pageMetadata } from '@/lib/metadata';
import { routeByPath } from '@/lib/routes';
import { StructuredData } from '@/components/structured-data';

const route = routeByPath('/conformance/');
export const metadata = pageMetadata(route);

export default function ConformanceIndex() {
  return <div className="shell conformance-page"><StructuredData route={route} /><header className="hero"><p className="eyebrow">Interface compiler proof</p><h1>Cross-host conformance</h1><p className="lede">Inspect every production brand against the same generated components, capability profiles, and evidence boundaries.</p></header><section className="section" aria-labelledby="brands-heading"><div className="section-heading"><div><p className="eyebrow">Browser references</p><h2 id="brands-heading">Production brands</h2></div><p>Native host fixtures remain distinct from browser evidence and product outcome claims.</p></div><div className="conformance-index-grid">{conformanceRecords.map((record) => <article key={record.slug}><h3>{record.title}</h3><p>Brand {record.brandVersion} · Conformance {record.contractVersion}</p><p>{record.recipes.length} recipes · {record.profiles.length} profiles · {record.hostTracks.length} host tracks</p><Link className="button" href={`/conformance/${record.slug}/`}>Open reference</Link></article>)}</div></section></div>;
}
