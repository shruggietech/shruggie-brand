'use strict';

const { Readable } = require('node:stream');

// This fixture replaces got, rather than patching or retaining its cache chain.
// Keep this surface limited to the two APIs used by pinned @wordpress/env.
async function responseFor(url, signal) {
  const response = await fetch(url, {
    cache: 'no-store',
    signal: signal ? AbortSignal.any([signal, AbortSignal.timeout(120_000)]) : AbortSignal.timeout(120_000),
  });
  if (!response.ok) {
    await response.body?.cancel();
    throw new Error(`Download failed with HTTP ${response.status}: ${url}`);
  }
  return response;
}

function request(url) {
  return {
    async json() {
      return (await responseFor(url)).json();
    },
  };
}

request.stream = function stream(url) {
  const controller = new AbortController();
  let output;
  output = Readable.from((async function* download() {
    const response = await responseFor(url, controller.signal);
    const total = Number(response.headers.get('content-length')) || 0;
    let received = 0;
    const body = response.body;
    if (body) {
      for await (const chunk of body) {
        received += chunk.length;
        output.emit('downloadProgress', { percent: total ? Math.min(received / total, 1) : 0 });
        yield Buffer.from(chunk);
      }
    }
    output.emit('downloadProgress', { percent: 1 });
  })(), { objectMode: false });
  const destroy = output.destroy;
  output.destroy = function cancel(error) {
    controller.abort();
    return destroy.call(this, error);
  };
  return output;
};

module.exports = request;
