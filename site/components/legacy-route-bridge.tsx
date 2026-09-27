'use client';

import { useEffect } from 'react';

export function LegacyRouteBridge({ destination, label }: { destination: string; label: string }) {
  useEffect(() => {
    const suffix = window.location.search + window.location.hash;
    window.location.replace(destination + suffix);
  }, [destination]);
  return <main id="content" className="legacy-route-bridge"><meta httpEquiv="refresh" content={`1;url=${destination}`} /><h1>This page has moved</h1><p>Continue to the {label} page.</p><a href={destination}>Open {label}</a></main>;
}
