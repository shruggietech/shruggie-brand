import { createReadStream, existsSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { extname, join, normalize, resolve } from 'node:path';
import { chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { inflateSync } from 'node:zlib';
import { downloadFiles, htmlRoutes, iconFiles, iconRoutes, requiredFiles, tableRoutes } from '../tests/site.test.mjs';

const root = resolve(import.meta.dirname, '..', 'out');
const types = { '.css': 'text/css', '.html': 'text/html', '.ico': 'image/x-icon', '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml', '.txt': 'text/plain', '.webmanifest': 'application/manifest+json', '.xml': 'application/xml', '.woff2': 'font/woff2' };
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
const server = createServer((request, response) => {
  try {
    const path = diskPath(request.url ?? '/');
    if (!existsSync(path) || !statSync(path).isFile()) { response.writeHead(404).end('not found'); return; }
    response.writeHead(200, { 'content-type': types[extname(path)] ?? 'application/octet-stream' });
    createReadStream(path).pipe(response);
  } catch { response.writeHead(400).end('bad request'); }
});
await new Promise((accept) => server.listen(0, '127.0.0.1', accept));
const address = server.address();
const base = `http://127.0.0.1:${address.port}`;
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
  const raw = inflateSync(Buffer.concat(compressed)); const stride = width * 4; let cursor = 0; let previous = Buffer.alloc(stride); let minAlpha = 255; let visible = 0;
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
    for (let i = 3; i < stride; i += 4) { minAlpha = Math.min(minAlpha, row[i]); if (row[i] > 0) visible += 1; }
    previous = row;
  }
  return { width, height, opaque: minAlpha === 255, srgb, visible };
}
function icoSizes(buffer) {
  if (buffer.length < 6 || !buffer.subarray(0, 4).equals(Buffer.from([0, 0, 1, 0]))) throw new Error('invalid ICO signature');
  const count = buffer.readUInt16LE(4); if (buffer.length < 6 + count * 16) throw new Error('truncated ICO directory'); const sizes = [];
  for (let index = 0; index < count; index += 1) { const offset = 6 + index * 16; const width = buffer[offset] || 256; const height = buffer[offset + 1] || 256; const length = buffer.readUInt32LE(offset + 8); const start = buffer.readUInt32LE(offset + 12); if (width !== height || start + length > buffer.length) throw new Error(`invalid ICO entry ${index}`); sizes.push(width); }
  return sizes;
}
const browser = await chromium.launch({ headless: true });
try {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await context.newPage();
  await page.goto(base + '/');
  check(await page.locator('h1').textContent() === 'We build comprehensive brands', 'homepage headline does not match the approved wording');
  check(await page.locator('.brand-card').count() === 5, 'homepage must show exactly the five production brand cards');
  check(await page.locator('.brand-icon img').count() === 5, 'every brand card must include an icon');
  const homeText = (await page.locator('body').innerText()).toLowerCase();
  for (const rejected of ['a shruggietech project', 'skill 1.', 'canon', 'example brand', 'read the system']) check(!homeText.includes(rejected), `homepage contains retired wording: ${rejected}`);
  for (const route of htmlRoutes) {
    for (const width of [360, 1280]) {
      await page.setViewportSize({ width, height: 900 });
      const response = await page.goto(base + route);
      check(response?.status() === 200, `${route} returned ${response?.status()}`);
      check((await page.title()).endsWith('| ShruggieTech'), `${route} lacks a company-aligned page title`);
      check(await page.locator('meta[name="description"]').count() === 1, `${route} lacks a meta description`);
      check(await page.locator('link[rel="canonical"]').count() === 1, `${route} lacks a canonical URL`);
      check(await page.locator('meta[property="og:title"]').count() === 1, `${route} lacks Open Graph metadata`);
      check(await page.locator('meta[name="twitter:card"]').count() === 1, `${route} lacks Twitter card metadata`);
      check(await page.locator('link[rel="icon"]').count() >= 1, `${route} lacks a favicon`);
      if (route === '/shruggietech/guidelines/') {
        check(!(await page.locator('body').innerText()).toLowerCase().includes('a shruggietech project'), `${route} contains a self-endorsement`);
      }
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      if (overflow > 1) {
        const offenders = await page.evaluate(() => [...document.querySelectorAll('*')].filter((element) => element.getBoundingClientRect().right > document.documentElement.clientWidth + 1).slice(0, 5).map((element) => `${element.tagName}.${element.className}`));
        failures.push(`${route} overflows horizontally at ${width}px by ${overflow}px (${offenders.join(', ')})`);
      }
      const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
      for (const violation of results.violations) failures.push(`${route} at ${width}px fails ${violation.id}: ${violation.nodes.map((node) => node.target.join(' ')).join(', ')}`);
    }
  }
  await page.setViewportSize({ width: 1280, height: 900 });
  for (const route of tableRoutes) { await page.goto(base + route); check(await page.locator('table').count() > 0, `${route} does not render its Markdown table semantically`); }
  await page.goto(base + '/');
  for (const card of await page.locator('.brand-card').all()) { const box = await card.boundingBox(); check(Boolean(box && box.width >= 44 && box.height >= 44), 'portfolio card target is smaller than 44 by 44 CSS pixels'); }
  for (const file of [...requiredFiles, ...downloadFiles]) { const response = await page.request.get(base + file); check(response.ok(), `${file} is missing from the export`); }
  const expectedPngs = new Map([['/favicon-16x16.png', 16], ['/favicon-32x32.png', 32], ['/apple-touch-icon.png', 180], ['/android-chrome-192x192.png', 192], ['/android-chrome-512x512.png', 512]]);
  for (const file of iconFiles) {
    const response = await page.request.get(base + file); check(response.ok(), `${file} cannot be fetched for icon validation`); if (!response.ok()) continue;
    const buffer = Buffer.from(await response.body());
    try {
      if (file.endsWith('.png')) { const info = pngInfo(buffer); const size = expectedPngs.get(file); check(info.width === size && info.height === size, `${file} is ${info.width}x${info.height}, expected ${size}x${size}`); check(info.srgb, `${file} lacks an sRGB declaration`); check(info.visible > 0, `${file} has no visible pixels`); if (file.includes('apple-touch') || file.includes('android-chrome')) check(info.opaque, `${file} must have an opaque platform background`); }
      else if (file.endsWith('.ico')) check(JSON.stringify(icoSizes(buffer)) === JSON.stringify([16, 24, 32, 48, 64, 128, 256]), `${file} lacks the required ICO entries`);
      else if (file.endsWith('.svg')) { const text = buffer.toString('utf8'); check(text.includes('<svg') && text.includes('<image'), `${file} lacks SVG artwork`); const references = [...text.matchAll(/(?:href|xlink:href)=["']([^"']+)/g)].map((match) => match[1]); check(references.every((reference) => reference.startsWith('data:') || reference.startsWith('#')), `${file} has an unresolved nested dependency`); }
    } catch (error) { failures.push(`${file} does not decode: ${error.message}`); }
  }
  const manifestResponse = await page.request.get(base + '/site.webmanifest');
  if (manifestResponse.ok()) {
    const manifest = await manifestResponse.json(); check(Array.isArray(manifest.icons) && manifest.icons.length >= 2, 'site.webmanifest lacks installable icons');
    for (const icon of manifest.icons ?? []) { const match = /^(\d+)x(\d+)$/.exec(icon.sizes ?? ''); check(Boolean(match), `manifest icon ${icon.src} has an invalid size declaration`); if (!match) continue; const response = await page.request.get(new URL(icon.src, base).href); check(response.ok(), `manifest icon ${icon.src} is missing`); if (!response.ok()) continue; try { const info = pngInfo(Buffer.from(await response.body())); check(info.width === Number(match[1]) && info.height === Number(match[2]), `manifest icon ${icon.src} dimensions disagree with ${icon.sizes}`); check(info.srgb, `manifest icon ${icon.src} lacks an sRGB declaration`); check(info.opaque, `manifest icon ${icon.src} must be opaque`); } catch (error) { failures.push(`manifest icon ${icon.src} does not decode: ${error.message}`); } }
  }
  for (const route of iconRoutes) {
    await page.goto(base + route); const icons = await page.locator('link[rel="icon"]').evaluateAll((links) => links.map((link) => new URL(link.href).pathname));
    check(['/favicon.svg', '/favicon.ico', '/favicon-32x32.png', '/favicon-16x16.png'].every((href) => icons.includes(href)), `${route} does not inherit the complete shared icon contract`);
    const apple = await page.locator('link[rel="apple-touch-icon"]').evaluateAll((links) => links.map((link) => new URL(link.href).pathname)); check(apple.includes('/apple-touch-icon.png'), `${route} lacks the Apple touch icon relationship`);
  }
} finally {
  await browser.close();
  server.close();
}
if (failures.length) { console.error(failures.map((failure) => `FAIL ${failure}`).join('\n')); process.exit(1); }
console.log(`verified ${htmlRoutes.length} HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations`);
