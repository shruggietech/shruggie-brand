import type { InlineSegment, InstructionBlock, PortalResource } from '@/lib/guidelines';

export function InlineContent({ segments }: { segments: InlineSegment[] }) {
  return <>{segments.map((segment, index) => segment.type === 'code' ? <code key={index}>{segment.text}</code> : segment.type === 'link' ? <a href={segment.href} key={index}>{segment.text}</a> : <span key={index}>{segment.text}</span>)}</>;
}

export function InstructionBlocks({ blocks }: { blocks: InstructionBlock[] }) {
  return <>{blocks.map((block, index) => {
    if (block.type === 'heading') { const Heading = block.depth <= 2 ? 'h3' : 'h4'; return <Heading key={index}><InlineContent segments={block.segments} /></Heading>; }
    if (block.type === 'paragraph') return <p key={index}><InlineContent segments={block.segments} /></p>;
    if (block.type === 'list') { const List = block.ordered ? 'ol' : 'ul'; return <List key={index}>{block.items.map((item, itemIndex) => <li key={itemIndex}><InlineContent segments={item} /></li>)}</List>; }
    if (block.type === 'table') return <div className="guide-table-scroll" key={index} role="region" aria-label="Scrollable instruction table" tabIndex={0}><table><thead><tr>{block.headers.map((header) => <th key={header}>{header}</th>)}</tr></thead><tbody>{block.rows.map((row, rowIndex) => <tr key={rowIndex}>{row.map((cell, cellIndex) => <td key={cellIndex}><InlineContent segments={cell} /></td>)}</tr>)}</tbody></table></div>;
    return <pre key={index}><code data-language={block.language || undefined}>{block.text}</code></pre>;
  })}</>;
}

export function ResourceList({ resources }: { resources: PortalResource[] }) {
  return <section className="guide-section" aria-labelledby="resources"><h2 id="resources">Documents and containers</h2><p className="guide-lead">Manifests, source instructions, and platform containers are listed as resources, not image previews.</p><ul className="resource-list">{resources.map((resource) => <li key={resource.id} data-resource-format={resource.format}><span className="resource-type" aria-hidden="true">{resource.format.toUpperCase()}</span><span><strong>{resource.title}</strong><small>{resource.summary}</small></span><a data-kit-asset href={resource.url}>Download <span className="sr-only">{resource.title}</span></a></li>)}</ul></section>;
}
