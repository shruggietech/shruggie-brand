const ShruggieTechRuntime = (() => {
  const classNames = (...values) => values.filter(Boolean).join(" ");

  function Button({ variant = "primary", size = "md", className = "", children, ...props }) {
    const normalizedSize = size === "default" ? "md" : size;
    return <button className={classNames("sh-button", `sh-button--${variant}`, `sh-button--${normalizedSize}`, className)} {...props}>{children}</button>;
  }

  function Badge({ tone = "accent", className = "", children, ...props }) {
    const variant = tone === "warning" ? "emphasis" : tone === "success" ? "accent" : tone;
    return <span className={classNames("sh-badge", `sh-badge--${variant}`, className)} {...props}>{children}</span>;
  }

  function Card({ className = "", children, ...props }) {
    return <div className={classNames("sh-card", className)} {...props}>{children}</div>;
  }

  function SectionHeading({ label, title, description, align = "left", className = "" }) {
    return <div className={classNames("sh-section-heading", align === "center" && "runtime-center", className)}>
      {label ? <span className="eyebrow">{label}</span> : null}
      <h2 className="sh-section-heading__title">{title}</h2>
      {description ? <p className="sh-section-heading__description">{description}</p> : null}
    </div>;
  }

  function ShruggieCTA({ href = "#", variant = "primary", children, ...props }) {
    return <span className="runtime-cta" {...props}>
      <a href={href}><Button variant={variant}>{children}</Button></a>
      <span className="runtime-cta__tag" aria-hidden="true"><span>¯\_(ツ)_/¯</span> We'll figure it out.</span>
    </span>;
  }

  function Field({ as: Element = "input", label, required, error, id, children, className = "", ...props }) {
    const fieldId = id || props.name;
    return <label className="sh-field" htmlFor={fieldId}>
      {label ? <span className="sh-field__label">{label}{required ? <span className="sh-field__required"> *</span> : null}</span> : null}
      <Element id={fieldId} className={classNames("sh-field__control", className)} aria-invalid={error ? "true" : undefined} {...props}>{children}</Element>
      {error ? <span className="sh-field__error" role="alert">{error}</span> : null}
    </label>;
  }

  const Input = props => <Field {...props} />;
  const Textarea = props => <Field as="textarea" {...props} />;
  const Select = props => <Field as="select" {...props} />;
  const Divider = props => <hr className="sh-divider" {...props} />;

  return { Button, Badge, Card, SectionHeading, ShruggieCTA, Input, Textarea, Select, Divider };
})();

window.ShruggieTechDesignSystem_1f6967 = ShruggieTechRuntime;
