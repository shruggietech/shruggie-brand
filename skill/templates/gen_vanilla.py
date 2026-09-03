#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_vanilla.py: tokens/, styles.css and components/ for non-React surfaces.

NEW in this kit. In the three kits that came before, everything under tokens/
and components/ was hand-authored per brand, which is precisely where drift
gets in: colors.css and nextjs/globals.css are the same system written twice by
hand, and only one of them is checked. This generator reads brand.json and the
canon so the vanilla layer is derived from the same numbers the shadcn binding
uses.

    python3 build/gen_vanilla.py <brand.json> <kit-dir>
"""
import json, os, sys
from coloraide import Color

HERE = os.path.dirname(os.path.abspath(__file__))


def rgb_parts(hex_):
    c = Color(hex_).convert("srgb")
    return " ".join(str(int(round(v * 255))) for v in c[:3])


CORE_JSX = {
    "Button": 'export function Button({{ variant = "primary", size = "md", children, ...props }}) {{\n'
              '  return <button className={{`{p}-button {p}-button--${{variant}} {p}-button--${{size}}`}} type="button" {{...props}}>{{children}}</button>;\n}}\n',
    "Badge": 'export function Badge({{ tone = "neutral", children }}) {{\n'
             '  return <span className={{`{p}-badge {p}-badge--${{tone}}`}}>{{children}}</span>;\n}}\n',
    "Card": 'export function Card({{ children, ...props }}) {{\n'
            '  return <div className="{p}-card" {{...props}}>{{children}}</div>;\n}}\n',
    "Divider": 'export function Divider() {{\n  return <hr className="{p}-divider" />;\n}}\n',
    "SectionHeading": 'export function SectionHeading({{ eyebrow, title, description }}) {{\n'
                      '  return <header className="{p}-section-heading">{{eyebrow ? <div className="{p}-eyebrow">{{eyebrow}}</div> : null}}'
                      '<h2 className="{p}-section-heading__title">{{title}}</h2>'
                      '{{description ? <p className="{p}-section-heading__description">{{description}}</p> : null}}</header>;\n}}\n',
}

FORM_JSX = {
    "Input": ("input", "text"),
    "Textarea": ("textarea", None),
    "Select": ("select", None),
}


def kebab(name):
    import re as _re
    return _re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def emit_components(kit, P, brand, w):
    rows = brand.get("domain_components") or {}
    css = [
        ".{p}-button {{ align-items: center; border: var(--{p}-stroke-hairline) solid transparent; border-radius: var(--{p}-radius-md); cursor: pointer; display: inline-flex; font-family: var(--{p}-font-body); font-weight: var(--{p}-weight-medium); gap: var(--{p}-space-2); justify-content: center; transition: background var(--{p}-motion-fast) var(--{p}-ease), border-color var(--{p}-motion-fast) var(--{p}-ease), color var(--{p}-motion-fast) var(--{p}-ease); }}",
        ".{p}-button--sm {{ font-size: var(--{p}-body-xs); min-height: 2rem; padding: 0 var(--{p}-space-3); }}",
        ".{p}-button--md {{ font-size: var(--{p}-body-sm); min-height: 2.5rem; padding: 0 var(--{p}-space-4); }}",
        ".{p}-button--lg {{ font-size: var(--{p}-body-md); min-height: 3rem; padding: 0 var(--{p}-space-5); }}",
        ".{p}-button--primary {{ background: var(--{p}-accent); color: var(--{p}-primary-foreground); }}",
        ".{p}-button--primary:hover {{ background: var(--{p}-accent-deep); }}",
        ".{p}-button--secondary {{ background: var(--{p}-panel-raised); border-color: var(--{p}-border); color: var(--{p}-fg); }}",
        ".{p}-button--secondary:hover, .{p}-button--ghost:hover {{ background: var(--{p}-hover); }}",
        ".{p}-button--ghost {{ background: transparent; color: var(--{p}-fg-muted); }}",
        ".{p}-badge {{ align-items: center; border: var(--{p}-stroke-hairline) solid var(--{p}-border); border-radius: var(--{p}-radius-pill); display: inline-flex; font-family: var(--{p}-font-mono); font-size: var(--{p}-body-xs); gap: var(--{p}-space-1); line-height: 1; padding: var(--{p}-space-1) var(--{p}-space-2); }}",
        '.{p}-badge::before {{ background: currentColor; border-radius: 50%; content: ""; height: .375rem; width: .375rem; }}',
        ".{p}-badge--accent {{ background: var(--{p}-accent-10); border-color: var(--{p}-accent-20); color: var(--{p}-accent); }}",
        ".{p}-badge--emphasis {{ background: var(--{p}-orange-12); color: var(--{p}-warning); }}",
        ".{p}-badge--neutral {{ color: var(--{p}-fg-muted); }}",
        ".{p}-badge--danger {{ background: var(--{p}-fault-12); color: var(--{p}-danger); }}",
        ".{p}-card {{ background: var(--{p}-panel); border: var(--{p}-stroke-hairline) solid var(--{p}-border); border-radius: var(--{p}-radius-xl); padding: var(--{p}-space-5); }}",
        ".{p}-divider {{ background: var(--{p}-border); border: 0; height: var(--{p}-stroke-hairline); margin: var(--{p}-space-5) 0; }}",
        ".{p}-section-heading {{ max-width: var(--{p}-content-narrow); }}",
        ".{p}-section-heading__title {{ margin-top: var(--{p}-space-2); }}",
        ".{p}-section-heading__description {{ color: var(--{p}-fg-muted); }}",
        ".{p}-field {{ display: grid; gap: var(--{p}-space-2); }}",
        ".{p}-field__label {{ font-size: var(--{p}-body-sm); font-weight: var(--{p}-weight-medium); }}",
        ".{p}-field__required {{ color: var(--{p}-warning); }}",
        ".{p}-field__control {{ background: var(--{p}-bg); border: var(--{p}-stroke-hairline) solid var(--{p}-border); border-radius: var(--{p}-radius-md); color: var(--{p}-fg); font: inherit; min-height: 2.75rem; padding: var(--{p}-space-2) var(--{p}-space-3); width: 100%; }}",
        ".{p}-field__control:hover {{ border-color: var(--{p}-fg-muted); }}",
        '.{p}-field__control[aria-invalid="true"] {{ border-color: var(--{p}-danger); }}',
        ".{p}-field__error {{ color: var(--{p}-danger); font-size: var(--{p}-body-xs); }}",
    ]
    for comp, props in rows.items():
        k = kebab(comp)
        cells_ = [x for x in props if x != "selected"]
        cols = " ".join(["minmax(0, 1fr)"] + ["8rem"] * (len(cells_) - 1))
        css += [
            ".{p}-%s {{ align-items: center; border: var(--{p}-stroke-hairline) solid transparent; border-radius: var(--{p}-radius-md); color: var(--{p}-fg-muted); display: grid; font-family: var(--{p}-font-mono); font-size: var(--{p}-body-xs); gap: var(--{p}-space-3); grid-template-columns: %s; min-height: 2.75rem; padding: 0 var(--{p}-space-3); }}" % (k, cols),
            ".{p}-%s:hover {{ background: var(--{p}-hover); color: var(--{p}-fg); }}" % k,
            '.{p}-%s[aria-selected="true"] {{ background: var(--{p}-accent-10); border-color: var(--{p}-accent-20); color: var(--{p}-fg); }}' % k,
            ".{p}-%s__%s {{ color: var(--{p}-fg); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}" % (k, cells_[0]),
            "@media (max-width: 42rem) {{ .{p}-%s {{ grid-template-columns: minmax(0, 1fr) 6rem; }} %s {{ display: none; }} }}"
            % (k, ", ".join(".{p}-%s__%s" % (k, x) for x in cells_[1:-1]) or ".{p}-%s__%s" % (k, cells_[-1])),
        ]
    w("components/components.css", "\n".join(c.format(p=P) for c in css) + "\n")

    for name, tpl in CORE_JSX.items():
        w("components/core/%s.jsx" % name, tpl.format(p=P))
    for comp, props in rows.items():
        k = kebab(comp)
        sel = " aria-selected={selected}" if "selected" in props else ""
        args = ", ".join(("%s = false" % x) if x == "selected" else x for x in props)
        cells = "".join('<div className="%s-%s__%s" role="cell">{%s}</div>' % (P, k, x, x)
                        for x in props if x != "selected")
        w("components/core/%s.jsx" % comp,
          'export function %s({ %s }) {\n  return <div className="%s-%s" role="row"%s>%s</div>;\n}\n'
          % (comp, args, P, k, sel, cells))
    for name, (tag, typ) in FORM_JSX.items():
        el = ("<%s className=\"%s-field__control\" id={id} {...props}%s />"
              % (tag, P, (' type="%s"' % typ) if typ else "")) if tag != "select" else (
              "<select className=\"%s-field__control\" id={id} {...props}>{children}</select>" % P)
        extra = ", children" if tag == "select" else ""
        w("components/forms/%s.jsx" % name,
          'export function %s({ id, label, required = false, error%s, ...props }) {\n'
          '  return (\n'
          '    <div className="%s-field">\n'
          '      <label className="%s-field__label" htmlFor={id}>{label}{required ? <span className="%s-field__required" aria-hidden="true"> *</span> : null}</label>\n'
          '      %s\n'
          '      {error ? <p className="%s-field__error" role="alert">{error}</p> : null}\n'
          '    </div>\n'
          '  );\n}\n' % (name, extra, P, P, P, el, P))

    w("components/README.md",
      "# %s components\n\n"
      "GENERATED by `build/gen_vanilla.py` from `brand.json`. Regenerate rather than editing.\n\n"
      "These framework-light React components carry the %s interface grammar for mocks and\n"
      "non-React surfaces. Import `../styles.css` and `components.css`, then compose the JSX\n"
      "modules. Every visual value resolves through the `--%s-*` token namespace, so there is\n"
      "no raw hex and no raw px anywhere in this directory.\n\n"
      "Core covers Button, Badge, Card, Divider and SectionHeading, plus one row component per\n"
      "entry in `domain_components`. Form components expose a visible label, required state and\n"
      "an accessible error message. Status is carried by a dot or a text label as well as colour.\n"
      % (brand["title"], brand["title"], P))


def main():
    spec, kit = sys.argv[1], sys.argv[2]
    B = json.load(open(spec, encoding="utf-8"))
    canon = json.load(open(os.path.join(HERE, "..", "references", "01-canon.json"), encoding="utf-8"))
    imm = canon["color"]["immutable"]
    ramp = canon["color"]["neutral_ramp"]
    g = canon["geometry"]
    fams = canon["typography"]["families"]

    P = B["slug"][:2].lower()
    A = B["accent"]
    S = B.get("surfaces", {})
    title = B["title"]
    lg = B.get("logo") or {}
    fg_on_accent = (B.get("color") or {}).get("accent", {}).get(
        "bright", {}).get("legal_foreground_when_used_as_fill", {}).get("color", "#000000")

    def w(rel, text):
        p = os.path.join(kit, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    # ---- tokens/colors.css
    colors = """/* {title} color tokens. GENERATED by gen_vanilla.py from brand.json. */
