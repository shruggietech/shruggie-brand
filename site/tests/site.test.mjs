import brands from '../generated/brands.json' with { type: 'json' };
import routeContract from '../generated/routes.json' with { type: 'json' };
import { readFileSync } from 'node:fs';

const assetLibrarySource = readFileSync(new URL('../components/guidelines/asset-library-client.tsx', import.meta.url), 'utf8');
const topicContentSource = readFileSync(new URL('../components/guidelines/topic-content.tsx', import.meta.url), 'utf8');
const globalStyles = readFileSync(new URL('../app/globals.css', import.meta.url), 'utf8');
if (!assetLibrarySource.includes('className="asset-preview-media"') || !topicContentSource.includes('className="asset-preview-media"')) throw new Error('both guideline preview surfaces must use the shared media wrapper');
if (!globalStyles.includes('.asset-preview-media') || !globalStyles.includes('object-fit: contain')) throw new Error('shared preview containment styles are missing');

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
