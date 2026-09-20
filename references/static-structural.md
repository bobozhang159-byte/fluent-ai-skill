# Static structural workflow

Use this reference for ANSYS Mechanical static structural analyses.

## Required definition

- Geometry source and whether defeaturing or midsurface extraction is permitted
- Consistent unit system
- Material properties appropriate to the requested behavior, with source and temperature dependence when relevant
- Contact pairs and intended contact behavior
- Loads, constraints, preload, symmetry assumptions, and load-step history
- Requested outputs and engineering acceptance criteria

Do not infer missing constraints merely to suppress rigid-body motion. If stabilization is used for diagnosis, label its results non-final.

## Setup checks

- Confirm body count, suppressed bodies, named selections, coordinate systems, and material assignments.
- Inspect contact detection, initial penetration or gaps, and connection topology.
- Choose element order and mesh controls from geometry and expected gradients rather than a fixed global size.
- Reference loads and supports through stable named selections, not transient GUI selection IDs.

## Solve evidence

- Capture solver status, warnings, unconverged substeps, weak springs, contact status, and element-quality warnings.
- Export total deformation, relevant directional deformation, equivalent stress where meaningful, contact results when relevant, and reaction totals.
- Preserve mesh statistics and at least one image that makes the boundary conditions reviewable.

