import { createReadStream, existsSync, mkdirSync, rmSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { extname, join, normalize, resolve } from 'node:path';
import { chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { inflateSync } from 'node:zlib';
import { downloadFiles, htmlRoutes, iconFiles, iconRoutes, requiredFiles, routeRecords, tableRoutes, visualRoutes, visualThemes, visualWidths } from '../tests/site.test.mjs';
import { payloadFailures } from './payload-contract.mjs';
import { isCanonicalRedirect, selectVerificationOrigin } from './verification-origin.mjs';

const root = resolve(import.meta.dirname, '..', 'out');
const visualRoot = resolve(import.meta.dirname, '..', 'test-results', 'visual');
rmSync(visualRoot, { recursive: true, force: true });
mkdirSync(visualRoot, { recursive: true });
const routeByPath = new Map(routeRecords.map((route) => [route.pathname, route]));
const types = { '.css': 'text/css', '.html': 'text/html', '.ico': 'image/x-icon', '.json': 'application/json', '.pdf': 'application/pdf', '.png': 'image/png', '.svg': 'image/svg+xml', '.txt': 'text/plain', '.webmanifest': 'application/manifest+json', '.xml': 'application/xml', '.woff2': 'font/woff2' };
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
  const raw = inflateSync(Buffer.concat(compressed)); const stride = width * 4; let cursor = 0; let previous = Buffer.alloc(stride); let minAlpha = 255; let visible = 0; let artwork = 0; const corners = [];
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
    for (let i = 3; i < stride; i += 4) { minAlpha = Math.min(minAlpha, row[i]); if (row[i] > 0) visible += 1; if (row[i] > 0 && (row[i - 3] !== 0 || row[i - 2] !== 0 || row[i - 1] !== 0)) artwork += 1; }
    if (y === 0 || y === height - 1) for (const x of [0, width - 1]) corners.push([...row.subarray(x * 4, x * 4 + 4)]);
    previous = row;
  }
  return { width, height, opaque: minAlpha === 255, srgb, visible, artwork, corners };
}
function icoEntries(buffer) {
  if (buffer.length < 6 || !buffer.subarray(0, 4).equals(Buffer.from([0, 0, 1, 0]))) throw new Error('invalid ICO signature');
  const count = buffer.readUInt16LE(4); if (buffer.length < 6 + count * 16) throw new Error('truncated ICO directory'); const entries = [];
  for (let index = 0; index < count; index += 1) { const offset = 6 + index * 16; const width = buffer[offset] || 256; const height = buffer[offset + 1] || 256; const length = buffer.readUInt32LE(offset + 8); const start = buffer.readUInt32LE(offset + 12); if (width !== height || start + length > buffer.length) throw new Error(`invalid ICO entry ${index}`); entries.push({ size: width, payload: buffer.subarray(start, start + length) }); }
  return entries;
}
const hasCanonicalBlackCorners = (info) => info.corners.length === 4 && info.corners.every((pixel) => JSON.stringify(pixel) === JSON.stringify([0, 0, 0, 255]));
const hasVisibleArtwork = (info) => info.artwork >= Math.max(1, Math.ceil(info.width * info.height * 0.005));
const browser = await chromium.launch({ headless: true });
try {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, permissions: ['clipboard-read', 'clipboard-write'] });
  const page = await context.newPage();
  await page.goto(base + '/');
  check(await page.locator('h1').textContent() === 'We build comprehensive brands', 'homepage headline does not match the approved wording');
  check(await page.locator('.brand-card').count() === 5, 'homepage must show exactly the five production brand cards');
  check(await page.locator('.brand-icon img').count() === 5, 'every brand card must include an icon');
  const homeText = (await page.locator('body').innerText()).toLowerCase();
  for (const rejected of ['a shruggietech project', 'skill 1.', 'canon', 'example brand', 'read the system']) check(!homeText.includes(rejected), `homepage contains retired wording: ${rejected}`);
  const visibleHeaderLinks = async () => page.locator('a').evaluateAll((links) => links.filter((link) => { const rect = link.getBoundingClientRect(); return ['Documentation', 'Download the Skill', 'View on GitHub', 'Portfolio'].includes(link.textContent?.trim()) && rect.bottom > 0 && rect.top < window.innerHeight && rect.right > 0 && rect.left < window.innerWidth; }).map((link) => ({ text: link.textContent?.trim(), href: new URL(link.href).pathname })));
  const desktopLinks = await visibleHeaderLinks();
  check(JSON.stringify(desktopLinks) === JSON.stringify([{ text: 'Documentation', href: '/docs/' }]), `desktop landing navigation must expose only Documentation (${JSON.stringify(desktopLinks)})`);
  await page.setViewportSize({ width: 360, height: 900 });
  await page.getByRole('button', { name: 'Toggle Menu' }).click();
  const mobileLinks = await visibleHeaderLinks();
  check(JSON.stringify(mobileLinks) === JSON.stringify([{ text: 'Documentation', href: '/docs/' }, { text: 'Download the Skill', href: '/ShruggieTech/shruggie-brand/releases/latest' }, { text: 'View on GitHub', href: '/ShruggieTech/shruggie-brand' }]), `mobile landing menu must expose the three approved destinations in order (${JSON.stringify(mobileLinks)})`);
  for (const link of await page.getByRole('link').filter({ hasText: /^(Documentation|Download the Skill|View on GitHub)$/ }).all()) { const box = await link.boundingBox(); if (box && box.y < 900) check(box.width >= 44 && box.height >= 44, `${await link.textContent()} mobile navigation target is smaller than 44 by 44 CSS pixels`); }
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
      const publicText = await page.locator('body').innerText();
      for (const rejected of ['How we build brands', 'How we build', 'The ShruggieTech Variance Contract']) check(!publicText.includes(rejected), `${route} contains retired public wording: ${rejected}`);
      if (contract.kind === 'docs-index' || contract.kind === 'docs-page') check(await page.locator('header a').filter({ hasText: /^Documentation$/ }).count() <= 1, `${route} repeats the documentation root in navigation at ${width}px`);
      if (route === '/shruggietech/guidelines/') {
        check(!(await page.locator('body').innerText()).toLowerCase().includes('a shruggietech project'), `${route} contains a self-endorsement`);
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
  await page.goto(base + '/docs/04-toolchain/');
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
    const resting = await paginationCard.evaluate((element) => { const style = getComputedStyle(element); return { borderColor: style.borderColor, titleColor: getComputedStyle(element.querySelector('p')).color, bodyColor: getComputedStyle(document.body).color }; });
    check(resting.borderColor !== 'rgb(229, 231, 235)' && resting.titleColor !== resting.bodyColor, 'documentation pagination card lacks a persistent resting affordance');
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
        const logo = page.locator('.header-logo:visible').first();
        const logoBox = await logo.boundingBox();
        check(Boolean(logoBox && logoBox.width >= 100 && logoBox.height >= 24), `${route} ${theme} header logo is not legible at ${width}px`);
        const logoPath = await logo.evaluate((element) => new URL(element.src).pathname);
        check(logoPath === (theme === 'dark' ? '/shruggietech-logo-dark.svg' : '/shruggietech-logo-light.svg'), `${route} ${theme} uses the wrong visible ShruggieTech lockup`);
        const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
        for (const violation of results.violations) failures.push(`${route} in ${theme} at ${width}px fails ${violation.id}: ${violation.nodes.map((node) => `${node.target.join(' ')} (${node.failureSummary ?? 'no contrast detail'})`).join(', ')}`);
        const routeName = route === '/' ? 'home' : route === '/docs/' ? 'docs-index' : 'docs-variance-contract';
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
  const textLink = page.locator('.hero .text-link');
  const linkBackground = await textLink.evaluate((element) => ({ image: getComputedStyle(element).backgroundImage, size: getComputedStyle(element).backgroundSize, duration: getComputedStyle(element).transitionDuration }));
  check(linkBackground.image !== 'none' && linkBackground.size.startsWith('0px') && Number.parseFloat(linkBackground.duration) >= 0.12 && Number.parseFloat(linkBackground.duration) <= 0.3, `landing text link lacks its animated underline treatment (${JSON.stringify(linkBackground)})`);
  for (const selector of ['.hero .button', '.brand-card', '.header-identity']) check(!['0px 2px', '100% 2px'].includes(await page.locator(selector).first().evaluate((element) => getComputedStyle(element).backgroundSize)), `${selector} incorrectly inherits the ordinary-link underline`);
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await textLink.hover();
  const reducedStyle = await textLink.evaluate((element) => ({ duration: getComputedStyle(element).transitionDuration, size: getComputedStyle(element).backgroundSize, reduced: matchMedia('(prefers-reduced-motion: reduce)').matches }));
  check(reducedStyle.reduced && Number.parseFloat(reducedStyle.duration) <= 0.001 && !reducedStyle.size.startsWith('0px'), `reduced-motion mode does not preserve a static underline without animation (${JSON.stringify(reducedStyle)})`);
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  for (const card of await page.locator('.brand-card').all()) { const box = await card.boundingBox(); check(Boolean(box && box.width >= 44 && box.height >= 44), 'portfolio card target is smaller than 44 by 44 CSS pixels'); }
  for (const file of [...requiredFiles, ...downloadFiles]) {
    const response = await page.request.get(base + file);
    check(response.ok(), `${file} is missing from the export`);
    if (!response.ok()) continue;
    const body = Buffer.from(await response.body());
    for (const failure of payloadFailures(file, response.headers()['content-type'], body)) failures.push(`${file} ${failure}`);
  }
  const expectedPngs = new Map([['/favicon-16x16.png', 16], ['/favicon-32x32.png', 32], ['/apple-touch-icon.png', 180], ['/android-chrome-192x192.png', 192], ['/android-chrome-512x512.png', 512]]);
  for (const file of iconFiles) {
    const response = await page.request.get(base + file); check(response.ok(), `${file} cannot be fetched for icon validation`); if (!response.ok()) continue;
    const buffer = Buffer.from(await response.body());
    try {
      if (file.endsWith('.png')) { const info = pngInfo(buffer); const size = expectedPngs.get(file); check(info.width === size && info.height === size, `${file} is ${info.width}x${info.height}, expected ${size}x${size}`); check(info.srgb, `${file} lacks an sRGB declaration`); check(info.visible > 0, `${file} has no visible pixels`); check(hasVisibleArtwork(info), `${file} contains only its black background and no measurable ShruggieTech artwork`); check(info.opaque, `${file} must have an opaque platform background`); check(hasCanonicalBlackCorners(info), `${file} does not use canonical #000000 corner pixels`); }
      else if (file.endsWith('.ico')) { const entries = icoEntries(buffer); check(JSON.stringify(entries.map((entry) => entry.size)) === JSON.stringify([16, 24, 32, 48, 64, 128, 256]), `${file} lacks the required ICO entries`); for (const entry of entries) { const info = pngInfo(entry.payload); check(hasCanonicalBlackCorners(info), `${file} ${entry.size}px frame does not use canonical #000000 corner pixels`); check(hasVisibleArtwork(info), `${file} ${entry.size}px frame contains only its black background and no measurable ShruggieTech artwork`); } }
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
