import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';

export function baseOptions(): BaseLayoutProps {
  return {
    nav: { title: <img src="/shruggietech-logo.svg" alt="ShruggieTech" className="header-logo" /> },
    links: [
      { text: 'Portfolio', url: '/#portfolio' },
      { text: 'How we build brands', url: '/docs' },
      { text: 'Download the skill', url: 'https://github.com/ShruggieTech/shruggie-brand/releases/latest', external: true },
      { text: 'GitHub', url: 'https://github.com/ShruggieTech/shruggie-brand', external: true },
    ],
  };
}
