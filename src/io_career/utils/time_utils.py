from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

try:
    BJ_TZ = ZoneInfo("Asia/Shanghai")
except ZoneInfoNotFoundError:
    BJ_TZ = timezone(timedelta(hours=8))


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def now_bj() -> datetime:
    return now_utc().astimezone(BJ_TZ)


def bj_date_str() -> str:
    return now_bj().strftime("%Y-%m-%d")


def bj_time_str() -> str:
    return now_bj().strftime("%Y-%m-%d %H:%M:%S")
