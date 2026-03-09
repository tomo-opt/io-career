from io_career.models import JobRecord
from io_career.pipeline.diff import compute_daily_diff, merge_with_history


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


def test_compute_daily_diff_marks_new_records():
    records, new_rows = compute_daily_diff([mk("a"), mk("b")], [{"record_id": "a"}])
    assert len(records) == 2
    assert [r.record_id for r in new_rows] == ["b"]
    assert records[0].is_new_today is False
    assert records[1].is_new_today is True


def test_merge_with_history_keeps_old_records():
    current = [mk("a"), mk("b")]
    previous = [
        {"record_id": "a", "org_name": "Org", "job_title": "Intern", "status": "active"},
        {"record_id": "c", "org_name": "Org", "job_title": "Older Intern", "status": "active"},
    ]
    merged, new_rows = merge_with_history(current, previous)

    merged_ids = {r.record_id for r in merged}
    assert merged_ids == {"a", "b", "c"}
    assert [r.record_id for r in new_rows] == ["b"]
    c = next(r for r in merged if r.record_id == "c")
    assert c.status == "not_seen_today"
