'use strict';
// wp-env 11 expects a callable CommonJS export from the patched upstream implementation.
const upstream = require('simple-git-upstream');

function simpleGit(base, options) {
  const initial = typeof base === 'string' ? { baseDir: base } : (base || {});
  const settings = { ...initial, ...options };
  settings.allowEnvironment = [...(settings.allowEnvironment || []), 'GIT_TERMINAL_PROMPT'];
  return upstream.simpleGit(settings);
}

module.exports = Object.assign(simpleGit, upstream, { simpleGit });
