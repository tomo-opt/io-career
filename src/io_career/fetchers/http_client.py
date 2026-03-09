from __future__ import annotations

import time
from typing import Optional

import requests


class HttpClient:
    def __init__(self, timeout: int = 25, retries: int = 2, backoff_seconds: float = 1.5) -> None:
        self.timeout = timeout
        self.retries = retries
        self.backoff_seconds = backoff_seconds
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        })

    def get(self, url: str, params: Optional[dict] = None) -> requests.Response:
        last_err: Optional[Exception] = None
        for attempt in range(self.retries + 1):
            try:
                resp = self.session.get(url, timeout=self.timeout, params=params)
                resp.raise_for_status()
                return resp
            except Exception as exc:
                last_err = exc
                if attempt < self.retries:
                    time.sleep(self.backoff_seconds * (attempt + 1))
        raise RuntimeError(f"HTTP request failed: {url} ({last_err})") from last_err

    def post(self, url: str, json_payload: Optional[dict] = None) -> requests.Response:
        last_err: Optional[Exception] = None
        for attempt in range(self.retries + 1):
            try:
                response = self.session.post(url, timeout=self.timeout, json=json_payload)
                response.raise_for_status()
                return response
            except Exception as exc:
                last_err = exc
                if attempt < self.retries:
                    time.sleep(self.backoff_seconds * (attempt + 1))
        raise RuntimeError(f"HTTP request failed: {url} ({last_err})") from last_err
