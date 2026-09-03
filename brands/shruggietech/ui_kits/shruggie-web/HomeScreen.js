// HomeScreen — hero + services preview + products preview + closing CTA.
const { Button: STButton, Card: STCard, Badge: STBadge, SectionHeading: STHeading, ShruggieCTA: STCTA } =
  window.ShruggieTechDesignSystem_1f6967;

const SERVICES = [
  { icon: "palette", title: "Digital Strategy & Brand", desc: "Identity systems, brand standards, and content architecture that translate across every touchpoint." },
  { icon: "code-xml", title: "Development & Integration", desc: "Marketing sites to custom applications — the full technical stack, shaped around your situation." },
  { icon: "trending-up", title: "Revenue & Marketing Ops", desc: "SEO, AEO, ads, and analytics wired into the systems that turn attention into revenue." },
  { icon: "cpu", title: "AI & Data Analysis", desc: "AI wired into the systems you already use: chatbots, RAG, semantic search, workflow automation." },
];

const PRODUCTS_PREVIEW = [
  { icon: "package", name: "shruggie-indexer", badge: "v0.1.2 — Active", desc: "Cross-platform file indexing with hash-based content identities and EXIF extraction." },
  { icon: "database", name: "metadexer", badge: "In Development", desc: "Content-addressed asset management: storage, cataloging, dedup, and search at scale." },
];

function HeroBg() {
  return (
    <div aria-hidden="true" style={{ position: "absolute", inset: 0, overflow: "hidden" }}>
      <div style={{
        position: "absolute", inset: 0,
        background:
          "radial-gradient(ellipse 80% 60% at 20% 40%, rgba(43,204,115,.10) 0%, transparent 70%)," +
          "radial-gradient(ellipse 60% 80% at 80% 60%, rgba(43,204,115,.06) 0%, transparent 70%)," +
          "radial-gradient(ellipse 70% 50% at 50% 15%, rgba(43,204,115,.07) 0%, transparent 60%)",
      }} />
      <div style={{
        position: "absolute", inset: 0, opacity: .5,
        backgroundImage: "radial-gradient(rgba(43,204,115,.18) 1px, transparent 1px)",
        backgroundSize: "26px 26px",
        maskImage: "radial-gradient(ellipse 70% 70% at 50% 45%, #000 30%, transparent 75%)",
        WebkitMaskImage: "radial-gradient(ellipse 70% 70% at 50% 45%, #000 30%, transparent 75%)",
      }} />
    </div>
  );
}

function HomeScreen({ onNavigate }) {
  return (
    <div>
      {/* Hero */}
      <section style={{ position: "relative", background: "var(--sh-bg)", overflow: "hidden" }}>
        <HeroBg />
        <div className="kit-container" style={{ position: "relative", zIndex: 1, paddingTop: 140, paddingBottom: 120 }}>
          <h1 style={{
            margin: 0, maxWidth: 900, fontFamily: "var(--font-display)", fontWeight: 700,
            fontSize: "clamp(44px, 6vw, 72px)", lineHeight: 1.05, letterSpacing: "-0.03em", color: "var(--sh-fg)",
          }}>
            We advance your vision.
          </h1>
          <p style={{ marginTop: 24, maxWidth: 620, fontSize: 18, lineHeight: 1.6, color: "var(--text-secondary)" }}>
            You have a business to run. We handle the technology that makes it grow: modern websites,
            marketing engines, AI integrations, and custom software, shaped around how you actually work.
          </p>
          <div style={{ marginTop: 40, display: "flex", flexWrap: "wrap", alignItems: "center", gap: 16 }}>
            <STCTA href="#" onClick={(e) => { e.preventDefault(); onNavigate("Contact"); }}>Start a Conversation</STCTA>
            <a href="#" onClick={(e) => { e.preventDefault(); onNavigate("Work"); }}>
              <STButton variant="secondary">See Our Work</STButton>
            </a>
          </div>
        </div>
      </section>

      {/* Services preview */}
      <section style={{ background: "var(--surface-dark-warm)", paddingTop: 96, paddingBottom: 96 }}>
        <div className="kit-container">
          <STHeading label="What We Do" title="Four ways we move you forward"
            description="Strategy, design, development, and marketing, shaped around how your business actually operates." />
          <div style={{ marginTop: 48, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
            {SERVICES.map((s) => (
              <STCard key={s.title} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <Icon name={s.icon} size={28} color="var(--accent-color)" />
                <h3 style={{ margin: "4px 0 0", fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 22, color: "var(--text-primary)" }}>{s.title}</h3>
                <p style={{ margin: 0, fontSize: 15, color: "var(--text-secondary)" }}>{s.desc}</p>
              </STCard>
            ))}
          </div>
        </div>
      </section>

      {/* Products preview */}
      <section style={{ background: "var(--surface-dark-rich)", paddingTop: 96, paddingBottom: 96 }}>
        <div className="kit-container">
          <STHeading label="Products" title="We build things we need, then share them" />
          <div style={{ marginTop: 48, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
            {PRODUCTS_PREVIEW.map((p) => (
              <STCard key={p.name} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <Icon name={p.icon} size={26} color="var(--accent-color)" />
                <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12 }}>
                  <h3 style={{ margin: 0, fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 20, color: "var(--text-primary)" }}>{p.name}</h3>
                  <STBadge>{p.badge}</STBadge>
                </div>
                <p style={{ margin: 0, fontSize: 15, color: "var(--text-secondary)" }}>{p.desc}</p>
                <a href="#" onClick={(e) => { e.preventDefault(); onNavigate("Products"); }}
                  style={{ marginTop: 4, display: "inline-flex", alignItems: "center", gap: 6, fontFamily: "var(--font-display)", fontSize: 14, fontWeight: 500, color: "var(--accent-color)" }}>
                  GitHub <Icon name="external-link" size={14} />
                </a>
              </STCard>
            ))}
          </div>
        </div>
      </section>

      {/* Closing CTA */}
      <section style={{ background: "var(--surface-dark-deep)", paddingTop: 96, paddingBottom: 112, textAlign: "center" }}>
        <div className="kit-container">
          <h2 style={{ margin: 0, fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 40, letterSpacing: "-0.02em", color: "var(--sh-fg)" }}>
            Let's scope your project.
          </h2>
          <div style={{ marginTop: 32, display: "flex", justifyContent: "center" }}>
            <STCTA href="#" onClick={(e) => { e.preventDefault(); onNavigate("Contact"); }}>Get in Touch</STCTA>
          </div>
        </div>
      </section>
    </div>
  );
}

Object.assign(window, { HomeScreen });
