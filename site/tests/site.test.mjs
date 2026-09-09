import brands from '../generated/brands.json' with { type: 'json' };
import routeContract from '../generated/routes.json' with { type: 'json' };
import { readFileSync } from 'node:fs';

const assetLibrarySource = readFileSync(new URL('../components/guidelines/asset-library-client.tsx', import.meta.url), 'utf8');
const topicContentSource = readFileSync(new URL('../components/guidelines/topic-content.tsx', import.meta.url), 'utf8');
const footerSource = readFileSync(new URL('../components/footer.tsx', import.meta.url), 'utf8');
const globalStyles = readFileSync(new URL('../app/globals.css', import.meta.url), 'utf8');
if (!assetLibrarySource.includes('className="asset-preview-media"') || !topicContentSource.includes('className="asset-preview-media"')) throw new Error('both guideline preview surfaces must use the shared media wrapper');
if (!/\.asset-preview-media img \{[^}]*width: 100%;[^}]*height: 100%;[^}]*object-fit: contain;[^}]*\}/s.test(globalStyles)) throw new Error('shared preview containment styles must bind full media sizing to contain fitting');

const footerRecords = [...footerSource.matchAll(/\{ label: '([^']+)', href: '([^']+)', kind: '([^']+)' \}/g)].map((match) => ({ label: match[1], href: match[2], kind: match[3] }));
const expectedFooterRecords = [
  { label: 'Brands', href: '/', kind: 'internal' },
  { label: 'Documentation', href: '/docs', kind: 'internal' },
  { label: 'Download the skill', href: 'https://github.com/ShruggieTech/shruggie-brand/releases/latest', kind: 'new-tab' },
  { label: 'Company', href: 'https://shruggie.tech/', kind: 'same-tab' },
  { label: 'Source', href: 'https://github.com/ShruggieTech/shruggie-brand', kind: 'new-tab' },
  { label: 'License', href: 'https://github.com/ShruggieTech/shruggie-brand/blob/main/LICENSE', kind: 'new-tab' },
];
export function footerPolicyProblems(records) {
  const problems = [];
  if (JSON.stringify(records) !== JSON.stringify(expectedFooterRecords)) problems.push('footer records differ from the approved ordered policy');
  if (records.filter((record) => record.kind === 'new-tab').length !== 3) problems.push('footer must declare exactly three separate-context destinations');
  if (records.find((record) => record.label === 'Company')?.kind !== 'same-tab') problems.push('Company must remain a same-tab destination');
  return problems;
}
if (footerPolicyProblems(footerRecords).length > 0) throw new Error(`footer destination policy failed: ${footerPolicyProblems(footerRecords).join(', ')}`);
if (!footerSource.includes("target={link.kind === 'new-tab' ? '_blank' : undefined}") || !footerSource.includes("rel={link.kind === 'new-tab' ? 'noopener noreferrer' : undefined}")) throw new Error('footer separate-context records lack conditional target and relationship attributes');
if (footerPolicyProblems(expectedFooterRecords.map((record) => record.label === 'Source' ? { ...record, kind: 'same-tab' } : record)).length === 0) throw new Error('footer policy helper accepts missing separate-context safety metadata');
if (footerPolicyProblems(expectedFooterRecords.map((record) => record.label === 'Company' ? { ...record, kind: 'new-tab' } : record)).length === 0) throw new Error('footer policy helper accepts accidental new-tab behavior on Company');

export function interactionStyleProblems(styles) {
  const problems = [];
  if (!/\.docs-pagination > a > div \{[^}]*align-items: center;[^}]*\}/s.test(styles)) problems.push('pagination cue row lacks explicit center alignment');
  if (!/\.docs-pagination > a > div > svg \{[^}]*width: 1rem;[^}]*height: 1rem;[^}]*flex: 0 0 1rem;[^}]*translate: 0 -\.0625rem;[^}]*\}/s.test(styles)) problems.push('pagination chevron lacks stable dimensions and optical centering');
  if (!/:where\(button\[data-theme-toggle\], \[data-theme-toggle\] button\):not\(:disabled\) \{[^}]*cursor: pointer;[^}]*\}/s.test(styles)) problems.push('enabled theme buttons lack a pointer cursor');
  if (!/:where\(button\[data-theme-toggle\], \[data-theme-toggle\] button\):disabled \{[^}]*cursor: not-allowed;[^}]*\}/s.test(styles)) problems.push('disabled theme buttons lack disabled cursor treatment');
  return problems;
}
if (interactionStyleProblems(globalStyles).length > 0) throw new Error(`interaction style contract failed: ${interactionStyleProblems(globalStyles).join(', ')}`);

