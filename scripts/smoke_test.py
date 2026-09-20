"""Launch ANSYS Workbench through PyWorkbench and verify script execution."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="242")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--show-gui", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    client_dir = run_dir / "client"
    server_dir = run_dir / "server"
    client_dir.mkdir(parents=True, exist_ok=True)
    server_dir.mkdir(parents=True, exist_ok=True)
    log_file = run_dir / "pyworkbench.log"
    journal_file = Path(__file__).with_name("workbench_smoke.wbjn")

    try:
        from ansys.workbench.core import launch_workbench
    except Exception as exc:
        print(json.dumps({"status": "error", "stage": "import", "error": str(exc)}))
        return 2

    wb = None
    try:
        wb = launch_workbench(
            version=args.version,
            show_gui=args.show_gui,
            client_workdir=str(client_dir),
            server_workdir=str(server_dir),
        )
        wb.set_log_file(str(log_file))
        result = wb.run_script_string(
            journal_file.read_text(encoding="utf-8"),
            log_level="info",
        )
        if isinstance(result, str):
            payload = json.loads(result)
        elif isinstance(result, dict):
            payload = result
        else:
            raise TypeError(
                f"Unexpected Workbench script result type: {type(result).__name__}"
            )
        payload["workbench_version"] = str(wb.server_version)
        payload["run_dir_name"] = run_dir.name
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload.get("status") == "ok" else 1
    except Exception as exc:
        print(json.dumps(
            {"status": "error", "stage": "workbench", "error": str(exc)},
            ensure_ascii=False,
        ))
        return 1
    finally:
        if wb is not None:
            try:
                wb.exit()
            except Exception as exc:
                print(json.dumps(
                    {"status": "warning", "stage": "shutdown", "error": str(exc)}
                ), file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
