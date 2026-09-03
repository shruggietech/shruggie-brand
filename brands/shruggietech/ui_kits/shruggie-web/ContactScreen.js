// ContactScreen — contact form with live validation-lite + success state.
const { Input: CtInput, Textarea: CtTextarea, Select: CtSelect, Button: CtButton } =
  window.ShruggieTechDesignSystem_1f6967;
const { useState: useCtState } = React;

function ContactScreen() {
  const [sent, setSent] = useCtState(false);
  const [form, setForm] = useCtState({ name: "", email: "", company: "", message: "", referral: "" });
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));
  const submit = (e) => { e.preventDefault(); setSent(true); };

  return (
    <div>
      <section style={{ background: "var(--surface-dark-warm)", paddingTop: 140, paddingBottom: 56 }}>
        <div className="kit-container">
          <h1 style={{ margin: 0, fontFamily: "var(--font-display)", fontWeight: 700, fontSize: "clamp(40px,5vw,56px)", letterSpacing: "-0.025em", color: "var(--sh-fg)" }}>Let's talk.</h1>
          <p style={{ marginTop: 20, maxWidth: 620, fontSize: 18, lineHeight: 1.6, color: "var(--text-secondary)" }}>
            Tell us what you're building. We'll figure out how to move it forward.
          </p>
        </div>
      </section>

      <section style={{ background: "var(--bg-primary)", paddingTop: 56, paddingBottom: 112 }}>
        <div className="kit-container" style={{ display: "grid", gridTemplateColumns: "1.3fr 1fr", gap: 64, alignItems: "start" }}>
          <div>
            {sent ? (
              <div role="status" style={{ borderRadius: 12, border: "1px solid var(--green-bright-40)", background: "rgba(43,204,115,.06)", padding: 32, textAlign: "center" }}>
                <p style={{ margin: 0, fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 26, color: "var(--text-primary)" }}>Thanks for reaching out.</p>
                <p style={{ margin: "10px 0 0", fontSize: 16, color: "var(--text-secondary)" }}>We'll get back to you soon!</p>
                <div style={{ marginTop: 20 }}>
                  <CtButton variant="secondary" size="sm" onClick={() => { setSent(false); setForm({ name: "", email: "", company: "", message: "", referral: "" }); }}>Send another</CtButton>
                </div>
              </div>
            ) : (
              <form onSubmit={submit} style={{ display: "flex", flexDirection: "column", gap: 24 }}>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
                  <CtInput label="Name" required name="name" placeholder="Your name" value={form.name} onChange={set("name")} />
                  <CtInput label="Email" required name="email" type="email" placeholder="you@company.com" value={form.email} onChange={set("email")} />
                </div>
                <CtInput label="Company / Organization" name="company" placeholder="Your company (optional)" value={form.company} onChange={set("company")} />
                <CtTextarea label="How can we help?" required name="message" rows={5} placeholder="Tell us about your project or question" value={form.message} onChange={set("message")} />
                <CtSelect label="How did you hear about us?" name="referral" value={form.referral} onChange={set("referral")}>
                  <option value="">Select an option (optional)</option>
                  <option value="Search engine">Search engine</option>
                  <option value="Referral">Referral</option>
                  <option value="Social media">Social media</option>
                  <option value="Other">Other</option>
                </CtSelect>
                <div><CtButton type="submit" variant="primary">Send Message</CtButton></div>
              </form>
            )}
          </div>

          <aside style={{ display: "flex", flexDirection: "column", gap: 28, paddingTop: 8 }}>
            <div>
              <div className="eyebrow">Where we are</div>
              <p style={{ margin: "12px 0 0", fontSize: 16, color: "var(--text-secondary)" }}>Knoxville, Tennessee<br />Made in the USA 🇺🇸</p>
            </div>
            <div>
              <div className="eyebrow">What to expect</div>
              <ul style={{ margin: "12px 0 0", padding: 0, listStyle: "none", display: "flex", flexDirection: "column", gap: 10 }}>
                {["A real reply from a real person", "A scoped, honest plan", "Full ownership of everything we build"].map((t) => (
                  <li key={t} style={{ display: "flex", gap: 10, alignItems: "center", fontSize: 15, color: "var(--text-secondary)" }}>
                    <Icon name="check" size={16} color="var(--accent-color)" /> {t}
                  </li>
                ))}
              </ul>
            </div>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: 22, color: "var(--accent-color)" }}>¯\_(ツ)_/¯</div>
          </aside>
        </div>
      </section>
    </div>
  );
}

Object.assign(window, { ContactScreen });
