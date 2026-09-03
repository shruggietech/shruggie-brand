// Footer — four-column site footer with brand, pages, products, connect.
const FOOTER_PAGES = ["Services", "Work", "Research", "Blog", "About", "Contact"];
const FOOTER_PRODUCTS = ["shruggie-indexer", "metadexer", "rustif", "shruggie-feedtools"];
const FOOTER_SOCIAL = [
  { icon: "github", label: "GitHub" },
  { icon: "facebook", label: "Facebook" },
  { icon: "instagram", label: "Instagram" },
  { icon: "twitter", label: "X (Twitter)" },
];

function Footer({ onNavigate }) {
  const col = { display: "flex", flexDirection: "column", gap: 12 };
  const head = { margin: "0 0 16px", fontFamily: "var(--font-display)", fontSize: 14, fontWeight: 500, textTransform: "uppercase", letterSpacing: ".06em", color: "var(--text-muted)" };
  const link = { fontSize: 14, color: "var(--text-secondary)", textDecoration: "none" };
  const nav = (label) => (e) => { e.preventDefault(); onNavigate(label); };
  return (
    <footer style={{ background: "var(--bg-secondary)" }}>
      <div className="kit-container" style={{ paddingTop: 64, paddingBottom: 64 }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 48 }}>
          <div>
            <img src="../../assets/logo-darkbg.png" alt="ShruggieTech" style={{ height: 30, width: "auto" }} />
            <p style={{ marginTop: 16, maxWidth: 240, fontSize: 14, color: "var(--text-secondary)" }}>
              Modern digital systems, software, and AI-driven experiences.
            </p>
          </div>
          <div>
            <h3 style={head}>Pages</h3>
            <ul style={{ ...col, listStyle: "none", padding: 0, margin: 0 }}>
              {FOOTER_PAGES.map((p) => <li key={p}><a href="#" style={link} onClick={nav(p)}>{p}</a></li>)}
            </ul>
          </div>
          <div>
            <h3 style={head}>Products</h3>
            <ul style={{ ...col, listStyle: "none", padding: 0, margin: 0 }}>
              {FOOTER_PRODUCTS.map((p) => <li key={p}><a href="#" style={{ ...link, fontFamily: "var(--font-mono)" }} onClick={nav("Products")}>{p}</a></li>)}
            </ul>
          </div>
          <div>
            <h3 style={head}>Connect</h3>
            <div style={{ display: "flex", gap: 16 }}>
              {FOOTER_SOCIAL.map((s) => (
                <a key={s.label} href="#" aria-label={s.label} style={{ color: "var(--text-secondary)" }} onClick={(e) => e.preventDefault()}>
                  <Icon name={s.icon} size={20} />
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
      <div style={{ borderTop: "1px solid var(--border-color)" }}>
        <div className="kit-container" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", paddingTop: 24, paddingBottom: 24 }}>
          <p style={{ margin: 0, fontSize: 12, color: "var(--text-muted)" }}>© Copyright Shruggie, LLC 2026 · Made in the USA 🇺🇸</p>
          <a href="#" style={{ fontSize: 12, color: "var(--text-muted)", textDecoration: "none" }} onClick={(e) => e.preventDefault()}>Privacy Policy</a>
        </div>
      </div>
    </footer>
  );
}

Object.assign(window, { Footer });
