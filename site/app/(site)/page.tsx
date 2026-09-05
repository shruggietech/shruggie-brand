import type { CSSProperties } from 'react';
import Link from 'next/link';
import { brands } from '@/lib/brands';
import { pageMetadata } from '@/lib/metadata';
import { routeByPath } from '@/lib/routes';
import { StructuredData } from '@/components/structured-data';

const route = routeByPath('/');
export const metadata = pageMetadata(route);

export default function Home() {
  return <div className="shell">
    <StructuredData route={route} />
    <section className="hero"><p className="eyebrow">Brand building by ShruggieTech</p><h1>We build comprehensive brands</h1><p className="lede">We shape distinct identities with a repeatable process, then ship the standards, assets, and tools that keep them coherent.</p><div className="actions"><a className="button primary" href="#portfolio">Explore the portfolio</a><a className="button" href="https://github.com/ShruggieTech/shruggie-brand/releases/latest">Download the skill</a></div><Link className="text-link" href="/docs">See how we build brands.</Link></section>
    <section className="section" id="portfolio" aria-labelledby="portfolio-heading"><div className="section-heading"><div><p className="eyebrow">Selected work</p><h2 id="portfolio-heading">Identity spectrum</h2></div><p>Distinct identities, each supported by a complete and reusable system.</p></div><div className="brand-grid">{brands.map((brand) => <Link className="brand-card" href={`/${brand.slug}/`} key={brand.slug} style={{ '--brand-accent': brand.accent } as CSSProperties}><span className="brand-icon"><img src={brand.icon} alt="" /></span><h3>{brand.title}</h3><p>{brand.descriptor}</p><span className="card-link">View brand</span></Link>)}</div></section>
    <section className="system-callout"><p className="eyebrow">The system underneath</p><h2>Strategy, standards, assets, and implementation.</h2><p>Our process makes brand decisions repeatable and the results immediately useful to designers, developers, and operators.</p><div className="actions"><Link className="button primary" href="/docs">Explore the process</Link><a className="button" href="https://github.com/ShruggieTech/shruggie-brand/releases/latest">Download the skill</a></div></section>
  </div>;
}
