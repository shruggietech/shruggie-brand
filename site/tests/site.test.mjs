import brands from '../generated/brands.json' with { type: 'json' };
import routeContract from '../generated/routes.json' with { type: 'json' };

export const routeRecords = routeContract.routes;
export const brandRoutes = routeRecords.filter((route) => ['brand', 'downloads', 'guidelines'].includes(route.kind)).map((route) => route.pathname);
export const docRoutes = routeRecords.filter((route) => ['docs-index', 'docs-page'].includes(route.kind)).map((route) => route.pathname);
export const tableRoutes = ['00-variance-contract', '02-kit-anatomy', '04-toolchain', '05-shadcn-binding', '06-logo-protocol', '07-voice', '08-glyph-construction', '09-portability'].map((slug) => `/docs/${slug}/`);
export const htmlRoutes = routeRecords.map((route) => route.pathname);
export const visualRoutes = ['/docs/', '/docs/04-toolchain/'];
export const visualThemes = ['light', 'dark'];
export const visualWidths = [360, 1280];
export const requiredFiles = ['/favicon.svg', '/favicon.ico', '/favicon-16x16.png', '/favicon-32x32.png', '/apple-touch-icon.png', '/android-chrome-192x192.png', '/android-chrome-512x512.png', '/site.webmanifest', '/robots.txt', '/sitemap.xml', '/static.json', ...routeRecords.map((route) => route.social.path)];
export const iconFiles = ['/favicon.svg', '/favicon.ico', '/favicon-16x16.png', '/favicon-32x32.png', '/apple-touch-icon.png', '/android-chrome-192x192.png', '/android-chrome-512x512.png'];
export const iconRoutes = ['/', '/docs/', '/docs/04-toolchain/'];
export const downloadFiles = brands.flatMap((brand) => { const root = `/${brand.slug}/downloads/files`; return [`${root}/${brand.slug}-brand-guide.pdf`, `${root}/logos/svg/${brand.slug}-mark-color.svg`, `${root}/logos/svg/${brand.slug}-horizontal-color.svg`, `${root}/icons/manifest.json`, `${root}/icons/web/favicon.ico`, `${root}/icons/android/manifest.json`, `${root}/icons/apple/ios/manifest.json`, `${root}/icons/apple/macos/manifest.json`, `${root}/icons/windows/manifest.json`, `${root}/icons/windows/classic/app.ico`, brand.specimen, `/${brand.slug}/brand/r/theme.json`]; });
