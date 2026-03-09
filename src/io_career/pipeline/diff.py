from __future__ import annotations

from typing import Dict, List, Tuple

from io_career.models import JobRecord
from io_career.utils.time_utils import bj_date_str


def compute_daily_diff(current: List[JobRecord], previous_rows: List[Dict]) -> Tuple[List[JobRecord], List[JobRecord]]:
    prev_ids = {str(row.get("record_id")) for row in previous_rows}
    new_records: List[JobRecord] = []
    for rec in current:
        rec.is_new_today = rec.record_id not in prev_ids
        if rec.is_new_today:
            new_records.append(rec)
    return current, new_records


def merge_with_history(current: List[JobRecord], previous_rows: List[Dict]) -> Tuple[List[JobRecord], List[JobRecord]]:
    today = bj_date_str()
    previous_map = {str(row.get("record_id")): row for row in previous_rows if row.get("record_id")}

    merged: List[JobRecord] = []
    new_records: List[JobRecord] = []

    for rec in current:
        prev = previous_map.pop(rec.record_id, None)
        rec.is_new_today = prev is None
        rec.last_seen_date = today
        rec.status = "active"
        if rec.is_new_today:
            new_records.append(rec)
        merged.append(rec)

    for row in previous_map.values():
        old = _row_to_record(row)
        old.is_new_today = False
        if not old.last_seen_date:
            old.last_seen_date = today
        if old.status == "active":
            old.status = "not_seen_today"
        merged.append(old)

    merged.sort(key=lambda r: (not r.is_new_today, r.org_name.lower(), r.job_title.lower()))
    return merged, new_records


def _row_to_record(row: Dict) -> JobRecord:
    return JobRecord(
        record_id=str(row.get("record_id", "")),
        org_name=str(row.get("org_name", "")),
        org_group=str(row.get("org_group", "")),
        job_title=str(row.get("job_title", "")),
        job_type=str(row.get("job_type", "")),
        location=str(row.get("location", "")),
        country_or_region=str(row.get("country_or_region", "")),
        deadline=str(row.get("deadline", "")),
        posted_date=str(row.get("posted_date", "")),
        job_url=str(row.get("job_url", "")),
        source_url=str(row.get("source_url", "")),
        source_type=str(row.get("source_type", "")),
        summary=str(row.get("summary", "")),
        language=str(row.get("language", "en")),
        scraped_at=str(row.get("scraped_at", "")),
        scraped_date_bj=str(row.get("scraped_date_bj", "")),
        is_new_today=bool(row.get("is_new_today", False)),
        last_seen_date=str(row.get("last_seen_date", "")),
        status=str(row.get("status", "active")),
    )
