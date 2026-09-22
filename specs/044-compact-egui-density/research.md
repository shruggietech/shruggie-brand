# Research: Compact egui Desktop Density

## R1. Cause of the regression

**Decision**: Treat `style.spacing.interact_size = target_minimum` as the direct cause of the oversized desktop presentation. The generated adapter currently assigns the 44-unit canon target to both axes for every runtime and density, so native switches, radio-style controls, selectors, and buttons all inherit touch sizing.

**Rationale**: The operator screenshots match the generated value: ordinary 13-to-14-point text sits inside controls approximately 44 points tall, compact density cannot reduce it, and the same global minimum affects unrelated widgets.

**Alternatives considered**: Editing ESO Weave's local style would hide the generator defect and violate the source boundary. Reducing the canonical target globally would weaken Web/React and touch behavior outside the reported desktop context.

## R2. Fine-pointer control height

**Decision**: Derive the comfortable fine-pointer height as `target minimum - 2 * pointer hit slop`, which is 28 points under the current canon, and multiply it by the existing compact density value of 0.82 for a 22.96-point compact height.

**Rationale**: Both inputs are already governed and this interpretation gives the hit-slop token an actual native purpose. The result matches the pre-regression ESO Weave style range and the user's one-line-control expectation without adding brand-specific numbers.

**Alternatives considered**: A hard-coded 22-point height would reproduce the old application value but would not trace to shared contracts. Scaling the 44-point target directly would still produce 36.08-point compact controls, which remains visibly oversized.

## R3. Conservative runtime selection

**Decision**: Use compact fine-pointer sizing only when pointer precision is explicitly fine and touch is false. Treat coarse, mixed, none, and any touch-capable profile as conservative and retain 44 points.

**Rationale**: Mixed devices can receive touch at any time, and missing precision cannot safely prove a small target is operable. Runtime capabilities already expose both fields.

**Alternatives considered**: Selecting only from density repeats the regression's missing capability distinction. Selecting fine size whenever a mouse exists would make mixed touch hardware too small.

## R4. Text scaling and padding

**Decision**: Scale text from stable theme defaults, then choose the larger of the profile target and scaled body text plus vertical padding. Derive button padding and item spacing from `spacing.control.block` with restrained ratios.

**Rationale**: A fixed compact height can clip large user text. The max rule keeps the normal state dense but grows predictably under accessibility scaling. Shared ratios make native widgets visually consistent.

**Alternatives considered**: Counter-scaling fonts violates the existing host-owned text-scale contract. Hard-coded padding would break traceability and drift from density selection.

## R5. Adapter versioning

**Decision**: Publish the correction as egui adapter 1.0.1, expand compiler-major-2 compatibility to accept 1.0.1, and advance the BrandBuilder compiler and immutable bundle identity to 2.0.1.

**Rationale**: The version policy explicitly classifies generated Rust fixes that preserve public symbols as patch changes. Consumers must be able to distinguish the corrected adapter bytes from 1.0.0, and changed generator bytes require a new immutable `bb2.0.1` bundle identity so two implementations never share one package filename.

**Alternatives considered**: Keeping 1.0.0 would give different immutable adapter bytes the same identity. A minor bump is unnecessary because no public helper or capability is added.
