// ProductsScreen — hero, four product cards, engineering philosophy, CTA.
const { Card: PrCard, Badge: PrBadge, SectionHeading: PrHeading, ShruggieCTA: PrCTA } =
  window.ShruggieTechDesignSystem_1f6967;

const PRODUCTS = [
  { icon: "package", name: "shruggie-indexer", badge: "v0.1.2 — Active", tone: "green", lang: "TypeScript",
    desc: "Cross-platform file and directory indexing tool. Produces structured JSON with hash-based content identities, filesystem metadata, and EXIF extraction.",
    links: ["GitHub", "Docs"] },
  { icon: "database", name: "metadexer", badge: "Pre-release — In Development", tone: "green", lang: "TypeScript",
    desc: "Content-addressed asset management system. Storage, cataloging, deduplication, and search across large, heterogeneous digital collections.",
    links: ["GitHub"] },
  { icon: "file-text", name: "shruggie-feedtools", badge: "Active", tone: "green", lang: "Python",
    desc: "Reference project for Python tool conventions, packaging patterns, and GUI design language.",
    links: ["GitHub"] },
  { icon: "cpu", name: "rustif", badge: "Declaration Phase", tone: "orange", lang: "Rust",
    desc: "A proposed Rust-native metadata processing engine. The next-generation successor to thirty years of metadata infrastructure.",
    links: ["Read Declaration"] },
];

function ProductsScreen({ onNavigate }) {
  return (
    <div>
      <section style={{ background: "var(--surface-dark-products)", paddingTop: 140, paddingBottom: 72 }}>
        <div className="kit-container">
          <h1 style={{ margin: 0, fontFamily: "var(--font-display)", fontWeight: 700, fontSize: "clamp(40px,5vw,56px)", letterSpacing: "-0.025em", color: "var(--sh-fg)" }}>Products</h1>
          <p style={{ marginTop: 20, maxWidth: 640, fontSize: 18, lineHeight: 1.6, color: "var(--text-secondary)" }}>
            We build things we need, then share them with the community.
          </p>
        </div>
      </section>

      <section style={{ background: "var(--bg-primary)", paddingTop: 72, paddingBottom: 96 }}>
        <div className="kit-container">
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 32 }}>
            {PRODUCTS.map((p) => (
              <PrCard key={p.name} style={{ display: "flex", flexDirection: "column", gap: 0 }}>
                <Icon name={p.icon} size={28} color="var(--accent-color)" style={{ marginBottom: 12 }} />
                <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 16 }}>
                  <h3 style={{ margin: 0, fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 20, color: "var(--text-primary)" }}>{p.name}</h3>
                  <PrBadge tone={p.tone}>{p.badge}</PrBadge>
                </div>
                <p style={{ margin: "16px 0 0", flex: 1, fontSize: 15, lineHeight: 1.6, color: "var(--text-secondary)" }}>{p.desc}</p>
                <div style={{ marginTop: 20, display: "flex", alignItems: "center", gap: 20 }}>
                  {p.links.map((l) => (
                    <a key={l} href="#" onClick={(e) => e.preventDefault()}
                      style={{ display: "inline-flex", alignItems: "center", gap: 6, fontFamily: "var(--font-display)", fontSize: 14, fontWeight: 500, color: "var(--accent-color)" }}>
                      {l} <Icon name="external-link" size={14} />
                    </a>
                  ))}
                  <span style={{ marginLeft: "auto", fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--text-muted)" }}>{p.lang}</span>
                </div>
              </PrCard>
            ))}
          </div>
        </div>
      </section>

      <section style={{ background: "var(--surface-dark-deep)", paddingTop: 88, paddingBottom: 88 }}>
        <div className="kit-container" style={{ display: "grid", gridTemplateColumns: "1.4fr 1fr", gap: 48, alignItems: "center" }}>
          <div>
            <PrHeading title="How We Build Software" />
            <p style={{ marginTop: 20, fontSize: 18, lineHeight: 1.7, color: "var(--text-body-light)" }}>
              Every product begins with a specification written for AI-first consumption, structured so AI coding
              agents produce correct implementations within single context windows. This methodology multiplies
              engineering throughput without proportional headcount. It is how a small team builds production-grade tools.
            </p>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {["Spec", "Generate", "Review", "Ship"].map((step, i) => (
              <div key={step} style={{ display: "flex", alignItems: "center", gap: 14 }}>
                <div style={{ width: 34, height: 34, flex: "none", borderRadius: 8, display: "grid", placeItems: "center", background: "var(--green-bright-10)", color: "var(--accent-color)", fontFamily: "var(--font-mono)", fontSize: 13 }}>{i + 1}</div>
                <div style={{ fontFamily: "var(--font-display)", fontWeight: 500, color: "var(--text-primary)" }}>{step}</div>
                {i < 3 && <Icon name="arrow-right" size={16} color="var(--text-muted)" style={{ marginLeft: "auto" }} />}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section style={{ background: "var(--sh-bg)", paddingTop: 96, paddingBottom: 112, textAlign: "center" }}>
        <div className="kit-container">
          <h2 style={{ margin: 0, fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 40, letterSpacing: "-0.02em", color: "var(--sh-fg)" }}>The code is open. Jump in.</h2>
          <div style={{ marginTop: 32, display: "flex", justifyContent: "center" }}>
            <PrCTA href="#" onClick={(e) => e.preventDefault()}>View on GitHub</PrCTA>
          </div>
        </div>
      </section>
    </div>
  );
}

Object.assign(window, { ProductsScreen });
