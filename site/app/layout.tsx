import type { Metadata } from "next";
import localFont from "next/font/local";
import Link from "next/link";
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
  title: { default: "Shruggie Brand", template: "%s | Shruggie Brand" },
  description: "Verified brand kits, implementation guidance, and installable registries for ShruggieTech projects.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`dark ${geist.variable} ${spaceGrotesk.variable} ${geistMono.variable}`}>
      <body>
        <a className="skip-link" href="#content">Skip to content</a>
        <header className="site-header">
          <Link className="site-name" href="/">Shruggie Brand</Link>
          <nav aria-label="Primary navigation">
            <Link href="/docs/">Documentation</Link>
            <a href="https://github.com/ShruggieTech/shruggie-brand">GitHub</a>
          </nav>
        </header>
        <main id="content">{children}</main>
        <footer>
          <span>A ShruggieTech project</span>
          <span>Skill 1.1.2 · Canon 1.1.2</span>
        </footer>
      </body>
    </html>
  );
}
