# Workbench CFD Automation Skill

An independent Codex skill for evidence-backed CFD workflows that use Workbench, Fluent, and supported scripting interfaces. The skill covers capability checks, geometry transfer, meshing, boundary naming, setup, solving, validation, and result export.

This is a community project, not an official product. It is not affiliated with or endorsed by Ansys, Inc. No Ansys software, documentation, logo, or sample project is included. Users must provide their own installation and valid product licenses.

## Install

Copy `SKILL.md`, `agents/`, `references/`, and `scripts/` into a folder named `workbench-cfd-automation` in your Codex skills directory, then invoke it with `$workbench-cfd-automation`. The folder name and the `name` field in `SKILL.md` should match.

## Contents

- `SKILL.md`: routing and shared operating rules
- `references/`: workflow-specific guidance, including a Workbench-first geometry-transfer procedure
- `scripts/`: installation preflight, control-channel smoke test, and run-evidence completeness check

## Scope and limitations

The geometry-transfer example was exercised on one Workbench 24.2 installation. Other versions, license configurations, APIs, and model types must be checked locally. The scripts report installation or file-evidence checks; they do not prove license entitlement, convergence, or engineering validity. This skill is intended for educational and research workflows, not as a substitute for qualified review, certification, or safety-critical engineering approval.

Do not publish case files, solver data, license-server settings, installation paths, raw logs, or screenshots from a local installation without checking them for confidential or personal information.

## Names and trademarks

Ansys®, Workbench®, and Fluent® are referenced only to identify compatible products. Their names and marks belong to their respective owners. This project does not imply sponsorship, affiliation, or endorsement.

## License

Original materials in this repository are offered under the MIT License, subject to `SOURCES.md`, `THIRD_PARTY_NOTICES.md`, and applicable trademark rights. See `LICENSE`.
