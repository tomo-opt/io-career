from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from io_career.models import JobRecord
from io_career.utils.io_utils import ensure_dir, write_csv, write_json, write_markdown_table
from io_career.utils.time_utils import bj_date_str, bj_time_str


def records_to_rows(records: List[JobRecord]) -> List[Dict]:
    return [r.to_dict() for r in records]


def export_latest(root: Path, records: List[JobRecord], errors: List[str]) -> None:
    out = root / "data" / "processed" / "latest"
    ensure_dir(out)
    rows = records_to_rows(records)
    write_json(out / "jobs.json", rows)
    write_csv(out / "jobs.csv", rows)
    write_markdown_table(
        out / "jobs.md",
        rows,
        ["org_name", "job_title", "job_type", "location", "deadline", "job_url", "is_new_today"],
    )
    write_json(
        out / "metadata.json",
        {
            "generated_at_bj": bj_time_str(),
            "record_count": len(rows),
            "error_count": len(errors),
            "errors": errors,
        },
    )


def export_daily_new(root: Path, new_records: List[JobRecord]) -> Path:
    out = root / "data" / "processed" / "daily_new"
    ensure_dir(out)
    fp = out / f"{bj_date_str()}_new_positions.txt"
    if not new_records and fp.exists():
        return fp

    lines: List[str] = []
    for r in new_records:
        lines.extend([
            f"[Organization] {r.org_name}",
            f"[Position] {r.job_title}",
            f"[Location] {r.location}",
            f"[Deadline] {r.deadline}",
            f"[Link] {r.job_url}",
            "--------------------------------------------------",
        ])
    if not lines:
        lines = ["No new positions found today."]
    fp.write_text("\n".join(lines), encoding="utf-8")
    return fp


def export_archive(root: Path, records: List[JobRecord]) -> None:
    out = root / "data" / "archive" / bj_date_str()
    ensure_dir(out)
    write_json(out / "jobs.json", records_to_rows(records))


def export_site_data(root: Path, rows: List[Dict], errors: List[str]) -> None:
    out = root / "site" / "data"
    ensure_dir(out)
    write_json(out / "jobs.json", rows)
    write_json(out / "meta.json", {"last_update_bj": bj_time_str(), "count": len(rows), "errors": errors})
