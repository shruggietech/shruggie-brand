# Contract: Shared Site Shell and Homepage

## Homepage contract

The hero exposes, in DOM order, `Documentation` at `/docs`, `Download Skill` at the canonical latest-release URL, and `Explore Our Portfolio` at `#portfolio`. The first action uses the generated CTA background token. The latter two use the generated accessible green token. The portfolio cue is `aria-hidden` and the supporting link has deliberate margin from the button row.

The portfolio section retains `id="portfolio"`, uses exact heading `Our Portfolio`, and contains the phrase `identity spectrum` in its adjacent description. `The system underneath`, its copy, its buttons, its wrapper, and `.system-callout` styles are absent.

## Shared navigation contract

Main-site navigation includes Documentation, Company, Download Skill, and View on GitHub. Docs navigation omits only Documentation. Company and Download Skill use their canonical HTTPS destinations and render with safe external-link behavior in desktop and mobile navigation.

## Shared footer contract

The ordered footer records are Documentation, Download Skill, Company, Source, and License. Brands and `Download the skill` are invalid. Download Skill, Source, and License use `target="_blank"` with `rel="noopener noreferrer"`. Company has neither attribute and remains same-tab.

## Layout stability contract

At identical desktop conditions, compare the shared navigation header, visible logo, and visible menu region on `/` and every retained brand download route. At identical docs conditions, compare `#nd-docs-layout` and `.docs-page` on `/docs/`, a page with a visible desktop TOC, and a page without TOC items. Each left edge, right edge, width, and center required by the specification has a one CSS-pixel tolerance.

Exercise light and dark themes, 1280px and narrow 360px widths, short and tall content, and browser contexts with device scale factors 1 and 2. Assert `scrollWidth <= clientWidth + 1` for every measured route. Desktop TOC pages retain a visible sticky `#nd-toc`; pages without items retain equivalent right-track allocation. Narrow routes expose no desktop rail and no hidden or clipped article content.

The short-to-tall case must assert that the natural homepage exceeds the viewport, create a controlled header-only state that does not exceed the viewport, and compare the same header and visible navigation-control boxes across those two proven scrollbar states.

## Isolation contract

Neutral `/<brand-slug>/guidelines/` routes must not render `.site-footer`, `.header-logo`, or the shared ShruggieTech promotional Company and Download Skill navigation.
