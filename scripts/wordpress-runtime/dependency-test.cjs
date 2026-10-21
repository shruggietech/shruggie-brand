'use strict';
const assert = require('node:assert/strict');
const { createRequire } = require('node:module');
const { test } = require('node:test');
const wpRequire = createRequire(require.resolve('@wordpress/env/package.json'));
const gitRequire = createRequire(wpRequire.resolve('simple-git'));
const parser = gitRequire('@simple-git/argv-parser');
const yaml = wpRequire('js-yaml');

test('the installed Git parser classifies VISUAL as an unsafe editor in every casing', () => {
  for (const name of ['VISUAL', 'visual', 'Visual']) {
    const findings = parser.vulnerabilityCheck(['commit', '--amend'], { [name]: 'fixture-editor' });
    assert.ok(findings.some(item => item.category === 'allowUnsafeEditor'));
  }
});

test('the installed YAML dumper preserves the Docker Compose mapping shapes used by wp-env', () => {
  const compose = { services: { wordpress: { image: 'wordpress:php8.2', ports: ['18889:80'], volumes: ['A:/fixture:/var/www/html/wp-content/stbb-fixture'], environment: { WORDPRESS_DEBUG: '1', EMPTY: '' } } } };
  assert.deepEqual(yaml.load(yaml.dump(compose)), compose);
});

test('empty YAML merge sources consume the configured merge budget', () => {
  const input = 'empty: &empty {}\nmerged:\n  <<: [' + Array(20).fill('*empty').join(', ') + ']\n';
  assert.throws(() => yaml.load(input, { maxTotalMergeKeys: 2 }));
});
