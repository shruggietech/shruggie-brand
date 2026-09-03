// ServicesScreen — page hero, four service pillars, process, CTA.
const { SectionHeading: SvHeading, ShruggieCTA: SvCTA, Badge: SvBadge } =
  window.ShruggieTechDesignSystem_1f6967;

const PILLARS = [
  { id: "01", title: "Digital Strategy & Brand",
    lead: "Your brand is the first thing people see and the last thing they remember. We make both count.",
    caps: ["Logo & visual identity systems", "Color & typography systems", "Brand standards kits", "Website strategy & content architecture", "Marketing collateral & print"] },
  { id: "02", title: "Development & Integration",
    lead: "We build, migrate, and integrate. From marketing sites to custom applications, we handle the full technical stack.",
    caps: ["Custom websites & web apps", "CMS deployment & migration", "Blockchain & smart contracts", "Third-party integrations", "DNS, hosting & replatforming"] },
  { id: "03", title: "Revenue Flows & Marketing Ops",
    lead: "Visibility means nothing without conversion. We build the systems that turn attention into revenue.",
    caps: ["SEO strategy & execution", "Answer Engine Optimization (AEO)", "Google Ads & Meta advertising", "Analytics (GA4, GTM, Search Console)", "Reviews & reputation management"] },
  { id: "04", title: "AI & Data Analysis",
    lead: "AI is not magic. It is infrastructure. We help you build AI systems that solve real problems.",
    caps: ["Conversational AI & chatbots", "RAG system design", "Semantic & vector search", "Workflow automation", "AI adoption consulting"] },
];

const PROCESS = [
  { k: "Discuss", d: "We learn how your business actually works before proposing anything." },
  { k: "Create", d: "We design, build, and iterate against a clear written specification." },
  { k: "Deliver", d: "We ship working systems, measure them, and hand you full ownership." },
];

function PillarSection({ p, index }) {
  const alt = index % 2 === 1;
  return (
    <section style={{ background: alt ? "var(--surface-dark-warm)" : "var(--bg-primary)", paddingTop: 72, paddingBottom: 72 }}>
      <div className="kit-container" style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 48, alignItems: "start" }}>
        <div>
          <span className="eyebrow" style={{ fontFamily: "var(--font-mono)", fontSize: 13 }}>{p.id}</span>
          <h2 style={{ margin: "12px 0 0", fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 34, letterSpacing: "-0.02em", color: "var(--text-primary)" }}>{p.title}</h2>
          <p style={{ marginTop: 16, fontSize: 18, lineHeight: 1.6, color: "var(--text-secondary)" }}>{p.lead}</p>
        </div>
        <ul style={{ margin: 0, padding: 0, listStyle: "none", display: "flex", flexDirection: "column", gap: 12, paddingTop: 8 }}>
          {p.caps.map((c) => (
            <li key={c} style={{ display: "flex", gap: 10, alignItems: "center", fontSize: 15, color: "var(--text-secondary)" }}>
              <Icon name="check" size={16} color="var(--accent-color)" /> {c}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

function ServicesScreen({ onNavigate }) {
  return (
    <div>
      <section style={{ background: "var(--surface-dark-warm)", paddingTop: 140, paddingBottom: 72 }}>
        <div className="kit-container">
          <h1 style={{ margin: 0, fontFamily: "var(--font-display)", fontWeight: 700, fontSize: "clamp(40px,5vw,56px)", letterSpacing: "-0.025em", color: "var(--sh-fg)" }}>Services</h1>
          <p style={{ marginTop: 20, maxWidth: 640, fontSize: 18, lineHeight: 1.6, color: "var(--text-secondary)" }}>
            Strategy, design, development, and marketing, shaped around how your business actually operates.
          </p>
        </div>
      </section>

      {PILLARS.map((p, i) => <PillarSection key={p.id} p={p} index={i} />)}

      <section style={{ background: "var(--surface-dark-rich)", paddingTop: 96, paddingBottom: 96 }}>
        <div className="kit-container">
          <SvHeading label="Our Process" title="How We Work" align="center"
            description="Every engagement follows an iterative Discuss, Create, Deliver cycle." />
          <div style={{ marginTop: 48, display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 24 }}>
            {PROCESS.map((s, i) => (
              <div key={s.k} style={{ padding: 28, border: "1px solid rgba(255,255,255,.08)", borderRadius: 12, background: "rgba(255,255,255,.02)" }}>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 13, color: "var(--accent-color)" }}>{String(i + 1).padStart(2, "0")}</div>
                <h3 style={{ margin: "10px 0 8px", fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 22, color: "var(--text-primary)" }}>{s.k}</h3>
                <p style={{ margin: 0, fontSize: 15, color: "var(--text-secondary)" }}>{s.d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section style={{ background: "var(--surface-dark-deep)", paddingTop: 96, paddingBottom: 112, textAlign: "center" }}>
        <div className="kit-container">
          <h2 style={{ margin: 0, fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 40, letterSpacing: "-0.02em", color: "var(--sh-fg)" }}>Let's scope your project.</h2>
          <div style={{ marginTop: 32, display: "flex", justifyContent: "center" }}>
            <SvCTA href="#" onClick={(e) => { e.preventDefault(); onNavigate("Contact"); }}>Get in Touch</SvCTA>
          </div>
        </div>
      </section>
    </div>
  );
}

Object.assign(window, { ServicesScreen });
