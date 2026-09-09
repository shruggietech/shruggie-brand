'use client';

import type { CSSProperties } from 'react';
import { useRef, useState } from 'react';
import type { Brand } from '@/lib/brands';

const noticeId = 'portfolio-third-party-notice';

function brandStyle(brand: Brand) {
  return {
    '--brand-accent': brand.accent,
    ...(brand.showcaseSurface ? {
      '--brand-showcase-surface': brand.showcaseSurface,
      '--brand-showcase-foreground': brand.showcaseForeground,
    } : {}),
  } as CSSProperties;
}

function BrandName({ brand }: { brand: Brand }) {
  return <>{brand.title}{brand.vendorBoundary && <sup className="vendor-marker" aria-describedby={noticeId}>*<span className="sr-only"> Independent third-party project</span></sup>}</>;
}

function BrandActions({ brand }: { brand: Brand }) {
  return <div className="brand-actions">
    <a href={brand.guidelinesPath}>Guidelines</a>
    <a href={brand.kitArchive} download={brand.kitArchiveFilename}>Download Kit</a>
  </div>;
}

function DesktopBrandCard({ brand }: { brand: Brand }) {
  const card = useRef<HTMLElement>(null);
  const [dismissed, setDismissed] = useState(false);
  return <article
    className="brand-card"
    data-actions-dismissed={dismissed ? 'true' : undefined}
    data-showcase-surface={brand.showcaseSurface ? 'governed' : undefined}
    onBlurCapture={(event) => { if (!event.currentTarget.contains(event.relatedTarget)) setDismissed(false); }}
    onFocusCapture={(event) => { if (event.target !== event.currentTarget) setDismissed(false); }}
    onKeyDown={(event) => { if (event.key === 'Escape') { setDismissed(true); card.current?.focus(); } }}
    onPointerLeave={() => setDismissed(false)}
    ref={card}
    style={brandStyle(brand)}
    tabIndex={-1}
  >
    <span className="brand-icon"><img src={brand.icon} alt="" /></span>
    <h3><BrandName brand={brand} /></h3>
    <div className="brand-card-stage">
      <p className="brand-card-description">{brand.descriptor}</p>
      <BrandActions brand={brand} />
    </div>
  </article>;
}

export function BrandPortfolio({ brands }: { brands: Brand[] }) {
  const notices = [...new Set(brands.flatMap((brand) => brand.vendorBoundary ? [brand.vendorBoundary] : []))];
  return <>
    <div className="brand-grid brand-grid-desktop">
      {brands.map((brand) => <DesktopBrandCard brand={brand} key={brand.slug} />)}
    </div>
    <div className="brand-accordion-list">
      {brands.map((brand) => <details className="brand-accordion" data-showcase-surface={brand.showcaseSurface ? 'governed' : undefined} key={brand.slug} style={brandStyle(brand)}>
        <summary><span className="brand-icon"><img src={brand.icon} alt="" /></span><span className="mobile-brand-title"><BrandName brand={brand} /></span></summary>
        <div className="brand-accordion-panel"><p>{brand.descriptor}</p><BrandActions brand={brand} /></div>
      </details>)}
    </div>
    {notices.length > 0 && <aside className="portfolio-vendor-notice" id={noticeId} aria-label="Third-party brand notice">
      {notices.map((notice) => <p key={notice}>* {notice}</p>)}
    </aside>}
    <noscript><style>{'.brand-card .brand-card-description{opacity:0}.brand-card .brand-actions{opacity:1;pointer-events:auto;transform:none}'}</style></noscript>
  </>;
}
