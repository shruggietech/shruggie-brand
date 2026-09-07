import type { ColorEntry } from '@/lib/guidelines';
import { CopyValue } from './copy-value';

function Palette({ id, title, entries }: { id: string; title: string; entries: ColorEntry[] }) {
  return <section className="guide-section" aria-labelledby={id}><h2 id={id}>{title}</h2><div className="color-list">{entries.map((entry) => <article className="color-row" key={entry.token} data-color-token={entry.token}><div className="color-summary"><span className="color-chip" style={{ background: entry.hex }} aria-hidden="true" /><span className="color-name"><strong>{entry.role}</strong><code>{entry.token}</code>{entry.aliases.length > 0 && <small>Also: {entry.aliases.join(', ')}</small>}</span><code className="color-hex">{entry.hex}</code><CopyValue value={entry.hex} label={`${entry.role} HEX`} /></div><details className="color-details"><summary>See more color values</summary><dl><div><dt>RGB</dt><dd><code>{entry.rgb}</code></dd></div><div><dt>HSL</dt><dd><code>{entry.hsl}</code></dd></div><div><dt>OKLCH</dt><dd><code>{entry.oklch}</code></dd></div><div><dt>Lab D50</dt><dd><code>{entry.lab.replace(' (D50)', '')}</code></dd></div></dl><p>{entry.print}</p></details></article>)}</div></section>;
}

export function ColorReference({ palettes }: { palettes: { dark: ColorEntry[]; light: ColorEntry[] } }) {
  return <><p className="guide-lead">HEX is the canonical screen reference. Open one row for derived formats and print guidance.</p><Palette id="dark-palette" title="Dark palette" entries={palettes.dark} /><Palette id="light-palette" title="Light palette" entries={palettes.light} /></>;
}
