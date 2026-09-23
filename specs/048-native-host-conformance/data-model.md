# Data Model: Native Host Conformance

## Native role

Fields: platform, role, relative asset path, source mark variant, dimensions, appearance, alpha policy, background policy, safe content region, mask set, displayed host surface, and platform reference. Each generated artifact maps to exactly one role and one source master, though a role may have multiple sizes or themes. A role without raster capability is explicitly skipped.

## Rendered state

Fields: semantic kind (status or control), enabled state, theme, interaction state, foreground, local background, text ratio, state-cue ratio, and normative versus project threshold. Status and active-control text require at least 4.5:1. Genuinely inactive control labels retain a project 4.5:1 rule despite the normative exemption.

## Consumer selection

Fields: application identity, pinned kit version and hash, declared package resource path, actual package resource hash, matching generated path/hash, host version or theme, and attribution. States are generated, copied/pinned, packaged, and displayed. A BrandBuilder source correction does not advance the consumer state by itself.
