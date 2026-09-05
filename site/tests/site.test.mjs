import brands from '../generated/brands.json' with { type: 'json' };
import meta from '../generated/docs/meta.json' with { type: 'json' };

export const brandRoutes = brands.flatMap((brand) => [`/${brand.slug}/`, `/${brand.slug}/downloads/`]);
export const docRoutes = meta.pages.map((page) => page === 'index' ? '/docs/' : `/docs/${page}/`);
export const tableRoutes = ['00-variance-contract', '02-kit-anatomy', '04-toolchain', '05-shadcn-binding', '06-logo-protocol', '07-voice', '08-glyph-construction', '09-portability'].map((slug) => `/docs/${slug}/`);
export const htmlRoutes = ['/', ...brandRoutes, ...docRoutes];
export const requiredFiles = ['/favicon.svg', '/favicon-16x16.png', '/favicon-32x32.png', '/apple-touch-icon.png', '/android-chrome-192x192.png', '/android-chrome-512x512.png', '/site.webmanifest', '/social-preview.png', '/robots.txt', '/sitemap.xml', '/static.json'];
