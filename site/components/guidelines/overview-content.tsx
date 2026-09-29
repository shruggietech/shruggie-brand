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

function ListOrExplanation({ values, empty }: { values?: string[]; empty: string }) {
  return values?.length ? <ul>{values.map((value) => <li key={value}>{value}</li>)}</ul> : <p>{empty}</p>;
}

export function GuidelineOverview({ portal }: { portal: GuidelinePortal }) {
  const value = portal.content.overview;
  const contract = portal.implementation;
  const slug = portal.brand.slug;
  const overrides = Object.entries(contract.rules.overrides);
  const house = contract.rules.inheritance === 'shruggietech-house';
  const messages = portal.brand.messaging;
  const messageRoles = [
    ['slogan', 'Slogan'],
    ['short_description', 'Short description'],
    ['long_description', 'Long description'],
    ['introductory_statement', 'Introduction'],
    ['positioning', 'Positioning'],
    ['mission', 'Mission'],
    ['vision', 'Vision'],
    ['values', 'Values'],
    ['brand_promise', 'Brand promise'],
  ] as const;

  return <>
    {messageRoles.some(([role]) => messages[role]) && <section className="guide-section" aria-labelledby="brand-overview">
      <h2 id="brand-overview">Brand overview</h2>
      <dl>{messageRoles.filter(([role]) => messages[role]).map(([role, label]) => <div key={role} data-message-role={role.replaceAll('_', '-')}><dt>{label}</dt><dd>{messages[role]}</dd></div>)}</dl>
    </section>}
    {value.foundation && <section className="guide-section" aria-labelledby="foundations">
      <h2 id="foundations">{value.foundation_title || 'Foundations'}</h2>
      <p>{value.foundation}</p>
    </section>}
    {value.promises?.length ? <section className="guide-section" aria-labelledby="promises">
      <h2 id="promises">Promises</h2>
      <ListOrExplanation values={value.promises} empty="" />
    </section> : null}
    {(value.in_scope?.length || value.out_of_scope?.length || value.sharp_edge || portal.brand.vendorBoundary) && <section className="guide-section" aria-labelledby="boundaries">
      <h2 id="boundaries">Boundaries</h2>
      <div className="guide-columns">
        {value.in_scope?.length ? <div><h3>In scope</h3><ListOrExplanation values={value.in_scope} empty="" /></div> : null}
        {value.out_of_scope?.length ? <div><h3>Out of scope</h3><ListOrExplanation values={value.out_of_scope} empty="" /></div> : null}
      </div>
      {value.sharp_edge && <aside className="guide-notice"><strong>Important boundary</strong><p>{value.sharp_edge}</p></aside>}
      {portal.brand.vendorBoundary && <p>{portal.brand.vendorBoundary}</p>}
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
