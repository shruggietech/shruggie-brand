import { notFound } from 'next/navigation';
import Link from 'next/link';
import { brands, brandBySlug } from '@/lib/brands';
import { pageMetadata } from '@/lib/metadata';
import { routeByPath } from '@/lib/routes';
import { StructuredData } from '@/components/structured-data';

export function generateStaticParams() { return brands.map(({ slug }) => ({ slug })); }
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) { const brand = brandBySlug((await params).slug); if (!brand) notFound(); return pageMetadata(routeByPath(`/${brand.slug}/`)); }
export default async function BrandPage({ params }: { params: Promise<{ slug: string }> }) { const brand = brandBySlug((await params).slug); if (!brand) notFound(); const route = routeByPath(`/${brand.slug}/`); return <div className="shell"><StructuredData route={route} /><section className="brand-hero" style={{ '--brand-accent': brand.accent } as React.CSSProperties}><div><p className="eyebrow">Brand portfolio</p><h1>{brand.title}</h1><p className="lede">{brand.descriptor}</p><p>{brand.idea}</p><div className="actions"><Link className="button primary" href={`/${brand.slug}/downloads/`}>Download assets</Link><a className="button" href={`/${brand.slug}/guidelines/`}>Open guidelines</a></div></div><img className="brand-logo" src={brand.logo} alt={`${brand.title} logo`} /></section><section className="section"><p className="eyebrow">Implementation</p><h2>Built to ship.</h2><p className="lede">Version {brand.version} includes production assets, standards, typography specimens, and an installable shadcn registry.</p><div className="actions"><a className="text-link" href={`/${brand.slug}/brand/r/registry.json`}>Open registry</a><Link className="text-link" href="/#portfolio">Back to portfolio</Link></div></section></div>; }
