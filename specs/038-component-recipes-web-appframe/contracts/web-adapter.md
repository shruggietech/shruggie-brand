# Contract: Web and React Adapter

## Framework-neutral entry points

- `tokens/interface.css` exposes stable `--bb-*` semantic custom properties without React or Tailwind.
- `web/components.css` uses only the public semantic namespace, environment inputs, system forced colors, and documented structural constants.
- `web/component-recipes.json`, `app-frame-hosts.json`, `support-matrix.json`, and `adapter.json` provide machine-readable authority and packaging evidence.

## React entry points

- `web/react/server.tsx` exports structural AppFrame markup, Button, IconButton, Field, FormControls, ListRow, SplitPane structure, StatusBadge, Card, and EmptyState without a client directive or browser-global import access.
- `web/react/client.tsx` begins with `use client` and exports the environment bridge plus Radix-backed Toolbar, Tabs, Menu, Dialog, and Toast behavior and interactive SplitPane behavior.
- `web/react/index.ts` documents direct server and client imports and does not erase the client boundary.

React is a peer dependency. The exact Radix aggregate package is a declared dependency for the client entry. Tailwind, Next.js, Vite, Tauri, and Wails are not runtime dependencies.

## AppFrame handoff

Every responsibility resolves to one owner. Host-owned values arrive through documented `--bb-host-*` properties or region data. AppFrame-owned values use browser environment inputs and normalized props. Radix portals target the AppFrame overlay root. A host cannot also ask AppFrame to consume the same inset.

## Verification

The generated specimen exercises semantic tokens, all states, Tab and arrow-key paths, Escape dismissal, focus return, announcements, target sizes, resize, safe areas, titlebar avoidance, IME obstruction, reduced motion, forced colors, and scaled text. Python validates contracts and deterministic source; TypeScript checks server/client packaging; Playwright and axe validate browser behavior. Support records distinguish real engine execution from simulated host configurations.
