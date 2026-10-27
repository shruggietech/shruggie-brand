'use client';

import type { CSSProperties } from 'react';
import { useEffect, useRef, useState } from 'react';
import type { Brand } from '@/lib/brands';

const noticeId = 'portfolio-third-party-notice';

function brandStyle(brand: Brand) {
  return {
    '--brand-accent': brand.accent,
    '--brand-portfolio-surface': brand.portfolioSurface,
  } as CSSProperties;
}

function BrandName({ brand }: { brand: Brand }) {
  if (!brand.vendorBoundary) return <>{brand.title}</>;
  return <>{brand.title.slice(0, -2)}<span className="vendor-title-end">{brand.title.slice(-2)}<sup className="vendor-marker" aria-describedby={noticeId}>*<span className="sr-only"> Independent third-party project</span></sup></span></>;
}

function BrandActions({ brand }: { brand: Brand }) {
  return <div className="brand-actions">
    <a href={brand.guidelinesPath}>Guidelines</a>
    <a href={brand.kitArchive} download={brand.kitArchiveFilename}>Download Kit</a>
  </div>;
}

function DesktopBrandCard({ brand }: { brand: Brand }) {
  const card = useRef<HTMLElement>(null);
  const title = useRef<HTMLHeadingElement>(null);
  const [dismissed, setDismissed] = useState(false);
  const description = brand.approvedMessaging.short_description;
  useEffect(() => {
    const cardElement = card.current;
    const titleElement = title.current;
    const contentElement = titleElement?.querySelector<HTMLElement>('.brand-title-text');
    if (!cardElement || !titleElement || !contentElement) return;
    let frame = 0;
    let disposed = false;
    const fitTitle = () => {
      titleElement.style.fontSize = '';
      titleElement.style.maxWidth = '';
      titleElement.style.whiteSpace = 'nowrap';
      titleElement.style.overflowWrap = 'normal';
      const available = Math.max(0, titleElement.clientWidth - 24);
      const naturalWidth = contentElement.getBoundingClientRect().width;
      if (naturalWidth <= available) return;
      // An enlarged browser default font must retain the rem-based title size.
      // Wrap it within the card instead of reducing it toward a fixed pixel size.
      if (parseFloat(getComputedStyle(document.documentElement).fontSize) > 16) {
        titleElement.style.maxWidth = 'calc(100% - 24px)';
        titleElement.style.whiteSpace = 'normal';
        titleElement.style.overflowWrap = 'anywhere';
        return;
      }
      const baseSize = parseFloat(getComputedStyle(titleElement).fontSize);
      const minimumSize = 18;
      let fittedSize = Math.max(minimumSize, Math.floor(baseSize * available / naturalWidth * 10) / 10);
      titleElement.style.fontSize = `${fittedSize}px`;
      while (contentElement.getBoundingClientRect().width > available && fittedSize > minimumSize) {
        fittedSize = Math.max(minimumSize, fittedSize - .5);
        titleElement.style.fontSize = `${fittedSize}px`;
      }
      if (contentElement.getBoundingClientRect().width > available) {
        titleElement.style.maxWidth = 'calc(100% - 24px)';
        titleElement.style.whiteSpace = 'normal';
        titleElement.style.overflowWrap = 'anywhere';
      }
    };
    const scheduleFit = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(fitTitle);
    };
    const observer = new ResizeObserver(scheduleFit);
    observer.observe(cardElement);
    void document.fonts.ready.then(() => { if (!disposed) scheduleFit(); });
    scheduleFit();
    return () => { disposed = true; observer.disconnect(); cancelAnimationFrame(frame); };
  }, [brand.title, brand.vendorBoundary]);
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
    <h3 ref={title}><span className="brand-title-text"><BrandName brand={brand} /></span></h3>
    <div className="brand-card-stage">
      {description && <p className="brand-card-description">{description}</p>}
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
        <div className="brand-accordion-panel">{brand.approvedMessaging.short_description && <p>{brand.approvedMessaging.short_description}</p>}<BrandActions brand={brand} /></div>
      </details>)}
    </div>
    {hasThirdPartyProjects && <aside className="portfolio-vendor-notice" id={noticeId} aria-label="Third-party brand notice">
      <p>* Third-party projects are independently owned and operated.</p>
    </aside>}
    <noscript><style>{'.brand-card .brand-card-description{opacity:0}.brand-card .brand-actions{opacity:1;visibility:visible;pointer-events:auto;transform:none}'}</style></noscript>
  </>;
}
