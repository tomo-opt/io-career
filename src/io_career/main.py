from __future__ import annotations

import argparse
from pathlib import Path

from io_career.pipeline.exporters import export_site_data
from io_career.pipeline.orchestrator import compare_latest_to_archive_today, run_pipeline
from io_career.source_registry import SourceRegistry
from io_career.utils.io_utils import read_json


def cmd_run(root: Path) -> int:
    stats = run_pipeline(root)
    print("Run completed")
    for k, v in stats.items():
        print(f"- {k}: {v}")
    return 0


def cmd_validate_sources(root: Path) -> int:
    errors = SourceRegistry(root).validate()
    if errors:
        print("Source validation failed")
        for err in errors:
            print(f"- {err}")
        return 1
    print("Source validation passed")
    return 0


def cmd_export_site(root: Path) -> int:
    rows = read_json(root / "data" / "processed" / "latest" / "jobs.json") or []
    meta = read_json(root / "data" / "processed" / "latest" / "metadata.json") or {}
    export_site_data(root, rows, meta.get("errors", []))
    print("Site data exported")
    return 0


def cmd_compare(root: Path) -> int:
    stats = compare_latest_to_archive_today(root)
    print("Compare summary")
    for k, v in stats.items():
        print(f"- {k}: {v}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="io-career CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("run")
    sub.add_parser("validate-sources")
    sub.add_parser("export-site")
    sub.add_parser("compare")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(__file__).resolve().parents[2]

    if args.command == "run":
        return cmd_run(root)
    if args.command == "validate-sources":
        return cmd_validate_sources(root)
    if args.command == "export-site":
        return cmd_export_site(root)
    if args.command == "compare":
        return cmd_compare(root)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
