/** @param {{ status: string, version: string, releaseUrl: string }} publication */
export function releaseBadge(publication) {
  if (publication.status !== 'release') return null;
  return { label: `BrandBuilder ${publication.version}`, href: publication.releaseUrl };
}
