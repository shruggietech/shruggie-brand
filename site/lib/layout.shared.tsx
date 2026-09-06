import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';

export function baseOptions({ includeDocsLink = true }: { includeDocsLink?: boolean } = {}): BaseLayoutProps {
  const links: NonNullable<BaseLayoutProps['links']> = [
    ...(includeDocsLink ? [{ text: 'Documentation', url: '/docs' }] : []),
    { text: 'Download the Skill', url: 'https://github.com/ShruggieTech/shruggie-brand/releases/latest', external: true, on: 'menu' },
    { text: 'View on GitHub', url: 'https://github.com/ShruggieTech/shruggie-brand', external: true, on: 'menu' },
  ];
  return {
    nav: { title: <span className="header-identity"><img src="/shruggietech-logo-dark.svg" alt="ShruggieTech" className="header-logo header-logo-dark" /><img src="/shruggietech-logo-light.svg" alt="ShruggieTech" className="header-logo header-logo-light" /></span> },
    links,
  };
}
