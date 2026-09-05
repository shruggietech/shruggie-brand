import defaultComponents from "fumadocs-ui/mdx";
import type { MDXComponents } from "mdx/types";

export function getMDXComponents(components?: MDXComponents): MDXComponents {
  return {
    ...defaultComponents,
    pre: (props) => <pre tabIndex={0} {...props} />,
    table: (props) => <div className="relative overflow-auto prose-no-margin my-6" tabIndex={0}><table {...props} /></div>,
    ...components,
  };
}
