'use strict';

const assert = require('node:assert/strict');
const { createServer } = require('node:http');
const { once } = require('node:events');
const { readFileSync, existsSync, mkdtempSync, rmSync } = require('node:fs');
const { tmpdir } = require('node:os');
const path = require('node:path');
const { Writable } = require('node:stream');
const { pipeline } = require('node:stream/promises');
const { test } = require('node:test');
const client = require('./index.cjs');

async function fixture(handler, check) {
  const server = createServer(handler);
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  try {
    await check(`http://127.0.0.1:${server.address().port}`);
  } finally {
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
  }
}

test('each JSON request reaches the server and does not replay another response or cookie', async () => {
  let requests = 0;
  await fixture((request, response) => {
    assert.equal(request.headers.cookie, undefined);
    response.writeHead(200, { 'content-type': 'application/json', 'cache-control': 'public, max-age=3600', 'set-cookie': 'session=private' });
    response.end(JSON.stringify({ request: ++requests }));
  }, async base => {
    assert.deepEqual(await client(base).json(), { request: 1 });
    assert.deepEqual(await client(base).json(), { request: 2 });
  });
  assert.equal(requests, 2);
});

test('ZIP bytes and progress survive redirects and streaming pipeline backpressure', async () => {
  const bytes = Buffer.from('504b03040000000000000000', 'hex');
  await fixture((request, response) => {
    if (request.url === '/redirect') {
      response.writeHead(302, { location: '/archive' }).end();
    } else {
      response.writeHead(200, { 'content-length': bytes.length });
      response.end(bytes);
    }
  }, async base => {
    const received = [];
    const progress = [];
    const input = client.stream(`${base}/redirect`);
    input.on('downloadProgress', value => progress.push(value.percent));
    await pipeline(input, new Writable({ write(chunk, encoding, done) { received.push(chunk); setImmediate(done); } }));
    assert.deepEqual(Buffer.concat(received), bytes);
    assert.equal(progress.at(-1), 1);
  });
});

test('HTTP failures reject both APIs instead of writing error pages as ZIPs', async () => {
  await fixture((request, response) => response.writeHead(404).end('missing'), async base => {
    await assert.rejects(client(base).json(), /HTTP 404/);
    await assert.rejects(pipeline(client.stream(base), new Writable({ write(chunk, encoding, done) { done(); } })), /HTTP 404/);
  });
});

test('a truncated response fails the download pipeline', async () => {
  await fixture((request, response) => {
    response.writeHead(200, { 'content-length': 1000 });
    response.flushHeaders();
    response.write('short');
    setImmediate(() => response.destroy());
  }, async base => {
    await assert.rejects(pipeline(client.stream(base), new Writable({ write(chunk, encoding, done) { done(); } })));
  });
});

test('destroying the download stream cancels its pending request', { timeout: 5000 }, async () => {
  let acceptClose;
  const connectionClosed = new Promise(resolve => { acceptClose = resolve; });
  await fixture((request, response) => {
    response.once('close', acceptClose);
    response.writeHead(200);
    response.flushHeaders();
    response.write('first');
  }, async base => {
    const input = client.stream(base);
    const closed = once(input, 'close');
    await once(input, 'data');
    input.destroy();
    await closed;
    await connectionClosed;
    assert.equal(input.destroyed, true);
  });
});

test('pinned wp-env resolves the replacement and no vulnerable cache package remains', () => {
  const installed = path.dirname(require.resolve('@wordpress/env/package.json'));
  assert.equal(JSON.parse(readFileSync(path.join(installed, 'package.json'), 'utf8')).version, '11.16.0');
  const resolved = require.resolve('got', { paths: [installed] });
  assert.equal(require(resolved), client);
  assert.equal(existsSync(path.join(__dirname, '..', 'node_modules', 'http-cache-semantics')), false);
  assert.equal(existsSync(path.join(__dirname, '..', 'node_modules', 'cacheable-request')), false);
});

test('the installed wp-env downloads and extracts a ZIP through the replacement', async () => {
  const installed = path.dirname(require.resolve('@wordpress/env/package.json'));
  const { downloadZipSource } = require(path.join(installed, 'lib', 'download-sources.js'));
  const AdmZip = require('adm-zip');
  const zip = new AdmZip();
  zip.addFile('source/README.txt', Buffer.from('fresh fixture bytes'));
  const bytes = zip.toBuffer();
  const temporary = mkdtempSync(path.join(tmpdir(), 'stbb-fetch-'));
  try {
    await fixture((request, response) => response.writeHead(200, { 'content-length': bytes.length }).end(bytes), async base => {
      const destination = path.join(temporary, 'source');
      const progress = [];
      await downloadZipSource({ url: base, path: destination }, {
        onProgress: value => progress.push(value), spinner: {}, debug: false,
      });
      assert.equal(readFileSync(path.join(destination, 'README.txt'), 'utf8'), 'fresh fixture bytes');
      assert.equal(progress[0], 0);
      assert.equal(progress.at(-1), 1);
      assert.equal(existsSync(`${destination}.zip`), false);
    });
  } finally {
    assert.ok(path.resolve(temporary).startsWith(`${path.resolve(tmpdir())}${path.sep}`));
    rmSync(temporary, { recursive: true, force: true });
  }
});
