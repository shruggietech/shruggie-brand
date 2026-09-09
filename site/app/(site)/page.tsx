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
    <section className="hero"><p className="eyebrow">Brand building by ShruggieTech</p><h1>We build comprehensive brands</h1><p className="lede">We shape distinct identities with a repeatable process, then ship the standards, assets, and tools that keep them coherent.</p><div className="actions"><Link className="button primary" href="/docs">Documentation</Link><a className="button" href="https://github.com/ShruggieTech/shruggie-brand/releases/latest" target="_blank" rel="noopener noreferrer">Download Skill</a></div><a className="text-action hero-portfolio-link" href="#portfolio">Explore Our Portfolio<span aria-hidden="true">↓</span></a></section>
    <section className="section" id="portfolio" aria-labelledby="portfolio-heading"><div className="section-heading"><div><p className="eyebrow">Selected work</p><h2 id="portfolio-heading">Our Portfolio</h2></div><p>Explore our identity spectrum: a portfolio of distinct brands, each built with its own system, voice, and purpose.</p></div><div className="brand-grid">{brands.map((brand) => <Link className="brand-card" data-showcase-surface={brand.showcaseSurface ? 'governed' : undefined} href={`/${brand.slug}/`} key={brand.slug} style={{ '--brand-accent': brand.accent, ...(brand.showcaseSurface ? { '--brand-showcase-surface': brand.showcaseSurface, '--brand-showcase-foreground': brand.showcaseForeground } : {}) } as CSSProperties}><span className="brand-icon"><img src={brand.icon} alt="" /></span><h3>{brand.title}</h3><p>{brand.descriptor}</p>{brand.vendorBoundarySummary && <small className="vendor-boundary">{brand.vendorBoundarySummary}</small>}<span className="card-link">View brand</span></Link>)}</div></section>
  </div>;
}
