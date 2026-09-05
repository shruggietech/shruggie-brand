import Link from 'next/link';

export function Footer() {
  return <footer className="site-footer"><div><span className="footer-identity"><img src="/shruggietech-logo-dark.svg" alt="ShruggieTech" className="footer-logo footer-logo-dark" /><img src="/shruggietech-logo-light.svg" alt="ShruggieTech" className="footer-logo footer-logo-light" /></span><p>Building distinct brands with systems that keep them useful.</p></div><nav aria-label="Footer navigation"><Link href="/">Brands</Link><Link href="/docs">How we build</Link><a href="https://github.com/ShruggieTech/shruggie-brand/releases/latest">Download the skill</a><a href="https://shruggie.tech/">Company</a><a href="https://github.com/ShruggieTech/shruggie-brand">Source</a><a href="https://github.com/ShruggieTech/shruggie-brand/blob/main/LICENSE">License</a></nav></footer>;
}
