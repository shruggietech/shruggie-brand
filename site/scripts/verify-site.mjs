import { createReadStream, existsSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { extname, join, normalize, resolve } from 'node:path';
import { chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { htmlRoutes, requiredFiles, tableRoutes } from '../tests/site.test.mjs';

const root = resolve(import.meta.dirname, '..', 'out');
const types = { '.css': 'text/css', '.html': 'text/html', '.ico': 'image/x-icon', '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml', '.txt': 'text/plain', '.xml': 'application/xml', '.woff2': 'font/woff2' };
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
      check(await page.locator('meta[name="description"]').count() === 1, `${route} lacks a meta description`);
      check(await page.locator('link[rel="canonical"]').count() === 1, `${route} lacks a canonical URL`);
      check(await page.locator('meta[property="og:title"]').count() === 1, `${route} lacks Open Graph metadata`);
      check(await page.locator('meta[name="twitter:card"]').count() === 1, `${route} lacks Twitter card metadata`);
      check(await page.locator('link[rel="icon"]').count() >= 1, `${route} lacks a favicon`);
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
  for (const file of requiredFiles) { const response = await page.request.get(base + file); check(response.ok(), `${file} is missing from the export`); }
} finally {
  await browser.close();
  server.close();
}
if (failures.length) { console.error(failures.map((failure) => `FAIL ${failure}`).join('\n')); process.exit(1); }
console.log(`verified ${htmlRoutes.length} HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations`);
