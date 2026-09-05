import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';

export function baseOptions({ includeDocsLink = true }: { includeDocsLink?: boolean } = {}): BaseLayoutProps {
  const links: NonNullable<BaseLayoutProps['links']> = [
    { text: 'Portfolio', url: '/#portfolio' },
    ...(includeDocsLink ? [{ text: 'How we build brands', url: '/docs' }] : []),
    { text: 'Download the skill', url: 'https://github.com/ShruggieTech/shruggie-brand/releases/latest', external: true },
    { text: 'GitHub', url: 'https://github.com/ShruggieTech/shruggie-brand', external: true },
  ];
  return {
    nav: { title: <span className="header-identity"><img src="/shruggietech-logo-dark.svg" alt="ShruggieTech" className="header-logo header-logo-dark" /><img src="/shruggietech-logo-light.svg" alt="ShruggieTech" className="header-logo header-logo-light" /></span> },
    links,
  };
}
