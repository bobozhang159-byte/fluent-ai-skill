# Fluent-first CFD workflow

Use this reference for Fluent and CFX simulations. Prefer Fluent plus PyFluent for new automated workflows; retain CFX when required by an existing project, model capability, or user choice.

## Required physical definition

- Fluid domain or CAD source, dimensionality, reference frame, and unit system
- Steady or transient formulation and the time scale of interest
- Incompressible, weakly compressible, or compressible behavior
- Fluid properties and their pressure or temperature dependence
- Inlet, outlet, wall, symmetry, periodic, interface, and initialization conditions
- Gravity, rotation, energy, species, radiation, porous media, multiphase, or reacting-flow models when relevant
- Quantities of interest and acceptance criteria

Do not select a turbulence, multiphase, combustion, cavitation, or radiation model merely because it is common. Tie the selection to flow regime, geometry, near-wall resolution, available inputs, and desired outputs.

## Geometry and mesh

- Verify that the fluid region is closed and that every boundary zone has an intentional, stable name.
- Validate each semantic boundary by entity type, count, area, position, and normal direction. Recheck zone names and types after every remesh; never assume CAD topology IDs remain stable.
- Check topology, interfaces, small gaps, leakage paths, and unintended disconnected volumes.
- Define the near-wall strategy before meshing: wall-resolved, wall-function, or model-specific treatment.
- Record cell count, element types, inflation layers, growth, skewness, orthogonal quality, and local refinement regions.
- Base quality acceptance on the selected solver and physics, then inspect the worst cells rather than relying only on averages.

## Setup and solve

- State the pressure- or density-based solver choice and why it fits the Mach number and physics.
- Enable the energy equation and property variation when heat transfer can affect density, viscosity, or the requested result.
- Initialize from physically meaningful values. Patch regions only when their purpose is documented.
- Define report monitors for the requested engineering quantities before iterating.
- Keep transcripts, residual histories, monitor histories, and case/data files.
- Inventory cell zones and boundary zones immediately before solving; compare the inventory with the manifest and reject missing, duplicate, or type-mismatched zones.
- On divergence, diagnose mesh, boundaries, initialization, time scale, numerics, and physical models. Do not silently loosen convergence criteria or switch models to force completion.

## Convergence and credibility

Residual reduction is necessary but not sufficient. Accept a result only after checking:

1. Relevant integral monitors such as pressure drop, mass flow, force, moment, temperature, heat rate, or species flow have stabilized or reached a repeatable transient/statistical state.
2. Global and boundary mass imbalance is acceptably small relative to through-flow; include energy and species balances when those equations are active.
3. The field is free from unphysical values, unexplained reversed flow, clipping, or boundary-condition domination.
4. Steady assumptions are credible; otherwise use transient analysis and establish time-step plus sampling independence.
5. Mesh sensitivity is assessed for quantities that drive the conclusion.
6. Near-wall resolution is consistent with the selected turbulence treatment.

## Deliverables

Save the model manifest, geometry provenance, meshing and solver journals, Workbench project when used, Fluent case/data files, transcript, residual and monitor CSV files, mesh-quality summary, balance checks, contour and vector plots, and a concise validation status.