:root {{
  --{p}-accent: {acc};
  --{p}-accent-deep: {deep};
  --{p}-accent-accessible: {accessible};
  --{p}-dim: {dim};
  --{p}-orange: {orange};
  --{p}-orange-cta: {orange_cta};
  --{p}-fault: {fault};
  --{p}-fault-deep: {faultd};
  --{p}-void: {base};
  --{p}-surface: {card};
  --{p}-surface-sunken: {popover};
  --{p}-surface-raised: {secondary};
  --{p}-surface-hover: {hover};
  --{p}-line: {border};
  --{p}-text: #FFFFFF;
  --{p}-text-muted: {muted_dark};
  --{p}-light-surface: {light};
  --{p}-light-panel: #FFFFFF;
  --{p}-light-text: {gray950};
  --{p}-light-text-muted: {muted_light};
  --{p}-light-line: {gray200};
  --{p}-accent-10: rgb({acc_rgb} / 10%);
  --{p}-accent-20: rgb({acc_rgb} / 20%);
  --{p}-orange-12: rgb({or_rgb} / 12%);
  --{p}-fault-12: rgb({fa_rgb} / 12%);
  --{p}-bg: var(--{p}-void);
  --{p}-panel: var(--{p}-surface);
  --{p}-panel-raised: var(--{p}-surface-raised);
  --{p}-hover: var(--{p}-surface-hover);
  --{p}-border: var(--{p}-line);
  --{p}-fg: var(--{p}-text);
  --{p}-fg-muted: var(--{p}-text-muted);
  --{p}-link: var(--{p}-accent);
  --{p}-focus: var(--{p}-accent);
  --{p}-warning: var(--{p}-orange);
  --{p}-danger: var(--{p}-fault);
  --{p}-primary-foreground: {fgacc};
}}

