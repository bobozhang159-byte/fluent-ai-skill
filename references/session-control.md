# Session control and ownership

Read this reference when ANSYS is already open, a live MCP or gRPC connector is available, or more than one automation route could control the same application.

## Choose one route

Select one controller as the sole mutation owner for the active session:

- **Managed session:** launch Workbench or Fluent from PyWorkbench/PyFluent. This is the default for reproducible unattended runs.
- **Live connected session:** attach through a supported connector using explicit connection metadata supplied by the application or connector. Probe the project, mode, version, and working directory before changing anything.
- **In-application journal:** execute a Workbench, Mechanical, SpaceClaim, Fluent, or CFX journal from the already open application when attachment is not supported.
- **Batch run:** launch `RunWB2` or a solver with a journal for deterministic non-interactive execution.

Do not let PyWorkbench, PyFluent, an MCP server, and a journal mutate the same session concurrently. A connector being reachable proves transport only; it does not prove that the expected project, model, meshing mode, or solver state is loaded.

## Live-session intake

Before mutation, record:

- ANSYS product, release, process ID when available, and solver or meshing mode
- project/case path, working directory, dirty or unsaved state, and current cell/status state
- available operations: inspect, modify, mesh, solve, query fields, export, and save
- controller route and shutdown ownership

Never replace, clear, suppress, or overwrite existing user work without explicit authorization. Prefer saving to a new project or case path. If safe attachment is unavailable, explain the limitation and offer a managed or journal-driven session instead of using blind GUI clicks.

## Shutdown and license release

Only the controller that launched a process should close it automatically. For a user-owned live session, save only to an authorized path and leave the application open unless the user asks otherwise. Confirm child solver processes terminate and licenses are released after managed or batch runs.
