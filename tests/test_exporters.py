from pathlib import Path

from io_career.models import JobRecord
from io_career.pipeline.exporters import export_daily_new


def mk(record_id: str) -> JobRecord:
    return JobRecord(
        record_id=record_id,
        org_name="Org",
        org_group="Group",
        job_title="Intern",
        job_type="Internship",
        location="NY",
        country_or_region="US",
        deadline="",
        posted_date="",
        job_url="https://example.com",
        source_url="https://example.com/source",
        source_type="official",
        summary="",
        language="en",
        scraped_at="",
        scraped_date_bj="2026-03-09",
        is_new_today=False,
        last_seen_date="2026-03-09",
        status="active",
    )


def test_export_daily_new_keeps_existing_file_when_no_new(tmp_path: Path):
    first = export_daily_new(tmp_path, [mk("a")])
    original = first.read_text(encoding="utf-8")

    second = export_daily_new(tmp_path, [])
    assert second == first
    assert second.read_text(encoding="utf-8") == original
