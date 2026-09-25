# Data Model: S053

## Brand source

`color_roles.identity[]` has `id`, `label`, `source`, and `use`. `source` is a restricted reference into approved brand source (`accent.*`, `logo.role_colors.color.*`, legacy approved palette indices, or explicitly selected `semantic_colors.*`). Duplicate IDs, unresolved paths, non-hex targets, and empty usage fail. `color_roles.combinations[]` names an approved combination of formal IDs, its intended use, and its `logo.full`, `logo.reduced`, or `brand.applications` artwork reference. Unknown formal IDs and duplicate combination IDs fail.

`color_roles.interface_overrides` is an optional mapping from a declared cue role to dark/light source references. It changes only the role mapping, never an approved source value. Overrides require explicit human approval evidence when they alter an existing production brand.

## Canon role model

`color.role_model.interface_cues` maps each cue to purpose, non-color cue, and dark/light source references. `semantic.action` and `semantic.emphasis` resolve from the explicit palette choice. Other sources resolve from approved brand or canon paths. The model is shared data, not independent generator prose.

## Resolved role record

Each role record contains `id`, `label`, `source`, `hex`, `use`, and, for interface cues, `theme`, `foreground`, `foreground_contrast`, `surface`, `surface_contrast`, and `non_color_cue`. Approved identity combinations are emitted as ID references beside those records. The foreground ratio is remeasured from the resolved hex and must meet 4.5:1 for text-bearing fills. Focus and selection also retain contrast against their actual theme surface. The generated `color-roles.json` and guideline projection use this record; adapter manifests and registry guidance point to it.

## Compatibility

Historical `shruggietech-house` continues to resolve the same orange/action pair when explicitly selected. Existing semantic token names, native/web adapter colors, and registry CSS variables keep their values. A brand may select `independent` without changing its ownership, parent, endorsement, or typography mode. Cross-brand hue measurements are not approval evidence.