.{p}-light {{
  --{p}-bg: var(--{p}-light-surface);
  --{p}-panel: var(--{p}-light-panel);
  --{p}-panel-raised: var(--{p}-light-panel);
  --{p}-hover: #F0EFED;
  --{p}-border: var(--{p}-light-line);
  --{p}-fg: var(--{p}-light-text);
  --{p}-fg-muted: var(--{p}-light-text-muted);
  --{p}-accent: var(--{p}-accent-accessible);
  --{p}-accent-deep: var(--{p}-accent-accessible);
  --{p}-link: var(--{p}-accent-accessible);
  --{p}-focus: var(--{p}-accent-accessible);
  --{p}-warning: var(--{p}-orange-cta);
  --{p}-danger: var(--{p}-fault-deep);
  --{p}-primary-foreground: #FFFFFF;
}}
""".format(title=title, p=P, acc=A["bright"], deep=A["deep"], accessible=A["accessible"],
           dim=A.get("dim", ramp["gray-400"]["hex"]), orange=imm["orange"]["hex"],
           orange_cta=imm["orange-cta"]["hex"], fault=imm["fault"]["hex"],
           faultd=imm["fault-deep"]["hex"], base=S.get("base", "#000000"),
           card=S.get("card", ramp["gray-950"]["hex"]), popover=S.get("popover", ramp["gray-950"]["hex"]),
           secondary=S.get("secondary", ramp["gray-900"]["hex"]), hover=S.get("hover", ramp["gray-800"]["hex"]),
           border=ramp["border-dark"]["hex"], muted_dark=ramp["gray-400"]["hex"],
           light=ramp["light-base"]["hex"], gray950=ramp["gray-950"]["hex"],
           muted_light=ramp["gray-600"]["hex"], gray200=ramp["gray-200"]["hex"],
           acc_rgb=rgb_parts(A["bright"]), or_rgb=rgb_parts(imm["orange"]["hex"]),
           fa_rgb=rgb_parts(imm["fault"]["hex"]), fgacc=fg_on_accent)
    w("tokens/colors.css", colors)

    # ---- tokens/typography.css
    ts = canon["typography"]["scale"]
    lines = [":root {"]
    for role, key in (("display", "display"), ("body", "body"), ("mono", "mono")):
        lines.append("  --%s-font-%s: %s;" % (P, role, fams[key]["stack"]))
    lines += ["  --%s-weight-regular: 400;" % P,
              "  --%s-weight-medium: 500;" % P,
              "  --%s-weight-bold: 700;" % P]
    for step, val in ts.get("display", {}).items():
        lines.append("  --%s-display-%s: %s;" % (P, step, val["size"]))
    for step, val in ts.get("body", {}).items():
        lines.append("  --%s-body-%s: %s;" % (P, step, val["size"]))
    lines.append("  --%s-tracking-display: %s;" % (P, ts["display"]["lg"]["tracking"]))
    for k, v in (canon["typography"].get("tracking") or {}).items():
        lines.append("  --%s-tracking-%s: %s;" % (P, k.replace("_label", ""), v))
    lines.append("  --%s-leading-display: %s;" % (P, ts["display"]["lg"]["line_height"]))
    lines.append("  --%s-leading-body: %s;" % (P, ts["body"]["md"]["line_height"]))
    lines.append("  --%s-leading-code: %s;" % (P, ts["body"]["sm"]["line_height"]))
    lines.append("}")
    w("tokens/typography.css", "\n".join(lines) + "\n")

    # ---- tokens/spacing.css
    sp = [":root {"]
    for i, px in enumerate(g["spacing"]["scale_px"], start=1):
        sp.append("  --%s-space-%d: %grem;" % (P, i, px / 16.0))
    for name, spec_ in g["radius"].items():
        if name == "base_variable":
            continue
        px = spec_["px"]
        sp.append("  --%s-radius-%s: %s;" % (P, "pill" if name == "full" else name,
                                             "9999px" if px >= 9999 else "%dpx" % px))
    sp += ["  --%s-stroke-hairline: 1px;" % P,
           "  --%s-stroke-icon: 1.5px;" % P,
           "  --%s-stroke-focus: 2px;" % P,
           "  --%s-motion-fast: 120ms;" % P,
           "  --%s-motion-normal: 180ms;" % P,
           "  --%s-motion-slow: 240ms;" % P,
           "  --%s-ease: %s;" % (P, canon["motion"]["approved_easing"][0]),
           "  --%s-content-max: %s;" % (P, g["layout"]["content_max"]),
           "  --%s-content-narrow: %s;" % (P, g["layout"]["narrow_max"]),
           "  --%s-clearspace-ratio: %.4f;" % (P, lg.get("clear_space_units", 100) / float(lg.get("grid", 1000))),
           "}"]
    w("tokens/spacing.css", "\n".join(sp) + "\n")

    # ---- tokens/base.css
    w("tokens/base.css", """*, *::before, *::after {{ box-sizing: border-box; }}
