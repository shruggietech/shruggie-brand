import type { GuidelinePortal, GuidelineTopic } from '@/lib/guidelines';
import { AssetLibrary } from './asset-library';
import { ColorReference } from './color-reference';
import { InlineContent, InstructionBlocks } from './resource-list';
import { GuidelineOverview } from './overview-content';

function Items({ values, empty }: { values?: string[]; empty: string }) { return values?.length ? <ul>{values.map((value) => <li key={value}>{value}</li>)}</ul> : <p>{empty}</p>; }

function Voice({ portal }: { portal: GuidelinePortal }) { const value = portal.content.voice; return <><section className="guide-section"><h2 id="governing-principle">Governing principle</h2><p className="guide-lead">{value.principle}</p><p>Use this principle to review headlines, product copy, and instructions before applying a particular tone.</p></section><section className="guide-section"><h2 id="voice-qualities">Voice qualities</h2><div className="guide-columns"><div><h3>Qualities</h3><Items values={value.qualities} empty="Use the governing principle as the current voice guide." /></div><div><h3>Lead with</h3><Items values={value.lead_with} empty="Choose an opening that serves the reader's immediate task." /></div><div><h3>Avoid</h3><Items values={value.avoid} empty="No additional brand-specific avoidance examples are listed." /></div></div></section><section className="guide-section"><h2 id="personality">Personality</h2><div className="personality-list">{value.personality?.map((row) => <article key={row[0]}><h3>{row[0]}</h3><p>{row[1]}</p><small>Avoid: {row[2]}</small></article>)}</div></section></>; }
function Logos({ portal }: { portal: GuidelinePortal }) { const value = portal.content.logos; const logoFamily = portal.asset_families.find((family) => family.key === 'logos'); return <><section className="guide-section"><h2 id="usage">Usage</h2><p>{value.guidance}</p><p>A brand mark is the symbol alone; wide and stacked lockups are distinct approved combinations. Choose artwork for the intended viewing surface and size. <a href="/docs/asset-glossary/">Read the asset language</a> for detail, ink, and background terms.</p>{logoFamily?.assets.slice(0, 3).map((asset) => <figure className={`logo-example ${asset.surface}-well`} key={asset.id}><div className="asset-preview-media"><img src={asset.preview.url} alt={`${asset.title} example`} /></div><figcaption>{asset.title}</figcaption></figure>)}</section><section className="guide-section"><h2 id="minimum-sizes">Minimum sizes</h2><p>Use these rendered-size limits when choosing a logo form. The Assets page offers exact files and size variants.</p><dl className="metric-list">{Object.entries(value.minimum_sizes || {}).map(([name, size]) => <div key={name}><dt>{name}</dt><dd>{size} px</dd></div>)}</dl>{value.reduced_below_px && <p>Use the reduced mark below {value.reduced_below_px} px.</p>}</section><section className="guide-section"><h2 id="prohibitions">Prohibitions</h2><Items values={value.prohibitions} empty="No additional brand-specific prohibitions are declared here. Preserve the approved artwork and minimum sizes." /></section></>; }
function Typography({ portal }: { portal: GuidelinePortal }) { const families = portal.content.typography.families || {}; return <section className="guide-section"><h2 id="type-families">Type families</h2><p>Use each family for its declared role and only the delivered weights. The downloaded kit contains the local font files and exact binding instructions.</p><div className="type-list">{Object.entries(families).map(([role, family]) => <article key={role}><span>{role}</span><h3>{family.name}</h3><p>Delivered weights: {family.weights.join(', ')}</p></article>)}</div></section>; }
function Components({ portal }: { portal: GuidelinePortal }) { return <section className="guide-section"><h2 id="domain-components">Domain components</h2><p>These are brand-specific content examples and the fields they need. Match their behavior and states to the delivered component recipes; this list is not an installed UI library.</p><div className="component-list">{Object.entries(portal.content.components).map(([name, fields]) => <article key={name}><h3>{name}</h3><p>Content and state fields:</p><ul>{fields.map((field) => <li key={field}><code>{field.replaceAll('_', ' ')}</code></li>)}</ul></article>)}</div><p><a href="/docs/11-interface-implementation/">Read the interface implementation guide</a> to select a supported host adapter.</p></section>; }
function Integration({ portal }: { portal: GuidelinePortal }) { return portal.instructions.length ? <>{portal.instructions.map((instruction, index) => <section className="guide-section instruction-section" id={`instruction-${index + 1}`} key={instruction.source_path}><p className="guide-eyebrow">{instruction.platform.replaceAll('-', ' ')}</p><InstructionBlocks blocks={instruction.blocks} /><p>Use the source instructions with this brand&apos;s exact downloaded kit and versioned bindings.</p><a className="guide-source-download" href={instruction.source_url}>Download {instruction.platform.replaceAll('-', ' ')} source instructions</a></section>)}</> : <section className="guide-section"><h2 id="platform-instructions">Platform instructions</h2><p>This kit has no brand-specific platform instructions. Use the delivered consumer contract and the <a href="/docs/11-interface-implementation/">shared integration guide</a> for supported adapters.</p></section>; }
function Expressions({ portal }: { portal: GuidelinePortal }) {
  const assets = portal.asset_families.find((family) => family.key === 'expressions')?.assets ?? [];
  return <>
    <p className="guide-lead">Approved non-core treatments for selected settings. These do not replace core logo masters.</p>
    {assets.map((asset) => {
      const delivery = asset.deliveries[0];
      if (!delivery) throw new Error(`Missing governed expression delivery: ${asset.id}`);
      return <section className="guide-section" id={asset.id} key={asset.id}>
        <h2>{asset.title}</h2>
        <figure className={`expression-preview ${asset.preview_well ?? asset.surface}-well`}>
          <img src={asset.preview.url} alt={asset.accessibility?.alt ?? asset.title} />
          <figcaption>{asset.summary}</figcaption>
        </figure>
        <dl className="expression-details">
          <div><dt>Role</dt><dd>{asset.role.replaceAll('-', ' ')}</dd></div>
          <div><dt>Use</dt><dd>{asset.usage?.use}</dd></div>
          <div><dt>Avoid</dt><dd>{asset.usage?.avoid}</dd></div>
          <div><dt>Legibility</dt><dd>{asset.accessibility?.legibility}</dd></div>
          <div><dt>Text overlay</dt><dd>{asset.accessibility?.text_overlay}</dd></div>
          <div><dt>Motion</dt><dd>{asset.accessibility?.reduced_motion}</dd></div>
          <div><dt>Disclosure</dt><dd>{asset.accessibility?.disclosure}</dd></div>
          <div><dt>Credit</dt><dd>{asset.credit?.attribution}</dd></div>
          <div><dt>License</dt><dd>{asset.credit?.license}</dd></div>
        </dl>
        <a className="guide-source-download" href={delivery.url}>Download supplied source</a>
      </section>;
    })}
  </>;
}

export function TopicContent({ portal, topic }: { portal: GuidelinePortal; topic: GuidelineTopic }) {
  if (topic.key === 'overview') return <GuidelineOverview portal={portal} />;
  if (topic.key === 'voice') return <Voice portal={portal} />;
  if (topic.key === 'logos') return <Logos portal={portal} />;
  if (topic.key === 'color') return <ColorReference palettes={portal.palettes} roles={portal.color_roles} />;
  if (topic.key === 'typography') return <Typography portal={portal} />;
  if (topic.key === 'components') return <Components portal={portal} />;
  if (topic.key === 'expressions') return <Expressions portal={portal} />;
  if (topic.key === 'assets') return <AssetLibrary portal={portal} />;
  return <Integration portal={portal} />;
}
