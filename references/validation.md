# Simulation validation

Apply checks proportional to the model's consequence and purpose.

## Mandatory checks

1. Confirm the unit system and order of magnitude of every input.
2. Review every solver error and warning; completion alone is not validation.
3. Compare loads with reactions, accounting for inertia, symmetry, remote points, and coupled fields.
4. Inspect deformation shape for compatibility with supports and expected load paths.
5. Locate peak results and determine whether they are physical, contact-driven, or singular.
6. Check element quality and resolution in regions governing the conclusion.

## Conditional checks

- Perform mesh sensitivity when a local maximum or derived margin drives the conclusion.
- Check contact sensitivity for frictional, nonlinear, opening, or sliding interfaces.
- Check time-step or substep sensitivity for path-dependent and transient behavior.
- Compare against an analytical estimate, handbook result, experiment, or independently formulated reduced model when available.

## Status labels

- `PASS`: required checks passed and evidence was saved.
- `CONDITIONAL`: the run completed, but a stated assumption or missing comparison limits confidence.
- `FAIL`: solver, balance, units, mesh, or physics checks invalidate the conclusion.
- `NOT_ASSESSED`: insufficient inputs or evidence; never convert this to `PASS`.

Also report workflow state separately:

- `CAPABILITY_CONFIRMED`: the selected controller demonstrated the required operation.
- `SETUP_READY`: geometry, mesh, zones, physics, and requested monitors passed pre-solve review.
- `SOLVED`: the solver produced result files and no unresolved fatal error; this is not an engineering verdict.
- `VALIDATED`: the applicable numerical and physical checks passed.

Do not collapse these states into a single statement such as “the ANSYS case is complete.”