html {{ background: var(--{p}-bg); color: var(--{p}-fg); font-family: var(--{p}-font-body); font-size: var(--{p}-body-md); line-height: var(--{p}-leading-body); -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }}
body {{ margin: 0; }}
h1, h2, h3, h4 {{ margin: 0 0 var(--{p}-space-4); font-family: var(--{p}-font-display); font-weight: var(--{p}-weight-bold); letter-spacing: var(--{p}-tracking-display); line-height: var(--{p}-leading-display); }}
h1 {{ font-size: var(--{p}-display-md); }}
h2 {{ font-size: var(--{p}-display-sm); }}
h3 {{ font-size: var(--{p}-display-xs); font-weight: var(--{p}-weight-medium); }}
p {{ margin: 0 0 var(--{p}-space-4); }}
code, pre, kbd, samp {{ font-family: var(--{p}-font-mono); line-height: var(--{p}-leading-code); font-variant-ligatures: none; font-feature-settings: "liga" 0, "clig" 0, "calt" 0; }}
a {{ color: var(--{p}-link); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
:focus-visible {{ outline: var(--{p}-stroke-focus) solid var(--{p}-focus); outline-offset: 2px; }}
.{p}-eyebrow {{ color: var(--{p}-accent); font-family: var(--{p}-font-mono); font-size: var(--{p}-body-xs); letter-spacing: var(--{p}-tracking-eyebrow); text-transform: uppercase; }}
.{p}-endorsement {{ color: var(--{p}-fg-muted); font-family: var(--{p}-font-mono); font-size: var(--{p}-body-xs); letter-spacing: var(--{p}-tracking-eyebrow); text-transform: uppercase; }}
@media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; scroll-behavior: auto !important; }} }}
""".format(p=P))

    # ---- styles.css
    w("styles.css", "/* %s design system entry point. GENERATED by gen_vanilla.py. */\n"
                    '@import "./fonts/fonts.css";\n'
                    '@import "./tokens/colors.css";\n'
                    '@import "./tokens/typography.css";\n'
                    '@import "./tokens/spacing.css";\n'
                    '@import "./tokens/base.css";\n' % title)

    # ---- tokens/brand.tokens.json (W3C DTCG)
    dtcg = {
        "$schema": "https://design-tokens.github.io/community-group/format/",
        "meta": {"name": title, "version": B.get("version", "1.0.0"),
                 "parent": "ShruggieTech", "mode": "dark-first"},
        "color": {"$type": "color",
                  "identity": {"$value": A["bright"]},
                  "identityDeep": {"$value": A["deep"]},
                  "identityAccessible": {"$value": A["accessible"]},
                  "dim": {"$value": A.get("dim", ramp["gray-400"]["hex"])},
                  "background": {"$value": S.get("base", "#000000")},
                  "surface": {"$value": S.get("card", ramp["gray-950"]["hex"])},
                  "surfaceRaised": {"$value": S.get("secondary", ramp["gray-900"]["hex"])},
                  "border": {"$value": ramp["border-dark"]["hex"]},
                  "text": {"$value": "#FFFFFF"},
                  "textMuted": {"$value": ramp["gray-400"]["hex"]},
                  "emphasis": {"$value": imm["orange"]["hex"]},
                  "fault": {"$value": imm["fault"]["hex"]}},
        "fontFamily": {"$type": "fontFamily",
                       "display": {"$value": fams["display"]["name"]},
                       "body": {"$value": fams["body"]["name"]},
                       "mono": {"$value": fams["mono"]["name"]}},
        "dimension": {"$type": "dimension", **{
            "space%d" % i: {"$value": {"value": px, "unit": "px"}}
            for i, px in enumerate(g["spacing"]["scale_px"][:6], start=1)}, **{
            "radiusSmall": {"$value": {"value": 6, "unit": "px"}},
            "radiusControl": {"$value": {"value": 8, "unit": "px"}},
            "radiusPanel": {"$value": {"value": 12, "unit": "px"}}}},
        "logo": {"grid": {"$value": lg.get("grid", 1000)},
                 "outerRadius": {"$value": lg.get("outer_radius_units")},
                 "ring": {"$value": lg.get("inner_radius_units")},
                 "aperture": {"$value": lg.get("aperture_degrees")},
                 "slot": {"$value": lg.get("slot_degrees")},
                 "clearSpace": {"$value": lg.get("clear_space_units", 100)},
                 "reducedBelow": {"$value": lg.get("reduced_below_px", 32)}},
    }
    with open(os.path.join(kit, "tokens", "brand.tokens.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(dtcg, f, indent=2, ensure_ascii=False); f.write("\n")

    emit_components(kit, P, B, w)
    print("wrote %s and %s" % (os.path.join(kit, "tokens"), os.path.join(kit, "components")))


if __name__ == "__main__":
    sys.exit(main())
