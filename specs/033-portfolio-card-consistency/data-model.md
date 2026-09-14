# Data Model: Portfolio Card Consistency

## Portfolio entry

| Field | Meaning | Validation |
| --- | --- | --- |
| `slug` | Stable public brand identifier | Existing generated value; never used as a visual-policy exception |
| `title` | Visible portfolio name | Rendered as white text; receives a marker only when a vendor boundary exists |
| `descriptor` | Visible portfolio description | Rendered in full as white text with positive bottom clearance |
| `accent` | Brand-specific emphasis color | Retained for borders, rings, and the dark fallback gradient |
| `icon` | Approved generated icon URL | Existing source and geometry remain unchanged |
| `guidelinesPath` | Explicit Guidelines destination | Retained exactly and exposed only through the named action |
| `kitArchive` | Explicit kit download destination | Retained exactly with its download filename |
| `showcaseSurface` | Optional generated showcase surface | Used on the homepage only when the legal foreground is white |
| `showcaseForeground` | Generated legal foreground for the showcase surface | `#FFFFFF` makes a governed surface eligible for the dark homepage family; any other value selects the fallback |
| `vendorBoundary` | Optional detailed affiliation/provenance wording | Used only as the applicability signal on the homepage; full wording remains on detailed routes and metadata |

## Portfolio presentation

| Property | Contract |
| --- | --- |
| Surface | Governed dark surface when paired with white, otherwise accent-derived dark fallback |
| Visible text | Exact white for titles, descriptions, mobile copy, and action labels |
| Icon well | Existing dark neutral well with approved icon contained and centered |
| Desktop geometry | Fixed size with reserved action stage and positive lower content clearance |
| Mobile geometry | Native disclosure with contained content, positive panel padding, and no horizontal clipping |

## Desktop action state

| State | Description visibility | Action visibility/focusability | Transition |
| --- | --- | --- | --- |
| Resting | Visible | Hidden and not focusable | Card focus or pointer hover reveals |
| Revealed | Hidden | Visible and focusable | Pointer exit or focus exit restores resting |
| Action focused | Hidden | Visible with dual focus indicator | Tab advances between actions or out of card |
| Dismissed | Visible | Hidden and not focusable | Escape returns focus to card; focus exit or pointer re-entry resets dismissal |
| Reduced motion | Same state semantics | Same focus semantics | Motion transforms and animated transitions are removed |

## Mobile disclosure state

| State | Summary | Panel | Actions |
| --- | --- | --- | --- |
| Closed | Visible, white, keyboard operable | Hidden by native disclosure semantics | Hidden and not focusable |
| Open | Visible with expanded cue | Visible with white description | Visible, white, and keyboard operable |

## Third-party disclosure

| Entity | Rule |
| --- | --- |
| Applicability | A portfolio entry is marked when `vendorBoundary` is non-empty |
| Marker | Visible asterisk, accessible equivalent, and `aria-describedby` reference to the shared notice |
| Notice presence | One notice when any applicable entry exists; none otherwise |
| Notice copy | `* Third-party projects are independently owned and operated.` |
| Detailed wording | Retained unchanged outside the homepage summary |

## Relationships

- Every portfolio entry has exactly two explicit actions.
- Zero or more portfolio entries may reference the one shared third-party notice.
- The shared notice never contains or aggregates detailed vendor-boundary strings.
- Homepage presentation is derived from generated content but does not modify generated records or brand-specific route presentation.
