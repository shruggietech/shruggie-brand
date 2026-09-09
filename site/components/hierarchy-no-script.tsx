import type { GuidelinePortal } from '@/lib/guidelines';
import { guidelineSections } from '@/lib/guidelines';
import { documentationTree } from '@/lib/documentation';

export function GuidelineNoScriptNav({ portal, currentPath }: { portal: GuidelinePortal; currentPath: string }) {
  return <noscript><nav className="hierarchy-noscript-nav" aria-label="Guideline topics"><ul>{guidelineSections(portal).map((section) => section.destination
    ? <li key={section.label}><a href={section.destination.path} aria-current={section.destination.path === currentPath ? 'page' : undefined}>{section.destination.label}</a></li>
    : <li key={section.label}><span>{section.label}</span><ul>{section.children?.map((topic) => <li key={topic.key}><a href={topic.path} aria-current={topic.path === currentPath ? 'page' : undefined}>{topic.label}</a></li>)}</ul></li>)}</ul></nav></noscript>;
}

export function DocumentationNoScriptNav({ currentPath }: { currentPath: string }) {
  const tree = documentationTree();
  return <noscript><nav className="hierarchy-noscript-nav" aria-label="Documentation pages"><ul>{tree.children.map((node) => node.type === 'page'
    ? <li key={node.url}><a href={node.url} aria-current={node.url === currentPath ? 'page' : undefined}>{node.name}</a></li>
    : node.type === 'folder' ? <li key={String(node.name)}><span>{node.name}</span><ul>{node.children.filter((child) => child.type === 'page').map((child) => child.type === 'page' ? <li key={child.url}><a href={child.url} aria-current={child.url === currentPath ? 'page' : undefined}>{child.name}</a></li> : null)}</ul></li> : null)}</ul></nav></noscript>;
}
