import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import type { ReactNode } from 'react';
import { baseOptions } from '@/lib/layout.shared';
import { documentationTree } from '@/lib/documentation';
import { DocumentationSidebarTheme } from '@/components/documentation-sidebar-theme';

export default function Layout({ children }: { children: ReactNode }) { return <DocsLayout tree={documentationTree()} {...baseOptions({ includeDocsLink: false })} slots={{ themeSwitch: DocumentationSidebarTheme }}>{children}</DocsLayout>; }
