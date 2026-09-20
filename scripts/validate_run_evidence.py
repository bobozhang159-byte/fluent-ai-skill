"""Check that an ANSYS automation run retained its declared evidence files.

This is a delivery-completeness check, not a solver or engineering validator.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_GROUPS = {
    "manifest": ["model_manifest.json", "manifest.json"],
    "geometry_or_mesh": ["*.scdoc", "*.scdocx", "*.dsco", "*.step", "*.stp", "*.msh", "*.msh.h5"],
    "solver_state": ["*.cas", "*.cas.h5", "*.res", "*.wbpj"],
    "solver_results": ["*.dat", "*.dat.h5", "*.res", "*.rst"],
    "transcript_or_log": ["*.trn", "*.log", "solve.out"],
    "report": ["report.md", "validation_report.md", "report.json", "validation_summary.json"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument(
        "--require",
        action="append",
        default=[],
        metavar="GLOB",
        help="Additional required glob; repeat for multiple files.",
    )
    return parser.parse_args()


def find_any(root: Path, patterns: list[str]) -> list[str]:
    matches: set[str] = set()
    for pattern in patterns:
        matches.update(str(path.relative_to(root)) for path in root.rglob(pattern) if path.is_file())
    return sorted(matches)


def main() -> int:
    args = parse_args()
    root = args.run_dir.resolve()
    if not root.is_dir():
        print(json.dumps({"status": "ERROR", "error": f"Not a directory: {root}"}, indent=2))
        return 2

    checks: dict[str, dict[str, object]] = {}
    for name, patterns in DEFAULT_GROUPS.items():
        matches = find_any(root, patterns)
        checks[name] = {"passed": bool(matches), "patterns": patterns, "matches": matches}

    for index, pattern in enumerate(args.require, start=1):
        matches = find_any(root, [pattern])
        checks[f"required_{index}"] = {"passed": bool(matches), "patterns": [pattern], "matches": matches}

    passed = all(bool(item["passed"]) for item in checks.values())
    payload = {
        "status": "PASS" if passed else "FAIL",
        "scope": "filesystem evidence completeness only",
        "run_dir_name": root.name,
        "checks": checks,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
