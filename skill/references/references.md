# References

This library supports decisions in the [BrandBuilder manual](10-system-architecture.md). It is a curated external-source bibliography, not the specification of a delivered brand kit. A cited standard becomes a project requirement only where the local manual or constitution adopts it. Design systems and heuristics are advisory examples. Follow the delivered kit's own versioned facts for implementation. Links were reviewed on 2026-09-27; an external outage does not invalidate the local explanation.

## Brand strategy and human-centered design

### REF-UX-NIELSEN

**Source:** Nielsen Norman Group, [10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/). **Class:** Advisory usability framework. **Use:** Review whether a proposed control communicates status, gives a predictable result, and helps recover from mistakes. Apply in [interface recipes](11-interface-implementation.md) and [discovery](03-interview.md). **Limit:** A heuristic review is not WCAG conformance or user research.

### REF-UX-SHNEIDERMAN

**Source:** Ben Shneiderman, [The Eight Golden Rules of Interface Design](https://www.cs.umd.edu/users/ben/goldenrules.html). **Class:** Advisory usability framework. **Use:** Check consistency, feedback, user control, and reversible actions in a component recipe. Apply in [interface implementation](11-interface-implementation.md). **Limit:** Adapt to the actual task and host conventions.

### REF-UX-NORMAN

**Source:** Don Norman, [The Design of Everyday Things, revised and expanded edition](https://jnd.org/books/the-design-of-everyday-things-revised-and-expanded-edition/). **Class:** Further reading, publisher/author book description. **Use:** Ask during [discovery](03-interview.md) what a user expects an action to do and which visible cues help them find it. **Limit:** The linked book page supports bibliographic identity; no unreviewed passage is treated as a project rule.

### REF-UX-UXDI

**Source:** UX Design Institute, [Seven UX Design Principles](https://www.uxdesigninstitute.com/blog/ux-design-principles-2026/). **Class:** Educational synthesis. **Use:** Orient a new reader to broad interaction questions before using the specific standards and framework references below. **Limit:** The page title signals a 2026 update while displayed publication metadata says 10 September 2024; technical requirements must be traced to primary sources.

### REF-BRAND-KELLER

**Source:** Kevin Lane Keller, [Conceptualizing, Measuring, and Managing Customer-Based Brand Equity](https://journals.sagepub.com/doi/10.1177/002224299305700101), 1993. **Class:** Research, abstract/bibliographic record. **Use:** In [discovery](03-interview.md), separate evidence about audience awareness and associations from the team's desired positioning. **Limit:** The complete paper was not reviewed here; do not attribute an exact method or result beyond its accessible record.

### REF-BRAND-KAPFERER

**Source:** Jean-Noël Kapferer, [The New Strategic Brand Management](https://www.koganpage.com/marketing-communications/the-new-strategic-brand-management-9780749465155), fifth edition, 2012. **Class:** Further reading, publisher record. **Use:** Consider the publisher-described Brand Identity Prism as one prompt for examining identity dimensions in [discovery](03-interview.md). **Limit:** Validate any detailed framework claim against the actual edition and passage before adopting it.

### REF-BRAND-DISTINCTIVE

**Source:** Ehrenberg-Bass Institute, [Brands of Distinction](https://marketingscience.info/news-and-insights/brands-of-distinction). **Class:** Advisory brand research. **Use:** Document what an audience already recognizes before changing a supplied mark in the [logo protocol](06-logo-protocol.md). **Limit:** Distinctive-asset research does not require related brands to use separate formal hue families or authorize redrawing approved geometry.

## Accessibility, semantics, and content

### REF-A11Y-WCAG21

**Source:** W3C WAI, [Web Content Accessibility Guidelines 2.1](https://www.w3.org/TR/WCAG21/). **Class:** Normative standard, adopted by this repository at Level AA. **Use:** Apply the applicable success criteria to generated and hosted surfaces in [verification](12-verification-versioning.md). **Limit:** The Understanding pages below are informative explanations; a local test of one criterion is not complete conformance.

### REF-A11Y-COLOR

**Source:** W3C WAI, [Understanding Use of Color](https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html). **Class:** Informative WCAG explanation. **Use:** Pair color-coded status or brand cues with text, shape, or another perceivable signal in [interface implementation](11-interface-implementation.md). **Limit:** Check the referenced normative success criterion for the actual obligation.

### REF-A11Y-CONTRAST

**Source:** W3C WAI, [Understanding Contrast (Minimum)](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum). **Class:** Informative WCAG explanation. **Use:** Measure text against its rendered background as required by the local AA gate in [verification](12-verification-versioning.md). **Limit:** Asset palette names or nominal token values alone do not prove rendered contrast.

### REF-A11Y-NONTEXT

**Source:** W3C WAI, [Understanding Non-text Contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast). **Class:** Informative WCAG explanation. **Use:** Check visible boundaries and state cues of controls and informative graphics in [component recipes](11-interface-implementation.md). **Limit:** Apply the criterion's scope and exceptions to the actual component.

### REF-A11Y-KEYBOARD

**Source:** W3C WAI, [Understanding Keyboard](https://www.w3.org/WAI/WCAG21/Understanding/keyboard). **Class:** Informative WCAG explanation. **Use:** Exercise links, menus, and controls without a pointer in [verification](12-verification-versioning.md). **Limit:** A keyboard path alone does not establish meaningful focus order or visible focus.

### REF-A11Y-FOCUS

**Source:** W3C WAI, [Understanding Focus Visible](https://www.w3.org/WAI/WCAG21/Understanding/focus-visible). **Class:** Informative WCAG explanation. **Use:** Inspect visible focus on the rendered hosted guide and component examples. **Limit:** Verify the actual state, including against brand backgrounds.

### REF-A11Y-HEADINGS

**Source:** W3C WAI, [Understanding Headings and Labels](https://www.w3.org/WAI/WCAG21/Understanding/headings-and-labels). **Class:** Informative WCAG explanation. **Use:** Give each guideline section a heading that describes its content and each control a meaningful label. **Limit:** A heading hierarchy is also a reader-navigation design decision, not a substitute for all other criteria.

### REF-A11Y-REFLOW

**Source:** W3C WAI, [Understanding Reflow](https://www.w3.org/WAI/WCAG21/Understanding/reflow). **Class:** Informative WCAG explanation. **Use:** Inspect guideline versions, definitions, and resources at narrow width and 200% zoom. **Limit:** Apply the criterion's content exceptions only where actually relevant.

### REF-A11Y-WRITING

**Source:** W3C WAI, [Writing for Web Accessibility](https://www.w3.org/WAI/tips/writing/). **Class:** Informative authoring guidance. **Use:** Write descriptive links, headings, and instructions in [the manual](10-system-architecture.md) and generated topics. **Limit:** This checklist supplements the normative WCAG criteria.

### REF-A11Y-APG

**Source:** W3C WAI, [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/). **Class:** Informative component patterns. **Use:** Compare keyboard and semantic behavior for a web widget in [interface implementation](11-interface-implementation.md). **Limit:** Prefer native elements where they fit; a pattern example is not proof that an implementation passes WCAG.

### REF-DOC-DIATAXIS

**Source:** Diátaxis, [Documentation framework](https://diataxis.fr/). **Class:** Advisory content organization. **Use:** Decide whether a page teaches, guides a task, explains a concept, or supplies a reference before adding content to [the documentation system](10-system-architecture.md). **Limit:** It does not replace local publication or version contracts.

## Interface systems and web foundations

### REF-UI-CARBON

**Source:** IBM, [Carbon color overview](https://carbondesignsystem.com/elements/color/overview/). **Class:** Advisory design-system example. **Use:** Distinguish formal brand colors from semantic interface cues when writing [color roles](00-variance-contract.md). **Limit:** Carbon's palette is not BrandBuilder canon and does not authorize recoloring a brand mark.

### REF-UI-APPLE

**Source:** Apple, [Human Interface Guidelines design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles). **Class:** Platform guidance. **Use:** Review an Apple-hosted surface against current platform expectations in [portability](09-portability.md). **Limit:** The linked page exposes limited text to this audit; do not claim detailed requirements absent from the page or from a pinned platform edition.

### REF-UI-FLUENT

**Source:** Microsoft, [Fluent UI](https://developer.microsoft.com/en-us/fluentui). **Class:** Advisory platform design-system portal. **Use:** Compare host control conventions when planning a Windows interface in [portability](09-portability.md). **Limit:** Its tokens are not this repository's brand palette.

### REF-UI-FLUENT2

**Source:** Microsoft, [Fluent 2](https://fluent2.microsoft.design/). **Class:** Advisory design-system guidance. **Use:** Check state, layout, and component language for a Fluent host. **Limit:** Match the host's actual Fluent edition and library before coding.

### REF-UI-FLUENT-ANDROID

**Source:** Microsoft, [Fluent UI Android](https://github.com/microsoft/fluentui-android#readme). **Class:** External component implementation. **Use:** Compare an Android host's chosen library with its own theme contract. **Limit:** BrandBuilder does not generate a Fluent Android adapter.

### REF-WEB-HTML

**Source:** WHATWG, [HTML semantics](https://html.spec.whatwg.org/multipage/semantics.html). **Class:** Living standard. **Use:** Choose native headings, sections, links, buttons, and lists before adding custom roles in [interface implementation](11-interface-implementation.md). **Limit:** Inspect the current standard and the target host behavior for a specific element.

### REF-WEB-ID

**Source:** WHATWG, [The `id` attribute](https://html.spec.whatwg.org/multipage/dom.html#the-id-attribute). **Class:** Living standard. **Use:** Keep document IDs unique for guideline anchors, and use repeatable classes for shared styling. **Limit:** A valid ID does not make the linked heading useful by itself.

### REF-WEB-SPECIFICITY

**Source:** W3C, [Selectors Level 4 specificity](https://www.w3.org/TR/selectors-4/#specificity-rules). **Class:** CSS specification. **Use:** Review selector precedence before overriding generated tokens in [the web binding](05-shadcn-binding.md). **Limit:** Check actual cascade layers and origin as well as specificity.

### REF-WEB-VARIABLES

**Source:** MDN, [Using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties). **Class:** Implementation explanation. **Use:** Trace inherited semantic tokens and deliberate local overrides in [interface implementation](11-interface-implementation.md). **Limit:** The CSS specifications and browser behavior govern the feature.

### REF-WEB-NEXT

**Source:** Vercel, [Next.js accessibility](https://nextjs.org/docs/architecture/accessibility). **Class:** Framework guidance. **Use:** Check route titles, focus, and link navigation in this static site's [toolchain](04-toolchain.md). **Limit:** Match the repository's installed Next.js version and verify the exported result.

### REF-WEB-REACT

**Source:** React, [Providing a label for an input](https://react.dev/reference/react-dom/components/input#providing-a-label-for-an-input). **Class:** Framework guidance. **Use:** Connect visible input labels to controls in [interface recipes](11-interface-implementation.md). **Limit:** The form still needs task-specific validation and error wording.

### REF-WEB-RADIX

**Source:** Radix, [Accessibility overview](https://www.radix-ui.com/primitives/docs/overview/accessibility). **Class:** Component-library guidance. **Use:** Review primitive keyboard and accessible-name behavior when composing a [web recipe](11-interface-implementation.md). **Limit:** Consumer composition and styling remain the host's responsibility.

### REF-WEB-SHADCN

**Source:** shadcn/ui, [Theming](https://ui.shadcn.com/docs/theming). **Class:** Implementation guide. **Use:** Map generated semantic variables to the supported [registry binding](05-shadcn-binding.md). **Limit:** Use the consumer's pinned shadcn contract, not an assumed latest CLI or registry behavior.

### REF-WEB-TAILWIND

**Source:** Tailwind CSS, [Hover, focus, and other states](https://tailwindcss.com/docs/hover-focus-and-other-states). **Class:** Framework guidance. **Use:** Express focus and preference states without hiding meaning behind color alone in [interface recipes](11-interface-implementation.md). **Limit:** Match the installed Tailwind version and inspect actual output.

### REF-WEB-FUMADOCS

**Source:** Fumadocs, [Fumadocs UI](https://www.fumadocs.dev/docs/ui). **Class:** Documentation-framework guidance. **Use:** Check this site's manual navigation, TOC, and search in [the documentation system](10-system-architecture.md). **Limit:** The generated MDX and browser result remain the local acceptance evidence.

## Android and platform identity assets

### REF-ANDROID-MOBILE

**Source:** Android Developers, [Mobile design](https://developer.android.com/design/ui/mobile). **Class:** Platform guidance. **Use:** Begin host planning for navigation, content hierarchy, input, and scalable reading across device sizes. **Limit:** The current kit supplies Android assets, not a Compose interface adapter.

### REF-ANDROID-COMPONENTS

**Source:** Android Developers, [Material components](https://developer.android.com/design/ui/mobile/guides/components/material-overview). **Class:** Platform design guidance. **Use:** Select host controls by task and state when integrating [portable assets](09-portability.md). **Limit:** Material styling does not replace the brand's formal palette or imply generated Compose components.

### REF-ANDROID-LAYOUT

**Source:** Android Developers, [Adapt layout and content](https://developer.android.com/design/ui/mobile/guides/layout-and-content/adapt-layout). **Class:** Platform guidance. **Use:** Test hierarchy and readable content in a resizable Android window. **Limit:** The Android host owns layout implementation and validation.

### REF-ANDROID-BARS

**Source:** Android Developers, [System bars](https://developer.android.com/design/ui/mobile/guides/foundations/system-bars). **Class:** Platform guidance. **Use:** Plan contrast and insets around host chrome. **Limit:** Host and OS version determine effective bar behavior.

### REF-ANDROID-ACCESS

**Source:** Android Developers, [Accessibility in Jetpack Compose](https://developer.android.com/develop/ui/compose/accessibility). **Class:** Platform implementation guidance. **Use:** Give host controls meaningful semantics and test focus and scalable text. **Limit:** This repository does not generate a Compose adapter.

### REF-ANDROID-M3

**Source:** Android Developers, [Material 3 in Compose](https://developer.android.com/develop/ui/compose/designsystems/material3). **Class:** Platform implementation guidance. **Use:** Compare semantic roles with a host's Material 3 theme. **Limit:** Dynamic interface colors do not alter approved logo geometry or formal brand colors.

### REF-ANDROID-CUSTOM

**Source:** Android Developers, [Custom design systems in Compose](https://developer.android.com/develop/ui/compose/designsystems/custom). **Class:** Platform implementation guidance. **Use:** Define an explicit mapping from kit tokens to a custom host theme when needed. **Limit:** Such mapping is host work until a generated adapter is shipped.

### REF-ANDROID-INSETS

**Source:** Android Developers, [Window insets in Compose](https://developer.android.com/develop/ui/compose/system/insets). **Class:** Platform implementation guidance. **Use:** Keep content clear of system UI in a Compose host. **Limit:** Validate on the actual target OS and window configuration.

### REF-ANDROID-ADAPTIVE-ICON

**Source:** Android Developers, [Adaptive icon design](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive). **Class:** Platform asset guidance. **Use:** Choose the kit's launcher foreground/background and monochrome roles in [the toolchain](04-toolchain.md). **Limit:** Launcher layers and store listing images have separate uses.

### REF-ANDROID-PLAY-ICON

**Source:** Android Developers, [Google Play icon specifications](https://developer.android.com/distribute/google-play/resources/icon-design-specifications). **Class:** Distribution asset guidance. **Use:** Check the store listing image separately from the installed launcher icon. **Limit:** Validate the current Play publishing requirements when releasing an app.

### REF-APPLE-APP-ICON

**Source:** Apple, [App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons). **Class:** Platform asset guidance. **Use:** Select the appropriate kit export for an Apple app in [the toolchain](04-toolchain.md). **Limit:** Xcode and platform editions determine final packaging.

### REF-APPLE-XCODE-ICON

**Source:** Apple, [Configuring your app icon](https://developer.apple.com/documentation/xcode/configuring-your-app-icon). **Class:** Platform implementation guidance. **Use:** Verify the app asset catalog configuration after importing the kit image. **Limit:** A correct source PNG does not prove host configuration.

### REF-WINDOWS-ICON

**Source:** Microsoft, [App icon construction](https://learn.microsoft.com/en-us/windows/apps/design/iconography/app-icon-construction). **Class:** Platform asset guidance. **Use:** Compare the supplied Windows icon roles and sizes with app packaging needs. **Limit:** This canonical URL replaces an older redirected iconography path retained in historical research.

### REF-WINDOWS-ICON-DESIGN

**Source:** Microsoft, [App icon design](https://learn.microsoft.com/en-us/windows/apps/design/iconography/app-icon-design). **Class:** Platform asset guidance. **Use:** Review visual fit for a Windows host without editing approved source geometry. **Limit:** Host packaging and rendered appearance require their own checks.

### REF-WEB-MANIFEST

**Source:** W3C, [Web Application Manifest](https://www.w3.org/TR/appmanifest/). **Class:** Web specification. **Use:** Check declared icon roles and start URL in [the toolchain](04-toolchain.md). **Limit:** A valid manifest does not prove installed-browser rendering.

### REF-WEB-MASKABLE

**Source:** web.dev, [Maskable icons](https://web.dev/articles/maskable-icon). **Class:** Browser implementation guidance. **Use:** Preview the maskable icon safe region before release. **Limit:** Inspect actual platform masks as well as source dimensions.

## WordPress authoring and integration

The entries in this collection guide future native adapter and starter work. BrandBuilder does not currently ship either WordPress deliverable; [interface implementation](11-interface-implementation.md) identifies the present handoff boundary.

### REF-WP-GLOBAL

**Source:** WordPress Developer Resources, [Global Settings and Styles](https://developer.wordpress.org/themes/global-settings-and-styles/). **Class:** Platform theme guidance. **Use:** Map brand tokens to native `theme.json` settings and styles in a future adapter. **Limit:** Pin the target WordPress core and schema version.

### REF-WP-HIERARCHY

**Source:** WordPress Developer Resources, [Global Settings and Styles core concepts](https://developer.wordpress.org/themes/core-concepts/global-settings-and-styles/). **Class:** Platform theme guidance. **Use:** Test effective styling across core, theme, child theme, and saved user settings. **Limit:** Do not treat a generated theme value as final when a later layer overrides it.

### REF-WP-FORMAT

**Source:** WordPress Developer Resources, [Versioned `theme.json` format](https://developer.wordpress.org/block-editor/how-to-guides/themes/global-settings-and-styles/). **Class:** Platform format guidance. **Use:** Choose a schema supported by the target core release before generating a theme. **Limit:** The documentation records version 3 from WordPress 6.6; verify the selected host version rather than assuming the latest schema.

### REF-WP-CUSTOM

**Source:** WordPress Developer Resources, [Custom settings](https://developer.wordpress.org/themes/global-settings-and-styles/settings/custom/). **Class:** Platform implementation guidance. **Use:** Separate custom brand tokens from native presets when designing a future mapping. **Limit:** Host consumers must actually read a custom property for it to affect UI.

### REF-WP-COLOR

**Source:** WordPress Developer Resources, [Color settings](https://developer.wordpress.org/themes/global-settings-and-styles/settings/color/). **Class:** Platform implementation guidance. **Use:** Map approved palette roles to editor-visible color presets and test effective front-end output. **Limit:** Presets do not waive rendered contrast checks.

### REF-WP-TYPE

**Source:** WordPress Developer Resources, [Typography settings and font faces](https://developer.wordpress.org/themes/global-settings-and-styles/settings/typography/). **Class:** Platform implementation guidance. **Use:** Plan licensed font files and native typography controls for a future theme. **Limit:** Check font rights, loading, and actual rendered text.

### REF-WP-EDITOR-ASSETS

**Source:** WordPress Developer Resources, [Loading editor assets](https://developer.wordpress.org/block-editor/how-to-guides/enqueueing-assets-in-the-editor/). **Class:** Platform implementation guidance. **Use:** Test editor and front-end asset loading separately. **Limit:** A front-end stylesheet does not establish editor parity.

### REF-WP-BLOCK-CSS

**Source:** WordPress Developer Resources, [Block stylesheets](https://developer.wordpress.org/themes/features/block-stylesheets/). **Class:** Platform implementation guidance. **Use:** Associate component CSS with native blocks in a future adapter. **Limit:** Verify load context and supported core version.

### REF-WP-VARIATIONS

**Source:** WordPress Developer Resources, [Block style variations](https://developer.wordpress.org/themes/features/block-style-variations/). **Class:** Platform authoring guidance. **Use:** Offer legitimate component variations to an editor without flattening all brand rules into one style. **Limit:** The future adapter must define which variants it actually ships.

### REF-WP-STRUCTURE

**Source:** WordPress Developer Resources, [Theme structure](https://developer.wordpress.org/themes/core-concepts/theme-structure/). **Class:** Platform implementation guidance. **Use:** Place future templates, styles, and parts in supported native locations. **Limit:** A reference to theme structure is not an installable theme artifact.

### REF-WP-PATTERNS

**Source:** WordPress Developer Resources, [Patterns](https://developer.wordpress.org/themes/patterns/). **Class:** Platform authoring guidance. **Use:** Plan reusable native content compositions for a future starter. **Limit:** Keep sample content distinct from editable user content.

### REF-WP-CURATION

**Source:** WordPress Developer Resources, [Curating the editor experience](https://developer.wordpress.org/block-editor/how-to-guides/curating-the-editor-experience/). **Class:** Platform authoring guidance. **Use:** Decide which editor controls a supported theme should expose for its use case. **Limit:** Do not impose restrictions without an owner-approved product requirement.

### REF-WP-CHILD

**Source:** WordPress Developer Resources, [Child themes](https://developer.wordpress.org/themes/advanced-topics/child-themes/). **Class:** Platform customization guidance. **Use:** Preserve client changes outside a parent theme when planning a future handoff. **Limit:** Test the actual parent/child override order.

### REF-WP-ENV

**Source:** WordPress Developer Resources, [`wp-env`](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-env/). **Class:** Platform testing tool. **Use:** Reproduce editor and front-end checks against a pinned WordPress environment. **Limit:** Local test success is evidence for the tested version and configuration only.

## Native egui implementation

### REF-EGUI-PROJECT

**Source:** egui maintainers, [egui project](https://github.com/emilk/egui). **Class:** Framework reference. **Use:** Understand the immediate-mode host model before mapping [component recipes](11-interface-implementation.md). **Limit:** Match the exact adapter pin when implementing.

### REF-EGUI-ARCHITECTURE

**Source:** egui maintainers, [egui architecture](https://github.com/emilk/egui/blob/main/ARCHITECTURE.md). **Class:** Framework design explanation. **Use:** Trace input, state, and paint responsibilities in a native host. **Limit:** The linked `main` branch may differ from the delivered adapter's version.

### REF-EGUI-ACCESS

**Source:** egui maintainers, [Accessibility guide](https://github.com/emilk/egui/blob/main/docs/accessibility.md). **Class:** Framework implementation guidance. **Use:** Review accessible names, focus, and platform bridge when consuming generated native tokens. **Limit:** AccessKit exposure depends on the host integration and platform; the adapter cannot prove it alone.

### REF-EGUI-TEST

**Source:** docs.rs, [egui_kittest 0.36.1](https://docs.rs/egui_kittest/0.36.1/egui_kittest/). **Class:** Version-pinned test API. **Use:** Exercise native component state and interaction at the adapter's pin. **Limit:** Rendering and assistive-technology behavior still need host evidence.

### REF-EGUI-VERSION

**Source:** crates.io, [egui 0.36.1](https://crates.io/crates/egui/0.36.1). **Class:** Version-pinned package record. **Use:** Check compatibility for the delivered native adapter in [interface implementation](11-interface-implementation.md). **Limit:** Do not infer later API behavior from this record.

## Maintaining this library

Add a source when it helps a concrete reader decision. Assign a new `REF-*` ID and never silently reuse an old one for a different work. Record issuing body, accurate title, URL, edition or version where known, class, use, local application, and limit. Check the source and its local citations, then run the reference validator and publication build. If a URL moves, retain the ID and record the canonical replacement; if a work is superseded, preserve the old edition's meaning and add a new entry when needed. Review external reachability separately from local ID and package validity. Do not copy substantial third-party content into this library.
