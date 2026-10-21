'use strict';
const assert = require('node:assert/strict');
const { createRequire } = require('node:module');
const { test } = require('node:test');
const wpRequire = createRequire(require.resolve('@wordpress/env/package.json'));
const gitRequire = createRequire(wpRequire.resolve('simple-git'));
const parser = gitRequire('@simple-git/argv-parser');
const yaml = wpRequire('js-yaml');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

test('wp-env CommonJS factory clones into an empty directory with the patched implementation', async t => {
  const SimpleGit = wpRequire('simple-git');
  assert.equal(typeof SimpleGit, 'function');
  const temporaryRoot = fs.realpathSync(os.tmpdir());
  const temporary = fs.mkdtempSync(path.join(temporaryRoot, 'wp-env-git-'));
  t.after(() => {
    assert.equal(path.dirname(fs.realpathSync(temporary)), temporaryRoot);
    assert.match(path.basename(temporary), /^wp-env-git-/);
    fs.rmSync(temporary, { recursive: true, force: true });
  });
  const source = path.join(temporary, 'source');
  const target = path.join(temporary, 'target');
  fs.mkdirSync(source);
  const environment = { ...process.env, GIT_TERMINAL_PROMPT: '0' };
  for (const name of ['EDITOR', 'VISUAL', 'GIT_EDITOR', 'GIT_SEQUENCE_EDITOR']) delete environment[name];
  await SimpleGit(source).env(environment).init();
  const git = SimpleGit({ progress() {} }).env(environment);
  await git.clone(source, target, { '--depth': '1', '--no-checkout': null });
  assert.equal(await git.cwd(target).checkIsRepo('root'), true);
});

test('the installed Git parser classifies VISUAL as an unsafe editor in every casing', async () => {
  for (const name of ['VISUAL', 'visual', 'Visual']) {
    const findings = parser.vulnerabilityCheck(['commit', '--amend'], { [name]: 'fixture-editor' });
    assert.ok(findings.some(item => item.category === 'allowUnsafeEditor'));
    await assert.rejects(wpRequire('simple-git')().env({ [name]: 'fixture-editor' }).raw('status'), /not permitted/);
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
