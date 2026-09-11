# Documentation Footer Contract

## Documentation routes

Every exported route whose pathname begins with `/docs/` contains zero elements matching `.site-footer`. The documentation page continues to expose the applicable Fumadocs pagination destinations through `.docs-pagination`, in the established sequence from the generated documentation inventory.

The absence contract applies to the documentation index, middle articles, and the final article at desktop and narrow viewport widths. It also applies to the accessibility tree, so hiding the footer with presentation-only styling does not satisfy the contract.

## Marketing route

The homepage contains exactly one `.site-footer`. Its ordered records remain Documentation, Download Skill, Company, Source, and License. Download Skill, Source, and License retain separate-context opener isolation, while Company remains same-tab.

## Brand guideline routes

Per-brand guideline and download routes contain zero `.site-footer` elements and retain their existing dedicated guide-footer behavior.

## Regression gate

Source checks reject a documentation page that imports or renders the shared `Footer` and reject documentation-specific styling of `.site-footer`. Rendered checks reject any documentation route with `.site-footer`, any representative documentation page with missing or undersized pagination destinations, or any homepage footer-policy change.
