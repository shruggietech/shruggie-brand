'use client';

import { useEffect, useMemo, useState } from 'react';
import type { AssetFamily, PortalResource } from '@/lib/guidelines';
import { ResourceList } from './resource-list';

type FilterKey = 'family' | 'platform' | 'appearance' | 'role' | 'format';
const emptyFilters: Record<FilterKey, string> = { family: '', platform: '', appearance: '', role: '', format: '' };

export function AssetLibraryClient({ families, resources }: { families: AssetFamily[]; resources: PortalResource[] }) {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState(emptyFilters);
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    setQuery(params.get('q') ?? '');
    setFilters({ family: params.get('family') ?? '', platform: params.get('platform') ?? '', appearance: params.get('appearance') ?? '', role: params.get('role') ?? '', format: params.get('format') ?? '' });
  }, []);
  useEffect(() => {
    const params = new URLSearchParams();
    if (query) params.set('q', query);
    for (const [key, value] of Object.entries(filters)) if (value) params.set(key, value);
    history.replaceState(null, '', `${location.pathname}${params.size ? `?${params}` : ''}${location.hash}`);
  }, [query, filters]);
  const options = useMemo(() => ({
    family: families.map((family) => family.key),
    platform: [...new Set(families.flatMap((family) => family.assets.map((asset) => asset.platform)))].sort(),
    appearance: [...new Set(families.flatMap((family) => family.assets.map((asset) => asset.appearance)))].sort(),
    role: [...new Set(families.flatMap((family) => family.assets.map((asset) => asset.role)))].sort(),
    format: [...new Set(families.flatMap((family) => family.assets.flatMap((asset) => asset.formats)))].sort(),
  }), [families]);
  const visible = useMemo(() => families.map((family) => ({
    ...family,
    assets: family.assets.filter((asset) => {
      const haystack = `${family.title} ${asset.title} ${asset.summary} ${asset.role} ${asset.platform} ${asset.appearance} ${asset.formats.join(' ')} ${asset.deliveries.map((item) => item.path).join(' ')}`.toLowerCase();
      return (!query || haystack.includes(query.toLowerCase())) && (!filters.family || family.key === filters.family) && (!filters.platform || asset.platform === filters.platform) && (!filters.appearance || asset.appearance === filters.appearance) && (!filters.role || asset.role === filters.role) && (!filters.format || asset.formats.includes(filters.format));
    }),
  })).filter((family) => family.assets.length), [families, filters, query]);
  const count = visible.reduce((total, family) => total + family.assets.length, 0);
  const reset = () => { setQuery(''); setFilters(emptyFilters); };
  return <>
    <div className="asset-tools" role="search" aria-label="Filter brand assets">
      <label className="asset-search">Search assets<input type="search" value={query} onChange={(event) => setQuery(event.target.value)} /></label>
      {(Object.keys(filters) as FilterKey[]).map((key) => <label key={key}>{key[0].toUpperCase() + key.slice(1)}<select value={filters[key]} onChange={(event) => setFilters((current) => ({ ...current, [key]: event.target.value }))}><option value="">All</option>{options[key].map((value) => <option value={value} key={value}>{value.replaceAll('-', ' ')}</option>)}</select></label>)}
      <button type="button" onClick={reset}>Reset</button>
      <p className="asset-count" aria-live="polite">{count} representative {count === 1 ? 'asset' : 'assets'}</p>
    </div>
    {count === 0 && <div className="asset-empty"><h2>No matching assets</h2><p>Clear the search or reset the filters to browse the complete library.</p><button type="button" onClick={reset}>Show all assets</button></div>}
    {visible.map((family) => <section className="asset-family guide-section" id={family.key} key={family.key}>
      <h2>{family.title}</h2><p className="guide-lead">{family.summary}</p>
      <div className="asset-grid">{family.assets.map((asset) => <article className="asset-tile" key={asset.id} data-family={family.key} data-platform={asset.platform} data-role={asset.role}>
        <div className={`asset-preview ${asset.surface}-well`}><div className="asset-preview-media"><img src={asset.preview.url} alt={`${asset.title} preview`} /></div></div>
        <div className="asset-summary"><h3>{asset.title}</h3><p>{asset.summary}</p><p className="asset-variants">{asset.formats.map((item) => item.toUpperCase()).join(', ')} · {asset.variants.join(', ')}</p>
          <details><summary>View {asset.deliveries.length} {asset.deliveries.length === 1 ? 'delivery' : 'deliveries'}</summary><ul className="delivery-list">{asset.deliveries.map((delivery) => <li key={delivery.path}><a data-kit-asset href={delivery.url}>{delivery.path.split('/').at(-1)}</a><span>{[delivery.format.toUpperCase(), delivery.width && delivery.height ? `${delivery.width} × ${delivery.height}` : delivery.embedded_sizes?.length ? `${delivery.embedded_sizes.join(', ')} px embedded` : null, delivery.destination].filter(Boolean).join(' · ')}</span><code>{delivery.path}</code></li>)}</ul></details>
        </div>
      </article>)}</div>
    </section>)}
    <ResourceList resources={resources} />
  </>;
}
