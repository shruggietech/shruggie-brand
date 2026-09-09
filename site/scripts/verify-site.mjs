import { createReadStream, existsSync, mkdirSync, rmSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { extname, join, normalize, resolve } from 'node:path';
import { chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { inflateSync } from 'node:zlib';
import { downloadFiles, htmlRoutes, iconFiles, iconRoutes, requiredFiles, routeRecords, tableRoutes, visualRoutes, visualThemes, visualWidths } from '../tests/site.test.mjs';
import guidelinePortals from '../generated/guidelines.json' with { type: 'json' };
import brands from '../generated/brands.json' with { type: 'json' };
import documentationRecords from '../generated/documentation.json' with { type: 'json' };
import { payloadFailures } from './payload-contract.mjs';
import { isCanonicalRedirect, selectVerificationOrigin } from './verification-origin.mjs';

const root = resolve(import.meta.dirname, '..', 'out');
const visualRoot = resolve(import.meta.dirname, '..', 'test-results', 'visual');
rmSync(visualRoot, { recursive: true, force: true });
mkdirSync(visualRoot, { recursive: true });
const routeByPath = new Map(routeRecords.map((route) => [route.pathname, route]));
const portalBySlug = new Map(guidelinePortals.map((portal) => [portal.brand.slug, portal]));
const documentationByPath = new Map(documentationRecords.map((record) => [record.navigation.path, record]));
const types = { '.css': 'text/css', '.html': 'text/html', '.ico': 'image/x-icon', '.json': 'application/json', '.pdf': 'application/pdf', '.png': 'image/png', '.svg': 'image/svg+xml', '.txt': 'text/plain', '.webmanifest': 'application/manifest+json', '.xml': 'application/xml', '.woff2': 'font/woff2', '.zip': 'application/zip' };
function diskPath(url) {
  const pathname = decodeURIComponent(new URL(url, 'http://local').pathname);
  const safe = normalize(pathname).replace(/^([/\\])+/, '');
  let path = join(root, safe);
  if (pathname.endsWith('/')) path = join(path, 'index.html');
  else if (existsSync(path) && statSync(path).isDirectory()) path = join(path, 'index.html');
  else if (!extname(pathname) && existsSync(`${path}.html`)) path = `${path}.html`;
  if (!resolve(path).startsWith(root)) throw new Error('unsafe request path');
  return path;
}
const selectedOrigin = selectVerificationOrigin(process.env.SITE_VERIFY_BASE_URL);
let server;
let base = selectedOrigin.base;
if (selectedOrigin.kind === 'local') {
  server = createServer((request, response) => {
    try {
      const requestUrl = new URL(request.url ?? '/', 'http://local');
      if (requestUrl.pathname !== '/' && !requestUrl.pathname.endsWith('/') && !extname(requestUrl.pathname)) {
        const canonicalPath = diskPath(`${requestUrl.pathname}/`);
        if (existsSync(canonicalPath) && statSync(canonicalPath).isFile()) { response.writeHead(308, { location: `${requestUrl.pathname}/${requestUrl.search}` }).end(); return; }
      }
      const path = diskPath(request.url ?? '/');
      if (!existsSync(path) || !statSync(path).isFile()) { response.writeHead(404).end('not found'); return; }
      response.writeHead(200, { 'content-type': types[extname(path)] ?? 'application/octet-stream' });
      createReadStream(path).pipe(response);
    } catch { response.writeHead(400).end('bad request'); }
  });
  await new Promise((accept) => server.listen(0, '127.0.0.1', accept));
  const address = server.address();
  base = `http://127.0.0.1:${address.port}`;
}
const failures = [];
const check = (condition, message) => { if (!condition) failures.push(message); };
function previewLayoutProblems(sample) {
  const tolerance = 1;
  const problems = [];
  const contained = (inner, outer) => inner.left >= outer.left - tolerance && inner.top >= outer.top - tolerance && inner.right <= outer.right + tolerance && inner.bottom <= outer.bottom + tolerance;
  if (!contained(sample.media, sample.outer)) problems.push('media crosses preview boundary');
  if (!contained(sample.imageBox, sample.media) || !contained(sample.media, sample.imageBox)) problems.push('image box disagrees with media boundary');
  if (sample.objectFit !== 'contain') problems.push('image does not use computed contain fitting');
  if (sample.objectPosition !== '50% 50%') problems.push('image does not use computed centered positioning');
  if (sample.transform !== 'none') problems.push('image applies a presentation transform');
  if (!contained(sample.artwork, sample.media)) problems.push('artwork crosses media boundary');
  if (Math.abs((sample.artwork.left - sample.media.left) - (sample.media.right - sample.artwork.right)) > tolerance) problems.push('artwork is not horizontally centered');
  if (Math.abs((sample.artwork.top - sample.media.top) - (sample.media.bottom - sample.artwork.bottom)) > tolerance) problems.push('artwork is not vertically centered');
  if (sample.dividerTop < sample.outer.bottom - tolerance) problems.push('preview crosses metadata divider');
  return problems;
}
check(previewLayoutProblems({ outer: { left: 0, top: 0, right: 100, bottom: 100 }, media: { left: 10, top: 10, right: 90, bottom: 90 }, imageBox: { left: 10, top: 10, right: 90, bottom: 90 }, artwork: { left: 20, top: 30, right: 80, bottom: 70 }, objectFit: 'contain', objectPosition: '50% 50%', transform: 'none', dividerTop: 100 }).length === 0, 'preview geometry helper rejects a valid centered fixture');
check(previewLayoutProblems({ outer: { left: 0, top: 0, right: 100, bottom: 100 }, media: { left: 10, top: 10, right: 90, bottom: 90 }, imageBox: { left: 10, top: 10, right: 90, bottom: 90 }, artwork: { left: 8, top: 10, right: 70, bottom: 90 }, objectFit: 'cover', objectPosition: '0% 50%', transform: 'matrix(1, 0, 0, 1, 2, 0)', dividerTop: 95 }).length >= 6, 'preview geometry helper accepts overflow, off-center, transformed, cropped, or divider-crossing fixtures');
function paginationCueProblems(sample) {
  const problems = [];
  if (Math.abs(sample.iconCenter - sample.labelCenter) > 1.1) problems.push('chevron is not vertically centered with its complete label group');
  if (Math.abs(sample.iconWidth - 16) > 0.5 || Math.abs(sample.iconHeight - 16) > 0.5) problems.push('chevron dimensions are unstable');
  if (sample.flexShrink !== '0') problems.push('chevron can shrink');
  if (!sample.translate.includes('-1')) problems.push('chevron lacks the approved optical lift');
  return problems;
}
check(paginationCueProblems({ iconCenter: 49, labelCenter: 50, iconWidth: 16, iconHeight: 16, flexShrink: '0', translate: '0px -1px' }).length === 0, 'pagination helper rejects the approved centered cue fixture');
check(paginationCueProblems({ iconCenter: 44, labelCenter: 50, iconWidth: 12, iconHeight: 14, flexShrink: '1', translate: 'none' }).length === 4, 'pagination helper accepts center drift, size collapse, flex shrink, or missing optical correction');
function themeControlProblems(sample) {
  const problems = [];
  if (!sample.disabled && sample.cursor !== 'pointer') problems.push('enabled theme control lacks pointer cursor');
  if (sample.disabled && sample.cursor !== 'not-allowed') problems.push('disabled theme control lacks disabled cursor');
  if (sample.role !== 'button' || !sample.name) problems.push('theme control lacks button semantics or accessible name');
  if (sample.width < 44 || sample.height < 44) problems.push('theme control target is smaller than 44 by 44 CSS pixels');
  return problems;
}
check(themeControlProblems({ disabled: false, cursor: 'pointer', role: 'button', name: 'Toggle Theme', width: 62, height: 44 }).length === 0, 'theme helper rejects a valid enabled control');
check(themeControlProblems({ disabled: true, cursor: 'pointer', role: 'button', name: '', width: 30, height: 30 }).length === 3, 'theme helper accepts incorrect disabled cursor, missing semantics, or undersized target');
function geometryProblems(reference, sample, fields = ['left', 'right', 'width', 'center'], tolerance = 1) {
  return fields.filter((field) => Math.abs(reference[field] - sample[field]) > tolerance).map((field) => `${field} drifted by ${Math.abs(reference[field] - sample[field]).toFixed(2)} CSS pixels`);
}
check(geometryProblems({ left: 10, right: 110, width: 100, center: 60 }, { left: 10.5, right: 110.5, width: 100, center: 60.5 }).length === 0, 'geometry helper rejects raster-rounding tolerance');
check(geometryProblems({ left: 10, right: 110, width: 100, center: 60 }, { left: 13, right: 113, width: 100, center: 63 }).length === 3, 'geometry helper accepts visible horizontal drift');
function paeth(left, above, upperLeft) {
  const estimate = left + above - upperLeft;
  const dl = Math.abs(estimate - left); const da = Math.abs(estimate - above); const du = Math.abs(estimate - upperLeft);
  return dl <= da && dl <= du ? left : da <= du ? above : upperLeft;
}
function pngInfo(buffer) {
  if (!buffer.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]))) throw new Error('invalid PNG signature');
  let offset = 8; let width = 0; let height = 0; let depth = 0; let colorType = 0; let srgb = false; const compressed = [];
  while (offset + 12 <= buffer.length) {
    const length = buffer.readUInt32BE(offset); const kind = buffer.toString('ascii', offset + 4, offset + 8); const data = buffer.subarray(offset + 8, offset + 8 + length);
    if (kind === 'IHDR') { width = data.readUInt32BE(0); height = data.readUInt32BE(4); depth = data[8]; colorType = data[9]; }
    if (kind === 'sRGB') srgb = true;
    if (kind === 'IDAT') compressed.push(data);
    offset += 12 + length;
    if (kind === 'IEND') break;
  }
  if (!width || !height || depth !== 8 || colorType !== 6) throw new Error(`unsupported PNG ${width}x${height} depth ${depth} color ${colorType}`);
  const raw = inflateSync(Buffer.concat(compressed)); const stride = width * 4; let cursor = 0; let previous = Buffer.alloc(stride); let minAlpha = 255; let visible = 0; let artwork = 0; let chromatic = 0; const corners = [];
  for (let y = 0; y < height; y += 1) {
    const filter = raw[cursor]; const row = Buffer.from(raw.subarray(cursor + 1, cursor + 1 + stride)); cursor += stride + 1;
    for (let i = 0; i < stride; i += 1) {
      const left = i >= 4 ? row[i - 4] : 0; const above = previous[i]; const upperLeft = i >= 4 ? previous[i - 4] : 0;
      if (filter === 1) row[i] = (row[i] + left) & 255;
      else if (filter === 2) row[i] = (row[i] + above) & 255;
      else if (filter === 3) row[i] = (row[i] + Math.floor((left + above) / 2)) & 255;
      else if (filter === 4) row[i] = (row[i] + paeth(left, above, upperLeft)) & 255;
      else if (filter !== 0) throw new Error(`unsupported PNG filter ${filter}`);
    }
    for (let i = 3; i < stride; i += 4) { minAlpha = Math.min(minAlpha, row[i]); if (row[i] > 0) visible += 1; if (row[i] > 0 && (row[i - 3] !== 0 || row[i - 2] !== 0 || row[i - 1] !== 0)) artwork += 1; if (row[i] > 0 && (row[i - 3] !== row[i - 2] || row[i - 2] !== row[i - 1])) chromatic += 1; }
    if (y === 0 || y === height - 1) for (const x of [0, width - 1]) corners.push([...row.subarray(x * 4, x * 4 + 4)]);
    previous = row;
  }
  return { width, height, opaque: minAlpha === 255, srgb, visible, artwork, chromatic, corners };
}
function icoEntries(buffer) {
  if (buffer.length < 6 || !buffer.subarray(0, 4).equals(Buffer.from([0, 0, 1, 0]))) throw new Error('invalid ICO signature');
  const count = buffer.readUInt16LE(4); if (buffer.length < 6 + count * 16) throw new Error('truncated ICO directory'); const entries = [];
  for (let index = 0; index < count; index += 1) { const offset = 6 + index * 16; const width = buffer[offset] || 256; const height = buffer[offset + 1] || 256; const length = buffer.readUInt32LE(offset + 8); const start = buffer.readUInt32LE(offset + 12); if (width !== height || start + length > buffer.length) throw new Error(`invalid ICO entry ${index}`); entries.push({ size: width, payload: buffer.subarray(start, start + length) }); }
  return entries;
}
const hasCanonicalBlackCorners = (info) => info.corners.length === 4 && info.corners.every((pixel) => JSON.stringify(pixel) === JSON.stringify([0, 0, 0, 255]));
const hasVisibleArtwork = (info) => info.artwork >= Math.max(1, Math.ceil(info.width * info.height * 0.005));
const retiredPublicPhrases = ['how we build brands', 'how we build', 'the shruggietech variance contract', 'shruggietech variance contract', 'the variance contract'];
const browser = await chromium.launch({ headless: true });
try {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, permissions: ['clipboard-read', 'clipboard-write'] });
  const page = await context.newPage();
  const measurePreviewLayouts = async (route, selector, dividerSelector, label) => {
    const samples = await page.locator(selector).evaluateAll((elements, divider) => elements.map((outerElement) => {
      const mediaElement = outerElement.querySelector('.asset-preview-media');
      const imageElement = mediaElement?.querySelector('img');
      const dividerElement = outerElement.querySelector(divider) ?? outerElement.parentElement?.querySelector(divider);
      if (!mediaElement || !imageElement || !dividerElement || !imageElement.naturalWidth || !imageElement.naturalHeight) return null;
      const box = (element) => { const rect = element.getBoundingClientRect(); return { left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom, width: rect.width, height: rect.height }; };
      const media = box(mediaElement); const outer = outerElement.matches('.logo-example') ? media : box(outerElement);
      const imageBox = box(imageElement); const style = getComputedStyle(imageElement);
      const sourceRatio = imageElement.naturalWidth / imageElement.naturalHeight; const mediaRatio = media.width / media.height;
      const width = sourceRatio > mediaRatio ? media.width : media.height * sourceRatio;
      const height = sourceRatio > mediaRatio ? media.width / sourceRatio : media.height;
      const artwork = { left: media.left + (media.width - width) / 2, top: media.top + (media.height - height) / 2, right: media.left + (media.width + width) / 2, bottom: media.top + (media.height + height) / 2 };
      return { outer, media, imageBox, artwork, objectFit: style.objectFit, objectPosition: style.objectPosition, transform: style.transform, dividerTop: dividerElement.getBoundingClientRect().top, source: imageElement.getAttribute('src') };
    }), dividerSelector);
    check(samples.length > 0 && samples.every(Boolean), `${route} ${label} lacks measurable preview members`);
    for (const sample of samples.filter(Boolean)) for (const problem of previewLayoutProblems(sample)) failures.push(`${route} ${label} ${sample.source}: ${problem}`);
  };
  const verifyFooter = async (route, exerciseKeyboard = false) => {
    await page.goto(base + route);
    const links = await page.locator('.site-footer nav a').evaluateAll((elements) => elements.map((element) => ({ label: element.textContent?.trim(), href: element.getAttribute('href'), target: element.getAttribute('target'), rel: element.getAttribute('rel') })));
    const expected = [
      { label: 'Documentation', href: '/docs/', target: null, rel: null },
      { label: 'Download Skill', href: 'https://github.com/ShruggieTech/shruggie-brand/releases/latest', target: '_blank', rel: 'noopener noreferrer' },
      { label: 'Company', href: 'https://shruggie.tech/', target: null, rel: null },
      { label: 'Source', href: 'https://github.com/ShruggieTech/shruggie-brand', target: '_blank', rel: 'noopener noreferrer' },
      { label: 'License', href: 'https://github.com/ShruggieTech/shruggie-brand/blob/main/LICENSE', target: '_blank', rel: 'noopener noreferrer' },
    ];
    check(JSON.stringify(links) === JSON.stringify(expected), `${route} footer destination policy differs from the approved contract (${JSON.stringify(links)})`);
    for (const link of await page.locator('.site-footer nav a').all()) {
      const box = await link.boundingBox();
      check(Boolean(box && box.width >= 44 && box.height >= 44), `${route} footer link ${await link.textContent()} is smaller than 44 by 44 CSS pixels`);
    }
    const source = page.locator('.site-footer nav a', { hasText: /^Source$/ });
    await source.focus();
    const focus = await source.evaluate((element) => { const style = getComputedStyle(element); return { active: document.activeElement === element, outlineStyle: style.outlineStyle, outlineWidth: Number.parseFloat(style.outlineWidth) }; });
    check(focus.active && focus.outlineStyle !== 'none' && focus.outlineWidth >= 2, `${route} footer link lacks visible keyboard focus (${JSON.stringify(focus)})`);
    if (exerciseKeyboard) {
      const popupPromise = context.waitForEvent('page');
      await source.press('Enter');
      const popup = await popupPromise;
      check(Boolean(popup), `${route} keyboard activation did not open Source in a separate context`);
      await popup.close();
    }
    await page.evaluate(() => scrollTo(0, 0));
  };
  const verifyNavigation = async (route, includeDocumentation) => {
    const isDocs = route.startsWith('/docs/');
    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(base + route);
    const expected = [
      ...(includeDocumentation ? [{ label: 'Documentation', href: '/docs/' }] : []),
      { label: 'Company', href: 'https://shruggie.tech/' },
      { label: 'Download Skill', href: 'https://github.com/ShruggieTech/shruggie-brand/releases/latest' },
    ];
    for (const record of expected) {
      const link = page.locator(isDocs ? '#nd-sidebar a:visible' : '#nd-nav a:visible').filter({ hasText: new RegExp(`^${record.label}$`) });
      check(await link.count() === 1, `${route} desktop navigation lacks exactly one visible ${record.label} link`);
      if (await link.count() !== 1) continue;
      check(await link.getAttribute('href') === record.href, `${route} ${record.label} destination is not canonical`);
      const linkBox = await link.boundingBox();
      check(Boolean(linkBox && linkBox.width >= 44 && linkBox.height >= 44), `${route} desktop ${record.label} target is smaller than 44 by 44 CSS pixels`);
      if (record.label !== 'Documentation') {
        const rel = (await link.getAttribute('rel') ?? '').split(/\s+/);
        check(await link.getAttribute('target') === '_blank' && rel.includes('noopener') && rel.includes('noreferrer'), `${route} ${record.label} lacks safe external navigation behavior`);
      }
    }
    await page.setViewportSize({ width: 360, height: 800 });
    await page.reload({ waitUntil: 'networkidle' });
    const toggle = page.getByRole('button', { name: isDocs ? 'Open Sidebar' : 'Toggle Menu' });
    check(await toggle.count() === 1, `${route} lacks an accessible mobile menu control`);
    if (await toggle.count() === 1) await toggle.click();
    for (const record of expected.filter(({ label }) => label !== 'Documentation')) {
      const link = page.locator(isDocs ? '#nd-sidebar-mobile a:visible' : '#nd-nav a:visible').filter({ hasText: new RegExp(`^${record.label}$`) });
      check(await link.count() === 1, `${route} mobile navigation lacks exactly one visible ${record.label} link`);
      if (await link.count() !== 1) continue;
      const rel = (await link.getAttribute('rel') ?? '').split(/\s+/);
      check(await link.getAttribute('href') === record.href && await link.getAttribute('target') === '_blank' && rel.includes('noopener') && rel.includes('noreferrer'), `${route} mobile ${record.label} policy differs from desktop`);
      const linkBox = await link.boundingBox();
      check(Boolean(linkBox && linkBox.width >= 44 && linkBox.height >= 44), `${route} mobile ${record.label} target is smaller than 44 by 44 CSS pixels`);
    }
  };
  const box = async (targetPage, selector) => {
    const measured = await targetPage.locator(selector).first().evaluate((element) => { const rect = element.getBoundingClientRect(); return { left: rect.left, right: rect.right, width: rect.width, center: rect.left + rect.width / 2 }; });
    return measured;
  };
  const namedBoxes = async (targetPage, selector) => targetPage.locator(selector).evaluateAll((elements) => Object.fromEntries(elements.map((element) => { const rect = element.getBoundingClientRect(); return [element.textContent?.trim(), { left: rect.left, right: rect.right, width: rect.width, center: rect.left + rect.width / 2 }]; })));
  const settleTheme = async (targetPage, route, theme) => {
    await targetPage.goto(base + route);
    await targetPage.evaluate((selectedTheme) => localStorage.setItem('theme', selectedTheme), theme);
    await targetPage.reload({ waitUntil: 'networkidle' });
  };
  const verifyStableGeometry = async () => {
    const brandPortalPairs = brands.map((brand) => ({ overview: `/${brand.slug}/guidelines/`, assets: `/${brand.slug}/downloads/` }));
    for (const scale of [1, 2]) {
      const geometryContext = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: scale });
      const geometryPage = await geometryContext.newPage();
      for (const theme of visualThemes) {
        await settleTheme(geometryPage, '/', theme);
        const gutter = await geometryPage.locator('html').evaluate((element) => getComputedStyle(element).scrollbarGutter);
        check(gutter.includes('stable'), `shared document shell lacks stable scrollbar allocation at scale ${scale}`);
        const headerReference = await box(geometryPage, '#nd-nav nav');
        const controlReferences = await namedBoxes(geometryPage, '#nd-nav nav a:visible');
        const tallState = await geometryPage.evaluate(() => ({ clientHeight: document.documentElement.clientHeight, scrollHeight: document.documentElement.scrollHeight }));
        check(tallState.scrollHeight > tallState.clientHeight, `/ ${theme} scale ${scale} does not exercise the asserted tall-page scrollbar state (${JSON.stringify(tallState)})`);
        await geometryPage.evaluate(() => { document.querySelector('#content')?.setAttribute('hidden', ''); document.querySelector('.site-footer')?.setAttribute('hidden', ''); });
        const shortState = await geometryPage.evaluate(() => ({ clientHeight: document.documentElement.clientHeight, scrollHeight: document.documentElement.scrollHeight }));
        check(shortState.scrollHeight <= shortState.clientHeight, `/ ${theme} scale ${scale} does not exercise the asserted short-page scrollbar state (${JSON.stringify(shortState)})`);
        for (const problem of geometryProblems(headerReference, await box(geometryPage, '#nd-nav nav'))) failures.push(`/ ${theme} scale ${scale} short-to-tall header ${problem}`);
        const shortControls = await namedBoxes(geometryPage, '#nd-nav nav a:visible');
        for (const [label, reference] of Object.entries(controlReferences)) for (const problem of geometryProblems(reference, shortControls[label])) failures.push(`/ ${theme} scale ${scale} short-to-tall ${label} control ${problem}`);
        for (const routes of brandPortalPairs) {
          await settleTheme(geometryPage, routes.overview, theme);
          const portalShellReference = await box(geometryPage, '#nd-docs-layout');
          const portalPageReference = await box(geometryPage, '.guideline-page');
          const portalSidebarReference = await box(geometryPage, '#nd-sidebar');
          await settleTheme(geometryPage, routes.assets, theme);
          for (const problem of geometryProblems(portalShellReference, await box(geometryPage, '#nd-docs-layout'))) failures.push(`${routes.assets} ${theme} scale ${scale} portal shell ${problem}`);
          for (const problem of geometryProblems(portalPageReference, await box(geometryPage, '.guideline-page'), ['left', 'width', 'center'])) failures.push(`${routes.assets} ${theme} scale ${scale} portal page ${problem}`);
          for (const problem of geometryProblems(portalSidebarReference, await box(geometryPage, '#nd-sidebar'))) failures.push(`${routes.assets} ${theme} scale ${scale} portal navigation ${problem}`);
        }
        await settleTheme(geometryPage, '/docs/', theme);
        const docsShellReference = await box(geometryPage, '#nd-docs-layout');
        const docsPageReference = await box(geometryPage, '.docs-page');
        const docsSidebarReference = await box(geometryPage, '#nd-sidebar');
        const placeholderWidth = await geometryPage.locator('#nd-docs-layout').evaluate((element) => getComputedStyle(element).getPropertyValue('--fd-toc-width').trim());
        check(placeholderWidth === '268px', `/docs/ ${theme} scale ${scale} does not reserve the desktop TOC track (${placeholderWidth})`);
        for (const route of ['/docs/04-toolchain/', '/docs/09-portability/']) {
          await settleTheme(geometryPage, route, theme);
          for (const problem of geometryProblems(docsShellReference, await box(geometryPage, '#nd-docs-layout'))) failures.push(`${route} ${theme} scale ${scale} docs shell ${problem}`);
          for (const problem of geometryProblems(docsPageReference, await box(geometryPage, '.docs-page'), ['left', 'width', 'center'])) failures.push(`${route} ${theme} scale ${scale} docs page ${problem}`);
          for (const problem of geometryProblems(docsSidebarReference, await box(geometryPage, '#nd-sidebar'))) failures.push(`${route} ${theme} scale ${scale} docs navigation ${problem}`);
          const toc = geometryPage.locator('#nd-toc:visible');
          check(await toc.count() === 1 && await toc.evaluate((element) => getComputedStyle(element).position === 'sticky'), `${route} ${theme} scale ${scale} lacks a usable sticky desktop TOC`);
        }
      }
      for (const viewport of [{ width: 1280, height: 900 }, { width: 360, height: 800 }, { width: 640, height: 450 }]) {
        await geometryPage.setViewportSize(viewport);
        for (const route of ['/', ...brandPortalPairs.flatMap(({ overview, assets }) => [overview, assets]), '/docs/', '/docs/04-toolchain/']) {
          await geometryPage.goto(base + route);
          const overflow = await geometryPage.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
          check(overflow <= 1, `${route} overflows horizontally by ${overflow}px at ${viewport.width}x${viewport.height} scale ${scale}`);
        }
      }
      await geometryContext.close();
    }
  };
  const measurePagination = async (route, width, theme, forceWrap = false) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto(base + route);
    await page.evaluate((selectedTheme) => localStorage.setItem('theme', selectedTheme), theme);
    await page.reload({ waitUntil: 'networkidle' });
    const links = page.locator('.docs-pagination > a');
    if (forceWrap && await links.count() > 0) await links.first().locator('p').first().evaluate((element) => { element.style.width = '3rem'; element.style.whiteSpace = 'normal'; element.style.overflowWrap = 'anywhere'; });
    const samples = await links.evaluateAll((elements) => elements.map((element) => {
      const labelGroup = element.querySelector(':scope > div'); const icon = labelGroup?.querySelector('svg'); const label = labelGroup?.querySelector('p');
      if (!labelGroup || !icon || !label) return null;
      const iconBox = icon.getBoundingClientRect(); const labelBox = labelGroup.getBoundingClientRect(); const iconStyle = getComputedStyle(icon); const labelStyle = getComputedStyle(label);
      return { iconCenter: iconBox.top + iconBox.height / 2, labelCenter: labelBox.top + labelBox.height / 2, iconWidth: iconBox.width, iconHeight: iconBox.height, flexShrink: iconStyle.flexShrink, translate: iconStyle.translate, labelLines: labelBox.height / Number.parseFloat(labelStyle.lineHeight) };
    }));
    check(samples.length > 0 && samples.every(Boolean), `${route} ${theme} at ${width}px lacks measurable pagination cues`);
    for (const sample of samples.filter(Boolean)) for (const problem of paginationCueProblems(sample)) failures.push(`${route} ${theme} at ${width}px: ${problem} (${JSON.stringify(sample)})`);
    if (forceWrap) check(samples.some((sample) => sample && sample.labelLines > 1.5), `${route} ${theme} at ${width}px did not exercise a wrapped pagination label`);
  };
  await verifyFooter('/', true);
  await verifyNavigation('/', true);
  await verifyNavigation('/docs/04-toolchain/', false);
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto(base + '/');
  check(await page.locator('h1').textContent() === 'We build comprehensive brands', 'homepage headline does not match the approved wording');
  const heroActions = await page.locator('.hero a').evaluateAll((elements) => elements.map((element) => ({ label: element.textContent?.trim(), href: element.getAttribute('href'), target: element.getAttribute('target'), rel: element.getAttribute('rel') })));
  check(JSON.stringify(heroActions) === JSON.stringify([
    { label: 'Documentation', href: '/docs/', target: null, rel: null },
    { label: 'Download Skill', href: 'https://github.com/ShruggieTech/shruggie-brand/releases/latest', target: '_blank', rel: 'noopener noreferrer' },
    { label: 'Explore Our Portfolio↓', href: '#portfolio', target: null, rel: null },
  ]), `homepage hero action order or policy differs from the approved contract (${JSON.stringify(heroActions)})`);
  check(await page.locator('#portfolio-heading').textContent() === 'Our Portfolio', 'homepage portfolio heading is not exact');
  check((await page.locator('#portfolio .section-heading > p').textContent() ?? '').includes('identity spectrum'), 'homepage portfolio description omits identity spectrum');
  check(await page.locator('.system-callout').count() === 0 && !(await page.locator('body').innerText()).includes('The system underneath'), 'homepage still emits the removed system callout');
  const portfolioAction = page.locator('.hero-portfolio-link');
  const portfolioSpacing = await portfolioAction.evaluate((element) => { const previous = element.previousElementSibling; const link = element.getBoundingClientRect(); const prior = previous?.getBoundingClientRect(); const cue = element.querySelector('[aria-hidden="true"]'); const cueBox = cue?.getBoundingClientRect(); return { gap: prior ? link.top - prior.bottom : 0, linkCenter: link.top + link.height / 2, cueCenter: cueBox ? cueBox.top + cueBox.height / 2 : 0, cue: cue?.textContent, hidden: cue?.getAttribute('aria-hidden') }; });
  check(portfolioSpacing.gap >= 20 && Math.abs(portfolioSpacing.linkCenter - portfolioSpacing.cueCenter) <= 1 && portfolioSpacing.cue === '↓' && portfolioSpacing.hidden === 'true', `homepage portfolio supporting action spacing or cue alignment failed (${JSON.stringify(portfolioSpacing)})`);
  check(await page.locator('.brand-card').count() === 6, 'homepage must render exactly six desktop brand cards');
  check(await page.locator('.brand-accordion').count() === 6, 'homepage must render exactly six mobile brand disclosures');
  check(await page.locator('.brand-card a').count() === 12, 'desktop cards must expose exactly two actions per brand');
  check(await page.locator('.portfolio-vendor-notice').count() === 1, 'portfolio must render exactly one shared third-party notice');
  check(await page.locator('.vendor-boundary').count() === 0, 'portfolio must not repeat card-level vendor notices');
  const applicableBrands = new Set((await page.locator('.brand-card .vendor-marker').evaluateAll((markers) => markers.map((marker) => marker.closest('.brand-card')?.querySelector('h3')?.textContent?.replace(' Independent third-party project', '').replace('*', '').trim()))).filter(Boolean));
  check(JSON.stringify([...applicableBrands].sort()) === JSON.stringify(brands.filter((brand) => brand.vendorBoundary).map((brand) => brand.title).sort()), `portfolio vendor markers differ from generated applicability (${JSON.stringify([...applicableBrands])})`);
  const sharedNoticeText = await page.locator('.portfolio-vendor-notice').innerText();
  for (const notice of [...new Set(brands.flatMap((brand) => brand.vendorBoundary ? [brand.vendorBoundary] : []))]) check(sharedNoticeText.includes(notice), 'shared third-party notice does not preserve generated wording');
  const measurePortfolioIcons = async (selector, label) => {
    for (const card of await page.locator(selector).all()) {
      const title = await card.locator(selector === '.brand-card' ? 'h3' : '.mobile-brand-title').textContent();
      const wrapper = await card.locator('.brand-icon').boundingBox();
      const image = await card.locator('.brand-icon img').boundingBox();
      check(Boolean(wrapper && image), `${title} ${label} icon lacks measurable bounds`);
      if (!wrapper || !image) continue;
      check(Math.abs(wrapper.width - wrapper.height) <= 0.5, `${title} ${label} icon wrapper is not square (${wrapper.width}x${wrapper.height})`);
      check(Math.abs(image.width - image.height) <= 0.5, `${title} ${label} icon image box is not square (${image.width}x${image.height})`);
      check(image.x >= wrapper.x && image.y >= wrapper.y && image.x + image.width <= wrapper.x + wrapper.width + 0.5 && image.y + image.height <= wrapper.y + wrapper.height + 0.5, `${title} ${label} icon escapes its wrapper`);
      check(Math.abs((image.x - wrapper.x) - (wrapper.x + wrapper.width - image.x - image.width)) <= 0.5, `${title} ${label} icon has asymmetric horizontal margins`);
      check(Math.abs((image.y - wrapper.y) - (wrapper.y + wrapper.height - image.y - image.height)) <= 0.5, `${title} ${label} icon has asymmetric vertical margins`);
    }
  };
  await measurePortfolioIcons('.brand-card', 'desktop');
  for (const [index, card] of (await page.locator('.brand-card').all()).entries()) {
    check(await card.evaluate((element) => element.tagName === 'ARTICLE' && !element.hasAttribute('href')), `${brands[index].slug} desktop card is an implicit navigation target`);
    const before = await card.boundingBox();
    const links = await card.locator('.brand-actions a').evaluateAll((anchors) => anchors.map((anchor) => ({ label: anchor.textContent?.trim(), href: anchor.getAttribute('href'), download: anchor.getAttribute('download') })));
    check(JSON.stringify(links) === JSON.stringify([
      { label: 'Guidelines', href: brands[index].guidelinesPath, download: null },
      { label: 'Download Kit', href: brands[index].kitArchive, download: brands[index].kitArchiveFilename },
    ]), `${brands[index].slug} desktop actions differ from generated destinations (${JSON.stringify(links)})`);
    await card.hover();
    await page.waitForTimeout(200);
    check(await card.locator('.brand-actions').evaluate((element) => getComputedStyle(element).opacity) === '1', `${brands[index].slug} desktop actions do not remain revealed on hover`);
    const hovered = await card.boundingBox();
    await card.locator('.brand-actions a').first().focus();
    const focused = await card.boundingBox();
    check(Boolean(before && hovered && focused && Math.abs(before.width - hovered.width) <= .5 && Math.abs(before.height - hovered.height) <= .5 && Math.abs(before.width - focused.width) <= .5 && Math.abs(before.height - focused.height) <= .5), `${brands[index].slug} card geometry changes across interaction states`);
    await page.keyboard.press('Escape');
    await page.waitForTimeout(200);
    check(await card.locator('.brand-actions').evaluate((element) => getComputedStyle(element).opacity) === '0' && await card.locator('.brand-card-description').evaluate((element) => getComputedStyle(element).opacity) === '1', `${brands[index].slug} action panel is not dismissible with Escape`);
  }
  const glitchpadCard = page.locator('.brand-card', { hasText: 'Glitchpad' });
  const glitchpadCardStyle = await glitchpadCard.evaluate((element) => ({ backgroundColor: getComputedStyle(element).backgroundColor, backgroundImage: getComputedStyle(element).backgroundImage, foreground: getComputedStyle(element).color, bodyForeground: getComputedStyle(element.querySelector('.brand-card-description')).color, surface: element.getAttribute('data-showcase-surface'), shadow: getComputedStyle(element.querySelector('.brand-icon')).boxShadow }));
  check(glitchpadCardStyle.surface === 'governed' && glitchpadCardStyle.backgroundColor === 'rgb(18, 20, 22)' && glitchpadCardStyle.backgroundImage === 'none', `Glitchpad card does not use its governed charcoal surface (${JSON.stringify(glitchpadCardStyle)})`);
  check(glitchpadCardStyle.foreground === 'rgb(255, 255, 255)' && glitchpadCardStyle.bodyForeground === 'rgb(255, 255, 255)', `Glitchpad card does not use its generated contrast foreground (${JSON.stringify(glitchpadCardStyle)})`);
  check(glitchpadCardStyle.shadow === 'none', `Glitchpad card retains an accent showcase glow (${glitchpadCardStyle.shadow})`);
  for (const card of await page.locator('.brand-card').all()) {
    if ((await card.locator('h3').textContent()) === 'Glitchpad') continue;
    const style = await card.evaluate((element) => ({ image: getComputedStyle(element).backgroundImage, surface: element.getAttribute('data-showcase-surface') }));
    if (style.surface === 'governed') check(style.image === 'none', `${await card.locator('h3').textContent()} governed showcase added an unapproved background image (${JSON.stringify(style)})`);
    else check(style.surface === null && style.image !== 'none', `${await card.locator('h3').textContent()} lost its existing showcase fallback (${JSON.stringify(style)})`);
  }
  const homeText = (await page.locator('body').innerText()).toLowerCase();
  for (const rejected of ['a shruggietech project', 'skill 1.', 'canon', 'example brand', 'read the system']) check(!homeText.includes(rejected), `homepage contains retired wording: ${rejected}`);
  const visibleHeaderLinks = async () => page.locator('#nd-nav a').evaluateAll((links) => links.filter((link) => { const rect = link.getBoundingClientRect(); return ['Documentation', 'Company', 'Download Skill', 'View on GitHub'].includes(link.textContent?.trim()) && rect.bottom > 0 && rect.top < window.innerHeight && rect.right > 0 && rect.left < window.innerWidth; }).map((link) => ({ text: link.textContent?.trim(), href: link.getAttribute('href') })));
  const desktopLinks = await visibleHeaderLinks();
  check(JSON.stringify(desktopLinks) === JSON.stringify([{ text: 'Documentation', href: '/docs/' }, { text: 'Company', href: 'https://shruggie.tech/' }, { text: 'Download Skill', href: 'https://github.com/ShruggieTech/shruggie-brand/releases/latest' }]), `desktop landing navigation differs from the approved order (${JSON.stringify(desktopLinks)})`);
  await page.setViewportSize({ width: 360, height: 900 });
  check(await page.locator('.brand-grid-desktop').evaluate((element) => getComputedStyle(element).display) === 'none', 'desktop card grid remains exposed at the mobile breakpoint');
  check(await page.locator('.brand-accordion-list').evaluate((element) => getComputedStyle(element).display) === 'block', 'mobile disclosures are not exposed at the mobile breakpoint');
  for (const [index, disclosure] of (await page.locator('.brand-accordion').all()).entries()) {
    check(!(await disclosure.evaluate((element) => element.open)), `${brands[index].slug} mobile disclosure does not begin collapsed`);
    check(!(await disclosure.locator('.brand-actions a').first().isVisible()), `${brands[index].slug} collapsed disclosure exposes hidden actions`);
    const summary = disclosure.locator('summary');
    const summaryBox = await summary.boundingBox();
    check(Boolean(summaryBox && summaryBox.width >= 44 && summaryBox.height >= 44), `${brands[index].slug} disclosure target is smaller than 44 by 44 CSS pixels`);
  }
  const firstDisclosure = page.locator('.brand-accordion').first();
  await firstDisclosure.locator('summary').focus();
  await page.keyboard.press('Enter');
  check(await firstDisclosure.evaluate((element) => element.open), 'keyboard activation does not expand a mobile disclosure');
  check(await firstDisclosure.locator('.brand-actions a').count() === 2 && await firstDisclosure.locator('.brand-actions a').first().isVisible(), 'expanded mobile disclosure lacks both visible actions');
  await measurePortfolioIcons('.brand-accordion', 'mobile');
  await page.evaluate(() => { document.documentElement.style.zoom = '2'; });
  await measurePortfolioIcons('.brand-accordion', '200-percent zoom');
  check(await firstDisclosure.evaluate((element) => element.scrollWidth <= element.clientWidth + 2), 'expanded mobile disclosure clips horizontally at 200 percent zoom');
  await page.evaluate(() => { document.documentElement.style.zoom = ''; });
  await page.getByRole('button', { name: 'Toggle Menu' }).click();
  const mobileLinks = await visibleHeaderLinks();
  check(JSON.stringify(mobileLinks) === JSON.stringify([{ text: 'Documentation', href: '/docs/' }, { text: 'Company', href: 'https://shruggie.tech/' }, { text: 'Download Skill', href: 'https://github.com/ShruggieTech/shruggie-brand/releases/latest' }, { text: 'View on GitHub', href: 'https://github.com/ShruggieTech/shruggie-brand' }]), `mobile landing menu differs from the approved order (${JSON.stringify(mobileLinks)})`);
  for (const link of await page.getByRole('link').filter({ hasText: /^(Documentation|Company|Download Skill|View on GitHub)$/ }).all()) { const box = await link.boundingBox(); if (box && box.y < 900) check(box.width >= 44 && box.height >= 44, `${await link.textContent()} mobile navigation target is smaller than 44 by 44 CSS pixels`); }
  await page.locator('a').filter({ hasText: /^Documentation$/ }).evaluateAll((links) => links.find((link) => { const rect = link.getBoundingClientRect(); return rect.bottom > 0 && rect.top < window.innerHeight; })?.focus());
  await page.keyboard.press('Escape');
  await page.waitForTimeout(100);
  const escapedLinks = await visibleHeaderLinks();
  const menuState = await page.getByRole('button', { name: 'Toggle Menu' }).getAttribute('data-state');
  check(menuState === 'closed', `mobile landing menu does not close with Escape (${menuState}; ${JSON.stringify(escapedLinks)})`);
  for (const route of htmlRoutes) {
    const contract = routeByPath.get(route);
    check(Boolean(contract), `${route} is absent from the generated route contract`);
    if (!contract) continue;
    for (const width of [360, 1280]) {
      await page.setViewportSize({ width, height: 900 });
      const response = await page.goto(base + route);
      check(response?.status() === 200, `${route} returned ${response?.status()}`);
      check(await page.title() === contract.documentTitle, `${route} title disagrees with the route contract`);
      const oneContent = async (selector) => await page.locator(selector).count() === 1 ? await page.locator(selector).getAttribute('content') : null;
      check(await oneContent('meta[name="description"]') === contract.description, `${route} description disagrees with the route contract`);
      check(await page.locator('link[rel="canonical"]').count() === 1 && await page.locator('link[rel="canonical"]').getAttribute('href') === contract.canonical, `${route} canonical URL disagrees with the route contract`);
      check(await oneContent('meta[property="og:title"]') === contract.documentTitle, `${route} Open Graph title disagrees with the route contract`);
      check(await oneContent('meta[property="og:description"]') === contract.description, `${route} Open Graph description disagrees with the route contract`);
      check(await oneContent('meta[property="og:url"]') === contract.canonical, `${route} Open Graph URL disagrees with the route contract`);
      check(await oneContent('meta[property="og:image"]') === contract.social.url, `${route} Open Graph image disagrees with the route contract`);
      check(await oneContent('meta[property="og:image:width"]') === String(contract.social.width), `${route} Open Graph image width disagrees with the route contract`);
      check(await oneContent('meta[property="og:image:height"]') === String(contract.social.height), `${route} Open Graph image height disagrees with the route contract`);
      check(await oneContent('meta[property="og:image:type"]') === contract.social.type, `${route} Open Graph image type disagrees with the route contract`);
      check(await oneContent('meta[property="og:image:alt"]') === contract.social.alt, `${route} Open Graph image alt text disagrees with the route contract`);
      check(await oneContent('meta[name="twitter:card"]') === 'summary_large_image', `${route} lacks the large Twitter card contract`);
      check(await oneContent('meta[name="twitter:title"]') === contract.documentTitle, `${route} Twitter title disagrees with the route contract`);
      check(await oneContent('meta[name="twitter:description"]') === contract.description, `${route} Twitter description disagrees with the route contract`);
      check(await oneContent('meta[name="twitter:image"]') === contract.social.url, `${route} Twitter image disagrees with the route contract`);
      check(await oneContent('meta[name="twitter:image:alt"]') === contract.social.alt, `${route} Twitter image alt text disagrees with the route contract`);
      const jsonLdScripts = page.locator('script[type="application/ld+json"]');
      check(await jsonLdScripts.count() === 1, `${route} must expose exactly one JSON-LD graph`);
      if (await jsonLdScripts.count() === 1) {
        try { check(JSON.stringify(JSON.parse(await jsonLdScripts.textContent())) === JSON.stringify(contract.structuredData), `${route} JSON-LD disagrees with the route contract`); }
        catch (error) { failures.push(`${route} JSON-LD cannot be parsed: ${error.message}`); }
      }
      check(await page.locator('link[rel="icon"]').count() >= 1, `${route} lacks a favicon`);
      const publicSurface = `${await page.content()}\n${JSON.stringify(contract)}`.toLowerCase();
      for (const rejected of retiredPublicPhrases) check(!publicSurface.includes(rejected), `${route} contains retired public wording in rendered content, metadata, or route data: ${rejected}`);
      if (contract.brandSlug === 'eso-weave') {
        check((await page.locator('body').innerText()).includes(contract.vendorBoundary), `${route} does not visibly render the ESO Weave vendor boundary`);
        check(await oneContent('meta[name="brand-vendor-boundary"]') === contract.vendorBoundary, `${route} omits the ESO Weave vendor-boundary metadata`);
        const brandEntity = contract.structuredData['@graph'].find((item) => item['@type'] === 'Brand');
        if (contract.kind === 'guidelines') check(brandEntity?.disambiguatingDescription === contract.vendorBoundary && brandEntity?.usageInfo === contract.vendorBoundaryUrl, `${route} omits the ESO Weave structured vendor boundary`);
      }
      if (contract.kind === 'docs-index' || contract.kind === 'docs-page') check(await page.locator('header a').filter({ hasText: /^Documentation$/ }).count() <= 1, `${route} repeats the documentation root in navigation at ${width}px`);
      if (contract.kind === 'docs-page' && width === 1280) {
        const record = documentationByPath.get(route);
        check(Boolean(record), `${route} lacks generated documentation navigation metadata`);
        if (record) check(await page.locator('#nd-sidebar button[data-state="open"]').filter({ hasText: new RegExp(`^${record.navigation.section}$`) }).count() === 1, `${route} does not keep its ${record.navigation.section} parent identifiable and expanded`);
      }
      if (route === '/shruggietech/guidelines/') {
        check(!(await page.locator('body').innerText()).toLowerCase().includes('a shruggietech project'), `${route} contains a self-endorsement`);
      }
      if (['guidelines', 'guidelines-topic', 'downloads'].includes(contract.kind)) {
        const portal = portalBySlug.get(contract.brandSlug);
        check(Boolean(portal), `${route} lacks a generated portal record`);
        check(await page.locator('.guideline-page').count() === 1, `${route} lacks one guideline document`);
        check(await page.locator('.guide-nav-title').count() >= 1, `${route} lacks the brand-specific guideline identity`);
        if (width === 1280) check(await page.locator('#nd-sidebar a[data-active="true"], #nd-sidebar a[aria-current="page"]').count() >= 1, `${route} lacks an active desktop guideline topic`);
        if (width === 1280 && ['logos', 'color', 'typography'].includes(contract.guideTopic)) check(await page.locator('#nd-sidebar button[data-state="open"]').filter({ hasText: /^Identity$/ }).count() === 1, `${route} does not keep its Identity parent identifiable and expanded`);
        check(await page.locator('.guide-footer a[href="#guide-title"]').count() === 1, `${route} lacks a separate Back to top link`);
        check(await page.locator('.guide-footer .guide-host-exit[href="/"]').count() === 1, `${route} lacks a separate All brands exit`);
        check(await page.locator('.shell, .site-footer').count() === 0, `${route} leaks the marketing-site shell into the guideline portal`);
        const bodyText = (await page.locator('body').innerText()).toLowerCase();
        check(!bodyText.includes('we build comprehensive brands'), `${route} leaks host marketing copy into the guideline portal`);
        if (contract.guideTopic === 'color') {
          check(await page.locator('.color-row').count() === portal.palettes.dark.length + portal.palettes.light.length, `${route} does not render every dark and light palette entry`);
          check(await page.getByRole('heading', { name: 'Dark palette' }).count() === 1 && await page.getByRole('heading', { name: 'Light palette' }).count() === 1, `${route} lacks independently grouped dark and light palettes`);
          const copy = page.locator('.guide-copy').first();
          const copySize = await copy.evaluate((element) => ({ width: element.getBoundingClientRect().width, height: element.getBoundingClientRect().height }));
          check(copySize.width >= 44 && copySize.height >= 44, `${route} color copy target is smaller than 44px (${JSON.stringify(copySize)})`);
          await copy.click();
          const copyStatus = copy.locator('xpath=following-sibling::span[@data-copy-status][1]');
          await copyStatus.waitFor({ state: 'attached' });
          await page.waitForFunction((buttonLabel) => [...document.querySelectorAll('button')].find((button) => button.getAttribute('aria-label') === buttonLabel)?.nextElementSibling?.textContent?.startsWith('Copied '), await copy.getAttribute('aria-label'));
          check((await copyStatus.textContent()).startsWith('Copied '), `${route} copy action did not announce success`);
          await page.locator('.color-details').first().locator('summary').click();
          check(await page.locator('.color-details[open]').count() === 1, `${route} cannot reveal one row's secondary color formats independently`);
        }
        if (contract.guideTopic === 'assets') {
          check(await page.locator('.asset-tile').count() === portal.asset_families.reduce((total, family) => total + family.assets.length, 0), `${route} does not render every representative visual asset`);
          check(await page.locator('.resource-list li').count() === portal.resources.length, `${route} does not render every nonvisual resource`);
          const previewHeights = await page.locator('.asset-preview').evaluateAll((elements) => elements.map((element) => element.getBoundingClientRect().height));
          check(previewHeights.every((height) => height <= 193), `${route} contains an unbounded asset preview`);
          const assetLinks = page.locator('a[data-kit-asset]');
          const catalogHrefs = await assetLinks.evaluateAll((links) => links.map((link) => link.getAttribute('href')));
          const expectedHrefs = [...portal.asset_families.flatMap((family) => family.assets.flatMap((asset) => asset.deliveries.map((delivery) => delivery.url))), ...portal.resources.map((resource) => resource.url)];
          check(new Set(catalogHrefs).size === catalogHrefs.length, `${route} repeats a delivery path in the catalog`);
          check(expectedHrefs.length === catalogHrefs.length && expectedHrefs.every((href) => catalogHrefs.includes(href)), `${route} catalog does not exactly cover its generated deliveries and resources`);
          await page.getByLabel('Search assets').fill('no-such-brand-asset');
          check(await page.locator('.asset-empty').count() === 1 && (await page.locator('.asset-count').textContent()).startsWith('0 '), `${route} lacks an honest empty result state`);
          await page.getByRole('button', { name: 'Show all assets' }).click();
          check(await page.locator('.asset-tile').count() > 0 && new URL(page.url()).search === '', `${route} reset does not restore the full library and clean URL`);
        }
        if (width === 1280) {
          await page.evaluate(() => { document.documentElement.style.zoom = '2'; });
          const zoomOverflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
          check(zoomOverflow <= 1, `${route} overflows horizontally at 200 percent zoom by ${zoomOverflow}px`);
          await page.evaluate(() => { document.documentElement.style.zoom = ''; });
        }
      }
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      if (overflow > 1) {
        const offenders = await page.evaluate(() => [...document.querySelectorAll('*')].filter((element) => element.getBoundingClientRect().right > document.documentElement.clientWidth + 1).slice(0, 5).map((element) => `${element.tagName}.${element.className}`));
        failures.push(`${route} overflows horizontally at ${width}px by ${overflow}px (${offenders.join(', ')})`);
      }
      const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
      for (const violation of results.violations) failures.push(`${route} at ${width}px fails ${violation.id}: ${violation.nodes.map((node) => `${node.target.join(' ')} (${node.failureSummary ?? 'no contrast detail'})`).join(', ')}`);
    }
  }
  for (const portal of guidelinePortals) {
    for (const topic of ['assets', 'logos']) {
      const route = topic === 'assets' ? `/${portal.brand.slug}/downloads/` : `/${portal.brand.slug}/guidelines/${topic}/`;
      for (const width of [360, 768, 1280]) {
        for (const theme of visualThemes) {
          await page.setViewportSize({ width, height: 900 });
          await page.goto(base + route);
          await page.evaluate((selectedTheme) => localStorage.setItem('theme', selectedTheme), theme);
          await page.reload({ waitUntil: 'networkidle' });
          if (topic === 'assets') await measurePreviewLayouts(route, '.asset-preview', '.asset-summary', `${theme} at ${width}px`);
          else await measurePreviewLayouts(route, '.logo-example', 'figcaption', `${theme} at ${width}px`);
          if (width === 1280) {
            await page.evaluate(() => { document.documentElement.style.zoom = '2'; });
            if (topic === 'assets') await measurePreviewLayouts(route, '.asset-preview', '.asset-summary', `${theme} at 200 percent zoom`);
            else await measurePreviewLayouts(route, '.logo-example', 'figcaption', `${theme} at 200 percent zoom`);
            await page.evaluate(() => { document.documentElement.style.zoom = ''; });
          }
        }
      }
    }
  }
  await page.setViewportSize({ width: 1280, height: 900 });
  for (const sample of [{ route: '/glitchpad/guidelines/logos/', child: '/glitchpad/guidelines/logos/' }, { route: '/docs/06-logo-protocol/', child: '/docs/06-logo-protocol/' }]) {
    await page.goto(base + sample.route);
    const identity = page.locator('#nd-sidebar button').filter({ hasText: /^Identity$/ });
    check(await identity.count() === 1, `${sample.route} lacks the keyboard-operable Identity disclosure`);
    if (await identity.count() !== 1) continue;
    await identity.focus();
    await identity.press('Enter');
    check(await identity.getAttribute('data-state') === 'closed', `${sample.route} Identity disclosure does not collapse from the keyboard`);
    await identity.press('Enter');
    check(await identity.getAttribute('data-state') === 'open' && await page.locator(`#nd-sidebar a[href="${sample.child}"]`).isVisible(), `${sample.route} Identity disclosure does not restore its active child from the keyboard`);
  }
  const noScriptContext = await browser.newContext({ viewport: { width: 1280, height: 900 }, javaScriptEnabled: false });
  const noScriptPage = await noScriptContext.newPage();
  await noScriptPage.goto(base + '/');
  check(await noScriptPage.locator('.brand-card a').count() === 12 && await noScriptPage.locator('.brand-card a').first().isVisible() && await noScriptPage.locator('.brand-accordion summary').count() === 6, 'no-script homepage does not retain visible guidelines, downloads, and disclosures');
  await noScriptPage.goto(base + '/glitchpad/downloads/');
  check(await noScriptPage.locator('.hierarchy-noscript-nav a').count() === 8, 'no-script guideline fallback does not expose the complete navigation hierarchy');
  check(await noScriptPage.locator('.hierarchy-noscript-nav a[aria-current="page"]').count() === 1, 'no-script guideline fallback does not identify the current topic');
  check(await noScriptPage.locator('.asset-tile').count() > 0 && await noScriptPage.locator('.resource-list a[data-kit-asset]').count() > 0, 'no-script asset route does not retain complete server-rendered browsing and downloads');
  check((await noScriptPage.locator('body').innerText()).includes('Search and filters require JavaScript'), 'no-script asset route does not explain its progressive enhancement boundary');
  await noScriptPage.goto(base + '/docs/06-logo-protocol/');
  check(await noScriptPage.locator('.hierarchy-noscript-nav a').count() === 10, 'no-script documentation fallback does not expose the complete navigation hierarchy');
  check(await noScriptPage.locator('.hierarchy-noscript-nav a[aria-current="page"]').count() === 1, 'no-script documentation fallback does not identify the current page');
  for (const brand of brands) {
    const removedRoot = await noScriptPage.goto(`${base}/${brand.slug}/`);
    check(removedRoot?.status() === 404, `/${brand.slug}/ remains reachable after removing brand landing pages`);
  }
  await noScriptContext.close();
  const touchContext = await browser.newContext({ viewport: { width: 1024, height: 900 }, hasTouch: true });
  const touchPage = await touchContext.newPage();
  await touchPage.goto(base + '/');
  check(await touchPage.locator('.brand-grid-desktop').evaluate((element) => getComputedStyle(element).display) === 'none', 'wide touch-only viewport exposes hover-dependent desktop cards');
  check(await touchPage.locator('.brand-accordion-list').evaluate((element) => getComputedStyle(element).display) === 'block', 'wide touch-only viewport does not expose native disclosures');
  await touchPage.locator('.brand-accordion summary').first().tap();
  check(await touchPage.locator('.brand-accordion').first().locator('.brand-actions a').first().isVisible(), 'wide touch-only disclosure does not reveal its actions');
  await touchPage.goto(base + '/glitchpad/guidelines/logos/');
  const touchIdentity = touchPage.locator('#nd-sidebar button').filter({ hasText: /^Identity$/ });
  check(await touchIdentity.count() === 1, 'touch guideline navigation lacks the Identity disclosure');
  if (await touchIdentity.count() === 1) {
    if (await touchIdentity.getAttribute('data-state') === 'open') await touchIdentity.tap();
    await touchIdentity.tap();
    check(await touchPage.locator('#nd-sidebar a[href="/glitchpad/guidelines/logos/"]').isVisible(), 'touch guideline navigation cannot reveal the active Identity child');
  }
  await touchPage.goto(base + '/docs/06-logo-protocol/');
  const touchDocsIdentity = touchPage.locator('#nd-sidebar button').filter({ hasText: /^Identity$/ });
  check(await touchDocsIdentity.count() === 1, 'touch documentation navigation lacks the Identity disclosure');
  if (await touchDocsIdentity.count() === 1) {
    if (await touchDocsIdentity.getAttribute('data-state') === 'open') await touchDocsIdentity.tap();
    await touchDocsIdentity.tap();
    check(await touchPage.locator('#nd-sidebar a[href="/docs/06-logo-protocol/"]').isVisible(), 'touch documentation navigation cannot reveal the active Identity child');
  }
  await touchContext.close();
  const sitemapResponse = await page.request.get(base + '/sitemap.xml');
  check(sitemapResponse.ok(), 'sitemap.xml cannot be fetched');
  if (sitemapResponse.ok()) {
    const sitemapText = await sitemapResponse.text();
    const locations = [...sitemapText.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]);
    const expectedLocations = routeRecords.map((route) => route.canonical);
    check(JSON.stringify(locations) === JSON.stringify(expectedLocations), 'sitemap entries or ordering disagree with the route contract');
    for (const location of locations) {
      const localPath = new URL(location).pathname;
      const response = await page.request.get(base + localPath, { maxRedirects: 0 });
      check(response.status() === 200, `sitemap URL ${location} does not resolve directly`);
    }
  }
  for (const route of routeRecords) {
    const response = await page.request.get(base + route.social.path);
    check(response.ok(), `${route.social.path} cannot be fetched`);
    if (response.ok()) {
      try {
        const info = pngInfo(Buffer.from(await response.body()));
        check(info.width === route.social.width && info.height === route.social.height, `${route.social.path} dimensions disagree with its route contract`);
        check(info.opaque && info.visible > 0, `${route.social.path} must be an opaque visible preview`);
      } catch (error) { failures.push(`${route.social.path} does not decode: ${error.message}`); }
    }
    if (route.pathname !== '/') {
      const withoutSlash = route.pathname.slice(0, -1);
      const redirect = await page.request.get(base + withoutSlash, { maxRedirects: 0 });
      check(isCanonicalRedirect(redirect.status(), redirect.headers().location, base, withoutSlash), `${withoutSlash} must permanently redirect once to its canonical same-origin trailing-slash path`);
    }
  }
  await page.setViewportSize({ width: 1280, height: 900 });
  await verifyFooter('/docs/04-toolchain/');
  check(await page.locator('.docs-page [style*="--callout-color"]').count() === 3, 'toolchain guidance must render the three explicit alert types as callouts');
  check(await page.locator('.docs-page blockquote').count() === 0, 'explicit toolchain alerts must not remain ordinary blockquotes');
  const codeBlocks = page.locator('.docs-page figure:has(pre)');
  check(await codeBlocks.count() > 0, 'toolchain guidance must render a native Fumadocs code block');
  const copyButton = page.getByRole('button', { name: 'Copy Text' }).first();
  check(await copyButton.count() === 1, 'toolchain code block lacks its copy action');
  if (await copyButton.count() === 1) {
    await copyButton.focus();
    const focusStyle = await copyButton.evaluate((element) => { const style = getComputedStyle(element); return { outlineStyle: style.outlineStyle, outlineWidth: Number.parseFloat(style.outlineWidth) }; });
    check(focusStyle.outlineStyle !== 'none' && focusStyle.outlineWidth >= 2, 'toolchain copy action lacks a visible keyboard focus indicator');
    await page.keyboard.press('Enter');
    const clipboard = await page.evaluate(() => navigator.clipboard.readText());
    check(clipboard.trim().length > 0, 'toolchain code block copy action produced an empty clipboard');
  }
  const preBehavior = await page.locator('.docs-page figure:has(pre)').first().evaluate((figure) => { const scroller = figure.querySelector('[role="region"]'); const pre = figure.querySelector('pre'); if (!scroller || !pre) return null; return { overflowX: getComputedStyle(scroller).overflowX, whiteSpace: getComputedStyle(pre).whiteSpace }; });
  check(Boolean(preBehavior && ['auto', 'scroll'].includes(preBehavior.overflowX) && preBehavior.whiteSpace.startsWith('pre')), `documentation code blocks do not preserve horizontal scrolling and preformatted whitespace (${JSON.stringify(preBehavior)})`);
  const tokenColors = await page.locator('.docs-page figure pre code span').evaluateAll((tokens) => [...new Set(tokens.map((token) => getComputedStyle(token).color))]);
  check(tokenColors.length > 1, 'documentation syntax highlighting has been flattened to one token color');
  const stringToken = page.locator(".docs-page .shiki span[style*='--shiki-light:#032F62']").first();
  check(await stringToken.count() === 1, 'toolchain guidance lacks a verifiable code string token');
  if (await stringToken.count() === 1) {
    const stringColors = await stringToken.evaluate((element) => { const probe = document.createElement('i'); probe.style.color = 'var(--primary)'; document.body.append(probe); const result = { actual: getComputedStyle(element).color, expected: getComputedStyle(probe).color }; probe.remove(); return result; });
    check(stringColors.actual === stringColors.expected, `documentation code string token is not the generated green (${JSON.stringify(stringColors)})`);
  }
  const inlineCode = page.locator('.docs-page :not(pre) > code').first();
  check(await inlineCode.count() === 1, 'toolchain guidance lacks a rendered inline-code sample');
  if (await inlineCode.count() === 1) check((await inlineCode.evaluate((element) => getComputedStyle(element).backgroundColor)) !== 'rgba(0, 0, 0, 0)', 'inline code lacks a distinct surface');
  check(await page.locator('header a').filter({ hasText: /^Documentation$/ }).count() <= 1, 'documentation header repeats the current documentation destination');
  const activeSidebar = page.locator('#nd-sidebar a[data-active="true"]');
  check(await activeSidebar.count() === 1, 'documentation sidebar must expose exactly one active page');
  if (await activeSidebar.count() === 1) check(Number(await activeSidebar.evaluate((element) => getComputedStyle(element).fontWeight)) >= 600, 'documentation sidebar active state is not visually distinct');
  const headingSizes = await page.locator('.docs-page h1, .docs-page h2, .docs-page h3').evaluateAll((headings) => headings.map((heading) => ({ tag: heading.tagName, size: Number.parseFloat(getComputedStyle(heading).fontSize) })));
  check(headingSizes.every(({ tag, size }) => size <= (tag === 'H1' ? 40 : tag === 'H2' ? 30 : 24)), 'documentation heading scale exceeds the readable content hierarchy');
  const firstSection = page.locator('.docs-page h2').first();
  if (await firstSection.count() === 1) { await firstSection.scrollIntoViewIfNeeded(); await page.waitForTimeout(100); check(await page.locator('#nd-toc a[data-active="true"]').count() >= 1, 'documentation table of contents lacks an active state after section navigation'); }
  await page.goto(base + '/docs/');
  const startLink = page.locator('.docs-page a[href*="releases/latest"]').first();
  const startBox = await startLink.boundingBox();
  check(Boolean(startBox && startBox.y < 900), 'documentation landing page does not surface its next action in the first viewport');
  const paginationCard = page.locator('.docs-pagination > a').first();
  check(await paginationCard.count() === 1, 'documentation landing page lacks a pagination card');
  if (await paginationCard.count() === 1) {
    const resting = await paginationCard.evaluate((element) => { const style = getComputedStyle(element); const title = element.querySelector(':scope > div > p'); const description = element.querySelector(':scope > p'); return { borderColor: style.borderColor, background: style.backgroundColor, decoration: style.textDecorationLine, height: element.getBoundingClientRect().height, titleWeight: Number(getComputedStyle(title).fontWeight), descriptionWeight: Number(getComputedStyle(description).fontWeight), descriptionWrap: getComputedStyle(description).whiteSpace }; });
    check(resting.decoration === 'none' && resting.height >= 44 && resting.titleWeight > resting.descriptionWeight && resting.descriptionWrap === 'normal', `documentation pagination contract failed (${JSON.stringify(resting)})`);
    await paginationCard.hover();
    const hovered = await paginationCard.evaluate((element) => ({ borderColor: getComputedStyle(element).borderColor, background: getComputedStyle(element).backgroundColor, decoration: getComputedStyle(element).textDecorationLine }));
    check(hovered.borderColor !== resting.borderColor && hovered.background === resting.background && hovered.decoration === 'none', `documentation pagination hover state is not neutral and border-led (${JSON.stringify({ resting, hovered })})`);
  }
  const editorial = page.locator('.docs-page :where(p, li, td, blockquote) > a').first();
  check(await editorial.count() === 1 && await editorial.evaluate((element) => getComputedStyle(element).textDecorationLine.includes('underline')), 'editorial links lack a persistent resting underline');
  for (const paginationCase of [{ route: '/docs/', count: 1 }, { route: '/docs/02-kit-anatomy/', count: 2 }, { route: '/docs/09-portability/', count: 1 }]) {
    await page.goto(base + paginationCase.route);
    const links = page.locator('.docs-pagination > a');
    check(await links.count() === paginationCase.count, `${paginationCase.route} has the wrong pagination neighbor count`);
    for (const href of await links.evaluateAll((elements) => elements.map((element) => element.getAttribute('href')))) check(Boolean(href && href.startsWith('/docs/') && href !== paginationCase.route), `${paginationCase.route} has an invalid pagination destination: ${href}`);
  }
  for (const route of ['/docs/', '/docs/02-kit-anatomy/', '/docs/09-portability/']) for (const width of visualWidths) for (const theme of visualThemes) await measurePagination(route, width, theme, route === '/docs/02-kit-anatomy/' && width === 360);
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto(base + '/docs/');
  for (const theme of visualThemes) {
    await page.evaluate((selectedTheme) => localStorage.setItem('theme', selectedTheme), theme);
    await page.reload({ waitUntil: 'networkidle' });
    const control = page.locator('button[data-theme-toggle]:visible');
    check(await control.count() === 1, `documentation ${theme} theme lacks the shared light/dark toggle button`);
    if (await control.count() !== 1) continue;
    const state = await control.evaluate((element) => { const box = element.getBoundingClientRect(); const style = getComputedStyle(element); return { disabled: element.disabled, cursor: style.cursor, role: element.tagName.toLowerCase(), name: element.getAttribute('aria-label'), width: box.width, height: box.height }; });
    for (const problem of themeControlProblems(state)) failures.push(`documentation ${theme} theme control: ${problem} (${JSON.stringify(state)})`);
    await control.focus();
    const focus = await control.evaluate((element) => { const style = getComputedStyle(element); return { active: document.activeElement === element, outlineStyle: style.outlineStyle, outlineWidth: Number.parseFloat(style.outlineWidth) }; });
    check(focus.active && focus.outlineStyle !== 'none' && focus.outlineWidth >= 2, `documentation ${theme} theme control lacks visible keyboard focus (${JSON.stringify(focus)})`);
    const wasDark = await page.locator('html').evaluate((element) => element.classList.contains('dark'));
    await control.press('Enter');
    try { await page.waitForFunction((previous) => document.documentElement.classList.contains('dark') !== previous, wasDark, { timeout: 5000 }); }
    catch { check(false, `documentation ${theme} theme control did not change theme after keyboard activation`); }
    await control.evaluate((element) => { element.disabled = true; });
    const disabled = await control.evaluate((element) => { const box = element.getBoundingClientRect(); const style = getComputedStyle(element); return { disabled: element.disabled, cursor: style.cursor, role: element.tagName.toLowerCase(), name: element.getAttribute('aria-label'), width: box.width, height: box.height }; });
    for (const problem of themeControlProblems(disabled)) failures.push(`documentation disabled theme control: ${problem} (${JSON.stringify(disabled)})`);
  }
  const themeSurfaces = new Map();
  for (const route of visualRoutes) {
    for (const width of visualWidths) {
      for (const theme of visualThemes) {
        await page.setViewportSize({ width, height: 900 });
        await page.goto(base + route);
        await page.evaluate((selectedTheme) => localStorage.setItem('theme', selectedTheme), theme);
        await page.reload({ waitUntil: 'networkidle' });
        await page.waitForTimeout(350);
        check(await page.locator('html').evaluate((element, selectedTheme) => element.classList.contains('dark') === (selectedTheme === 'dark'), theme), `${route} did not settle in the requested ${theme} theme`);
        const surface = await page.evaluate(() => { const style = getComputedStyle(document.body); return `${style.backgroundColor}|${style.color}`; });
        themeSurfaces.set(`${route}:${width}:${theme}`, surface);
        if (['guidelines', 'guidelines-topic', 'downloads'].includes(routeByPath.get(route)?.kind)) {
          check(await page.locator('.header-logo:visible').count() === 0, `${route} leaks the host ShruggieTech lockup into the brand-owned portal`);
          check(await page.locator('.guide-nav-title').count() >= 1, `${route} lacks its brand-owned portal identity at ${width}px`);
        } else {
          const logo = page.locator('.header-logo:visible').first();
          const logoBox = await logo.boundingBox();
          check(Boolean(logoBox && logoBox.width >= 100 && logoBox.height >= 24), `${route} ${theme} header logo is not legible at ${width}px`);
          const logoState = await logo.evaluate((element) => ({ complete: element.complete, naturalWidth: element.naturalWidth, naturalHeight: element.naturalHeight, path: new URL(element.src).pathname }));
          check(logoState.complete && logoState.naturalWidth > 0 && logoState.naturalHeight > 0, `${route} ${theme} header logo did not load a decodable image at ${width}px`);
          check(logoState.path === (theme === 'dark' ? '/shruggietech-logo-dark.svg' : '/shruggietech-logo-light.svg'), `${route} ${theme} uses the wrong visible ShruggieTech lockup`);
        }
        const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
        for (const violation of results.violations) failures.push(`${route} in ${theme} at ${width}px fails ${violation.id}: ${violation.nodes.map((node) => `${node.target.join(' ')} (${node.failureSummary ?? 'no contrast detail'})`).join(', ')}`);
        const routeName = route === '/' ? 'home' : route.replace(/^\//, '').replace(/\/$/, '').replaceAll('/', '-');
        const filename = `${routeName}-${theme}-${width}.png`;
        await page.screenshot({ path: join(visualRoot, filename), fullPage: true });
      }
      check(themeSurfaces.get(`${route}:${width}:light`) !== themeSurfaces.get(`${route}:${width}:dark`), `${route} light and dark themes resolve to the same surface at ${width}px`);
    }
  }
  await page.setViewportSize({ width: 1280, height: 900 });
  for (const route of tableRoutes) { await page.goto(base + route); check(await page.locator('table').count() > 0, `${route} does not render its Markdown table semantically`); }
  await page.goto(base + '/');
  const primaryAction = page.locator('.hero .button.primary');
  const actionStyle = await primaryAction.evaluate((element) => { const style = getComputedStyle(element); const probe = document.createElement('i'); probe.style.backgroundColor = 'var(--brand-cta)'; document.body.append(probe); const result = { background: style.backgroundColor, cta: getComputedStyle(probe).backgroundColor, color: style.color, transitionDuration: style.transitionDuration }; probe.remove(); return result; });
  check(actionStyle.background === actionStyle.cta, `primary landing action does not use the generated CTA token (${JSON.stringify(actionStyle)})`);
  check(actionStyle.color === 'rgb(255, 255, 255)', 'primary landing action must use white text');
  check(Number.parseFloat(actionStyle.transitionDuration) >= 0.12 && Number.parseFloat(actionStyle.transitionDuration) <= 0.3, 'interactive motion must remain within the 120-300ms contract');
  for (const theme of visualThemes) {
    await page.evaluate((selectedTheme) => localStorage.setItem('theme', selectedTheme), theme);
    await page.reload({ waitUntil: 'networkidle' });
    const themedPrimary = page.locator('.hero .button.primary');
    await themedPrimary.hover();
    let contrast = await new AxeBuilder({ page }).include('.hero .button.primary').withRules(['color-contrast']).analyze();
    check(contrast.violations.length === 0, `primary landing action hover state fails WCAG contrast in ${theme} theme`);
    await page.mouse.move(0, 899);
    await themedPrimary.focus();
    contrast = await new AxeBuilder({ page }).include('.hero .button.primary').withRules(['color-contrast']).analyze();
    check(contrast.violations.length === 0, `primary landing action focus state fails WCAG contrast in ${theme} theme`);
  }
  const secondaryActionColor = await page.locator('.hero .button:not(.primary)').evaluate((element) => getComputedStyle(element).color);
  const primaryTokenColor = await page.evaluate(() => { const probe = document.createElement('i'); probe.style.color = 'var(--primary)'; document.body.append(probe); const color = getComputedStyle(probe).color; probe.remove(); return color; });
  check(secondaryActionColor === primaryTokenColor, `secondary landing action does not use the generated accessible green token (${secondaryActionColor} != ${primaryTokenColor})`);
  const textLink = page.locator('.hero .text-action');
  const linkBackground = await textLink.evaluate((element) => ({ image: getComputedStyle(element).backgroundImage, decoration: getComputedStyle(element).textDecorationLine, height: element.getBoundingClientRect().height, cue: element.querySelector('[aria-hidden="true"]')?.textContent }));
  check(linkBackground.image === 'none' && linkBackground.decoration === 'none' && linkBackground.height >= 44 && linkBackground.cue === '↓', `landing text action violates its semantic treatment (${JSON.stringify(linkBackground)})`);
  for (const selector of ['.hero .button', '.brand-card a', '.header-identity', '.site-footer a']) check(await page.locator(selector).first().evaluate((element) => getComputedStyle(element).textDecorationLine) === 'none', `${selector} inherits an ordinary-link underline`);
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await textLink.hover();
  const reducedStyle = await textLink.evaluate((element) => ({ duration: getComputedStyle(element).transitionDuration, decoration: getComputedStyle(element).textDecorationLine, reduced: matchMedia('(prefers-reduced-motion: reduce)').matches }));
  check(reducedStyle.reduced && Number.parseFloat(reducedStyle.duration) <= 0.001 && reducedStyle.decoration === 'none', `reduced-motion text action contract failed (${JSON.stringify(reducedStyle)})`);
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  await page.goto(base + '/');
  for (const action of await page.locator('.brand-card a').all()) { const box = await action.boundingBox(); check(Boolean(box && box.width >= 44 && box.height >= 44), 'portfolio action target is smaller than 44 by 44 CSS pixels'); }
  for (const file of [...requiredFiles, ...downloadFiles]) {
    const response = await page.request.get(base + file);
    check(response.ok(), `${file} is missing from the export`);
    if (!response.ok()) continue;
    const body = Buffer.from(await response.body());
    for (const failure of payloadFailures(file, response.headers()['content-type'], body)) failures.push(`${file} ${failure}`);
  }
  await verifyStableGeometry();
  const lockupContracts = new Map([['/shruggietech-logo-dark.svg', '#F2F5FA'], ['/shruggietech-logo-light.svg', '#0A0A0A']]);
  for (const [file, wordmarkFill] of lockupContracts) {
    const response = await page.request.get(base + file);
    check(response.ok(), `${file} cannot be fetched for lockup validation`);
    if (!response.ok()) continue;
    try {
      const text = await response.text();
      check(text.includes('<svg') && text.includes('<image') && text.includes('<path'), `${file} lacks the complete lockup payload`);
      check(new RegExp(`fill=["']${wordmarkFill}["']`, 'i').test(text), `${file} lacks its expected ${wordmarkFill} wordmark fill`);
      const references = [...text.matchAll(/(?:href|xlink:href)=["']([^"']+)/g)].map((match) => match[1]);
      check(references.length > 0 && references.every((reference) => reference.startsWith('data:') || reference.startsWith('#')), `${file} has an unresolved nested dependency`);
      const embedded = /href=["']data:image\/png;base64,([^"']+)/i.exec(text);
      check(Boolean(embedded), `${file} lacks its embedded colored mark`);
      if (embedded) {
        const info = pngInfo(Buffer.from(embedded[1], 'base64'));
        check(info.visible > 0 && info.artwork > 0 && info.chromatic > 0, `${file} embedded mark is empty or monochrome`);
      }
    } catch (error) { failures.push(`${file} lockup payload does not decode: ${error.message}`); }
  }
  const expectedPngs = new Map([['/favicon-16x16.png', 16], ['/favicon-32x32.png', 32], ['/apple-touch-icon.png', 180], ['/android-chrome-192x192.png', 192], ['/android-chrome-512x512.png', 512]]);
  for (const file of iconFiles) {
    const response = await page.request.get(base + file); check(response.ok(), `${file} cannot be fetched for icon validation`); if (!response.ok()) continue;
    const buffer = Buffer.from(await response.body());
    try {
      if (file.endsWith('.png')) { const info = pngInfo(buffer); const size = expectedPngs.get(file); check(info.width === size && info.height === size, `${file} is ${info.width}x${info.height}, expected ${size}x${size}`); check(info.srgb, `${file} lacks an sRGB declaration`); check(info.visible > 0, `${file} has no visible pixels`); check(hasVisibleArtwork(info), `${file} contains only its black background and no measurable ShruggieTech artwork`); check(info.opaque, `${file} must have an opaque platform background`); check(hasCanonicalBlackCorners(info), `${file} does not use canonical #000000 corner pixels`); }
      else if (file.endsWith('.ico')) { const entries = icoEntries(buffer); check(JSON.stringify(entries.map((entry) => entry.size)) === JSON.stringify([16, 24, 32, 48, 64, 128, 256]), `${file} lacks the required ICO entries`); for (const entry of entries) { const info = pngInfo(entry.payload); check(info.width === entry.size && info.height === entry.size, `${file} ${entry.size}px directory entry decodes as ${info.width}x${info.height}`); check(info.srgb, `${file} ${entry.size}px frame lacks an sRGB declaration`); check(info.opaque, `${file} ${entry.size}px frame must be opaque`); check(info.visible > 0, `${file} ${entry.size}px frame has no visible pixels`); check(hasCanonicalBlackCorners(info), `${file} ${entry.size}px frame does not use canonical #000000 corner pixels`); check(hasVisibleArtwork(info), `${file} ${entry.size}px frame contains only its black background and no measurable ShruggieTech artwork`); } }
      else if (file.endsWith('.svg')) { const text = buffer.toString('utf8'); check(text.includes('<svg') && text.includes('<image'), `${file} lacks SVG artwork`); check(/<rect[^>]+fill=["']#000000["']/i.test(text), `${file} does not declare the canonical #000000 background`); const references = [...text.matchAll(/(?:href|xlink:href)=["']([^"']+)/g)].map((match) => match[1]); check(references.every((reference) => reference.startsWith('data:') || reference.startsWith('#')), `${file} has an unresolved nested dependency`); }
    } catch (error) { failures.push(`${file} does not decode: ${error.message}`); }
  }
  const manifestResponse = await page.request.get(base + '/site.webmanifest');
  if (manifestResponse.ok()) {
    const manifest = await manifestResponse.json(); check(Array.isArray(manifest.icons) && manifest.icons.length >= 2, 'site.webmanifest lacks installable icons'); check(manifest.background_color === '#000000' && manifest.theme_color === '#000000', 'site.webmanifest must declare canonical #000000 background and theme colors');
    for (const icon of manifest.icons ?? []) { const match = /^(\d+)x(\d+)$/.exec(icon.sizes ?? ''); check(Boolean(match), `manifest icon ${icon.src} has an invalid size declaration`); if (!match) continue; const response = await page.request.get(new URL(icon.src, base).href); check(response.ok(), `manifest icon ${icon.src} is missing`); if (!response.ok()) continue; try { const info = pngInfo(Buffer.from(await response.body())); check(info.width === Number(match[1]) && info.height === Number(match[2]), `manifest icon ${icon.src} dimensions disagree with ${icon.sizes}`); check(info.srgb, `manifest icon ${icon.src} lacks an sRGB declaration`); check(info.opaque, `manifest icon ${icon.src} must be opaque`); check(hasCanonicalBlackCorners(info), `manifest icon ${icon.src} does not use canonical #000000 corner pixels`); check(hasVisibleArtwork(info), `manifest icon ${icon.src} contains only its black background and no measurable ShruggieTech artwork`); } catch (error) { failures.push(`manifest icon ${icon.src} does not decode: ${error.message}`); } }
  }
  for (const route of iconRoutes) {
    await page.goto(base + route); const icons = await page.locator('link[rel="icon"]').evaluateAll((links) => links.map((link) => new URL(link.href).pathname));
    check(['/favicon.svg', '/favicon.ico', '/favicon-32x32.png', '/favicon-16x16.png'].every((href) => icons.includes(href)), `${route} does not inherit the complete shared icon contract`);
    const apple = await page.locator('link[rel="apple-touch-icon"]').evaluateAll((links) => links.map((link) => new URL(link.href).pathname)); check(apple.includes('/apple-touch-icon.png'), `${route} lacks the Apple touch icon relationship`);
  }
} finally {
  await browser.close();
  server?.close();
}
if (failures.length) { console.error(failures.map((failure) => `FAIL ${failure}`).join('\n')); process.exit(1); }
console.log(`verified ${htmlRoutes.length} HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations`);
