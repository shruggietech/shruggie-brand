# WordPress fixture HTTP transport

The pinned `@wordpress/env` 11.16.0 uses two HTTP-client entry points: `got(url).json()` for the WordPress stable-version response and `got.stream(url)` with a progress event for ZIP downloads. This fixture overrides its `got` dependency with a local, dependency-free compatibility transport using Node's built-in `fetch` and streams. It performs uncached requests and removes `got`, `cacheable-request` and `http-cache-semantics` from the installed dependency graph. This addresses the unpatched GHSA-ch52-4w7c-c8xp dependency without suppressing the required npm audit.

The transport supports redirects, JSON, byte streams, progress, HTTP error propagation, truncated-stream errors, cancellation and a two-minute request timeout. It does not implement got's broader API. The fixture pins wp-env and tests its resolution to this transport; an upstream runner upgrade must review the compatibility surface. This is test infrastructure only and is not bundled into brand kits or consumer applications.

Run `npm ci --ignore-scripts`, `npm test`, and `npm audit --audit-level=moderate` from `scripts/wordpress-runtime/`, then exercise both pinned WordPress/PHP pairs through `scripts/test_wordpress_runtime.py`.
