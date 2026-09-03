// Header — fixed translucent site header with logo, nav, CTA.
// Nav links drive the UI-kit's active screen (interactive recreation).
const { useState, useEffect } = React;
const { Button } = window.ShruggieTechDesignSystem_1f6967;

const NAV = ["Services", "Work", "Research", "Products", "About", "Blog"];

function Header({ current, onNavigate }) {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const root = document.querySelector("#kit-scroll");
    const el = root || window;
    const onScroll = () => {
      const y = root ? root.scrollTop : window.scrollY;
      setScrolled(y > 12);
    };
    el.addEventListener("scroll", onScroll, { passive: true });
    return () => el.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      style={{
        position: "sticky", top: 0, zIndex: 50,
        transition: "background-color .2s, backdrop-filter .2s",
        backgroundColor: scrolled ? "color-mix(in srgb, var(--bg-primary) 80%, transparent)" : "transparent",
        backdropFilter: scrolled ? "blur(12px)" : "none",
        WebkitBackdropFilter: scrolled ? "blur(12px)" : "none",
      }}
    >
      <div className="kit-container" style={{ display: "flex", height: 64, alignItems: "center", justifyContent: "space-between" }}>
        <a href="#" onClick={(e) => { e.preventDefault(); onNavigate("Home"); }} style={{ display: "flex", alignItems: "center" }}>
          <img src="../../assets/logo-darkbg.png" alt="ShruggieTech" style={{ height: 30, width: "auto" }} />
        </a>
        <nav style={{ display: "flex", gap: 4 }}>
          {NAV.map((label) => {
            const active = current === label;
            return (
              <a key={label} href="#"
                onClick={(e) => { e.preventDefault(); onNavigate(label); }}
                style={{
                  position: "relative", padding: "8px 12px",
                  fontFamily: "var(--font-body)", fontSize: 14, fontWeight: 500,
                  textTransform: "uppercase", letterSpacing: ".03em",
                  color: active ? "var(--text-primary)" : "var(--text-secondary)",
                  transition: "color .2s",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.color = "var(--text-primary)")}
                onMouseLeave={(e) => (e.currentTarget.style.color = active ? "var(--text-primary)" : "var(--text-secondary)")}
              >
                {label}
                <span style={{
                  position: "absolute", bottom: 2, left: 12, right: 12, height: 2,
                  background: "var(--accent-color)", transformOrigin: "left",
                  transform: active ? "scaleX(1)" : "scaleX(0)", transition: "transform .2s",
                }} />
              </a>
            );
          })}
        </nav>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <a href="#" onClick={(e) => { e.preventDefault(); onNavigate("Contact"); }}>
            <Button variant="primary" size="sm">Get in Touch</Button>
          </a>
        </div>
      </div>
    </header>
  );
}

Object.assign(window, { Header });
