import portals from '@/generated/guidelines.json';
import type { Root } from 'fumadocs-core/page-tree';
import type { TOCItemType } from 'fumadocs-core/toc';

export type InlineSegment = { type: 'text' | 'code' | 'link'; text: string; href?: string };
export type InstructionBlock =
  | { type: 'heading'; depth: number; segments: InlineSegment[] }
  | { type: 'paragraph'; segments: InlineSegment[] }
  | { type: 'list'; ordered: boolean; items: InlineSegment[][] }
  | { type: 'table'; headers: string[]; rows: InlineSegment[][][] }
  | { type: 'code'; language: string; text: string };
export type ColorEntry = { token: string; role: string; hex: string; rgb: string; hsl: string; oklch: string; lab: string; print: string; aliases: string[] };
export type Delivery = { path: string; url: string; format: string; role?: string; platform?: string; appearance?: string; source_variant?: string; destination?: string; width?: number | null; height?: number | null; embedded_sizes?: number[]; sha256?: string };
export type PortalAsset = { id: string; title: string; role: string; platform: string; appearance: string; surface: 'light' | 'dark'; summary: string; formats: string[]; variants: string[]; preview: Delivery; deliveries: Delivery[] };
export type AssetFamily = { key: string; title: string; summary: string; assets: PortalAsset[] };
export type PortalResource = Delivery & { id: string; title: string; resource_kind: string; summary: string };
export type GuidelineTopic = { key: string; title: string; description: string };
export type GuidelinePortal = {
  schema_version: string;
  brand: { slug: string; title: string; descriptor: string; idea: string; affiliation: string };
  topics: GuidelineTopic[];
  content: {
    overview: { foundation_title?: string; foundation?: string; promises?: string[]; in_scope?: string[]; out_of_scope?: string[]; sharp_edge?: string };
    voice: { principle?: string; qualities?: string[]; lead_with?: string[]; avoid?: string[]; personality?: string[][] };
    logos: { guidance?: string; minimum_sizes?: Record<string, number>; reduced_below_px?: number | null; prohibitions?: string[] };
    typography: { mode?: string; families?: Record<string, { name: string; weights: number[] }> };
    components: Record<string, string[]>;
  };
  palettes: { dark: ColorEntry[]; light: ColorEntry[] };
  asset_families: AssetFamily[];
  resources: PortalResource[];
  instructions: { key: string; title: string; platform: string; source_path: string; source_url: string; blocks: InstructionBlock[] }[];
  portable_guide: string;
};

export const guidelinePortals = portals as unknown as GuidelinePortal[];

export function guidelineBySlug(slug: string) { return guidelinePortals.find((portal) => portal.brand.slug === slug); }

export function guidelineTopic(portal: GuidelinePortal, segments?: string[]) {
  if (!segments?.length) return portal.topics[0];
  if (segments.length !== 1) return undefined;
  return portal.topics.find((topic) => topic.key === segments[0]);
}

export function guidelinePath(slug: string, topic: string) { return topic === 'overview' ? `/${slug}/guidelines/` : `/${slug}/guidelines/${topic}/`; }

export function guidelineTree(portal: GuidelinePortal): Root {
  return {
    type: 'root',
    name: `${portal.brand.title} guidelines`,
    children: portal.topics.map((topic) => ({ type: 'page', name: topic.title, url: guidelinePath(portal.brand.slug, topic.key) })),
  };
}

export function topicToc(portal: GuidelinePortal, topic: GuidelineTopic): TOCItemType[] {
  if (topic.key === 'color') return [{ title: 'Dark palette', url: '#dark-palette', depth: 2 }, { title: 'Light palette', url: '#light-palette', depth: 2 }];
  if (topic.key === 'assets') return [...portal.asset_families.map((family) => ({ title: family.title, url: `#${family.key}`, depth: 2 })), { title: 'Documents and containers', url: '#resources', depth: 2 }];
  if (topic.key === 'integration') return portal.instructions.map((instruction, index) => ({ title: `${instruction.platform}: ${instruction.title}`, url: `#instruction-${index + 1}`, depth: 2 }));
  const sections: Record<string, string[]> = { overview: ['Foundations', 'Promises', 'Boundaries'], voice: ['Governing principle', 'Voice qualities', 'Personality'], logos: ['Usage', 'Minimum sizes', 'Prohibitions'], typography: ['Type families'], components: ['Domain components'] };
  return (sections[topic.key] ?? []).map((title) => ({ title, url: `#${title.toLowerCase().replaceAll(' ', '-')}`, depth: 2 }));
}
