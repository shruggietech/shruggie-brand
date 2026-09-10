import brands from '../generated/brands.json' with { type: 'json' };
import guidelinePortals from '../generated/guidelines.json' with { type: 'json' };
import documentation from '../generated/documentation.json' with { type: 'json' };
import routeContract from '../generated/routes.json' with { type: 'json' };
import { existsSync, readFileSync } from 'node:fs';

const assetLibrarySource = readFileSync(new URL('../components/guidelines/asset-library-client.tsx', import.meta.url), 'utf8');
const topicContentSource = readFileSync(new URL('../components/guidelines/topic-content.tsx', import.meta.url), 'utf8');
const footerSource = readFileSync(new URL('../components/footer.tsx', import.meta.url), 'utf8');
const brandPortfolioSource = readFileSync(new URL('../components/brand-portfolio.tsx', import.meta.url), 'utf8');
const homepageSource = readFileSync(new URL('../app/(site)/page.tsx', import.meta.url), 'utf8');
const marketingLayoutSource = readFileSync(new URL('../app/(site)/layout.tsx', import.meta.url), 'utf8');
const layoutSource = readFileSync(new URL('../lib/layout.shared.tsx', import.meta.url), 'utf8');
const globalStyles = readFileSync(new URL('../app/globals.css', import.meta.url), 'utf8');
const guidelineLayoutSource = readFileSync(new URL('../app/(guidelines)/[slug]/layout.tsx', import.meta.url), 'utf8');
const guidelinePageSource = readFileSync(new URL('../app/(guidelines)/[slug]/guidelines/[[...topic]]/page.tsx', import.meta.url), 'utf8');
const downloadsSource = readFileSync(new URL('../components/guidelines/downloads-content.tsx', import.meta.url), 'utf8');
const documentationLayoutSource = readFileSync(new URL('../app/docs/layout.tsx', import.meta.url), 'utf8');
const documentationPageSource = readFileSync(new URL('../app/docs/[[...slug]]/page.tsx', import.meta.url), 'utf8');
const documentationTreeSource = readFileSync(new URL('../lib/documentation.ts', import.meta.url), 'utf8');
const noScriptHierarchySource = readFileSync(new URL('../components/hierarchy-no-script.tsx', import.meta.url), 'utf8');
if (!assetLibrarySource.includes('className="asset-preview-media"') || !topicContentSource.includes('className="asset-preview-media"')) throw new Error('both guideline preview surfaces must use the shared media wrapper');
if (!/\.asset-preview-media img \{[^}]*width: 100%;[^}]*height: 100%;[^}]*object-fit: contain;[^}]*\}/s.test(globalStyles)) throw new Error('shared preview containment styles must bind full media sizing to contain fitting');

