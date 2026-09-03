// App — UI-kit router. Header nav switches screens; screens fall back to Home.
const { useState: useAppState, useEffect: useAppEffect } = React;

function GenericScreen({ title, blurb }) {
  return (
    <section style={{ background: "var(--surface-dark-warm)", minHeight: 520, paddingTop: 140, paddingBottom: 120 }}>
      <div className="kit-container">
        <h1 style={{ margin: 0, fontFamily: "var(--font-display)", fontWeight: 700, fontSize: "clamp(40px,5vw,56px)", letterSpacing: "-0.025em", color: "var(--sh-fg)" }}>{title}</h1>
        <p style={{ marginTop: 20, maxWidth: 640, fontSize: 18, lineHeight: 1.6, color: "var(--text-secondary)" }}>{blurb}</p>
      </div>
    </section>
  );
}

function App() {
  const [screen, setScreen] = useAppState("Home");
  const scrollRef = React.useRef(null);
  const go = (name) => { setScreen(name); if (scrollRef.current) scrollRef.current.scrollTop = 0; };
  useAppEffect(() => { if (window.lucide) window.lucide.createIcons(); });

  let body;
  if (screen === "Home") body = <HomeScreen onNavigate={go} />;
  else if (screen === "Services") body = <ServicesScreen onNavigate={go} />;
  else if (screen === "Products") body = <ProductsScreen onNavigate={go} />;
  else if (screen === "Contact") body = <ContactScreen />;
  else if (screen === "Work") body = <GenericScreen title="Work" blurb="Selected engagements — from local tire shops owning their search to nonprofits scaling their reach. Case studies live here on the full site." />;
  else if (screen === "Research") body = <GenericScreen title="Research" blurb="Published notes on multi-agent coding workflows, specification-driven development, and metadata infrastructure." />;
  else if (screen === "About") body = <GenericScreen title="About" blurb="A small team solving real problems with modern technology. Based in Knoxville, Tennessee." />;
  else body = <GenericScreen title={screen} blurb="This section is part of the full ShruggieTech site. This UI kit focuses on Home, Services, Products, and Contact." />;

  return (
    <div ref={scrollRef} id="kit-scroll" style={{ height: "100vh", overflowY: "auto", background: "var(--bg-primary)" }}>
      <Header current={screen === "Home" ? "" : screen} onNavigate={go} />
      {body}
      <Footer onNavigate={go} />
    </div>
  );
}

function mountApp() {
  const el = document.getElementById("shruggie-kit-root");
  if (!el) return;
  ReactDOM.createRoot(el).render(<App />);
}
mountApp();
