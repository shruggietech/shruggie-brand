'use client';

import type { CSSProperties } from 'react';
import { useRef, useState } from 'react';
import type { Brand } from '@/lib/brands';

const noticeId = 'portfolio-third-party-notice';

function brandStyle(brand: Brand) {
  return {
    '--brand-accent': brand.accent,
    '--brand-portfolio-surface': brand.portfolioSurface,
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
    aria-label={`${brand.title} portfolio card. Focus to reveal actions.`}
    data-actions-dismissed={dismissed ? 'true' : undefined}
    data-portfolio-surface="governed-dark"
    onBlurCapture={(event) => { if (!event.currentTarget.contains(event.relatedTarget)) setDismissed(false); }}
    onFocusCapture={(event) => { if (event.target !== event.currentTarget) setDismissed(false); }}
    onKeyDown={(event) => { if (event.key === 'Escape') { setDismissed(true); card.current?.focus(); } }}
    onPointerEnter={() => setDismissed(false)}
    onPointerLeave={() => { if (!card.current?.contains(document.activeElement)) setDismissed(false); }}
    ref={card}
    style={brandStyle(brand)}
    tabIndex={0}
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
  const hasThirdPartyProjects = brands.some((brand) => Boolean(brand.vendorBoundary));
  return <>
    <div className="brand-grid brand-grid-desktop">
      {brands.map((brand) => <DesktopBrandCard brand={brand} key={brand.slug} />)}
    </div>
    <div className="brand-accordion-list">
      {brands.map((brand) => <details className="brand-accordion" data-portfolio-surface="governed-dark" key={brand.slug} style={brandStyle(brand)}>
        <summary><span className="brand-icon"><img src={brand.icon} alt="" /></span><span className="mobile-brand-title"><BrandName brand={brand} /></span></summary>
        <div className="brand-accordion-panel"><p>{brand.descriptor}</p><BrandActions brand={brand} /></div>
      </details>)}
    </div>
    {hasThirdPartyProjects && <aside className="portfolio-vendor-notice" id={noticeId} aria-label="Third-party brand notice">
      <p>* Third-party projects are independently owned and operated.</p>
    </aside>}
    <noscript><style>{'.brand-card .brand-card-description{opacity:0}.brand-card .brand-actions{opacity:1;visibility:visible;pointer-events:auto;transform:none}'}</style></noscript>
  </>;
}
