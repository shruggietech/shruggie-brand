import type { CSSProperties } from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import brands from "../../generated/brands.json";

export function generateStaticParams() {
  return brands.map((brand) => ({ slug: brand.slug }));
}

export default async function BrandPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const brand = brands.find((item) => item.slug === slug);
  if (!brand) notFound();
  return (
    <div className="shell" style={{ "--sh-accent": brand.accent, "--brand-accent": brand.accent } as CSSProperties}>
      <section className="brand-hero">
        <div>
          <p className="eyebrow">{brand.kind === "fixture" ? "Pipeline fixture" : "ShruggieTech identity"}</p>
          <h1>{brand.title}</h1>
          <p className="lede">{brand.descriptor}</p>
          <p className="meta">Kit {brand.version} · {brand.idea}</p>
          <div className="actions">
            <a className="button primary" href={`/${brand.slug}/guidelines/`}>Open guidelines</a>
            <Link className="button" href={`/${brand.slug}/downloads/`}>Downloads</Link>
          </div>
        </div>
        <img className="brand-logo" src={brand.logo} alt={`${brand.title} horizontal logo`} />
      </section>
      <section className="section">
        <p className="eyebrow">Installable registry</p>
        <h2>Use the verified theme</h2>
        <p className="lede">Registry files are copied directly from the kit build.</p>
        <pre><code>{`npx shadcn@latest registry add @${brand.slug}=https://brand.shruggie.tech/${brand.slug}/brand/r/{name}.json\nnpx shadcn@latest add @${brand.slug}/theme`}</code></pre>
      </section>
    </div>
  );
}