const footerRecords = [...footerSource.matchAll(/\{ label: '([^']+)', href: '([^']+)', kind: '([^']+)' \}/g)].map((match) => ({ label: match[1], href: match[2], kind: match[3] }));
const expectedFooterRecords = [
  { label: 'Documentation', href: '/docs', kind: 'internal' },
  { label: 'Download Skill', href: 'https://github.com/ShruggieTech/shruggie-brand/releases/latest', kind: 'new-tab' },
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
if (!marketingLayoutSource.includes('<Footer />')) throw new Error('marketing layout no longer renders the shared footer');
if (documentationPageSource.includes("@/components/footer") || documentationPageSource.includes('<Footer')) throw new Error('documentation page composes the shared marketing footer');
if (!documentationPageSource.includes("footer={{ className: 'docs-pagination'")) throw new Error('documentation page no longer provides contextual pagination');
if (/\.docs-page \.site-footer\b/.test(globalStyles)) throw new Error('documentation styles retain obsolete shared-footer coupling');

const navigationRecords = [...layoutSource.matchAll(/\{ text: '([^']+)', url: '([^']+)'(?:, external: (true))?(?:, on: 'menu')? \}/g)].map((match) => ({ label: match[1], href: match[2], external: match[3] === 'true' }));
const expectedNavigationRecords = [
  { label: 'Documentation', href: '/docs', external: false },
  { label: 'Company', href: 'https://shruggie.tech/', external: true },
  { label: 'Download Skill', href: 'https://github.com/ShruggieTech/shruggie-brand/releases/latest', external: true },
  { label: 'View on GitHub', href: 'https://github.com/ShruggieTech/shruggie-brand', external: true },
];
if (JSON.stringify(navigationRecords) !== JSON.stringify(expectedNavigationRecords)) throw new Error(`shared navigation records differ from the approved ordered policy: ${JSON.stringify(navigationRecords)}`);
if (!homepageSource.includes('<Link className="button primary" href="/docs">Documentation</Link>')) throw new Error('homepage lacks the approved Documentation primary action');
if (!homepageSource.includes('className="button" href="https://github.com/ShruggieTech/shruggie-brand/releases/latest" target="_blank" rel="noopener noreferrer">Download Skill</a>')) throw new Error('homepage lacks the safely isolated Download Skill secondary action');
if (!homepageSource.includes('<a className="text-action hero-portfolio-link" href="#portfolio">Explore Our Portfolio<span aria-hidden="true">↓</span></a>')) throw new Error('homepage lacks the approved portfolio supporting action and decorative cue');
if (!homepageSource.includes('<h2 id="portfolio-heading">Our Portfolio</h2>') || !homepageSource.includes('Explore our identity spectrum: a portfolio of distinct brands, each built with its own system, voice, and purpose.')) throw new Error('homepage portfolio wording differs from the approved contract');
for (const retired of ['The system underneath', 'Strategy, standards, assets, and implementation.', 'system-callout']) if (homepageSource.includes(retired)) throw new Error(`homepage retains removed callout source: ${retired}`);
if (/\.system-callout\b/.test(globalStyles)) throw new Error('global styles retain obsolete system callout selectors');
if (!/html \{[^}]*scrollbar-gutter: stable;/s.test(globalStyles)) throw new Error('shared document root does not reserve a stable scrollbar gutter');
if (!/\.hero-portfolio-link \{[^}]*margin-top:/s.test(globalStyles)) throw new Error('portfolio supporting action lacks deliberate shared hero spacing');

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
const expectedBrandSlugs = ['covarity', 'cueson', 'eso-weave', 'fragcap', 'glitchpad', 'go-schedule', 'shruggietech'];
if (JSON.stringify(brands.map((brand) => brand.slug).sort()) !== JSON.stringify(expectedBrandSlugs)) throw new Error('generated brand inventory does not contain the seven production brands');
const esoWeave = brands.find((brand) => brand.slug === 'eso-weave');
if (esoWeave?.idea !== 'Unofficial automation for ESO' || esoWeave?.descriptor !== 'Cross-platform desktop companion for The Elder Scrolls Online') throw new Error('ESO Weave public wording differs from the Gate 2 approval');
if (!esoWeave?.vendorBoundary?.includes('not affiliated with')) throw new Error('ESO Weave public record omits the required vendor boundary');
const cueson = brands.find((brand) => brand.slug === 'cueson');
if (cueson?.idea !== 'Universal captions and subtitles' || cueson?.descriptor !== 'A lossless, structured interchange layer for subtitle and caption content.') throw new Error('Cueson public wording differs from the Gate 2 approval');
if (cueson?.parent !== 'ShruggieTech' || cueson?.endorsement !== 'shruggietech-project' || cueson?.ownership !== 'shruggietech-owned') throw new Error('Cueson public affiliation differs from the approved owned-project contract');
for (const brand of brands) {
  const expectedArchive = `/${brand.slug}/downloads/${brand.slug}-brand-${brand.version}.zip`;
  if (brand.guidelinesPath !== `/${brand.slug}/guidelines/` || brand.kitArchive !== expectedArchive || brand.kitArchiveFilename !== expectedArchive.split('/').at(-1)) throw new Error(`${brand.slug} generated action destinations are incomplete or inconsistent`);
  if ('vendorBoundarySummary' in brand) throw new Error(`${brand.slug} retains obsolete card-level vendor summary copy`);
}
const expectedBrandNavigation = [
  ['overview', 'Overview', 'Overview', 0], ['voice', 'Voice', 'Voice', 0], ['logos', 'Logo', 'Identity', 0], ['color', 'Color', 'Identity', 1],
  ['typography', 'Typography', 'Identity', 2], ['components', 'Components', 'Components', 0], ['assets', 'Assets', 'Assets', 0], ['integration', 'Integration', 'Integration', 0],
];
for (const portal of guidelinePortals) {
  const actual = portal.topics.map(({ key, label, section, order }) => [key, label, section, order]);
  if (JSON.stringify(actual) !== JSON.stringify(expectedBrandNavigation)) throw new Error(`${portal.brand.slug} guideline hierarchy differs from the approved contract`);
  if (portal.brand.version !== brands.find((brand) => brand.slug === portal.brand.slug)?.version) throw new Error(`${portal.brand.slug} portal omits the brand version needed by the consolidated Overview`);
  const assets = portal.topics.find((topic) => topic.key === 'assets');
  if (assets?.path !== `/${portal.brand.slug}/downloads/`) throw new Error(`${portal.brand.slug} Assets does not use the stable downloads route`);
}
const expectedDocumentationNavigation = [
  ['Overview', 'Overview', '/docs/'], ['Foundation', 'Contract', '/docs/00-variance-contract/'], ['Foundation', 'Kit', '/docs/02-kit-anatomy/'],
  ['Discovery', 'Interview', '/docs/03-interview/'], ['Identity', 'Logo', '/docs/06-logo-protocol/'], ['Identity', 'Glyphs', '/docs/08-glyph-construction/'],
  ['Identity', 'Continuity', '/docs/identity-continuity/'], ['Identity', 'Voice', '/docs/07-voice/'], ['Implementation', 'Toolchain', '/docs/04-toolchain/'], ['Implementation', 'shadcn', '/docs/05-shadcn-binding/'],
  ['Implementation', 'Portability', '/docs/09-portability/'],
];
if (JSON.stringify(documentation.map((record) => [record.navigation.section, record.navigation.label, record.navigation.path])) !== JSON.stringify(expectedDocumentationNavigation)) throw new Error('documentation hierarchy differs from the approved contract');
if (JSON.stringify([...documentation].sort((left, right) => left.navigation.paginationOrder - right.navigation.paginationOrder).map((record) => record.slug)) !== JSON.stringify(['index', '00-variance-contract', '02-kit-anatomy', '03-interview', '04-toolchain', '05-shadcn-binding', '06-logo-protocol', '07-voice', '08-glyph-construction', '09-portability', 'identity-continuity'])) throw new Error('documentation pagination no longer preserves the established sequence');
if (!guidelineLayoutSource.includes('tree={guidelineTree(portal)}') || !guidelinePageSource.includes('<GuidelineNoScriptNav')) throw new Error('brand routes do not share the generated hierarchy and no-script fallback');
if (!documentationLayoutSource.includes('tree={documentationTree()}') || !noScriptHierarchySource.includes('DocumentationNoScriptNav')) throw new Error('documentation routes do not share the generated hierarchy and no-script fallback');
if (!documentationTreeSource.includes("type: 'folder' as const") || !documentationTreeSource.includes('paginationOrder') || !noScriptHierarchySource.includes('<ul>') || !noScriptHierarchySource.includes('aria-current=') || !globalStyles.includes(".hierarchy-noscript-nav a[aria-current='page']")) throw new Error('grouped navigation lacks semantic nested structure, stable pagination, or a visibly styled no-script current state');
if (!guidelinePageSource.includes("topic.key !== 'assets'") || !guidelinePageSource.includes('dynamicParams = false')) throw new Error('obsolete guidelines Assets route is still statically generated');
if (!downloadsSource.includes('<AssetLibrary portal={portal} />') || !downloadsSource.includes('Direct downloads')) throw new Error('Assets does not combine direct downloads and the generated asset library');
if (!topicContentSource.includes('id="brand-overview"') || !topicContentSource.includes('portal.brand.idea') || !topicContentSource.includes('id="built-to-ship"') || !topicContentSource.includes('/brand/r/registry.json')) throw new Error('consolidated Overview does not preserve the retired brand-page content and registry entry point');
if (existsSync(new URL('../app/(site)/[slug]/page.tsx', import.meta.url))) throw new Error('retired brand-root page source still exists');
if (!brandPortfolioSource.includes('className="brand-card"') || !brandPortfolioSource.includes('className="brand-accordion"') || !brandPortfolioSource.includes('<summary>')) throw new Error('portfolio component lacks the required desktop article and native mobile disclosure structures');
if (!brandPortfolioSource.includes("event.key === 'Escape'") || !brandPortfolioSource.includes("data-actions-dismissed={dismissed ? 'true' : undefined}") || !brandPortfolioSource.includes('<noscript><style>')) throw new Error('desktop action reveal lacks Escape dismissal or its no-script visible-action fallback');
if (!/@media \(hover: none\), \(pointer: coarse\) \{[^}]*\.brand-grid-desktop \{ display: none; \}[^}]*\.brand-accordion-list \{ display: block; \}/s.test(globalStyles)) throw new Error('wide touch-only devices do not receive the native disclosure presentation');
if (!brandPortfolioSource.includes('<a href={brand.guidelinesPath}>Guidelines</a>') || !brandPortfolioSource.includes('<a href={brand.kitArchive} download={brand.kitArchiveFilename}>Download Kit</a>')) throw new Error('portfolio component lacks exact generated Guidelines and Download Kit actions');
if (!brandPortfolioSource.includes("const noticeId = 'portfolio-third-party-notice'") || !brandPortfolioSource.includes('id={noticeId}') || !brandPortfolioSource.includes('aria-describedby={noticeId}')) throw new Error('portfolio component lacks one accessible shared vendor-notice association');
if (brandPortfolioSource.includes('vendorBoundarySummary') || homepageSource.includes('vendorBoundarySummary') || homepageSource.includes('href={`/${brand.slug}/`}')) throw new Error('portfolio retains retired repeated disclaimer or implicit full-card navigation');
for (const route of routeRecords.filter((route) => route.brandSlug === 'eso-weave')) if (route.vendorBoundary !== esoWeave.vendorBoundary || route.vendorBoundaryUrl !== 'https://brand.shruggie.tech/eso-weave/guidelines/') throw new Error(`${route.pathname} omits the ESO Weave vendor-boundary metadata`);
if (routeRecords.some((route) => route.kind === 'brand' || brands.some((brand) => route.pathname === `/${brand.slug}/`) || route.pathname.endsWith('/guidelines/assets/'))) throw new Error('route contract retains a removed brand root or duplicate Assets route');
export const brandRoutes = routeRecords.filter((route) => ['downloads', 'guidelines', 'guidelines-topic'].includes(route.kind)).map((route) => route.pathname);
export const docRoutes = routeRecords.filter((route) => ['docs-index', 'docs-page'].includes(route.kind)).map((route) => route.pathname);
export const tableRoutes = ['00-variance-contract', '02-kit-anatomy', '04-toolchain', '05-shadcn-binding', '06-logo-protocol', '07-voice', '08-glyph-construction', '09-portability'].map((slug) => `/docs/${slug}/`);
export const htmlRoutes = routeRecords.map((route) => route.pathname);
export const guidelineRoutes = routeRecords.filter((route) => ['guidelines', 'guidelines-topic'].includes(route.kind)).map((route) => route.pathname);
export const visualRoutes = ['/', ...brands.flatMap((brand) => [`/${brand.slug}/guidelines/`, `/${brand.slug}/downloads/`]), '/glitchpad/guidelines/color/', '/docs/', '/docs/00-variance-contract/'];
export const visualThemes = ['light', 'dark'];
export const visualWidths = [360, 1280];
export const requiredFiles = ['/favicon.svg', '/favicon.ico', '/favicon-16x16.png', '/favicon-32x32.png', '/apple-touch-icon.png', '/android-chrome-192x192.png', '/android-chrome-512x512.png', '/shruggietech-logo-dark.svg', '/shruggietech-logo-light.svg', '/site.webmanifest', '/robots.txt', '/sitemap.xml', '/static.json', ...routeRecords.map((route) => route.social.path)];
export const iconFiles = ['/favicon.svg', '/favicon.ico', '/favicon-16x16.png', '/favicon-32x32.png', '/apple-touch-icon.png', '/android-chrome-192x192.png', '/android-chrome-512x512.png'];
export const iconRoutes = ['/', '/docs/', '/docs/04-toolchain/'];
export const downloadFiles = brands.flatMap((brand) => { const root = `/${brand.slug}/downloads/files`; return [brand.kitArchive, `${root}/${brand.slug}-brand-guide.pdf`, `${root}/logos/svg/${brand.slug}-mark-color.svg`, `${root}/logos/svg/${brand.slug}-horizontal-color.svg`, `${root}/icons/manifest.json`, `${root}/icons/web/favicon.ico`, `${root}/icons/android/manifest.json`, `${root}/icons/apple/ios/manifest.json`, `${root}/icons/apple/macos/manifest.json`, `${root}/icons/windows/manifest.json`, `${root}/icons/windows/classic/app.ico`, ...(brand.slug === 'cueson' ? [`${root}/consumer-handoff.json`] : []), brand.specimen, `/${brand.slug}/brand/r/theme.json`]; });
