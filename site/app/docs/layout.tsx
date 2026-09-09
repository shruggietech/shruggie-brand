import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import type { ReactNode } from 'react';
import { baseOptions } from '@/lib/layout.shared';
import { documentationTree } from '@/lib/documentation';

export default function Layout({ children }: { children: ReactNode }) { return <DocsLayout tree={documentationTree()} {...baseOptions({ includeDocsLink: false })}>{children}</DocsLayout>; }
