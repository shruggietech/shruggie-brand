# S072 Public Messaging Contract

Only canonical messaging records may supply reusable public messages. WordPress hero descriptions and Next.js OG alternative descriptions use an approved short_description with site-metadata permission. A long description, slogan, legacy descriptor, functional descriptor, brand idea, or social-only sentence cannot fill that role automatically.

WordPress omits the entire optional description paragraph when unavailable. Next.js uses the brand title alone when no permitted description exists; otherwise its alt is title, comma, space, then the exact approved short description. Escaping must preserve string meaning in emitted TSX and HTML.

The social image itself retains separately approved social_copy and composition. Changing reusable copy does not grant permission to change that image. Existing guides retain the role/equality rules of S067; #328's cover redesign is separate.
