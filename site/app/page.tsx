import type { CSSProperties } from "react";
import Link from "next/link";
import brands from "../generated/brands.json";

export default function Home() {
  const production = brands.filter((brand) => brand.kind !== "fixture");
  const fixture = brands.find((brand) => brand.kind === "fixture");
  return (
    <div className="shell">
      <section className="hero">
        <div>
          <p className="eyebrow">Brand and design system</p>
          <h1>One canon. Five distinct voices.</h1>
        </div>
        <div>
          <p className="lede">Verified kits, accessible tokens, implementation guidance, and installable registries for every ShruggieTech identity.</p>
          <div className="actions">
            <Link className="button primary" href="/docs/">Read the system</Link>
            <a className="button" href="https://github.com/ShruggieTech/shruggie-brand/releases">Download bundles</a>
          </div>
        </div>
      </section>
      <section className="section" aria-labelledby="brands-heading">
        <div className="section-heading">
          <h2 id="brands-heading">Identity spectrum</h2>
          <p>Each product owns one accent under the shared parent system. The complete set makes the remaining hue space visible.</p>
        </div>
        <div className="brand-grid">
          {production.map((brand) => (
            <Link className="brand-card" href={`/${brand.slug}/`} key={brand.slug} style={{ "--brand-accent": brand.accent } as CSSProperties}>
              <span className="swatch" aria-hidden="true" />
              <h3>{brand.title}</h3>
              <p>{brand.descriptor}</p>
            </Link>
          ))}
        </div>
      </section>
      {fixture && (
        <section className="section">
          <p className="eyebrow">Worked example</p>
          <h2>Test the whole pipeline</h2>
          <p className="lede">The synthetic fixture exercises every generator and gate while leaving the production identity spectrum untouched.</p>
          <div className="actions"><Link className="button" href={`/${fixture.slug}/`}>Open the fixture</Link></div>
        </section>
      )}
    </div>
  );
}
