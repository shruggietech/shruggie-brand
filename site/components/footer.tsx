import Link from 'next/link';

const footerLinks = [
  { label: 'Documentation', href: '/docs', kind: 'internal' },
  { label: 'Download Skill', href: 'https://github.com/ShruggieTech/shruggie-brand/releases/latest', kind: 'new-tab' },
  { label: 'Company', href: 'https://shruggie.tech/', kind: 'same-tab' },
  { label: 'Source', href: 'https://github.com/ShruggieTech/shruggie-brand', kind: 'new-tab' },
  { label: 'License', href: 'https://github.com/ShruggieTech/shruggie-brand/blob/main/LICENSE', kind: 'new-tab' },
] as const;

export function Footer() {
  return <footer className="site-footer"><div><span className="footer-identity"><img src="/shruggietech-logo-dark.svg" alt="ShruggieTech" className="footer-logo footer-logo-dark" /><img src="/shruggietech-logo-light.svg" alt="ShruggieTech" className="footer-logo footer-logo-light" /></span><p>Building distinct brands with systems that keep them useful.</p></div><nav aria-label="Footer navigation">{footerLinks.map((link) => link.kind === 'internal' ? <Link href={link.href} key={link.label}>{link.label}</Link> : <a href={link.href} target={link.kind === 'new-tab' ? '_blank' : undefined} rel={link.kind === 'new-tab' ? 'noopener noreferrer' : undefined} key={link.label}>{link.label}</a>)}</nav></footer>;
}
