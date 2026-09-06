import assert from 'node:assert/strict';
import test from 'node:test';

import { isCanonicalRedirect, selectVerificationOrigin } from '../scripts/verification-origin.mjs';

test('uses the local verifier when no remote origin is supplied', () => {
  assert.deepEqual(selectVerificationOrigin(undefined), { kind: 'local', base: null });
  assert.deepEqual(selectVerificationOrigin('  '), { kind: 'local', base: null });
});

test('accepts only the exact production HTTPS origin', () => {
  assert.deepEqual(selectVerificationOrigin('https://brand.shruggie.tech'), {
    kind: 'remote',
    base: 'https://brand.shruggie.tech',
  });
  assert.deepEqual(selectVerificationOrigin('https://brand.shruggie.tech/'), {
    kind: 'remote',
    base: 'https://brand.shruggie.tech',
  });
});

test('rejects an insecure production origin', () => {
  assert.throws(
    () => selectVerificationOrigin('http://brand.shruggie.tech'),
    /must use HTTPS/,
  );
});

test('rejects unexpected hosts and non-origin URL components', () => {
  for (const candidate of [
    'https://shruggie.tech',
    'https://brand.shruggie.tech.example.com',
    'https://brand.shruggie.tech:8443',
    'https://brand.shruggie.tech/docs/',
    'https://brand.shruggie.tech/?preview=true',
    'https://brand.shruggie.tech/#preview',
    'https://user:password@brand.shruggie.tech',
  ]) {
    assert.throws(() => selectVerificationOrigin(candidate), /exactly https:\/\/brand\.shruggie\.tech/);
  }
});

test('rejects malformed origins with a clear error', () => {
  assert.throws(() => selectVerificationOrigin('not a URL'), /valid absolute URL/);
});

test('accepts safe permanent redirects from local serving and GitHub Pages', () => {
  assert.equal(isCanonicalRedirect(308, '/docs/', 'http://127.0.0.1:4000', '/docs'), true);
  assert.equal(isCanonicalRedirect(301, 'https://brand.shruggie.tech/docs/', 'https://brand.shruggie.tech', '/docs'), true);
});

test('rejects temporary, cross-origin, and incorrect canonical redirects', () => {
  assert.equal(isCanonicalRedirect(302, '/docs/', 'https://brand.shruggie.tech', '/docs'), false);
  assert.equal(isCanonicalRedirect(301, 'https://example.com/docs/', 'https://brand.shruggie.tech', '/docs'), false);
  assert.equal(isCanonicalRedirect(301, '/docs/other/', 'https://brand.shruggie.tech', '/docs'), false);
  assert.equal(isCanonicalRedirect(301, null, 'https://brand.shruggie.tech', '/docs'), false);
});
