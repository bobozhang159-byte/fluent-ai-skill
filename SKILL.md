---
name: workbench-cfd-automation
description: Build, control, diagnose, validate, and export ANSYS CFD simulations, primarily Fluent and optionally CFX, through Workbench, PyWorkbench, PyFluent, MCP connections, and native journals. Use for end-to-end geometry-to-results workflows, live or managed sessions, meshing, named boundaries, fluid flow, heat transfer, turbulence, and parameter studies; also supports related Mechanical workflows.
---

# Workbench CFD Automation

Automate ANSYS Workbench with a Fluent-first CFD workflow while keeping model assumptions, controller ownership, execution records, and result checks auditable.

## Start safely

1. Read [references/local-installation.md](references/local-installation.md) for the target installation. Treat discovered paths and license settings as local-only data; do not commit them.
2. Run `scripts/preflight.ps1` before the first execution in a session or after an installation change.
3. Work in a new timestamped run directory. Never modify or overwrite source CAD, material data, or an existing Workbench project.
4. Prefer PyWorkbench and native Workbench journals over mouse/keyboard automation. Use GUI automation only when no supported scripting path exists, and disclose the reduced reliability.
5. Read [references/session-control.md](references/session-control.md) when ANSYS is already open, a live-session connector is available, or several control routes could address the same session. Assign exactly one controller as owner before mutating the model.
6. If the user asks to work in the Workbench desktop, launch or attach to visible Workbench first and keep it as the project/session owner. Do not silently switch to an independently opened product or an external mesh/solver route. For the locally verified Workbench 24.2 geometry workflow, follow [references/geometry-transfer.md](references/geometry-transfer.md), then revalidate it on the target release.

## Define the model

Before solving, establish the analysis type, geometry or fluid-domain source, units, material models, boundary and initial conditions, requested outputs, and acceptance criteria. Ask only for missing information that could materially change the physics. Record assumptions explicitly; never invent a boundary condition, material property, turbulence model, phase interaction, heat source, or safety limit.

For Fluent or CFX work, read [references/fluent-cfd.md](references/fluent-cfd.md). For a complete geometry-to-results request, also read [references/end-to-end-cfd.md](references/end-to-end-cfd.md). Use Fluent by default for new CFD automation unless the user, an existing project, or a required model specifically calls for CFX. For static structural work, read [references/static-structural.md](references/static-structural.md).

## Execute

1. Produce a model manifest containing inputs, assumptions, software version, controller route, intended outputs, and acceptance criteria.
2. Run a capability gate for every requested stage: geometry, meshing, naming/scoping, physics setup, solve, result extraction, and export. An installed executable or reachable server does not prove that the required operation is available.
3. Generate deterministic Workbench and solver scripts in the run directory. Use PyWorkbench for project orchestration and PyFluent, an approved MCP connector, or Fluent journals/TUI for Fluent meshing, solving, monitors, and exports.
4. Execute the gated workflow in [references/end-to-end-cfd.md](references/end-to-end-cfd.md). Perform a setup-only pass when practical, inspect messages and named-zone mapping, and then solve.
5. Retry a failed stage only once after identifying an evidence-based root cause and changing the relevant input. If that repair fails, stop and report the stage evidence; changing the requested application/control route requires user approval. Do not conceal solver divergence by weakening physical tolerances or changing the physical model.
6. Save the project, scripts, logs, tables, figures, and reproduction evidence together. Use `scripts/validate_run_evidence.py` as a filesystem completeness check; it does not establish engineering validity.

Use `scripts/smoke_test.py` to verify the PyWorkbench control channel before attempting a real model.

## Validate and report

Read [references/validation.md](references/validation.md) before accepting results. For CFD, require the fluid-specific checks in [references/fluent-cfd.md](references/fluent-cfd.md). Distinguish capability, setup, execution, numerical convergence, and engineering validity. A visible contour, saved project, or solver `Completed` state is not by itself proof of a valid result. Report failed, blocked, unsupported, or inconclusive checks alongside successful ones.
