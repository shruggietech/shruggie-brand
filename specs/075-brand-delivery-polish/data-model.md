# S075 Data Model

Approved messages retain independent approved/absent/unresolved states, exact text, uses and provenance. Only DanceWithMe865 short_description changes state, from absent to approved; social_copy and other message approvals remain independent.

Rendered messages retain semantic role wrappers and explicit exact-value content. Optional reference labels stay separate. Canonical HTML retains one wrapper per role. Rendering emits ordered DOM continuation fragments when needed and reconstructs exact source text. Duplicate/nested canonical roles and text drift are invalid.

Alias states are undiscovered, inspected, reconciled, verified or blocked. Current state is blocked after successful zone discovery and denied DNS/rules inspection. External IDs and credentials remain private; denied inspection never authorizes overwriting unknown state.

Candidate stages are local verified, pushed/reviewed, merged, tagged and published. Each advances only with stage-specific evidence; a local commit cannot claim live completion.

A recovery receipt binds repository, published tag, original qualified run, immutable content SHA, candidate/Pages artifact IDs and digests, official release digests, and the separate deployment-controller SHA. A transported TAR retains its digest and released publication identity. Recovery states are resolved, qualified, transported, activated and live-verified; neither a transport receipt nor intermediate Pages status proves activation.
