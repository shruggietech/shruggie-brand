'use client';

import { useState } from 'react';
import type { ConformanceRecord } from '@/lib/conformance';

export function ConformanceReference({ record }: { record: ConformanceRecord }) {
  const [profile, setProfile] = useState('normal-desktop');
  const selected = record.profiles.find((item) => item.id === profile) ?? record.profiles[0];
  return <div className="conformance-reference">
    <section className="conformance-controls" aria-labelledby="profile-heading">
      <p className="eyebrow">Generated capability matrix</p><h2 id="profile-heading">Reference profile</h2>
      <div className="conformance-profile-list" role="group" aria-label="Reference profile">
        {record.profiles.map((item) => <button key={item.id} type="button" aria-pressed={item.id === profile} onClick={() => setProfile(item.id)}>{item.id.replaceAll('-', ' ')}</button>)}
      </div>
      <dl className="conformance-profile-summary"><div><dt>Viewport</dt><dd>{selected.viewport.width} × {selected.viewport.height}, {selected.viewport.orientation}</dd></div><div><dt>Input</dt><dd>{selected.input.touch ? 'touch' : selected.input.pointer} · {selected.input.keyboard ? 'keyboard' : 'no hardware keyboard'}</dd></div><div><dt>Adaptation</dt><dd>{selected.motion} motion · {selected.contrast} contrast · {selected.text_scale}× text</dd></div></dl>
    </section>
    <section aria-labelledby="specimen-heading"><h2 id="specimen-heading">Interactive browser specimen</h2><p>The embedded specimen is generated from this brand&apos;s pinned adapter. It is browser-reference evidence only.</p><iframe className="conformance-frame" src={`${record.specimenPath}?profile=${profile}`} title={`${record.title} generated browser conformance specimen`} /></section>
    <section aria-labelledby="host-heading"><h2 id="host-heading">Host evidence boundary</h2><div className="conformance-host-grid">{record.hostTracks.map((track) => <article key={track.id}><h3>{track.id.replaceAll('-', ' ')}</h3><p><strong>{track.status}</strong> · {track.evidence_class}</p><dl><dt>Host</dt><dd>{track.host_version}</dd><dt>Renderer</dt><dd>{track.renderer_version}</dd><dt>Target</dt><dd>{track.target_version}</dd><dt>Tool</dt><dd>{track.tool_version}</dd></dl><p>{track.profiles.length} declared profiles</p></article>)}</div><p className="conformance-boundary">Actual-host and consumer-adoption evidence remain separately tracked and pending proof. Browser emulation cannot promote either state.</p></section>
  </div>;
}
