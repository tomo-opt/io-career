from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml

REQUIRED_SOURCE_FIELDS = {"id", "org_name", "org_group", "source_url", "source_type", "strategy"}


class SourceRegistry:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.sources_dir = root / "sources"

    def load_all_sources(self) -> List[Dict]:
        files = [self.sources_dir / "official_sources.yaml", self.sources_dir / "aggregator_sources.yaml"]
        all_sources: List[Dict] = []
        for file in files:
            payload = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
            all_sources.extend(payload.get("sources", []))
        return all_sources

    def validate(self) -> List[str]:
        errors: List[str] = []
        seen_ids = set()
        for src in self.load_all_sources():
            missing = REQUIRED_SOURCE_FIELDS.difference(src.keys())
            if missing:
                errors.append(f"{src.get('id', '<missing-id>')}: missing fields {sorted(missing)}")
            sid = src.get("id")
            if sid in seen_ids:
                errors.append(f"duplicate source id: {sid}")
            seen_ids.add(sid)
        return errors