export const routeRecords = routeContract.routes;
const expectedBrandSlugs = ['covarity', 'eso-weave', 'fragcap', 'glitchpad', 'go-schedule', 'shruggietech'];
if (JSON.stringify(brands.map((brand) => brand.slug).sort()) !== JSON.stringify(expectedBrandSlugs)) throw new Error('generated brand inventory does not contain the six production brands');
const esoWeave = brands.find((brand) => brand.slug === 'eso-weave');
if (esoWeave?.idea !== 'Unofficial automation for ESO' || esoWeave?.descriptor !== 'Cross-platform desktop companion for The Elder Scrolls Online') throw new Error('ESO Weave public wording differs from the Gate 2 approval');
if (!esoWeave?.vendorBoundary?.includes('not affiliated with')) throw new Error('ESO Weave public record omits the required vendor boundary');
for (const route of routeRecords.filter((route) => route.brandSlug === 'eso-weave')) if (route.vendorBoundary !== esoWeave.vendorBoundary || route.vendorBoundaryUrl !== 'https://brand.shruggie.tech/eso-weave/guidelines/') throw new Error(`${route.pathname} omits the ESO Weave vendor-boundary metadata`);
export const brandRoutes = routeRecords.filter((route) => ['brand', 'downloads', 'guidelines', 'guidelines-topic'].includes(route.kind)).map((route) => route.pathname);
export const docRoutes = routeRecords.filter((route) => ['docs-index', 'docs-page'].includes(route.kind)).map((route) => route.pathname);
export const tableRoutes = ['00-variance-contract', '02-kit-anatomy', '04-toolchain', '05-shadcn-binding', '06-logo-protocol', '07-voice', '08-glyph-construction', '09-portability'].map((slug) => `/docs/${slug}/`);
export const htmlRoutes = routeRecords.map((route) => route.pathname);
export const guidelineRoutes = routeRecords.filter((route) => ['guidelines', 'guidelines-topic'].includes(route.kind)).map((route) => route.pathname);
export const visualRoutes = ['/', ...brands.flatMap((brand) => [`/${brand.slug}/`, `/${brand.slug}/guidelines/`]), '/glitchpad/guidelines/color/', '/glitchpad/guidelines/assets/', '/docs/', '/docs/00-variance-contract/'];
export const visualThemes = ['light', 'dark'];
export const visualWidths = [360, 1280];
export const requiredFiles = ['/favicon.svg', '/favicon.ico', '/favicon-16x16.png', '/favicon-32x32.png', '/apple-touch-icon.png', '/android-chrome-192x192.png', '/android-chrome-512x512.png', '/shruggietech-logo-dark.svg', '/shruggietech-logo-light.svg', '/site.webmanifest', '/robots.txt', '/sitemap.xml', '/static.json', ...routeRecords.map((route) => route.social.path)];
export const iconFiles = ['/favicon.svg', '/favicon.ico', '/favicon-16x16.png', '/favicon-32x32.png', '/apple-touch-icon.png', '/android-chrome-192x192.png', '/android-chrome-512x512.png'];
export const iconRoutes = ['/', '/docs/', '/docs/04-toolchain/'];
export const downloadFiles = brands.flatMap((brand) => { const root = `/${brand.slug}/downloads/files`; return [`${root}/${brand.slug}-brand-guide.pdf`, `${root}/logos/svg/${brand.slug}-mark-color.svg`, `${root}/logos/svg/${brand.slug}-horizontal-color.svg`, `${root}/icons/manifest.json`, `${root}/icons/web/favicon.ico`, `${root}/icons/android/manifest.json`, `${root}/icons/apple/ios/manifest.json`, `${root}/icons/apple/macos/manifest.json`, `${root}/icons/windows/manifest.json`, `${root}/icons/windows/classic/app.ico`, brand.specimen, `/${brand.slug}/brand/r/theme.json`]; });
