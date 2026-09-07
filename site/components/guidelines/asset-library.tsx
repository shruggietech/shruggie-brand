import type { GuidelinePortal } from '@/lib/guidelines';
import { AssetLibraryClient } from './asset-library-client';

export function AssetLibrary({ portal }: { portal: GuidelinePortal }) {
  return <><p className="guide-lead">Browse by purpose. Each tile represents one design; open its details for every verified size, format, alias, and destination.</p><noscript><p className="guide-notice">Search and filters require JavaScript. The complete library remains available below.</p></noscript><AssetLibraryClient families={portal.asset_families} resources={portal.resources} /></>;
}
