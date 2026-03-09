from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass(slots=True)
class JobRecord:
    record_id: str
    org_name: str
    org_group: str
    job_title: str
    job_type: str
    location: str
    country_or_region: str
    deadline: str
    posted_date: str
    job_url: str
    source_url: str
    source_type: str
    summary: str
    language: str
    scraped_at: str
    scraped_date_bj: str
    is_new_today: bool
    last_seen_date: str
    status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
