# End-to-end CFD workflow

Use this reference when the request spans geometry creation or import through meshing, named boundaries, Fluent/CFX setup, solution, and exported results.

## Stage gates

Each stage must emit a status and evidence path. Stop at a hard failure instead of fabricating later-stage completion.

1. **CAPABILITY:** prove that the selected controller can perform every requested stage and can save evidence. Probe the required module license through a minimal checkout or setup-only action; running license services alone is not proof of product entitlement.
2. **INTAKE:** normalize geometry dimensions, units, fluid properties, operating regime, boundary conditions, requested outputs, and acceptance criteria in a manifest.
3. **GEOMETRY:** create or import the solid/fluid domain. Save the native or neutral geometry separately. Verify body count, dimensions, volume, watertightness, shared topology/interfaces, and intended fluid regions. A successful file save is not a geometry pass: transfer it into the downstream Meshing cell, inspect the actual body/topology inventory, and reopen the saved project to confirm the link persists.
4. **SCOPING:** create semantic names such as `inlet`, `outlet`, `wall`, `symmetry`, `interface`, and `fluid`. Validate each by entity type, count, location, area, orientation, and parent body. Reject zero or ambiguous matches; never rely on transient topology IDs alone.
5. **MESH_PLAN:** select topology, element type, global size, local refinement, inflation, growth, and near-wall target from the physics and quantities of interest.
6. **MESH_GATE:** generate the mesh and record cell/node/face counts, zone inventory, worst quality values and locations, inflation achievement, disconnected regions, and scale. Apply at most two justified repair cycles. Revalidate named zones after every remesh or geometry update.
7. **SETUP:** select solver, models, materials, cell zones, boundary types and values, initialization, numerics, monitors, and requested exports. Produce a setup-only checkpoint and inventory the final boundary-zone mapping before iteration.
8. **PRE_SOLVE:** check units, reference pressure/frame, material coverage, boundary completeness, flow direction, backflow values, rotating interfaces, turbulence quantities, time step, and report definitions.
9. **SOLVE:** retain transcript, residuals, monitor histories, warnings, errors, and case/data checkpoints. Do not change physics or tolerances merely to obtain `Completed`.
10. **RESULTS:** extract the requested scalar values plus reviewable contours, vectors, streamlines, profiles, or animations. Record surface/zone scope and units for every reported value.
11. **VALIDATION:** apply mass, energy, and species balances as relevant; verify monitor stabilization, mesh/time-step sensitivity, near-wall consistency, field plausibility, and analytical/experimental comparison when available.
12. **DELIVERY:** save the Workbench project when used, geometry, mesh, named-zone inventory, setup scripts, case/data or CFX results, logs, tables, images, validation status, and a reproduction command.

## Geometry route selection

- Use SpaceClaim/Discovery scripting or PyAnsys Geometry for parameterized native construction when the required operations are supported and can be validated.
- Import STEP/Parasolid/SCDOC for complex CAD; preserve the source and perform repair on a copy.
- Use Fluent Meshing watertight/fault-tolerant workflows when they fit the CAD and boundary-layer strategy.
- Do not claim full geometry automation if the selected API can only import an already prepared fluid domain.

For a visible Workbench workflow, use [geometry-transfer.md](geometry-transfer.md) for a locally tested SpaceClaim-to-Workbench import, Meshing inspection, save, and reopen procedure. Treat it as version-scoped evidence, not as a universal limitation or guarantee for other releases.

## Retry and route changes

- On a failed stage, preserve the log and identify the failing boundary between products before editing the model.
- Allow one targeted repair for that stage. The repair must address an evidenced cause; do not rotate through SpaceClaim, DesignModeler, external meshing, standalone Fluent, and Workbench as speculative retries.
- If the targeted repair fails, stop. Explain the evidence and ask before changing a user-requested application route or control mode.
- Do not mark a stage successful from a process exit code or output-file existence alone. Require application-side evidence for the stage's expected entities or data.

## Status vocabulary

- `PASS`: the stage completed and its acceptance checks passed.
- `WARNING`: the stage completed with a documented non-fatal limitation.
- `BLOCKED`: a required input, license, connection, or user authorization is missing.
- `FAIL`: the stage ran but violated a hard numerical, physical, or evidence gate.
- `UNSUPPORTED`: the selected control route cannot perform the requested operation.

Keep stage status separate from overall engineering validity.
