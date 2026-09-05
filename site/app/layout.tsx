import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import { RootProvider } from 'fumadocs-ui/provider/next';
import { siteDescription, siteUrl } from '@/lib/metadata';
import "./globals.css";

const geist = localFont({
  src: [
    { path: "../generated/fonts/Geist-Regular.woff2", weight: "400" },
    { path: "../generated/fonts/Geist-Medium.woff2", weight: "500" },
  ],
  variable: "--font-geist",
});

const spaceGrotesk = localFont({
  src: [
    { path: "../generated/fonts/SpaceGrotesk-Medium.woff2", weight: "500" },
    { path: "../generated/fonts/SpaceGrotesk-Bold.woff2", weight: "700" },
  ],
  variable: "--font-space-grotesk",
});

const geistMono = localFont({
  src: "../generated/fonts/GeistMono-Regular.woff2",
  weight: "400",
  variable: "--font-geist-mono",
});

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: { default: "Brands | ShruggieTech", template: "%s | ShruggieTech" },
  description: siteDescription,
  applicationName: 'ShruggieTech Brands',
  manifest: '/site.webmanifest',
  icons: { icon: [{ url: '/favicon.svg', type: 'image/svg+xml' }, { url: '/favicon.ico', type: 'image/x-icon' }, { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' }, { url: '/favicon-16x16.png', sizes: '16x16', type: 'image/png' }], apple: [{ url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' }] },
};

export const viewport: Viewport = { themeColor: '#080B0D' };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning className={`dark ${geist.variable} ${spaceGrotesk.variable} ${geistMono.variable}`}>
      <body>
        <a className="skip-link" href="#content">Skip to content</a>
        <RootProvider theme={{ defaultTheme: 'dark', enableSystem: false }} search={{ options: { type: 'static', api: '/static.json' } }}>{children}</RootProvider>
      </body>
    </html>
  );
}
