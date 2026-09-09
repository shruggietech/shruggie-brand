import records from '@/generated/documentation.json';
import type { Root } from 'fumadocs-core/page-tree';

export type DocumentationRecord = {
  slug: string;
  title: string;
  description: string;
  navigation: { section: string; sectionOrder: number; label: string; order: number; path: string };
};

export const documentationRecords = records as DocumentationRecord[];

export function documentationTree(): Root {
  const groups = new Map<string, DocumentationRecord[]>();
  for (const record of [...documentationRecords].sort((left, right) => left.navigation.sectionOrder - right.navigation.sectionOrder || left.navigation.order - right.navigation.order)) {
    const group = groups.get(record.navigation.section) ?? [];
    group.push(record);
    groups.set(record.navigation.section, group);
  }
  return {
    type: 'root',
    name: 'Documentation',
    children: [...groups.entries()].map(([label, pages]) => pages.length === 1 && pages[0].navigation.label === label
      ? { type: 'page' as const, name: pages[0].navigation.label, url: pages[0].navigation.path }
      : { type: 'folder' as const, name: label, defaultOpen: true, collapsible: true, children: pages.map((page) => ({ type: 'page' as const, name: page.navigation.label, url: page.navigation.path })) }),
  };
}
