'use client';

import { usePathname } from 'next/navigation';
import { useEffect } from 'react';

let pendingPaginationPath: string | null = null;

function normalizedPath(path: string): string {
  return path.endsWith('/') ? path : `${path}/`;
}

export function DocumentationPaginationFocus() {
  const pathname = usePathname();

  useEffect(() => {
    function rememberPaginationClick(event: MouseEvent) {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const target = event.target;
      if (!(target instanceof Element)) return;
      const link = target.closest<HTMLAnchorElement>('.docs-pagination > a[href]');
      if (!link || link.target && link.target !== '_self') return;
      const destination = new URL(link.href, window.location.href);
      if (destination.origin !== window.location.origin || destination.hash) return;
      if (normalizedPath(destination.pathname) === normalizedPath(window.location.pathname)) return;
      pendingPaginationPath = normalizedPath(destination.pathname);
    }

    document.addEventListener('click', rememberPaginationClick, true);
    return () => document.removeEventListener('click', rememberPaginationClick, true);
  }, []);

  useEffect(() => {
    if (!pendingPaginationPath || pendingPaginationPath !== normalizedPath(pathname)) return;
    pendingPaginationPath = null;
    const frame = requestAnimationFrame(() => {
      const heading = document.querySelector<HTMLElement>('.docs-page h1');
      if (!heading) return;
      heading.tabIndex = -1;
      heading.focus({ preventScroll: true });
      window.scrollTo({ top: 0, behavior: 'instant' });
    });
    return () => cancelAnimationFrame(frame);
  }, [pathname]);

  return null;
}
