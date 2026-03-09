from __future__ import annotations

from pathlib import Path
from typing import Dict

from io_career.pipeline.diff import merge_with_history
from io_career.pipeline.engine import CrawlEngine
from io_career.pipeline.exporters import export_archive, export_daily_new, export_latest, export_site_data, records_to_rows
from io_career.source_registry import SourceRegistry
from io_career.utils.io_utils import read_json, write_json
from io_career.utils.time_utils import bj_date_str


def run_pipeline(root: Path) -> Dict[str, object]:
    registry = SourceRegistry(root)
    sources = registry.load_all_sources()

    engine = CrawlEngine(root)
    crawled_records, errors = engine.crawl_sources(sources)

    prev = read_json(root / "data" / "processed" / "latest" / "jobs.json") or []
    records, new_records = merge_with_history(crawled_records, prev)

    write_json(root / "data" / "raw" / f"{bj_date_str()}_crawled_active_snapshot.json", records_to_rows(crawled_records))

    export_latest(root, records, errors)
    daily_fp = export_daily_new(root, new_records)
    export_archive(root, records)
    export_site_data(root, records_to_rows(records), errors)

    return {
        "source_count": len(sources),
        "active_crawled_today_count": len(crawled_records),
        "record_count": len(records),
        "new_count": len(new_records),
        "error_count": len(errors),
        "daily_new_file": str(daily_fp),
    }


def compare_latest_to_archive_today(root: Path) -> Dict[str, int]:
    from io_career.utils.time_utils import bj_date_str

    latest = read_json(root / "data" / "processed" / "latest" / "jobs.json") or []
    today_archive = read_json(root / "data" / "archive" / bj_date_str() / "jobs.json") or []

    latest_ids = {r.get("record_id") for r in latest}
    archive_ids = {r.get("record_id") for r in today_archive}

    return {
        "latest_count": len(latest_ids),
        "archive_today_count": len(archive_ids),
        "delta": len(latest_ids.symmetric_difference(archive_ids)),
    }
