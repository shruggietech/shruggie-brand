# Research: Site Shell and Homepage Stabilization

## Decision 1: Treat scrollbar allocation as shared document infrastructure

**Decision**: Apply `scrollbar-gutter: stable` to the document root so pages with different heights reserve the same inline scrollbar space.

**Rationale**: Issues #176 and #178 both describe small route-dependent horizontal movement and explicitly identify differing scrollbar presence as a likely cause. The homepage uses a centered 1180px shell, while the shared Fumadocs layouts also center within the viewport. Reserving the gutter at the root addresses both systems without route-specific compensation.

**Alternatives rejected**: Per-route padding, transforms, negative margins, and fixed pixel offsets would encode current browser geometry and violate both issue contracts.

## Decision 2: Retain Fumadocs' built-in right-rail reservation

**Decision**: Preserve and verify the Fumadocs desktop TOC placeholder contract, then add an owned desktop layout variable rule only if measurements show the track is not consistently reserved.

**Rationale**: Fumadocs 16.14.3 emits `#nd-toc-placeholder` for pages with no TOC items and sets the same 268px layout variable as `#nd-toc` at the `xl` breakpoint. Its main article is already capped at 900px and centered inside the main grid area. The first correction should therefore be the shared scrollbar gutter, backed by measurements, instead of overriding a stable library grid.

**Alternatives rejected**: Absolutely positioning the TOC would duplicate framework behavior. Forking page slots would add maintenance risk. Disabling the TOC would fail the usability requirement.

## Decision 3: Keep canonical navigation policy in `baseOptions()`

**Decision**: Add Company and Download Skill to the existing shared Fumadocs link records, with `external: true`, and keep Documentation conditional so docs pages do not repeat their current root destination.

**Rationale**: HomeLayout and DocsLayout already consume the same base options. Fumadocs supplies desktop and mobile rendering plus external-link semantics from those records.

**Alternatives rejected**: Separate header implementations could drift. Adding raw anchors to individual layouts would miss mobile navigation and subpages.

## Decision 4: Preserve the footer's surface-specific Company behavior

**Decision**: Remove Brands, rename Download Skill, and retain Company as same-tab in the footer. Header Company and Download Skill remain safe external navigation links.

**Rationale**: S022 deliberately locked Company to same-tab in the footer while requiring Download Skill, Source, and License to open separately. Issue #177 explicitly says to retain #163 behavior for those three footer destinations, so its general external-navigation wording does not supersede the approved footer-specific record.

**Alternatives rejected**: Changing footer Company to new-tab would regress S022 and contradict its existing negative contract test.

## Decision 5: Verify semantic and geometric behavior at two layers

**Decision**: Use Node source-policy tests for exact records and Playwright checks for rendered navigation, hero states, bounding boxes, overflow, themes, breakpoints, and scale emulation.

**Rationale**: Source tests prevent regeneration regressions. Browser measurements prove computed layout rather than assuming CSS declarations are sufficient.

**Alternatives rejected**: Screenshots alone are imprecise and brittle. Source inspection alone cannot detect computed drift, mobile menus, or accessibility failures.

## Decision 6: Keep the removed callout absent from source

**Decision**: Delete the callout JSX and its now-unused CSS selectors.

**Rationale**: Issue #172 prohibits CSS hiding and reserved space. Removing both authoritative markup and dead styles yields the clearest regeneration contract.

**Alternatives rejected**: `display: none` or conditional flags would retain obsolete content and permit accidental restoration.
