// Icon — thin wrapper over lucide UMD. Renders <span class="i" data-lucide>.
// A shared registry re-runs lucide.createIcons() after each mount so newly
// rendered icons get their SVG injected.
const { useEffect } = React;

function Icon({ name, size = 20, color, style, className = "" }) {
  useEffect(() => {
    if (window.lucide) window.lucide.createIcons();
  });
  return (
    <span
      className={"i " + className}
      style={{ width: size, height: size, color, ...style }}
    >
      <i data-lucide={name}></i>
    </span>
  );
}

Object.assign(window, { Icon });
