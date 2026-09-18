const views = [
  {
    id: 'documentation-ownership',
    title: 'Documentation ownership',
    intro: 'Each surface has one job and an explicit boundary.',
    items: [
      ['Main manual', 'Owns system architecture, operating modes, contracts, verification, versions, and extension procedures.'],
      ['Hosted brand reference', 'Owns the current approved brand presentation, assets, bindings, affiliation, and generated version summary.'],
      ['Bundled implementation contract', 'Owns exact delivered paths, version pins, checks, recovery bytes, and offline implementation rules.'],
    ],
  },
  {
    id: 'operating-modes',
    title: 'Operating modes',
    intro: 'The requested outcome determines the mode before files change.',
    items: [
      ['Author', 'Change governed sources and templates, then regenerate and verify.'],
      ['Implementation', 'Consume exact generated contracts without creating parallel authority.'],
      ['Audit', 'Inspect and report conformance evidence without silently changing the delivery.'],
    ],
  },
  {
    id: 'capability-loop',
    title: 'Capability improvement loop',
    intro: 'Reusable gaps move upstream only through explicit authorization and versioned adoption.',
    items: [
      ['1. Consumer need', 'Identify a reproducible requirement that the current shared contract does not satisfy.'],
      ['2. Local gap record', 'Capture the need, semantic concept, and evidence without changing shared authority.'],
      ['3. Authorized upstream change', 'Update the owning canon, recipe, or adapter only after human authorization.'],
      ['4. Versioned adoption', 'Publish, verify, and let consumers deliberately adopt the exact new version.'],
    ],
  },
] as const;

export function DocumentationOverviews() {
  return <section className="documentation-overviews" aria-labelledby="documentation-system-overview">
    <h2 id="documentation-system-overview">How the system fits together</h2>
    <p>These summaries express the same relationships visually and in visible text, so they remain complete without scripts, animation, color, or graphics.</p>
    <div className="documentation-overview-grid">
      {views.map((view) => <article className="documentation-overview" key={view.id} aria-labelledby={view.id}>
        <h3 id={view.id}>{view.title}</h3>
        <p>{view.intro}</p>
        <ol>{view.items.map(([label, description]) => <li key={label}><strong>{label}</strong><span>{description}</span></li>)}</ol>
      </article>)}
    </div>
  </section>;
}
