# Discover the target ANSYS installation

This reference is intentionally generic. Installation roots, license endpoints, service names, and user-specific Python paths belong to each operator's machine and must not be checked into a public repository.

## Preflight

- Identify the exact Workbench/solver release requested by the project.
- Prefer the matching `AWP_ROOT<release>` environment variable when present; otherwise ask the user to identify the installation root rather than assuming a machine-specific path.
- Confirm only the executables and Python modules needed for the requested stages. `scripts/preflight.ps1` performs presence checks; it does not prove that a product license is available.
- Test entitlement for each required module with the smallest safe checkout or setup-only operation before beginning a long unattended run.
- Select the Python environment from the installed ANSYS release or a dedicated project environment. Do not assume that the operating-system `python` command points to a compatible interpreter.
- Repeat these checks after an upgrade, repair, or installation-path change.

## Protect local configuration

Do not commit output containing license-server hostnames or ports, usernames, full installation paths, machine names, environment dumps, or raw logs. Before attaching a diagnostic report to an issue, review and redact it. A running license service is not evidence of entitlement to every ANSYS module.
