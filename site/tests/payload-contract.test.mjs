import assert from 'node:assert/strict';
import test from 'node:test';

import { payloadFailures } from '../scripts/payload-contract.mjs';

const png = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10, 1]);
const ico = Buffer.alloc(23);
ico.set([0, 0, 1, 0, 1, 0, 1, 1], 0);
ico.writeUInt32LE(1, 14);
ico.writeUInt32LE(22, 18);
ico[22] = 1;
const zip = Buffer.concat([Buffer.from([80, 75, 3, 4]), Buffer.alloc(18), Buffer.from([80, 75, 5, 6]), Buffer.alloc(18)]);

test('accepts valid supported payload types and content types', () => {
  const cases = [
    ['/guide.pdf', 'application/pdf', Buffer.from('%PDF-1.4\nbody\n%%EOF\n')],
    ['/preview.png', 'image/png', png],
    ['/favicon.ico', 'image/vnd.microsoft.icon', ico],
    ['/logo.svg', 'image/svg+xml', Buffer.from('<svg xmlns="http://www.w3.org/2000/svg"></svg>')],
    ['/registry.json', 'application/json; charset=utf-8', Buffer.from('{"name":"brand"}')],
    ['/consumer-handoff.json', 'application/json; charset=utf-8', Buffer.from('{"brand":"cueson","sha256":"abc"}')],
    ['/site.webmanifest', 'application/manifest+json; charset=utf-8', Buffer.from('{"icons":[]}')],
    ['/sitemap.xml', 'application/xml', Buffer.from('<?xml version="1.0"?><urlset></urlset>')],
    ['/robots.txt', 'text/plain; charset=utf-8', Buffer.from('User-agent: *\nSitemap: https://example.test/sitemap.xml\n')],
    ['/kit.zip', 'application/zip', zip],
  ];

  for (const [path, type, body] of cases) {
    assert.deepEqual(payloadFailures(path, type, body), [], path);
  }
});

test('rejects empty bodies and HTML error documents', () => {
  assert.match(payloadFailures('/guide.pdf', 'application/pdf', Buffer.alloc(0)).join('\n'), /body is empty/);
  const failures = payloadFailures('/guide.pdf', 'text/html; charset=utf-8', Buffer.from('<html>Error</html>'));
  assert.match(failures.join('\n'), /content type/);
  assert.match(failures.join('\n'), /PDF signature/);
});

test('rejects malformed structured and binary payloads', () => {
  assert.match(payloadFailures('/registry.json', 'application/json', Buffer.from('{')).join('\n'), /valid JSON/);
  assert.match(payloadFailures('/registry.json', 'application/json', Buffer.from('[]')).join('\n'), /JSON object/);
  assert.match(payloadFailures('/site.webmanifest', 'application/manifest+json', Buffer.from('[]')).join('\n'), /JSON object/);
  assert.match(payloadFailures('/sitemap.xml', 'application/xml', Buffer.from('<html></html>')).join('\n'), /XML urlset/);
  assert.match(payloadFailures('/logo.svg', 'image/svg+xml', Buffer.from('<html></html>')).join('\n'), /SVG document/);
  assert.match(payloadFailures('/preview.png', 'image/png', Buffer.from('not png')).join('\n'), /PNG signature/);
  assert.match(payloadFailures('/favicon.ico', 'image/vnd.microsoft.icon', Buffer.from('not ico')).join('\n'), /ICO signature/);
  assert.match(payloadFailures('/kit.zip', 'application/zip', Buffer.from('not zip')).join('\n'), /ZIP signature/);
});

test('rejects unsupported file types', () => {
  assert.deepEqual(payloadFailures('/download.bin', 'application/octet-stream', Buffer.from('data')), ['has unsupported payload type']);
});
