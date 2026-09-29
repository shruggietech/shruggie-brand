'use client';

import publication from '@/generated/publication.json';
import { ThemeSwitch, type ThemeSwitchProps } from 'fumadocs-ui/layouts/shared/slots/theme-switch';
import { releaseBadge } from '@/lib/documentation-sidebar-publication.mjs';

export function DocumentationSidebarTheme({ className, ...props }: ThemeSwitchProps) {
  const badge = releaseBadge(publication);
  return <>
    {badge && <a className="docs-manual-version" href={badge.href} aria-label={`${badge.label} official release`}>{badge.label}</a>}
    <ThemeSwitch {...props} className={`${className ?? ''} ${badge ? 'docs-manual-theme' : 'docs-manual-theme-only'}`} />
  </>;
}
