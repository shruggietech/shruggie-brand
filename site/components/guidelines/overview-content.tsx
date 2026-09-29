import type { GuidelinePortal } from '@/lib/guidelines';

const versionLabels: Record<string, string> = {
  brand_version: 'Brand identity',
  canon_version: 'Shared brand system',
  interface_canon_version: 'Interface rules',
  component_recipe_version: 'Component recipes',
  web_react_adapter_version: 'Web and React adapter',
  egui_adapter_version: 'egui adapter',
  compiler_version: 'BrandBuilder',
};

const bindingLabels: Record<string, string> = {
  interface_canon: 'Default interface rules',
  component_recipes: 'Component recipes',
  web_adapter: 'Web and React adapter',
  web_support_matrix: 'Web support coverage',
  egui_adapter: 'egui adapter',
  egui_support_matrix: 'egui support coverage',
};

export function GuidelineOverview({ portal }: { portal: GuidelinePortal }) {
  const essentials = portal.essentials;
  const contract = portal.implementation;
  const slug = portal.brand.slug;
  const overrides = Object.entries(contract.rules.overrides);
  const house = contract.rules.inheritance === 'shruggietech-house';
  const words = Object.entries(essentials.approved_words);
  const strategy = Object.entries(essentials.strategy);
  const roleLabels: Record<string, string> = { slogan: 'Slogan', short_description: 'Short description', long_description: 'Long description', introductory_statement: 'Introduction', positioning: 'Positioning', mission: 'Mission', vision: 'Vision', values: 'Values', brand_promise: 'Brand promise' };
  const sourceAssets = portal.asset_families.filter((family) => ['logos', 'marks', 'social', 'web'].includes(family.key)).map((family) => ({ family, asset: family.assets[0] })).filter((entry) => entry.asset);

  return <>
    <section className="guide-section" aria-labelledby="name-and-relationship">
      <h2 id="name-and-relationship">Name and relationship</h2>
      <p><strong>Approved name:</strong> {essentials.name}</p>
      {essentials.relationship && <p><strong>Relationship:</strong> {essentials.relationship}</p>}
      {essentials.written_form && <p><strong>Written form:</strong> {essentials.written_form}</p>}
      {essentials.name_story.map((value) => <p key={value}>{value}</p>)}
    </section>
    {words.length > 0 && <section className="guide-section" aria-labelledby="approved-words">
      <h2 id="approved-words">Approved words</h2>
      <dl>{words.map(([role, value]) => <div key={role} data-message-role={role.replaceAll('_', '-')}><dt>{roleLabels[role]}</dt><dd>{value}</dd></div>)}</dl>
    </section>}
    <section className="guide-section" aria-labelledby="visual-signatures">
      <h2 id="visual-signatures">Visual signatures</h2>
      {essentials.mark_guidance && <p><strong>Mark:</strong> {essentials.mark_guidance}</p>}
      {essentials.palette_guidance && <p><strong>Color:</strong> {essentials.palette_guidance}</p>}
      {portal.color_roles?.identity.length ? <ul>{portal.color_roles.identity.map((color) => <li key={color.id}>{color.label}: <code>{color.hex}</code></li>)}</ul> : null}
      <p><strong>Type:</strong> Display {essentials.type_families.display}; body {essentials.type_families.body}; mono {essentials.type_families.mono}. See <a href={`/${slug}/guidelines/logo/`}>Logo</a>, <a href={`/${slug}/guidelines/color/`}>Color</a>, and <a href={`/${slug}/guidelines/typography/`}>Typography</a> for detailed rules.</p>
    </section>
    <section className="guide-section" aria-labelledby="where-each-asset-belongs">
      <h2 id="where-each-asset-belongs">Where each asset belongs</h2>
      <p>Choose the delivered artwork for its declared surface, role, and size. The <a href={`/${slug}/guidelines/assets/#asset-library`}>asset library</a> contains every verified variant.</p>
      <ul>{sourceAssets.map(({ family, asset }) => <li key={family.key}><strong>{family.title}:</strong> <a href={asset.preview.url}>{asset.title}</a> ({asset.preview.destination}).</li>)}</ul>
      {essentials.reduced_below_px != null && <p>The reduced mark takes over at and below {essentials.reduced_below_px} px.</p>}
    </section>
    <section className="guide-section" aria-labelledby="usage-limits">
      <h2 id="usage-limits">Usage limits</h2>
      <p>Keep the delivered artwork geometry unchanged. The <a href={`/${slug}/guidelines/logo/`}>Logo</a> page has the complete mark rules.</p>
      {essentials.usage_limits.length > 0 && <ul>{essentials.usage_limits.map((value) => <li key={value}>{value}</li>)}</ul>}
      {essentials.visual_boundary && <p>{essentials.visual_boundary}</p>}
    </section>
    {strategy.length > 0 && <section className="guide-section" aria-labelledby="brand-strategy">
      <h2 id="brand-strategy">Brand strategy</h2>
      <dl>{strategy.map(([role, value]) => <div key={role} data-message-role={role.replaceAll('_', '-')}><dt>{roleLabels[role]}</dt><dd>{value}</dd></div>)}</dl>
    </section>}
    <section className="guide-section contract-summary" aria-labelledby="implementation-authority">
      <h2 id="implementation-authority">Implementation authority</h2>
      <p>An interface is the controls, layout, and feedback a person uses. {house ? 'This brand starts with shared ShruggieTech interface rules while keeping its own approved identity and any declared overrides.' : 'This brand uses its own delivered interface rules and approved identity. Its palette is independent of ShruggieTech house styling.'}</p>
      {portal.brand.affiliation && <p><strong>Relationship:</strong> {portal.brand.affiliation}</p>}
      <p>For the current published kit, inspect the <a href={`/${slug}/facts/documentation.json`}>public documentation facts (JSON)</a>. Example query: <code>GET /{slug}/facts/documentation.json</code>. The file declares schema version {contract.schema_version} and documentation contract version {contract.documentation_contract_version}. A downloaded kit keeps its own pinned facts at <code>{contract.bundled.facts_path}</code>.</p>
      <h3>Interface overrides</h3>
      {overrides.length ? <><p>Each entry changes one interface role for this brand. The default references come from the delivered interface rules; the effective reference is declared in <code>brand.json</code>. Use the dark or light default for the surface you are implementing, then apply this brand&apos;s effective reference to the named role. The change does not replace the whole interface or brand identity.</p><dl className="metric-list">{overrides.map(([name, effective]) => { const defaults = contract.rules.default_references[name]; return <div key={name}><dt><code>{name}</code></dt><dd><span>Dark default: <code>{defaults.dark}</code></span><span>Light default: <code>{defaults.light}</code></span><span>Default source: <code>{defaults.source}</code></span><span>Effective reference: <code>{effective}</code></span></dd></div>; })}</dl></> : <p>No brand-specific interface overrides are declared. The delivered interface rules supply the default values for controls, layout, and feedback.</p>}
    </section>
    <section className="guide-section contract-summary" aria-labelledby="versions-and-bindings">
      <h2 id="versions-and-bindings">Versions and bindings</h2>
      <p>These version domains move independently. Match each integration to the exact files in the downloaded kit.</p>
      <dl className="metric-list">{Object.entries(contract.versions).map(([name, version]) => <div key={name}><dt>{versionLabels[name] || name.replaceAll('_', ' ')}</dt><dd><code>{version}</code></dd></div>)}</dl>
      <h3>Implementation files</h3>
      <ul>{Object.entries(contract.bindings).map(([name, path]) => <li key={name}><strong>{bindingLabels[name] || name.replaceAll('_', ' ')}:</strong> <code>{path}</code></li>)}</ul>
      <p>The <a href={contract.hosted.manual_path}>BrandBuilder system manual</a> explains the shared architecture. The downloaded kit governs its pinned implementation bytes.</p>
    </section>
    <section className="guide-section" aria-labelledby="get-the-kit">
      <h2 id="get-the-kit">Get the kit</h2>
      <p>Download the kit for its approved assets, typography specimens, and exact implementation files. In a Next.js and Tailwind v4 project using the pinned shadcn CLI, the registry catalog lists available resources for discovery; an individual item URL supplies an installable theme or component. Open the catalog, choose the item your host needs, then follow the <a href="/docs/05-shadcn-binding/">shadcn installation instructions</a>. The catalog alone does not install a theme or the complete kit.</p>
      <ul>
        <li><a href={`/${slug}/downloads/${contract.bundle.package.filename}`}>Download {portal.brand.title} kit</a></li>
        <li><a href={`/${slug}/brand/r/registry.json`}>Browse the {portal.brand.title} registry catalog (JSON)</a></li>
        <li><a href={`/${slug}/brand/r/theme.json`}>Inspect the {portal.brand.title} installable theme item (JSON)</a></li>
      </ul>
    </section>
  </>;
}
