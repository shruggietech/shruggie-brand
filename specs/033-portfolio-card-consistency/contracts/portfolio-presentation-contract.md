# Contract: Homepage Portfolio Presentation

## Card contract

- Every production portfolio entry appears once as a desktop article and once as a mobile native disclosure.
- Every visible title, descriptor, and action label computes to `rgb(255, 255, 255)`.
- A governed surface is retained only when its generated legal foreground is `#FFFFFF`; all other entries use the accent-derived dark fallback.
- I Heart PR Tours uses the approved color heart icon and the shared dark fallback, not its white guideline surface.
- Approved icon source files, geometry, colors, proportions, and transparency remain unchanged.
- Visible description or action content retains at least 16 CSS pixels of clearance from the card's bottom border.

## Action contract

- Each entry exposes exactly `Guidelines` and `Download Kit` with the generated explicit destinations and download filename.
- A desktop card at rest shows its description and makes action anchors invisible and non-focusable.
- Pointer hover or keyboard focus on the card reveals both actions without changing card or grid geometry.
- Action labels remain white in resting, hover, active, and focus-visible states.
- Action text contrast is at least 4.5:1 and the focus indicator maintains at least 3:1 contrast against adjacent colors.
- Every action target measures at least 44 by 44 CSS pixels.
- Escape dismisses revealed actions, restores the description, and returns focus to the card.
- Pointer exit resets ordinary hover presentation. After Escape returns focus to the card, dismissal remains in force until focus exits or the pointer enters again, so incidental pointer movement cannot immediately reopen the actions.
- Reduced-motion preferences remove motion without removing state or focus cues.
- Mobile disclosures retain native open/closed semantics and do not expose closed-panel actions.

## Third-party notice contract

- A marker appears if and only if the entry has a non-empty generated vendor boundary.
- Every marker includes an accessible text equivalent and references `portfolio-third-party-notice`.
- If one or more markers exist, exactly one element with that ID is rendered.
- The element contains exactly one paragraph whose visible text is `* Third-party projects are independently owned and operated.`
- Adding another applicable entry does not change the paragraph count or text.
- If no markers exist, the notice element is absent.
- Detailed vendor-boundary strings do not appear in the homepage notice and remain unchanged on guideline routes, structured data, and metadata.

## Responsive and accessibility contract

- Desktop, representative narrow desktop, mobile, and 200 percent zoom layouts contain no clipped or overlapping portfolio content.
- Revealing actions changes no measured card width, height, or grid position by more than 0.5 CSS pixels.
- Keyboard-only and pointer users can reach both actions for every entry.
- The affected homepage produces zero WCAG 2.1 AA violations in the repository's browser audit.

## Failure contract

Verification fails when any visible card copy is not white, a light showcase surface reaches the homepage, action contrast or focus falls below the declared floor, a hidden action remains focusable, content loses bottom clearance, reveal changes geometry, the notice is missing, duplicated, or expanded, a marker loses its association, an explicit destination drifts, or detailed vendor metadata changes.
