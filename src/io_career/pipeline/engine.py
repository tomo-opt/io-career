from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

from io_career.fetchers.http_client import HttpClient
from io_career.models import JobRecord
from io_career.parsers.common import (
    deduplicate,
    normalize_item,
    parse_oracle_ce_api,
    parse_html_links,
    parse_html_structured,
    parse_json_api,
    parse_rss,
    parse_workday_api,
)


class CrawlEngine:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.http = HttpClient()

    def crawl_sources(self, sources: List[Dict]) -> Tuple[List[JobRecord], List[str]]:
        records: List[JobRecord] = []
        errors: List[str] = []
        for source in sources:
            try:
                raw = self._crawl_one(source)
                records.extend(normalize_item(source, i) for i in raw if i.get("job_title"))
            except Exception as exc:
                if not source.get("fail_silently", False):
                    errors.append(f"{source.get('id')}: {exc}")
        return deduplicate(records), errors

    def _crawl_one(self, source: Dict) -> List[Dict]:
        strategy = source.get("strategy")
        urls = [source["source_url"]] + list(source.get("fallback_urls", []))
        last_exc: Exception | None = None
        resp = None
        for url in urls:
            try:
                if strategy == "workday_api":
                    rows = self._crawl_workday_api(source, url)
                    if rows:
                        return rows
                    resp = None
                else:
                    resp = self.http.get(url)
                    break
            except Exception as exc:
                last_exc = exc
                continue
        if strategy == "workday_api" and resp is None:
            if last_exc is None:
                return []
            raise RuntimeError(f"all source URLs failed ({last_exc})")
        if resp is None:
            raise RuntimeError(f"all source URLs failed ({last_exc})")

        if strategy == "json_api":
            return parse_json_api(source, resp.text)
        if strategy == "oracle_ce_api":
            return parse_oracle_ce_api(source, resp.text)
        if strategy == "workday_api":
            return parse_workday_api(source, resp.text)
        if strategy == "html_links":
            return parse_html_links(source, resp.text)
        if strategy == "html_structured":
            return parse_html_structured(source, resp.text)
        if strategy == "rss":
            return parse_rss(source, resp.text)
        raise ValueError(f"Unsupported strategy: {strategy}")

    def _crawl_workday_api(self, source: Dict, url: str) -> List[Dict]:
        options = source.get("options", {})
        max_items = int(options.get("max_items", 120))
        page_limit = min(int(source.get("request_payload", {}).get("limit", 20)), 20)
        offset = 0
        collected: List[Dict] = []

        while len(collected) < max_items:
            payload = {
                "appliedFacets": {},
                "limit": page_limit,
                "offset": offset,
                "searchText": "",
            }
            resp = self.http.post(url, json_payload=payload)
            batch = parse_workday_api(source, resp.text)
            if not batch:
                break
            collected.extend(batch)
            if len(batch) < page_limit:
                break
            offset += page_limit

        return collected[:max_items]
